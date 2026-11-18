"""
FinVanguard 360 - Customer Churn Propensity & Attrition Model
Analyzes customer tenure, account balance, digital activity, and RFM metrics
to flag high-value depositors at imminent risk of attrition.
"""

import os
import csv
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, z))))

def run_churn_analysis():
    summary_path = os.path.join(DATA_PROC_DIR, "customer_risk_summary.csv")
    customers = []
    with open(summary_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            customers.append(r)
            
    # Logistic Churn Propensity weights
    # Risk factors: inactivity, low products, dormant recency, low credit score
    high_value_at_risk = []
    total_at_risk_deposits = 0.0
    
    for c in customers:
        is_active = int(c["is_active_member"])
        num_prod = int(c["num_products"])
        deposit = float(c["deposit_balance"])
        recency = int(c["recency_days"])
        tenure = int(c["tenure_months"])
        
        # Linear score
        z = -1.2
        if is_active == 0: z += 1.45
        if num_prod == 1: z += 0.95
        elif num_prod >= 4: z -= 0.85
        if recency > 90: z += 0.75
        if tenure < 12: z += 0.40
        if deposit < 2000: z += 0.50
        
        churn_prob = round(sigmoid(z), 3)
        
        # Identify High-Value At-Risk accounts: Deposit > $25,000 and churn_prob >= 0.50
        if deposit >= 25000 and churn_prob >= 0.50:
            high_value_at_risk.append({
                "customer_id": c["customer_id"],
                "account_tier": c["account_tier"],
                "region": c["region"],
                "deposit_balance": deposit,
                "num_products": num_prod,
                "is_active_member": is_active,
                "recency_days": recency,
                "churn_probability": churn_prob
            })
            total_at_risk_deposits += deposit
            
    high_value_at_risk.sort(key=lambda x: x["deposit_balance"], reverse=True)
    
    print("==================================================")
    print("      CUSTOMER CHURN & ATTRITION ANALYSIS         ")
    print("==================================================")
    print(f"  • High-Value At-Risk Customers: {len(high_value_at_risk):,}")
    print(f"  • Total At-Risk Deposit Capital: ${total_at_risk_deposits:,.2f}")
    print(f"  • Top 5 At-Risk Depositors:")
    for top in high_value_at_risk[:5]:
        print(f"    - [{top['customer_id']}] {top['account_tier']} ({top['region']}): ${top['deposit_balance']:,.2f} | Churn Prob: {top['churn_probability']*100:.1f}%")
    print("==================================================")

if __name__ == "__main__":
    run_churn_analysis()
