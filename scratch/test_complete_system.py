import requests
import io
import json

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    print("=================================================================")
    print("CCPRA SYSTEM-WIDE VERIFICATION & AUDIT SUITE")
    print("=================================================================")

    # Test 1: Root HTML Page
    print("\n[1] Testing GET / ...")
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    html = r.text
    required_elements = [
        "Executive Overview",
        "Churn Analytics",
        "Customer Segments",
        "Revenue Intelligence",
        "Customer Explorer",
        "Prediction Lab",
        "churn-heatmap-container",
        "scatterTenureChargesChart",
        "stackedProportionChart",
        "tenureHistogramChart",
        "chargesHistogramChart",
        "segmentBubbleChart",
        "seg-compare-select-a",
        "seg-compare-select-b",
        "revenueParetoChart",
        "sim-threshold-slider",
        "subtab-batch-predictor",
        "batch-dropzone",
        "batch-results-table",
        "predictedRiskHistChart",
        "overviewChurnChart"
    ]
    for elem in required_elements:
        assert elem in html, f"Missing element in index.html: {elem}"
    print("  -> Passed. All 6 workspaces, charts, and interactive features present.")

    # Test 2: Overview API
    print("\n[2] Testing GET /api/overview ...")
    r = requests.get(f"{BASE_URL}/api/overview")
    assert r.status_code == 200
    ov = r.json()
    assert ov["total_customers"] == 7043
    assert ov["actual_churned"] == 1869
    assert ov["actual_retained"] == 5174
    assert ov["churn_rate_pct"] == 26.54
    assert ov["predicted_high_risk"] == 1039
    assert ov["monthly_revenue_at_risk"] == 85546.25
    assert ov["total_mrr"] == 456116.60
    assert ov["expected_monthly_loss"] == 139980.72
    print(f"  -> Passed. Total Customers: {ov['total_customers']}, High Risk: {ov['predicted_high_risk']}, MRR at Risk: ${ov['monthly_revenue_at_risk']}")

    # Test 3: Scatter Data API
    print("\n[3] Testing GET /api/scatter-data ...")
    r = requests.get(f"{BASE_URL}/api/scatter-data")
    assert r.status_code == 200
    sc = r.json()
    assert sc["count"] == 700
    assert len(sc["points"]) == 700
    churn_pts = sum(1 for p in sc["points"] if p["churn"] == "Yes")
    sample_rate = round(churn_pts / 700 * 100, 2)
    print(f"  -> Passed. 700 stratified sample points. Churn rate in sample: {sample_rate}% (mirrors true 26.54%).")

    # Test 4: Advanced Charts API
    print("\n[4] Testing GET /api/advanced-charts ...")
    r = requests.get(f"{BASE_URL}/api/advanced-charts")
    assert r.status_code == 200
    adv = r.json()
    assert "heatmap" in adv
    assert len(adv["heatmap"]["cells"]) == 9
    assert "tenure_histogram" in adv
    assert len(adv["tenure_histogram"]["bins"]) == 6
    assert "charges_histogram" in adv
    assert len(adv["charges_histogram"]["bins"]) == 5
    assert "stacked_100" in adv
    assert "contract" in adv["stacked_100"]
    assert "bubble_segments" in adv
    assert len(adv["bubble_segments"]) == 9
    assert "pareto" in adv
    assert len(adv["pareto"]["labels"]) == 4
    assert adv["pareto"]["cumulative_percentages"][-1] == 100.0
    assert "predicted_risk_histogram" in adv
    assert len(adv["predicted_risk_histogram"]["bins"]) == 10
    print(f"  -> Passed. Heatmap (9 cells), Pareto (4 channels), Bubble (9 segments), Histograms validated.")

    # Test 5: Operational Threshold Simulator API
    print("\n[5] Testing GET /api/threshold-sim ...")
    r = requests.get(f"{BASE_URL}/api/threshold-sim?threshold=0.60")
    assert r.status_code == 200
    sim_base = r.json()
    assert sim_base["flagged_customers"] == 1039
    assert sim_base["flagged_monthly_charges"] == 85546.25
    assert sim_base["delta_customers"] == 0
    assert sim_base["delta_charges"] == 0.0

    r = requests.get(f"{BASE_URL}/api/threshold-sim?threshold=0.50")
    assert r.status_code == 200
    sim_50 = r.json()
    assert sim_50["flagged_customers"] > 1039
    print(f"  -> Passed. Threshold 0.60: {sim_base['flagged_customers']} accts (${sim_base['flagged_monthly_charges']}). Threshold 0.50: {sim_50['flagged_customers']} accts (${sim_50['flagged_monthly_charges']}).")

    # Test 6: Batch Template, Scoring, and Download
    print("\n[6] Testing Batch Customer Prediction Workflow ...")
    tmpl_res = requests.get(f"{BASE_URL}/api/predict-batch/template")
    assert tmpl_res.status_code == 200
    tmpl_csv = tmpl_res.text
    assert "customerID" in tmpl_csv
    assert "SeniorCitizen" in tmpl_csv
    lines = tmpl_csv.strip().split("\n")
    assert len(lines) == 6 # Header + 5 sample rows

    # Score batch with template
    files = {"file": ("test_batch.csv", io.BytesIO(tmpl_csv.encode("utf-8")), "text/csv")}
    batch_res = requests.post(f"{BASE_URL}/api/predict-batch", files=files)
    assert batch_res.status_code == 200
    batch_json = batch_res.json()
    assert batch_json["status"] == "success"
    assert batch_json["total_scored"] == 5
    assert len(batch_json["preview_rows"]) == 5
    assert "Predicted_Probability" in batch_json["preview_rows"][0]
    assert "Prescribed_Action" in batch_json["preview_rows"][0]

    # Test download
    dl_res = requests.get(f"{BASE_URL}/api/predict-batch/download")
    assert dl_res.status_code == 200
    assert "attachment" in dl_res.headers.get("Content-Disposition", "")
    assert "Predicted_Churn_Probability" in dl_res.text
    print(f"  -> Passed. Scored 5 records. Predicted churners: {batch_json['predicted_churners']}, Downloadable CSV streamed successfully.")

    # Test 7: Batch Error Handling with Missing Columns
    print("\n[7] Testing Batch Error Handling ...")
    bad_csv = "customerID,tenure\n1234,5\n"
    files = {"file": ("bad_batch.csv", io.BytesIO(bad_csv.encode("utf-8")), "text/csv")}
    bad_res = requests.post(f"{BASE_URL}/api/predict-batch", files=files)
    assert bad_res.status_code == 400
    bad_json = bad_res.json()
    assert bad_json["status"] == "error"
    assert "missing" in bad_json["message"].lower() and "required" in bad_json["message"].lower()
    print(f"  -> Passed. Gracefully returned 400 with missing columns: {bad_json['message']}")

    # Test 8: Single Customer Prediction API
    print("\n[8] Testing POST /api/predict ...")
    sample_payload = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 2,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.70,
        "TotalCharges": 151.65
    }
    pred_res = requests.post(f"{BASE_URL}/api/predict", json=sample_payload)
    assert pred_res.status_code == 200
    pred = pred_res.json()["prediction"]
    assert pred["predicted_churn_probability"] > 0.60
    assert pred["predicted_churn_class"] == "Yes"
    assert pred["churn_risk_category"] == "High Risk"
    print(f"  -> Passed. Prediction prob: {pred['predicted_churn_probability']} ({pred['churn_risk_category']}).")

    # Test 9: Model Evaluation API & Confusion Matrix
    print("\n[9] Testing GET /api/model-evaluation ...")
    me_res = requests.get(f"{BASE_URL}/api/model-evaluation")
    assert me_res.status_code == 200
    me = me_res.json()
    cm = me.get("confusion_matrix") or me.get("confusion_matrix_test")
    cm_total = cm["true_negatives"] + cm["false_positives"] + cm["false_negatives"] + cm["true_positives"]
    assert cm_total == 1409
    assert cm["true_negatives"] == 926
    assert cm["false_positives"] == 109
    assert cm["false_negatives"] == 165
    assert cm["true_positives"] == 209
    lr_model = [m for m in me.get("models", []) if m.get("selected")][0]
    assert lr_model["accuracy"] == 0.8055
    assert lr_model["roc_auc"] == 0.8421
    print(f"  -> Passed. Confusion matrix: 926 TN + 109 FP + 165 FN + 209 TP = {cm_total} holdout records.")

    # Test 10: Customer Explorer & CSV Export
    print("\n[10] Testing Customer Explorer & Export ...")
    cust_res = requests.get(f"{BASE_URL}/api/customers?page=1&limit=15&risk=High%20Risk")
    assert cust_res.status_code == 200
    cust_data = cust_res.json()
    assert cust_data["total"] == 1039
    assert len(cust_data["items"]) == 15

    exp_res = requests.get(f"{BASE_URL}/api/customers/export?risk=High%20Risk")
    assert exp_res.status_code == 200
    assert "attachment" in exp_res.headers.get("Content-Disposition", "")
    assert len(exp_res.text.strip().split("\n")) == 1040 # 1 header + 1039 records
    print(f"  -> Passed. Filtered high risk: {cust_data['total']} accounts. CSV export: 1,039 records.")

    print("\n=================================================================")
    print("ALL 10 TEST SUITES PASSED PERFECTLY!")
    print("=================================================================")

if __name__ == "__main__":
    run_tests()
