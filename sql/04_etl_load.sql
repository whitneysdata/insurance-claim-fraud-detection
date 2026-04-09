-- ═════════════════════════════════════════════
-- FILE: 04_etl_load.sql
-- Load staging → 3NF tables with type casting
-- ═════════════════════════════════════════════

-- Safe re-run guard: clear tables before loading
TRUNCATE TABLE claims        RESTART IDENTITY CASCADE;
TRUNCATE TABLE policies      RESTART IDENTITY CASCADE;
TRUNCATE TABLE policyholders RESTART IDENTITY CASCADE;

-- ── STEP 1: Load policyholders ─────────────
INSERT INTO policyholders (
    customer_id, customer_name, age,
    marital_status, employment_status,
    no_of_family_members, social_class,
    customer_education_level, tenure,
    risk_segmentation, house_type,
    address_line1, address_line2,
    city, state, postal_code
)
SELECT
    customer_id,
    customer_name,
    age::INT,
    marital_status,
    employment_status,
    no_of_family_members::INT,
    social_class,
    customer_education_level,  -- NULLs preserved as-is
    tenure::INT,
    risk_segmentation,
    house_type,
    address_line1,
    address_line2,              -- 85% NULL — structural, not data error
    city,
    state,
    postal_code
FROM staging_claims;

-- Verify
SELECT COUNT(*) AS policyholders_loaded FROM policyholders; -- expect 10000


-- ── STEP 2: Load policies ───────────────────
INSERT INTO policies (
    policyholder_id, policy_number,
    insurance_type, premium_amount,
    policy_eff_dt, agent_id
)
SELECT
    ph.policyholder_id,
    s.policy_number,
    s.insurance_type,
    s.premium_amount::DECIMAL(10,2),
    s.policy_eff_dt::DATE,
    s.agent_id
FROM staging_claims s
JOIN policyholders ph ON s.customer_id = ph.customer_id;

SELECT COUNT(*) AS policies_loaded FROM policies; -- expect 10000


-- ── STEP 3: Load claims ─────────────────────
INSERT INTO claims (
    policy_id, transaction_id, txn_date_time,
    loss_dt, report_dt, claim_amount,
    claim_status, incident_severity,
    authority_contacted, any_injury,
    police_report_available, incident_state,
    incident_city, incident_hour_of_the_day,
    vendor_id
)
SELECT
    p.policy_id,
    s.transaction_id,
    s.txn_date_time::TIMESTAMP,
    s.loss_dt::DATE,
    s.report_dt::DATE,
    s.claim_amount::DECIMAL(12,2),
    s.claim_status,
    s.incident_severity,
    s.authority_contacted,  -- NULLs preserved
    s.any_injury::INT::BOOLEAN,
    s.police_report_available::INT::BOOLEAN,
    s.incident_state,
    s.incident_city,         -- NULLs preserved
    s.incident_hour_of_the_day::INT,
    s.vendor_id              -- NULLs preserved
FROM staging_claims s
JOIN policies p ON s.policy_number = p.policy_number;

SELECT COUNT(*) AS claims_loaded FROM claims; -- expect 10000

-- ── FINAL VERIFICATION ──────────────────────
SELECT 'policyholders' AS tbl, COUNT(*) FROM policyholders
UNION ALL
SELECT 'policies',              COUNT(*) FROM policies
UNION ALL
SELECT 'claims',                COUNT(*) FROM claims;