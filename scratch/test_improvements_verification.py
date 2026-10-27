import sys
import json
import math
import urllib.request
import urllib.parse
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

def log_pass(msg):
    print(f" [PASS] {msg}")

def log_fail(msg):
    print(f" [FAIL] {msg}")
    sys.exit(1)

def http_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode('utf-8')

def http_post(path, data):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode('utf-8')

print("=" * 70)
print("TEST SUITE 1: IMPROVEMENT 1 — CUSTOMER-SPECIFIC MODEL EXPLAINABILITY")
print("=" * 70)

high_risk_payload = {
    "gender": "Female",
    "SeniorCitizen": "1",
    "Partner": "No",
    "Dependents": "No",
    "tenure": "2",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": "95.50",
    "TotalCharges": "191.00"
}

status, body = http_post("/api/predict", high_risk_payload)
assert status == 200, f"Expected 200, got {status}"
data = json.loads(body)
assert data["status"] == "success", "Expected status=success"

pred = data["prediction"]
expl = data["explanation"]
print(f"High-Risk Customer Predicted Churn: {pred['churn_risk_percentage']}% (Prob: {pred['churn_probability']})")
print(f"Decision Score (z): {expl['decision_score']:.4f}, Reconstructed: {expl['reconstructed_score']:.4f}")

# Math check: sigmoid(decision_score) == churn_probability
sigmoid_prob = 1.0 / (1.0 + math.exp(-expl["decision_score"]))
abs_prob_diff = abs(sigmoid_prob - pred["churn_probability"])
if abs_prob_diff < 1e-4:
    log_pass(f"Probability reconstruction exact (diff: {abs_prob_diff:.2e})")
else:
    log_fail(f"Probability reconstruction failed: {abs_prob_diff}")

# Math check: reconstructed_score == decision_score
score_diff = abs(expl["decision_score"] - expl["reconstructed_score"])
if score_diff < 1e-5:
    log_pass(f"Decision score linear reconstruction exact (diff: {score_diff:.2e})")
else:
    log_fail(f"Decision score reconstruction failed: {score_diff}")

# Check top risk increasing
assert len(expl["top_risk_increasing"]) > 0, "Expected positive contributions"
assert len(expl["top_risk_increasing"]) <= 3, "Max 3 positive contributions"
for item in expl["top_risk_increasing"]:
    assert item["contribution"] > 0, "Risk increasing contribution must be positive"
    print(f"   [+] Risk Elevator: {item['label']} => +{item['contribution']:.4f}")
log_pass("Top risk increasing contributions verified (+ log-odds, max 3)")

# Check top risk reducing
assert len(expl["top_risk_reducing"]) <= 3, "Max 3 negative contributions"
for item in expl["top_risk_reducing"]:
    assert item["contribution"] < 0, "Risk reducing contribution must be negative"
    print(f"   [-] Protective Factor: {item['label']} => {item['contribution']:.4f}")
log_pass("Top protective contributions verified (- log-odds, max 3)")

assert "disclaimer" in expl and "causal" in expl["disclaimer"], "Expected causality disclaimer"
log_pass("Methodology disclaimer present in payload")

# Low-risk customer test
low_risk_payload = {
    "gender": "Male",
    "SeniorCitizen": "0",
    "Partner": "Yes",
    "Dependents": "Yes",
    "tenure": "60",
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "Yes",
    "DeviceProtection": "Yes",
    "TechSupport": "Yes",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Two year",
    "PaperlessBilling": "No",
    "PaymentMethod": "Credit card (automatic)",
    "MonthlyCharges": "65.00",
    "TotalCharges": "3900.00"
}

status2, body2 = http_post("/api/predict", low_risk_payload)
assert status2 == 200
data2 = json.loads(body2)
pred2 = data2["prediction"]
expl2 = data2["explanation"]
print(f"Low-Risk Customer Predicted Churn: {pred2['churn_risk_percentage']}% (Prob: {pred2['churn_probability']})")
print(f"Decision Score (z): {expl2['decision_score']:.4f}, Reconstructed: {expl2['reconstructed_score']:.4f}")

assert pred2["churn_risk_percentage"] < 10.0, "Expected low risk < 10%"
assert expl2["decision_score"] < 0, "Expected negative decision score for low risk"
log_pass("Customer-specific attribution verified across contrasting customer presets")

print("\n" + "=" * 70)
print("TEST SUITE 2: IMPROVEMENT 2 — CHART-TO-CUSTOMER DRILL-DOWN FILTERS")
print("=" * 70)

# Drill-down test 1: Month-to-month + Fiber optic
q1 = urllib.parse.urlencode({"contract": "Month-to-month", "internet": "Fiber optic", "page": 1, "page_size": 20})
status, body = http_get(f"/api/customers?{q1}")
assert status == 200
res1 = json.loads(body)
assert res1["total"] > 0
for c in res1["items"]:
    assert c["Contract"] == "Month-to-month", f"Contract mismatch: {c['Contract']}"
    assert c["InternetService"] == "Fiber optic", f"Internet mismatch: {c['InternetService']}"
log_pass(f"Drilldown 1 (Month-to-month + Fiber optic): Returned {res1['total']} matching records with 100% filter adherence")

# Drill-down test 2: High Risk filter
q2 = urllib.parse.urlencode({"risk": "High Risk", "page": 1, "page_size": 20})
status, body = http_get(f"/api/customers?{q2}")
assert status == 200
res2 = json.loads(body)
assert res2["total"] == 1039, f"Expected exactly 1,039 high-risk records, got {res2['total']}"
for c in res2["items"]:
    assert c["Churn_Risk_Category"] == "High Risk"
log_pass(f"Drilldown 2 (High Risk tier): Returned exact portfolio count 1,039 records")

# Drill-down test 3: Two year contract
q3 = urllib.parse.urlencode({"contract": "Two year", "page": 1, "page_size": 20})
status, body = http_get(f"/api/customers?{q3}")
assert status == 200
res3 = json.loads(body)
assert res3["total"] == 1695, f"Expected 1,695 Two-year contracts, got {res3['total']}"
for c in res3["items"]:
    assert c["Contract"] == "Two year"
log_pass(f"Drilldown 3 (Two year contract): Returned exact portfolio count 1,695 records")

# CSV export adherence
csv_q = urllib.parse.urlencode({"contract": "Month-to-month", "internet": "Fiber optic"})
status, body = http_get(f"/api/customers/export?{csv_q}")
assert status == 200
lines = body.strip().split("\n")
assert len(lines) == res1["total"] + 1, f"CSV lines ({len(lines)}) should match total + header ({res1['total'] + 1})"
log_pass(f"CSV export adhered to drill-down filters ({len(lines)-1} data rows exported)")

print("\n" + "=" * 70)
print("TEST SUITE 3: IMPROVEMENT 3 — PORTFOLIO BENCHMARKING & TABLE FORMATTING")
print("=" * 70)

df = pd.read_csv("data/powerbi/customer_churn_analytics.csv")
portfolio_mean_charges = df["MonthlyCharges"].mean()
portfolio_median_charges = df["MonthlyCharges"].median()
portfolio_mean_tenure = df["tenure"].mean()
portfolio_median_tenure = df["tenure"].median()

cohort_0_12 = df[df["tenure"] <= 12]
cohort_0_12_rate = (cohort_0_12["Churn"] == "Yes").mean() * 100

print(f"Portfolio Mean Monthly Charges: ${portfolio_mean_charges:.2f} (App baseline: $64.76)")
print(f"Portfolio Mean Tenure: {portfolio_mean_tenure:.1f} Mo, Median: {portfolio_median_tenure:.1f} Mo (App baseline: 32.4 mo, 29.0 mo)")
print(f"Cohort 0-12 Mo Churn Rate: {cohort_0_12_rate:.1f}% (App baseline: 47.4%)")

assert abs(portfolio_mean_charges - 64.76) < 0.01, "Monthly charges benchmark mismatch"
assert abs(portfolio_mean_tenure - 32.4) < 0.1, "Tenure mean benchmark mismatch"
assert abs(portfolio_median_tenure - 29.0) < 0.1, "Tenure median benchmark mismatch"
assert abs(cohort_0_12_rate - 47.4) < 0.1, "Cohort churn benchmark mismatch"
log_pass("Contextual portfolio benchmarks match dataset ground truth with 100% precision")

print("\n" + "=" * 70)
print("ALL IMPROVEMENTS VERIFICATION COMPLETED SUCCESSFULLY!")
print("=" * 70)
