"""
FinVanguard 360 - Realistic Banking Dataset Generator
Generates realistic retail & commercial banking data for:
- Customers (Demographics, Financial Profiles, Products, Churn)
- Loans (Portfolio, Amortization, Delinquencies, Credit Risk Grades)
- Transactions (Daily Activity, Multi-channel, Anomaly / High-Risk Flags)
"""

import os
import csv
import random
import math
from datetime import datetime, timedelta

# Set fixed seed for reproducibility
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)

NUM_CUSTOMERS = 10000
NUM_LOANS = 6500
NUM_TRANSACTIONS = 40000

REGIONS = ["Northeast", "Midwest", "South", "West", "Metro Central"]
EMPLOYMENT_TYPES = ["Salaried Full-Time", "Self-Employed", "Executive", "Freelance / Gig", "Retired"]
ACCOUNT_TIERS = ["Basic Checking", "Gold Advantage", "Platinum Preferred", "Private Wealth"]
LOAN_TYPES = ["Home Mortgage", "Auto Loan", "Personal Unsecured", "Small Business (SMB)", "Education / Student"]
TRANSACTION_CATEGORIES = [
    "Groceries & Food", "Utilities & Bills", "Travel & Airlines", "Entertainment & Dining",
    "Electronics & Retail", "Mortgage / Loan EMI", "Brokerage & Investment", "ATM Withdrawal", "Healthcare"
]
CHANNELS = ["Mobile Banking App", "Online Web Portal", "Point of Sale (POS)", "ATM Network", "In-Branch Wire"]

def generate_customers():
    print(f"[*] Generating {NUM_CUSTOMERS} customer profiles...")
    customers = []
    
    for i in range(1, NUM_CUSTOMERS + 1):
        cust_id = f"CUST-{10000 + i}"
        age = int(random.triangular(21, 75, 38))
        gender = random.choices(["Female", "Male", "Non-Binary"], weights=[49, 49, 2])[0]
        region = random.choice(REGIONS)
        emp_status = random.choices(EMPLOYMENT_TYPES, weights=[55, 20, 10, 8, 7])[0]
        
        # Income with slight right skew
        if emp_status == "Executive":
            income = round(random.uniform(120000, 340000), 2)
        elif emp_status == "Retired":
            income = round(random.uniform(28000, 85000), 2)
        elif emp_status == "Self-Employed":
            income = round(random.uniform(40000, 220000), 2)
        else:
            income = round(random.triangular(32000, 180000, 68000), 2)
            
        # Credit Score (Bell curve around 685, min 380, max 850)
        credit_score = int(random.gauss(685, 80))
        credit_score = max(380, min(850, credit_score))
        
        tenure_months = int(random.uniform(3, 120))
        
        # Account Tier influenced by income
        if income > 150000:
            tier = random.choices(ACCOUNT_TIERS, weights=[5, 15, 45, 35])[0]
        elif income > 75000:
            tier = random.choices(ACCOUNT_TIERS, weights=[20, 45, 30, 5])[0]
        else:
            tier = random.choices(ACCOUNT_TIERS, weights=[65, 25, 10, 0])[0]
            
        # Balances
        if tier == "Private Wealth":
            deposit_balance = round(random.uniform(50000, 350000), 2)
        elif tier == "Platinum Preferred":
            deposit_balance = round(random.uniform(15000, 95000), 2)
        elif tier == "Gold Advantage":
            deposit_balance = round(random.uniform(3500, 35000), 2)
        else:
            deposit_balance = round(random.uniform(350, 8500), 2)
            
        num_products = random.choices([1, 2, 3, 4, 5], weights=[35, 30, 20, 10, 5])[0]
        has_credit_card = 1 if (random.random() < 0.72 or credit_score > 700) else 0
        is_active_member = 1 if random.random() < 0.78 else 0
        
        # Churn logic: higher churn if inactive, low products, low credit score, low balance
        churn_prob = 0.08
        if is_active_member == 0:
            churn_prob += 0.22
        if num_products == 1:
            churn_prob += 0.15
        if deposit_balance < 1000:
            churn_prob += 0.12
        if credit_score < 580:
            churn_prob += 0.08
        if tenure_months < 12:
            churn_prob += 0.06
            
        is_churned = 1 if random.random() < min(0.85, churn_prob) else 0
        
        customers.append({
            "customer_id": cust_id,
            "age": age,
            "gender": gender,
            "region": region,
            "employment_status": emp_status,
            "annual_income": income,
            "credit_score": credit_score,
            "tenure_months": tenure_months,
            "account_tier": tier,
            "deposit_balance": deposit_balance,
            "num_products": num_products,
            "has_credit_card": has_credit_card,
            "is_active_member": is_active_member,
            "churn_status": is_churned
        })
        
    return customers

def generate_loans(customers):
    print(f"[*] Generating {NUM_LOANS} loans across customer base...")
    loans = []
    
    # Map customers by ID for fast lookup
    cust_map = {c["customer_id"]: c for c in customers}
    sampled_cust_ids = random.sample(list(cust_map.keys()), NUM_LOANS)
    
    for idx, c_id in enumerate(sampled_cust_ids, 1):
        loan_id = f"LN-{50000 + idx}"
        cust = cust_map[c_id]
        
        l_type = random.choices(LOAN_TYPES, weights=[32, 28, 22, 12, 6])[0]
        
        if l_type == "Home Mortgage":
            amount = round(random.triangular(120000, 650000, 280000), -2)
            term_months = random.choice([180, 240, 360])
            base_rate = 6.25
        elif l_type == "Small Business (SMB)":
            amount = round(random.triangular(30000, 250000, 85000), -2)
            term_months = random.choice([36, 60, 84])
            base_rate = 8.50
        elif l_type == "Auto Loan":
            amount = round(random.triangular(12000, 65000, 32000), -2)
            term_months = random.choice([36, 48, 60, 72])
            base_rate = 5.75
        elif l_type == "Education / Student":
            amount = round(random.triangular(8000, 75000, 28000), -2)
            term_months = random.choice([60, 120])
            base_rate = 6.80
        else: # Personal Unsecured
            amount = round(random.triangular(2500, 35000, 12000), -2)
            term_months = random.choice([12, 24, 36, 48])
            base_rate = 10.50
            
        # Interest rate adjustment based on credit score
        cs = cust["credit_score"]
        if cs >= 800:
            rate_spread = -1.25
            risk_grade = "AAA"
        elif cs >= 740:
            rate_spread = -0.60
            risk_grade = "AA"
        elif cs >= 670:
            rate_spread = 0.50
            risk_grade = "A"
        elif cs >= 620:
            rate_spread = 2.10
            risk_grade = "BBB"
        elif cs >= 580:
            rate_spread = 4.25
            risk_grade = "BB"
        elif cs >= 520:
            rate_spread = 6.75
            risk_grade = "B"
        else:
            rate_spread = 9.50
            risk_grade = "CCC"
            
        interest_rate = max(3.25, round(base_rate + rate_spread + random.uniform(-0.35, 0.35), 2))
        
        # Monthly EMI Calculation
        r_monthly = (interest_rate / 100.0) / 12.0
        n_periods = term_months
        if r_monthly > 0:
            monthly_emi = round(amount * (r_monthly * ((1 + r_monthly) ** n_periods)) / (((1 + r_monthly) ** n_periods) - 1), 2)
        else:
            monthly_emi = round(amount / n_periods, 2)
            
        # Debt-to-income calculation
        monthly_income = max(1000, cust["annual_income"] / 12.0)
        dti = round((monthly_emi + random.uniform(200, 900)) / monthly_income, 3)
        dti = min(0.85, max(0.08, dti))
        
        # Delinquency logic (Days Past Due - DPD)
        # Higher probability of delinquency if low credit score, high DTI, or high rate
        default_prob = 0.015
        if cs < 580: default_prob += 0.16
        elif cs < 640: default_prob += 0.08
        if dti > 0.45: default_prob += 0.10
        if cust["churn_status"] == 1: default_prob += 0.05
        
        rand_roll = random.random()
        if rand_roll < default_prob * 0.4:
            loan_status = "Default / Charged Off"
            dpd = int(random.uniform(91, 180))
            is_default = 1
        elif rand_roll < default_prob * 0.7:
            loan_status = "60-89 Days Delinquent"
            dpd = int(random.uniform(60, 89))
            is_default = 0
        elif rand_roll < default_prob:
            loan_status = "30-59 Days Delinquent"
            dpd = int(random.uniform(30, 59))
            is_default = 0
        elif random.random() < 0.12:
            loan_status = "Fully Paid"
            dpd = 0
            is_default = 0
        else:
            loan_status = "Current / Performing"
            dpd = 0
            is_default = 0
            
        # Loan-to-Value (LTV)
        if l_type in ["Home Mortgage", "Auto Loan"]:
            ltv = round(random.uniform(0.55, 0.95), 2)
        else:
            ltv = 1.0  # Unsecured
            
        loans.append({
            "loan_id": loan_id,
            "customer_id": c_id,
            "loan_type": l_type,
            "principal_amount": amount,
            "interest_rate_pct": interest_rate,
            "term_months": term_months,
            "monthly_installment": monthly_emi,
            "debt_to_income_ratio": dti,
            "loan_to_value_ratio": ltv,
            "days_past_due": dpd,
            "loan_status": loan_status,
            "credit_risk_grade": risk_grade,
            "is_default_event": is_default
        })
        
    return loans

def generate_transactions(customers):
    print(f"[*] Generating {NUM_TRANSACTIONS} multi-channel transactions...")
    transactions = []
    cust_ids = [c["customer_id"] for c in customers]
    
    start_date = datetime(2025, 1, 1)
    
    for i in range(1, NUM_TRANSACTIONS + 1):
        txn_id = f"TXN-{100000 + i}"
        c_id = random.choice(cust_ids)
        
        # Random date in 2025-2026
        days_offset = random.randint(0, 420)
        txn_date = start_date + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        category = random.choice(TRANSACTION_CATEGORIES)
        channel = random.choices(CHANNELS, weights=[45, 25, 18, 8, 4])[0]
        
        if category in ["Mortgage / Loan EMI", "Brokerage & Investment"]:
            amount = round(random.triangular(500, 4500, 1400), 2)
            txn_type = "Debit"
        elif category == "ATM Withdrawal":
            amount = round(random.choice([20, 40, 60, 100, 200, 300, 500]), 2)
            txn_type = "Debit"
        elif category in ["Groceries & Food", "Entertainment & Dining"]:
            amount = round(random.uniform(8.50, 185.00), 2)
            txn_type = "Debit"
        elif category == "Travel & Airlines":
            amount = round(random.triangular(120, 2200, 480), 2)
            txn_type = "Debit"
        else:
            amount = round(random.uniform(25, 650), 2)
            txn_type = random.choices(["Debit", "Credit"], weights=[82, 18])[0]
            
        # Anomaly / High-Risk Flag
        # Flagged if very high amount, international off-hours, or unusual channel
        is_high_risk = 0
        if amount > 3500 and channel in ["Mobile Banking App", "Online Web Portal"] and txn_date.hour in [1, 2, 3, 4]:
            is_high_risk = 1
        elif amount > 7500 and channel == "In-Branch Wire":
            is_high_risk = 1 if random.random() < 0.35 else 0
        elif random.random() < 0.008:
            is_high_risk = 1
            
        transactions.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "transaction_timestamp": txn_date.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "channel": channel,
            "transaction_type": txn_type,
            "amount_usd": amount,
            "is_high_risk_flag": is_high_risk
        })
        
    return transactions

def write_csv(filepath, data, fieldnames):
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] Saved {len(data)} rows to {filepath}")

def main():
    print("==================================================")
    print("FinVanguard 360 - Synthesizing Financial Dataset")
    print("==================================================")
    
    customers = generate_customers()
    loans = generate_loans(customers)
    transactions = generate_transactions(customers)
    
    write_csv(
        os.path.join(DATA_RAW_DIR, "customers.csv"),
        customers,
        list(customers[0].keys())
    )
    
    write_csv(
        os.path.join(DATA_RAW_DIR, "loans.csv"),
        loans,
        list(loans[0].keys())
    )
    
    write_csv(
        os.path.join(DATA_RAW_DIR, "transactions.csv"),
        transactions,
        list(transactions[0].keys())
    )
    
    print("\n[SUCCESS] Raw banking dataset successfully compiled!")

if __name__ == "__main__":
    main()
