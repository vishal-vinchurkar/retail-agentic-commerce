#!/usr/bin/env python3
import os
import sys
import json
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.sample_data import PRODUCTS, STORES, CUSTOMERS, DISTRIBUTION_CENTERS, SUPPLIERS, AGENT_DEFINITIONS, DIVISIONS

import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        connection_name=os.getenv("SNOWFLAKE_CONNECTION_NAME", "novamart_demo")
    )

def load_products(conn):
    print(f"Loading {len(PRODUCTS)} products...")
    cursor = conn.cursor()
    
    cursor.execute("TRUNCATE TABLE IF EXISTS NOVAMART_RETAIL.PRODUCT_360.PRODUCTS")
    
    for i, p in enumerate(PRODUCTS):
        tags_json = json.dumps(p.get('tags', []))
        attributes_json = json.dumps(p.get('attributes', {}))
        
        sql = f"""
        INSERT INTO NOVAMART_RETAIL.PRODUCT_360.PRODUCTS 
        (SKU, PRODUCT_NAME, DIVISION, CATEGORY, SUBCATEGORY, BRAND, SUPPLIER_ID, BASE_PRICE, CURRENT_PRICE, 
         UNIT_COST, WEIGHT_KG, CUBE_M3, LEAD_TIME_DAYS, REORDER_POINT, SAFETY_STOCK, PACK_SIZE, 
         TAGS, ATTRIBUTES, IMAGE_URL, IS_ACTIVE, CREATED_AT, UPDATED_AT)
        SELECT '{p['sku']}',
               '{p['name'].replace("'", "''")}',
               '{p['division']}',
               '{p['category']}',
               '{p['subcategory']}',
               '{p['brand'].replace("'", "''")}',
               '{p.get('supplier_id', 'SUP-001')}',
               {p['base_price']},
               {p['current_price']},
               {p['cost']},
               {p['weight_kg']},
               {p['cube_m3']},
               {p['lead_time_days']},
               {p['reorder_point']},
               {p['safety_stock']},
               {p.get('pack_size', 1)},
               PARSE_JSON('{tags_json}'),
               PARSE_JSON('{attributes_json}'),
               NULL,
               TRUE,
               CURRENT_TIMESTAMP(),
               CURRENT_TIMESTAMP()
        """
        try:
            cursor.execute(sql)
        except Exception as e:
            print(f"  Error inserting {p['sku']}: {e}")
        
        if (i + 1) % 100 == 0:
            print(f"  Loaded {i + 1}/{len(PRODUCTS)} products...")
    
    cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS")
    count = cursor.fetchone()[0]
    print(f"Total products in Snowflake: {count}")
    cursor.close()
    return count

def load_stores(conn):
    print(f"\nLoading {len(STORES)} stores...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.PRODUCT_360.STORES (
        STORE_ID VARCHAR(20) PRIMARY KEY,
        STORE_NAME VARCHAR(100),
        STATE VARCHAR(10),
        SUBURB VARCHAR(100),
        LATITUDE FLOAT,
        LONGITUDE FLOAT,
        DC_ID VARCHAR(20),
        FORMAT VARCHAR(20),
        SQM INT,
        STAFF_COUNT INT,
        CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )
    """)
    
    for store in STORES:
        cursor.execute(f"""
        INSERT INTO NOVAMART_RETAIL.PRODUCT_360.STORES 
        (STORE_ID, STORE_NAME, STATE, SUBURB, LATITUDE, LONGITUDE, DC_ID, FORMAT, SQM, STAFF_COUNT)
        SELECT '{store['id']}', '{store['name'].replace("'", "''")}', '{store['state']}', 
                '{store['suburb']}', {store['lat']}, {store['lng']}, '{store['dc']}',
                '{store['format']}', {store['sqm']}, {store['staff']}
        """)
    
    print(f"  Loaded {len(STORES)} stores")
    cursor.close()

def load_customers(conn):
    print(f"\nLoading customers...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS (
        CUSTOMER_ID VARCHAR(20) PRIMARY KEY,
        FIRST_NAME VARCHAR(50),
        LAST_NAME VARCHAR(50),
        EMAIL VARCHAR(100),
        TIER VARCHAR(20),
        LOYALTY_POINTS INT,
        LIFETIME_VALUE FLOAT,
        AVG_BASKET FLOAT,
        PURCHASE_FREQUENCY VARCHAR(20),
        PREFERRED_STORE_ID VARCHAR(20),
        PREFERRED_CHANNEL VARCHAR(20),
        SEGMENTS ARRAY,
        FREE_DELIVERY_REMAINING INT,
        CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
        LAST_ACTIVE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )
    """)
    
    for cust in CUSTOMERS:
        name_parts = cust['name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        segments_json = json.dumps(cust.get('segments', []))
        
        cursor.execute(f"""
        INSERT INTO NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS 
        (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, TIER, LOYALTY_POINTS, LIFETIME_VALUE, AVG_BASKET,
         PURCHASE_FREQUENCY, PREFERRED_STORE_ID, PREFERRED_CHANNEL, SEGMENTS, FREE_DELIVERY_REMAINING)
        SELECT '{cust['id']}', '{first_name}', '{last_name}', '{cust['email']}', '{cust['tier']}',
               {cust['loyalty_points']}, {cust['lifetime_value']}, {cust['avg_basket']},
               '{cust['purchase_frequency']}', '{cust['preferred_store']}', '{cust['preferred_channel']}',
               PARSE_JSON('{segments_json}'), {cust.get('free_delivery_remaining', 0)}
        """)
    
    more_customers = generate_more_customers(100)
    for cust in more_customers:
        segments_json = json.dumps(cust.get('segments', []))
        cursor.execute(f"""
        INSERT INTO NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS 
        (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, TIER, LOYALTY_POINTS, LIFETIME_VALUE, AVG_BASKET,
         PURCHASE_FREQUENCY, PREFERRED_STORE_ID, PREFERRED_CHANNEL, SEGMENTS, FREE_DELIVERY_REMAINING)
        SELECT '{cust['id']}', '{cust['first_name']}', '{cust['last_name']}', '{cust['email']}', '{cust['tier']}',
               {cust['loyalty_points']}, {cust['lifetime_value']}, {cust['avg_basket']},
               '{cust['purchase_frequency']}', '{cust['preferred_store']}', '{cust['preferred_channel']}',
               PARSE_JSON('{segments_json}'), {cust.get('free_delivery_remaining', 0)}
        """)
    
    cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS")
    count = cursor.fetchone()[0]
    print(f"  Loaded {count} customers")
    cursor.close()

def generate_more_customers(count):
    first_names = ["Liam", "Noah", "Oliver", "Elijah", "William", "James", "Benjamin", "Lucas", "Henry", "Alexander",
                   "Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella", "Mia", "Evelyn", "Harper", "Luna",
                   "Michael", "Daniel", "Matthew", "Joseph", "David", "Emily", "Madison", "Elizabeth", "Victoria", "Grace"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    tiers = ["BRONZE", "SILVER", "GOLD", "PLATINUM"]
    tier_weights = [0.4, 0.35, 0.2, 0.05]
    frequencies = ["monthly", "fortnightly", "weekly", "occasional"]
    channels = ["online", "in-store", "omni"]
    segments_options = ["price-conscious", "tech-enthusiast", "home-decorator", "fashion-forward", "outdoor-lover", 
                        "family-focused", "health-conscious", "premium-buyer", "bargain-hunter", "loyal"]
    
    customers = []
    for i in range(count):
        tier = random.choices(tiers, weights=tier_weights)[0]
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        loyalty_multiplier = {"BRONZE": 1, "SILVER": 3, "GOLD": 8, "PLATINUM": 20}[tier]
        
        cust = {
            "id": f"CUST-{10000 + i:05d}",
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{random.randint(1,999)}@email.com",
            "tier": tier,
            "loyalty_points": random.randint(100, 5000) * loyalty_multiplier,
            "lifetime_value": round(random.uniform(200, 2000) * loyalty_multiplier, 2),
            "avg_basket": round(random.uniform(50, 150) * (1 + loyalty_multiplier * 0.1), 2),
            "purchase_frequency": random.choice(frequencies),
            "preferred_store": random.choice([s['id'] for s in STORES]),
            "preferred_channel": random.choice(channels),
            "segments": random.sample(segments_options, k=random.randint(1, 3)),
            "free_delivery_remaining": random.randint(0, 5) * (1 if tier in ["GOLD", "PLATINUM"] else 0)
        }
        customers.append(cust)
    
    return customers

def load_inventory(conn):
    print("\nGenerating inventory data...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY (
        SKU VARCHAR(30),
        LOCATION_ID VARCHAR(20),
        LOCATION_TYPE VARCHAR(10),
        ON_HAND_QTY INT,
        ALLOCATED_QTY INT,
        IN_TRANSIT_QTY INT,
        AVAILABLE_TO_PROMISE INT,
        LAST_RECEIPT_DATE DATE,
        LAST_SOLD_DATE DATE,
        DAYS_OF_SUPPLY INT,
        UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
        PRIMARY KEY (SKU, LOCATION_ID)
    )
    """)
    
    cursor.execute("SELECT SKU FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS")
    skus = [row[0] for row in cursor.fetchall()]
    
    if not skus:
        print("  No products found, skipping inventory")
        cursor.close()
        return
    
    dc_ids = ["SYD-DC-01", "MEL-DC-02", "BNE-DC-03", "PER-DC-04", "ADL-DC-05"]
    store_ids = [s['id'] for s in STORES]
    
    total_rows = 0
    
    for sku in skus:
        for dc in random.sample(dc_ids, k=random.randint(2, 5)):
            on_hand = random.randint(50, 500)
            allocated = random.randint(5, int(on_hand * 0.3))
            in_transit = random.randint(0, 200)
            atp = on_hand - allocated + in_transit
            days_supply = random.randint(10, 90)
            last_receipt = random.randint(1, 30)
            last_sold = random.randint(0, 7)
            
            cursor.execute(f"""
            INSERT INTO NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY 
            (SKU, LOCATION_ID, LOCATION_TYPE, ON_HAND_QTY, ALLOCATED_QTY, IN_TRANSIT_QTY, AVAILABLE_TO_PROMISE, 
             LAST_RECEIPT_DATE, LAST_SOLD_DATE, DAYS_OF_SUPPLY)
            SELECT '{sku}', '{dc}', 'DC', {on_hand}, {allocated}, {in_transit}, {atp}, 
                   DATEADD(day, -{last_receipt}, CURRENT_DATE()), DATEADD(day, -{last_sold}, CURRENT_DATE()), {days_supply}
            """)
            total_rows += 1
        
        for store in random.sample(store_ids, k=random.randint(5, 12)):
            on_hand = random.randint(2, 50)
            allocated = random.randint(0, int(on_hand * 0.2))
            in_transit = random.randint(0, 20)
            atp = on_hand - allocated + in_transit
            days_supply = random.randint(3, 30)
            last_receipt = random.randint(1, 14)
            last_sold = random.randint(0, 3)
            
            cursor.execute(f"""
            INSERT INTO NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY 
            (SKU, LOCATION_ID, LOCATION_TYPE, ON_HAND_QTY, ALLOCATED_QTY, IN_TRANSIT_QTY, AVAILABLE_TO_PROMISE, 
             LAST_RECEIPT_DATE, LAST_SOLD_DATE, DAYS_OF_SUPPLY)
            SELECT '{sku}', '{store}', 'STORE', {on_hand}, {allocated}, {in_transit}, {atp}, 
                   DATEADD(day, -{last_receipt}, CURRENT_DATE()), DATEADD(day, -{last_sold}, CURRENT_DATE()), {days_supply}
            """)
            total_rows += 1
        
        if total_rows % 1000 == 0:
            print(f"  Loaded {total_rows} inventory records...")
    
    cursor.execute("SELECT COUNT(*) FROM NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY")
    count = cursor.fetchone()[0]
    print(f"  Total inventory records: {count}")
    cursor.close()

def load_orders(conn):
    print("\nGenerating order history...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.CUSTOMER_360.ORDERS (
        ORDER_ID VARCHAR(20) PRIMARY KEY,
        CUSTOMER_ID VARCHAR(20),
        ORDER_DATE TIMESTAMP_NTZ,
        CHANNEL VARCHAR(20),
        STORE_ID VARCHAR(20),
        STATUS VARCHAR(20),
        SUBTOTAL FLOAT,
        DISCOUNT FLOAT,
        SHIPPING FLOAT,
        TAX FLOAT,
        TOTAL FLOAT,
        PAYMENT_METHOD VARCHAR(30),
        DELIVERY_METHOD VARCHAR(30),
        CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )
    """)
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.CUSTOMER_360.ORDER_ITEMS (
        ORDER_ITEM_ID VARCHAR(30) PRIMARY KEY,
        ORDER_ID VARCHAR(20),
        SKU VARCHAR(30),
        QUANTITY INT,
        UNIT_PRICE FLOAT,
        DISCOUNT_AMOUNT FLOAT,
        LINE_TOTAL FLOAT
    )
    """)
    
    cursor.execute("SELECT CUSTOMER_ID FROM NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT SKU, CURRENT_PRICE FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS")
    products = [(row[0], row[1]) for row in cursor.fetchall()]
    
    if not products:
        print("  No products found, skipping orders")
        cursor.close()
        return
    
    statuses = ["DELIVERED", "DELIVERED", "DELIVERED", "SHIPPED", "PROCESSING", "CANCELLED"]
    channels = ["online", "in-store", "click-collect"]
    payment_methods = ["credit_card", "debit_card", "afterpay", "paypal", "gift_card"]
    delivery_methods = ["standard", "express", "click-collect", "in-store"]
    
    order_count = 0
    item_count = 0
    
    for i in range(2000):
        order_id = f"ORD-{100000 + i:06d}"
        customer_id = random.choice(customer_ids)
        order_date = datetime.now() - timedelta(days=random.randint(0, 365))
        channel = random.choice(channels)
        store_id = random.choice([s['id'] for s in STORES]) if channel != "online" else None
        status = random.choice(statuses)
        
        num_items = random.randint(1, 6)
        order_products = random.sample(products, k=min(num_items, len(products)))
        
        subtotal = 0
        items_data = []
        for j, (sku, price) in enumerate(order_products):
            qty = random.randint(1, 3)
            discount = round(price * random.uniform(0, 0.15), 2) if random.random() > 0.7 else 0
            line_total = round((price - discount) * qty, 2)
            subtotal += line_total
            
            item_id = f"{order_id}-{j+1:02d}"
            items_data.append((item_id, order_id, sku, qty, price, discount, line_total))
            item_count += 1
        
        discount = round(subtotal * random.uniform(0, 0.1), 2) if random.random() > 0.6 else 0
        shipping = 0 if channel == "in-store" else (0 if subtotal > 100 else round(random.uniform(5, 15), 2))
        tax = round((subtotal - discount + shipping) * 0.1, 2)
        total = round(subtotal - discount + shipping + tax, 2)
        
        store_val = f"'{store_id}'" if store_id else "NULL"
        cursor.execute(f"""
        INSERT INTO NOVAMART_RETAIL.CUSTOMER_360.ORDERS 
        (ORDER_ID, CUSTOMER_ID, ORDER_DATE, CHANNEL, STORE_ID, STATUS, SUBTOTAL, DISCOUNT, SHIPPING, TAX, TOTAL, PAYMENT_METHOD, DELIVERY_METHOD)
        SELECT '{order_id}', '{customer_id}', '{order_date.strftime('%Y-%m-%d %H:%M:%S')}', '{channel}', {store_val}, 
                '{status}', {subtotal}, {discount}, {shipping}, {tax}, {total}, 
                '{random.choice(payment_methods)}', '{random.choice(delivery_methods)}'
        """)
        order_count += 1
        
        for item in items_data:
            cursor.execute(f"""
            INSERT INTO NOVAMART_RETAIL.CUSTOMER_360.ORDER_ITEMS 
            (ORDER_ITEM_ID, ORDER_ID, SKU, QUANTITY, UNIT_PRICE, DISCOUNT_AMOUNT, LINE_TOTAL)
            SELECT '{item[0]}', '{item[1]}', '{item[2]}', {item[3]}, {item[4]}, {item[5]}, {item[6]}
            """)
        
        if order_count % 200 == 0:
            print(f"  Generated {order_count} orders, {item_count} items...")
    
    print(f"  Total orders: {order_count}, items: {item_count}")
    cursor.close()

def load_agent_definitions(conn):
    print("\nLoading agent definitions...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE TABLE NOVAMART_RETAIL.AGENTS.AGENT_REGISTRY (
        AGENT_ID VARCHAR(50) PRIMARY KEY,
        AGENT_NAME VARCHAR(100),
        ICON VARCHAR(10),
        COLOR VARCHAR(20),
        CAPABILITIES ARRAY,
        DATA_SOURCES ARRAY,
        OUTPUT_TYPE VARCHAR(100),
        IS_ACTIVE BOOLEAN DEFAULT TRUE,
        CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )
    """)
    
    for agent_id, agent in AGENT_DEFINITIONS.items():
        caps_json = json.dumps(agent['capabilities'])
        sources_json = json.dumps(agent['data_sources'])
        
        cursor.execute(f"""
        INSERT INTO NOVAMART_RETAIL.AGENTS.AGENT_REGISTRY 
        (AGENT_ID, AGENT_NAME, ICON, COLOR, CAPABILITIES, DATA_SOURCES, OUTPUT_TYPE)
        SELECT '{agent_id}', '{agent['name']}', '{agent['icon']}', '{agent['color']}',
               PARSE_JSON('{caps_json}'), PARSE_JSON('{sources_json}'), '{agent['output']}'
        """)
    
    print(f"  Loaded {len(AGENT_DEFINITIONS)} agent definitions")
    cursor.close()

def create_views(conn):
    print("\nCreating analytics views...")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE OR REPLACE VIEW NOVAMART_RETAIL.ANALYTICS.PRODUCT_INVENTORY_SUMMARY AS
    SELECT 
        p.SKU,
        p.PRODUCT_NAME,
        p.DIVISION,
        p.CATEGORY,
        p.BRAND,
        p.CURRENT_PRICE,
        p.BASE_PRICE,
        ROUND((p.BASE_PRICE - p.CURRENT_PRICE) / NULLIF(p.BASE_PRICE, 0) * 100, 1) AS DISCOUNT_PCT,
        SUM(CASE WHEN i.LOCATION_TYPE = 'DC' THEN i.ON_HAND_QTY ELSE 0 END) AS DC_ON_HAND,
        SUM(CASE WHEN i.LOCATION_TYPE = 'STORE' THEN i.ON_HAND_QTY ELSE 0 END) AS STORE_ON_HAND,
        SUM(i.AVAILABLE_TO_PROMISE) AS TOTAL_ATP,
        COUNT(DISTINCT CASE WHEN i.LOCATION_TYPE = 'STORE' THEN i.LOCATION_ID END) AS STORES_WITH_STOCK
    FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS p
    LEFT JOIN NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY i ON p.SKU = i.SKU
    GROUP BY p.SKU, p.PRODUCT_NAME, p.DIVISION, p.CATEGORY, p.BRAND, p.CURRENT_PRICE, p.BASE_PRICE
    """)
    
    cursor.execute("""
    CREATE OR REPLACE VIEW NOVAMART_RETAIL.ANALYTICS.SALES_BY_CATEGORY AS
    SELECT 
        p.DIVISION,
        p.CATEGORY,
        DATE_TRUNC('month', o.ORDER_DATE) AS MONTH,
        COUNT(DISTINCT o.ORDER_ID) AS ORDER_COUNT,
        SUM(oi.QUANTITY) AS UNITS_SOLD,
        SUM(oi.LINE_TOTAL) AS REVENUE,
        AVG(oi.LINE_TOTAL) AS AVG_LINE_VALUE
    FROM NOVAMART_RETAIL.CUSTOMER_360.ORDER_ITEMS oi
    JOIN NOVAMART_RETAIL.CUSTOMER_360.ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN NOVAMART_RETAIL.PRODUCT_360.PRODUCTS p ON oi.SKU = p.SKU
    WHERE o.STATUS != 'CANCELLED'
    GROUP BY p.DIVISION, p.CATEGORY, DATE_TRUNC('month', o.ORDER_DATE)
    """)
    
    cursor.execute("""
    CREATE OR REPLACE VIEW NOVAMART_RETAIL.ANALYTICS.CUSTOMER_SEGMENTS AS
    SELECT 
        c.TIER,
        COUNT(*) AS CUSTOMER_COUNT,
        AVG(c.LIFETIME_VALUE) AS AVG_LTV,
        AVG(c.AVG_BASKET) AS AVG_BASKET,
        AVG(c.LOYALTY_POINTS) AS AVG_POINTS,
        SUM(CASE WHEN c.PREFERRED_CHANNEL = 'online' THEN 1 ELSE 0 END) AS ONLINE_PREFERRED,
        SUM(CASE WHEN c.PREFERRED_CHANNEL = 'in-store' THEN 1 ELSE 0 END) AS INSTORE_PREFERRED,
        SUM(CASE WHEN c.PREFERRED_CHANNEL = 'omni' THEN 1 ELSE 0 END) AS OMNI_PREFERRED
    FROM NOVAMART_RETAIL.CUSTOMER_360.CUSTOMERS c
    GROUP BY c.TIER
    """)
    
    cursor.execute("""
    CREATE OR REPLACE VIEW NOVAMART_RETAIL.ANALYTICS.DC_PERFORMANCE AS
    SELECT 
        dc.DC_ID,
        dc.DC_NAME,
        dc.STATE,
        dc.CAPACITY_PALLETS,
        dc.DAILY_THROUGHPUT,
        dc.STORES_SERVED,
        COUNT(DISTINCT i.SKU) AS UNIQUE_SKUS,
        SUM(i.ON_HAND_QTY) AS TOTAL_ON_HAND,
        SUM(i.IN_TRANSIT_QTY) AS TOTAL_IN_TRANSIT,
        SUM(i.AVAILABLE_TO_PROMISE) AS TOTAL_ATP
    FROM NOVAMART_RETAIL.SUPPLY_CHAIN.DISTRIBUTION_CENTERS dc
    LEFT JOIN NOVAMART_RETAIL.SUPPLY_CHAIN.INVENTORY i ON dc.DC_ID = i.LOCATION_ID AND i.LOCATION_TYPE = 'DC'
    GROUP BY dc.DC_ID, dc.DC_NAME, dc.STATE, dc.CAPACITY_PALLETS, dc.DAILY_THROUGHPUT, dc.STORES_SERVED
    """)
    
    print("  Created 4 analytics views")
    cursor.close()

def main():
    print("=" * 60)
    print("NOVAMART AGENTIC COMMERCE - SNOWFLAKE DATA LOADER")
    print("=" * 60)
    
    conn = get_connection()
    print(f"Connected to Snowflake")
    
    try:
        load_products(conn)
        load_stores(conn)
        load_customers(conn)
        load_inventory(conn)
        load_orders(conn)
        load_agent_definitions(conn)
        create_views(conn)
        
        print("\n" + "=" * 60)
        print("DATA LOAD COMPLETE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during data load: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
