# FinVanguard 360° | System & Data Architecture

## 1. High-Level Data Flow

```mermaid
flowchart TD
    subgraph DataSources["Data Ingestion Layer"]
        CUST["Raw Customers Data (10,000 records)"]
        LOANS["Raw Loan Facilities (6,500 records)"]
        TXNS["Raw Transactions (40,000 records)"]
    end

    subgraph DW["Data Warehouse & Modeling Layer (Star Schema)"]
        DIM_C["dim_customer (SCD Type 1)"]
        DIM_CP["dim_credit_profile"]
        FACT_L["fact_loans (Grain: 1 row/loan)"]
        FACT_T["fact_transactions (Grain: 1 row/txn)"]
    end

    subgraph Analytics["Analytics & ML Engine"]
        RFM["RFM Segmentation (NTILE 5)"]
        RISK["Credit Risk Scorecard (PD, LGD, EAD)"]
        CHURN["Churn Propensity Predictor"]
        STRESS["Macro Stress-Test Matrix"]
    end

    subgraph Presentation["Presentation & BI Layer"]
        DASH["Interactive Executive Web Dashboard (HTML5/Tailwind/Chart.js)"]
        PY_DASH["Streamlit Interactive Application"]
        EXEC_REP["Executive Summary & Audit Reports"]
    end

    CUST --> DIM_C
    CUST --> DIM_CP
    LOANS --> FACT_L
    TXNS --> FACT_T

    DIM_C --> RFM
    FACT_T --> RFM
    FACT_L --> RISK
    DIM_CP --> RISK
    RFM --> CHURN
    RISK --> STRESS

    RFM --> DASH
    RISK --> DASH
    STRESS --> DASH
    RFM --> PY_DASH
    RISK --> PY_DASH
    DASH --> EXEC_REP
```

---

## 2. Star Schema Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    dim_customer ||--o{ fact_loans : "disburses"
    dim_customer ||--o{ fact_transactions : "executes"
    dim_customer ||--|| dim_credit_profile : "holds"

    dim_customer {
        string customer_id PK
        int age
        string gender
        string region
        string employment_status
        numeric annual_income
        string account_tier
        int is_active_member
    }

    dim_credit_profile {
        int credit_profile_key PK
        string customer_id FK
        int credit_score
        string credit_rating_grade
        int tenure_months
        int has_credit_card
        int num_banking_products
    }

    fact_loans {
        string loan_id PK
        string customer_id FK
        string loan_type
        numeric principal_amount
        numeric interest_rate_pct
        int term_months
        numeric monthly_installment
        numeric debt_to_income_ratio
        int days_past_due
        string loan_status
        string credit_risk_grade
        int is_default_event
    }

    fact_transactions {
        string transaction_id PK
        string customer_id FK
        timestamp transaction_timestamp
        string category
        string channel
        string transaction_type
        numeric amount_usd
        int is_high_risk_flag
    }
```

---

## 3. Financial Mathematical Models Implemented

### 1. Net Interest Margin (NIM)
$$\text{NIM} = \frac{\text{Investment Returns / Loan Interest} - \text{Deposit Interest Paid}}{\text{Average Earning Assets}}$$

### 2. Basel II Expected Loss ($EL$)
$$\text{EL} = \text{PD} \times \text{LGD} \times \text{EAD}$$
* **$\text{PD}$ (Probability of Default)**: Estimated through calibrated logistic scoring based on FICO, DTI, and facility collateral.
* **$\text{LGD}$ (Loss Given Default)**: $20\%$ for residential mortgages; $50\%$ for unsecured facilities.
* **$\text{EAD}$ (Exposure at Default)**: Outstanding principal facility balance.

### 3. Credit Model Discrimination Metrics
* **ROC-AUC**: Evaluates ranking capability between non-delinquent and defaulted accounts.
* **Gini Coefficient**:
  $$\text{Gini} = 2 \times \text{AUC} - 1$$
* **Kolmogorov-Smirnov (KS) Statistic**:
  $$\text{KS} = \max_t |F_{\text{good}}(t) - F_{\text{bad}}(t)|$$
