-- ====================================================================
-- FinVanguard 360 - Enterprise Banking Star Schema DDL
-- Compatible with PostgreSQL, Snowflake, BigQuery, Amazon Redshift
-- ====================================================================

CREATE SCHEMA IF NOT EXISTS banking_dw;

-- --------------------------------------------------------------------
-- 1. Dimension Tables
-- --------------------------------------------------------------------

CREATE TABLE banking_dw.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(32) UNIQUE NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(16),
    region VARCHAR(32) NOT NULL,
    employment_status VARCHAR(64) NOT NULL,
    annual_income NUMERIC(15, 2) NOT NULL,
    account_tier VARCHAR(32) NOT NULL,
    is_active_member SMALLINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE banking_dw.dim_credit_profile (
    credit_profile_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    credit_score INT NOT NULL,
    credit_rating_grade VARCHAR(8) NOT NULL, -- AAA, AA, A, BBB, BB, B, CCC
    tenure_months INT NOT NULL,
    has_credit_card SMALLINT DEFAULT 0,
    num_banking_products INT DEFAULT 1,
    effective_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES banking_dw.dim_customer(customer_id)
);

CREATE TABLE banking_dw.dim_branch (
    branch_key SERIAL PRIMARY KEY,
    branch_code VARCHAR(16) UNIQUE NOT NULL,
    region VARCHAR(32) NOT NULL,
    city VARCHAR(64) NOT NULL,
    manager_name VARCHAR(64)
);

-- --------------------------------------------------------------------
-- 2. Fact Tables (Grain: 1 row per Loan & 1 row per Transaction)
-- --------------------------------------------------------------------

CREATE TABLE banking_dw.fact_loans (
    loan_key SERIAL PRIMARY KEY,
    loan_id VARCHAR(32) UNIQUE NOT NULL,
    customer_id VARCHAR(32) NOT NULL,
    loan_type VARCHAR(64) NOT NULL, -- Mortgage, Auto, Personal, SMB
    principal_amount NUMERIC(15, 2) NOT NULL,
    interest_rate_pct NUMERIC(5, 2) NOT NULL,
    term_months INT NOT NULL,
    monthly_installment NUMERIC(10, 2) NOT NULL,
    debt_to_income_ratio NUMERIC(5, 3) NOT NULL,
    loan_to_value_ratio NUMERIC(5, 3) NOT NULL,
    days_past_due INT DEFAULT 0,
    loan_status VARCHAR(64) NOT NULL, -- Current, 30-59 DPD, 60-89 DPD, Default
    credit_risk_grade VARCHAR(8) NOT NULL,
    is_default_event SMALLINT DEFAULT 0,
    disbursement_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES banking_dw.dim_customer(customer_id)
);

CREATE TABLE banking_dw.fact_transactions (
    transaction_key BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(32) UNIQUE NOT NULL,
    customer_id VARCHAR(32) NOT NULL,
    transaction_timestamp TIMESTAMP NOT NULL,
    category VARCHAR(64) NOT NULL,
    channel VARCHAR(32) NOT NULL, -- Mobile, Online, POS, ATM, Wire
    transaction_type VARCHAR(16) NOT NULL, -- Debit, Credit
    amount_usd NUMERIC(12, 2) NOT NULL,
    is_high_risk_flag SMALLINT DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES banking_dw.dim_customer(customer_id)
);

-- --------------------------------------------------------------------
-- 3. Optimized Indexing for Fast OLAP Querying
-- --------------------------------------------------------------------
CREATE INDEX idx_loans_customer ON banking_dw.fact_loans(customer_id);
CREATE INDEX idx_loans_status ON banking_dw.fact_loans(loan_status);
CREATE INDEX idx_loans_dpd ON banking_dw.fact_loans(days_past_due);
CREATE INDEX idx_txns_customer ON banking_dw.fact_transactions(customer_id);
CREATE INDEX idx_txns_timestamp ON banking_dw.fact_transactions(transaction_timestamp);
CREATE INDEX idx_txns_risk ON banking_dw.fact_transactions(is_high_risk_flag);
