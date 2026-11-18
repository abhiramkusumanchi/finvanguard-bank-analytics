-- ====================================================================
-- FinVanguard 360 - Executive Portfolio KPIs & Net Interest Margin (NIM)
-- Objective: Calculate Total AUM, WAIR, NPL Ratio, and Segment Performance
-- ====================================================================

WITH PortfolioRollup AS (
    SELECT 
        l.loan_type,
        COUNT(l.loan_id) AS total_loans,
        SUM(l.principal_amount) AS total_disbursed_usd,
        ROUND(AVG(l.interest_rate_pct), 2) AS avg_interest_rate,
        -- Weighted Average Interest Rate (WAIR)
        ROUND(
            SUM(l.principal_amount * l.interest_rate_pct) / NULLIF(SUM(l.principal_amount), 0),
            2
        ) AS weighted_avg_rate_pct,
        -- Non-Performing Loans (90+ DPD)
        SUM(CASE WHEN l.days_past_due >= 90 THEN l.principal_amount ELSE 0 END) AS npl_principal_usd,
        -- Delinquent Principal (30+ DPD)
        SUM(CASE WHEN l.days_past_due >= 30 THEN l.principal_amount ELSE 0 END) AS total_delinquent_usd
    FROM banking_dw.fact_loans l
    GROUP BY l.loan_type
),
OverallTotals AS (
    SELECT 
        SUM(total_disbursed_usd) AS portfolio_total_usd,
        SUM(npl_principal_usd) AS portfolio_npl_usd
    FROM PortfolioRollup
)
SELECT 
    p.loan_type,
    p.total_loans,
    p.total_disbursed_usd,
    ROUND((p.total_disbursed_usd / ot.portfolio_total_usd) * 100, 2) AS portfolio_share_pct,
    p.weighted_avg_rate_pct,
    p.npl_principal_usd,
    -- NPL Ratio per Product
    ROUND((p.npl_principal_usd / NULLIF(p.total_disbursed_usd, 0)) * 100, 2) AS npl_ratio_pct,
    -- Total Delinquency Rate
    ROUND((p.total_delinquent_usd / NULLIF(p.total_disbursed_usd, 0)) * 100, 2) AS total_delinquency_rate_pct
FROM PortfolioRollup p
CROSS JOIN OverallTotals ot
ORDER BY p.total_disbursed_usd DESC;
