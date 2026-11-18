-- ====================================================================
-- FinVanguard 360 - Customer RFM Segmentation & Churn Propensity
-- Demonstrates: Advanced Window Functions (NTILE), CTEs, and Behavioral Scoring
-- ====================================================================

WITH CustomerTransactionSummary AS (
    SELECT 
        c.customer_id,
        c.region,
        c.account_tier,
        c.annual_income,
        c.is_active_member,
        c.created_at,
        -- Recency: Days since last transaction (using current benchmark date)
        COALESCE(DATE_PART('day', '2026-03-01'::timestamp - MAX(t.transaction_timestamp)), 365) AS recency_days,
        -- Frequency: Total count of debit transactions
        COUNT(t.transaction_id) AS frequency,
        -- Monetary: Total debit volume
        COALESCE(SUM(CASE WHEN t.transaction_type = 'Debit' THEN t.amount_usd ELSE 0 END), 0) AS monetary_value
    FROM banking_dw.dim_customer c
    LEFT JOIN banking_dw.fact_transactions t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.region, c.account_tier, c.annual_income, c.is_active_member, c.created_at
),
RFM_Scores AS (
    SELECT 
        customer_id,
        region,
        account_tier,
        annual_income,
        is_active_member,
        recency_days,
        frequency,
        monetary_value,
        -- Recency Quintile (Lower days = higher score: 5 is best)
        6 - NTILE(5) OVER (ORDER BY recency_days ASC) AS r_score,
        -- Frequency Quintile (Higher count = higher score: 5 is best)
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        -- Monetary Quintile (Higher spend = higher score: 5 is best)
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM CustomerTransactionSummary
),
RFM_Segments AS (
    SELECT 
        customer_id,
        region,
        account_tier,
        annual_income,
        is_active_member,
        recency_days,
        frequency,
        monetary_value,
        r_score,
        f_score,
        m_score,
        CONCAT(r_score, f_score, m_score) AS rfm_composite_code,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions & VIPs'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Accounts'
            WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent High-Potential'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk (Declining Engagement)'
            ELSE 'Hibernating / Dormant'
        END AS rfm_cohort
    FROM RFM_Scores
)
-- Aggregate summary for executive retention dashboard
SELECT 
    rfm_cohort,
    COUNT(customer_id) AS cohort_size,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_transactions_count,
    ROUND(AVG(monetary_value), 2) AS avg_monetary_spend_usd,
    ROUND(AVG(annual_income), 2) AS avg_customer_income_usd,
    ROUND(
        (COUNT(CASE WHEN is_active_member = 0 THEN 1 END)::numeric / COUNT(customer_id)) * 100,
        2
    ) AS inactive_attrition_risk_pct
FROM RFM_Segments
GROUP BY rfm_cohort
ORDER BY cohort_size DESC;
