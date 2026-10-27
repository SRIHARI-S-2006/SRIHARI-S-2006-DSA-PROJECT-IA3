import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss

uci_path = "data/external/Customer Churn.csv"
df = pd.read_csv(uci_path)

# Clean column names (strip whitespace)
df.columns = [c.strip().replace('  ', ' ') for c in df.columns]

# Target is 'Churn'
X = df.drop(columns=['Churn'])
y = df['Churn']

print("UCI Dataset shape:", df.shape)
print("UCI Churn distribution:\n", y.value_counts(normalize=True))

# 80/20 Stratified Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]

metrics = {
    'dataset_name': 'UCI Iranian Telecom Churn Dataset',
    'source': 'UCI Machine Learning Repository (archive.ics.uci.edu/dataset/563)',
    'total_records': len(df),
    'test_records': len(y_test),
    'churn_rate': float(y.mean()),
    'models': {
        'Logistic Regression': {
            'accuracy': round(accuracy_score(y_test, y_pred_lr), 4),
            'precision': round(precision_score(y_test, y_pred_lr), 4),
            'recall': round(recall_score(y_test, y_pred_lr), 4),
            'f1': round(f1_score(y_test, y_pred_lr), 4),
            'roc_auc': round(roc_auc_score(y_test, y_prob_lr), 4),
            'brier': round(brier_score_loss(y_test, y_prob_lr), 4)
        },
        'Random Forest': {
            'accuracy': round(accuracy_score(y_test, y_pred_rf), 4),
            'precision': round(precision_score(y_test, y_pred_rf), 4),
            'recall': round(recall_score(y_test, y_pred_rf), 4),
            'f1': round(f1_score(y_test, y_pred_rf), 4),
            'roc_auc': round(roc_auc_score(y_test, y_prob_rf), 4),
            'brier': round(brier_score_loss(y_test, y_prob_rf), 4)
        }
    },
    'top_features_rf': [
        {'feature': feat, 'importance': round(imp, 4)}
        for feat, imp in sorted(zip(X.columns, rf.feature_importances_), key=lambda x: x[1], reverse=True)[:8]
    ]
}

print(json.dumps(metrics, indent=2))

with open('data/external/uci_benchmark_results.json', 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2)

print("Saved data/external/uci_benchmark_results.json")
