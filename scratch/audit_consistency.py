import json
import math
import joblib
import pandas as pd
import numpy as np
import urllib.request

BASE_DIR = r"c:\Users\sriha\Downloads\customer-churn-prediction-retention-analytics-main\customer-churn-prediction-retention-analytics-main"
pipeline = joblib.load(f"{BASE_DIR}/models/selected_churn_model.joblib")
preprocessor = pipeline.named_steps['preprocessor']
classifier = pipeline.named_steps['classifier']

# Input 1: EXACT UI High-Risk Preset (from preset-high-risk in app.js)
preset_input = {
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

# Input 2: Custom verification test input from scratch/test_improvements_verification.py
custom_input = {
    "gender": "Female",
    "SeniorCitizen": 1,
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
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.50,
    "TotalCharges": 191.00
}

def audit_input(name, input_data):
    print("=" * 80)
    print(f"AUDIT FOR: {name}")
    print("=" * 80)
    
    df = pd.DataFrame([input_data])
    
    # 1. Pipeline predict_proba and decision_function
    proba_pipeline = float(pipeline.predict_proba(df)[0][1])
    decision_score_model = float(pipeline.decision_function(df)[0])
    
    # 2. Probability reconstructed from decision_score using sigmoid
    sigmoid_prob = 1.0 / (1.0 + math.exp(-decision_score_model))
    
    # 3. Decision score reconstructed from intercept + sum(contributions)
    X_trans = preprocessor.transform(df)
    dense_vec = X_trans.toarray()[0] if hasattr(X_trans, "toarray") else X_trans[0]
    intercept = float(classifier.intercept_[0])
    coefs = classifier.coef_[0]
    all_contribs = coefs * dense_vec
    reconstructed_decision_score = float(intercept + np.sum(all_contribs))
    
    # 4. Call live Flask API (/api/predict)
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({k: str(v) for k, v in input_data.items()}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        api_data = json.loads(resp.read().decode('utf-8'))
        
    api_pred = api_data["prediction"]
    api_expl = api_data["explanation"]
    
    # What frontend displays:
    # app.js:
    # probPct.textContent = `${pred.churn_risk_percentage}%`
    # scoreVal.textContent = `${s >= 0 ? '+' : ''}${s.toFixed(2)}`
    frontend_displayed_prob_str = f"{api_pred['churn_risk_percentage']}%"
    frontend_displayed_score_str = f"{api_expl['decision_score']:+.2f}"
    
    print(f"1. Predicted probability from pipeline:                      {proba_pipeline:.6f} ({proba_pipeline*100:.2f}%)")
    print(f"2. Decision score from model (decision_function):           {decision_score_model:+.6f}")
    print(f"3. Probability reconstructed via sigmoid:                   {sigmoid_prob:.6f} ({sigmoid_prob*100:.2f}%)")
    print(f"4. Decision score reconstructed (intercept + sum contribs): {reconstructed_decision_score:+.6f}")
    print(f"5. Probability returned by /api/predict:                    {api_pred['churn_probability']:.6f} (display: {api_pred['churn_risk_percentage']}%)")
    print(f"6. Decision score returned by /api/predict:                 {api_expl['decision_score']:+.6f} (display: {frontend_displayed_score_str})")
    print(f"7. Frontend Displayed Probability:                          {frontend_displayed_prob_str}")
    print(f"8. Frontend Displayed Decision Score:                       {frontend_displayed_score_str}")
    
    # Verification checks
    assert abs(proba_pipeline - sigmoid_prob) < 1e-10, "Sigmoid prob mismatch"
    assert abs(decision_score_model - reconstructed_decision_score) < 1e-12, "Reconstructed decision score mismatch"
    assert abs(api_pred['churn_probability'] - proba_pipeline) < 1e-4, "API prob mismatch"
    assert abs(api_expl['decision_score'] - decision_score_model) < 1e-4, "API score mismatch"
    assert frontend_displayed_score_str == f"{decision_score_model:+.2f}", "Frontend score format mismatch"
    print("\n -> ALL VALUES AGREE WITH ZERO DISCREPANCY!\n")

audit_input("A. UI High-Risk Preset (#preset-high-risk)", preset_input)
audit_input("B. Custom Test Script Payload (Senior=1, Streaming=Yes, Charges=95.50)", custom_input)
