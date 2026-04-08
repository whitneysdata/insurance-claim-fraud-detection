-- ════════════════════════════════════════════════════════
-- PROJECT : Insurance Claim Fraud Detection
-- FILE    : 01_staging_table.sql
-- PURPOSE : Raw import table — all TEXT to prevent type errors
-- DATABASE: insurance_fraud_db
-- ══════════════════════════════════════════════════════=═

DROP TABLE IF EXISTS staging_claims;

CREATE TABLE staging_claims (
    txn_date_time              TEXT,
    transaction_id             TEXT,
    customer_id                TEXT,
    policy_number              TEXT,
    policy_eff_dt              TEXT,
    loss_dt                    TEXT,
    report_dt                  TEXT,
    insurance_type             TEXT,
    premium_amount             TEXT,
    claim_amount               TEXT,
    customer_name              TEXT,
    address_line1              TEXT,
    address_line2              TEXT,  -- 85% null — intentional optional field
    city                       TEXT,
    state                      TEXT,
    postal_code                TEXT,
    ssn                        TEXT,  -- PII: will be excluded from final tables
    marital_status             TEXT,
    age                        TEXT,
    tenure                     TEXT,
    employment_status          TEXT,
    no_of_family_members       TEXT,
    risk_segmentation          TEXT,
    house_type                 TEXT,
    social_class               TEXT,
    routing_number             TEXT,  -- PII: will be excluded from final tables
    acct_number                TEXT,  -- PII: will be excluded from final tables
    customer_education_level   TEXT,
    claim_status               TEXT,  -- A = Approved, D = Denied (fraud label)
    incident_severity          TEXT,
    authority_contacted        TEXT,
    any_injury                 TEXT,
    police_report_available    TEXT,
    incident_state             TEXT,
    incident_city              TEXT,
    incident_hour_of_the_day   TEXT,
    agent_id                   TEXT,
    vendor_id                  TEXT   -- 32% null — not all claims use a vendor
);

-- Verify table exists
SELECT 'staging_claims created successfully' AS status;

-- verify impoted csv file exists
SELECT COUNT(*) FROM staging_claims;
