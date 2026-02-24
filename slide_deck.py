"""
NovaMart: Agentic Retail Intelligence Platform
AI Solution Pitch Slide Deck - Panel Interview Prompt 1
"""

import streamlit as st

st.set_page_config(page_title="NovaMart - AI Solution Pitch", page_icon="❄️", layout="wide", initial_sidebar_state="collapsed")

TOTAL_SLIDES = 7

if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0

def go_next():
    if st.session_state.slide_idx < TOTAL_SLIDES - 1:
        st.session_state.slide_idx += 1

def go_prev():
    if st.session_state.slide_idx > 0:
        st.session_state.slide_idx -= 1

idx = st.session_state.slide_idx
progress_pct = ((idx + 1) / TOTAL_SLIDES) * 100

SLIDE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {{ font-family: 'Inter', sans-serif !important; }}
.stApp {{ background: linear-gradient(180deg, #070a12 0%, #0c1225 50%, #0a0f1a 100%); }}
header, [data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
.stDeployButton {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}
[data-testid="stSidebar"] {{ display: none !important; }}
h1, h2, h3, h4, h5 {{ color: white !important; }}
[data-testid="stHorizontalBlock"] {{ align-items: stretch; }}

.progress-track {{ position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: rgba(255,255,255,0.05); z-index: 9999; }}
.progress-fill {{ height: 100%; width: {progress_pct}%; background: linear-gradient(90deg, #29B5E8, #06b6d4); border-radius: 0 2px 2px 0; box-shadow: 0 0 12px rgba(41,181,232,0.4); }}
.slide-counter {{ position: fixed; bottom: 1.5rem; left: 50%; transform: translateX(-50%); font-size: 0.75rem; color: rgba(255,255,255,0.2); font-weight: 500; letter-spacing: 0.15em; z-index: 100; }}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.slide-content {{ animation: fadeInUp 0.5s ease-out; padding-top: 0.5rem; }}

.slide-section {{ font-size: 0.75rem; color: #29B5E8; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; margin-bottom: 0.75rem; }}
.slide-title {{ font-size: 3rem; font-weight: 800; color: white; margin-bottom: 0.5rem; line-height: 1.1; letter-spacing: -0.02em; }}
.slide-subtitle {{ font-size: 1.15rem; color: rgba(255,255,255,0.5); font-weight: 400; margin-bottom: 2rem; line-height: 1.5; }}
</style>
"""

st.markdown(SLIDE_CSS, unsafe_allow_html=True)

st.markdown(f"""
<div class="progress-track"><div class="progress-fill"></div></div>
<div class="slide-counter">{idx + 1} / {TOTAL_SLIDES}</div>
""", unsafe_allow_html=True)

nav_left, slide_area, nav_right = st.columns([0.5, 11, 0.5])

with nav_left:
    st.markdown("<div style='height: 45vh;'></div>", unsafe_allow_html=True)
    if idx > 0:
        st.button("‹", on_click=go_prev, key="nav_prev")

with nav_right:
    st.markdown("<div style='height: 45vh;'></div>", unsafe_allow_html=True)
    if idx < TOTAL_SLIDES - 1:
        st.button("›", on_click=go_next, key="nav_next")

with slide_area:
    st.markdown('<div class="slide-content">', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 1: The Retail AI Challenge
    # ══════════════════════════════════════════
    if idx == 0:
        st.markdown('<div class="slide-section">The Problem</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">The Retail AI Challenge</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-subtitle">Disconnected systems, reactive supply chains, and customer experiences stuck in the keyword era</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="text-align:center; padding: 1rem 0;">
<div style="font-size: 3.5rem; font-weight: 800; color: #29B5E8; line-height: 1;">$1.73T</div>
<div style="font-size: 1rem; color: rgba(255,255,255,0.5); margin-top: 0.75rem;">Lost annually to inventory distortion</div>
<div style="font-size: 0.75rem; color: rgba(255,255,255,0.25); margin-top: 0.25rem;">IHL Group, 2025</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align:center; padding: 1rem 0;">
<div style="font-size: 3.5rem; font-weight: 800; color: #29B5E8; line-height: 1;">77%</div>
<div style="font-size: 1rem; color: rgba(255,255,255,0.5); margin-top: 0.75rem;">Of e-commerce professionals use AI daily</div>
<div style="font-size: 0.75rem; color: rgba(255,255,255,0.25); margin-top: 0.25rem;">All About AI, 2025</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align:center; padding: 1rem 0;">
<div style="font-size: 3.5rem; font-weight: 800; color: #29B5E8; line-height: 1;">45%</div>
<div style="font-size: 1rem; color: rgba(255,255,255,0.5); margin-top: 0.75rem;">Abandon digital experiences that fail expectations</div>
<div style="font-size: 0.75rem; color: rgba(255,255,255,0.25); margin-top: 0.25rem;">ContentGrip / VML Report, 2025</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.05rem; color: #29B5E8; margin-bottom: 0.5rem;">Fragmented Search</div>
<div style="color: rgba(255,255,255,0.65); font-size: 0.95rem; line-height: 1.7;">"Birthday party for a 5 year old" returns garden tools and wine accessories</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.05rem; color: #29B5E8; margin-bottom: 0.5rem;">Disconnected Pricing</div>
<div style="color: rgba(255,255,255,0.65); font-size: 0.95rem; line-height: 1.7;">Pricing ignores loyalty. Inventory ignores demand. Stale prices on out-of-stock items</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.05rem; color: #29B5E8; margin-bottom: 0.5rem;">Reactive Replenishment</div>
<div style="color: rgba(255,255,255,0.65); font-size: 0.95rem; line-height: 1.7;">Run out, reorder, wait. Weekly PO cycles. Demand signals ignored until too late</div>
</div>""", unsafe_allow_html=True)
        with col4:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.5rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.05rem; color: #29B5E8; margin-bottom: 0.5rem;">Manual at Scale</div>
<div style="color: rgba(255,255,255,0.65); font-size: 0.95rem; line-height: 1.7;">Hundreds of SKUs managed manually. No personalisation. Same experience for all</div>
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 2: From Copilots to Autonomous Agents
    # ══════════════════════════════════════════
    elif idx == 1:
        st.markdown('<div class="slide-section">The Paradigm Shift</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">From Copilots to Autonomous Agents</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-subtitle">AI that doesn\'t just answer questions - it takes action on governed enterprise data</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 2rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.1rem; color: rgba(255,255,255,0.25); margin-bottom: 0.75rem;">Gen 1: Chatbots</div>
<div style="color: rgba(255,255,255,0.45); font-size: 1rem; line-height: 1.8;">Rule-based. Script-driven.<br>The customer adapts to the system.</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 2rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.1rem; color: rgba(255,255,255,0.25); margin-bottom: 0.75rem;">Gen 2: Copilots</div>
<div style="color: rgba(255,255,255,0.45); font-size: 1rem; line-height: 1.8;">LLM suggestions. Humans still decide.<br>AI assists but never acts.</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="background: linear-gradient(135deg, rgba(41,181,232,0.1), rgba(41,181,232,0.04)); border: 1px solid rgba(41,181,232,0.2); border-radius: 16px; padding: 2rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.1rem; color: #29B5E8; margin-bottom: 0.75rem;">Gen 3: Agentic AI</div>
<div style="color: rgba(255,255,255,0.7); font-size: 1rem; line-height: 1.8;">Autonomous agents that sense, decide, and act.<br>The system adapts to the customer.</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.75rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.1rem; color: white; margin-bottom: 0.5rem;">AI on governed data, not data moved to AI</div>
<div style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">Cortex runs where the data lives. No extraction, no pipeline, no security gaps.</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-left: 3px solid #29B5E8; border-radius: 14px; padding: 1.75rem; height: 100%;">
<div style="font-weight: 700; font-size: 1.1rem; color: white; margin-bottom: 0.5rem;">Snowflake-native, end to end</div>
<div style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">Cortex Search, Cortex Complete, Cortex Analyst, and Streamlit. No external APIs.</div>
</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 3: Solution Architecture
    # ══════════════════════════════════════════
    elif idx == 2:
        st.markdown('<div class="slide-section">Solution Architecture</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">NovaMart: Agentic Retail Intelligence</div>', unsafe_allow_html=True)

        ARCH = """
<div style="max-width: 100%; font-family: Inter, sans-serif;">

<!-- Layer 1: Frontend -->
<div style="background: linear-gradient(135deg, rgba(41,181,232,0.12), rgba(41,181,232,0.05)); border: 1px solid rgba(41,181,232,0.2); border-radius: 12px; padding: 12px 18px; display: flex; align-items: center; gap: 16px; margin-bottom: 8px;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, #29B5E8, #0D5B8C); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
</div>
<div>
<div style="color: white; font-weight: 700; font-size: 14px;">Streamlit Glassmorphism UI</div>
<div style="color: rgba(255,255,255,0.5); font-size: 12px; margin-top: 2px;">Dark/Light mode &middot; Cinematic boot &middot; Agent cascade &middot; Activity stream</div>
</div>
<div style="margin-left: auto; color: rgba(41,181,232,0.5); font-size: 11px; font-weight: 700; letter-spacing: 0.08em;">LAYER 1</div>
</div>

<!-- Connector -->
<div style="text-align: center; padding: 2px 0; color: rgba(41,181,232,0.35); font-size: 16px;">▾</div>

<!-- Layer 2: Snowflake + Protocols -->
<div style="display: flex; gap: 10px; margin-bottom: 8px;">
<div style="flex: 1.1; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.18); border-radius: 12px; padding: 12px 14px;">
<div style="color: #29B5E8; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; text-align: center;">&#10052; Snowflake Native</div>
<div style="display: flex; gap: 5px;">
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.18); border-radius: 8px; padding: 8px 3px;">
<div style="color: #29B5E8; font-size: 13px; font-weight: 800;">Search</div>
<div style="color: rgba(255,255,255,0.45); font-size: 10px;">Semantic</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.18); border-radius: 8px; padding: 8px 3px;">
<div style="color: #29B5E8; font-size: 13px; font-weight: 800;">Complete</div>
<div style="color: rgba(255,255,255,0.45); font-size: 10px;">LLM</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.18); border-radius: 8px; padding: 8px 3px;">
<div style="color: #29B5E8; font-size: 13px; font-weight: 800;">Analyst</div>
<div style="color: rgba(255,255,255,0.45); font-size: 10px;">Text-to-SQL</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.18); border-radius: 8px; padding: 8px 3px;">
<div style="color: #29B5E8; font-size: 13px; font-weight: 800;">Streamlit</div>
<div style="color: rgba(255,255,255,0.45); font-size: 10px;">Experience</div></div>
</div>
</div>
<div style="flex: 0.9; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 12px 14px;">
<div style="color: rgba(255,255,255,0.35); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; text-align: center;">Industry Protocols</div>
<div style="display: flex; gap: 5px;">
<div style="flex:1; text-align:center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 2px;">
<div style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 800;">UCP</div>
<div style="color: rgba(255,255,255,0.3); font-size: 10px;">Commerce</div></div>
<div style="flex:1; text-align:center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 2px;">
<div style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 800;">A2A</div>
<div style="color: rgba(255,255,255,0.3); font-size: 10px;">Agent</div></div>
<div style="flex:1; text-align:center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 2px;">
<div style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 800;">MCP</div>
<div style="color: rgba(255,255,255,0.3); font-size: 10px;">Context</div></div>
<div style="flex:1; text-align:center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 2px;">
<div style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 800;">AP2</div>
<div style="color: rgba(255,255,255,0.3); font-size: 10px;">Payment</div></div>
<div style="flex:1; text-align:center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 2px;">
<div style="color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 800;">ACP</div>
<div style="color: rgba(255,255,255,0.3); font-size: 10px;">Txn</div></div>
</div>
</div>
</div>

<!-- Connector -->
<div style="text-align: center; padding: 2px 0; color: rgba(41,181,232,0.35); font-size: 16px;">▾</div>

<!-- Layer 3: Agents -->
<div style="background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-radius: 12px; padding: 12px 14px; margin-bottom: 8px;">
<div style="display: flex; gap: 5px; margin-bottom: 8px;">
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F4CA;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Demand</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Forecasting</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F464;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Customer</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Segmentation</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F4E6;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Inventory</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">ATP &amp; Stock</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F4B0;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Pricing</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Dynamic</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F3ED;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Fulfillment</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Routing</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F69A;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Logistics</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Route Opt.</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.06); border: 1px solid rgba(41,181,232,0.15); border-radius: 8px; padding: 10px 3px;">
<div style="font-size: 18px;">&#x1F91D;</div><div style="color: white; font-size: 11px; font-weight: 700; margin-top: 2px;">Supplier</div><div style="color: rgba(255,255,255,0.35); font-size: 9px;">Auto-PO</div></div>
</div>
<div style="text-align: center; font-size: 10px; color: rgba(41,181,232,0.5); font-weight: 700; letter-spacing: 0.1em;">&larr; A2A: STRUCTURED CONTEXT PASSING &rarr;</div>
</div>

<!-- Connector -->
<div style="text-align: center; padding: 2px 0; color: rgba(41,181,232,0.35); font-size: 16px;">▾</div>

<!-- Layer 4+5: Cortex Services + Data -->
<div style="display: flex; gap: 10px; margin-bottom: 8px;">
<div style="flex: 1; background: linear-gradient(135deg, rgba(13,91,140,0.15), rgba(41,181,232,0.06)); border: 1px solid rgba(41,181,232,0.2); border-radius: 12px; padding: 12px 16px;">
<div style="color: rgba(41,181,232,0.6); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 5px;">Cortex AI Services</div>
<div style="color: rgba(255,255,255,0.55); font-size: 12px; line-height: 1.6;">Vector Embeddings &middot; LLM Inference &middot; Semantic Models</div>
</div>
<div style="flex: 1; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.12); border-radius: 12px; padding: 12px 16px;">
<div style="color: rgba(41,181,232,0.6); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 5px;">Snowflake Data Platform</div>
<div style="display: flex; gap: 5px; flex-wrap: wrap;">
<span style="font-size: 10px; padding: 3px 10px; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.15); border-radius: 20px; color: rgba(255,255,255,0.55);">PRODUCT_360</span>
<span style="font-size: 10px; padding: 3px 10px; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.15); border-radius: 20px; color: rgba(255,255,255,0.55);">CUSTOMER_360</span>
<span style="font-size: 10px; padding: 3px 10px; background: rgba(41,181,232,0.08); border: 1px solid rgba(41,181,232,0.15); border-radius: 20px; color: rgba(255,255,255,0.55);">SUPPLY_CHAIN</span>
</div>
</div>
</div>

<!-- Connector -->
<div style="text-align: center; padding: 2px 0; color: rgba(41,181,232,0.35); font-size: 16px;">▾</div>

<!-- Layer 6: Distribution -->
<div style="display: flex; gap: 6px;">
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.1); border-radius: 10px; padding: 10px 4px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #29B5E8; margin: 0 auto 4px; box-shadow: 0 0 8px rgba(41,181,232,0.5);"></div>
<div style="color: white; font-size: 11px; font-weight: 700;">Sydney</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.1); border-radius: 10px; padding: 10px 4px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #29B5E8; margin: 0 auto 4px; box-shadow: 0 0 8px rgba(41,181,232,0.5);"></div>
<div style="color: white; font-size: 11px; font-weight: 700;">Melbourne</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.1); border-radius: 10px; padding: 10px 4px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #29B5E8; margin: 0 auto 4px; box-shadow: 0 0 8px rgba(41,181,232,0.5);"></div>
<div style="color: white; font-size: 11px; font-weight: 700;">Brisbane</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.1); border-radius: 10px; padding: 10px 4px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #29B5E8; margin: 0 auto 4px; box-shadow: 0 0 8px rgba(41,181,232,0.5);"></div>
<div style="color: white; font-size: 11px; font-weight: 700;">Perth</div></div>
<div style="flex:1; text-align:center; background: rgba(41,181,232,0.04); border: 1px solid rgba(41,181,232,0.1); border-radius: 10px; padding: 10px 4px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: #29B5E8; margin: 0 auto 4px; box-shadow: 0 0 8px rgba(41,181,232,0.5);"></div>
<div style="color: white; font-size: 11px; font-weight: 700;">Adelaide</div></div>
</div>

</div>
"""
        st.markdown(ARCH, unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 4: Key Differentiation
    # ══════════════════════════════════════════
    elif idx == 3:
        st.markdown('<div class="slide-section">Why Snowflake</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">Key Differentiation</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-subtitle">Cortex, Snowflake Intelligence, and Cortex Code put us in a uniquely strong position to deliver AI outcomes</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            for title, desc in [
                ("Zero Data Movement", "AI runs where the data already lives. No ETL pipelines to separate ML platforms. No copies. No security trade-offs."),
                ("Snowflake Intelligence + Cortex Code", "Executive insights and developer acceleration, natively integrated. From idea to production on a single platform."),
                ("Native Governance", "Every agent decision fully auditable. Column-level security, dynamic data masking, and role-based access - all built in."),
            ]:
                st.markdown(f"""<div style="background: linear-gradient(135deg, rgba(41,181,232,0.06), rgba(41,181,232,0.02)); border: 1px solid rgba(41,181,232,0.15); border-radius: 14px; padding: 1.5rem; margin-bottom: 0.75rem;">
<div style="font-weight: 700; font-size: 1.15rem; color: #29B5E8; margin-bottom: 0.5rem;">{title}</div>
<div style="color: rgba(255,255,255,0.65); font-size: 1rem; line-height: 1.7;">{desc}</div></div>""", unsafe_allow_html=True)

        with col2:
            for title, desc in [
                ("Streamlit: AI to Experience", "From Cortex output to production app on the same platform. This was built by one SE - no front-end team."),
                ("Single Platform Economics", "Pay-per-query. No GPU clusters to manage. No model hosting fees. Consumption-based."),
                ("Data Already Here", "Product 360, Customer 360, Supply Chain already in Snowflake. Activation cost is near zero."),
            ]:
                st.markdown(f"""<div style="background: linear-gradient(135deg, rgba(41,181,232,0.06), rgba(41,181,232,0.02)); border: 1px solid rgba(41,181,232,0.15); border-radius: 14px; padding: 1.5rem; margin-bottom: 0.75rem;">
<div style="font-weight: 700; font-size: 1.15rem; color: #29B5E8; margin-bottom: 0.5rem;">{title}</div>
<div style="color: rgba(255,255,255,0.65); font-size: 1rem; line-height: 1.7;">{desc}</div></div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 5: LIVE DEMO
    # ══════════════════════════════════════════
    elif idx == 4:
        st.markdown('<div class="slide-section">Live Demonstration</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">Live Demo</div>', unsafe_allow_html=True)

        st.markdown("""
<div style="height: 3rem;"></div>
<div style="background: linear-gradient(135deg, rgba(232,90,79,0.12), rgba(233,109,100,0.06)); border: 1px solid rgba(232,90,79,0.25); border-radius: 24px; padding: 4rem; text-align: center;">
    <div style="font-size: 2.5rem; font-weight: 800; color: white; margin-bottom: 1.25rem;">NovaMart: Agentic Retail Intelligence</div>
    <div style="color: rgba(255,255,255,0.6); font-size: 1.15rem; line-height: 1.8; max-width: 700px; margin: 0 auto;">
        End-to-end autonomous commerce - from natural language intent to order fulfilment and supplier PO
    </div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 6: What You Just Saw
    # ══════════════════════════════════════════
    elif idx == 5:
        st.markdown('<div class="slide-section">Post-Demo</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">What You Just Saw</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-subtitle">End-to-end agentic commerce on Snowflake Cortex</div>', unsafe_allow_html=True)

        st.markdown("""
<div style="text-align: center; padding: 0.5rem 0 2rem;">
<div style="display: inline-flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center;">
<span style="padding: 0.6rem 1.25rem; background: rgba(41,181,232,0.1); border: 1px solid rgba(41,181,232,0.25); border-radius: 100px; color: #29B5E8; font-weight: 600; font-size: 1rem;">Cortex Search</span>
<span style="padding: 0.6rem 1.25rem; background: rgba(41,181,232,0.1); border: 1px solid rgba(41,181,232,0.25); border-radius: 100px; color: #29B5E8; font-weight: 600; font-size: 1rem;">Cortex Complete</span>
<span style="padding: 0.6rem 1.25rem; background: rgba(41,181,232,0.1); border: 1px solid rgba(41,181,232,0.25); border-radius: 100px; color: #29B5E8; font-weight: 600; font-size: 1rem;">Cortex Analyst</span>
<span style="padding: 0.6rem 1.25rem; background: rgba(41,181,232,0.1); border: 1px solid rgba(41,181,232,0.25); border-radius: 100px; color: #29B5E8; font-weight: 600; font-size: 1rem;">Streamlit</span>
</div>
</div>
""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="text-align: center; padding: 1.5rem;">
<div style="font-size: 3rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.5rem;">7 / 7</div>
<div style="color: rgba(255,255,255,0.8); font-size: 1.05rem; font-weight: 600;">Agents Executed</div>
<div style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 0.4rem;">All autonomous, all real-time</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="text-align: center; padding: 1.5rem;">
<div style="font-size: 3rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.5rem;">9 / 9</div>
<div style="color: rgba(255,255,255,0.8); font-size: 1.05rem; font-weight: 600;">Protocols Active</div>
<div style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 0.4rem;">4 Snowflake + 5 Industry</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="text-align: center; padding: 1.5rem;">
<div style="font-size: 3rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.5rem;">1</div>
<div style="color: rgba(255,255,255,0.8); font-size: 1.05rem; font-weight: 600;">Auto-PO Generated</div>
<div style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 0.4rem;">Event-driven, zero lag</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 2rem; background: rgba(41,181,232,0.05); border: 1px solid rgba(41,181,232,0.12); border-radius: 16px;">
<div style="color: rgba(255,255,255,0.75); font-size: 1.1rem; line-height: 1.7;">
From <strong style="color: white;">"help me plan a birthday party"</strong> to order confirmed, supply chain routed,<br>and auto-replenishment PO generated. One platform. Fully governed. Fully auditable.
</div>
</div>
""", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SLIDE 7: Business Value & Next Steps
    # ══════════════════════════════════════════
    elif idx == 6:
        st.markdown('<div class="slide-section">Business Value</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-title">Why This Matters</div>', unsafe_allow_html=True)
        st.markdown('<div class="slide-subtitle">Three value pillars that agentic AI unlocks for retail</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(41,181,232,0.12); border-left: 4px solid #29B5E8; border-radius: 0 14px 14px 0; padding: 2rem; height: 100%;">
<div style="font-size: 2.5rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.75rem; opacity: 0.7;">01</div>
<div style="font-weight: 700; font-size: 1.15rem; color: white; margin-bottom: 0.75rem;">Customer Experience Gap</div>
<div style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">Every agent shares context. Search knows inventory. Pricing knows loyalty. One seamless experience.</div>
</div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(41,181,232,0.12); border-left: 4px solid #29B5E8; border-radius: 0 14px 14px 0; padding: 2rem; height: 100%;">
<div style="font-size: 2.5rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.75rem; opacity: 0.7;">02</div>
<div style="font-weight: 700; font-size: 1.15rem; color: white; margin-bottom: 0.75rem;">Supply Chain Velocity</div>
<div style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">Reactive to predictive. Event-driven replenishment. Zero lag between demand signal and supplier PO.</div>
</div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(41,181,232,0.12); border-left: 4px solid #29B5E8; border-radius: 0 14px 14px 0; padding: 2rem; height: 100%;">
<div style="font-size: 2.5rem; font-weight: 800; color: #29B5E8; margin-bottom: 0.75rem; opacity: 0.7;">03</div>
<div style="font-weight: 700; font-size: 1.15rem; color: white; margin-bottom: 0.75rem;">Intelligence at Scale</div>
<div style="color: rgba(255,255,255,0.6); font-size: 1rem; line-height: 1.8;">AI agents manage thousands of SKUs with personalised pricing, real-time inventory, and contextual recommendations.</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div style="background: linear-gradient(135deg, rgba(41,181,232,0.08), rgba(41,181,232,0.03)); border: 1px solid rgba(41,181,232,0.18); border-radius: 20px; padding: 2.5rem; text-align: center; margin-top: 2.5rem;">
    <div style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 0.75rem;">Ready to Start</div>
    <div style="color: rgba(255,255,255,0.6); font-size: 1.05rem; line-height: 1.8;">
        Scoped POC on a single category and segment using Cortex Search + Complete.<br>
        Consumption-based, no upfront cost. We can be in production faster than you'd expect.
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
