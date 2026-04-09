-- Download files that will be exported to python 
-- Export 1: Frequency & Severity by Insurance Type
SELECT p.insurance_type,
       COUNT(*) AS total_claims,
       ROUND(AVG(c.claim_amount),2) AS avg_severity,
       SUM(CASE WHEN c.claim_status='D' THEN 1 ELSE 0 END) AS denied_claims
FROM claims c
JOIN policies p ON c.policy_id=p.policy_id
GROUP BY p.insurance_type;

-- Export 2: Loss Ratio by Insurance Type
SELECT p.insurance_type,
       ROUND(SUM(p.premium_amount),2) AS total_premiums,
       ROUND(SUM(c.claim_amount),2)   AS total_claims,
       ROUND(SUM(c.claim_amount)*100.0
           /NULLIF(SUM(p.premium_amount),0),2) AS loss_ratio_pct
FROM policies p
JOIN claims c ON p.policy_id=c.policy_id
GROUP BY p.insurance_type;

-- Export 3: Fraud Flags
WITH B AS (
    SELECT c.*,
           p.insurance_type,
           p.premium_amount,
           AVG(c.claim_amount) OVER(PARTITION BY p.insurance_type) AS type_avg
    FROM claims c
    JOIN policies p ON c.policy_id=p.policy_id
)
SELECT transaction_id, insurance_type, claim_amount, claim_status,
       police_report_available, any_injury,
       ROUND(type_avg,2) AS type_avg_claim,
       CASE WHEN claim_amount>(2*type_avg) AND police_report_available=FALSE
            THEN 'FLAGGED' ELSE 'OK' END AS sql_fraud_flag
FROM B;

-- Export 4: Settlement Lag
SELECT p.insurance_type, c.incident_severity,
       ROUND(AVG(c.report_dt-c.loss_dt),1)             AS avg_report_lag,
       ROUND(AVG(c.txn_date_time::DATE-c.report_dt),1) AS avg_process_lag,
       COUNT(*) AS num_claims
FROM claims c
JOIN policies p ON c.policy_id=p.policy_id
WHERE c.loss_dt IS NOT NULL
GROUP BY 1,2 ORDER BY avg_process_lag DESC;

-- Export 5: Full profile for Python ML model
SELECT
    ph.age, ph.marital_status, ph.employment_status,
    ph.no_of_family_members, ph.social_class,
    ph.customer_education_level, ph.tenure,
    ph.risk_segmentation, ph.house_type,
    p.insurance_type, p.premium_amount,
    c.claim_amount, c.claim_status,
    c.incident_severity, c.authority_contacted,
    c.any_injury, c.police_report_available,
    c.incident_state, c.incident_hour_of_the_day,
    (c.report_dt - c.loss_dt)                 AS report_lag_days,
    (c.txn_date_time::DATE - c.report_dt)     AS process_lag_days,
    CASE WHEN c.vendor_id IS NULL THEN 0 ELSE 1 END AS vendor_involved
FROM policyholders ph
JOIN policies p ON ph.policyholder_id = p.policyholder_id
JOIN claims   c ON p.policy_id       = c.policy_id;
