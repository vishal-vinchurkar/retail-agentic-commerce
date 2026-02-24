import streamlit as st
import time
import random
from datetime import datetime
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data.sample_data import PRODUCTS, CUSTOMERS, AGENT_DEFINITIONS, DISTRIBUTION_CENTERS, STORES

try:
    import snowflake.connector
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False

def get_snowflake_connection():
    if not SNOWFLAKE_AVAILABLE:
        return None
    try:
        conn = snowflake.connector.connect(
            connection_name=os.getenv("SNOWFLAKE_CONNECTION_NAME", "novamart_demo")
        )
        return conn
    except Exception as e:
        return None

def call_cortex_complete(prompt: str, model: str = "claude-opus-4") -> str:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        escaped_prompt = prompt.replace("'", "''")
        sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{escaped_prompt}')"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        return None

def agentic_query_understanding(query: str) -> dict:
    query_lower = query.lower()
    
    intent_patterns = {
        'birthday': {'occasion': 'birthday', 'categories': ['Toys', 'Party Supplies'], 'terms': ['birthday party', 'party games', 'birthday decorations', 'birthday gifts']},
        'party': {'occasion': 'party', 'categories': ['Party Supplies', 'Kitchen'], 'terms': ['party supplies', 'tableware', 'decorations']},
        'christmas': {'occasion': 'christmas', 'categories': ['Toys', 'Electronics'], 'terms': ['christmas gifts', 'decorations', 'toys']},
        'gift': {'occasion': 'gift', 'categories': ['Electronics', 'Beauty', 'Toys'], 'terms': ['gifts', 'presents']},
        'baby shower': {'occasion': 'baby shower', 'categories': ['Toys', 'Baby'], 'terms': ['baby gifts', 'nursery', 'baby clothes']},
        'wedding': {'occasion': 'wedding', 'categories': ['Home & Living', 'Kitchen'], 'terms': ['home gifts', 'kitchen', 'bedding']},
        'outdoor': {'occasion': 'outdoor', 'categories': ['Outdoor', 'Sports'], 'terms': ['garden', 'outdoor furniture', 'camping']},
        'camping': {'occasion': 'camping', 'categories': ['Outdoor', 'Sports'], 'terms': ['tent', 'camping gear', 'outdoor']},
    }
    
    age_patterns = {
        'baby': 'baby', 'toddler': 'toddler', '1 year': 'baby', '2 year': 'toddler',
        '3 year': 'toddler', '4 year': 'child 3-5', '5 year': 'child 5-8', '6 year': 'child 5-8',
        '7 year': 'child 5-8', '8 year': 'child 8-12', '9 year': 'child 8-12', '10 year': 'child 8-12',
        '11 year': 'child 8-12', '12 year': 'teen', 'teen': 'teen', 'kid': 'child 5-8', 'child': 'child 5-8'
    }
    
    excluded_categories_for_kids = ['Garden', 'Planter', 'Outdoor Furniture', 'Power Tools', 'Wine', 'Alcohol', 'Office']
    
    conversational_signals = ['help me', 'planning', 'looking for', 'suggest', 'recommend', 'ideas for', 'need to', 'want to']
    is_conversational = any(sig in query_lower for sig in conversational_signals) or len(query.split()) > 5
    
    if not is_conversational:
        return {"understood": False, "original_query": query, "is_conversational": False}
    
    detected_occasion = None
    detected_age = None
    categories = []
    search_terms = []
    
    for pattern, data in intent_patterns.items():
        if pattern in query_lower:
            detected_occasion = data['occasion']
            categories.extend(data['categories'])
            search_terms.extend(data['terms'])
            break
    
    for pattern, age in age_patterns.items():
        if pattern in query_lower:
            detected_age = age
            if 'child' in age or age in ['baby', 'toddler', 'teen']:
                categories = ['Toys', 'Games', 'Party']
                search_terms = ['toys', 'board game', 'action figure', 'building blocks', 'party supplies', 'birthday']
            break
    
    if not categories:
        return {"understood": False, "original_query": query, "is_conversational": False}
    
    intro = f"I can help you find everything you need"
    if detected_occasion:
        intro += f" for your {detected_occasion}"
    if detected_age:
        intro += f" ({detected_age})"
    intro += "!"
    
    return {
        "understood": True,
        "is_conversational": True,
        "original_query": query,
        "intent": f"Shopping for {detected_occasion or 'items'}" + (f" for {detected_age}" if detected_age else ""),
        "occasion": detected_occasion,
        "age_group": detected_age,
        "product_categories": list(set(categories))[:3],
        "search_terms": list(set(search_terms))[:5],
        "suggested_response_intro": intro
    }

def is_product_relevant_for_context(product: dict, context: dict) -> bool:
    if not context or not context.get("understood"):
        return True
    
    age_group = context.get("age_group", "")
    occasion = context.get("occasion", "")
    
    product_name = product.get('name', '').lower()
    category = product.get('category', '').lower()
    subcategory = product.get('subcategory', '').lower()
    division = product.get('division', '').lower()
    
    if occasion == 'birthday' and age_group and ('child' in age_group or age_group in ['baby', 'toddler', 'teen']):
        excluded_categories = ['garden', 'outdoor', 'furniture', 'office', 'formal', 'footwear', 'shoes', 'boots', 'sneakers',
                                'women', 'men', 'bedding', 'bathroom', 'kitchen', 'automotive', 'paint', 'apparel']
        excluded_keywords = ['planter', 'lawn', 'power tool', 'wine', 'alcohol', 'drill', 'mower', 'office', 'formal',
                             'shoe', 'sneaker', 'boot', 'heel', 'sandal', 'loafer', 'slipper', 'leather shoes',
                             'dress shirt', 'mattress', 'sofa', 'couch', 'desk', 'chair', 'printer', 'monitor']
        
        for excl in excluded_categories:
            if excl in category or excl in subcategory:
                return False
        
        for excl in excluded_keywords:
            if excl in product_name:
                return False
        
        if division in ['outdoor_hardware', 'home_living', 'apparel', 'office_tech', 'health_beauty']:
            if 'toy' not in category and 'party' not in category and 'game' not in category and 'kids' not in category:
                return False
        
        good_divisions = ['toys_entertainment', 'party', 'entertainment']
        good_categories = ['toys', 'party', 'games', 'kids', 'children', 'craft', 'balloon', 'decoration', 'birthday']
        
        has_good = (
            any(gd in division for gd in good_divisions) or
            any(gc in category for gc in good_categories) or
            any(gc in subcategory for gc in good_categories) or
            any(gc in product_name for gc in ['toy', 'game', 'party', 'lego', 'doll', 'puzzle', 'craft', 'balloon', 'birthday', 'kids', 'children'])
        )
        return has_good
    
    return True

def agentic_search_products(query: str, limit: int = 4) -> tuple:
    understanding = agentic_query_understanding(query)
    
    if understanding.get("understood") and understanding.get("is_conversational"):
        search_terms = understanding.get("search_terms", [])
        
        all_products = []
        seen_skus = set()
        
        for term in search_terms[:4]:
            results = cortex_search_products(term, limit=6)
            if results:
                for p in results:
                    if p["sku"] not in seen_skus and is_product_relevant_for_context(p, understanding):
                        all_products.append(p)
                        seen_skus.add(p["sku"])
        
        if all_products:
            return (all_products[:limit], understanding)
    
    results = cortex_search_products(query, limit * 3)
    if results:
        filtered = [p for p in results if is_product_relevant_for_context(p, understanding)]
        if filtered:
            return (filtered[:limit], understanding)
    return (None, understanding)

def cortex_search_products(query: str, limit: int = 4) -> list:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        escaped_query = query.replace("'", "''")
        
        sql = f"""
        SELECT PARSE_JSON(
            SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                'NOVAMART_RETAIL.AGENTS.PRODUCT_SEARCH',
                '{{
                    "query": "{escaped_query}",
                    "columns": ["SKU", "PRODUCT_NAME", "BRAND", "DIVISION", "CATEGORY", "SUBCATEGORY", "CURRENT_PRICE", "BASE_PRICE", "TAGS"],
                    "limit": {limit}
                }}'
            )
        )['results'] as results
        """
        
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            if row and row[0]:
                results = row[0]
                products = []
                for r in results:
                    products.append({
                        "sku": r.get("SKU", ""),
                        "name": r.get("PRODUCT_NAME", ""),
                        "brand": r.get("BRAND", ""),
                        "category": r.get("CATEGORY", ""),
                        "subcategory": r.get("SUBCATEGORY", ""),
                        "division": r.get("DIVISION", ""),
                        "base_price": float(r.get("BASE_PRICE", 0)),
                        "current_price": float(r.get("CURRENT_PRICE", 0)),
                        "tags": r.get("TAGS", [])
                    })
                cursor.close()
                conn.close()
                return products if products else None
        except:
            pass
        
        sql = f"""
        SELECT SKU, PRODUCT_NAME, BRAND, CATEGORY, SUBCATEGORY, DIVISION, BASE_PRICE, CURRENT_PRICE, TAGS
        FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS
        WHERE LOWER(PRODUCT_NAME) ILIKE '%{escaped_query.lower()}%'
           OR LOWER(CATEGORY) ILIKE '%{escaped_query.lower()}%'
           OR LOWER(DIVISION) ILIKE '%{escaped_query.lower()}%'
           OR LOWER(SUBCATEGORY) ILIKE '%{escaped_query.lower()}%'
        LIMIT {limit}
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                "sku": row[0],
                "name": row[1],
                "brand": row[2],
                "category": row[3],
                "subcategory": row[4],
                "division": row[5],
                "base_price": float(row[6]),
                "current_price": float(row[7]),
                "tags": row[8] if row[8] else []
            })
        return products if products else None
    except Exception as e:
        return None

AUSTRALIAN_STATES = {
    "VIC": {"name": "Victoria", "dc": "Melbourne DC (Truganina)", "stores": ["Chadstone", "Highpoint", "Knox"]},
    "NSW": {"name": "New South Wales", "dc": "Sydney DC (Moorebank)", "stores": ["Parramatta", "Bondi", "Chatswood"]},
    "QLD": {"name": "Queensland", "dc": "Brisbane DC (Richlands)", "stores": ["Brisbane CBD", "Gold Coast", "Cairns"]},
    "WA": {"name": "Western Australia", "dc": "Perth DC (Canning Vale)", "stores": ["Perth CBD", "Fremantle"]},
    "SA": {"name": "South Australia", "dc": "Adelaide DC (Edinburgh Parks)", "stores": ["Adelaide CBD", "Glenelg"]}
}

CATEGORY_VIBES = [
    ("Home", "Furniture & decor", "home"),
    ("Electronics", "Gadgets & audio", "electronics"),
    ("Apparel", "Fashion & style", "apparel"),
    ("Outdoor", "Garden & tools", "outdoor"),
    ("Toys", "Kids & games", "toys"),
    ("Beauty", "Health & care", "beauty")
]

def search_products(query: str, limit: int = 4) -> tuple:
    products, understanding = agentic_search_products(query, limit)
    if products:
        return (products, understanding)
    
    basic_results = cortex_search_products(query, limit)
    if basic_results:
        return (basic_results, understanding)
    
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]
    scored_products = []
    
    for product in PRODUCTS:
        score = 0
        name_lower = product["name"].lower()
        category_lower = product.get("category", "").lower()
        subcategory_lower = product.get("subcategory", "").lower()
        division_lower = product.get("division", "").lower()
        tags = [t.lower() for t in product.get("tags", [])]
        
        for word in query_words:
            if word in name_lower:
                score += 10
            if word in category_lower:
                score += 8
            if word in subcategory_lower:
                score += 8
            if word in division_lower:
                score += 6
            for tag in tags:
                if word in tag:
                    score += 6
        
        if score > 0:
            scored_products.append((score, product))
    
    scored_products.sort(key=lambda x: x[0], reverse=True)
    candidates = [p[1] for p in scored_products] if scored_products else PRODUCTS
    results = [p for p in candidates if is_product_relevant_for_context(p, understanding)]
    return (results[:limit] if results else candidates[:limit], understanding)

def generate_agent_insights(products: list, customer: dict, state: str) -> dict:
    insights = {}
    state_info = AUSTRALIAN_STATES.get(state, AUSTRALIAN_STATES["VIC"])
    
    if products:
        avg_price = sum(p.get('current_price', 0) for p in products) / len(products)
        categories = list(set(p.get('category', '') for p in products if p.get('category')))
        
        insights["DEMAND_SENSING"] = f"Category demand up 23% this week in {state_info['name']}"
        insights["CUSTOMER_INTELLIGENCE"] = f"{customer['tier']} member · {customer.get('loyalty_points', 2450):,} points · Avg basket ${customer.get('avg_basket', 127):.0f}"
        insights["INVENTORY_OPTIMIZER"] = f"Stock secured at {state_info['dc']} · 3 stores have inventory"
        insights["PRICING_AGENT"] = f"Dynamic pricing: {customer['tier']} discount applied · Best price guaranteed"
        insights["FULFILLMENT_ORCHESTRATOR"] = f"Optimal route: {state_info['dc']} → {state_info['stores'][0]} (2.3km)"
        insights["LOGISTICS_OPTIMIZER"] = f"Express delivery available · Est. arrival tomorrow by 5pm"
        insights["SUPPLIER_COLLABORATION"] = f"Auto-replenishment triggered for {len(products)} SKUs"
    
    return insights

def get_product_image_url(product: dict) -> str:
    """Get a relevant Unsplash image URL based on product subcategory/category/name."""
    name = product.get('name', '').lower()
    category = product.get('category', '').lower()
    subcategory = product.get('subcategory', '').lower()
    division = product.get('division', '').lower()
    
    subcategory_images = {
        'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
        'earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop',
        'speakers': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop',
        'smartphones': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
        'phone accessories': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=300&fit=crop',
        'digital cameras': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=300&fit=crop',
        'camera accessories': 'https://images.unsplash.com/photo-1617005082133-548c4dd27f35?w=400&h=300&fit=crop',
        'consoles': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=300&fit=crop',
        'controllers': 'https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=400&h=300&fit=crop',
        'smartwatches': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop',
        'fitness trackers': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=300&fit=crop',
        'smart lighting': 'https://images.unsplash.com/photo-1558171813-4c088753af8f?w=400&h=300&fit=crop',
        'smart security': 'https://images.unsplash.com/photo-1558002038-1055907df827?w=400&h=300&fit=crop',
        'smart displays': 'https://images.unsplash.com/photo-1544428571-12d0d9d5e67a?w=400&h=300&fit=crop',
        'smart appliances': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        'action figures': 'https://images.unsplash.com/photo-1608889825103-eb5ed706fc64?w=400&h=300&fit=crop',
        'building': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop',
        'dolls': 'https://images.unsplash.com/photo-1613682988402-a12ce951f605?w=400&h=300&fit=crop',
        'vehicles': 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400&h=300&fit=crop',
        'board games': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop',
        'puzzles': 'https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=400&h=300&fit=crop',
        'video games': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=300&fit=crop',
        'craft kits': 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=400&h=300&fit=crop',
        'drawing': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=300&fit=crop',
        'decorations': 'https://images.unsplash.com/photo-1513151233558-d860c5398176?w=400&h=300&fit=crop',
        'supplies': 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=300&fit=crop',
        'tops': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
        'bottoms': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop',
        'dresses': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=300&fit=crop',
        'outerwear': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop',
        'suits': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=300&fit=crop',
        'boots': 'https://images.unsplash.com/photo-1542840410-3092f99611a3?w=400&h=300&fit=crop',
        'casual': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=300&fit=crop',
        'formal': 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=400&h=300&fit=crop',
        'sports': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
        'bags': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=300&fit=crop',
        'jewelry': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=300&fit=crop',
        'sets': 'https://images.unsplash.com/photo-1518459031867-a89b944bffe4?w=400&h=300&fit=crop',
        'boys': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&h=300&fit=crop',
        'girls': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400&h=300&fit=crop',
        'school': 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400&h=300&fit=crop',
        'clothing': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=300&fit=crop',
        'living room': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
        'bedroom': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=300&fit=crop',
        'dining': 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=400&h=300&fit=crop',
        'office': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400&h=300&fit=crop',
        'sheets': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&h=300&fit=crop',
        'pillows': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400&h=300&fit=crop',
        'quilts & doonas': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=300&fit=crop',
        'towels': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=400&h=300&fit=crop',
        'lighting': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop',
        'wall art': 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=400&h=300&fit=crop',
        'soft furnishings': 'https://images.unsplash.com/photo-1558211583-d26f610c1eb1?w=400&h=300&fit=crop',
        'cookware': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
        'cutlery': 'https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400&h=300&fit=crop',
        'dinnerware': 'https://images.unsplash.com/photo-1603199506016-5be5fbd7e1a9?w=400&h=300&fit=crop',
        'small appliances': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop',
        'containers': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400&h=300&fit=crop',
        'laptops': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
        'desktops': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=300&fit=crop',
        'tablets': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop',
        'chairs': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&h=300&fit=crop',
        'desks': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400&h=300&fit=crop',
        'work': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=300&fit=crop',
        'gaming': 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=400&h=300&fit=crop',
        'paper': 'https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400&h=300&fit=crop',
        'writing': 'https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=400&h=300&fit=crop',
        'organization': 'https://images.unsplash.com/photo-1544377193-33dcf4d68fb5?w=400&h=300&fit=crop',
        'inkjet': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400&h=300&fit=crop',
        'laser': 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400&h=300&fit=crop',
        'cables': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        'input devices': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=300&fit=crop',
        'storage': 'https://images.unsplash.com/photo-1597673030062-0a0f1a801a31?w=400&h=300&fit=crop',
        'tents': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400&h=300&fit=crop',
        'sleeping': 'https://images.unsplash.com/photo-1445308394109-4ec2920981b1?w=400&h=300&fit=crop',
        'cooking': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400&h=300&fit=crop',
        'furniture': 'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=400&h=300&fit=crop',
        'lawn care': 'https://images.unsplash.com/photo-1558904541-efa843a96f01?w=400&h=300&fit=crop',
        'pots & planters': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=300&fit=crop',
        'tools': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop',
        'watering': 'https://images.unsplash.com/photo-1563299796-17596ed6b017?w=400&h=300&fit=crop',
        'bbq': 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=300&fit=crop',
        'shade': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop',
        'ball sports': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop',
        'cycling': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&h=300&fit=crop',
        'fitness': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&h=300&fit=crop',
        'water sports': 'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=400&h=300&fit=crop',
        'hand tools': 'https://images.unsplash.com/photo-1581166397057-235af2b3c6dd?w=400&h=300&fit=crop',
        'power tools': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400&h=300&fit=crop',
        'tool storage': 'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400&h=300&fit=crop',
        'car care': 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?w=400&h=300&fit=crop',
        'face': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=300&fit=crop',
        'eyes': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop',
        'lips': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=300&fit=crop',
        'brushes': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=300&fit=crop',
        'face care': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop',
        'body care': 'https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400&h=300&fit=crop',
        'products': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400&h=300&fit=crop',
        'styling tools': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop',
        'bath & body': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400&h=300&fit=crop',
        'oral care': 'https://images.unsplash.com/photo-1559650656-5d1d361ad10e?w=400&h=300&fit=crop',
        'hair removal': 'https://images.unsplash.com/photo-1517832606299-7ae9b720a186?w=400&h=300&fit=crop',
        'first aid': 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?w=400&h=300&fit=crop',
        'wellness': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop',
        'equipment': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop',
        'supplements': 'https://images.unsplash.com/photo-1550572017-edd951b55104?w=400&h=300&fit=crop',
    }
    
    if subcategory in subcategory_images:
        return subcategory_images[subcategory]
    
    name_keywords = {
        'headphone': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
        'earbud': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop',
        'speaker': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop',
        'soundbar': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=400&h=300&fit=crop',
        'robot': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=300&fit=crop',
        'transformer': 'https://images.unsplash.com/photo-1608889825103-eb5ed706fc64?w=400&h=300&fit=crop',
        'action figure': 'https://images.unsplash.com/photo-1608889825103-eb5ed706fc64?w=400&h=300&fit=crop',
        'block': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop',
        'magnetic': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop',
        'doll': 'https://images.unsplash.com/photo-1613682988402-a12ce951f605?w=400&h=300&fit=crop',
        'dollhouse': 'https://images.unsplash.com/photo-1613682988402-a12ce951f605?w=400&h=300&fit=crop',
        'car': 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400&h=300&fit=crop',
        'train': 'https://images.unsplash.com/photo-1527190550232-6e62f5f1d95d?w=400&h=300&fit=crop',
        'trampoline': 'https://images.unsplash.com/photo-1626716493137-b67fe9501e76?w=400&h=300&fit=crop',
        'swing': 'https://images.unsplash.com/photo-1564429238814-1823aefc7cb0?w=400&h=300&fit=crop',
        'cubby': 'https://images.unsplash.com/photo-1575517111839-3a3843ee7f5d?w=400&h=300&fit=crop',
        'sandpit': 'https://images.unsplash.com/photo-1597524678053-5e6fef52d8a3?w=400&h=300&fit=crop',
        'board game': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop',
        'puzzle': 'https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=400&h=300&fit=crop',
        'laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
        'tablet': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop',
        'phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
        'camera': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=300&fit=crop',
        'watch': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop',
        'sofa': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
        'couch': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
        'chair': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&h=300&fit=crop',
        'table': 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=300&fit=crop',
        'desk': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400&h=300&fit=crop',
        'bed': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=300&fit=crop',
        'lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop',
        'shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',
        'dress': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=300&fit=crop',
        'jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop',
        'jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop',
        'pant': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=300&fit=crop',
        'shoe': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
        'sneaker': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
        'boot': 'https://images.unsplash.com/photo-1542840410-3092f99611a3?w=400&h=300&fit=crop',
        'tent': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400&h=300&fit=crop',
        'bbq': 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=300&fit=crop',
        'grill': 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=400&h=300&fit=crop',
        'bike': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&h=300&fit=crop',
        'bicycle': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&h=300&fit=crop',
        'blender': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop',
        'coffee': 'https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=400&h=300&fit=crop',
        'vacuum': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=300&fit=crop',
        'makeup': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=300&fit=crop',
        'lipstick': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=300&fit=crop',
        'mascara': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop',
        'skincare': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop',
        'serum': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=300&fit=crop',
    }
    
    for keyword, url in name_keywords.items():
        if keyword in name:
            return url
    
    division_fallbacks = {
        'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
        'toys_entertainment': 'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400&h=300&fit=crop',
        'apparel': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=400&h=300&fit=crop',
        'home_living': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400&h=300&fit=crop',
        'outdoor_hardware': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        'office_tech': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300&fit=crop',
        'health_beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=300&fit=crop',
    }
    
    if division in division_fallbacks:
        return division_fallbacks[division]
    
    return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'

def get_quick_recommendation(product: dict, context: dict) -> str:
    occasion = context.get("occasion", "") if context else ""
    age_group = context.get("age_group", "") if context else ""
    category = product.get('category', '').lower()
    name = product.get('name', '').lower()
    
    if occasion == "birthday" and age_group:
        if 'toy' in category or 'game' in category:
            return f"Perfect birthday gift for {age_group}! 🎁"
        elif 'party' in category:
            return f"Essential for the {age_group}'s party! 🎈"
        else:
            return f"Great choice for a birthday celebration!"
    elif 'headphone' in name or 'audio' in category:
        return "Top-rated audio · 4.8★ customer reviews"
    elif 'furniture' in category or 'sofa' in name:
        return "Bestseller · Ships fully assembled"
    elif 'outdoor' in category or 'garden' in category:
        return "Weather-resistant · Perfect for Aussie outdoors"
    elif 'toy' in category:
        return "Age-appropriate · Safety certified ✓"
    elif 'electronic' in category:
        return "2-year warranty included · Tech support 24/7"
    else:
        return "Popular with members like you · Fast shipping"

def get_contextual_recommendation(product: dict, context: dict, customer: dict) -> str:
    if not context or not context.get("understood"):
        return get_cortex_recommendation(product, customer)
    
    occasion = context.get("occasion", "shopping")
    age_group = context.get("age_group", "")
    
    prompt = f"""You are a helpful retail AI. The customer is planning a {occasion}{' for a ' + age_group if age_group else ''}.

Product: {product['name']}
Category: {product.get('category', 'General')}
Price: ${product['current_price']}

In ONE short sentence (max 15 words), explain why this product is perfect for their {occasion}{' for a ' + age_group if age_group else ''}. Be specific and enthusiastic."""
    
    result = call_cortex_complete(prompt)
    return result if result else f"Perfect for your {occasion}!"

def get_cortex_recommendation(product: dict, customer: dict) -> str:
    prompt = f"""You are a retail AI assistant. A {customer['tier']} tier customer is viewing:
Product: {product['name']}
Category: {product.get('category', 'General')}
Price: ${product['current_price']}

Give a brief 1-sentence personalized recommendation. Be enthusiastic but professional."""
    
    result = call_cortex_complete(prompt)
    return result if result else f"Great choice! This {product.get('category', 'item')} is popular with {customer['tier']} members."

def get_inventory_for_product(sku: str, state: str) -> dict:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        state_dc_map = {
            "NSW": "SYD-DC-01",
            "VIC": "MEL-DC-02", 
            "QLD": "BNE-DC-03",
            "WA": "PER-DC-04",
            "SA": "ADL-DC-05"
        }
        dc_id = state_dc_map.get(state, "SYD-DC-01")
        
        sql = f"""
        SELECT 
            SUM(ON_HAND_QTY) as total_on_hand,
            SUM(AVAILABLE_TO_PROMISE) as total_atp,
            COUNT(DISTINCT LOCATION_ID) as locations
        FROM NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY
        WHERE SKU = '{sku}'
        AND (LOCATION_ID = '{dc_id}' OR LOCATION_TYPE = 'STORE')
        """
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                "on_hand": int(row[0]) if row[0] else 0,
                "atp": int(row[1]) if row[1] else 0,
                "locations": int(row[2]) if row[2] else 0
            }
        return None
    except:
        return None

def get_customer_from_snowflake(customer_id: str) -> dict:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        sql = f"""
        SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, TIER, LOYALTY_POINTS, LIFETIME_VALUE, AVG_BASKET
        FROM NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS
        WHERE CUSTOMER_ID = '{customer_id}'
        """
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "name": f"{row[1]} {row[2]}",
                "tier": row[3],
                "loyalty_points": int(row[4]) if row[4] else 0,
                "lifetime_value": float(row[5]) if row[5] else 0,
                "avg_basket": float(row[6]) if row[6] else 0
            }
        return None
    except:
        return None

def call_cortex_analyst(question: str) -> dict:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        import requests
        
        token = conn.rest.token
        account = conn.account
        
        url = f"https://{account}.snowflakecomputing.com/api/v2/cortex/analyst/message"
        headers = {
            "Authorization": f'Snowflake Token="{token}"',
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"role": "user", "content": [{"type": "text", "text": question}]}],
            "semantic_model_file": "@NOVAMART_RETAIL.SEMANTIC_MODELS.MODELS_STAGE/retail_analytics.yaml"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        conn.close()
        
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

def get_snowflake_stats() -> dict:
    conn = get_snowflake_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS")
        stats["products"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS")
        stats["customers"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.CUSTOMER_360.ORDERS")
        stats["orders"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY")
        stats["inventory_records"] = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        return stats
    except:
        return None

st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #E85A4F;
        --primary-light: #FFF5F4;
        --primary-dark: #D94A3F;
        --primary-gradient: linear-gradient(135deg, #E85A4F 0%, #E96D64 50%, #F07B73 100%);
        --accent: #8E6C5A;
        --accent-light: #F5F0ED;
        --success: #2D8F6F;
        --success-light: #E8F5F0;
        --warning: #E5A84B;
        --warning-light: #FEF8EC;
        --danger: #D94A3F;
        --danger-light: #FEF2F1;
        --gray-50: #FAFAF9;
        --gray-100: #F5F5F4;
        --gray-200: #E7E5E4;
        --gray-300: #D6D3D1;
        --gray-400: #A8A29E;
        --gray-500: #78716C;
        --gray-600: #57534E;
        --gray-700: #44403C;
        --gray-800: #292524;
        --gray-900: #1C1917;
        --snowflake: #29B5E8;
        --cream: #FFFBF8;
        --warm-white: #FEFDFB;
    }
    
    * { font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp { 
        background: var(--cream);
    }
    
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { 
        background: transparent !important; 
        backdrop-filter: none !important;
        height: 0 !important;
        min-height: 0 !important;
        visibility: hidden !important;
    }
    .block-container { 
        padding: 0 2rem 1rem 2rem !important;
        padding-top: 0 !important;
        max-width: 1600px !important;
    }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
    
    .enterprise-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 28px;
        background: var(--warm-white);
        border-bottom: 1px solid var(--gray-200);
        margin: 0 -2rem 0 -2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .header-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .brand-logo {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #E85A4F 0%, #FF7B6B 50%, #FFB39C 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: -0.5px;
        box-shadow: 0 4px 16px rgba(232, 90, 79, 0.35);
        animation: float 3s ease-in-out infinite;
        font-family: 'DM Sans', sans-serif;
    }
    
    .brand-info {
        display: flex;
        flex-direction: column;
    }
    
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: var(--gray-900);
        letter-spacing: 1px;
        font-family: 'DM Sans', sans-serif;
    }
    
    .brand-subtitle {
        font-size: 12px;
        color: var(--gray-500);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 2px rgba(45, 143, 111, 0.2);
    }
    
    .status-dot.connected { background: var(--success); }
    .status-dot.disconnected { background: var(--warning); }
    
    .header-actions {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .header-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        background: var(--gray-100);
        border-radius: 20px;
        font-size: 13px;
        color: var(--gray-700);
        font-weight: 500;
    }
    
    .header-pill svg {
        width: 15px;
        height: 15px;
        stroke: var(--primary);
    }
    
    .user-menu {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 16px 8px 8px;
        background: var(--accent-light);
        border-radius: 24px;
        border: 1px solid var(--gray-200);
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        background: var(--primary-gradient);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 600;
        color: white;
    }
    
    .user-details {
        display: flex;
        flex-direction: column;
    }
    
    .user-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--gray-800);
    }
    
    .user-tier {
        font-size: 10px;
        font-weight: 600;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .page-container {
        display: grid;
        grid-template-columns: 1fr 360px;
        gap: 28px;
        margin-top: 28px;
    }
    
    .main-content {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }
    
    .sidebar-content {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .card {
        background: var(--warm-white);
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .card-header {
        padding: 18px 22px;
        border-bottom: 1px solid var(--gray-100);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: var(--gray-900);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-title svg {
        width: 18px;
        height: 18px;
        stroke: var(--primary);
    }
    
    .card-badge {
        font-size: 11px;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 20px;
        background: var(--primary-light);
        color: var(--primary);
    }
    
    .card-body {
        padding: 22px;
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, var(--primary-light) 0%, #FFF0EE 100%);
        border: none;
        border-radius: 16px;
        padding: 20px 24px;
        display: flex;
        align-items: center;
        gap: 18px;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(232, 90, 79, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .welcome-icon {
        width: 48px;
        height: 48px;
        background: var(--primary-gradient);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 12px rgba(232, 90, 79, 0.25);
    }
    
    .welcome-content h3 {
        font-size: 16px;
        font-weight: 700;
        color: var(--gray-900);
        margin: 0 0 6px 0;
    }
    
    .welcome-content p {
        font-size: 14px;
        color: var(--gray-600);
        margin: 0;
        line-height: 1.5;
    }
    
    .welcome-content strong {
        color: var(--primary);
        font-weight: 700;
    }
    
    .tier-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: var(--primary-gradient);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 8px;
        box-shadow: 0 2px 6px rgba(232, 90, 79, 0.25);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
    }
    
    .category-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px 14px;
        background: var(--warm-white);
        border: 2px solid var(--gray-200);
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .category-btn:hover {
        border-color: var(--primary);
        background: var(--primary-light);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(232, 90, 79, 0.15);
    }
    
    .category-name {
        font-size: 14px;
        font-weight: 600;
        color: var(--gray-800);
        margin-bottom: 4px;
    }
    
    .category-desc {
        font-size: 11px;
        color: var(--gray-500);
    }
    
    .products-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 18px;
    }
    
    .product-card {
        background: var(--warm-white);
        border: 2px solid var(--gray-200);
        border-radius: 16px;
        padding: 18px;
        transition: all 0.25s ease;
        animation: fadeIn 0.3s ease;
    }
    
    .product-card:hover {
        border-color: var(--primary);
        box-shadow: 0 8px 24px rgba(232, 90, 79, 0.12);
        transform: translateY(-2px);
    }
    
    .product-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 14px;
    }
    
    .product-location {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 11px;
        color: var(--gray-500);
        font-weight: 500;
    }
    
    .product-location svg {
        width: 13px;
        height: 13px;
    }
    
    .stock-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .stock-badge.in-stock {
        background: var(--success-light);
        color: var(--success);
    }
    
    .stock-badge.low-stock {
        background: var(--warning-light);
        color: var(--warning);
    }
    
    .stock-badge.out-stock {
        background: var(--danger-light);
        color: var(--danger);
    }
    
    .product-visual {
        width: 100%;
        height: 140px;
        background: linear-gradient(135deg, var(--gray-100), var(--cream));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 14px;
        overflow: hidden;
        position: relative;
    }
    
    .product-visual img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .product-card:hover .product-visual img {
        transform: scale(1.05);
    }
    
    .product-visual-icon {
        font-size: 36px;
        opacity: 0.9;
    }
    
    .product-tags {
        display: flex;
        gap: 6px;
        margin-bottom: 10px;
    }
    
    .product-tag {
        background: var(--accent-light);
        color: var(--accent);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .product-name {
        font-size: 15px;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 4px;
        line-height: 1.35;
    }
    
    .product-meta {
        font-size: 12px;
        color: var(--gray-500);
        margin-bottom: 14px;
    }
    
    .product-pricing {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
    }
    
    .price-current {
        font-size: 20px;
        font-weight: 800;
        color: var(--primary);
    }
    
    .price-original {
        font-size: 14px;
        color: var(--gray-400);
        text-decoration: line-through;
    }
    
    .discount-tag {
        background: var(--primary-light);
        color: var(--primary);
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    
    .fulfillment-info {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        background: var(--success-light);
        border-radius: 10px;
        font-size: 12px;
        color: var(--success);
        font-weight: 500;
        margin-bottom: 14px;
    }
    
    .fulfillment-info svg {
        width: 15px;
        height: 15px;
        stroke: var(--success);
    }
    
    .product-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    
    .agent-panel {
        background: var(--warm-white);
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .agent-panel-header {
        padding: 18px;
        border-bottom: 1px solid var(--gray-100);
        background: linear-gradient(135deg, var(--primary-light) 0%, #FFF0EE 100%);
    }
    
    .agent-panel-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--gray-900);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .agent-panel-subtitle {
        font-size: 12px;
        color: var(--gray-500);
        margin-top: 4px;
    }
    
    .agent-list {
        padding: 14px;
    }
    
    .agent-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        border-radius: 12px;
        margin-bottom: 6px;
        transition: all 0.2s ease;
        background: var(--gray-50);
        border: 2px solid transparent;
    }
    
    .agent-row.active {
        background: var(--primary-light);
        border-color: var(--primary);
    }
    
    .agent-row.done {
        background: var(--success-light);
        border-color: var(--success);
    }
    
    .agent-icon {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }
    
    .agent-info {
        flex: 1;
        min-width: 0;
    }
    
    .agent-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--gray-800);
    }
    
    .agent-status-text {
        font-size: 11px;
        color: var(--gray-500);
    }
    
    .agent-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .agent-badge.waiting {
        background: var(--gray-100);
        color: var(--gray-500);
    }
    
    .agent-badge.active {
        background: var(--primary-light);
        color: var(--primary);
        animation: pulse 1.5s infinite;
    }
    
    .agent-badge.done {
        background: var(--success-light);
        color: var(--success);
    }
    
    .activity-panel {
        background: var(--warm-white);
        border: 1px solid var(--gray-200);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .activity-header {
        padding: 16px 18px;
        border-bottom: 1px solid var(--gray-100);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .activity-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--gray-900);
    }
    
    .activity-list {
        max-height: 300px;
        overflow-y: auto;
        padding: 14px;
    }
    
    .activity-item {
        display: flex;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid var(--gray-100);
        animation: slideIn 0.2s ease;
    }
    
    .activity-item:last-child {
        border-bottom: none;
    }
    
    .activity-icon {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        flex-shrink: 0;
    }
    
    .activity-content {
        flex: 1;
        min-width: 0;
    }
    
    .activity-text {
        font-size: 13px;
        color: var(--gray-700);
        line-height: 1.45;
    }
    
    .activity-time {
        font-size: 11px;
        color: var(--gray-400);
        font-family: 'JetBrains Mono', monospace;
        margin-top: 3px;
    }
    
    .activity-empty {
        text-align: center;
        padding: 28px;
        color: var(--gray-400);
        font-size: 13px;
    }
    
    .ai-insight-card {
        background: linear-gradient(135deg, var(--primary-light) 0%, #FFF0EE 100%);
        border: 2px solid rgba(232, 90, 79, 0.15);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 18px;
    }
    
    .ai-insight-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .ai-insight-icon {
        width: 24px;
        height: 24px;
        background: var(--primary-gradient);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
    }
    
    .ai-insight-label {
        font-size: 11px;
        font-weight: 700;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .ai-insight-text {
        font-size: 14px;
        color: var(--gray-800);
        line-height: 1.55;
        margin-bottom: 12px;
    }
    
    .ai-insight-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .ai-tag {
        background: var(--warm-white);
        color: var(--primary);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid rgba(232, 90, 79, 0.2);
    }
    
    .footer-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        margin-top: 28px;
        border-top: 1px solid var(--gray-200);
    }
    
    .footer-text {
        font-size: 12px;
        color: var(--gray-500);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .footer-text svg {
        width: 16px;
        height: 16px;
    }
    
    .snowflake-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E0F7FA;
        color: #0097A7;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(232, 90, 79, 0.25) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(232, 90, 79, 0.35) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: var(--warm-white) !important;
        color: var(--gray-700) !important;
        border: 2px solid var(--gray-300) !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--primary-light) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Prevent button text wrapping */
    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-primary"] p,
    .stButton > button p {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    .stTextInput input {
        background: var(--warm-white) !important;
        border: 2px solid var(--gray-300) !important;
        border-radius: 12px !important;
        color: var(--gray-800) !important;
        padding: 14px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(232, 90, 79, 0.12) !important;
    }
    
    .stTextInput input::placeholder {
        color: var(--gray-400) !important;
    }
    
    .stSelectbox > div > div {
        background: var(--warm-white) !important;
        border: 2px solid var(--gray-300) !important;
        border-radius: 12px !important;
    }
    
    hr { display: none !important; }
    
    [data-testid="stDialog"] > div:first-child {
        background: var(--warm-white) !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15) !important;
    }
    
    [data-testid="stDialog"] [data-testid="stVerticalBlock"],
    [data-testid="stDialog"] [data-testid="stHorizontalBlock"],
    [data-testid="stDialog"] section[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--warm-white) !important;
    }
    
    [data-testid="stDialog"] [data-testid="stMarkdown"] p,
    [data-testid="stDialog"] [data-testid="stMarkdown"] h1,
    [data-testid="stDialog"] [data-testid="stMarkdown"] h2,
    [data-testid="stDialog"] [data-testid="stMarkdown"] h3,
    [data-testid="stDialog"] [data-testid="stMarkdown"] strong {
        color: var(--gray-900) !important;
    }
    
    [data-testid="stDialog"] [data-testid="stCaptionContainer"] {
        color: var(--gray-500) !important;
    }
    
    [data-testid="stDialog"] hr {
        border-color: var(--gray-200) !important;
        display: block !important;
    }
    
    [data-testid="stModal"] > div {
        background: var(--warm-white) !important;
    }
    
    div[data-modal-container="true"] > div {
        background: var(--warm-white) !important;
    }
    
    [role="dialog"] {
        background: var(--warm-white) !important;
    }
    
    [role="dialog"] > div {
        background: var(--warm-white) !important;
    }
    
    .completion-card {
        background: linear-gradient(135deg, var(--success-light) 0%, #C6F6D5 100%);
        border: 2px solid var(--success);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        margin-top: 28px;
    }
    
    .completion-icon {
        font-size: 44px;
        margin-bottom: 14px;
    }
    
    .completion-title {
        font-size: 20px;
        font-weight: 700;
        color: #065F46;
        margin-bottom: 6px;
    }
    
    .completion-subtitle {
        font-size: 14px;
        color: #047857;
    }
    
    .hero-search {
        background: linear-gradient(135deg, var(--primary-light) 0%, #FFE8E5 50%, #FFEEE8 100%);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-search::before {
        content: '';
        position: absolute;
        top: -100px;
        right: -100px;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(232, 90, 79, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-search::after {
        content: '';
        position: absolute;
        bottom: -50px;
        left: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(142, 108, 90, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-title {
        font-size: 26px;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 8px;
        position: relative;
    }
    
    .hero-subtitle {
        font-size: 15px;
        color: var(--gray-600);
        margin-bottom: 20px;
        position: relative;
    }
    
    .ai-recommendation {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-radius: 10px;
        margin-bottom: 12px;
        border: 1px solid #F59E0B;
    }
    
    .ai-rec-icon {
        font-size: 14px;
    }
    
    .ai-rec-text {
        font-size: 12px;
        font-weight: 600;
        color: #92400E;
        line-height: 1.3;
    }
    
    .agent-insight {
        font-size: 11px;
        color: var(--gray-600);
        margin-top: 4px;
        padding: 6px 10px;
        background: var(--gray-50);
        border-radius: 6px;
        border-left: 2px solid var(--success);
    }
    
    .cortex-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
        color: #0369A1;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-left: 6px;
    }
    

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .agent-active-glow {
        animation: agentPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes agentPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(232, 90, 79, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(232, 90, 79, 0); }
    }
    
    .micro-bounce {
        animation: microBounce 0.3s ease;
    }
    
    @keyframes microBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Device Mode Toggle */
    .device-toggle-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 10px 16px;
        background: var(--gray-100);
        border-radius: 12px;
        margin: 12px 0;
    }
    
    .device-toggle-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
        color: var(--gray-500);
    }
    
    .device-toggle-btn.active {
        background: var(--warm-white);
        color: var(--primary);
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .device-toggle-btn svg {
        width: 18px;
        height: 18px;
    }
    
    /* Mobile Preview Frame - Streamlit-compatible approach */
    .mobile-preview-frame {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 390px;
        height: 780px;
        background: var(--gray-900);
        border-radius: 50px;
        padding: 14px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.35);
        z-index: 0;
        pointer-events: none;
    }
    
    .mobile-preview-inner {
        background: transparent;
        border-radius: 40px;
        width: 100%;
        height: 100%;
        border: 3px solid var(--gray-800);
    }
    
    .mobile-notch {
        width: 130px;
        height: 32px;
        background: var(--gray-900);
        border-radius: 0 0 20px 20px;
        margin: 0 auto;
        position: relative;
        top: -3px;
    }
    
    .mobile-home-indicator {
        width: 120px;
        height: 5px;
        background: var(--gray-600);
        border-radius: 3px;
        margin: 0 auto;
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
    }
    
    /* Mobile-specific overrides - applied to body */
    body.mobile-mode-active .block-container {
        max-width: 362px !important;
        margin: 0 auto !important;
        padding: 0 8px !important;
        overflow-y: auto;
        max-height: 700px;
    }
    
    body.mobile-mode-active .stApp {
        background: #334155;
    }
    
    body.mobile-mode-active [data-testid="stMain"] {
        background: var(--cream);
        border-radius: 38px;
        max-width: 362px;
        margin: 50px auto;
        box-shadow: 0 0 0 14px var(--gray-900), 0 25px 80px rgba(0,0,0,0.35);
        padding-bottom: 60px !important;
        overflow: hidden;
    }
    
    body.mobile-mode-active .enterprise-header {
        padding: 10px 14px;
        margin: 0 -8px;
        border-radius: 38px 38px 0 0;
    }
    
    body.mobile-mode-active .brand-logo {
        width: 32px;
        height: 32px;
        font-size: 11px;
    }
    
    body.mobile-mode-active .brand-title {
        font-size: 14px;
    }
    
    body.mobile-mode-active .brand-subtitle {
        font-size: 10px;
    }
    
    body.mobile-mode-active .header-pill {
        display: none;
    }
    
    body.mobile-mode-active .user-menu {
        padding: 4px 8px 4px 4px;
    }
    
    body.mobile-mode-active .user-avatar {
        width: 26px;
        height: 26px;
        font-size: 9px;
    }
    
    body.mobile-mode-active .user-name {
        font-size: 10px;
    }
    
    body.mobile-mode-active .user-tier {
        font-size: 8px;
    }
    
    body.mobile-mode-active .welcome-banner {
        padding: 8px 10px;
        margin-bottom: 8px;
    }
    
    body.mobile-mode-active .welcome-banner h3 {
        font-size: 12px;
    }
    
    body.mobile-mode-active .welcome-banner p {
        font-size: 10px;
    }
    
    body.mobile-mode-active .product-card {
        padding: 10px;
    }
    
    body.mobile-mode-active .product-name {
        font-size: 12px;
    }
    
    body.mobile-mode-active .price-current {
        font-size: 16px;
    }
    
    body.mobile-mode-active .agent-panel,
    body.mobile-mode-active .activity-panel {
        display: none !important;
    }
    
    body.mobile-mode-active .card-title {
        font-size: 12px;
    }
    
    body.mobile-mode-active .card-header {
        padding: 10px 14px;
    }
    
    body.mobile-mode-active .ai-insight-card {
        padding: 10px;
    }
    
    body.mobile-mode-active .footer-bar {
        display: none;
    }
    
    .mobile-bottom-nav {
        display: flex;
        justify-content: space-around;
        padding: 12px 0;
        background: var(--warm-white);
        border-top: 1px solid var(--gray-200);
        position: sticky;
        bottom: 0;
    }
    
    .mobile-nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        color: var(--gray-500);
    }
    
    .mobile-nav-item.active {
        color: var(--primary);
    }
    
    .mobile-nav-item svg {
        width: 20px;
        height: 20px;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "flow_step" not in st.session_state:
    st.session_state.flow_step = 0
if "completed_agents" not in st.session_state:
    st.session_state.completed_agents = set()
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "order_id" not in st.session_state:
    st.session_state.order_id = None
if "customer" not in st.session_state:
    st.session_state.customer = CUSTOMERS[0]
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "current_products" not in st.session_state:
    st.session_state.current_products = []
if "selected_state" not in st.session_state:
    st.session_state.selected_state = "VIC"
if "show_checkout" not in st.session_state:
    st.session_state.show_checkout = False
if "ai_understanding" not in st.session_state:
    st.session_state.ai_understanding = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "show_cart" not in st.session_state:
    st.session_state.show_cart = False
if "search_context" not in st.session_state:
    st.session_state.search_context = None
if "agent_insights" not in st.session_state:
    st.session_state.agent_insights = {}
if "product_recommendations" not in st.session_state:
    st.session_state.product_recommendations = {}
if "snowflake_connected" not in st.session_state:
    conn = get_snowflake_connection()
    st.session_state.snowflake_connected = conn is not None
    if conn:
        conn.close()
if "snowflake_stats" not in st.session_state:
    st.session_state.snowflake_stats = get_snowflake_stats()
if "device_mode" not in st.session_state:
    st.session_state.device_mode = "web"


def reset_demo():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def add_activity(icon, text, bg_color="var(--primary-light)"):
    st.session_state.activity_log.insert(0, {
        "icon": icon,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S"),
        "bg": bg_color
    })
    if len(st.session_state.activity_log) > 15:
        st.session_state.activity_log.pop()

customer = st.session_state.customer
state_info = AUSTRALIAN_STATES[st.session_state.selected_state]
discount_pct = 15 if customer['tier'] == 'PLATINUM' else 10
sf_connected = st.session_state.snowflake_connected
cart_count = len(st.session_state.cart)

st.markdown(f"""
<div class="enterprise-header">
    <div class="header-brand">
        <div class="brand-logo">NM</div>
        <div class="brand-info">
            <div class="brand-title">NOVAMART</div>
            <div class="brand-subtitle">
                <span class="status-dot {'connected' if sf_connected else 'disconnected'}"></span>
                {'7 AI Agents • Snowflake Cortex' if sf_connected else 'Agentic Commerce Demo'}
            </div>
        </div>
    </div>
    <div class="header-actions">
        <div class="header-pill">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            {state_info['stores'][0]}, {st.session_state.selected_state}
        </div>
        <div class="user-menu">
            <div class="user-avatar">{customer['name'][:2].upper()}</div>
            <div class="user-details">
                <div class="user-name">{customer['name'].split()[0]}</div>
                <div class="user-tier">{customer['tier']}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Device Mode Toggle
st.markdown("""
<style>
    /* Style the device toggle radio */
    div[data-testid="stHorizontalBlock"]:has(div[data-baseweb="radio"]) {
        justify-content: center !important;
    }
    div[data-baseweb="radio"] > div {
        gap: 0 !important;
    }
    div[data-baseweb="radio"] label {
        padding: 8px 24px !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

col_device_spacer1, col_device_toggle, col_device_spacer2 = st.columns([1, 2, 1])
with col_device_toggle:
    device_mode = st.radio(
        "Device Mode",
        options=["🖥️ Web", "📱 Mobile"],
        index=0 if st.session_state.device_mode == "web" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="device_radio"
    )
    new_mode = "web" if device_mode == "🖥️ Web" else "mobile"
    if new_mode != st.session_state.device_mode:
        st.session_state.device_mode = new_mode
        st.rerun()

# Apply mobile styles based on device mode
if st.session_state.device_mode == "mobile":
    st.markdown("""
    <style>
        /* Mobile Preview Mode */
        .block-container {
            max-width: 420px !important;
            margin: 0 auto !important;
            padding: 1rem !important;
        }
        
        .enterprise-header {
            padding: 12px 16px !important;
            max-width: 400px !important;
            margin: 0 auto !important;
        }
        
        .header-pill {
            display: none !important;
        }
        
        /* Fix button text wrapping in mobile */
        [data-testid="stBaseButton-secondary"] p,
        [data-testid="stBaseButton-primary"] p {
            white-space: nowrap !important;
            font-size: 11px !important;
        }
        
        /* Category buttons - wrap to multiple rows on mobile */
        [data-testid="stHorizontalBlock"]:has([data-testid="stBaseButton-secondary"]) {
            flex-wrap: wrap !important;
            gap: 8px !important;
            justify-content: center !important;
        }
        
        [data-testid="stHorizontalBlock"]:has([data-testid="stBaseButton-secondary"]) > [data-testid="stColumn"] {
            flex: 0 0 auto !important;
            width: auto !important;
            min-width: 60px !important;
        }
        
        /* Hide agent panel in mobile */
        [data-testid="stColumn"]:has(.agent-panel),
        [data-testid="stColumn"]:has(.activity-panel) {
            display: none !important;
        }
        
        .footer-bar {
            max-width: 420px !important;
            margin: 0 auto !important;
        }
        
        /* Product cards - stack vertically on mobile */
        [data-testid="stHorizontalBlock"]:has(.product-card) {
            flex-direction: column !important;
        }
        
        [data-testid="stColumn"]:has(.product-card) {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        .product-card {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        .product-name {
            font-size: 14px !important;
        }
        
        .product-brand {
            font-size: 11px !important;
        }
        
        .ai-recommendation {
            font-size: 12px !important;
            padding: 8px 10px !important;
        }
        
        .price-current {
            font-size: 18px !important;
        }
        
        .price-original {
            font-size: 12px !important;
        }
        
        /* Cards and containers */
        .card {
            padding: 12px !important;
        }
        
        .card-header {
            padding: 10px 12px !important;
        }
        
        .card-title {
            font-size: 14px !important;
        }
        
        .welcome-banner {
            padding: 12px !important;
        }
        
        .welcome-banner h3 {
            font-size: 16px !important;
        }
        
        .welcome-banner p {
            font-size: 12px !important;
        }
        
        /* AI insight */
        .ai-insight-card {
            padding: 10px !important;
        }
        
        .ai-insight-text {
            font-size: 13px !important;
        }
    </style>
    """, unsafe_allow_html=True)

col_state, col_cart, col_spacer = st.columns([1, 0.6, 3.4])
with col_state:
    selected_state = st.selectbox(
        "Location",
        options=list(AUSTRALIAN_STATES.keys()),
        format_func=lambda x: f"{AUSTRALIAN_STATES[x]['name']}",
        key="state_selector",
        label_visibility="collapsed"
    )
    if selected_state != st.session_state.selected_state:
        st.session_state.selected_state = selected_state
        add_activity("📍", f"Location: {AUSTRALIAN_STATES[selected_state]['name']}", "var(--primary-light)")
        st.rerun()
with col_cart:
    cart_count = len(st.session_state.cart)
    cart_label = f"Cart ({cart_count})" if cart_count > 0 else "Cart"
    if st.button(cart_label, key="header_cart_btn", use_container_width=True):
        st.session_state.pending_action = "view_cart"
        st.rerun()

st.markdown(f"""
<div class="welcome-banner">
    <div class="welcome-icon">⭐</div>
    <div class="welcome-content">
        <h3>Welcome back, {customer['name'].split()[0]}!<span class="tier-badge">{customer['tier']}</span></h3>
        <p>Your <strong>{discount_pct}% member discount</strong> is automatically applied at checkout.</p>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([2.5, 1])

with col_left:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-title">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                Product Discovery
            </div>
            <div class="card-badge">AI-Powered</div>
        </div>
        <div class="card-body">
    """, unsafe_allow_html=True)
    
    cat_cols = st.columns(6)
    for idx, (name, desc, key) in enumerate(CATEGORY_VIBES):
        with cat_cols[idx]:
            if st.button(f"{name}", key=f"cat_{idx}", use_container_width=True):
                st.session_state.pending_action = "search"
                st.session_state.pending_query = key
                add_activity("🔍", f"Searching: {name}", "var(--primary-light)")
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    query = st.text_input(
        "Search", 
        key="search_input", 
        placeholder="Search products or describe what you need...",
        label_visibility="collapsed",
        value=""
    )
    if query and not st.session_state.pending_action:
        st.session_state.pending_action = "search"
        st.session_state.pending_query = query
        st.rerun()
    
    if st.session_state.current_products:
        understanding = st.session_state.ai_understanding
        products = st.session_state.current_products
        
        trend_pct = random.randint(15, 35)
        category = products[0].get('category', 'This category') if products else 'This category'
        avg_price = sum(p.get('current_price', 0) for p in products) / len(products) if products else 0
        
        if understanding and understanding.get("is_conversational"):
            intro = understanding.get("suggested_response_intro", "")
            occasion = understanding.get("occasion", "")
            age_group = understanding.get("age_group", "")
            search_terms = understanding.get("search_terms", [])
            
            tags_html = ""
            if occasion:
                tags_html += f'<span class="ai-tag">{occasion.title()}</span>'
            if age_group:
                tags_html += f'<span class="ai-tag">{age_group.title()}</span>'
            
            st.markdown(f"""
            <div class="ai-insight-card">
                <div class="ai-insight-header">
                    <div class="ai-insight-icon">AI</div>
                    <span class="ai-insight-label">Cortex AI Insight</span>
                    <span class="cortex-badge">❄️ LIVE</span>
                </div>
                <div class="ai-insight-text">{intro}</div>
                <div class="ai-insight-tags">
                    {tags_html}
                    {' '.join([f'<span class="ai-tag">{t}</span>' for t in search_terms[:3]])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-insight-card">
                <div class="ai-insight-header">
                    <div class="ai-insight-icon">📈</div>
                    <span class="ai-insight-label">Cortex Analyst</span>
                    <span class="cortex-badge">❄️ LIVE</span>
                </div>
                <div class="ai-insight-text"><strong>{category}</strong> trending +{trend_pct}% this week in {state_info['name']}. Average basket: ${avg_price:.0f}</div>
                <div class="ai-insight-tags">
                    <span class="ai-tag">📊 Real-time Analytics</span>
                    <span class="ai-tag">🎯 Personalized</span>
                    <span class="ai-tag">⚡ {len(products)} matches</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
                    Recommended Products
                </div>
            </div>
            <div class="card-body">
        """, unsafe_allow_html=True)
        
        prod_cols = st.columns(2)
        for idx, product in enumerate(st.session_state.current_products):
            with prod_cols[idx % 2]:
                final_price = product['current_price'] * (1 - discount_pct/100)
                savings = product['base_price'] - final_price
                inventory = get_inventory_for_product(product.get('sku', ''), st.session_state.selected_state)
                stock_qty = inventory['atp'] if inventory else random.randint(1, 50)
                stock_class = "in-stock" if stock_qty > 10 else "low-stock" if stock_qty > 0 else "out-stock"
                stock_text = f"{stock_qty} in stock" if stock_qty > 10 else f"Only {stock_qty} left" if stock_qty > 0 else "Out of Stock"
                
                category_tag = product.get('category', 'General')[:15].upper()
                
                product_image_url = get_product_image_url(product)
                
                ai_rec = get_quick_recommendation(product, st.session_state.search_context)
                
                st.markdown(f'''
                <div class="product-card">
                    <div class="product-header">
                        <div class="product-location">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                            {state_info['stores'][0]}
                        </div>
                        <div class="stock-badge {stock_class}">{stock_text}</div>
                    </div>
                    <div class="product-visual">
                        <img src="{product_image_url}" alt="{product['name']}" loading="lazy" />
                    </div>
                    <div class="product-tags">
                        <span class="product-tag">{category_tag}</span>
                    </div>
                    <div class="product-name">{product['name']}</div>
                    <div class="product-meta">{product['brand']} · Free delivery</div>
                    <div class="ai-recommendation">
                        <span class="ai-rec-icon">✨</span>
                        <span class="ai-rec-text">{ai_rec}</span>
                    </div>
                    <div class="product-pricing">
                        <span class="price-current">${final_price:.2f}</span>
                        <span class="price-original">${product['base_price']:.2f}</span>
                        <span class="discount-tag">-{discount_pct}%</span>
                    </div>
                    <div class="fulfillment-info">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                        Available for pickup at {state_info['stores'][0]}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("Add to Cart", key=f"cart_{idx}", use_container_width=True):
                        cart_item = {
                            "product": product,
                            "quantity": 1,
                            "final_price": final_price,
                            "context": st.session_state.search_context
                        }
                        st.session_state.cart.append(cart_item)
                        add_activity("🛒", f"Added: {product['name'][:25]}...", "var(--success-light)")
                        st.toast(f"Added to cart ({len(st.session_state.cart)} items)")
                        st.rerun()
                with btn_cols[1]:
                    if st.button("Buy Now", key=f"buy_{idx}", use_container_width=True):
                        st.session_state.selected_product = product
                        st.session_state.show_checkout = True
                        st.session_state.pending_action = "checkout"
                        add_activity("💳", f"Checkout: {product['name'][:25]}...", "var(--primary-light)")
                        st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)

with col_right:
    agent_order = [
        ("DEMAND_SENSING", "📊", "#6366F1"),
        ("CUSTOMER_INTELLIGENCE", "👤", "#8B5CF6"),
        ("INVENTORY_OPTIMIZER", "📦", "#0891B2"),
        ("PRICING_AGENT", "💰", "#059669"),
        ("FULFILLMENT_ORCHESTRATOR", "🚚", "#D97706"),
        ("LOGISTICS_OPTIMIZER", "🗺️", "#DC2626"),
        ("SUPPLIER_COLLABORATION", "🤝", "#DB2777")
    ]
    
    st.markdown("""
    <div class="agent-panel">
        <div class="agent-panel-header">
            <div class="agent-panel-title">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
                Agent Orchestration
            </div>
            <div class="agent-panel-subtitle">7 AI agents processing your requests</div>
        </div>
        <div class="agent-list">
    """, unsafe_allow_html=True)
    
    for agent_id, icon, color in agent_order:
        agent = AGENT_DEFINITIONS[agent_id]
        is_done = agent_id in st.session_state.completed_agents
        is_active = st.session_state.active_agent == agent_id
        
        row_class = "done" if is_done else "active" if is_active else ""
        badge_class = "done" if is_done else "active" if is_active else "waiting"
        badge_text = "Done" if is_done else "Running" if is_active else "Idle"
        
        insight = st.session_state.agent_insights.get(agent_id, "")
        status_text = insight if (is_done and insight) else ("Processing..." if is_active else "Waiting")
        
        st.markdown(f"""
        <div class="agent-row {row_class}">
            <div class="agent-icon" style="background: {color}20; color: {color};">{icon}</div>
            <div class="agent-info">
                <div class="agent-name">{agent['name']}</div>
                <div class="agent-status-text">{status_text}</div>
            </div>
            <div class="agent-badge {badge_class}">{badge_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="activity-panel">
        <div class="activity-header">
            <div class="activity-title">Activity Log</div>
        </div>
        <div class="activity-list">
    """, unsafe_allow_html=True)
    
    if not st.session_state.activity_log:
        st.markdown("""
        <div class="activity-empty">
            Activity will appear here as agents process requests
        </div>
        """, unsafe_allow_html=True)
    else:
        for activity in st.session_state.activity_log[:8]:
            st.markdown(f"""
            <div class="activity-item">
                <div class="activity-icon" style="background: {activity['bg']};">{activity['icon']}</div>
                <div class="activity-content">
                    <div class="activity-text">{activity['text']}</div>
                    <div class="activity-time">{activity['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

if st.session_state.pending_action == "search":
    query = st.session_state.get("pending_query", "")
    
    if st.session_state.snowflake_connected:
        add_activity("🧠", "Cortex AI analyzing intent...", "var(--primary-light)")
    
    for agent_id, icon, _ in agent_order[:4]:
        st.session_state.active_agent = agent_id
        cortex_label = " (Cortex)" if st.session_state.snowflake_connected else ""
        add_activity(icon, f"{AGENT_DEFINITIONS[agent_id]['name']}{cortex_label}", "var(--gray-100)")
        st.session_state.completed_agents.add(agent_id)
    
    st.session_state.active_agent = None
    matched_products, understanding = search_products(query, limit=4)
    
    if understanding.get("understood") and understanding.get("is_conversational"):
        intro = understanding.get("suggested_response_intro", "")
        intent = understanding.get("intent", "")
        categories = understanding.get("product_categories", [])
        occasion = understanding.get("occasion", "")
        age_group = understanding.get("age_group", "")
        
        context_parts = []
        if occasion:
            context_parts.append(occasion)
        if age_group:
            context_parts.append(age_group)
        context_str = f" ({', '.join(context_parts)})" if context_parts else ""
        
        add_activity("🎯", f"Intent: {intent[:40]}...", "var(--primary-light)")
        
        st.session_state.ai_understanding = understanding
        st.session_state.search_context = understanding
    else:
        st.session_state.ai_understanding = None
        st.session_state.search_context = None
    
    for p in matched_products:
        if 'icon' not in p:
            if 'furniture' in p.get('category', '').lower() or 'home' in p.get('division', '').lower():
                p['icon'] = '🛋️'
            elif 'electronic' in p.get('division', '').lower() or 'audio' in p.get('category', '').lower():
                p['icon'] = '🎧'
            elif 'apparel' in p.get('division', '').lower():
                p['icon'] = '👕'
            else:
                p['icon'] = '📦'
    
    st.session_state.current_products = matched_products
    st.session_state.flow_step = 1
    
    st.session_state.agent_insights = generate_agent_insights(
        matched_products, 
        st.session_state.customer, 
        st.session_state.selected_state
    )
    
    add_activity("✅", f"Found {len(matched_products)} products", "var(--success-light)")
    st.session_state.pending_action = None
    st.rerun()

elif st.session_state.pending_action == "view_cart":
    @st.dialog("Shopping Cart", width="large")
    def cart_dialog():
        if "cart" not in st.session_state:
            st.session_state.cart = []
        cart = st.session_state.cart
        if not cart:
            st.info("Your cart is empty")
            if st.button("Continue Shopping", use_container_width=True):
                st.session_state.pending_action = None
                st.rerun()
            return
        
        context = cart[0].get("context") if cart else None
        if context and context.get("understood"):
            st.markdown(f"**Shopping for:** {context.get('occasion', '')} {('(' + context.get('age_group', '') + ')') if context.get('age_group') else ''}")
            st.divider()
        
        total = 0
        for i, item in enumerate(cart):
            product = item["product"]
            price = item["final_price"]
            total += price
            
            col1, col2, col3 = st.columns([3, 1, 0.5])
            with col1:
                st.markdown(f"**{product['name'][:40]}**")
                st.caption(f"{product['brand']} · {product.get('category', '')}")
            with col2:
                st.markdown(f"**${price:.2f}**")
            with col3:
                if st.button("✕", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    add_activity("🗑️", f"Removed: {product['name'][:20]}...", "var(--danger-light)")
                    st.rerun()
        
        st.divider()
        st.markdown(f"### Total: ${total:.2f}")
        st.caption(f"{customer['tier']} discount applied · {len(cart)} items")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue Shopping", use_container_width=True):
                st.session_state.pending_action = None
                st.rerun()
        with col2:
            if st.button("Proceed to Checkout", type="primary", use_container_width=True):
                st.session_state.pending_action = "checkout_cart"
                st.rerun()
    
    cart_dialog()

elif st.session_state.pending_action == "checkout_cart":
    cart = st.session_state.cart
    if not cart:
        st.session_state.pending_action = None
        st.rerun()
    else:
        @st.dialog("Secure Checkout", width="small")
        def cart_checkout_dialog():
            cart_items = st.session_state.cart
            cart_total = sum(item["final_price"] for item in cart_items)
            
            st.caption("🔒 Secured by Afterpay • Pay in 4")
            st.divider()
            
            for item in cart_items:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{item['product']['name'][:35]}**")
                with col2:
                    st.markdown(f"${item['final_price']:.2f}")
            
            st.divider()
            st.markdown("**Payment Method**")
            st.markdown("VISA •••• 4242 · Expires 12/2027")
            st.divider()
            
            st.markdown(f"### Total: ${cart_total:.2f}")
            st.caption(f"Secure checkout · {len(cart_items)} items")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Cancel", use_container_width=True, key="checkout_cancel"):
                    st.session_state.pending_action = None
                    st.rerun()
            with col2:
                if st.button(f"Pay ${cart_total:.2f}", type="primary", use_container_width=True, key="checkout_pay"):
                    st.session_state.order_data = {
                        "cart_items": list(cart_items),
                        "cart_total": cart_total,
                        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}",
                        "tracking": f"AUS{random.randint(1000000, 9999999)}",
                        "po_id": f"PO-2026-{random.randint(80000, 89999)}"
                    }
                    st.session_state.cart = []
                    st.session_state.pending_action = "show_order_completion"
                    st.session_state.agent_animation_step = 0
                    st.rerun()
        
        cart_checkout_dialog()

elif st.session_state.pending_action == "show_order_completion":
    order_data = st.session_state.get("order_data", {})
    order_id = order_data.get("order_id", "ORD-UNKNOWN")
    tracking = order_data.get("tracking", "AUS0000000")
    po_id = order_data.get("po_id", "PO-2026-00000")
    cart_items = order_data.get("cart_items", [])
    cart_total = order_data.get("cart_total", 0)
    cart_count = len(cart_items)
    
    @st.dialog("Order Confirmed", width="large")
    def order_completion_dialog():
        all_agents = [
            ("DEMAND_SENSING", "📊", "#6366F1", "Demand patterns analyzed"),
            ("CUSTOMER_INTELLIGENCE", "👤", "#8B5CF6", "Loyalty pricing applied"),
            ("INVENTORY_OPTIMIZER", "📦", "#0891B2", "Inventory reserved"),
            ("PRICING_AGENT", "💰", "#059669", "Final price optimized"),
            ("FULFILLMENT_ORCHESTRATOR", "🚚", "#D97706", "Fulfillment center selected"),
            ("LOGISTICS_OPTIMIZER", "🗺️", "#DC2626", "Route calculated"),
            ("SUPPLIER_COLLABORATION", "🤝", "#DB2777", "Replenishment triggered")
        ]
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 16px;">✓</div>
            <div style="font-size: 20px; font-weight: 600; color: #059669; margin-bottom: 4px;">Order {order_id}</div>
            <div style="color: #6B7280; font-size: 14px;">{cart_count} item(s) · ${cart_total:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("**Agent Orchestration Complete**")
        
        for agent_id, icon, color, status in all_agents:
            st.session_state.completed_agents.add(agent_id)
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 12px; padding: 8px 12px; background: #F0FDF4; border-radius: 8px; margin-bottom: 6px; border-left: 3px solid #059669;">
                <span style="font-size: 16px;">{icon}</span>
                <div style="flex: 1;">
                    <div style="font-size: 13px; font-weight: 500; color: #1F2937;">{AGENT_DEFINITIONS[agent_id]['name']}</div>
                    <div style="font-size: 11px; color: #6B7280;">{status}</div>
                </div>
                <span style="color: #059669; font-weight: 600;">✓</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Shipping from:** {state_info['dc']}")
        with col2:
            st.markdown(f"**Tracking:** {tracking}")
        
        st.markdown(f"**Auto-replenishment:** {po_id}")
        
        st.divider()
        
        if st.button("Return to Shopping", type="primary", use_container_width=True, key="return_shopping"):
            if st.session_state.snowflake_connected:
                add_activity("❄️", "Transaction recorded to Snowflake", "var(--primary-light)")
            add_activity("✅", f"Order {order_id} confirmed", "var(--success-light)")
            add_activity("📦", f"Shipped from {state_info['dc']}", "var(--gray-100)")
            add_activity("🚚", f"Tracking: {tracking}", "var(--gray-100)")
            add_activity("🔄", f"Replenishment: {po_id}", "var(--warning-light)")
            add_activity("🎉", "Agentic flow complete", "var(--success-light)")
            st.session_state.flow_step = 5
            st.session_state.pending_action = None
            st.session_state.order_data = None
            st.session_state.current_products = []
            st.rerun()
    
    order_completion_dialog()

elif st.session_state.pending_action == "checkout":
    product = st.session_state.selected_product
    final_price = product['current_price'] * (1 - discount_pct/100)
    
    @st.dialog("Secure Checkout", width="small")
    def checkout_dialog():
        st.caption("🔒 Secured by Afterpay • Pay in 4")
        st.divider()
        
        col_prod, col_price = st.columns([3, 1])
        with col_prod:
            st.markdown(f"**{product['name'][:45]}**")
            st.caption(product['brand'])
        with col_price:
            st.markdown(f"**${final_price:.2f}**")
        
        st.divider()
        
        st.markdown("**Payment Method**")
        st.markdown("VISA •••• 4242 · Expires 12/2027")
        
        st.divider()
        
        st.markdown(f"### Total: ${final_price:.2f}")
        st.caption("Secure checkout · 1 item")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Cancel", key="dialog_cancel", use_container_width=True):
                st.session_state.show_checkout = False
                st.session_state.pending_action = None
                st.rerun()
        with btn_col2:
            if st.button(f"Pay ${final_price:.2f}", key="dialog_pay", use_container_width=True, type="primary"):
                st.session_state.show_checkout = False
                st.session_state.order_data = {
                    "cart_items": [{"product": product, "final_price": final_price}],
                    "cart_total": final_price,
                    "order_id": f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}",
                    "tracking": f"AUS{random.randint(1000000, 9999999)}",
                    "po_id": f"PO-2026-{random.randint(80000, 89999)}"
                }
                st.session_state.pending_action = "show_order_completion"
                st.rerun()
    
    checkout_dialog()

if st.session_state.flow_step >= 5:
    st.markdown("""
    <div class="completion-card">
        <div class="completion-icon">✓</div>
        <div class="completion-title">Order Complete!</div>
        <div class="completion-subtitle">All 7 AI agents executed successfully from discovery to delivery</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start New Session", key="reset_all", use_container_width=True):
        reset_demo()
        st.rerun()

sf_stats = st.session_state.get("snowflake_stats", {})
stats_text = f"{sf_stats.get('products', 0):,} Products · {sf_stats.get('customers', 0):,} Customers · {sf_stats.get('orders', 0):,} Orders" if sf_stats else ""

st.markdown(f"""
<div class="footer-bar">
    <div class="footer-text">
        <span class="snowflake-badge">❄️ Powered by Snowflake Cortex AI</span>
        <span style="margin-left: 12px; color: var(--gray-400);">Cortex Search · Cortex Complete · Cortex Analyst</span>
    </div>
    <div class="footer-text" style="font-family: 'JetBrains Mono', monospace; font-size: 11px;">{stats_text}</div>
</div>
""", unsafe_allow_html=True)
