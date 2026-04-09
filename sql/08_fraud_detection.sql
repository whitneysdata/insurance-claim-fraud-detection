WITH ClaimBenchmarks AS (
    SELECT
        c.claim_id,
        c.transaction_id,
        p.insurance_type,
        c.claim_amount,
        c.claim_status,                -- D = denied (fraud proxy)
        c.incident_severity,
        c.police_report_available,
        c.any_injury,
        ph.risk_segmentation,
        -- Global average claim amount (benchmark)
        AVG(c.claim_amount) OVER ()     AS global_avg_claim,
        -- Average by insurance type (type-level benchmark)
        AVG(c.claim_amount) OVER (
            PARTITION BY p.insurance_type
        )                               AS type_avg_claim,
        -- Rank by claim amount within each insurance type
        RANK() OVER (
            PARTITION BY p.insurance_type
            ORDER BY c.claim_amount DESC
        )                               AS rank_within_type
    FROM claims c
    JOIN policies      p  ON c.policy_id       = p.policy_id
    JOIN policyholders ph ON p.policyholder_id  = ph.policyholder_id
)
SELECT
    *,
    ROUND(global_avg_claim, 2) AS global_avg,
    ROUND(type_avg_claim, 2)   AS type_avg,
    -- Rule-based flag: claim > 2x type average AND no police report
    CASE
        WHEN claim_amount > (2 * type_avg_claim)
         AND police_report_available = FALSE
        THEN 'FLAGGED'
        ELSE 'OK'
    END                         AS sql_fraud_flag
FROM ClaimBenchmarks
ORDER BY claim_amount DESC;