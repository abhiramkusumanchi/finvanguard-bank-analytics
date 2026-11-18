# 🏦 FinVanguard 360° | Commercial Banking Intelligence & Credit Risk Platform

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![SQL-StarSchema](https://img.shields.io/badge/SQL-Star%20Schema%20OLAP-orange.svg)](#)
[![Basel-II/III](https://img.shields.io/badge/Risk-Basel%20II%2FIII%20Compliant-emerald.svg)](#)
[![License-MIT](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **FinVanguard 360°** is an enterprise-grade commercial and retail banking intelligence platform designed to monitor portfolio health, predict credit default risk, analyze customer churn through behavioral RFM segmentation, and perform macroeconomic policy stress-testing.

---

## 🌟 Executive Highlights & Core Metrics

| Key Metric | Portfolio Value | Business Context |
| :--- | :--- | :--- |
| **Total Portfolio AUM** | **$1.35 Billion** | Combined loan assets ($936.5M) and customer deposits ($409.7M) |
| **Delinquency Exposure** | **11.21% ($104.9M)** | Accounts transitioning across 30, 60, and 90+ Days Past Due (DPD) |
| **Non-Performing Loans (NPL)** | **4.88% ($45.7M)** | Loans in 90+ DPD default category requiring legal workout |
| **Net Interest Margin (NIM)** | **3.78%** | Weighted Average Yield (8.19%) vs Cost of Funds (4.41%) |
| **Credit Model Separation** | **0.715 AUC / 33.2% KS** | Basel regulatory grade scorecard separating good vs bad borrowers |
| **At-Risk Deposit Capital** | **$115.9 Million** | 1,422 high-value accounts identified with >50% churn propensity |

---

## 🚀 Key Platform Features

1. **Executive Portfolio KPI Command Center**:
   - Real-time balance sheet monitoring, loan-to-deposit ratio tracking, and regional AUM concentration.
2. **Credit Risk & Basel II Default Engine**:
   - Computes **Probability of Default (PD)**, **Loss Given Default (LGD)**, and **Expected Loss ($EL$)**.
   - Interactive Underwriting Scorecard: enter applicant FICO, DTI, and facility type to compute instant credit decisioning.
3. **Customer Churn & Behavioral RFM Segmentation**:
   - Classifies customer base into 5 cohorts: *Champions & VIPs, Loyal Accounts, Recent High-Potential, At-Risk, and Hibernating*.
   - Early-warning roster prioritizing relationship manager outreach for accounts with >$25k deposits showing inactivity.
4. **Transaction & AML Anomaly Detection**:
   - Identifies high-risk velocity spikes, off-hours transfers, and cross-border payment anomalies across 40,000 transactions.
5. **Macroeconomic Stress-Testing Simulator**:
   - Dynamic scenario engine modeling interest rate shifts ($\pm 300\text{ bps}$), FICO cutoff tightening, and stagflation shocks on Net Interest Income and loan loss reserves.
6. **Production SQL Data Warehouse Pipeline**:
   - Optimized Star Schema with 5 production queries utilizing `NTILE(5)`, `LAG()`, CTEs, and window aggregations.

---

## 📂 Repository Architecture

```
finvanguard-bank-analytics/
├── data/
│   ├── raw/                      # Raw synthesized banking datasets
│   │   ├── customers.csv         # 10,000 customer demographic profiles
│   │   ├── loans.csv             # 6,500 loan facilities ($936.5M disbursed)
│   │   └── transactions.csv      # 40,000 multi-channel transactions
│   └── processed/
│       ├── customer_risk_summary.csv
│       └── portfolio_kpis.json
├── src/
│   ├── generate_data.py          # Calibrated realistic banking data generator
│   ├── analytics_pipeline.py     # RFM segmentation, DPD aging, and Basel EL calculations
│   ├── credit_risk_model.py      # Logistic credit risk scorecard (AUC, Gini, KS)
│   └── rfm_churn_model.py        # Customer attrition & deposit flight model
├── sql/
│   ├── 01_schema_ddl.sql         # Star Schema DDL with indexes
│   ├── 02_executive_kpis.sql     # Executive Portfolio Rollup CTEs & WAIR
│   ├── 03_credit_risk_delinquency.sql # Basel Expected Loss & DTI Matrix
│   ├── 04_rfm_customer_churn.sql # RFM Quintiles via NTILE(5) Window Functions
│   └── 05_anomaly_detection.sql  # Transaction velocity & high-risk AML flags
├── dashboard/
│   ├── index.html                # Zero-dependency interactive web dashboard
│   └── app.py                    # Streamlit interactive dashboard application
├── docs/
│   ├── ARCHITECTURE.md           # System data flow & ER diagrams
│   ├── RESUME_BULLETS.md         # Quantified STAR bullet points for your resume
│   └── STAR_INTERVIEW_GUIDE.md   # Complete interview question & answer scripts
├── README.md
└── requirements.txt
```

---

## ⚡ Quickstart: Launching the Dashboard

### Option 1: Standalone Web Dashboard (Instant — 0 Dependencies!)
Simply open `dashboard/index.html` in any web browser (Chrome, Edge, Safari, Firefox).
* No installation required.
* Fully interactive with dynamic sliders, live charts, underwriting calculator, and SQL viewer.

### Option 2: Python Analytics & Streamlit
```bash
# 1. Install optional Python packages
pip install -r requirements.txt

# 2. Run the analytics pipeline
python src/analytics_pipeline.py

# 3. Launch Streamlit UI
streamlit run dashboard/app.py
```

---

## 💼 Resume & Interview Resources
* Review [docs/RESUME_BULLETS.md](docs/RESUME_BULLETS.md) for pre-written, quantified bullet points.
* Review [docs/STAR_INTERVIEW_GUIDE.md](docs/STAR_INTERVIEW_GUIDE.md) to practice answering technical questions on Gini coefficients, Basel Expected Loss, and SQL window functions.

---

## 📜 License
MIT License. Created for portfolio showcases and technical demonstrations.
