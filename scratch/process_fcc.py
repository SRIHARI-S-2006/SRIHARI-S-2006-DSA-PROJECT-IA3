import json
import pandas as pd
from collections import Counter

with open('data/external/fcc_consumer_complaints_sample.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data)

# Clean fields
df['issue_type'] = df['issue_type'].fillna('Unknown').replace({'': 'Other'})
df['method'] = df['method'].fillna('Unspecified').replace({'': 'Unspecified'})
df['issue'] = df['issue'].fillna('General').replace({'': 'General'})
df['state'] = df['state'].fillna('Unknown').replace({'': 'Unknown'})

# Top issues
issue_counts = df['issue'].value_counts().head(8).to_dict()

# Top methods
method_counts = df['method'].value_counts().head(6).to_dict()

# Method by issue matrix (top 4 methods x top 4 issues)
top_methods = list(df['method'].value_counts().head(4).index)
top_issues = list(df['issue'].value_counts().head(4).index)

matrix = {}
for m in top_methods:
    sub = df[df['method'] == m]
    matrix[m] = {iss: int((sub['issue'] == iss).sum()) for iss in top_issues}

# Top states
state_counts = df['state'].value_counts().head(10).to_dict()

# Ticket created date parsing
df['ticket_date'] = pd.to_datetime(df['ticket_created'], errors='coerce')
valid_dates = df.dropna(subset=['ticket_date']).copy()
valid_dates['year_month'] = valid_dates['ticket_date'].dt.to_period('M').astype(str)
monthly_trend = valid_dates['year_month'].value_counts().sort_index().tail(12).to_dict()

fcc_metrics = {
    'dataset_name': 'FCC Consumer Complaints Open Data (CGB)',
    'source': 'Federal Communications Commission (opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj)',
    'total_sample_records': len(df),
    'date_range': f"{valid_dates['ticket_date'].min().strftime('%Y-%m-%d')} to {valid_dates['ticket_date'].max().strftime('%Y-%m-%d')}",
    'top_issues': issue_counts,
    'top_methods': method_counts,
    'method_issue_matrix': matrix,
    'top_states': state_counts,
    'monthly_trend': monthly_trend
}

print(json.dumps(fcc_metrics, indent=2))

with open('data/external/fcc_processed_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(fcc_metrics, f, indent=2)

print("Saved data/external/fcc_processed_metrics.json")
