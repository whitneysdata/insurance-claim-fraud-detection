-- ════════════════════════════════════════════════════════
-- FILE    : 02_create_tables.sql
-- PURPOSE : 3NF normalised schema — drop in FK order first
-- ════════════════════════════════════════════════════════

-- Drop in reverse FK order to avoid constraint errors
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS policyholders;

-- ════════════════════
-- TABLE 1: POLICYHOLDERS
-- Who the customer is
-- ════════════════════
CREATE TABLE policyholders (
    policyholder_id          SERIAL          PRIMARY KEY,
    customer_id              VARCHAR(20)     UNIQUE NOT NULL,
    customer_name            VARCHAR(120),
    age                      INT             CHECK (age BETWEEN 18 AND 100),
    marital_status           VARCHAR(1),     -- Y = married, N = single
    employment_status        VARCHAR(1),     -- Y = employed, N = unemployed
    no_of_family_members     INT,
    social_class             VARCHAR(5),     -- HI / MI / LI
    customer_education_level VARCHAR(30),    -- nullable: 529 missing
    tenure                   INT,            -- months as customer
    risk_segmentation        VARCHAR(2),     -- H / M / L
    house_type               VARCHAR(15),    -- Own / Mortgage / Rent
    address_line1            TEXT,
    address_line2            TEXT,           -- nullable: 85% missing (optional field)
    city                     VARCHAR(60),
    state                    VARCHAR(5),
    postal_code              VARCHAR(10)
    -- SSN, ROUTING_NUMBER, ACCT_NUMBER excluded (PII)
);

-- ════════════════════
-- TABLE 2: POLICIES
-- The insurance contract
-- ════════════════════
CREATE TABLE policies (
    policy_id                SERIAL          PRIMARY KEY,
    policyholder_id          INT             REFERENCES policyholders(policyholder_id),
    policy_number            VARCHAR(20)     UNIQUE NOT NULL,
    insurance_type           VARCHAR(20),    -- Health/Life/Mobile/Motor/Property/Travel
    premium_amount           DECIMAL(10,2)  NOT NULL,
    policy_eff_dt            DATE,
    agent_id                 VARCHAR(20)
);

-- ════════════════════
-- TABLE 3: CLAIMS
-- The transaction — fraud analysis table
-- ════════════════════
CREATE TABLE claims (
    claim_id                 SERIAL          PRIMARY KEY,
    policy_id                INT             REFERENCES policies(policy_id),
    transaction_id           VARCHAR(20)     UNIQUE NOT NULL,
    txn_date_time            TIMESTAMP,
    loss_dt                  DATE,
    report_dt                DATE,
    claim_amount             DECIMAL(12,2)  NOT NULL,
    claim_status             VARCHAR(1),    -- A = Approved | D = Denied (fraud proxy)
    incident_severity        VARCHAR(20),   -- Major Loss / Minor Loss / Total Loss
    authority_contacted      VARCHAR(20),   -- nullable: Police / Ambulance / Other
    any_injury               BOOLEAN,       -- 0 or 1 in source
    police_report_available  BOOLEAN,       -- 0 or 1 in source
    incident_state           VARCHAR(5),
    incident_city            VARCHAR(60),   -- nullable: 46 missing
    incident_hour_of_the_day INT            CHECK (incident_hour_of_the_day BETWEEN 0 AND 23),
    vendor_id                VARCHAR(20)    -- nullable: 3,245 missing
);

-- Confirm all three tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('policyholders', 'policies', 'claims')
ORDER BY table_name;