import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js_path = os.path.join(base_dir, 'website', 'static', 'app.js')

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update subtab-model-evaluation to also trigger loadModelDiagnostics()
old_eval_trigger = """      if (targetSubtab === "model-evaluation") {
        renderModelComparisonChart();
      }"""
new_eval_trigger = """      if (targetSubtab === "model-evaluation") {
        renderModelComparisonChart();
        loadModelDiagnostics();
      }"""
if old_eval_trigger in js:
    js = js.replace(old_eval_trigger, new_eval_trigger)
    print("Updated subtab switching to call loadModelDiagnostics()")

# 2. Update loadAdvancedVisualizations to also call lifecycle and box plot
old_adv_call = """  initThresholdSimulator();"""
new_adv_call = """  loadLifecycleRetention();
  loadDistributionBoxPlot();
  loadModelDiagnostics();
  initThresholdSimulator();"""
if old_adv_call in js and "loadLifecycleRetention();" not in js:
    js = js.replace(old_adv_call, new_adv_call, 1)
    print("Updated DOMContentLoaded to call lifecycle, box plot, and diagnostics")

# 3. Code for new visualizations
new_code = """
/* ==============================================================================
   DISTINCTIVE ANALYTICAL VIEWS & MODEL DIAGNOSTICS (PHASE 3 IMPLEMENTATION)
   ============================================================================== */

// State for Box Plot
let currentBoxMetric = "MonthlyCharges";
let cachedBoxData = null;

// 1. Customer Lifecycle & Pseudo-Retention Survivor Curve
async function loadLifecycleRetention() {
  const ctx = document.getElementById("lifecycleRetentionChart");
  if (!ctx) return;

  try {
    const res = await fetch("/api/lifecycle-retention");
    const data = await res.json();
    if (!data || !data.milestones) return;

    if (chartInstances["lifecycleRetentionChart"]) {
      chartInstances["lifecycleRetentionChart"].destroy();
    }

    const labels = data.milestones.map(m => `${m.milestone_months} Mo`);
    const retentionRates = data.milestones.map(m => m.pseudo_retention_rate);
    const activeCounts = data.milestones.map(m => m.accounts_active_at_milestone);

    chartInstances["lifecycleRetentionChart"] = new Chart(ctx, {
      data: {
        labels: labels,
        datasets: [
          {
            type: "line",
            label: "Pseudo-Retention Rate (%)",
            data: retentionRates,
            borderColor: "#38bdf8",
            backgroundColor: "rgba(56, 189, 248, 0.12)",
            fill: true,
            tension: 0.25,
            pointRadius: 4,
            pointHoverRadius: 6,
            yAxisID: "y"
          },
          {
            type: "bar",
            label: "Active Accounts (Count)",
            data: activeCounts,
            backgroundColor: "rgba(16, 185, 129, 0.25)",
            borderColor: "#10b981",
            borderWidth: 1,
            borderRadius: 3,
            maxBarThickness: 28,
            yAxisID: "y1"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            type: "linear",
            position: "left",
            min: 60,
            max: 100,
            grid: { color: "rgba(51, 65, 85, 0.3)" },
            ticks: { callback: v => `${v}%` },
            title: { display: true, text: "Empirical Retention Rate (%)", color: "#94a3b8" }
          },
          y1: {
            type: "linear",
            position: "right",
            beginAtZero: true,
            max: 8000,
            grid: { drawOnChartArea: false },
            ticks: { callback: v => v.toLocaleString() },
            title: { display: true, text: "Active Subscribers Remaining", color: "#94a3b8" }
          },
          x: {
            grid: { color: "rgba(51, 65, 85, 0.15)" },
            title: { display: true, text: "Tenure Milestone", color: "#94a3b8" }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === "line") {
                  return `Survivor Retention: ${c.parsed.y}% of cohort`;
                }
                return `Active Accounts: ${c.parsed.y.toLocaleString()} subscribers`;
              }
            }
          }
        }
      }
    });
  } catch (err) {
    console.error("Error loading lifecycle retention:", err);
  }
}

// 2. Statistical Box Plot (Charges & Tenure)
async function loadDistributionBoxPlot() {
  const canvas = document.getElementById("distributionBoxPlotChart");
  if (!canvas) return;

  try {
    if (!cachedBoxData) {
      const res = await fetch("/api/distribution-comparison");
      cachedBoxData = await res.json();
    }
    renderBoxPlotCanvas(currentBoxMetric);
  } catch (err) {
    console.error("Error loading box plot:", err);
  }
}

window.switchBoxMetric = function(metric) {
  currentBoxMetric = metric;
  document.querySelectorAll("#btn-box-charges, #btn-box-tenure").forEach(b => b.classList.remove("active"));
  const btn = document.getElementById(metric === "MonthlyCharges" ? "btn-box-charges" : "btn-box-tenure");
  if (btn) btn.classList.add("active");

  const churnMedEl = document.getElementById("box-churn-med");
  const retainMedEl = document.getElementById("box-retain-med");
  const textEl = document.getElementById("box-plot-insight-text");

  if (cachedBoxData && cachedBoxData[metric]) {
    const c = cachedBoxData[metric]["Yes"];
    const r = cachedBoxData[metric]["No"];
    if (metric === "MonthlyCharges") {
      if (churnMedEl) churnMedEl.textContent = `$${c.median.toFixed(2)}`;
      if (retainMedEl) retainMedEl.textContent = `$${r.median.toFixed(2)}`;
      if (textEl) textEl.textContent = `Monthly billing shows stark divergence: Churned median is $${c.median} (IQR $${c.iqr}) vs. Retained median $${r.median} (IQR $${r.iqr}).`;
    } else {
      if (churnMedEl) churnMedEl.textContent = `${c.median} mo`;
      if (retainMedEl) retainMedEl.textContent = `${r.median} mo`;
      if (textEl) textEl.textContent = `Tenure distribution highlights massive early vulnerability: 50% of churners leave by month ${c.median} (IQR ${c.iqr} mo) vs. retained median of ${r.median} mo.`;
    }
  }

  renderBoxPlotCanvas(metric);
};

function renderBoxPlotCanvas(metric) {
  const canvas = document.getElementById("distributionBoxPlotChart");
  if (!canvas || !cachedBoxData || !cachedBoxData[metric]) return;

  const data = cachedBoxData[metric];
  const churn = data["Yes"];
  const retain = data["No"];

  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const width = rect.width || canvas.parentElement.clientWidth || 500;
  const height = rect.height || 260;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, width, height);

  // Layout bounds
  const padLeft = 60;
  const padRight = 30;
  const padTop = 30;
  const padBottom = 40;
  const plotWidth = width - padLeft - padRight;
  const plotHeight = height - padTop - padBottom;

  // Determine min/max range
  const globalMin = metric === "MonthlyCharges" ? 10 : 0;
  const globalMax = metric === "MonthlyCharges" ? 130 : 80;

  const yScale = val => padTop + plotHeight - ((val - globalMin) / (globalMax - globalMin)) * plotHeight;

  // Gridlines and Y-axis ticks
  ctx.strokeStyle = "rgba(51, 65, 85, 0.35)";
  ctx.lineWidth = 1;
  ctx.font = "11px Inter, sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.textAlign = "right";

  const tickStep = metric === "MonthlyCharges" ? 20 : 12;
  for (let t = globalMin; t <= globalMax; t += tickStep) {
    const yPos = yScale(t);
    ctx.beginPath();
    ctx.moveTo(padLeft, yPos);
    ctx.lineTo(width - padRight, yPos);
    ctx.stroke();

    const label = metric === "MonthlyCharges" ? `$${t}` : `${t} mo`;
    ctx.fillText(label, padLeft - 8, yPos + 4);
  }

  // Draw 2 Box Plots: Col 1 = Retained, Col 2 = Churned
  const groups = [
    { name: "Retained (No)", stats: retain, color: "#10b981", colCenter: padLeft + plotWidth * 0.32 },
    { name: "Churned (Yes)", stats: churn, color: "#f43f5e", colCenter: padLeft + plotWidth * 0.72 }
  ];

  const boxWidth = Math.min(85, plotWidth * 0.28);

  groups.forEach(g => {
    const s = g.stats;
    const cx = g.colCenter;
    const yQ1 = yScale(s.q1);
    const yMed = yScale(s.median);
    const yQ3 = yScale(s.q3);
    const yMin = yScale(s.min);
    const yMax = yScale(s.max);
    const yMean = yScale(s.mean);

    // Whisker line (Min to Max)
    ctx.strokeStyle = g.color;
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(cx, yMin);
    ctx.lineTo(cx, yQ1);
    ctx.moveTo(cx, yQ3);
    ctx.lineTo(cx, yMax);
    ctx.stroke();

    // Top & Bottom Crossbars
    ctx.beginPath();
    ctx.moveTo(cx - 14, yMin);
    ctx.lineTo(cx + 14, yMin);
    ctx.moveTo(cx - 14, yMax);
    ctx.lineTo(cx + 14, yMax);
    ctx.stroke();

    // Box (Q1 to Q3)
    ctx.fillStyle = g.color === "#10b981" ? "rgba(16, 185, 129, 0.22)" : "rgba(244, 63, 94, 0.22)";
    const bTop = Math.min(yQ1, yQ3);
    const bHeight = Math.abs(yQ1 - yQ3);
    ctx.fillRect(cx - boxWidth / 2, bTop, boxWidth, bHeight);

    ctx.strokeStyle = g.color;
    ctx.lineWidth = 2;
    ctx.strokeRect(cx - boxWidth / 2, bTop, boxWidth, bHeight);

    // Median Line
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(cx - boxWidth / 2, yMed);
    ctx.lineTo(cx + boxWidth / 2, yMed);
    ctx.stroke();

    // Mean indicator (diamond)
    ctx.fillStyle = "#fbbf24";
    ctx.beginPath();
    ctx.moveTo(cx, yMean - 4);
    ctx.lineTo(cx + 4, yMean);
    ctx.lineTo(cx, yMean + 4);
    ctx.lineTo(cx - 4, yMean);
    ctx.closePath();
    ctx.fill();

    // Group labels underneath
    ctx.font = "600 12px Inter, sans-serif";
    ctx.fillStyle = g.color;
    ctx.textAlign = "center";
    ctx.fillText(g.name, cx, height - 14);

    // Value Badges (Median & Mean)
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = "#ffffff";
    const prefix = metric === "MonthlyCharges" ? "$" : "";
    const suffix = metric === "MonthlyCharges" ? "" : "m";
    ctx.fillText(`Med: ${prefix}${s.median.toFixed(1)}${suffix}`, cx, yMed - 6);
  });
}

// 3. Model Diagnostics (Cumulative Gains, Calibration, PR Curve)
async function loadModelDiagnostics() {
  try {
    const res = await fetch("/api/model-diagnostics");
    const data = await res.json();
    if (!data || data.error) return;

    renderCumulativeGainsChart(data.cumulative_gains);
    renderCalibrationCurveChart(data.calibration);
    renderPrecisionRecallChart(data.pr_curve);
  } catch (err) {
    console.error("Error loading model diagnostics:", err);
  }
}

// 3a. Cumulative Gains Chart
function renderCumulativeGainsChart(gainsData) {
  const ctx = document.getElementById("cumulativeGainsChart");
  if (!ctx || !gainsData) return;

  if (chartInstances["cumulativeGainsChart"]) {
    chartInstances["cumulativeGainsChart"].destroy();
  }

  const decileLabels = gainsData.map(g => `${g.decile * 10}%`);
  const gainValues = gainsData.map(g => g.cum_gain_pct);
  const baselineValues = gainsData.map(g => g.decile * 10);
  const liftValues = gainsData.map(g => g.cum_lift);

  chartInstances["cumulativeGainsChart"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: decileLabels,
      datasets: [
        {
          label: "Cumulative Churners Captured (%)",
          data: gainValues,
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",
          fill: true,
          pointRadius: 5,
          tension: 0.15,
          yAxisID: "y"
        },
        {
          label: "Baseline (Random Selection 1:1)",
          data: baselineValues,
          borderColor: "#64748b",
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false,
          yAxisID: "y"
        },
        {
          label: "Cumulative Lift (Factor)",
          data: liftValues,
          borderColor: "#c084fc",
          backgroundColor: "#c084fc",
          pointRadius: 4,
          tension: 0.15,
          fill: false,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 105,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` },
          title: { display: true, text: "Cumulative % of True Churners Captured", color: "#94a3b8" }
        },
        y1: {
          position: "right",
          beginAtZero: true,
          max: 3.5,
          grid: { drawOnChartArea: false },
          ticks: { callback: v => `${v.toFixed(1)}×` },
          title: { display: true, text: "Lift Multiplier", color: "#94a3b8" }
        },
        x: {
          title: { display: true, text: "Top % of Population Targeted (Deciles)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.2)" }
        }
      },
      plugins: {
        legend: { position: "top", labels: { boxWidth: 10, padding: 8 } },
        tooltip: {
          callbacks: {
            label: c => {
              if (c.dataset.label.includes("Lift")) {
                return `Cumulative Lift: ${c.parsed.y}× higher than random`;
              }
              return `${c.dataset.label}: ${c.parsed.y}%`;
            }
          }
        }
      }
    }
  });
}

// 3b. Calibration Curve / Reliability Diagram
function renderCalibrationCurveChart(calData) {
  const ctx = document.getElementById("calibrationCurveChart");
  if (!ctx || !calData) return;

  if (chartInstances["calibrationCurveChart"]) {
    chartInstances["calibrationCurveChart"].destroy();
  }

  const modelPoints = calData.prob_pred.map((p, i) => ({
    x: p,
    y: calData.prob_true[i]
  }));

  const perfectPoints = [
    { x: 0, y: 0 },
    { x: 25, y: 25 },
    { x: 50, y: 50 },
    { x: 75, y: 75 },
    { x: 100, y: 100 }
  ];

  chartInstances["calibrationCurveChart"] = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Logistic Regression Pipeline",
          data: modelPoints,
          borderColor: "#2dd4bf",
          backgroundColor: "#2dd4bf",
          showLine: true,
          tension: 0.15,
          pointRadius: 5,
          pointHoverRadius: 7
        },
        {
          label: "Perfect Calibration (Diagonal)",
          data: perfectPoints,
          borderColor: "#64748b",
          borderDash: [5, 5],
          pointRadius: 0,
          showLine: true,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: "linear",
          min: 0,
          max: 100,
          title: { display: true, text: "Mean Predicted Churn Probability (%)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` }
        },
        y: {
          min: 0,
          max: 100,
          title: { display: true, text: "Observed Empirical Positive Fraction (%)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` }
        }
      },
      plugins: {
        legend: { position: "top", labels: { boxWidth: 10, padding: 8 } },
        tooltip: {
          callbacks: {
            label: c => {
              if (c.dataset.label.includes("Perfect")) return "Perfect 1:1 Calibration";
              return `Pred: ${c.parsed.x.toFixed(1)}% | Actual: ${c.parsed.y.toFixed(1)}%`;
            }
          }
        }
      }
    }
  });
}

// 3c. Precision-Recall Curve linked to Thresholds
function renderPrecisionRecallChart(prPoints) {
  const ctx = document.getElementById("precisionRecallChart");
  if (!ctx || !prPoints) return;

  if (chartInstances["precisionRecallChart"]) {
    chartInstances["precisionRecallChart"].destroy();
  }

  const thresholdLabels = prPoints.map(p => p.threshold.toFixed(2));
  const precisionData = prPoints.map(p => p.precision);
  const recallData = prPoints.map(p => p.recall);
  const f1Data = prPoints.map(p => p.f1_score);

  chartInstances["precisionRecallChart"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: thresholdLabels,
      datasets: [
        {
          label: "Precision (%) [Purity of Churn Alert]",
          data: precisionData,
          borderColor: "#10b981",
          backgroundColor: "#10b981",
          pointRadius: 4,
          tension: 0.2
        },
        {
          label: "Recall (%) [Capture Rate of Churners]",
          data: recallData,
          borderColor: "#f43f5e",
          backgroundColor: "#f43f5e",
          pointRadius: 4,
          tension: 0.2
        },
        {
          label: "F1-Score (%) [Harmonic Mean]",
          data: f1Data,
          borderColor: "#c084fc",
          backgroundColor: "#c084fc",
          pointRadius: 4,
          borderDash: [4, 4],
          tension: 0.2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 105,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` },
          title: { display: true, text: "Metric Performance (%)", color: "#94a3b8" }
        },
        x: {
          title: { display: true, text: "Decision Boundary Threshold (Probability)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.2)" }
        }
      },
      plugins: {
        legend: { position: "top", labels: { boxWidth: 10, padding: 10 } },
        tooltip: {
          callbacks: {
            title: c => `Threshold τ = ${c[0].label}`,
            label: c => `${c.dataset.label}: ${c.parsed.y}%`
          }
        }
      }
    }
  });
}
"""

if "function loadLifecycleRetention()" not in js:
    js += "\n" + new_code
    print("Appended Phase 3 visualization functions to app.js")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js successfully!")
