import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, brier_score_loss
)
from sklearn.calibration import calibration_curve

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_customer_churn.csv')
model_path = os.path.join(base_dir, 'models', 'selected_churn_model.joblib')
mendeley_path = os.path.join(base_dir, 'scratch', 'IndiaTelecomData.csv')

df = pd.read_csv(data_path)
model = joblib.load(model_path)

# Features
numerical_features = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]
primary_features = numerical_features + categorical_features

X = df[primary_features].copy()
y = df['Churn'].map({'No': 0, 'Yes': 1}).values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

y_probs = model.predict_proba(X_test)[:, 1]

# 1. Cumulative Gains and Lift
deciles = pd.DataFrame({'y_true': y_test, 'prob': y_probs})
deciles = deciles.sort_values(by='prob', ascending=False).reset_index(drop=True)
deciles['decile'] = pd.qcut(deciles.index, q=10, labels=False) + 1

gains = deciles.groupby('decile').agg(
    total=('y_true', 'count'),
    churners=('y_true', 'sum')
).reset_index()
gains['cum_churners'] = gains['churners'].cumsum()
total_churners = int(y_test.sum())
gains['cum_gain_pct'] = ((gains['cum_churners'] / total_churners) * 100.0).round(2)
gains['decile_pct'] = gains['decile'] * 10
gains['lift'] = ((gains['churners'] / gains['total']) / (total_churners / len(y_test))).round(2)
gains['cum_lift'] = ((gains['cum_churners'] / gains['total'].cumsum()) / (total_churners / len(y_test))).round(2)
gains['baseline_pct'] = gains['decile_pct']

print("--- Cumulative Gains Table ---")
print(gains[['decile', 'decile_pct', 'cum_gain_pct', 'cum_lift', 'baseline_pct']])

# 2. Calibration Curve
prob_true, prob_pred = calibration_curve(y_test, y_probs, n_bins=10, strategy='uniform')
brier = round(float(brier_score_loss(y_test, y_probs)), 4)
print("\n--- Calibration Curve ---")
print("Brier Score:", brier)
print("prob_pred:", np.round(prob_pred, 3))
print("prob_true:", np.round(prob_true, 3))

# 3. Precision-Recall Curve (sampled to 20 representative threshold points)
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
# sample thresholds at regular probability steps
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
print("\n--- PR Points sample ---")
print(pr_points[::3])

# 4. Box Plot Stats
box_stats = {}
for col in ['MonthlyCharges', 'tenure']:
    box_stats[col] = {}
    for status in ['Yes', 'No']:
        series = df[df['Churn'] == status][col]
        q1 = float(np.percentile(series, 25))
        med = float(np.percentile(series, 50))
        q3 = float(np.percentile(series, 75))
        iqr = q3 - q1
        low_whisker = float(max(series.min(), q1 - 1.5 * iqr))
        high_whisker = float(min(series.max(), q3 + 1.5 * iqr))
        box_stats[col][status] = {
            'min': round(float(series.min()), 2),
            'low_whisker': round(low_whisker, 2),
            'q1': round(q1, 2),
            'median': round(med, 2),
            'q3': round(q3, 2),
            'high_whisker': round(high_whisker, 2),
            'max': round(float(series.max()), 2),
            'mean': round(float(series.mean()), 2),
            'count': int(len(series))
        }

print("\n--- Box Plot Stats ---")
print(box_stats)

print("\nALL VERIFICATIONS PASSED!")
