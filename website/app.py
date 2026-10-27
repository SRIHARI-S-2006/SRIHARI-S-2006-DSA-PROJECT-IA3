"""
Customer Churn Prediction & Retention Analytics (CCPRA)
Flask Web Application Backend
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, Response
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, brier_score_loss
)
from sklearn.calibration import calibration_curve

app = Flask(__name__, static_folder="static", template_folder="templates")

# Resolve project base directory relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "selected_churn_model.joblib")
ANALYTICS_CSV_PATH = os.path.join(BASE_DIR, "data", "powerbi", "customer_churn_analytics.csv")
MODEL_COMP_PATH = os.path.join(BASE_DIR, "outputs", "model_results", "model_comparison.csv")
LR_REPORT_PATH = os.path.join(BASE_DIR, "outputs", "model_results", "logistic_regression_classification_report.txt")
RF_REPORT_PATH = os.path.join(BASE_DIR, "outputs", "model_results", "random_forest_classification_report.txt")
EXTERNAL_DATA_PATH = os.path.join(BASE_DIR, "data", "external", "IndiaTelecomData.csv")

# Define exact feature inputs expected by the pipeline
NUMERICAL_FEATURES = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
CATEGORICAL_FEATURES = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]
PRIMARY_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# Load artifacts safely on startup
model_pipeline = None
df_analytics = None
model_metrics = None

try:
    if os.path.exists(MODEL_PATH):
        model_pipeline = joblib.load(MODEL_PATH)
        print(f"[CCPRA] Successfully loaded model from {MODEL_PATH}")
    else:
        print(f"[CCPRA Warning] Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"[CCPRA Error] Could not load model: {e}")

try:
    if os.path.exists(ANALYTICS_CSV_PATH):
        df_analytics = pd.read_csv(ANALYTICS_CSV_PATH)
        print(f"[CCPRA] Successfully loaded dataset: {len(df_analytics)} records")
    else:
        print(f"[CCPRA Warning] Analytics CSV not found at {ANALYTICS_CSV_PATH}")
except Exception as e:
    print(f"[CCPRA Error] Could not load dataset: {e}")


def calculate_retention_action(priority, contract, payment_method, online_security, tech_support):
    """
    Deterministic rule-based prescriptive retention recommendations matching
    src/generate_predictions.py
    """
    if priority in ['Priority 1 - Critical', 'Priority 2 - High']:
        actions = []
        if contract == 'Month-to-month':
            actions.append("Offer contract upgrade incentive")
        if payment_method == 'Electronic check':
            actions.append("Promote automatic payment enrollment")
        if online_security == 'No':
            actions.append("Offer security service retention package")
        if tech_support == 'No':
            actions.append("Offer technical support retention package")
        if not actions:
            actions.append("Engage proactive account review and customized retention offer")
        return "; ".join(actions)
    elif priority == 'Priority 3 - Medium':
        return "Monitor engagement and provide targeted retention offer"
    else:  # Priority 4 - Low
        return "Maintain relationship and monitor satisfaction"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/overview")
def api_overview():
    """
    Returns authentic high-level KPI scorecard metrics and revenue-at-risk computed from the dataset.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    total_customers = int(len(df_analytics))
    churned_customers = int((df_analytics['Churn'] == 'Yes').sum())
    retained_customers = int((df_analytics['Churn'] == 'No').sum())
    churn_rate = round((churned_customers / total_customers) * 100.0, 2)
    avg_monthly_charges = round(float(df_analytics['MonthlyCharges'].mean()), 2)
    total_mrr = round(float(df_analytics['MonthlyCharges'].sum()), 2)

    # Risk segment customer counts
    high_risk_count = int((df_analytics['High_Risk_Flag'] == 'Yes').sum()) if 'High_Risk_Flag' in df_analytics.columns else 0
    critical_count = int((df_analytics['Retention_Priority'] == 'Priority 1 - Critical').sum()) if 'Retention_Priority' in df_analytics.columns else 0
    medium_risk_count = int((df_analytics['Churn_Risk_Category'] == 'Medium Risk').sum()) if 'Churn_Risk_Category' in df_analytics.columns else 0
    low_risk_count = int((df_analytics['Churn_Risk_Category'] == 'Low Risk').sum()) if 'Churn_Risk_Category' in df_analytics.columns else 0

    # Genuine Revenue-at-Risk calculations
    # 1. Direct Exposure: Sum of MonthlyCharges for High-Risk (prob >= 0.60) customers
    high_risk_revenue = round(float(df_analytics.loc[df_analytics['High_Risk_Flag'] == 'Yes', 'MonthlyCharges'].sum()), 2) if 'High_Risk_Flag' in df_analytics.columns else 0.0
    critical_revenue = round(float(df_analytics.loc[df_analytics['Retention_Priority'] == 'Priority 1 - Critical', 'MonthlyCharges'].sum()), 2) if 'Retention_Priority' in df_analytics.columns else 0.0
    medium_risk_revenue = round(float(df_analytics.loc[df_analytics['Churn_Risk_Category'] == 'Medium Risk', 'MonthlyCharges'].sum()), 2) if 'Churn_Risk_Category' in df_analytics.columns else 0.0
    low_risk_revenue = round(float(df_analytics.loc[df_analytics['Churn_Risk_Category'] == 'Low Risk', 'MonthlyCharges'].sum()), 2) if 'Churn_Risk_Category' in df_analytics.columns else 0.0
    actual_churned_revenue = round(float(df_analytics.loc[df_analytics['Churn'] == 'Yes', 'MonthlyCharges'].sum()), 2)
    actual_retained_revenue = round(float(df_analytics.loc[df_analytics['Churn'] == 'No', 'MonthlyCharges'].sum()), 2)

    # Segment revenue exposures
    rev_by_contract = {c: round(float(df_analytics.loc[df_analytics['Contract'] == c, 'MonthlyCharges'].sum()), 2) for c in df_analytics['Contract'].unique()}
    high_risk_df = df_analytics[df_analytics['High_Risk_Flag'] == 'Yes']
    hr_by_contract = {c: round(float(high_risk_df.loc[high_risk_df['Contract'] == c, 'MonthlyCharges'].sum()), 2) for c in df_analytics['Contract'].unique()}
    hr_by_internet = {net: round(float(high_risk_df.loc[high_risk_df['InternetService'] == net, 'MonthlyCharges'].sum()), 2) for net in df_analytics['InternetService'].unique()}
    hr_by_payment = {pay: round(float(high_risk_df.loc[high_risk_df['PaymentMethod'] == pay, 'MonthlyCharges'].sum()), 2) for pay in df_analytics['PaymentMethod'].unique()}

    # 2. Probability-Weighted Expected Loss: sum(P_i * MonthlyCharges_i)
    if 'Predicted_Churn_Probability' in df_analytics.columns:
        expected_monthly_loss = round(float((df_analytics['Predicted_Churn_Probability'] * df_analytics['MonthlyCharges']).sum()), 2)
    else:
        expected_monthly_loss = round(high_risk_revenue, 2)

    annual_revenue_at_risk = round(high_risk_revenue * 12.0, 2)
    expected_annual_loss = round(expected_monthly_loss * 12.0, 2)
    high_risk_revenue_share_pct = round((high_risk_revenue / total_mrr) * 100.0, 2) if total_mrr > 0 else 0.0

    return jsonify({
        "total_customers": total_customers,
        "actual_churned": churned_customers,
        "actual_retained": retained_customers,
        "churn_rate_pct": churn_rate,
        "retention_rate_pct": round(100.0 - churn_rate, 2),
        "avg_monthly_charges": avg_monthly_charges,
        "total_mrr": total_mrr,
        "predicted_high_risk": high_risk_count,
        "predicted_critical": critical_count,
        "predicted_medium_risk": medium_risk_count,
        "predicted_low_risk": low_risk_count,
        "monthly_revenue_at_risk": high_risk_revenue,
        "critical_revenue_at_risk": critical_revenue,
        "medium_risk_revenue": medium_risk_revenue,
        "low_risk_revenue": low_risk_revenue,
        "actual_churned_revenue": actual_churned_revenue,
        "actual_retained_revenue": actual_retained_revenue,
        "annual_revenue_at_risk": annual_revenue_at_risk,
        "expected_monthly_loss": expected_monthly_loss,
        "expected_annual_loss": expected_annual_loss,
        "high_risk_revenue_share_pct": high_risk_revenue_share_pct,
        "revenue_by_contract": rev_by_contract,
        "high_risk_revenue_by_contract": hr_by_contract,
        "high_risk_revenue_by_internet": hr_by_internet,
        "high_risk_revenue_by_payment": hr_by_payment,
        "model_selected": "Logistic Regression (Pipeline)",
        "model_test_auc": 84.21,
        "model_test_accuracy": 80.55
    })


@app.route("/api/analytics-data")
def api_analytics_data():
    """
    Returns aggregated distributions for interactive charts with optional cross-filter support.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    filtered_df = df_analytics.copy()
    contract_filter = request.args.get("contract", "All").strip()
    internet_filter = request.args.get("internet", "All").strip()
    payment_filter = request.args.get("payment", "All").strip()
    tenure_filter = request.args.get("tenure", "All").strip()
    risk_filter = request.args.get("risk", "All").strip()

    if contract_filter and contract_filter != "All":
        filtered_df = filtered_df[filtered_df['Contract'] == contract_filter]
    if internet_filter and internet_filter != "All":
        filtered_df = filtered_df[filtered_df['InternetService'] == internet_filter]
    if payment_filter and payment_filter != "All":
        filtered_df = filtered_df[filtered_df['PaymentMethod'] == payment_filter]
    if tenure_filter and tenure_filter != "All" and 'Tenure_Group' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Tenure_Group'] == tenure_filter]
    if risk_filter and risk_filter != "All" and 'Churn_Risk_Category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Churn_Risk_Category'] == risk_filter]

    def get_group_stats(df, col, order=None):
        if col not in df.columns:
            return {"labels": [], "churn_rates": [], "churn_counts": [], "retained_counts": [], "totals": []}
        grp = df.groupby(col)['Churn'].value_counts().unstack().fillna(0)
        labels = order if order else sorted(list(grp.index))
        labels = [lbl for lbl in labels if lbl in grp.index]
        rates = []
        churn_counts = []
        retained_counts = []
        totals = []
        for lbl in labels:
            churn_n = int(grp.loc[lbl].get('Yes', 0))
            retain_n = int(grp.loc[lbl].get('No', 0))
            tot = churn_n + retain_n
            rate = round((churn_n / tot * 100.0), 2) if tot > 0 else 0.0
            rates.append(rate)
            churn_counts.append(churn_n)
            retained_counts.append(retain_n)
            totals.append(tot)
        return {
            "labels": labels,
            "churn_rates": rates,
            "churn_counts": churn_counts,
            "retained_counts": retained_counts,
            "totals": totals
        }

    # 1. Overall Churn Distribution
    churn_counts = filtered_df['Churn'].value_counts().to_dict()
    churn_dist = {
        "labels": ["Retained (No)", "Churned (Yes)"],
        "data": [int(churn_counts.get("No", 0)), int(churn_counts.get("Yes", 0))],
        "colors": ["#10b981", "#ef4444"]
    }

    # 2. Risk Distribution
    risk_order = ['Low Risk', 'Medium Risk', 'High Risk']
    risk_counts = filtered_df['Churn_Risk_Category'].value_counts().to_dict() if 'Churn_Risk_Category' in filtered_df.columns else {}
    risk_dist = {
        "labels": risk_order,
        "data": [int(risk_counts.get(r, 0)) for r in risk_order],
        "colors": ["#10b981", "#f59e0b", "#ef4444"]
    }

    # 3. Categorical breakdowns
    contracts_data = get_group_stats(filtered_df, 'Contract', ['Month-to-month', 'One year', 'Two year'])
    tenure_order = ['0–12 Months', '13–24 Months', '25–48 Months', '49–72 Months']
    tenure_data = get_group_stats(filtered_df, 'Tenure_Group', tenure_order)
    internet_data = get_group_stats(filtered_df, 'InternetService', ['DSL', 'Fiber optic', 'No'])
    payment_data = get_group_stats(filtered_df, 'PaymentMethod', [
        'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'
    ])
    tech_data = get_group_stats(filtered_df, 'TechSupport', ['No', 'Yes', 'No internet service'])
    charge_order = ['$0–$35', '$35.01–$70', '$70.01–$90', '$90.01–$120']
    charge_data = get_group_stats(filtered_df, 'Monthly_Charge_Range', charge_order)

    return jsonify({
        "total_filtered": int(len(filtered_df)),
        "churn_dist": churn_dist,
        "risk_dist": risk_dist,
        "contracts": contracts_data,
        "tenure_groups": tenure_data,
        "internet_services": internet_data,
        "payment_methods": payment_data,
        "tech_support": tech_data,
        "monthly_charges_bins": charge_data
    })


@app.route("/api/segments")
def api_segments():
    """
    Returns authentic aggregate customer segments and a 2D cross-tabulation matrix.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    # 2D Cross Matrix: Contract x InternetService
    contracts = ['Month-to-month', 'One year', 'Two year']
    internets = ['DSL', 'Fiber optic', 'No']
    matrix = []

    for c in contracts:
        for net in internets:
            sub = df_analytics[(df_analytics['Contract'] == c) & (df_analytics['InternetService'] == net)]
            count = int(len(sub))
            churn_count = int((sub['Churn'] == 'Yes').sum()) if count > 0 else 0
            churn_rate = round((churn_count / count * 100.0), 2) if count > 0 else 0.0
            avg_tenure = round(float(sub['tenure'].mean()), 1) if count > 0 else 0.0
            avg_charges = round(float(sub['MonthlyCharges'].mean()), 2) if count > 0 else 0.0
            avg_risk = round(float(sub['Predicted_Churn_Probability'].mean() * 100.0), 1) if count > 0 and 'Predicted_Churn_Probability' in sub.columns else 0.0
            hr_count = int((sub['High_Risk_Flag'] == 'Yes').sum()) if count > 0 and 'High_Risk_Flag' in sub.columns else 0

            matrix.append({
                "contract": c,
                "internet": net,
                "count": count,
                "churn_count": churn_count,
                "churn_rate": churn_rate,
                "avg_tenure": avg_tenure,
                "avg_monthly_charges": avg_charges,
                "avg_predicted_risk": avg_risk,
                "high_risk_count": hr_count
            })

    # Core actionable segments defined strictly by dataset attributes
    def build_segment_summary(name, condition, description):
        sub = df_analytics[condition]
        count = int(len(sub))
        churn_count = int((sub['Churn'] == 'Yes').sum()) if count > 0 else 0
        churn_rate = round((churn_count / count * 100.0), 2) if count > 0 else 0.0
        avg_tenure = round(float(sub['tenure'].mean()), 1) if count > 0 else 0.0
        avg_charges = round(float(sub['MonthlyCharges'].mean()), 2) if count > 0 else 0.0
        hr_count = int((sub['High_Risk_Flag'] == 'Yes').sum()) if count > 0 and 'High_Risk_Flag' in sub.columns else 0
        total_mrr = round(float(sub['MonthlyCharges'].sum()), 2) if count > 0 else 0.0
        return {
            "name": name,
            "description": description,
            "count": count,
            "churn_count": churn_count,
            "churn_rate": churn_rate,
            "avg_tenure": avg_tenure,
            "avg_monthly_charges": avg_charges,
            "high_risk_count": hr_count,
            "total_mrr": total_mrr
        }

    core_segments = [
        build_segment_summary(
            "Month-to-Month + Fiber Optic",
            (df_analytics['Contract'] == 'Month-to-month') & (df_analytics['InternetService'] == 'Fiber optic'),
            "High-friction tier: premium fiber service with zero lock-in contract"
        ),
        build_segment_summary(
            "Month-to-Month + Electronic Check",
            (df_analytics['Contract'] == 'Month-to-month') & (df_analytics['PaymentMethod'] == 'Electronic check'),
            "Highest-churn cohort: manual electronic billing with short contract"
        ),
        build_segment_summary(
            "New Subscribers (Tenure <= 12 Mo)",
            (df_analytics['tenure'] <= 12),
            "Early onboarding lifecycle cohort with elevated vulnerability"
        ),
        build_segment_summary(
            "Long-Term Contracts (1 & 2 Year)",
            (df_analytics['Contract'].isin(['One year', 'Two year'])),
            "High-stability committed subscribers with single-digit churn"
        ),
        build_segment_summary(
            "High-Value Fiber Optic ($85+/mo)",
            (df_analytics['InternetService'] == 'Fiber optic') & (df_analytics['MonthlyCharges'] >= 85.0),
            "Premium revenue contributors requiring white-glove retention care"
        )
    ]

    return jsonify({
        "matrix": matrix,
        "core_segments": core_segments
    })


def filter_and_sort_customers(df, search_query="", risk_filter="All", contract_filter="All", churn_filter="All", internet_filter="All", payment_filter="All", tenure_filter="All", sort_by="customerID", sort_dir="asc"):
    """
    Unified filter and sort utility for both table view and CSV download.
    """
    filtered = df.copy()

    if search_query:
        filtered = filtered[filtered['customerID'].str.lower().str.contains(search_query, na=False)]

    if risk_filter and risk_filter != "All":
        filtered = filtered[filtered['Churn_Risk_Category'] == risk_filter]

    if contract_filter and contract_filter != "All":
        filtered = filtered[filtered['Contract'] == contract_filter]

    if churn_filter and churn_filter != "All":
        filtered = filtered[filtered['Churn'] == churn_filter]

    if internet_filter and internet_filter != "All" and 'InternetService' in filtered.columns:
        filtered = filtered[filtered['InternetService'] == internet_filter]

    if payment_filter and payment_filter != "All" and 'PaymentMethod' in filtered.columns:
        filtered = filtered[filtered['PaymentMethod'] == payment_filter]

    if tenure_filter and tenure_filter != "All" and 'Tenure_Group' in filtered.columns:
        filtered = filtered[filtered['Tenure_Group'] == tenure_filter]

    valid_sort_cols = [
        'customerID', 'tenure', 'Contract', 'PaymentMethod', 'MonthlyCharges',
        'TotalCharges', 'Churn', 'Predicted_Churn_Probability', 'Churn_Risk_Category',
        'Retention_Priority', 'InternetService'
    ]
    if sort_by in valid_sort_cols and sort_by in filtered.columns:
        ascending = (sort_dir.lower() != 'desc')
        filtered = filtered.sort_values(by=sort_by, ascending=ascending)

    return filtered


@app.route("/api/customers")
def api_customers():
    """
    Searchable, filterable, sortable, and paginated customer records with full profile attributes.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    search_query = request.args.get("search", "").strip().lower()
    risk_filter = request.args.get("risk", "All").strip()
    contract_filter = request.args.get("contract", "All").strip()
    churn_filter = request.args.get("churn", "All").strip()
    internet_filter = request.args.get("internet", "All").strip()
    payment_filter = request.args.get("payment", "All").strip()
    tenure_filter = request.args.get("tenure", "All").strip()
    sort_by = request.args.get("sort_by", "customerID").strip()
    sort_dir = request.args.get("sort_dir", "asc").strip()
    page = max(1, int(request.args.get("page", 1)))
    per_page = max(5, min(100, int(request.args.get("per_page", 15))))

    filtered = filter_and_sort_customers(
        df_analytics, search_query, risk_filter, contract_filter, churn_filter,
        internet_filter, payment_filter, tenure_filter, sort_by, sort_dir
    )

    total_records = len(filtered)
    total_pages = max(1, int(np.ceil(total_records / per_page)))
    page = min(page, total_pages)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_data = filtered.iloc[start_idx:end_idx]

    columns_to_return = [
        'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
        'MonthlyCharges', 'TotalCharges', 'Churn', 'Tenure_Group',
        'Predicted_Churn_Probability', 'Churn_Risk_Percentage', 'Churn_Risk_Category',
        'Churn_Risk_Score', 'Retention_Priority', 'Retention_Action', 'High_Risk_Flag'
    ]

    items = []
    for _, row in page_data.iterrows():
        item = {}
        for col in columns_to_return:
            if col in row:
                val = row[col]
                if pd.isna(val):
                    item[col] = None
                elif isinstance(val, (np.floating, float)):
                    item[col] = round(float(val), 4)
                elif isinstance(val, (np.integer, int)):
                    item[col] = int(val)
                else:
                    item[col] = str(val)
            else:
                item[col] = None
        items.append(item)

    return jsonify({
        "items": items,
        "total": total_records,
        "page": page,
        "pages": total_pages,
        "per_page": per_page,
        "sort_by": sort_by,
        "sort_dir": sort_dir
    })


@app.route("/api/customers/export")
def api_customers_export():
    """
    Exports filtered and sorted customer records as a downloadable CSV.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    search_query = request.args.get("search", "").strip().lower()
    risk_filter = request.args.get("risk", "All").strip()
    contract_filter = request.args.get("contract", "All").strip()
    churn_filter = request.args.get("churn", "All").strip()
    internet_filter = request.args.get("internet", "All").strip()
    payment_filter = request.args.get("payment", "All").strip()
    tenure_filter = request.args.get("tenure", "All").strip()
    sort_by = request.args.get("sort_by", "customerID").strip()
    sort_dir = request.args.get("sort_dir", "asc").strip()

    filtered = filter_and_sort_customers(
        df_analytics, search_query, risk_filter, contract_filter, churn_filter,
        internet_filter, payment_filter, tenure_filter, sort_by, sort_dir
    )

    export_columns = [
        'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
        'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
        'MonthlyCharges', 'TotalCharges', 'Churn', 'Predicted_Churn_Probability',
        'Churn_Risk_Category', 'Retention_Priority', 'Retention_Action', 'High_Risk_Flag'
    ]
    export_cols = [c for c in export_columns if c in filtered.columns]
    csv_data = filtered[export_cols].to_csv(index=False)

    filename = "ccpra_customers_export.csv"
    parts = []
    if risk_filter and risk_filter != "All":
        parts.append(risk_filter.lower().replace(" ", "_"))
    if contract_filter and contract_filter != "All":
        parts.append(contract_filter.lower().replace(" ", "_"))
    if parts:
        filename = f"ccpra_customers_{'_'.join(parts)}.csv"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Executes live churn prediction using the genuine trained scikit-learn pipeline.
    """
    if model_pipeline is None:
        return jsonify({"error": "Saved machine learning model is unavailable on server"}), 500

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Empty or invalid JSON payload"}), 400

        # Extract and validate numerical features
        senior_citizen = int(data.get("SeniorCitizen", 0))
        tenure = int(data.get("tenure", 1))
        monthly_charges = float(data.get("MonthlyCharges", 50.0))
        total_charges = float(data.get("TotalCharges", tenure * monthly_charges))

        # Extract categorical features
        gender = str(data.get("gender", "Female")).strip()
        partner = str(data.get("Partner", "No")).strip()
        dependents = str(data.get("Dependents", "No")).strip()
        phone_service = str(data.get("PhoneService", "Yes")).strip()
        multiple_lines = str(data.get("MultipleLines", "No")).strip()
        internet_service = str(data.get("InternetService", "Fiber optic")).strip()
        online_security = str(data.get("OnlineSecurity", "No")).strip()
        online_backup = str(data.get("OnlineBackup", "No")).strip()
        device_protection = str(data.get("DeviceProtection", "No")).strip()
        tech_support = str(data.get("TechSupport", "No")).strip()
        streaming_tv = str(data.get("StreamingTV", "No")).strip()
        streaming_movies = str(data.get("StreamingMovies", "No")).strip()
        contract = str(data.get("Contract", "Month-to-month")).strip()
        paperless_billing = str(data.get("PaperlessBilling", "Yes")).strip()
        payment_method = str(data.get("PaymentMethod", "Electronic check")).strip()

        # Build exact 19-feature single-row DataFrame
        input_dict = {
            'SeniorCitizen': [senior_citizen],
            'tenure': [tenure],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges],
            'gender': [gender],
            'Partner': [partner],
            'Dependents': [dependents],
            'PhoneService': [phone_service],
            'MultipleLines': [multiple_lines],
            'InternetService': [internet_service],
            'OnlineSecurity': [online_security],
            'OnlineBackup': [online_backup],
            'DeviceProtection': [device_protection],
            'TechSupport': [tech_support],
            'StreamingTV': [streaming_tv],
            'StreamingMovies': [streaming_movies],
            'Contract': [contract],
            'PaperlessBilling': [paperless_billing],
            'PaymentMethod': [payment_method]
        }
        input_df = pd.DataFrame(input_dict)[PRIMARY_FEATURES]

        # Model inference
        probabilities = model_pipeline.predict_proba(input_df)[0]
        prob_churn = float(probabilities[1])
        prob_retain = float(probabilities[0])

        # Business segment derivations matching project specifications
        predicted_churn_class = "Yes" if prob_churn >= 0.50 else "No"
        risk_percentage = round(prob_churn * 100.0, 2)
        risk_score = int(round(prob_churn * 100.0))

        if prob_churn >= 0.60:
            risk_category = "High Risk"
            high_risk_flag = "Yes"
        elif prob_churn >= 0.30:
            risk_category = "Medium Risk"
            high_risk_flag = "No"
        else:
            risk_category = "Low Risk"
            high_risk_flag = "No"

        if prob_churn >= 0.80:
            retention_priority = "Priority 1 - Critical"
        elif prob_churn >= 0.60:
            retention_priority = "Priority 2 - High"
        elif prob_churn >= 0.30:
            retention_priority = "Priority 3 - Medium"
        else:
            retention_priority = "Priority 4 - Low"

        retention_action = calculate_retention_action(
            priority=retention_priority,
            contract=contract,
            payment_method=payment_method,
            online_security=online_security,
            tech_support=tech_support
        )

        # Calculate exact local feature attribution to predicted log-odds
        explanation = {}
        try:
            preprocessor = model_pipeline.named_steps.get('preprocessor')
            classifier = model_pipeline.named_steps.get('classifier')
            if preprocessor is not None and classifier is not None and hasattr(classifier, 'coef_'):
                transformed = preprocessor.transform(input_df)
                if hasattr(transformed, 'toarray'):
                    transformed = transformed.toarray()

                feat_names = preprocessor.get_feature_names_out() if hasattr(preprocessor, 'get_feature_names_out') else [f"f_{i}" for i in range(transformed.shape[1])]
                coefs = classifier.coef_[0]
                intercept = float(classifier.intercept_[0]) if hasattr(classifier, 'intercept_') else 0.0

                raw_contributions = transformed[0] * coefs
                decision_score = float(model_pipeline.decision_function(input_df)[0])
                reconstructed_score = intercept + float(np.sum(raw_contributions))

                def format_friendly_name(f_name):
                    if f_name == "num__tenure":
                        return f"Tenure ({tenure} mo)"
                    elif f_name == "num__MonthlyCharges":
                        return f"Monthly Charges (${monthly_charges:.2f})"
                    elif f_name == "num__TotalCharges":
                        return f"Total Charges (${total_charges:.2f})"
                    elif f_name == "num__SeniorCitizen":
                        return "Senior Citizen (Yes)" if senior_citizen == 1 else "Senior Citizen (No)"
                    elif f_name.startswith("cat__"):
                        clean = f_name[5:]
                        parts = clean.split("_", 1)
                        if len(parts) == 2:
                            col, val = parts
                            return f"{col}: {val}"
                        return clean
                    return f_name

                pos_list = []
                neg_list = []
                for fn, raw_c in zip(feat_names, raw_contributions):
                    c_val = float(raw_c)
                    if abs(c_val) < 1e-4:
                        continue
                    friendly = format_friendly_name(fn)
                    item = {
                        "feature": fn,
                        "label": friendly,
                        "contribution": round(c_val, 4),
                        "direction": "risk_increasing" if c_val > 0 else "risk_reducing"
                    }
                    if c_val > 0:
                        pos_list.append(item)
                    else:
                        neg_list.append(item)

                pos_list.sort(key=lambda x: x["contribution"], reverse=True)
                neg_list.sort(key=lambda x: x["contribution"])

                explanation = {
                    "intercept": round(intercept, 4),
                    "decision_score": round(decision_score, 4),
                    "reconstructed_score": round(reconstructed_score, 4),
                    "top_risk_increasing": pos_list[:3],
                    "top_risk_reducing": neg_list[:3],
                    "disclaimer": "Linear model log-odds contributions (β_i * x_i). Indicates feature weights in the trained model pipeline, not causal proof."
                }
        except Exception as ex:
            print(f"[CCPRA Error] Feature explanation failed: {ex}")
            explanation = {"error": "Local feature explanation calculation failed"}

        return jsonify({
            "status": "success",
            "prediction": {
                "churn_probability": round(prob_churn, 4),
                "predicted_churn_probability": round(prob_churn, 4),
                "retain_probability": round(prob_retain, 4),
                "churn_risk_percentage": risk_percentage,
                "churn_risk_score": risk_score,
                "predicted_churn": predicted_churn_class,
                "predicted_churn_class": predicted_churn_class,
                "churn_risk_category": risk_category,
                "retention_priority": retention_priority,
                "retention_action": retention_action,
                "high_risk_flag": high_risk_flag
            },
            "explanation": explanation,
            "input_summary": {
                "tenure": tenure,
                "contract": contract,
                "monthly_charges": monthly_charges,
                "total_charges": total_charges,
                "internet_service": internet_service,
                "payment_method": payment_method
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/scatter-data")
def api_scatter_data():
    """
    Returns an optimized stratified representative sample of customer records
    for high-performance scatter plotting (Tenure vs Monthly Charges).
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    # Sample ~700 records preserving exact class balance (26.54% churn)
    churn_yes = df_analytics[df_analytics['Churn'] == 'Yes']
    churn_no = df_analytics[df_analytics['Churn'] == 'No']

    sample_yes = churn_yes.sample(n=min(186, len(churn_yes)), random_state=42)
    sample_no = churn_no.sample(n=min(514, len(churn_no)), random_state=42)
    sampled = pd.concat([sample_yes, sample_no]).sample(frac=1.0, random_state=42)

    points = []
    for _, row in sampled.iterrows():
        points.append({
            "id": str(row['customerID']),
            "customerID": str(row['customerID']),
            "x": int(row['tenure']),
            "tenure": int(row['tenure']),
            "y": round(float(row['MonthlyCharges']), 2),
            "monthly_charges": round(float(row['MonthlyCharges']), 2),
            "churn": str(row['Churn']),
            "prob": round(float(row['Predicted_Churn_Probability'] * 100.0), 1) if 'Predicted_Churn_Probability' in row else 0.0,
            "predicted_risk": round(float(row['Predicted_Churn_Probability'] * 100.0), 1) if 'Predicted_Churn_Probability' in row else 0.0,
            "contract": str(row['Contract']),
            "net": str(row['InternetService'])
        })

    return jsonify({
        "points": points,
        "count": len(points),
        "total_sampled": len(points),
        "total_base": len(df_analytics)
    })


@app.route("/api/advanced-charts")
def api_advanced_charts():
    """
    Returns authentic distributions for heatmap, histograms, Pareto analysis,
    100% stacked distributions, and segment bubble charts.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    # 0. Churn Heatmap: Contract type vs Internet service
    contracts = ['Month-to-month', 'One year', 'Two year']
    internets = ['Fiber optic', 'DSL', 'No']
    cells = {}
    for c in contracts:
        for net in internets:
            sub = df_analytics[(df_analytics['Contract'] == c) & (df_analytics['InternetService'] == net)]
            n = len(sub)
            churn_n = int((sub['Churn'] == 'Yes').sum()) if n > 0 else 0
            rate = round((churn_n / n * 100.0), 2) if n > 0 else 0.0
            cells[f"{c}__{net}"] = {
                "contract": c,
                "internet": net,
                "total_customers": n,
                "churned_customers": churn_n,
                "retained_customers": n - churn_n,
                "churn_rate": rate
            }
    heatmap_obj = {
        "rows": contracts,
        "columns": internets,
        "cells": cells
    }

    # 1. Tenure Histogram (Split by Churn)
    tenure_bins = [0, 12, 24, 36, 48, 60, 72]
    tenure_labels = ['0-12 Mo', '13-24 Mo', '25-36 Mo', '37-48 Mo', '49-60 Mo', '61-72 Mo']
    t_cuts = pd.cut(df_analytics['tenure'], bins=tenure_bins, labels=tenure_labels, include_lowest=True)
    t_cross = pd.crosstab(t_cuts, df_analytics['Churn'])
    tenure_retained = [int(t_cross.loc[lbl].get('No', 0)) for lbl in tenure_labels if lbl in t_cross.index]
    tenure_churned = [int(t_cross.loc[lbl].get('Yes', 0)) for lbl in tenure_labels if lbl in t_cross.index]
    tenure_totals = [r + c for r, c in zip(tenure_retained, tenure_churned)]
    tenure_rates = [round(c / t * 100.0, 2) if t > 0 else 0.0 for c, t in zip(tenure_churned, tenure_totals)]
    tenure_hist = {
        "bins": tenure_labels,
        "labels": tenure_labels,
        "retained": tenure_retained,
        "churned": tenure_churned,
        "totals": tenure_totals,
        "churn_rates": tenure_rates
    }

    # 2. Monthly Charges Histogram (Split by Churn)
    charge_bins = [18.0, 35.0, 55.0, 75.0, 95.0, 120.0]
    charge_labels = ['$18-$35', '$35-$55', '$55-$75', '$75-$95', '$95-$120']
    c_cuts = pd.cut(df_analytics['MonthlyCharges'], bins=charge_bins, labels=charge_labels, include_lowest=True)
    c_cross = pd.crosstab(c_cuts, df_analytics['Churn'])
    charge_retained = [int(c_cross.loc[lbl].get('No', 0)) for lbl in charge_labels if lbl in c_cross.index]
    charge_churned = [int(c_cross.loc[lbl].get('Yes', 0)) for lbl in charge_labels if lbl in c_cross.index]
    charge_totals = [r + c for r, c in zip(charge_retained, charge_churned)]
    charge_rates = [round(c / t * 100.0, 2) if t > 0 else 0.0 for c, t in zip(charge_churned, charge_totals)]
    charges_hist = {
        "bins": charge_labels,
        "labels": charge_labels,
        "retained": charge_retained,
        "churned": charge_churned,
        "totals": charge_totals,
        "churn_rates": charge_rates
    }

    # 3. Model Predicted Probability Distribution Histogram
    prob_bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    prob_labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
    p_cuts = pd.cut(df_analytics['Predicted_Churn_Probability'], bins=prob_bins, labels=prob_labels, include_lowest=True)
    p_counts = p_cuts.value_counts(sort=False)
    p_counts_list = [int(p_counts.get(lbl, 0)) for lbl in prob_labels]
    prob_hist = {
        "bins": prob_labels,
        "labels": prob_labels,
        "counts": p_counts_list,
        "percentages": [round(c / len(df_analytics) * 100.0, 2) for c in p_counts_list],
        "tier_labels": [
            "Low Risk (<30%)" if i < 3 else (
                "Medium Risk (30-60%)" if i < 6 else (
                    "High Risk (60-80%)" if i < 8 else "Critical Triage (≥80%)"
                )
            ) for i in range(10)
        ],
        "thresholds": {"low": "30%", "high": "60%", "critical": "80%"}
    }

    # 4. Revenue-Risk Pareto Analysis (High-Risk MRR by Payment Method)
    hr_df = df_analytics[df_analytics['High_Risk_Flag'] == 'Yes']
    pareto_s = hr_df.groupby('PaymentMethod')['MonthlyCharges'].sum().sort_values(ascending=False)
    tot_hr_mrr = float(pareto_s.sum())
    cum_pct = (pareto_s.cumsum() / tot_hr_mrr * 100.0).round(2)
    pareto_chart = {
        "labels": list(pareto_s.index),
        "charges": [round(float(v), 2) for v in pareto_s.values],
        "cumulative_percentages": [float(p) for p in cum_pct.values],
        "cum_pct": [float(p) for p in cum_pct.values],
        "total_exposure": tot_hr_mrr
    }

    # 5. 100% Stacked Proportions (Historical Outcomes)
    def calc_stacked(col, order=None):
        ct = pd.crosstab(df_analytics[col], df_analytics['Churn'], normalize='index') * 100.0
        counts_t = pd.crosstab(df_analytics[col], df_analytics['Churn'])
        idx = order if order else list(ct.index)
        idx = [i for i in idx if i in ct.index]
        return {
            "labels": idx,
            "retained_pct": [round(float(ct.loc[i].get('No', 0)), 1) for i in idx],
            "churn_pct": [round(float(ct.loc[i].get('Yes', 0)), 1) for i in idx],
            "churned_pct": [round(float(ct.loc[i].get('Yes', 0)), 1) for i in idx],
            "churn_counts": [int(counts_t.loc[i].get('Yes', 0)) for i in idx]
        }

    stacked_contract = calc_stacked('Contract', ['Month-to-month', 'One year', 'Two year'])
    stacked_payment = calc_stacked('PaymentMethod', [
        'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'
    ])
    stacked_tech = calc_stacked('TechSupport', ['No', 'Yes', 'No internet service'])

    # 6. Segment Bubble Chart (Contract x Internet Service)
    contracts = ['Month-to-month', 'One year', 'Two year']
    internets = ['DSL', 'Fiber optic', 'No']
    bubbles = []
    for c in contracts:
        for net in internets:
            sub = df_analytics[(df_analytics['Contract'] == c) & (df_analytics['InternetService'] == net)]
            n = len(sub)
            if n == 0:
                continue
            churn_n = int((sub['Churn'] == 'Yes').sum())
            churn_rate = round((churn_n / n * 100.0), 2)
            avg_charges = round(float(sub['MonthlyCharges'].mean()), 2)
            hr_n = int((sub['High_Risk_Flag'] == 'Yes').sum()) if 'High_Risk_Flag' in sub.columns else 0
            avg_tenure = round(float(sub['tenure'].mean()), 1)
            avg_risk = round(float(sub['Predicted_Churn_Probability'].mean() * 100.0), 1) if 'Predicted_Churn_Probability' in sub else 0.0

            # Map bubble radius (scale n between 8 and 36 px)
            radius = round(8 + (n / 2500) * 28, 1)

            bubbles.append({
                "name": f"{c} + {net}",
                "label": f"{c} + {net}",
                "contract": c,
                "internet": net,
                "avg_charges": avg_charges,
                "x": avg_charges,
                "churn_rate": churn_rate,
                "y": churn_rate,
                "radius": radius,
                "r": radius,
                "count": n,
                "churn_count": churn_n,
                "high_risk_count": hr_n,
                "avg_tenure": avg_tenure,
                "avg_predicted_risk": avg_risk
            })

    return jsonify({
        "heatmap": heatmap_obj,
        "tenure_histogram": tenure_hist,
        "charges_histogram": charges_hist,
        "predicted_risk_histogram": prob_hist,
        "predicted_prob_histogram": prob_hist,
        "pareto": pareto_chart,
        "pareto_revenue": pareto_chart,
        "stacked_100": {
            "contract": stacked_contract,
            "payment": stacked_payment,
            "tech": stacked_tech,
            "tech_support": stacked_tech
        },
        "stacked_proportions": {
            "contract": stacked_contract,
            "payment": stacked_payment,
            "tech_support": stacked_tech
        },
        "bubble_segments": bubbles
    })


@app.route("/api/threshold-sim")
def api_threshold_sim():
    """
    Simulates operational risk threshold adjustment.
    """
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    try:
        threshold = float(request.args.get("threshold", 0.60))
        threshold = max(0.05, min(0.95, threshold))
    except ValueError:
        threshold = 0.60

    total_base = len(df_analytics)
    total_mrr = round(float(df_analytics['MonthlyCharges'].sum()), 2)

    flagged_mask = df_analytics['Predicted_Churn_Probability'] >= threshold
    flagged_df = df_analytics[flagged_mask]

    flagged_count = int(len(flagged_df))
    flagged_pct = round((flagged_count / total_base * 100.0), 2) if total_base > 0 else 0.0
    flagged_mrr = round(float(flagged_df['MonthlyCharges'].sum()), 2) if flagged_count > 0 else 0.0
    annual_mrr = round(flagged_mrr * 12.0, 2)

    # Actual outcome distribution within flagged cohort
    true_churners = int((flagged_df['Churn'] == 'Yes').sum()) if flagged_count > 0 else 0
    retained_in_flagged = int((flagged_df['Churn'] == 'No').sum()) if flagged_count > 0 else 0
    empirical_precision = round((true_churners / flagged_count * 100.0), 2) if flagged_count > 0 else 0.0
    empirical_recall = round((true_churners / 1869 * 100.0), 2)

    base_flagged = 1039
    base_charges = 85546.25
    delta_cust = flagged_count - base_flagged
    delta_chg = round(flagged_mrr - base_charges, 2)
    mrr_pct = round((flagged_mrr / total_mrr * 100.0), 2) if total_mrr > 0 else 0.0

    return jsonify({
        "threshold": threshold,
        "threshold_pct": round(threshold * 100.0, 1),
        "flagged_customers": flagged_count,
        "flagged_count": flagged_count,
        "flagged_customer_share_pct": flagged_pct,
        "flagged_pct": flagged_pct,
        "flagged_monthly_charges": flagged_mrr,
        "flagged_mrr": flagged_mrr,
        "flagged_mrr_share_pct": mrr_pct,
        "annualized_flagged_charges": annual_mrr,
        "annual_flagged_mrr": annual_mrr,
        "delta_customers": delta_cust,
        "delta_charges": delta_chg,
        "total_base": total_base,
        "total_mrr": total_mrr,
        "actual_churners_captured": true_churners,
        "retained_in_flagged": retained_in_flagged,
        "empirical_precision_pct": empirical_precision,
        "empirical_recall_pct": empirical_recall
    })


# Global cache for batch prediction export
last_batch_df = None

@app.route("/api/predict-batch", methods=["POST"])
def api_predict_batch():
    """
    Processes batch CSV upload for model inference. Validates required columns,
    executes genuine pipeline prediction, and returns summary stats with preview.
    """
    global last_batch_df
    if model_pipeline is None:
        return jsonify({"status": "error", "message": "Saved machine learning model is unavailable"}), 500

    try:
        # Check if file was sent via multipart or raw CSV body
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "No file selected for upload"}), 400
            df_upload = pd.read_csv(file)
        else:
            raw_data = request.get_data(as_text=True)
            if not raw_data.strip():
                return jsonify({"status": "error", "message": "Empty file or payload provided"}), 400
            from io import StringIO
            df_upload = pd.read_csv(StringIO(raw_data))

        if len(df_upload) == 0:
            return jsonify({"status": "error", "message": "Uploaded CSV contains 0 rows"}), 400

        # Validate required feature columns
        missing_cols = [c for c in PRIMARY_FEATURES if c not in df_upload.columns]
        if missing_cols:
            return jsonify({
                "status": "error",
                "message": f"CSV is missing {len(missing_cols)} required pipeline feature column(s): {', '.join(missing_cols)}",
                "missing_columns": missing_cols,
                "required_columns": PRIMARY_FEATURES
            }), 400

        # Prepare clean copy of features
        clean_df = df_upload.copy()

        # Coerce numeric fields safely
        clean_df['SeniorCitizen'] = pd.to_numeric(clean_df['SeniorCitizen'], errors='coerce').fillna(0).astype(int)
        clean_df['tenure'] = pd.to_numeric(clean_df['tenure'], errors='coerce').fillna(1).astype(int)
        clean_df['MonthlyCharges'] = pd.to_numeric(clean_df['MonthlyCharges'], errors='coerce').fillna(50.0).astype(float)
        clean_df['TotalCharges'] = pd.to_numeric(clean_df['TotalCharges'], errors='coerce').fillna(clean_df['tenure'] * clean_df['MonthlyCharges']).astype(float)

        # Ensure strings are stripped
        for c in CATEGORICAL_FEATURES:
            clean_df[c] = clean_df[c].astype(str).str.strip()

        # Execute genuine model inference
        input_data = clean_df[PRIMARY_FEATURES]
        probabilities = model_pipeline.predict_proba(input_data)
        churn_probs = probabilities[:, 1]
        retain_probs = probabilities[:, 0]

        # Attach predictions and prescriptive actions
        clean_df['Predicted_Churn_Probability'] = [round(float(p), 4) for p in churn_probs]
        clean_df['Churn_Risk_Percentage'] = [round(float(p * 100.0), 2) for p in churn_probs]
        clean_df['Predicted_Churn'] = ['Yes' if p >= 0.50 else 'No' for p in churn_probs]

        categories = []
        priorities = []
        actions = []
        high_risk_flags = []

        for _, row in clean_df.iterrows():
            prob = row['Predicted_Churn_Probability']
            if prob >= 0.60:
                cat = "High Risk"
                hr_flag = "Yes"
            elif prob >= 0.30:
                cat = "Medium Risk"
                hr_flag = "No"
            else:
                cat = "Low Risk"
                hr_flag = "No"

            if prob >= 0.80:
                pri = "Priority 1 - Critical"
            elif prob >= 0.60:
                pri = "Priority 2 - High"
            elif prob >= 0.30:
                pri = "Priority 3 - Medium"
            else:
                pri = "Priority 4 - Low"

            act = calculate_retention_action(
                pri,
                row['Contract'],
                row['PaymentMethod'],
                row['OnlineSecurity'],
                row['TechSupport']
            )

            categories.append(cat)
            priorities.append(pri)
            actions.append(act)
            high_risk_flags.append(hr_flag)

        clean_df['Churn_Risk_Category'] = categories
        clean_df['Retention_Priority'] = priorities
        clean_df['High_Risk_Flag'] = high_risk_flags
        clean_df['Retention_Action'] = actions

        last_batch_df = clean_df

        # Calculate summary metrics
        total_scored = int(len(clean_df))
        high_risk_count = int((clean_df['High_Risk_Flag'] == 'Yes').sum())
        critical_count = int((clean_df['Retention_Priority'] == 'Priority 1 - Critical').sum())
        total_mrr_scored = round(float(clean_df['MonthlyCharges'].sum()), 2)
        avg_risk = round(float(clean_df['Churn_Risk_Percentage'].mean()), 2)

        predicted_churners = int((clean_df['Predicted_Churn'] == 'Yes').sum())
        churn_rate_pct = round((predicted_churners / total_scored * 100.0), 2) if total_scored > 0 else 0.0

        preview_records = []
        for _, r in clean_df.head(25).iterrows():
            preview_records.append({
                "CustomerID": str(r['customerID']) if 'customerID' in clean_df.columns else "N/A",
                "Contract": str(r['Contract']),
                "InternetService": str(r['InternetService']),
                "MonthlyCharges": float(r['MonthlyCharges']),
                "Predicted_Probability": float(r['Churn_Risk_Percentage']),
                "Predicted_Class": str(r['Predicted_Churn']),
                "Risk_Tier": str(r['Churn_Risk_Category']),
                "Prescribed_Action": str(r['Retention_Action'])
            })

        return jsonify({
            "status": "success",
            "message": f"Successfully processed and scored {total_scored:,} records.",
            "total_scored": total_scored,
            "predicted_churners": predicted_churners,
            "predicted_churn_rate_pct": churn_rate_pct,
            "high_risk_count": high_risk_count,
            "preview_rows": preview_records,
            "summary": {
                "total_scored": total_scored,
                "predicted_churners": predicted_churners,
                "predicted_churn_rate_pct": churn_rate_pct,
                "high_risk_count": high_risk_count,
                "critical_count": critical_count,
                "total_mrr_scored": total_mrr_scored,
                "avg_risk_pct": avg_risk
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Batch prediction failed: {str(e)}"}), 400


@app.route("/api/predict-batch/download")
def api_predict_batch_download():
    """
    Downloads the most recently scored batch prediction results.
    """
    global last_batch_df
    if last_batch_df is None or len(last_batch_df) == 0:
        return jsonify({"error": "No batch prediction results found. Please run a batch prediction first."}), 404

    csv_data = last_batch_df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ccpra_batch_predictions_result.csv"}
    )


@app.route("/api/predict-batch/template")
def api_predict_batch_template():
    """
    Generates and downloads a clean 5-row CSV template with all 19 feature columns for testing.
    """
    sample_data = {
        "customerID": ["SAMPLE-001", "SAMPLE-002", "SAMPLE-003", "SAMPLE-004", "SAMPLE-005"],
        "gender": ["Female", "Male", "Female", "Male", "Female"],
        "SeniorCitizen": [0, 1, 0, 0, 1],
        "Partner": ["Yes", "No", "No", "Yes", "Yes"],
        "Dependents": ["No", "No", "No", "Yes", "No"],
        "tenure": [2, 14, 48, 62, 1],
        "PhoneService": ["Yes", "Yes", "Yes", "Yes", "No"],
        "MultipleLines": ["No", "Yes", "Yes", "Yes", "No phone service"],
        "InternetService": ["Fiber optic", "Fiber optic", "DSL", "DSL", "DSL"],
        "OnlineSecurity": ["No", "No", "Yes", "Yes", "No"],
        "OnlineBackup": ["No", "Yes", "Yes", "Yes", "No"],
        "DeviceProtection": ["No", "No", "Yes", "Yes", "No"],
        "TechSupport": ["No", "No", "Yes", "Yes", "No"],
        "StreamingTV": ["No", "Yes", "No", "Yes", "No"],
        "StreamingMovies": ["No", "Yes", "No", "Yes", "No"],
        "Contract": ["Month-to-month", "Month-to-month", "One year", "Two year", "Month-to-month"],
        "PaperlessBilling": ["Yes", "Yes", "No", "No", "Yes"],
        "PaymentMethod": [
            "Electronic check", "Electronic check", "Credit card (automatic)",
            "Bank transfer (automatic)", "Electronic check"
        ],
        "MonthlyCharges": [70.70, 95.50, 60.25, 84.80, 29.85],
        "TotalCharges": [151.65, 1340.20, 2892.00, 5257.60, 29.85]
    }
    sample_df = pd.DataFrame(sample_data)
    csv_data = sample_df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=ccpra_sample_upload_template.csv"}
    )


@app.route("/api/model-evaluation")
def api_model_evaluation():
    """
    Returns authentic holdout test performance metrics and full-base summary.
    """
    holdout_metrics = {
        "dataset_split": {
            "strategy": "80/20 Stratified Holdout Split (random_state=42)",
            "training_samples": 5634,
            "test_samples": 1409,
            "training_churn_rate": "26.54%",
            "test_churn_rate": "26.54%"
        },
        "models": [
            {
                "name": "Logistic Regression (Production Selected)",
                "accuracy": 0.8055,
                "precision": 0.6572,
                "recall": 0.5588,
                "f1_score": 0.6040,
                "roc_auc": 0.8421,
                "selected": True,
                "rationale": "Superior probability calibration (+2.28% ROC-AUC), +6.95% higher Recall, higher Precision, and clear coefficient explainability."
            },
            {
                "name": "Random Forest Classifier (Benchmark)",
                "accuracy": 0.7871,
                "precision": 0.6267,
                "recall": 0.4893,
                "f1_score": 0.5496,
                "roc_auc": 0.8193,
                "selected": False,
                "rationale": "High test set generalization but captured fewer true churners (-6.95% recall) compared to regularized Logistic Regression."
            }
        ],
        "confusion_matrix_test": {
            "description": "Evaluated on untouched test set (n=1,409)",
            "true_negatives": 926,
            "false_positives": 109,
            "false_negatives": 165,
            "true_positives": 209
        },
        "full_population_summary": {
            "description": "Model predictions applied to all 7,043 customers in subscriber base",
            "total_scored": 7043,
            "predicted_churn_count": 1562,
            "predicted_churn_rate_pct": 22.18,
            "high_risk_customers": 1039,
            "critical_priority_customers": 49,
            "historical_accuracy_on_full_base": 80.5
        }
    }
    return jsonify(holdout_metrics)


cached_diagnostics = None
cached_lifecycle = None
cached_distributions = None
cached_dataset_comp = None


def get_model_diagnostics():
    global cached_diagnostics
    if cached_diagnostics is not None:
        return cached_diagnostics

    if model_pipeline is not None and df_analytics is not None:
        try:
            X = df_analytics[PRIMARY_FEATURES].copy()
            y = df_analytics['Churn'].map({'No': 0, 'Yes': 1}).values
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.20, random_state=42, stratify=y
            )
            y_probs = model_pipeline.predict_proba(X_test)[:, 1]
            y_pred = (y_probs >= 0.50).astype(int)

            total_test = len(y_test)
            total_churners = int(y_test.sum())

            # Cumulative Gains & Lift
            deciles = pd.DataFrame({'y_true': y_test, 'prob': y_probs})
            deciles = deciles.sort_values(by='prob', ascending=False).reset_index(drop=True)
            deciles['decile'] = pd.qcut(deciles.index, q=10, labels=False) + 1

            gains = deciles.groupby('decile').agg(
                total=('y_true', 'count'),
                churners=('y_true', 'sum')
            ).reset_index()
            gains['cum_churners'] = gains['churners'].cumsum()
            gains['cum_gain_pct'] = ((gains['cum_churners'] / total_churners) * 100.0).round(2)
            gains['decile_pct'] = gains['decile'] * 10
            gains['lift'] = ((gains['churners'] / gains['total']) / (total_churners / total_test)).round(2)
            gains['cum_lift'] = ((gains['cum_churners'] / gains['total'].cumsum()) / (total_churners / total_test)).round(2)

            # Calibration curve
            prob_true, prob_pred = calibration_curve(y_test, y_probs, n_bins=10, strategy='uniform')
            brier = round(float(brier_score_loss(y_test, y_probs)), 4)

            # Precision-Recall curve across threshold spectrum
            pr_points = []
            test_thresholds = np.linspace(0.05, 0.95, 19)
            for t in test_thresholds:
                preds = (y_probs >= t).astype(int)
                p = precision_score(y_test, preds, zero_division=0)
                r = recall_score(y_test, preds, zero_division=0)
                f = f1_score(y_test, preds, zero_division=0)
                pr_points.append({
                    'threshold': round(float(t), 2),
                    'precision': round(float(p) * 100, 2),
                    'recall': round(float(r) * 100, 2),
                    'f1_score': round(float(f) * 100, 2)
                })

            cached_diagnostics = {
                "test_samples": total_test,
                "training_samples": len(y_train),
                "actual_churners": total_churners,
                "actual_retained": total_test - total_churners,
                "roc_auc": round(float(roc_auc_score(y_test, y_probs)) * 100, 2),
                "accuracy": round(float(accuracy_score(y_test, y_pred)) * 100, 2),
                "precision": round(float(precision_score(y_test, y_pred)) * 100, 2),
                "recall": round(float(recall_score(y_test, y_pred)) * 100, 2),
                "f1_score": round(float(f1_score(y_test, y_pred)) * 100, 2),
                "brier_score": brier,
                "cumulative_gains": gains.to_dict(orient='records'),
                "calibration": {
                    "prob_pred": [round(float(v) * 100, 2) for v in prob_pred],
                    "prob_true": [round(float(v) * 100, 2) for v in prob_true],
                    "brier_score": brier
                },
                "pr_curve": pr_points
            }
        except Exception as ex:
            print(f"[CCPRA Error] Could not compute model diagnostics: {ex}")
            cached_diagnostics = {"error": str(ex)}

    return cached_diagnostics or {}


def get_lifecycle_retention():
    global cached_lifecycle
    if cached_lifecycle is not None:
        return cached_lifecycle

    if df_analytics is not None:
        try:
            milestones = [1, 3, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72]
            lc_points = []
            tot_base = len(df_analytics)
            for m in milestones:
                sub = df_analytics[df_analytics['tenure'] >= m]
                count_m = len(sub)
                churn_m = int((sub['Churn'] == 'Yes').sum())
                churn_rate = round((churn_m / count_m * 100.0), 2) if count_m > 0 else 0.0
                ret_rate = round(100.0 - churn_rate, 2)
                pct_base = round((count_m / tot_base * 100.0), 1)
                lc_points.append({
                    "milestone_months": m,
                    "accounts_active_at_milestone": count_m,
                    "pct_of_total_base": pct_base,
                    "pseudo_retention_rate": ret_rate,
                    "cohort_churn_rate": churn_rate
                })

            cohort_windows = [
                ("0–1 Mo (Onboarding)", 0, 1),
                ("2–6 Mo (Early Lifecycle)", 2, 6),
                ("7–12 Mo (First Year Renewal)", 7, 12),
                ("13–24 Mo (Established)", 13, 24),
                ("25–48 Mo (Mature)", 25, 48),
                ("49–72 Mo (Loyal / Long-Term)", 49, 72)
            ]
            cohort_hazards = []
            for label, low, high in cohort_windows:
                sub = df_analytics[(df_analytics['tenure'] >= low) & (df_analytics['tenure'] <= high)]
                n_acc = len(sub)
                n_churn = int((sub['Churn'] == 'Yes').sum())
                crate = round((n_churn / n_acc * 100.0), 2) if n_acc > 0 else 0.0
                cohort_hazards.append({
                    "cohort_label": label,
                    "accounts": n_acc,
                    "churned": n_churn,
                    "churn_rate": crate,
                    "retention_rate": round(100.0 - crate, 2)
                })

            cached_lifecycle = {
                "milestones": lc_points,
                "cohort_hazards": cohort_hazards,
                "disclaimer": "Cross-sectional pseudo-retention model derived from portfolio tenure snapshot (n=7,043). Reflects tenure survivor distribution, not longitudinal cohort panel tracking."
            }
        except Exception as ex:
            print(f"[CCPRA Error] Could not compute lifecycle retention: {ex}")
            cached_lifecycle = {"error": str(ex)}

    return cached_lifecycle or {}


def get_distribution_comparison():
    global cached_distributions
    if cached_distributions is not None:
        return cached_distributions

    if df_analytics is not None:
        try:
            box_data = {}
            for col in ['MonthlyCharges', 'tenure']:
                box_data[col] = {}
                for status in ['Yes', 'No']:
                    series = df_analytics[df_analytics['Churn'] == status][col]
                    q1 = float(np.percentile(series, 25))
                    med = float(np.percentile(series, 50))
                    q3 = float(np.percentile(series, 75))
                    iqr = q3 - q1
                    low_w = float(max(series.min(), q1 - 1.5 * iqr))
                    high_w = float(min(series.max(), q3 + 1.5 * iqr))
                    box_data[col][status] = {
                        "min": round(float(series.min()), 2),
                        "low_whisker": round(low_w, 2),
                        "q1": round(q1, 2),
                        "median": round(med, 2),
                        "q3": round(q3, 2),
                        "high_whisker": round(high_w, 2),
                        "max": round(float(series.max()), 2),
                        "mean": round(float(series.mean()), 2),
                        "iqr": round(iqr, 2),
                        "count": int(len(series))
                    }
            cached_distributions = box_data
        except Exception as ex:
            print(f"[CCPRA Error] Could not compute box plot distributions: {ex}")
            cached_distributions = {"error": str(ex)}

    return cached_distributions or {}


def get_dataset_comparison():
    global cached_dataset_comp
    if cached_dataset_comp is not None:
        return cached_dataset_comp

    try:
        ext_path = EXTERNAL_DATA_PATH
        if not os.path.exists(ext_path):
            ext_path = os.path.join(BASE_DIR, "scratch", "IndiaTelecomData.csv")

        if os.path.exists(ext_path):
            df_in = pd.read_csv(ext_path)
            churn_in_pct = round(float(df_in['churn'].mean() * 100), 2)
            operators = df_in.groupby('telecom_partner')['churn'].agg(
                total='count',
                churners='sum'
            ).reset_index()
            operators['churn_rate'] = ((operators['churners'] / operators['total']) * 100).round(2)
            
            neg_data = int((df_in['data_used'] < 0).sum())
            neg_calls = int((df_in['calls_made'] < 0).sum())
            neg_sms = int((df_in['sms_sent'] < 0).sum())
            tot_anom = int(((df_in['data_used'] < 0) | (df_in['calls_made'] < 0) | (df_in['sms_sent'] < 0)).sum())

            cached_dataset_comp = {
                "dataset_name": "Indian Telecom Customer Churn Dataset",
                "source": "Mendeley Data (doi:10.17632/px3dt72xdw.1)",
                "author": "Patrick Koomson (July 2024)",
                "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                "records": len(df_in),
                "attributes_count": len(df_in.columns),
                "churn_rate_pct": churn_in_pct,
                "coverage_window": "January 1, 2020 – January 11, 2020 (11-day cross-sectional window)",
                "operators": operators.to_dict(orient='records'),
                "data_anomalies": {
                    "negative_data_usage_rows": neg_data,
                    "negative_calls_made_rows": neg_calls,
                    "negative_sms_sent_rows": neg_sms,
                    "total_anomalous_rows": tot_anom
                },
                "comparative_insights": [
                    {
                        "dimension": "Business Model Archetype",
                        "ccpra_baseline": "Postpaid Subscription Broadband & Landline (Fixed contracts, recurring credit/bank billing, lock-in terms).",
                        "india_external": "Prepaid Mobile Cellular Service (Quota-based data packs, SMS/voice bundles, tariff-driven portability)."
                    },
                    {
                        "dimension": "Primary Churn Drivers",
                        "ccpra_baseline": "Contract lock-in (Month-to-month 42.7% vs 2-Yr 2.8%), High Monthly Charges ($79.65 median), Electronic check friction.",
                        "india_external": "Usage exhaustion & network operator pricing (Vodafone 21.28% vs Airtel 17.16%), daily data consumption bounds."
                    },
                    {
                        "dimension": "Model Interoperability & External Validation",
                        "ccpra_baseline": "19 specialized feature inputs (Contract, TechSupport, OnlineBackup, InternetService, TotalCharges).",
                        "india_external": "Zero overlapping features beyond gender/dependents. Direct execution of CCPRA model on Indian data is mathematically impossible without synthetic feature fabrication."
                    }
                ]
            }
        else:
            cached_dataset_comp = {"error": "External dataset file not found"}
    except Exception as ex:
        print(f"[CCPRA Error] Could not compute dataset comparison: {ex}")
        cached_dataset_comp = {"error": str(ex)}

    return cached_dataset_comp or {}


cached_behavioral_intel = None

def get_behavioral_intelligence():
    """
    Returns multivariate correlation matrix, 2D service-contract churn heatmap,
    stratified scatterplot sample (300 points), and financial exposure hierarchy.
    """
    global cached_behavioral_intel
    if cached_behavioral_intel is not None:
        return cached_behavioral_intel

    fpath = os.path.join(BASE_DIR, "data", "processed", "advanced_behavioral_metrics.json")
    try:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                cached_behavioral_intel = json.load(f)
        else:
            cached_behavioral_intel = {"error": "Behavioral metrics file not found"}
    except Exception as ex:
        print(f"[CCPRA Error] Could not load behavioral metrics: {ex}")
        cached_behavioral_intel = {"error": str(ex)}

    return cached_behavioral_intel or {}


cached_market_intel = None

def get_external_market_intelligence():
    """
    Returns external macro market intelligence from official TRAI reports,
    FCC consumer complaints, and Mendeley telecom audits.
    """
    global cached_market_intel
    if cached_market_intel is not None:
        return cached_market_intel

    trai_path = os.path.join(BASE_DIR, "data", "external", "trai", "trai_processed_metrics.json")
    fcc_path = os.path.join(BASE_DIR, "data", "external", "fcc_processed_metrics.json")
    
    try:
        trai_data = {}
        if os.path.exists(trai_path):
            with open(trai_path, "r", encoding="utf-8") as f:
                trai_data = json.load(f)

        fcc_data = {}
        if os.path.exists(fcc_path):
            with open(fcc_path, "r", encoding="utf-8") as f:
                fcc_data = json.load(f)

        mendeley_comp = get_dataset_comparison()

        cached_market_intel = {
            "trai": trai_data,
            "fcc": fcc_data,
            "mendeley": mendeley_comp
        }
    except Exception as ex:
        print(f"[CCPRA Error] Could not load external market intelligence: {ex}")
        cached_market_intel = {"error": str(ex)}

    return cached_market_intel or {}


cached_uci_benchmark = None

def get_uci_benchmark():
    """
    Returns independent UCI Iranian Telecom Churn benchmark experiment metrics
    (Logistic Regression vs Random Forest on held-out split, and feature importance).
    """
    global cached_uci_benchmark
    if cached_uci_benchmark is not None:
        return cached_uci_benchmark

    fpath = os.path.join(BASE_DIR, "data", "external", "uci_benchmark_results.json")
    try:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                cached_uci_benchmark = json.load(f)
        else:
            cached_uci_benchmark = {"error": "UCI benchmark results file not found"}
    except Exception as ex:
        print(f"[CCPRA Error] Could not load UCI benchmark: {ex}")
        cached_uci_benchmark = {"error": str(ex)}

    return cached_uci_benchmark or {}


def get_provenance_registry():
    """
    Returns the comprehensive provenance registry for all 5 verified datasets.
    """
    return {
        "verified_count": 5,
        "last_audit_timestamp": "2026-10-27T07:35:00Z",
        "datasets": [
            {
                "id": "ccpra_us_telco",
                "title": "CCPRA Primary Telecom Dataset",
                "publisher": "IBM Business Analytics / Kaggle Community",
                "license": "Apache License 2.0 / Open Benchmark",
                "records": 7043,
                "features": 32,
                "coverage": "1–72 Months Lifecycle",
                "source_url": "https://www.kaggle.com/datasets/blastchar/telco-customer-churn",
                "local_file": "data/processed/cleaned_customer_churn.csv",
                "role": "Primary portfolio churn analysis, saved Logistic Regression inference, and risk scoring.",
                "quality_status": "Cleaned & Verified (0 missing values)"
            },
            {
                "id": "uci_iranian_churn",
                "title": "UCI Iranian Telecom Churn Dataset",
                "publisher": "UCI Machine Learning Repository (Gharehchopogh et al.)",
                "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                "records": 3150,
                "features": 14,
                "coverage": "9-Month Observational Window",
                "source_url": "https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset",
                "local_file": "data/external/Customer Churn.csv",
                "role": "Independent model benchmark (evaluating behavioral telemetry: complaints, seconds, call failures).",
                "quality_status": "Verified (All 14 numeric features intact)"
            },
            {
                "id": "trai_subscription_mnp",
                "title": "TRAI Telecom Subscription & MNP Report (PR 125/2026)",
                "publisher": "Telecom Regulatory Authority of India (Government of India)",
                "license": "Open Government Data (OGD) Platform / Official TRAI Census",
                "records": 1360700000,
                "features": "National & Circle Telecom Census",
                "coverage": "August 2026 Monthly Census",
                "source_url": "https://www.trai.gov.in/release-publication/reports/telecom-subscriptions-reports",
                "local_file": "data/external/trai/trai_press_release_subscription_sep2026.pdf",
                "role": "Macro market intelligence: 1.36B subscriber base, operator broadband market share, and 15.83M monthly MNP churn requests.",
                "quality_status": "Verified (Official 25-page TRAI Release)"
            },
            {
                "id": "fcc_cgb_complaints",
                "title": "FCC Consumer Complaints Open Data (CGB 3xyp-aqkj)",
                "publisher": "Federal Communications Commission (FCC)",
                "license": "U.S. Public Domain / Data.gov Open Government Directive",
                "records": 5000,
                "features": 17,
                "coverage": "2016-05-23 to 2024-10-12",
                "source_url": "https://opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj",
                "local_file": "data/external/fcc_consumer_complaints_sample.json",
                "role": "US consumer dissatisfaction analysis: billing, availability, equipment, and delivery method friction.",
                "quality_status": "Verified (Live SODA REST API Feed)"
            },
            {
                "id": "mendeley_indian_telco",
                "title": "Mendeley Indian Telecom Dataset (Koomson 2024)",
                "publisher": "Mendeley Data / Patrick Koomson (doi:10.17632/px3dt72xdw.1)",
                "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
                "records": 2026,
                "features": 14,
                "coverage": "January 1 to January 11, 2020",
                "source_url": "https://data.mendeley.com/datasets/px3dt72xdw/1",
                "local_file": "data/external/IndiaTelecomData.csv",
                "role": "Developing cellular market comparative analysis and data hygiene audit.",
                "quality_status": "Audited (Identified 167 accounts with negative usage values)"
            }
        ]
    }


@app.route("/api/model-diagnostics")
def api_model_diagnostics():
    """
    Returns authentic held-out test set diagnostics:
    Cumulative gains & lift by decile, probability calibration curve & Brier score,
    and precision-recall curve.
    """
    return jsonify(get_model_diagnostics())


@app.route("/api/lifecycle-retention")
def api_lifecycle_retention():
    """
    Returns cross-sectional pseudo-retention survivor curves and cohort hazards across tenure.
    """
    return jsonify(get_lifecycle_retention())


@app.route("/api/distribution-comparison")
def api_distribution_comparison():
    """
    Returns statistical box plot five-number summaries (min, q1, median, q3, max, mean, iqr)
    comparing MonthlyCharges and Tenure for Churned vs Retained subscribers.
    """
    return jsonify(get_distribution_comparison())


@app.route("/api/dataset-comparison")
def api_dataset_comparison():
    """
    Returns external validation analysis and structural comparison between
    CCPRA (IBM Telco) and Mendeley Indian Telecom datasets.
    """
    return jsonify(get_dataset_comparison())


@app.route("/api/behavioral-intelligence")
def api_behavioral_intelligence():
    """
    Returns multivariate correlation matrix, 2D service-contract churn heatmap,
    stratified scatterplot sample (300 points), and financial exposure hierarchy.
    """
    return jsonify(get_behavioral_intelligence())


@app.route("/api/external-market-intelligence")
def api_external_market_intelligence():
    """
    Returns external macro market intelligence from official TRAI reports,
    FCC consumer complaints, and Mendeley telecom audits.
    """
    return jsonify(get_external_market_intelligence())


@app.route("/api/uci-benchmark")
def api_uci_benchmark():
    """
    Returns independent UCI Iranian Telecom Churn benchmark experiment metrics
    (Logistic Regression vs Random Forest on held-out split, and feature importance).
    """
    return jsonify(get_uci_benchmark())


@app.route("/api/provenance")
def api_provenance():
    """
    Returns data provenance registry for all 5 verified datasets.
    """
    return jsonify(get_provenance_registry())


if __name__ == "__main__":
    print("[CCPRA] Launching Customer Churn Prediction Website...")
    print("[CCPRA] Local address: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
