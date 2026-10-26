# CCPRA Web Application - College Project Demonstration

An interactive, responsive Flask web application for the **Customer Churn Prediction & Retention Analytics (CCPRA)** system.

---

## Architecture

- **Backend**: Python 3.12, Flask, Pandas, Scikit-Learn, Joblib
- **Frontend**: HTML5, Vanilla CSS3 (modern dark navy dashboard theme), JavaScript (ES6+)
- **Visualizations**: Chart.js (Donut distributions, cohort churn bars)
- **Machine Learning**: Pre-trained serialized pipeline (`models/selected_churn_model.joblib`), no model retraining required.
- **Data Source**: Local verified dataset (`data/powerbi/customer_churn_analytics.csv`), zero database requirement.

---

## Features

1. **Executive Dashboard Overview & Revenue-at-Risk Intelligence**:
   - High-level KPIs: Total Customer Base (7,043), Actual Churn Rate (26.54%), High-Risk Customers (1,039), Total Monthly Base MRR ($456,116.60).
   - **Deterministic Revenue Exposure**: $85,546.25/mo ($1.03M/yr annualized) directly tied to accounts predicting $\ge 60\%$ churn probability (18.76% of total revenue).
   - **Probabilistic Expected Loss**: $139,980.72/mo ($1.68M/yr annualized) calculated via $\mathbb{E}[\text{Loss}] = \sum (P_i \times \text{Charges}_i)$ using predicted churn probabilities.
   - Comprehensive methodology cards explaining formulas, risk tier economics, and retention intervention assumptions.
   - Summary donut charts for actual outcome and model predicted risk tiers.

2. **Visual & Cohort Analytics & Customer Explorer**:
   - Interactive charts for Churn by Contract, Tenure lifecycle cohort, Internet service, and Payment method.
   - **Customer Analytics Explorer**: Search by ID, filter by risk tier/contract/churn status, and **sort any column ascending/descending**.
   - **One-Click CSV Export**: Download filtered cohorts directly to CSV via `/api/customers/export`.
   - Distinct, color-coded risk indicators: Low Risk (&lt;30%, green), Medium Risk (30-59%, yellow), High Risk (≥60%, red), and Critical Priority (≥80%, crimson).

3. **Live Churn Predictor**:
   - Real-time customer risk assessment form accepting all 19 primary model features.
   - Includes one-click **Demo Presets** (High-Risk vs. Low-Risk profile) for live demonstration.
   - Immediate feedback: Churn Probability %, Risk Meter, Predicted Class, Retention Priority (P1–P4), and prescriptive rule-based action.

4. **Model Evaluation & Verification**:
   - Genuine holdout test set benchmarks (n=1,409) comparing Logistic Regression (84.21% AUC, 80.55% Accuracy, 55.88% Recall, 65.72% Precision, 60.40% F1) vs Random Forest.
   - **Side-by-Side Algorithm Comparison Bar Chart** (Chart.js) visualizing metric differences.
   - Visual 2x2 confusion matrix with complete rate breakdown (Specificity: 89.47%, Sensitivity: 55.88%, False Alarm: 10.53%, Miss Rate: 44.12%).
   - Clear distinction between holdout test performance and full-base scoring (n=7,043).

5. **Algorithms & Mathematical Formulations with Worked Examples**:
   - Academic explanations of the Sigmoid function, Log-odds, Maximum Likelihood Estimation, L2 regularization, and Decision Tree ensembles.
   - **Step-by-step worked mathematical derivations** using actual CCPRA figures for Baseline Churn Rate, Accuracy, Precision, Recall, F1-Score, and ROC-AUC.

---

## How to Run

### Step 1: Activate Virtual Environment
Open PowerShell in the project directory:
```powershell
Set-Location "c:\Users\sriha\Downloads\customer-churn-prediction-retention-analytics-main\customer-churn-prediction-retention-analytics-main"
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Web Dependencies (if not already installed)
```powershell
pip install -r requirements_web.txt
```

### Step 3: Start the Flask Web Server
```powershell
python website/app.py
```

### Step 4: Open in Web Browser
Visit:
```
http://127.0.0.1:5000
```
