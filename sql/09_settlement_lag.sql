SELECT
    p.insurance_type,
    c.incident_severity,
    ROUND(AVG(c.report_dt - c.loss_dt), 1)              AS avg_report_lag_days,
    ROUND(AVG(c.txn_date_time::DATE - c.report_dt), 1)  AS avg_process_lag_days,
    ROUND(AVG(
        c.txn_date_time::DATE - c.loss_dt
    ), 1)                                             AS avg_total_lag_days,
    MIN(c.report_dt - c.loss_dt)                      AS fastest_report,
    MAX(c.report_dt - c.loss_dt)                      AS slowest_report,
    COUNT(*)                                             AS num_claims
FROM claims c
JOIN policies p ON c.policy_id = p.policy_id
WHERE c.loss_dt IS NOT NULL AND c.report_dt IS NOT NULL
GROUP BY p.insurance_type, c.incident_severity
ORDER BY avg_total_lag_days DESC;