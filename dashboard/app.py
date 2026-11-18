"""
FinVanguard 360 - Streamlit Interactive Banking Analytics Application
Run locally via:
    streamlit run dashboard/app.py
"""

import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set Page Config
st.set_page_config(
    page_title="FinVanguard 360 | Banking Intelligence Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Processed Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KPI_PATH = os.path.join(BASE_DIR, "data", "processed", "portfolio_kpis.json")
CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "customer_risk_summary.csv")

@st.cache_data
def load_data():
    with open(KPI_PATH, "r", encoding="utf-8") as f:
        kpis = json.load(f)
    df_customers = pd.read_csv(CSV_PATH)
    return kpis, df_customers

try:
    kpis, df_customers = load_data()
except Exception as e:
    st.error(f"Please run the analytics pipeline first: python src/analytics_pipeline.py (Error: {e})")
    st.stop()

# Custom CSS for Banking UI
st.markdown("""
<style>
    .metric-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .metric-val {
        font-size: 24px;
        font-weight: 700;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏦 FinVanguard 360°")
st.sidebar.markdown("**Commercial Banking & Credit Risk**")

selected_region = st.sidebar.selectbox("Filter by Region", ["All Regions"] + list(df_customers["region"].unique()))
selected_tier = st.sidebar.selectbox("Filter by Account Tier", ["All Tiers"] + list(df_customers["account_tier"].unique()))

# Filtered dataset
filtered_df = df_customers.copy()
if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_tier != "All Tiers":
    filtered_df = filtered_df[filtered_df["account_tier"] == selected_tier]

# Header
st.title("🏦 FinVanguard 360° Executive Intelligence Platform")
st.markdown("Real-time portfolio visibility, Basel credit risk scoring, RFM churn modeling, and macroeconomic stress-testing.")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive KPIs",
    "🛡️ Credit Risk & Basel",
    "👥 Customer Churn & RFM",
    "⚡ Stress-Test Simulator",
    "💻 SQL Architecture"
])

# -------------------------------------------------------------
# TAB 1: EXECUTIVE KPIS
# -------------------------------------------------------------
with tab1:
    exec_s = kpis["executive_summary"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Portfolio AUM", f"${exec_s['total_portfolio_aum']/1e9:.2f} Billion", "+6.4% YoY")
    with col2:
        st.metric("Total Loans Disbursed", f"${exec_s['total_loans_disbursed']/1e6:.1f} Million", "6,500 Facilities")
    with col3:
        st.metric("Delinquency Rate (30+ DPD)", f"{exec_s['delinquency_rate_pct']}%", "-0.4% QoQ")
    with col4:
        st.metric("Net Interest Margin (NIM)", f"{exec_s['net_interest_margin_pct']}%", f"WAIR: {exec_s['weighted_avg_interest_rate_pct']}%")

    st.markdown("---")
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.subheader("Credit Exposure & Default Rates by Product")
        loan_types_df = pd.DataFrame(kpis["loan_types"])
        fig_prod = px.bar(
            loan_types_df,
            x="loan_type",
            y="total_principal",
            color="default_rate_pct",
            color_continuous_scale="Viridis",
            labels={"total_principal": "Disbursed Principal ($)", "default_rate_pct": "Default Rate (%)"}
        )
        fig_prod.update_layout(template="plotly_dark")
        st.plotly_chart(fig_prod, use_container_width=True)

    with c_right:
        st.subheader("Regional AUM Distribution")
        reg_df = pd.DataFrame(kpis["regional_breakdown"])
        fig_reg = px.pie(
            reg_df,
            values="total_deposits",
            names="region",
            hole=0.4
        )
        fig_reg.update_layout(template="plotly_dark")
        st.plotly_chart(fig_reg, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: CREDIT RISK & BASEL
# -------------------------------------------------------------
with tab2:
    st.subheader("Basel II/III Delinquency Aging & Risk Scorecard")
    
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        aging_data = kpis["delinquency_buckets"]
        fig_aging = px.bar(
            x=list(aging_data.keys()),
            y=[v / 1e6 for v in aging_data.values()],
            labels={"x": "Aging Bucket", "y": "Volume ($M)"},
            title="Delinquency Aging Buckets ($ Millions)"
        )
        fig_aging.update_layout(template="plotly_dark")
        st.plotly_chart(fig_aging, use_container_width=True)

    with r_col2:
        grades = kpis["credit_grades"]
        fig_grade = px.bar(
            x=list(grades.keys()),
            y=list(grades.values()),
            labels={"x": "Internal Credit Rating Grade", "y": "Facility Count"},
            title="Credit Rating Grade Distribution"
        )
        fig_grade.update_layout(template="plotly_dark")
        st.plotly_chart(fig_grade, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: CUSTOMER CHURN & RFM
# -------------------------------------------------------------
with tab3:
    st.subheader("RFM Customer Segmentation & High-Value Attrition Alerts")
    
    rfm_counts = kpis["rfm_segments"]
    fig_rfm = px.pie(
        values=list(rfm_counts.values()),
        names=list(rfm_counts.keys()),
        title="Customer Base Segmentation (RFM Cohorts)",
        hole=0.35
    )
    fig_rfm.update_layout(template="plotly_dark")
    st.plotly_chart(fig_rfm, use_container_width=True)

    st.subheader("High-Value Depositor Early-Warning Table")
    at_risk_df = filtered_df[filtered_df["churn_status"] == 1].sort_values("deposit_balance", ascending=False).head(15)
    st.dataframe(at_risk_df[["customer_id", "region", "account_tier", "deposit_balance", "recency_days", "frequency_txns", "rfm_segment"]])

# -------------------------------------------------------------
# TAB 4: STRESS-TEST SIMULATOR
# -------------------------------------------------------------
with tab4:
    st.subheader("Macroeconomic Policy & Rate Shock Simulator")
    
    s_col1, s_col2 = st.columns([1, 2])
    with s_col1:
        rate_shift = st.slider("Interest Rate Shift (bps)", -200, 300, 100, step=25)
        fico_cutoff = st.slider("Minimum FICO Approval Cutoff", 550, 740, 640, step=10)
        macro_env = st.selectbox("Macro Condition", ["Baseline", "Mild Recession (+1.5% Unemp)", "Stagflation (+3.5% Unemp)"])
        
    with s_col2:
        projected_nim = 3.78 + (rate_shift * 0.45 / 100.0)
        fico_diff = 640 - fico_cutoff
        macro_mult = 1.8 if "Stagflation" in macro_env else (0.8 if "Mild" in macro_env else 0.0)
        proj_default = max(0.8, 3.55 - (fico_diff * 0.035) + macro_mult)
        bad_debt_mitigated = ((3.55 - proj_default) / 100.0 * 936.5)
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Projected NIM", f"{projected_nim:.2f}%", f"{rate_shift} bps")
            st.metric("Loan Approval Rate", f"{max(45, 85 - (fico_cutoff - 600)*0.28):.1f}%")
        with m2:
            st.metric("Projected Default Rate", f"{proj_default:.2f}%", f"{3.55 - proj_default:+.2f}% vs Base")
            st.metric("Bad Debt Mitigated", f"${bad_debt_mitigated:.2f}M")

# -------------------------------------------------------------
# TAB 5: SQL ARCHITECTURE
# -------------------------------------------------------------
with tab5:
    st.subheader("Enterprise Star Schema & Analytical Queries")
    st.markdown("Designed for Snowflake, BigQuery, and PostgreSQL OLAP environments.")
    
    st.code("""
-- Executive Portfolio Rollup CTE
WITH PortfolioRollup AS (
    SELECT 
        l.loan_type,
        COUNT(l.loan_id) AS total_loans,
        SUM(l.principal_amount) AS total_disbursed_usd,
        ROUND(SUM(l.principal_amount * l.interest_rate_pct) / NULLIF(SUM(l.principal_amount), 0), 2) AS weighted_avg_rate_pct,
        SUM(CASE WHEN l.days_past_due >= 90 THEN l.principal_amount ELSE 0 END) AS npl_principal_usd
    FROM banking_dw.fact_loans l
    GROUP BY l.loan_type
)
SELECT * FROM PortfolioRollup;
    """, language="sql")
