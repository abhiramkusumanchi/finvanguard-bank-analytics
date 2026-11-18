-- ====================================================================
-- FinVanguard 360 - Credit Risk Delinquency Roll-Rate & Expected Loss
-- Objective: Basel II/III Risk Modeling, DTI Tiers, and Loss Given Default
-- ====================================================================

WITH LoanCreditEnriched AS (
    SELECT 
        l.loan_id,
        l.customer_id,
        l.loan_type,
        l.principal_amount,
        l.interest_rate_pct,
        l.debt_to_income_ratio,
        l.days_past_due,
        l.credit_risk_grade,
        -- Categorize Debt-to-Income (DTI) Tiers
        CASE 
            WHEN l.debt_to_income_ratio < 0.25 THEN 'Low Risk (<25%)'
            WHEN l.debt_to_income_ratio BETWEEN 0.25 AND 0.40 THEN 'Moderate Risk (25-40%)'
            WHEN l.debt_to_income_ratio BETWEEN 0.40 AND 0.50 THEN 'Elevated Risk (40-50%)'
            ELSE 'Critical Risk (>50%)'
        END AS dti_tier,
        -- Delinquency Aging Buckets
        CASE 
            WHEN l.days_past_due = 0 THEN 'Current (0 DPD)'
            WHEN l.days_past_due BETWEEN 1 AND 29 THEN 'Grace Period (1-29 DPD)'
            WHEN l.days_past_due BETWEEN 30 AND 59 THEN 'Early Delinquent (30-59 DPD)'
            WHEN l.days_past_due BETWEEN 60 AND 89 THEN 'Late Delinquent (60-89 DPD)'
            ELSE 'NPL / Default (90+ DPD)'
        END AS delinquency_aging_bucket,
        -- Regulatory Probability of Default (PD) Estimate based on Rating Grade
        CASE l.credit_risk_grade
            WHEN 'AAA' THEN 0.002
            WHEN 'AA'  THEN 0.005
            WHEN 'A'   THEN 0.012
            WHEN 'BBB' THEN 0.028
            WHEN 'BB'  THEN 0.065
            WHEN 'B'   THEN 0.145
            ELSE 0.320 -- CCC / Subprime
        END AS pd_estimate,
        -- Baseline Loss Given Default (LGD)
        CASE 
            WHEN l.loan_type IN ('Home Mortgage', 'Auto Loan') THEN 0.20 -- Collateralized
            ELSE 0.50 -- Unsecured
        END AS lgd_estimate
    FROM banking_dw.fact_loans l
)
SELECT 
    delinquency_aging_bucket,
    dti_tier,
    COUNT(loan_id) AS loan_count,
    SUM(principal_amount) AS total_exposure_usd,
    ROUND(AVG(interest_rate_pct), 2) AS avg_interest_rate_pct,
    -- Basel Expected Loss Calculation: EL = PD * LGD * EAD
    ROUND(SUM(principal_amount * pd_estimate * lgd_estimate), 2) AS basel_expected_loss_usd
FROM LoanCreditEnriched
GROUP BY delinquency_aging_bucket, dti_tier
ORDER BY 
    CASE delinquency_aging_bucket
        WHEN 'Current (0 DPD)' THEN 1
        WHEN 'Grace Period (1-29 DPD)' THEN 2
        WHEN 'Early Delinquent (30-59 DPD)' THEN 3
        WHEN 'Late Delinquent (60-89 DPD)' THEN 4
        ELSE 5
    END,
    total_exposure_usd DESC;
