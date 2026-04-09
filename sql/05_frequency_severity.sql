SELECT
    p.insurance_type,
    COUNT(*)                                        AS total_claims,
    ROUND(AVG(c.claim_amount), 2)                 AS avg_severity,
    MIN(c.claim_amount)                             AS min_claim,
    MAX(c.claim_amount)                             AS max_claim,
    ROUND(SUM(c.claim_amount), 2)                 AS total_claimed,
    SUM(CASE WHEN c.claim_status = 'D' THEN 1 ELSE 0 END) AS denied_claims,
    ROUND(
        SUM(CASE WHEN c.claim_status = 'D' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    )                                               AS denial_rate_pct
FROM claims c
JOIN policies p ON c.policy_id = p.policy_id
GROUP BY p.insurance_type
ORDER BY denial_rate_pct DESC;