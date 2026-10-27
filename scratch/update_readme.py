readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Flask Website Section into README
web_section = """
---

## Production Web Application (Flask Enterprise Dashboard)

In addition to Power BI, CCPRA provides a standalone **Flask SaaS Analytics Dashboard** offering real-time model inference, interactive multidimensional cohort exploration, operational risk simulation, and batch CSV predictions.

### Core Workspaces:
1. **Executive Overview**:
   - Portfolio KPIs: Total Customer Base (7,043), Actual Historical Churn Rate (26.54%), High-Risk Subscribers (1,039), Portfolio MRR ($456,116.60), High-Risk Monthly Charges ($85,546.25 / 18.76% of MRR).
   - Ground Truth Churn Donut (5,174 Retained vs 1,869 Churned).
   - Contract Term Churn Comparison & Risk Tier Revenue Exposure.
2. **Churn Analytics**:
   - **Contract × Internet Service Ground Truth Churn Heatmap**: 3x3 interactive cross-tabulation intensity matrix with customer count and actual churn rate per cell; click to drill down into Customer Explorer.
   - **Customer Scatter Plot (Stratified n=700)**: Tenure (0–72 mo) vs Monthly Charges ($18–$120) colored by historical churn status with individual hover tooltips.
   - **Numeric Distribution Histograms**: Explicit 12-month tenure bins and billing charge ranges split by churn outcomes.
   - **100% Stacked Proportion Chart**: Observed historical outcome distributions with dimension toggles for Contract, Payment Method, and Tech Support.
3. **Customer Segments**:
   - **Multi-Segment Bubble Matrix**: 9 contract × internet service segments plotted across Average Monthly Charges ($) vs Historical Churn Rate (%) with bubble radius scaled to subscriber count; click to explore.
   - **Interactive Segment Comparison Tool**: Head-to-head benchmarking between any two customer segments with comparative delta scorecards.
4. **Revenue Intelligence**:
   - **Revenue-Risk Pareto Analysis (80/20 Rule)**: High-risk MRR exposure by billing channel with cumulative share line (Electronic check accounts for 82.49% of high-risk exposure).
   - **Operational Risk Threshold Simulator**: Dynamic slider (0.10 to 0.90) simulating operational workload and flagged MRR coverage.
   - **Transparent Retention Scenario**: Verified 25% high-risk retention math protecting $21,386.56/mo ($256,638.75/yr).
5. **Customer Explorer**:
   - Searchable subscriber registry (7,043 records) with filtering by Risk Tier, Contract, Internet, and Churn status, sortable columns, pagination, and filtered CSV export.
   - Slide-out customer detail inspector drawer displaying individual account parameters and prescribed retention playbooks.
6. **Prediction Lab**:
   - **Real-Time Single Predictor**: Form input evaluating subscriber parameters via the genuine trained pipeline.
   - **Batch Customer Prediction (CSV Engine)**: Upload CSV files, validate 19 required features, execute pipeline scoring, preview predictions, and download scored CSV results with prescribed playbooks.
   - **Model Evaluation & Diagnostics**: Holdout test metrics benchmark (84.21% ROC-AUC), confusion matrix diagnostics (926 TN, 109 FP, 165 FN, 209 TP = 1,409 holdout records), and predicted-risk distribution histogram.
"""

target_marker = "## How to Run"
if target_marker in content:
    content = content.replace(target_marker, web_section + "\n" + target_marker)
    print("Added Web Application section to README.md")

# Update How to Run with website startup instructions
old_run_section = """### 3. Open Power BI Dashboard
Launch Microsoft Power BI Desktop and open:
- `CCPRA_Customer_Churn_Analytics_FINAL.pbix` (or `CCPRA_Customer_Churn_Analytics_WORKING.pbix`)
- If prompted to refresh data, ensure data source points to `data/powerbi/customer_churn_analytics.csv`."""

new_run_section = """### 3. Launch Flask Web Application
To start the interactive analytics website locally:
```bash
python website/app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 4. Open Power BI Dashboard
Launch Microsoft Power BI Desktop and open:
- `CCPRA_Customer_Churn_Analytics_FINAL.pbix` (or `CCPRA_Customer_Churn_Analytics_WORKING.pbix`)
- If prompted to refresh data, ensure data source points to `data/powerbi/customer_churn_analytics.csv`."""

if old_run_section in content:
    content = content.replace(old_run_section, new_run_section)
    print("Updated How to Run section in README.md")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated README.md successfully.")
