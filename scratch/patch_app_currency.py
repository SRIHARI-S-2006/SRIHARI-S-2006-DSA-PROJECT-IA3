app_js_path = r"website\static\app.js"

with open(app_js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Currency format helper replacement
old_overview_snippet = """    const elTotalMrr = document.getElementById("kpi-total-mrr");
    if (elTotalMrr) elTotalMrr.textContent = `$${data.total_mrr.toLocaleString()}`;

    const elAvgCharges = document.getElementById("kpi-avg-charges");
    if (elAvgCharges && data.avg_monthly_charges) {
      elAvgCharges.textContent = `Avg $${data.avg_monthly_charges} / subscriber`;
    }

    const elRevenueRisk = document.getElementById("kpi-revenue-risk");
    if (elRevenueRisk) elRevenueRisk.textContent = `$${data.monthly_revenue_at_risk.toLocaleString()}`;

    const elRevenueShare = document.getElementById("kpi-revenue-share");
    if (elRevenueShare) elRevenueShare.textContent = `${data.high_risk_revenue_share_pct}% of Monthly MRR`;

    const elAnnualRisk = document.getElementById("kpi-annual-risk");
    if (elAnnualRisk) elAnnualRisk.textContent = `$${(data.annual_revenue_at_risk / 1000000).toFixed(2)}M / yr`;

    // Revenue Intelligence Section KPIs
    const revTotalMrr = document.getElementById("rev-total-mrr");
    if (revTotalMrr) revTotalMrr.textContent = `$${data.total_mrr.toLocaleString()}`;

    const revHighRiskMrr = document.getElementById("rev-high-risk-mrr");
    if (revHighRiskMrr) revHighRiskMrr.textContent = `$${data.monthly_revenue_at_risk.toLocaleString()}`;

    const revExpLoss = document.getElementById("rev-expected-loss");
    if (revExpLoss) revExpLoss.textContent = `$${data.expected_monthly_loss.toLocaleString()}`;

    const revActualLost = document.getElementById("rev-actual-lost");
    if (revActualLost && data.actual_churned_revenue) {
      revActualLost.textContent = `$${data.actual_churned_revenue.toLocaleString()}`;
    }"""

new_overview_snippet = """    const fmtCurrency = (v) => {
      if (v === null || v === undefined || isNaN(v)) return "$0.00";
      return "$" + Number(v).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    };

    const elTotalMrr = document.getElementById("kpi-total-mrr");
    if (elTotalMrr) elTotalMrr.textContent = fmtCurrency(data.total_mrr);

    const elAvgCharges = document.getElementById("kpi-avg-charges");
    if (elAvgCharges && data.avg_monthly_charges) {
      elAvgCharges.textContent = `Avg ${fmtCurrency(data.avg_monthly_charges)} / subscriber`;
    }

    const elRevenueRisk = document.getElementById("kpi-revenue-risk");
    if (elRevenueRisk) elRevenueRisk.textContent = fmtCurrency(data.monthly_revenue_at_risk);

    const elRevenueShare = document.getElementById("kpi-revenue-share");
    if (elRevenueShare) elRevenueShare.textContent = `${data.high_risk_revenue_share_pct}% Monthly Share`;

    const elAnnualRisk = document.getElementById("kpi-annual-risk");
    if (elAnnualRisk) elAnnualRisk.textContent = `$${(data.annual_revenue_at_risk / 1000000).toFixed(2)}M / yr`;

    // Revenue Intelligence Section KPIs
    const revTotalMrr = document.getElementById("rev-total-mrr");
    if (revTotalMrr) revTotalMrr.textContent = fmtCurrency(data.total_mrr);

    const revHighRiskMrr = document.getElementById("rev-high-risk-mrr");
    if (revHighRiskMrr) revHighRiskMrr.textContent = fmtCurrency(data.monthly_revenue_at_risk);

    const revExpLoss = document.getElementById("rev-expected-loss");
    if (revExpLoss) revExpLoss.textContent = fmtCurrency(data.expected_monthly_loss);

    const revActualLost = document.getElementById("rev-actual-lost");
    if (revActualLost && data.actual_churned_revenue) {
      revActualLost.textContent = fmtCurrency(data.actual_churned_revenue);
    }"""

if old_overview_snippet in js:
    js = js.replace(old_overview_snippet, new_overview_snippet)
    print("Patched currency formatting in app.js")
else:
    print("Warning: old_overview_snippet not found in app.js")

# Refine Chart.js global defaults
old_chart_defaults = """    // Chart.js Default Styling
    Chart.defaults.color = "#94a3b8";
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 6;"""

new_chart_defaults = """    // Chart.js Default Styling - Taste Skill Enterprise Palette
    Chart.defaults.color = "#94a3b8";
    Chart.defaults.font.family = "'Inter', system-ui, -apple-system, sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.plugins.tooltip.backgroundColor = "rgba(11, 16, 27, 0.95)";
    Chart.defaults.plugins.tooltip.borderColor = "rgba(255, 255, 255, 0.12)";
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 6;
    Chart.defaults.plugins.tooltip.boxPadding = 4;
    Chart.defaults.plugins.tooltip.titleFont = { family: "'Inter', sans-serif", size: 12, weight: "600" };
    Chart.defaults.plugins.tooltip.bodyFont = { family: "'JetBrains Mono', monospace", size: 11 };"""

if old_chart_defaults in js:
    js = js.replace(old_chart_defaults, new_chart_defaults)
    print("Patched Chart.js defaults in app.js")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("app.js updated successfully.")
