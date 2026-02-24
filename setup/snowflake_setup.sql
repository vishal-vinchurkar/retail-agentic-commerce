-- ============================================================
-- NovaMart Agentic Commerce Platform — Snowflake Environment Setup
-- ============================================================
-- Run this script in a Snowflake worksheet (ACCOUNTADMIN or equivalent)
-- to create all required objects before loading data.
-- ============================================================

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS NOVAMART_RETAIL
    COMMENT = 'NovaMart Agentic Commerce demo — fictitious retail data for educational purposes';

-- 2. Create schemas
CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.PRODUCT_360
    COMMENT = 'Product catalog, stores, and merchandising data';

CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.CUSTOMER_360
    COMMENT = 'Customer profiles, orders, and transaction history';

CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.SUPPLY_CHAIN
    COMMENT = 'Inventory, distribution centers, and logistics';

CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.AGENTS
    COMMENT = 'AI agent registry and orchestration metadata';

CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.ANALYTICS
    COMMENT = 'Aggregated views for Cortex Analyst';

CREATE SCHEMA IF NOT EXISTS NOVAMART_RETAIL.SEMANTIC_MODELS
    COMMENT = 'Cortex Analyst semantic model stage';

-- 3. Create the Products table (load script inserts into this)
CREATE TABLE IF NOT EXISTS NOVAMART_RETAIL.PRODUCT_360.PRODUCTS (
    SKU              VARCHAR(30)  PRIMARY KEY,
    PRODUCT_NAME     VARCHAR(200),
    DIVISION         VARCHAR(50),
    CATEGORY         VARCHAR(50),
    SUBCATEGORY      VARCHAR(50),
    BRAND            VARCHAR(100),
    SUPPLIER_ID      VARCHAR(20),
    BASE_PRICE       FLOAT,
    CURRENT_PRICE    FLOAT,
    UNIT_COST        FLOAT,
    WEIGHT_KG        FLOAT,
    CUBE_M3          FLOAT,
    LEAD_TIME_DAYS   INT,
    REORDER_POINT    INT,
    SAFETY_STOCK     INT,
    PACK_SIZE        INT DEFAULT 1,
    TAGS             ARRAY,
    ATTRIBUTES       VARIANT,
    IMAGE_URL        VARCHAR(500),
    IS_ACTIVE        BOOLEAN DEFAULT TRUE,
    CREATED_AT       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 4. Create the Distribution Centers table (used by analytics views)
CREATE TABLE IF NOT EXISTS NOVAMART_RETAIL.SUPPLY_CHAIN.DISTRIBUTION_CENTERS (
    DC_ID              VARCHAR(20)  PRIMARY KEY,
    DC_NAME            VARCHAR(100),
    STATE              VARCHAR(10),
    SUBURB             VARCHAR(100),
    LATITUDE           FLOAT,
    LONGITUDE          FLOAT,
    CAPACITY_PALLETS   INT,
    AUTOMATION_LEVEL   VARCHAR(10),
    WORKFORCE          INT,
    DAILY_THROUGHPUT   INT,
    STORES_SERVED      INT,
    OPERATING_HOURS    VARCHAR(20),
    CREATED_AT         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Seed the Distribution Centers (referenced by views; not in load script)
INSERT INTO NOVAMART_RETAIL.SUPPLY_CHAIN.DISTRIBUTION_CENTERS
    (DC_ID, DC_NAME, STATE, SUBURB, LATITUDE, LONGITUDE, CAPACITY_PALLETS, AUTOMATION_LEVEL, WORKFORCE, DAILY_THROUGHPUT, STORES_SERVED, OPERATING_HOURS)
SELECT * FROM VALUES
    ('SYD-DC-01', 'Sydney Distribution Centre',    'NSW', 'Moorebank',       -33.8688, 151.2093, 85000, 'HIGH',   1200, 180000, 245, '24/7'),
    ('MEL-DC-02', 'Melbourne Distribution Centre',  'VIC', 'Truganina',       -37.8136, 144.9631, 72000, 'HIGH',    980, 145000, 198, '24/7'),
    ('BNE-DC-03', 'Brisbane Distribution Centre',   'QLD', 'Richlands',       -27.4698, 153.0251, 45000, 'MEDIUM',  650,  95000, 142, '5AM-11PM'),
    ('PER-DC-04', 'Perth Distribution Centre',      'WA',  'Canning Vale',    -31.9505, 115.8605, 38000, 'MEDIUM',  420,  65000,  89, '5AM-11PM'),
    ('ADL-DC-05', 'Adelaide Distribution Centre',   'SA',  'Edinburgh Parks', -34.9285, 138.6007, 28000, 'MEDIUM',  280,  42000,  67, '6AM-10PM');

-- 5. Create Cortex Search service for product discovery
--    (Requires Cortex Search enabled on your Snowflake account)
CREATE OR REPLACE CORTEX SEARCH SERVICE NOVAMART_RETAIL.AGENTS.PRODUCT_SEARCH
    ON PRODUCT_NAME
    ATTRIBUTES DIVISION, CATEGORY, SUBCATEGORY, BRAND, TAGS
    WAREHOUSE = COMPUTE_WH        -- change to your warehouse name
    TARGET_LAG = '1 hour'
AS (
    SELECT
        SKU,
        PRODUCT_NAME,
        BRAND,
        DIVISION,
        CATEGORY,
        SUBCATEGORY,
        CURRENT_PRICE,
        BASE_PRICE,
        ARRAY_TO_STRING(TAGS, ', ') AS TAGS
    FROM NOVAMART_RETAIL.PRODUCT_360.PRODUCTS
    WHERE IS_ACTIVE = TRUE
);

-- 6. Create a stage for the Cortex Analyst semantic model
CREATE STAGE IF NOT EXISTS NOVAMART_RETAIL.SEMANTIC_MODELS.MODELS_STAGE
    COMMENT = 'Semantic model YAML files for Cortex Analyst';

-- Upload the semantic model:
--   PUT file://semantic_model/retail_analytics.yaml
--       @NOVAMART_RETAIL.SEMANTIC_MODELS.MODELS_STAGE
--       AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
--
-- Run the PUT command from SnowSQL or the Snowflake CLI,
-- or manually upload via the Snowsight UI (Data > Stages).

-- ============================================================
-- You're done!  Next steps:
--   1. Run the data loader:  python scripts/load_snowflake_data.py
--   2. Upload the semantic model (PUT command above)
--   3. Launch the app:       streamlit run app_showcase.py
-- ============================================================
