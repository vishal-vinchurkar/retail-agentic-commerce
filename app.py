import streamlit as st
import time
import random
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data.sample_data import PRODUCTS, CUSTOMERS, AGENT_DEFINITIONS

def search_products(query: str, limit: int = 3) -> list:
    """Search products based on query matching name, category, subcategory, or tags."""
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]
    scored_products = []
    
    for product in PRODUCTS:
        score = 0
        name_lower = product["name"].lower()
        category_lower = product.get("category", "").lower()
        subcategory_lower = product.get("subcategory", "").lower()
        tags = [t.lower() for t in product.get("tags", [])]
        
        for word in query_words:
            if word in name_lower:
                score += 10
            if word in category_lower:
                score += 8
            if word in subcategory_lower:
                score += 8
            for tag in tags:
                if word in tag:
                    score += 6
        
        if score > 0:
            scored_products.append((score, product))
    
    scored_products.sort(key=lambda x: x[0], reverse=True)
    return [p[1] for p in scored_products[:limit]] if scored_products else PRODUCTS[:limit]

st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    .stApp { background: linear-gradient(180deg, #0f0f14 0%, #1a1a24 100%); }
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 1rem !important; max-width: 800px !important; }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
    @keyframes typing { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-4px); } }
    @keyframes glow { 0%, 100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.3); } 50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); } }
    
    .chat-msg { animation: fadeIn 0.3s ease-out; margin-bottom: 1rem; }
    
    .user-bubble {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        margin-left: auto;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .assistant-msg {
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    
    .avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3d);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    
    .assistant-bubble {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.9);
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        max-width: 85%;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .thinking-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.15);
        padding: 10px 16px;
        border-radius: 12px;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.7);
        animation: pulse 2s infinite;
    }
    
    .thinking-dots {
        display: flex;
        gap: 4px;
    }
    
    .thinking-dots span {
        width: 6px;
        height: 6px;
        background: #6366f1;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    
    .product-inline {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 14px 16px;
        margin: 8px 0;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .product-inline:hover {
        border-color: rgba(139, 92, 246, 0.5);
        background: rgba(139, 92, 246, 0.05);
        transform: translateX(4px);
    }
    
    .order-card-inline {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(6, 182, 212, 0.05));
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 14px;
        padding: 16px;
        margin: 10px 0;
    }
    
    .tracking-line {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .tracking-line:last-child { border-bottom: none; }
    
    .tracking-dot {
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
    }
    
    .tracking-dot.pending {
        background: rgba(255,255,255,0.2);
        box-shadow: none;
    }
    
    .replenish-inline {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.05));
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 14px;
        padding: 14px;
        margin: 10px 0;
    }
    
    .agent-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        margin: 2px;
    }
    
    .agent-tag.done {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.2);
        color: #6ee7b7;
    }
    
    .brand-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .brand-icon-box {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        animation: glow 3s infinite;
    }
    
    .brand-name { color: white; font-size: 1.15rem; font-weight: 600; }
    .brand-tagline { color: rgba(255,255,255,0.4); font-size: 0.75rem; }
    
    .quick-chip {
        display: inline-block;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.7);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 4px;
    }
    
    .quick-chip:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    .complete-banner {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.08));
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        animation: fadeIn 0.5s ease;
    }
    
    hr { border-color: rgba(255,255,255,0.05) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "flow_step" not in st.session_state:
    st.session_state.flow_step = 0
if "completed_agents" not in st.session_state:
    st.session_state.completed_agents = set()
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "order_id" not in st.session_state:
    st.session_state.order_id = None
if "customer" not in st.session_state:
    st.session_state.customer = CUSTOMERS[0]
if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

def reset_demo():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

st.markdown("""
<div class="brand-bar">
    <div class="brand-icon-box">⚡</div>
    <div>
        <div class="brand-name">Retail Intelligence</div>
        <div class="brand-tagline">AI Shopping Assistant • Powered by Snowflake Cortex</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages and st.session_state.flow_step == 0:
    customer = st.session_state.customer
    st.markdown(f"""
    <div class="chat-msg">
        <div class="assistant-msg">
            <div class="avatar">🤖</div>
            <div class="assistant-bubble">
                Hi {customer['name'].split()[0]}! 👋<br><br>
                I'm your personal shopping assistant with <strong>7 AI agents</strong> working behind the scenes to find you the perfect products.<br><br>
                As a <span style="color: #f59e0b; font-weight: 600;">{customer['tier']}</span> member, you get exclusive pricing & priority fulfillment.<br><br>
                <em>What are you looking for today?</em>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="user-bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "assistant":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">🤖</div>
                <div class="assistant-bubble">{msg["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "thinking":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">{msg.get("icon", "⚡")}</div>
                <div class="thinking-indicator">
                    <div class="thinking-dots"><span></span><span></span><span></span></div>
                    {msg["content"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "products":
        customer = st.session_state.customer
        discount = 0.15 if customer['tier'] == 'PLATINUM' else 0.10
        
        st.markdown("""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">🛍️</div>
                <div class="assistant-bubble">
                    Found some great options for you! Here are my top picks:
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, product in enumerate(msg["products"]):
            final = product['current_price'] * (1 - discount)
            savings = product['base_price'] - final
            
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"""
                <div class="product-inline">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: white; font-size: 1rem; font-weight: 500;">{product['name']}</div>
                            <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 2px;">{product['brand']} • Free delivery</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #10b981; font-size: 1.2rem; font-weight: 600;">${final:.2f}</div>
                            <div style="color: rgba(255,255,255,0.3); font-size: 0.75rem; text-decoration: line-through;">${product['base_price']:.2f}</div>
                            <div style="color: #f59e0b; font-size: 0.7rem;">Save ${savings:.2f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Add", key=f"add_{idx}_{msg.get('ts', '')}"):
                    st.session_state.selected_product = product
                    st.session_state.pending_action = "checkout"
                    st.rerun()
    
    elif msg["role"] == "checkout":
        product = msg["product"]
        customer = st.session_state.customer
        discount = 0.15 if customer['tier'] == 'PLATINUM' else 0.10
        final = product['current_price'] * (1 - discount)
        
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">🛒</div>
                <div class="assistant-bubble">
                    Excellent choice! Here's your checkout:
                    <div class="order-card-inline" style="margin-top: 12px;">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <div style="color: white; font-weight: 500;">{product['name']}</div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">{product['brand']}</div>
                                <div style="color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-top: 8px;">
                                    ✓ {customer['tier']} discount<br>
                                    ✓ Free express delivery<br>
                                    ✓ 30-day returns
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: #10b981; font-size: 1.5rem; font-weight: 600;">${final:.2f}</div>
                                <div style="color: rgba(255,255,255,0.3); text-decoration: line-through;">${product['base_price']:.2f}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Confirm Purchase", key="confirm_btn", type="primary"):
            st.session_state.pending_action = "process_order"
            st.rerun()
    
    elif msg["role"] == "order_confirmed":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">✅</div>
                <div class="assistant-bubble">
                    <div style="color: #10b981; font-weight: 600; margin-bottom: 8px;">Order Confirmed!</div>
                    <div style="font-family: 'JetBrains Mono', monospace; color: #06b6d4; font-size: 0.9rem;">{msg['order_id']}</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 4px;">
                        Routing to fulfillment agents...
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "fulfillment":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">📦</div>
                <div class="assistant-bubble">
                    Your order is moving through fulfillment:
                    <div class="order-card-inline">
                        <div class="tracking-line">
                            <div class="tracking-dot"></div>
                            <div style="flex: 1;">
                                <div style="color: white; font-size: 0.85rem;">Order Received</div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem;">Assigned to Melbourne DC (Truganina)</div>
                            </div>
                            <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; font-family: 'JetBrains Mono';">{msg['times'][0]}</div>
                        </div>
                        <div class="tracking-line">
                            <div class="tracking-dot"></div>
                            <div style="flex: 1;">
                                <div style="color: white; font-size: 0.85rem;">Picked & Packed</div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem;">Quality verified</div>
                            </div>
                            <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; font-family: 'JetBrains Mono';">{msg['times'][1]}</div>
                        </div>
                        <div class="tracking-line">
                            <div class="tracking-dot"></div>
                            <div style="flex: 1;">
                                <div style="color: white; font-size: 0.85rem;">Shipped</div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem;">Tracking: {msg['tracking']}</div>
                            </div>
                            <div style="color: rgba(255,255,255,0.3); font-size: 0.7rem; font-family: 'JetBrains Mono';">{msg['times'][2]}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "replenishment":
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">🔄</div>
                <div class="assistant-bubble">
                    <span style="color: #fbbf24;">⚠️ Low inventory detected!</span><br>
                    Auto-triggered replenishment:
                    <div class="replenish-inline">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                            <span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; padding: 2px 8px; border-radius: 4px; font-size: 0.65rem; font-weight: 600;">AUTO-PO</span>
                            <span style="color: rgba(255,255,255,0.5); font-size: 0.75rem;">by Inventory Agent</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.65rem;">PO NUMBER</div>
                                <div style="color: #f59e0b; font-weight: 600; font-family: 'JetBrains Mono';">{msg['po_id']}</div>
                            </div>
                            <div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.65rem;">QTY</div>
                                <div style="color: white;">48 units</div>
                            </div>
                            <div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.65rem;">SUPPLIER</div>
                                <div style="color: white; font-size: 0.85rem;">Global Home Furnishings</div>
                            </div>
                            <div>
                                <div style="color: rgba(255,255,255,0.4); font-size: 0.65rem;">ETA</div>
                                <div style="color: white; font-size: 0.85rem;">Mar 15, 2026</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "complete":
        agent_chips = ""
        for agent_id in ["DEMAND_SENSING", "CUSTOMER_INTELLIGENCE", "INVENTORY_OPTIMIZER", "PRICING_AGENT", "FULFILLMENT_ORCHESTRATOR", "LOGISTICS_OPTIMIZER", "SUPPLIER_COLLABORATION"]:
            agent_chips += f'<span class="agent-tag done">✓ {AGENT_DEFINITIONS[agent_id]["name"].split()[0]}</span>'
        
        st.markdown(f"""
        <div class="chat-msg">
            <div class="assistant-msg">
                <div class="avatar">🎉</div>
                <div class="complete-banner">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">🎉</div>
                    <div style="color: white; font-size: 1.15rem; font-weight: 600;">End-to-End Flow Complete</div>
                    <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem; margin: 8px 0;">All 7 AI agents executed seamlessly</div>
                    <div style="margin-top: 12px;">
                        {agent_chips}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Start New Conversation", key="reset_btn"):
            reset_demo()
            st.rerun()

if st.session_state.pending_action == "search":
    query = st.session_state.get("pending_query", "")
    st.session_state.messages.append({"role": "user", "content": query})
    
    agents_flow = [
        ("DEMAND_SENSING", "📊", "Analyzing intent..."),
        ("CUSTOMER_INTELLIGENCE", "👤", "Loading preferences..."),
        ("INVENTORY_OPTIMIZER", "📦", "Checking stock..."),
        ("PRICING_AGENT", "💰", "Calculating prices...")
    ]
    
    for agent_id, icon, status in agents_flow:
        st.session_state.completed_agents.add(agent_id)
    
    ts = datetime.now().strftime("%H%M%S")
    matched_products = search_products(query)
    st.session_state.messages.append({"role": "products", "products": matched_products, "ts": ts})
    st.session_state.flow_step = 1
    st.session_state.pending_action = None
    st.rerun()

elif st.session_state.pending_action == "checkout":
    product = st.session_state.selected_product
    st.session_state.messages.append({"role": "checkout", "product": product})
    st.session_state.flow_step = 2
    st.session_state.pending_action = None
    st.rerun()

elif st.session_state.pending_action == "process_order":
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(100000, 999999)}"
    tracking = f"STK{random.randint(1000000, 9999999)}"
    po_id = f"PO-2026-{random.randint(80000, 89999)}"
    st.session_state.order_id = order_id
    
    st.session_state.messages.append({"role": "order_confirmed", "order_id": order_id})
    
    for agent_id in ["FULFILLMENT_ORCHESTRATOR", "LOGISTICS_OPTIMIZER", "SUPPLIER_COLLABORATION"]:
        st.session_state.completed_agents.add(agent_id)
    
    times = [
        datetime.now().strftime("%H:%M:%S"),
        datetime.now().strftime("%H:%M:%S"),
        datetime.now().strftime("%H:%M:%S")
    ]
    st.session_state.messages.append({"role": "fulfillment", "times": times, "tracking": tracking})
    st.session_state.messages.append({"role": "replenishment", "po_id": po_id})
    st.session_state.messages.append({"role": "complete"})
    st.session_state.flow_step = 5
    st.session_state.pending_action = None
    st.rerun()

if st.session_state.flow_step == 0:
    st.markdown("---")
    st.markdown("**💡 Try asking:**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛋️ Premium furniture", use_container_width=True, key="q1"):
            st.session_state.pending_query = "I'm looking for premium furniture for my living room"
            st.session_state.pending_action = "search"
            st.rerun()
        if st.button("🏠 Home office setup", use_container_width=True, key="q3"):
            st.session_state.pending_query = "Help me set up a home office"
            st.session_state.pending_action = "search"
            st.rerun()
    with col2:
        if st.button("🎧 Wireless headphones", use_container_width=True, key="q2"):
            st.session_state.pending_query = "I need wireless headphones for commuting"
            st.session_state.pending_action = "search"
            st.rerun()
        if st.button("📱 Smart home devices", use_container_width=True, key="q4"):
            st.session_state.pending_query = "What smart home devices do you have?"
            st.session_state.pending_action = "search"
            st.rerun()
    
    st.markdown("")
    query = st.text_input("Message", key="user_input", label_visibility="collapsed", placeholder="Type your message...")
    if query:
        st.session_state.pending_query = query
        st.session_state.pending_action = "search"
        st.rerun()

st.markdown("---")
st.caption("⚡ Retail Intelligence Platform • Snowflake Cortex AI")
