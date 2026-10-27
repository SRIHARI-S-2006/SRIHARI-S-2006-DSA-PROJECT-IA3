import pandas as pd
import numpy as np
import json

df = pd.read_csv('data/powerbi/customer_churn_analytics.csv')
print("Columns in analytics csv:", df.columns.tolist())

# 1. Correlation Matrix
corr_df = pd.DataFrame()
corr_df['Tenure'] = df['tenure']
corr_df['Monthly Charges'] = df['MonthlyCharges']
corr_df['Total Charges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
corr_df['Churn'] = (df['Churn'] == 'Yes').astype(int)
corr_df['Senior Citizen'] = (df['SeniorCitizen'] == 1).astype(int)
corr_df['Has Partner'] = (df['Partner'] == 'Yes').astype(int)
corr_df['Has Dependents'] = (df['Dependents'] == 'Yes').astype(int)

corr_matrix = corr_df.corr().round(3)
corr_result = {
    'variables': corr_matrix.columns.tolist(),
    'matrix': corr_matrix.values.tolist()
}
print("Correlation Variables:", corr_result['variables'])
print("Correlation Matrix Sample:\n", corr_matrix)

# 2. Service x Contract 2D Churn Heatmap
svc_contract = df.groupby(['InternetService', 'Contract']).agg(
    total=('customerID', 'count'),
    churns=('Churn', lambda x: (x == 'Yes').sum()),
    churn_rate=('Churn', lambda x: round((x == 'Yes').mean() * 100, 2)),
    avg_mrr=('MonthlyCharges', lambda x: round(x.mean(), 2))
).reset_index()
print("\nService x Contract Matrix:\n", svc_contract)

# 3. Stratified Scatterplot Sample (300 points)
sample_churned = df[df['Churn'] == 'Yes'].sample(n=150, random_state=42)
sample_retained = df[df['Churn'] == 'No'].sample(n=150, random_state=42)
sample_df = pd.concat([sample_churned, sample_retained])

scatter_points = []
for _, row in sample_df.iterrows():
    tot = float(row['TotalCharges']) if pd.notnull(row['TotalCharges']) and row['TotalCharges'] != ' ' else 0.0
    scatter_points.append({
        'id': row['customerID'],
        'x': int(row['tenure']),
        'y': round(float(row['MonthlyCharges']), 2),
        'r': max(4, min(14, int(tot / 600) + 4)), # radius proportional to total charges
        'churn': row['Churn'] == 'Yes',
        'risk': row.get('Churn_Risk_Category', 'Medium Risk'),
        'score': round(float(row.get('Predicted_Churn_Probability', 0.5)), 3),
        'contract': row['Contract']
    })

print(f"\nGenerated {len(scatter_points)} scatterplot points.")

# 4. Financial Concentration Treemap (Hierarchy: Risk Category -> Contract -> MRR)
treemap_hierarchy = []
for risk, r_grp in df.groupby('Churn_Risk_Category'):
    contracts = []
    for contract, c_grp in r_grp.groupby('Contract'):
        contracts.append({
            'name': contract,
            'mrr': round(float(c_grp['MonthlyCharges'].sum()), 2),
            'customers': int(len(c_grp)),
            'churn_rate': round(float((c_grp['Churn'] == 'Yes').mean() * 100), 2)
        })
    treemap_hierarchy.append({
        'name': risk,
        'total_mrr': round(float(r_grp['MonthlyCharges'].sum()), 2),
        'total_customers': int(len(r_grp)),
        'children': contracts
    })

print("\nFinancial Treemap Summary:")
for node in treemap_hierarchy:
    print(f" - {node['name']}: ${node['total_mrr']:,.2f} MRR ({node['total_customers']} customers)")

output_analytics = {
    'correlation': corr_result,
    'service_contract_matrix': svc_contract.to_dict(orient='records'),
    'scatter_sample': scatter_points,
    'financial_hierarchy': treemap_hierarchy
}

with open('data/processed/advanced_behavioral_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(output_analytics, f, indent=2)

print("\nSaved data/processed/advanced_behavioral_metrics.json successfully!")
