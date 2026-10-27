import joblib
import pandas as pd
import numpy as np

model = joblib.load('models/selected_churn_model.joblib')
preprocessor = model.named_steps['preprocessor']
classifier = model.named_steps['classifier']

print("Classifier classes:", classifier.classes_)
print("Classifier intercept:", classifier.intercept_)
print("Classifier coef shape:", classifier.coef_.shape)

# Load 1 sample customer from dataset
df = pd.read_csv('data/processed/cleaned_customer_churn.csv')
sample = df.iloc[[0]].drop(columns=['customerID', 'Churn', 'Churn_Value'], errors='ignore')

# Transform sample
transformed = preprocessor.transform(sample)
if hasattr(transformed, 'toarray'):
    transformed = transformed.toarray()

# Feature names
if hasattr(preprocessor, 'get_feature_names_out'):
    feature_names = preprocessor.get_feature_names_out()
else:
    feature_names = [f"f_{i}" for i in range(transformed.shape[1])]

print(f"Num features: {len(feature_names)}")
coefs = classifier.coef_[0]
intercept = classifier.intercept_[0]

contributions = transformed[0] * coefs
decision_func = model.decision_function(sample)[0]
reconstructed = intercept + np.sum(contributions)
prob = model.predict_proba(sample)[0, 1]
sigmoid_prob = 1 / (1 + np.exp(-decision_func))

print(f"Decision function: {decision_func:.6f}")
print(f"Reconstructed sum: {reconstructed:.6f}")
print(f"Difference: {abs(decision_func - reconstructed):.1e}")
print(f"Model probability: {prob:.6f}")
print(f"Sigmoid probability: {sigmoid_prob:.6f}")

# Top 3 positive and negative
contrib_df = pd.DataFrame({
    'feature': feature_names,
    'value': transformed[0],
    'coef': coefs,
    'contrib': contributions
})

pos = contrib_df[contrib_df['contrib'] > 0].sort_values('contrib', ascending=False).head(3)
neg = contrib_df[contrib_df['contrib'] < 0].sort_values('contrib', ascending=True).head(3)

print("\n--- TOP RISK-INCREASING (POSITIVE LOG-ODDS) ---")
print(pos[['feature', 'value', 'coef', 'contrib']])

print("\n--- TOP RISK-REDUCING (NEGATIVE LOG-ODDS) ---")
print(neg[['feature', 'value', 'coef', 'contrib']])
