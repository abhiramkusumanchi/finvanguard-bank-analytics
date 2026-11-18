# FinVanguard 360° | STAR Interview Preparation Guide

This guide provides verbatim interview scripts using the **STAR Method** (*Situation, Task, Action, Result*) for technical and behavioral interviews.

---

## 🎤 Question 1: "Can you walk me through this banking analytics project on your resume?"

### 🔹 Situation:
> *"Modern commercial and retail banks manage billions in assets, but their profitability is constantly threatened by two major factors: credit defaults and customer attrition. Traditional reporting is often static, siloed between credit risk and marketing, and incapable of interactive scenario planning."*

### 🔹 Task:
> *"My goal was to architect **FinVanguard 360°**, an end-to-end commercial banking intelligence platform that unites credit risk assessment, customer behavioral churn, transaction anomaly detection, and macroeconomic stress-testing into a single executive command center."*

### 🔹 Action:
> *"1. **Data Modeling & Architecture:** I engineered a 3NF Star Schema warehouse in SQL containing 10,000 customers, 6,500 loan facilities ($936M+ volume), and 40,000 multi-channel transactions.*
> *2. **Credit Risk & Basel Scoring:** I designed a statistical credit scoring engine modeling Days Past Due (30/60/90+ DPD roll-rates) and calculated Basel II Expected Loss ($EL = PD \times LGD \times EAD$). The model achieved a 0.715 ROC-AUC and 33.2% KS separation.*
> *3. **RFM & Churn Modeling:** I implemented an RFM segmentation algorithm using SQL window functions (`NTILE(5)`) and logistic churn scoring, which isolated 1,422 high-net-worth depositors with a >50% churn propensity, representing $115.9M in deposit flight risk.*
> *4. **Interactive BI & Stress-Testing:** I developed an interactive web dashboard with dynamic sliders enabling risk committees to test interest rate shifts (+/- 300 bps) and FICO cutoffs, instantly projecting Net Interest Margin (NIM) and bad debt mitigation."*

### 🔹 Result:
> *"The platform delivered real-time visibility across $1.35B in Total Portfolio AUM, identified $104.9M in at-risk facilities, and provided an automated underwriting tool that could pre-approve 82% of applications while reducing projected default losses by $2.84M."*

---

## 🎤 Question 2: "How did you build the Credit Risk Scoring model and evaluate its performance?"

### Answer Script:
> *"In banking, credit risk modeling revolves around the Basel regulatory framework. I modeled the **Probability of Default (PD)** as a function of the applicant's credit score (FICO), Debt-to-Income (DTI) ratio, Loan-to-Value (LTV), and whether the facility was secured (like a mortgage) or unsecured (like a personal loan).*
> 
> *To evaluate the scorecard:*
> * *I didn't just look at accuracy, because default events in banking are imbalanced (around 3.5% in our portfolio).*
> * *Instead, I evaluated the **ROC-AUC (0.715)** and the **Gini Coefficient (0.429)** to measure ranking discrimination.*
> * *I also computed the **Kolmogorov-Smirnov (KS) statistic (33.2%)**, which is the banking industry standard for measuring the maximum separation between the cumulative distribution of 'good' and 'bad' borrowers.*
> * *Finally, I calculated the regulatory **Expected Loss ($EL$)** by multiplying $PD \times LGD \times EAD$, where $LGD$ was set to 20% for secured loans and 50% for unsecured loans."*

---

## 🎤 Question 3: "How did you handle RFM segmentation in SQL and why was it valuable?"

### Answer Script:
> *"RFM stands for Recency, Frequency, and Monetary value. In SQL, I used Common Table Expressions (CTEs) and the `NTILE(5) OVER(...)` window function:*
> * *For **Recency**, I calculated the days elapsed since the customer's last debit transaction (`6 - NTILE(5) OVER(ORDER BY recency_days ASC)` so that fewer days gave a higher score).*
> * *For **Frequency**, I aggregated the total count of transactions.*
> * *For **Monetary**, I summed total debit volume.*
> 
> *The real business value came from cross-referencing RFM cohorts with deposit balances. We found that 1,422 accounts had high balances (over $25,000, totaling $115.9M) but hadn't transacted digitally in over 90 days. In retail banking, digital dormancy is the #1 leading indicator of imminent account closure. By routing these accounts to Relationship Managers for personalized retention, the bank could prevent substantial deposit runoff."*

---

## 🎤 Question 4: "What was the most challenging technical aspect of the project?"

### Answer Script:
> *"The most challenging aspect was designing the **Macroeconomic Stress-Testing Engine** to respond dynamically in real-time on the client side without lag.*
> 
> *When interest rates shift or credit score cutoffs change, it creates interdependent second-order effects: higher rates expand Net Interest Margin (NIM) on performing loans, but they also increase debt service burdens on variable-rate borrowers, elevating default rates. I mathematically calibrated the trade-off matrix between loan acceptance volume, expected interest revenue, and loan loss provisioning so that adjusting a slider instantly updates projected balance sheet metrics."*
