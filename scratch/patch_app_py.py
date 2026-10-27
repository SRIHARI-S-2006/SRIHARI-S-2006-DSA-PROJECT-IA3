app_path = r"website\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace api_scatter_data
old_scatter = """@app.route("/api/scatter-data")
def api_scatter_data():
    \"\"\"
    Returns an optimized stratified representative sample of customer records
    for high-performance scatter plotting (Tenure vs Monthly Charges).
    \"\"\"
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
            "x": int(row['tenure']),
            "y": round(float(row['MonthlyCharges']), 2),
            "churn": str(row['Churn']),
            "prob": round(float(row['Predicted_Churn_Probability'] * 100.0), 1) if 'Predicted_Churn_Probability' in row else 0.0,
            "contract": str(row['Contract']),
            "net": str(row['InternetService'])
        })

    return jsonify({"points": points, "total_sampled": len(points), "total_base": len(df_analytics)})"""

new_scatter = """@app.route("/api/scatter-data")
def api_scatter_data():
    \"\"\"
    Returns an optimized stratified representative sample of customer records
    for high-performance scatter plotting (Tenure vs Monthly Charges).
    \"\"\"
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
    })"""

if old_scatter in code:
    code = code.replace(old_scatter, new_scatter)
    print("Replaced api_scatter_data.")
else:
    print("Warning: old_scatter not found!")

# Replace api_advanced_charts
old_adv = """@app.route("/api/advanced-charts")
def api_advanced_charts():
    \"\"\"
    Returns authentic distributions for histograms, Pareto analysis,
    100% stacked distributions, and segment bubble charts.
    \"\"\"
    if df_analytics is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    # 1. Tenure Histogram (Split by Churn)
    tenure_bins = [0, 12, 24, 36, 48, 60, 72]
    tenure_labels = ['0-12 Mo', '13-24 Mo', '25-36 Mo', '37-48 Mo', '49-60 Mo', '61-72 Mo']
    t_cuts = pd.cut(df_analytics['tenure'], bins=tenure_bins, labels=tenure_labels, include_lowest=True)
    t_cross = pd.crosstab(t_cuts, df_analytics['Churn'])
    tenure_hist = {
        "labels": tenure_labels,
        "retained": [int(t_cross.loc[lbl].get('No', 0)) for lbl in tenure_labels if lbl in t_cross.index],
        "churned": [int(t_cross.loc[lbl].get('Yes', 0)) for lbl in tenure_labels if lbl in t_cross.index]
    }

    # 2. Monthly Charges Histogram (Split by Churn)
    charge_bins = [18.0, 35.0, 55.0, 75.0, 95.0, 120.0]
    charge_labels = ['$18-$35', '$35-$55', '$55-$75', '$75-$95', '$95-$120']
    c_cuts = pd.cut(df_analytics['MonthlyCharges'], bins=charge_bins, labels=charge_labels, include_lowest=True)
    c_cross = pd.crosstab(c_cuts, df_analytics['Churn'])
    charges_hist = {
        "labels": charge_labels,
        "retained": [int(c_cross.loc[lbl].get('No', 0)) for lbl in charge_labels if lbl in c_cross.index],
        "churned": [int(c_cross.loc[lbl].get('Yes', 0)) for lbl in charge_labels if lbl in c_cross.index]
    }

    # 3. Model Predicted Probability Distribution Histogram
    prob_bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    prob_labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
    p_cuts = pd.cut(df_analytics['Predicted_Churn_Probability'], bins=prob_bins, labels=prob_labels, include_lowest=True)
    p_counts = p_cuts.value_counts(sort=False)
    prob_hist = {
        "labels": prob_labels,
        "counts": [int(p_counts.get(lbl, 0)) for lbl in prob_labels],
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
        "cum_pct": [float(p) for p in cum_pct.values],
        "total_exposure": tot_hr_mrr
    }

    # 5. 100% Stacked Proportions (Historical Outcomes)
    def calc_stacked(col, order=None):
        ct = pd.crosstab(df_analytics[col], df_analytics['Churn'], normalize='index') * 100.0
        idx = order if order else list(ct.index)
        idx = [i for i in idx if i in ct.index]
        return {
            "labels": idx,
            "retained_pct": [round(float(ct.loc[i].get('No', 0)), 1) for i in idx],
            "churned_pct": [round(float(ct.loc[i].get('Yes', 0)), 1) for i in idx]
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
            
            # Map bubble radius (scale n between 8 and 36 px)
            radius = round(8 + (n / 2500) * 28, 1)

            bubbles.append({
                "label": f"{c} + {net}",
                "contract": c,
                "internet": net,
                "x": avg_charges,
                "y": churn_rate,
                "r": radius,
                "count": n,
                "churn_count": churn_n,
                "high_risk_count": hr_n
            })

    return jsonify({
        "tenure_histogram": tenure_hist,
        "charges_histogram": charges_hist,
        "predicted_prob_histogram": prob_hist,
        "pareto_revenue": pareto_chart,
        "stacked_proportions": {
            "contract": stacked_contract,
            "payment": stacked_payment,
            "tech_support": stacked_tech
        },
        "bubble_segments": bubbles
    })"""

new_adv = """@app.route("/api/advanced-charts")
def api_advanced_charts():
    \"\"\"
    Returns authentic distributions for heatmap, histograms, Pareto analysis,
    100% stacked distributions, and segment bubble charts.
    \"\"\"
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
    })"""

if old_adv in code:
    code = code.replace(old_adv, new_adv)
    print("Replaced api_advanced_charts.")
else:
    print("Warning: old_adv not found!")

# Replace api_threshold_sim
old_sim = """    return jsonify({
        "threshold": threshold,
        "threshold_pct": round(threshold * 100.0, 1),
        "flagged_count": flagged_count,
        "flagged_pct": flagged_pct,
        "flagged_mrr": flagged_mrr,
        "annual_flagged_mrr": annual_mrr,
        "total_base": total_base,
        "total_mrr": total_mrr,
        "actual_churners_captured": true_churners,
        "retained_in_flagged": retained_in_flagged
    })"""

new_sim = """    base_flagged = 1039
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
        "retained_in_flagged": retained_in_flagged
    })"""

if old_sim in code:
    code = code.replace(old_sim, new_sim)
    print("Replaced api_threshold_sim.")
else:
    print("Warning: old_sim not found!")

# Replace api_predict_batch preview records & KPI outputs
old_batch_return = """        # Prepare preview items (first 10)
        preview_cols = [
            'customerID' if 'customerID' in clean_df.columns else None,
            'Contract', 'tenure', 'MonthlyCharges',
            'Predicted_Churn_Probability', 'Predicted_Churn', 'Churn_Risk_Category',
            'Retention_Priority', 'Retention_Action'
        ]
        preview_cols = [c for c in preview_cols if c and c in clean_df.columns]
        preview_df = clean_df[preview_cols].head(10)

        preview_records = []
        for _, r in preview_df.iterrows():
            rec = {}
            for col in preview_cols:
                val = r[col]
                rec[col] = val if not pd.isna(val) else None
            preview_records.append(rec)

        return jsonify({
            "status": "success",
            "message": f"Successfully processed and scored {total_scored:,} records.",
            "summary": {
                "total_scored": total_scored,
                "high_risk_count": high_risk_count,
                "high_risk_pct": round((high_risk_count / total_scored * 100.0), 2) if total_scored > 0 else 0.0,
                "critical_count": critical_count,
                "total_mrr_scored": total_mrr_scored,
                "avg_risk_pct": avg_risk
            },
            "preview": preview_records
        })"""

new_batch_return = """        predicted_churners = int((clean_df['Predicted_Churn'] == 'Yes').sum())
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
        })"""

if old_batch_return in code:
    code = code.replace(old_batch_return, new_batch_return)
    print("Replaced api_predict_batch return.")
else:
    print("Warning: old_batch_return not found!")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated app.py successfully.")
