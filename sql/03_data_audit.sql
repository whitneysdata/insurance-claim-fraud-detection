-- ═════════════════════════════════════
-- FILE: 03_data_audit.sql
-- PURPOSE: data cleaning - Audit nulls, ranges, and value sets
-- ═════════════════════════════════════

-- 1. Row count confirmation
SELECT COUNT(*) AS total_rows FROM staging_claims;
-- Expected: 10000

-- 2. Null counts for every column
SELECT
    COUNT(*) - COUNT(txn_date_time)            AS null_txn_date,
    COUNT(*) - COUNT(claim_amount)             AS null_claim_amount,
    COUNT(*) - COUNT(premium_amount)           AS null_premium,
    COUNT(*) - COUNT(address_line2)            AS null_address2,   -- expect ~8505
    COUNT(*) - COUNT(vendor_id)                AS null_vendor,     -- expect ~3245
    COUNT(*) - COUNT(authority_contacted)      AS null_authority,  -- expect ~1945
    COUNT(*) - COUNT(customer_education_level) AS null_education,  
    COUNT(*) - COUNT(city)                      AS null_city,      
    COUNT(*) - COUNT(incident_city)            AS null_incident_city -- expect ~46
FROM staging_claims;

-- 3. Confirm no ? placeholders (this dataset uses real NULLs, not ?)
SELECT
    SUM(CASE WHEN claim_status        = '?' THEN 1 ELSE 0 END) AS q_claim_status,
    SUM(CASE WHEN insurance_type      = '?' THEN 1 ELSE 0 END) AS q_insurance_type,
    SUM(CASE WHEN risk_segmentation  = '?' THEN 1 ELSE 0 END) AS q_risk
FROM staging_claims;
-- All should return 0 — confirmed clean

-- 4. Verify CLAIM_STATUS values (fraud label)
SELECT claim_status, COUNT(*) AS count
FROM staging_claims
GROUP BY claim_status;
-- Expect: A = ~9497, D = ~503

-- 5. Verify insurance types
SELECT insurance_type, COUNT(*) AS count
FROM staging_claims
GROUP BY insurance_type
ORDER BY count DESC;
-- Expect: Health, Life, Mobile, Motor, Property, Travel

-- 6. Numeric range validation
SELECT
    MIN(premium_amount::DECIMAL)  AS min_premium,
    MAX(premium_amount::DECIMAL)  AS max_premium,
    MIN(claim_amount::DECIMAL)    AS min_claim,
    MAX(claim_amount::DECIMAL)    AS max_claim,
    MIN(age::INT)                  AS min_age,
    MAX(age::INT)                  AS max_age
FROM staging_claims;
-- Expect: premium 6–200 | claim 100–100000 | age 25–64

-- 7. Date format sanity check
SELECT
    txn_date_time,
    policy_eff_dt,
    loss_dt,
    report_dt
FROM staging_claims
LIMIT 5;
-- Dates look like: 2020-06-01 00:00:00 | 2015-06-23 | 2020-05-16 | 2020-05-21
