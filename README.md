# Retail Agentic Commerce Platform

> **Disclaimer:** "NovaMart" is a completely fictitious company name created solely for this educational demo. Any resemblance to a real company is purely coincidental. This code is for **experimentation and learning only** — it is not production-grade and must not be deployed to production. See [DISCLAIMER.md](DISCLAIMER.md) for the full notice.

An end-to-end demonstration of **agentic AI orchestration for retail commerce**, built on **Snowflake Cortex AI Services**. The platform showcases how multiple AI agents can collaborate across product discovery, inventory optimization, fulfillment, and supply chain operations.

Open `architecture_diagram_light.html` in a browser to see the full layered architecture.

---

## What's Inside

| Path | Purpose |
|------|---------|
| `app_showcase.py` | Main Streamlit application |
| `data/sample_data.py` | Synthetic product catalog, customers, stores, DCs (all fictitious) |
| `scripts/load_snowflake_data.py` | Loads sample data into your Snowflake account |
| `setup/snowflake_setup.sql` | Creates all required Snowflake objects (database, schemas, tables, Cortex Search) |
| `semantic_model/retail_analytics.yaml` | Cortex Analyst semantic model definition |
| `.streamlit/` | Streamlit theme configuration |
| `architecture_diagram_light.html` | Interactive architecture diagram |

---

## Snowflake Services Used

- **Cortex Search** — semantic product search over the product catalog
- **Cortex Complete** — LLM-powered query understanding and agent reasoning
- **Cortex Analyst** — natural-language analytics over sales, inventory, and customer data

---

## Setup Guide

### Prerequisites

- Python 3.9+
- A Snowflake account with **Cortex AI** enabled
- A [named connection](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#connecting-using-connections-toml) configured in your local `~/.snowflake/connections.toml`

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Configure Your Snowflake Connection

Add a named connection to `~/.snowflake/connections.toml`:

```toml
[novamart_demo]
account   = "<your-account>"
user      = "<your-user>"
authenticator = "externalbrowser"   # or another authenticator
warehouse = "COMPUTE_WH"           # your warehouse
database  = "NOVAMART_RETAIL"
schema    = "PRODUCT_360"
```

Or set a custom connection name via environment variable:

```bash
export SNOWFLAKE_CONNECTION_NAME="my_connection"
```

### Step 3 — Create Snowflake Objects

Open `setup/snowflake_setup.sql` in a Snowflake worksheet and run it. This creates:

- **Database:** `NOVAMART_RETAIL`
- **Schemas:** `PRODUCT_360`, `CUSTOMER_360`, `SUPPLY_CHAIN`, `AGENTS`, `ANALYTICS`, `SEMANTIC_MODELS`
- **Tables:** `PRODUCTS`, `DISTRIBUTION_CENTERS` (pre-seeded with 5 DCs)
- **Cortex Search Service:** `AGENTS.PRODUCT_SEARCH`
- **Stage:** `SEMANTIC_MODELS.MODELS_STAGE`

> **Note:** Edit the `WAREHOUSE` name in the Cortex Search service DDL to match your environment.

### Step 4 — Load Sample Data

```bash
python scripts/load_snowflake_data.py
```

This populates products, stores, customers, inventory, orders, agent definitions, and analytics views.

### Step 5 — Upload the Semantic Model

Using SnowSQL or the Snowflake CLI:

```bash
snow stage copy semantic_model/retail_analytics.yaml \
  @NOVAMART_RETAIL.SEMANTIC_MODELS.MODELS_STAGE \
  --overwrite
```

Or upload manually via Snowsight: **Data > Databases > NOVAMART_RETAIL > SEMANTIC_MODELS > MODELS_STAGE > Upload**.

### Step 6 — Run the App

```bash
streamlit run app_showcase.py
```

The app gracefully falls back to local sample data if Snowflake is not connected, so you can also run it standalone to explore the UI.

---

## Architecture

The platform is organized in four layers:

1. **Agentic Commerce Layer** — 7 specialized AI agents (Demand Sensing, Customer Intelligence, Inventory Optimizer, Pricing Agent, Fulfillment Orchestrator, Logistics Optimizer, Supplier Collaboration)
2. **Protocol Layer** — 5 agentic commerce protocol patterns (UCP, A2A, MCP, AP2, ACP)
3. **Snowflake Cortex AI Layer** — Cortex Search, Cortex Complete, Cortex Analyst
4. **Data Layer** — NOVAMART_RETAIL database with schemas for Product 360, Customer 360, Supply Chain, Agents, and Analytics

---

## Sample Data

All data is **synthetic and fictitious**:

- **7 Divisions** — Electronics, Home & Living, Apparel, Outdoor & Hardware, Office & Tech, Toys & Entertainment, Health & Beauty
- **450+ Products** across 50+ subcategories
- **19 Stores** across 5 Australian states
- **5 Distribution Centers** — Sydney, Melbourne, Brisbane, Perth, Adelaide
- **10 Suppliers** — fictitious global and local suppliers
- **100+ Customers** with loyalty tiers (Bronze, Silver, Gold, Platinum)
- **2,000 Orders** with line items

---

## License & Usage

This project is provided as-is for **educational and experimentation purposes only**. See [DISCLAIMER.md](DISCLAIMER.md) for the full disclaimer. No warranty of any kind is provided.
