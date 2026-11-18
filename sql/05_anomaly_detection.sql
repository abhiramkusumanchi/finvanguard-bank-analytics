-- ====================================================================
-- FinVanguard 360 - Transaction Velocity & AML Anomaly Detection
-- Demonstrates: Window Functions (LAG, OVER PARTITION BY), Time-Series
-- ====================================================================

WITH TransactionVelocity AS (
    SELECT 
        t.transaction_id,
        t.customer_id,
        t.transaction_timestamp,
        t.amount_usd,
        t.channel,
        t.category,
        t.is_high_risk_flag,
        -- Previous transaction timestamp for velocity checks
        LAG(t.transaction_timestamp) OVER (
            PARTITION BY t.customer_id 
            ORDER BY t.transaction_timestamp
        ) AS prev_txn_time,
        -- Rolling 7-day spend per customer
        SUM(t.amount_usd) OVER (
            PARTITION BY t.customer_id 
            ORDER BY t.transaction_timestamp
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS rolling_window_spend
    FROM banking_dw.fact_transactions t
)
SELECT 
    v.transaction_id,
    v.customer_id,
    c.account_tier,
    c.region,
    v.transaction_timestamp,
    v.amount_usd,
    v.channel,
    v.category,
    v.rolling_window_spend,
    ROUND(
        EXTRACT(EPOCH FROM (v.transaction_timestamp - v.prev_txn_time)) / 60.0,
        1
    ) AS minutes_since_last_txn,
    CASE 
        WHEN v.is_high_risk_flag = 1 THEN 'Flagged Anomaly Rule'
        WHEN v.amount_usd > 5000 AND v.channel IN ('Mobile Banking App', 'Online Web Portal') THEN 'Velocity Spike Alert'
        ELSE 'Normal Activity'
    END AS risk_classification
FROM TransactionVelocity v
JOIN banking_dw.dim_customer c ON v.customer_id = c.customer_id
WHERE v.is_high_risk_flag = 1 OR v.amount_usd > 4500
ORDER BY v.transaction_timestamp DESC
LIMIT 50;
