# Cortex Code (CoCo) Prompt

Use this prompt with Snowflake Cortex Code or any AI coding assistant to recreate or adapt this platform from scratch.

---

Build a Streamlit application for an agentic retail commerce platform called "NovaMart" (fictitious retailer). The app should demonstrate multi-agent AI orchestration for retail operations using Snowflake Cortex AI services.

Requirements:
- 7 AI agents: Demand Sensing, Customer Intelligence, Inventory Optimizer, Dynamic Pricing, Fulfillment Orchestrator, Logistics Optimizer, Supplier Collaboration
- 5 agentic commerce protocol patterns: UCP (Universal Commerce Protocol), A2A (Agent-to-Agent), MCP (Model Context Protocol), AP2 (Agent Payment Protocol), ACP (Agent Commerce Protocol)
- Product search using Snowflake Cortex Search with semantic understanding (e.g. "gift for a 5-year-old" should return toys, not shoes)
- Agent reasoning using Snowflake Cortex Complete (LLM)
- Analytics using Snowflake Cortex Analyst with a semantic model
- End-to-end commerce flow: search > product selection > cart > checkout > fulfillment > supply chain response
- Real-time agent activity stream showing agent collaboration
- Dark/light theme with glassmorphism UI
- Cinematic boot sequence on app load
- Graceful fallback to local sample data when Snowflake is not connected

Data model:
- Database: NOVAMART_RETAIL
- Schemas: PRODUCT_360 (products, stores), CUSTOMER_360 (customers, orders), SUPPLY_CHAIN (inventory, distribution centers), AGENTS (agent registry, cortex search service), ANALYTICS (aggregated views), SEMANTIC_MODELS (cortex analyst yaml)
- 7 product divisions: Electronics, Home & Living, Apparel, Outdoor & Hardware, Office & Tech, Toys & Entertainment, Health & Beauty
- 5 Australian distribution centers: Sydney, Melbourne, Brisbane, Perth, Adelaide
- Customer loyalty tiers: Bronze, Silver, Gold, Platinum
- Synthetic sample data for all entities

Snowflake services used:
- Cortex Search: NOVAMART_RETAIL.AGENTS.PRODUCT_SEARCH (semantic product search)
- Cortex Complete: SNOWFLAKE.CORTEX.COMPLETE() (agent reasoning, query understanding)
- Cortex Analyst: semantic model at @NOVAMART_RETAIL.SEMANTIC_MODELS.MODELS_STAGE/retail_analytics.yaml
- Named connection: configurable via SNOWFLAKE_CONNECTION_NAME env var
