SELECT
    p.insurance_type,
    COUNT(DISTINCT p.policy_id)             AS num_policies,
    ROUND(SUM(p.premium_amount), 2)          AS total_premiums,
    ROUND(SUM(c.claim_amount), 2)            AS total_claims,
    ROUND(
        SUM(c.claim_amount) * 100.0
        / NULLIF(SUM(p.premium_amount), 0)
    , 2)                                      AS loss_ratio_pct
FROM policies p
JOIN claims c ON p.policy_id = c.policy_id
GROUP BY p.insurance_type
ORDER BY loss_ratio_pct DESC;