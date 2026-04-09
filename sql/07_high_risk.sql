SELECT
    ph.customer_id,
    ph.age,
    ph.risk_segmentation,
    ph.social_class,
    ph.employment_status,
    ph.tenure,
    p.insurance_type,
    c.claim_amount,
    c.claim_status,
    p.premium_amount,
    ROUND(
        c.claim_amount * 100.0
        / NULLIF(p.premium_amount, 0)
    , 2)                          AS individual_loss_ratio
FROM policyholders ph
JOIN policies p ON ph.policyholder_id = p.policyholder_id
JOIN claims   c ON p.policy_id       = c.policy_id
WHERE ph.risk_segmentation = 'H'   -- H = High risk (1,455 customers)
   OR c.claim_amount > 50000
ORDER BY individual_loss_ratio DESC
LIMIT 25;