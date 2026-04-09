WITH DeniedByRisk AS (
    SELECT
        ph.risk_segmentation,
        ph.social_class,
        ph.employment_status,
        COUNT(*)                                             AS total_claims,
        SUM(CASE WHEN c.claim_status = 'D' THEN 1 ELSE 0 END) AS denied_claims,
        ROUND(AVG(c.claim_amount), 2)                     AS avg_claim,
        ROUND(SUM(p.premium_amount), 2)                    AS total_premiums
    FROM policyholders ph
    JOIN policies p ON ph.policyholder_id = p.policyholder_id
    JOIN claims   c ON p.policy_id       = c.policy_id
    GROUP BY
        ph.risk_segmentation,
        ph.social_class,
        ph.employment_status
)
SELECT *,
    ROUND(denied_claims * 100.0 / NULLIF(total_claims, 0), 2) AS denial_rate_pct,
    ROUND(
        SUM(avg_claim * total_claims) OVER()
        / SUM(total_premiums) OVER() * 100
    , 2)                                                    AS portfolio_loss_ratio,
    DENSE_RANK() OVER (
        ORDER BY denied_claims DESC
    )                                                       AS risk_rank
FROM DeniedByRisk
ORDER BY denial_rate_pct DESC;