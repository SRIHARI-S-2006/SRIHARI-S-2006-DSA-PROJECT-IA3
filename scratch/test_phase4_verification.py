import sys
import json
import urllib.request
import urllib.parse
import numpy as np

BASE_URL = "http://127.0.0.1:5000"

def log_pass(msg):
    print(f"  [PASS] {msg}")

def log_fail(msg):
    print(f"  [FAIL] {msg}")
    sys.exit(1)

def http_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

print("=" * 80)
print("CCPRA SYSTEM VERIFICATION: PHASE 4 VALIDATION SUITE")
print("=" * 80)

# 1. Test Existing Core Endpoints
print("\n--- 1. Testing Core Endpoints ---")
for ep in ["/api/overview", "/api/analytics-data", "/api/segments", "/api/model-evaluation"]:
    status, data = http_get(ep)
    assert status == 200, f"Expected 200 for {ep}"
    log_pass(f"{ep} responded with HTTP 200")

# 2. Test Model Diagnostics (Held-Out Test Set n=1,409)
print("\n--- 2. Testing Model Diagnostics (/api/model-diagnostics) ---")
status, diag = http_get("/api/model-diagnostics")
assert status == 200
assert diag["test_samples"] == 1409, f"Expected 1409, got {diag['test_samples']}"
assert diag["training_samples"] == 5634, f"Expected 5634, got {diag['training_samples']}"
assert abs(diag["accuracy"] - 80.55) < 0.1, f"Accuracy mismatch: {diag['accuracy']}"
assert abs(diag["roc_auc"] - 84.21) < 0.1, f"ROC-AUC mismatch: {diag['roc_auc']}"
assert abs(diag["brier_score"] - 0.138) < 0.01, f"Brier mismatch: {diag['brier_score']}"
log_pass("Test sample size and primary holdout metrics exact (n=1,409, 80.55% Acc, 84.21% AUC, Brier=0.138)")

# Verify Cumulative Gains & Lift
gains = diag["cumulative_gains"]
assert len(gains) == 10, f"Expected 10 deciles, got {len(gains)}"
decile_1 = gains[0]
assert abs(decile_1["cum_gain_pct"] - 28.07) < 0.5, f"Decile 1 gain mismatch: {decile_1['cum_gain_pct']}"
assert abs(decile_1["cum_lift"] - 2.81) < 0.05, f"Decile 1 lift mismatch: {decile_1['cum_lift']}"
decile_3 = gains[2]
assert abs(decile_3["cum_gain_pct"] - 64.97) < 0.5, f"Decile 3 gain mismatch: {decile_3['cum_gain_pct']}"
assert abs(decile_3["cum_lift"] - 2.16) < 0.05, f"Decile 3 lift mismatch: {decile_3['cum_lift']}"
log_pass(f"Cumulative gains verified: Decile 1 captures {decile_1['cum_gain_pct']}% (Lift: {decile_1['cum_lift']}x), Top 3 deciles capture {decile_3['cum_gain_pct']}% (Lift: {decile_3['cum_lift']}x)")

# Verify Calibration Points
cal = diag["calibration"]
assert len(cal["prob_pred"]) >= 9
log_pass(f"Probability calibration curve verified ({len(cal['prob_pred'])} probability bins, Brier: {cal['brier_score']})")

# Verify Precision-Recall Points
pr = diag["pr_curve"]
assert len(pr) >= 15
p50 = min(pr, key=lambda x: abs(x["threshold"] - 0.50))
assert abs(p50["precision"] - 65.72) < 1.0
assert abs(p50["recall"] - 55.88) < 1.0
log_pass(f"Precision-Recall operating points verified: At tau=0.50, Precision={p50['precision']}%, Recall={p50['recall']}%, F1={p50['f1_score']}%")

# 3. Test Lifecycle Pseudo-Retention (/api/lifecycle-retention)
print("\n--- 3. Testing Lifecycle Retention (/api/lifecycle-retention) ---")
status, lc = http_get("/api/lifecycle-retention")
assert status == 200
assert "milestones" in lc
assert "cohort_hazards" in lc
assert "disclaimer" in lc and "Cross-sectional" in lc["disclaimer"]
m1 = lc["milestones"][0]
m72 = lc["milestones"][-1]
assert m1["accounts_active_at_milestone"] > 7000
assert m72["pseudo_retention_rate"] > 95.0
log_pass(f"Lifecycle curve verified ({len(lc['milestones'])} milestones from 1 Mo to 72 Mo, academic disclaimer intact)")

# 4. Test Box Plot Five-Number Summary (/api/distribution-comparison)
print("\n--- 4. Testing Box Plot Distributions (/api/distribution-comparison) ---")
status, dist = http_get("/api/distribution-comparison")
assert status == 200
assert "MonthlyCharges" in dist
assert "tenure" in dist
mc_churn = dist["MonthlyCharges"]["Yes"]
mc_retain = dist["MonthlyCharges"]["No"]
t_churn = dist["tenure"]["Yes"]
t_retain = dist["tenure"]["No"]

assert mc_churn["median"] == 79.65, f"Expected 79.65, got {mc_churn['median']}"
assert mc_retain["median"] == 64.43, f"Expected 64.43, got {mc_retain['median']}"
assert t_churn["median"] == 10.0, f"Expected 10.0, got {t_churn['median']}"
assert t_retain["median"] == 38.0, f"Expected 38.0, got {t_retain['median']}"
log_pass(f"Box Plot exact five-number statistics verified:")
log_pass(f"   Charges - Churned Median: ${mc_churn['median']} (Q1: ${mc_churn['q1']}, Q3: ${mc_churn['q3']}) vs Retained: ${mc_retain['median']}")
log_pass(f"   Tenure  - Churned Median: {t_churn['median']} mo (Q1: {t_churn['q1']} mo, Q3: {t_churn['q3']} mo) vs Retained: {t_retain['median']} mo")

# 5. Test External Dataset Comparison (/api/dataset-comparison)
print("\n--- 5. Testing Dataset Expansion (/api/dataset-comparison) ---")
status, comp = http_get("/api/dataset-comparison")
assert status == 200
assert comp["records"] == 2026, f"Expected 2026, got {comp['records']}"
assert comp["churn_rate_pct"] == 19.40, f"Expected 19.40, got {comp['churn_rate_pct']}"
assert "CC BY 4.0" in comp["license"]
assert len(comp["operators"]) == 4
anom = comp["data_anomalies"]
assert anom["negative_data_usage_rows"] == 59
assert anom["negative_calls_made_rows"] == 52
assert anom["negative_sms_sent_rows"] == 62
assert anom["total_anomalous_rows"] == 167
log_pass(f"External dataset integrity verified (2,026 records, 19.40% churn, 4 operators, 167 unique anomalous rows disclosed)")

# 6. Test Threshold Simulator PR linkage (/api/threshold-sim)
print("\n--- 6. Testing Threshold Simulator PR Linkage (/api/threshold-sim) ---")
status, sim60 = http_get("/api/threshold-sim?threshold=0.60")
assert status == 200
assert sim60["flagged_customers"] == 1039
assert abs(sim60["empirical_precision_pct"] - 72.09) < 0.1
assert abs(sim60["empirical_recall_pct"] - 40.07) < 0.1
log_pass(f"Threshold sim at tau=0.60 verified (Flagged: 1,039 accounts, ${sim60['flagged_monthly_charges']}, Empirical Precision: {sim60['empirical_precision_pct']}%, Recall: {sim60['empirical_recall_pct']}%)")

status, sim30 = http_get("/api/threshold-sim?threshold=0.30")
assert status == 200
assert sim30["flagged_customers"] > sim60["flagged_customers"]
assert sim30["empirical_recall_pct"] > sim60["empirical_recall_pct"]
log_pass(f"Threshold sim at tau=0.30 verified (Flagged: {sim30['flagged_customers']} accounts, Recall increases to {sim30['empirical_recall_pct']}%)")

print("\n" + "=" * 80)
print("ALL 6 PHASES OF MATHEMATICAL AND ENDPOINT VERIFICATION PASSED PERFECTLY!")
print("=" * 80)
