# NovaMart: Agentic Retail Intelligence Platform

> **IMPORTANT DISCLAIMER**
>
> **"NovaMart" is a completely fictitious company name** created solely for the purposes of this educational demonstration. It does not represent, refer to, or have any affiliation with any real company, organization, or brand — past, present, or future. Any resemblance to an actual company name is purely coincidental and unintentional.
>
> This project is provided **strictly for educational and experimentation purposes only**. It is a concept demonstration of agentic AI patterns in a retail context. **This code must not be deployed to production environments** under any circumstances. It is not production-grade, has not been security-audited, and makes no guarantees of correctness, completeness, or fitness for any commercial use.
>
> All product names, customer names, store locations, financial figures, supplier details, and other data in this repository are **entirely fictional and synthetically generated**. No real customer data, transaction data, or business data of any kind is included.
>
> This project is **not affiliated with, endorsed by, or officially connected to Snowflake Inc.** or any other company. References to Snowflake services (Cortex Search, Cortex Complete, Cortex Analyst) reflect publicly documented capabilities used in an educational context. "Powered by Snowflake Cortex" is used descriptively, not as an endorsement.

---

## Overview

A demonstration of agentic AI orchestration for retail operations. This platform showcases how multiple AI agents can collaborate to handle commerce transactions and supply chain optimization — purely as an educational exercise.

## Features

- **7 Specialized AI Agents**: Demand Sensing, Inventory Optimization, Fulfillment Orchestration, Supplier Collaboration, Logistics Optimization, Dynamic Pricing, and Customer Intelligence
- **End-to-End Flow Visualization**: From product discovery through checkout, fulfillment, and automatic replenishment
- **5 Agentic Commerce Protocols**: UCP, A2A, MCP, AP2, ACP — demonstrated as conceptual orchestration patterns
- **Enterprise-Grade UX**: Dark/light theme, glassmorphism, smooth animations, and real-time activity streams
- **Synthetic Sample Data**: Multi-division retail structure with 5 divisions, 5 distribution centers, 6 suppliers, and comprehensive inventory data — all fictitious

## Running Locally

```bash
cd retail_intelligence_platform
streamlit run app_showcase.py
```

**Prerequisites:**
- Python 3.9+
- Streamlit 1.28+
- A Snowflake account with Cortex services enabled (optional — the app gracefully falls back to local sample data if Snowflake is not connected)

**Snowflake Connection:**

Set the `SNOWFLAKE_CONNECTION_NAME` environment variable to your named connection, or configure a named connection called `novamart_demo` in your local Snowflake configuration. No credentials are stored in this repository.

## Architecture

```
retail_intelligence_platform/
├── app_showcase.py            # Main Streamlit application (recommended)
├── app_elevated.py            # Alternate app variant
├── app_internal.py            # Alternate app variant
├── app.py                     # Base application
├── data/
│   └── sample_data.py         # Synthetic sample data (all fictitious)
├── scripts/
│   └── load_snowflake_data.py # Script to load sample data into Snowflake
├── semantic_model/
│   └── retail_analytics.yaml  # Cortex Analyst semantic model definition
├── .streamlit/
│   ├── config.toml            # Light theme config
│   └── config_showcase.toml   # Dark theme config
├── PRESENTER_GUIDE.md         # Demo presenter guide
├── DEMO_TALK_TRACK.md         # Detailed talk track script
├── DISCLAIMER.md              # Full legal disclaimer
└── README.md                  # This file
```

## Sample Data Structure

All data below is **synthetic and fictitious**:

- **Divisions**: Home & Living, Apparel, Electronics, Outdoor & Hardware, Office & Technology, Toys & Entertainment, Health & Beauty
- **Distribution Centers**: Sydney, Melbourne, Brisbane, Perth, Adelaide
- **Suppliers**: Fictitious global (China, Vietnam, Thailand, Taiwan) and local (Australia) suppliers
- **Products**: Cross-category inventory with full supply chain metadata
- **Customers**: Synthetically generated profiles with fictional names and emails

## Customization

To adapt for your own learning or organization:

1. Update `data/sample_data.py` with your divisions and product structure
2. Modify agent definitions to match your operational processes
3. Adjust styling in the CSS block within the app files
4. Configure your own Snowflake connection via the `SNOWFLAKE_CONNECTION_NAME` environment variable

## License & Usage

This project is provided as-is for **educational and experimentation purposes only**. See [DISCLAIMER.md](DISCLAIMER.md) for the full disclaimer.

- No warranty of any kind is provided
- Not suitable for production deployment
- No real business data is included
- Use at your own risk
