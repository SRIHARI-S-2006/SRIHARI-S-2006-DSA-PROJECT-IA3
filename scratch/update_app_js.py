app_js_path = r"website\static\app.js"

with open(app_js_path, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update DOMContentLoaded to invoke advanced features
old_dom_content = """document.addEventListener("DOMContentLoaded", () => {
  // 1. Navigation System (6 Core Workspaces)
  initNavigation();

  // 2. Executive Overview & Revenue Intelligence KPIs
  loadOverview();

  // 3. Interactive Churn Analytics
  initAnalyticsWorkspace();

  // 4. Customer Segments Workspace & Cross-Tabulation Matrix
  loadCustomerSegments();

  // 5. Customer Explorer & Detail Drawer
  initCustomerExplorer();

  // 6. Prediction Lab & Model Evaluation Diagnostics
  initPredictionLab();
});"""

new_dom_content = """document.addEventListener("DOMContentLoaded", () => {
  // 1. Navigation System (6 Core Workspaces)
  initNavigation();

  // 2. Executive Overview & Revenue Intelligence KPIs
  loadOverview();

  // 3. Interactive Churn Analytics
  initAnalyticsWorkspace();

  // 4. Customer Segments Workspace & Cross-Tabulation Matrix
  loadCustomerSegments();

  // 5. Customer Explorer & Detail Drawer
  initCustomerExplorer();

  // 6. Prediction Lab & Model Evaluation Diagnostics
  initPredictionLab();

  // 7. Advanced Analytical Visualizations & Features
  loadAdvancedVisualizations();
  initThresholdSimulator();
  initBatchPrediction();
});"""

if old_dom_content in js:
    js = js.replace(old_dom_content, new_dom_content)
    print("Updated DOMContentLoaded in app.js")
else:
    print("Warning: old_dom_content not found in app.js")

# 2. Add the implementation of the advanced features to the bottom of app.js
advanced_js = """
/* ==============================================================================
   7. ADVANCED VISUALIZATIONS & FEATURES IMPLEMENTATION
   ============================================================================== */
let cachedAdvancedData = null;
let currentStackedDim = "contract";

async function loadAdvancedVisualizations() {
  try {
    const [advRes, scatterRes] = await Promise.all([
      fetch("/api/advanced-charts"),
      fetch("/api/scatter-data")
    ]);
    const advData = await advRes.json();
    const scatterData = await scatterRes.json();

    if (!advData.error) {
      cachedAdvancedData = advData;

      // Render Churn Heatmap
      renderHeatmap(advData.heatmap);

      // Render Histograms
      renderHistograms(advData.tenure_histogram, advData.charges_histogram);

      // Render 100% Stacked Proportion
      renderStackedProportion(advData.stacked_100, currentStackedDim);

      // Render Segment Bubble Chart
      renderSegmentBubbleChart(advData.bubble_segments);

      // Initialize Segment Comparison Tool
      initSegmentComparison(advData.bubble_segments);

      // Render Revenue-Risk Pareto Chart
      renderParetoChart(advData.pareto);

      // Render Predicted-Risk Distribution Histogram
      renderPredictedRiskHist(advData.predicted_risk_histogram);
    }

    if (!scatterData.error && scatterData.points) {
      renderScatterChart(scatterData.points);
    }
  } catch (err) {
    console.error("Error loading advanced visualizations:", err);
  }
}

/* --- A. CHURN HEATMAP (Contract x Internet Service) --- */
function renderHeatmap(heatmapData) {
  const container = document.getElementById("churn-heatmap-container");
  if (!container || !heatmapData) return;

  container.innerHTML = "";

  // Column Headers: Empty top-left, then Internet Services
  const cornerHeader = document.createElement("div");
  cornerHeader.className = "heatmap-header-col";
  cornerHeader.textContent = "Contract \\ Internet";
  container.appendChild(cornerHeader);

  heatmapData.columns.forEach(col => {
    const hCol = document.createElement("div");
    hCol.className = "heatmap-header-col";
    hCol.textContent = col;
    container.appendChild(hCol);
  });

  // Rows
  heatmapData.rows.forEach(contract => {
    // Row Header
    const rHeader = document.createElement("div");
    rHeader.className = "heatmap-header-row";
    rHeader.textContent = contract;
    container.appendChild(rHeader);

    // Cells
    heatmapData.columns.forEach(internet => {
      const cellKey = `${contract}__${internet}`;
      const cellData = heatmapData.cells[cellKey];
      const cellDiv = document.createElement("div");
      cellDiv.className = "heatmap-cell";

      if (cellData) {
        const rate = cellData.churn_rate;
        const count = cellData.total_customers;
        const churned = cellData.churned_customers;

        // Color interpolation based on historical churn rate
        let bgStyle = "";
        let textCol = "#ffffff";
        if (rate >= 45) {
          bgStyle = `rgba(239, 68, 68, ${0.45 + (rate - 45) / 55 * 0.45})`;
          textCol = "#fecaca";
        } else if (rate >= 25) {
          bgStyle = `rgba(245, 158, 11, ${0.35 + (rate - 25) / 20 * 0.35})`;
          textCol = "#fef08a";
        } else if (rate >= 10) {
          bgStyle = `rgba(56, 189, 248, ${0.25 + (rate - 10) / 15 * 0.25})`;
          textCol = "#bae6fd";
        } else {
          bgStyle = `rgba(16, 185, 129, ${0.2 + rate / 10 * 0.25})`;
          textCol = "#a7f3d0";
        }

        cellDiv.style.background = bgStyle;
        cellDiv.title = `${contract} + ${internet}\\nChurn Rate: ${rate}% (${churned.toLocaleString()} / ${count.toLocaleString()} churned)\\nClick to drill down into Explorer`;

        cellDiv.innerHTML = `
          <span class="heatmap-rate" style="color: ${textCol}">${rate}%</span>
          <span class="heatmap-count">${count.toLocaleString()} accts</span>
        `;

        cellDiv.addEventListener("click", () => {
          drilldownSegment(contract, internet);
        });
      } else {
        cellDiv.innerHTML = `<span class="heatmap-count">N/A</span>`;
      }

      container.appendChild(cellDiv);
    });
  });
}

/* --- B. CUSTOMER SCATTER PLOT (Tenure vs Monthly Charges) --- */
function renderScatterChart(points) {
  const ctx = document.getElementById("scatterTenureChargesChart");
  if (!ctx || !points) return;

  if (chartInstances["scatterTenureChargesChart"]) {
    chartInstances["scatterTenureChargesChart"].destroy();
  }

  const retainedPoints = [];
  const churnedPoints = [];

  points.forEach(pt => {
    const item = {
      x: pt.tenure,
      y: pt.monthly_charges,
      customerID: pt.customerID,
      contract: pt.contract,
      predicted_risk: pt.predicted_risk
    };
    if (pt.churn === "Yes") {
      churnedPoints.push(item);
    } else {
      retainedPoints.push(item);
    }
  });

  chartInstances["scatterTenureChargesChart"] = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Retained Subscribers",
          data: retainedPoints,
          backgroundColor: "rgba(16, 185, 129, 0.6)",
          borderColor: "rgba(16, 185, 129, 0.9)",
          pointRadius: 3.5,
          hoverRadius: 6
        },
        {
          label: "Churned Subscribers",
          data: churnedPoints,
          backgroundColor: "rgba(239, 68, 68, 0.7)",
          borderColor: "rgba(239, 68, 68, 1.0)",
          pointRadius: 3.5,
          hoverRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: "Tenure (Months)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          min: 0,
          max: 75
        },
        y: {
          title: { display: true, text: "Monthly Charges ($)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `$${v}` },
          min: 15,
          max: 125
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => {
              const raw = c.raw;
              return [
                `ID: ${raw.customerID} (${raw.contract})`,
                `Tenure: ${raw.x} mo | Monthly: $${raw.y.toFixed(2)}`,
                `Predicted Churn Risk: ${raw.predicted_risk}%`
              ];
            }
          }
        }
      }
    }
  });
}

/* --- C. DISTRIBUTION HISTOGRAMS --- */
function renderHistograms(tenureHist, chargesHist) {
  // 1. Tenure Histogram
  const ctxT = document.getElementById("tenureHistogramChart");
  if (ctxT && tenureHist) {
    if (chartInstances["tenureHistogramChart"]) {
      chartInstances["tenureHistogramChart"].destroy();
    }
    chartInstances["tenureHistogramChart"] = new Chart(ctxT, {
      type: "bar",
      data: {
        labels: tenureHist.bins,
        datasets: [
          {
            label: "Retained",
            data: tenureHist.retained,
            backgroundColor: "#10b981",
            borderRadius: 4
          },
          {
            label: "Churned",
            data: tenureHist.churned,
            backgroundColor: "#ef4444",
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true, grid: { color: "rgba(51, 65, 85, 0.3)" } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              afterLabel: c => {
                const total = tenureHist.totals[c.dataIndex];
                const churnRate = tenureHist.churn_rates[c.dataIndex];
                return `Bin Total: ${total} accounts | Churn Rate: ${churnRate}%`;
              }
            }
          }
        }
      }
    });
  }

  // 2. Charges Histogram
  const ctxC = document.getElementById("chargesHistogramChart");
  if (ctxC && chargesHist) {
    if (chartInstances["chargesHistogramChart"]) {
      chartInstances["chargesHistogramChart"].destroy();
    }
    chartInstances["chargesHistogramChart"] = new Chart(ctxC, {
      type: "bar",
      data: {
        labels: chargesHist.bins,
        datasets: [
          {
            label: "Retained",
            data: chargesHist.retained,
            backgroundColor: "#10b981",
            borderRadius: 4
          },
          {
            label: "Churned",
            data: chargesHist.churned,
            backgroundColor: "#ef4444",
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true, grid: { color: "rgba(51, 65, 85, 0.3)" } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              afterLabel: c => {
                const total = chargesHist.totals[c.dataIndex];
                const churnRate = chargesHist.churn_rates[c.dataIndex];
                return `Bin Total: ${total} accounts | Churn Rate: ${churnRate}%`;
              }
            }
          }
        }
      }
    });
  }
}

/* --- D. 100% STACKED PROPORTION CHART --- */
function renderStackedProportion(stackedData, dim) {
  const ctx = document.getElementById("stackedProportionChart");
  if (!ctx || !stackedData || !stackedData[dim]) return;

  if (chartInstances["stackedProportionChart"]) {
    chartInstances["stackedProportionChart"].destroy();
  }

  const dimData = stackedData[dim];

  chartInstances["stackedProportionChart"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: dimData.labels,
      datasets: [
        {
          label: "Retained %",
          data: dimData.retained_pct,
          backgroundColor: "#10b981",
          borderRadius: 4
        },
        {
          label: "Churned %",
          data: dimData.churn_pct,
          backgroundColor: "#ef4444",
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: {
          stacked: true,
          beginAtZero: true,
          max: 100,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${c.parsed.y}% (${dimData.churn_counts ? dimData.churn_counts[c.dataIndex] : ""} accounts)`
          }
        }
      }
    }
  });
}

window.switchStackedDim = function(dim) {
  currentStackedDim = dim;
  document.querySelectorAll(".btn-metric-pill").forEach(b => b.classList.remove("active"));
  const activeBtn = document.getElementById(`btn-stacked-${dim}`);
  if (activeBtn) activeBtn.classList.add("active");
  if (cachedAdvancedData && cachedAdvancedData.stacked_100) {
    renderStackedProportion(cachedAdvancedData.stacked_100, dim);
  }
};

/* --- E. SEGMENT BUBBLE CHART --- */
function renderSegmentBubbleChart(bubbles) {
  const ctx = document.getElementById("segmentBubbleChart");
  if (!ctx || !bubbles) return;

  if (chartInstances["segmentBubbleChart"]) {
    chartInstances["segmentBubbleChart"].destroy();
  }

  const bubbleData = bubbles.map(b => ({
    x: b.avg_charges,
    y: b.churn_rate,
    r: b.radius,
    name: b.name,
    contract: b.contract,
    internet: b.internet,
    count: b.count,
    high_risk: b.high_risk_count
  }));

  chartInstances["segmentBubbleChart"] = new Chart(ctx, {
    type: "bubble",
    data: {
      datasets: [{
        label: "Customer Segments",
        data: bubbleData,
        backgroundColor: bubbleData.map(b => {
          if (b.y >= 45) return "rgba(239, 68, 68, 0.75)";
          if (b.y >= 25) return "rgba(245, 158, 11, 0.7)";
          if (b.y >= 10) return "rgba(56, 189, 248, 0.7)";
          return "rgba(16, 185, 129, 0.7)";
        }),
        borderColor: "rgba(255, 255, 255, 0.3)",
        borderWidth: 1.5,
        hoverBorderWidth: 2.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      onClick: (e, elements) => {
        if (elements && elements.length > 0) {
          const idx = elements[0].index;
          const seg = bubbleData[idx];
          drilldownSegment(seg.contract, seg.internet);
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Average Monthly Charges ($)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `$${v}` },
          min: 15,
          max: 100
        },
        y: {
          title: { display: true, text: "Historical Churn Rate (%)", color: "#94a3b8" },
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` },
          min: 0,
          max: 60
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => {
              const d = c.raw;
              return [
                `${d.name}`,
                `Subscribers: ${d.count.toLocaleString()} (Radius scaled)`,
                `Historical Churn: ${d.y}%`,
                `Avg Monthly: $${d.x.toFixed(2)}`,
                `High-Risk Base: ${d.high_risk.toLocaleString()} accounts`,
                `Click bubble to drill down into Customer Explorer`
              ];
            }
          }
        }
      }
    }
  });
}

/* --- F. SEGMENT COMPARISON TOOL --- */
function initSegmentComparison(segments) {
  const selA = document.getElementById("seg-compare-select-a");
  const selB = document.getElementById("seg-compare-select-b");
  if (!selA || !selB || !segments) return;

  selA.innerHTML = "";
  selB.innerHTML = "";

  segments.forEach((seg, i) => {
    const optA = document.createElement("option");
    optA.value = i;
    optA.textContent = `${seg.name} (${seg.count.toLocaleString()} accounts)`;
    selA.appendChild(optA);

    const optB = document.createElement("option");
    optB.value = i;
    optB.textContent = `${seg.name} (${seg.count.toLocaleString()} accounts)`;
    selB.appendChild(optB);
  });

  // Defaults: Segment 0 (Month-to-month + Fiber optic) vs Segment 8 (Two year + No internet)
  selA.value = "0";
  selB.value = segments.length > 8 ? "8" : "1";

  const updateComparison = () => {
    const segA = segments[parseInt(selA.value, 10)];
    const segB = segments[parseInt(selB.value, 10)];
    renderComparisonCards(segA, segB);
  };

  selA.addEventListener("change", updateComparison);
  selB.addEventListener("change", updateComparison);
  updateComparison();
}

function renderComparisonCards(a, b) {
  const grid = document.getElementById("segment-compare-grid");
  if (!grid || !a || !b) return;

  const countDelta = b.count - a.count;
  const churnDelta = b.churn_rate - a.churn_rate;
  const tenureDelta = b.avg_tenure - a.avg_tenure;
  const chargesDelta = b.avg_charges - a.avg_charges;
  const highRiskDelta = b.high_risk_count - a.high_risk_count;
  const riskProbDelta = b.avg_predicted_risk - a.avg_predicted_risk;

  grid.innerHTML = `
    <div class="compare-card">
      <span class="compare-card-title">Customer Count</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">${a.count.toLocaleString()}</span>
        <span class="compare-val-b">${b.count.toLocaleString()}</span>
      </div>
      <span class="compare-delta-pill ${countDelta >= 0 ? 'delta-success' : 'delta-neutral'}">
        ${countDelta >= 0 ? '+' : ''}${countDelta.toLocaleString()} delta
      </span>
    </div>

    <div class="compare-card">
      <span class="compare-card-title">Historical Churn Rate</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">${a.churn_rate}%</span>
        <span class="compare-val-b">${b.churn_rate}%</span>
      </div>
      <span class="compare-delta-pill ${churnDelta <= 0 ? 'delta-success' : 'delta-danger'}">
        ${churnDelta >= 0 ? '+' : ''}${churnDelta.toFixed(2)}% vs Baseline
      </span>
    </div>

    <div class="compare-card">
      <span class="compare-card-title">Average Tenure</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">${a.avg_tenure} mo</span>
        <span class="compare-val-b">${b.avg_tenure} mo</span>
      </div>
      <span class="compare-delta-pill ${tenureDelta >= 0 ? 'delta-success' : 'delta-danger'}">
        ${tenureDelta >= 0 ? '+' : ''}${tenureDelta.toFixed(1)} mo longevity
      </span>
    </div>

    <div class="compare-card">
      <span class="compare-card-title">Average Monthly ($)</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">$${a.avg_charges.toFixed(2)}</span>
        <span class="compare-val-b">$${b.avg_charges.toFixed(2)}</span>
      </div>
      <span class="compare-delta-pill delta-neutral">
        ${chargesDelta >= 0 ? '+' : ''}$${chargesDelta.toFixed(2)} / subscriber
      </span>
    </div>

    <div class="compare-card">
      <span class="compare-card-title">High-Risk Subscribers (≥60%)</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">${a.high_risk_count.toLocaleString()}</span>
        <span class="compare-val-b">${b.high_risk_count.toLocaleString()}</span>
      </div>
      <span class="compare-delta-pill ${highRiskDelta <= 0 ? 'delta-success' : 'delta-danger'}">
        ${highRiskDelta >= 0 ? '+' : ''}${highRiskDelta.toLocaleString()} accounts
      </span>
    </div>

    <div class="compare-card">
      <span class="compare-card-title">Avg Predicted Risk</span>
      <div class="compare-metric-row">
        <span class="compare-val-a">${a.avg_predicted_risk}%</span>
        <span class="compare-val-b">${b.avg_predicted_risk}%</span>
      </div>
      <span class="compare-delta-pill ${riskProbDelta <= 0 ? 'delta-success' : 'delta-danger'}">
        ${riskProbDelta >= 0 ? '+' : ''}${riskProbDelta.toFixed(2)}% risk spread
      </span>
    </div>
  `;
}

/* --- G. REVENUE-RISK PARETO CHART --- */
function renderParetoChart(paretoData) {
  const ctx = document.getElementById("revenueParetoChart");
  if (!ctx || !paretoData) return;

  if (chartInstances["revenueParetoChart"]) {
    chartInstances["revenueParetoChart"].destroy();
  }

  chartInstances["revenueParetoChart"] = new Chart(ctx, {
    data: {
      labels: paretoData.labels,
      datasets: [
        {
          type: "bar",
          label: "High-Risk MRR ($)",
          data: paretoData.charges,
          backgroundColor: "#f59e0b",
          yAxisID: "y",
          borderRadius: 4,
          maxBarThickness: 38
        },
        {
          type: "line",
          label: "Cumulative Exposure (%)",
          data: paretoData.cumulative_percentages,
          borderColor: "#38bdf8",
          backgroundColor: "#38bdf8",
          pointRadius: 5,
          pointHoverRadius: 7,
          yAxisID: "y1",
          tension: 0.1
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
          beginAtZero: true,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `$${(v / 1000).toFixed(0)}k` },
          title: { display: true, text: "High-Risk Monthly Revenue ($)", color: "#94a3b8" }
        },
        y1: {
          type: "linear",
          position: "right",
          beginAtZero: true,
          max: 105,
          grid: { drawOnChartArea: false },
          ticks: { callback: v => `${v}%` },
          title: { display: true, text: "Cumulative %", color: "#94a3b8" }
        },
        x: { grid: { display: false } }
      },
      plugins: {
        legend: { position: "top", labels: { boxWidth: 12, padding: 10 } },
        tooltip: {
          callbacks: {
            label: c => {
              if (c.dataset.type === "bar") {
                return `Monthly Exposure: $${c.parsed.y.toLocaleString()}`;
              }
              return `Cumulative Exposure: ${c.parsed.y}% of high-risk MRR`;
            }
          }
        }
      }
    }
  });
}

/* --- H. OPERATIONAL RISK THRESHOLD SIMULATOR --- */
function initThresholdSimulator() {
  const slider = document.getElementById("sim-threshold-slider");
  const valBadge = document.getElementById("sim-threshold-val");
  const countEl = document.getElementById("sim-flagged-count");
  const pctEl = document.getElementById("sim-flagged-pct");
  const mrrEl = document.getElementById("sim-flagged-mrr");
  const mrrPctEl = document.getElementById("sim-flagged-mrr-pct");
  const annualEl = document.getElementById("sim-annual-exposure");
  const deltaCountEl = document.getElementById("sim-delta-count");
  const deltaMrrEl = document.getElementById("sim-delta-mrr");

  if (!slider) return;

  let debounceTimer = null;

  slider.addEventListener("input", e => {
    const tVal = parseFloat(e.target.value);
    if (valBadge) valBadge.textContent = `${tVal.toFixed(2)} (${Math.round(tVal * 100)}%)`;

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/threshold-sim?threshold=${tVal}`);
        const sim = await res.json();
        if (sim.error) return;

        if (countEl) countEl.textContent = sim.flagged_customers.toLocaleString();
        if (pctEl) pctEl.textContent = `${sim.flagged_customer_share_pct}% of portfolio (7,043)`;
        if (mrrEl) mrrEl.textContent = `$${sim.flagged_monthly_charges.toLocaleString()}`;
        if (mrrPctEl) mrrPctEl.textContent = `${sim.flagged_mrr_share_pct}% of monthly MRR`;
        if (annualEl) annualEl.textContent = `$${(sim.annualized_flagged_charges / 1000000).toFixed(2)}M / yr`;

        if (deltaCountEl) {
          const sign = sim.delta_customers >= 0 ? "+" : "";
          deltaCountEl.textContent = `${sign}${sim.delta_customers.toLocaleString()} accounts`;
          deltaCountEl.className = sim.delta_customers > 0 ? "sim-metric-num text-danger" : (sim.delta_customers < 0 ? "sim-metric-num text-success" : "sim-metric-num text-teal");
        }

        if (deltaMrrEl) {
          const sign = sim.delta_charges >= 0 ? "+" : "";
          deltaMrrEl.textContent = `${sign}$${sim.delta_charges.toLocaleString()} / mo vs 0.60 baseline`;
        }
      } catch (err) {
        console.error("Threshold sim error:", err);
      }
    }, 120);
  });
}

/* --- I. PREDICTED-RISK DISTRIBUTION HISTOGRAM --- */
function renderPredictedRiskHist(histData) {
  const ctx = document.getElementById("predictedRiskHistChart");
  if (!ctx || !histData) return;

  if (chartInstances["predictedRiskHistChart"]) {
    chartInstances["predictedRiskHistChart"].destroy();
  }

  // Color bins by risk category
  const bgColors = [
    "#10b981", "#10b981", "#10b981", // 0.0-0.3 (Low Risk)
    "#f59e0b", "#f59e0b", "#f59e0b", // 0.3-0.6 (Medium Risk)
    "#ef4444", "#ef4444",            // 0.6-0.8 (High Risk)
    "#8b5cf6", "#a855f7"             // 0.8-1.0 (Critical Triage)
  ];

  chartInstances["predictedRiskHistChart"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: histData.bins,
      datasets: [{
        label: "Customers",
        data: histData.counts,
        backgroundColor: bgColors,
        borderRadius: 4,
        maxBarThickness: 42
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: "Predicted Churn Probability Interval", color: "#94a3b8" },
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          title: { display: true, text: "Customer Frequency", color: "#94a3b8" }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => {
              const count = c.parsed.y;
              const pct = histData.percentages[c.dataIndex];
              const tier = histData.tier_labels[c.dataIndex];
              return [
                `Accounts: ${count.toLocaleString()} (${pct}% of base)`,
                `Risk Tier: ${tier}`
              ];
            }
          }
        }
      }
    }
  });
}

/* --- J. BATCH CUSTOMER PREDICTION (CSV Engine) --- */
function initBatchPrediction() {
  const dropzone = document.getElementById("batch-dropzone");
  const fileInput = document.getElementById("batch-file-input");
  const errorBox = document.getElementById("batch-error-box");
  const errorMsg = document.getElementById("batch-error-msg");
  const spinner = document.getElementById("batch-spinner");
  const resultsContainer = document.getElementById("batch-results-container");

  if (!dropzone || !fileInput) return;

  const handleFile = async (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".csv")) {
      showError("Invalid file type. Please upload a comma-separated CSV file (.csv).");
      return;
    }

    // Reset UI
    hideError();
    if (resultsContainer) resultsContainer.classList.add("hidden");
    if (spinner) spinner.classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/predict-batch", {
        method: "POST",
        body: formData
      });
      const data = await res.json();

      if (spinner) spinner.classList.add("hidden");

      if (data.status === "error" || data.error) {
        showError(data.message || data.error || "Batch prediction encountered an error.");
        return;
      }

      // Populate KPI Summary
      const elTotal = document.getElementById("batch-kpi-total");
      const elChurners = document.getElementById("batch-kpi-churners");
      const elRate = document.getElementById("batch-kpi-rate");
      const elHighRisk = document.getElementById("batch-kpi-high-risk");

      if (elTotal) elTotal.textContent = (data.total_scored || 0).toLocaleString();
      if (elChurners) elChurners.textContent = (data.predicted_churners || 0).toLocaleString();
      if (elRate) elRate.textContent = `${data.predicted_churn_rate_pct || 0}%`;
      if (elHighRisk) elHighRisk.textContent = (data.high_risk_count || 0).toLocaleString();

      // Populate Table
      const tbody = document.getElementById("batch-results-tbody");
      if (tbody && data.preview_rows) {
        tbody.innerHTML = "";
        data.preview_rows.forEach((row, idx) => {
          const tr = document.createElement("tr");

          let tierBadge = `<span class="badge-risk-low">${row.Risk_Tier}</span>`;
          if (row.Risk_Tier === "High Risk" || row.Risk_Tier === "Critical Triage") {
            tierBadge = `<span class="badge-risk-high">${row.Risk_Tier}</span>`;
          } else if (row.Risk_Tier === "Medium Risk") {
            tierBadge = `<span class="badge-risk-medium">${row.Risk_Tier}</span>`;
          }

          const probColor = row.Predicted_Probability >= 60 ? "#f87171" : (row.Predicted_Probability >= 30 ? "#fbbf24" : "#34d399");

          tr.innerHTML = `
            <td>${idx + 1}</td>
            <td><strong>${row.CustomerID}</strong></td>
            <td>${row.Contract}</td>
            <td>${row.InternetService}</td>
            <td>$${parseFloat(row.MonthlyCharges).toFixed(2)}</td>
            <td><strong style="color: ${probColor}">${row.Predicted_Probability}%</strong></td>
            <td>${row.Predicted_Class === "Yes" ? '<span class="status-pill pill-danger">Churn</span>' : '<span class="status-pill pill-success">Retain</span>'}</td>
            <td>${tierBadge}</td>
            <td><span class="prescribed-action-sm">${row.Prescribed_Action}</span></td>
          `;
          tbody.appendChild(tr);
        });
      }

      if (resultsContainer) resultsContainer.classList.remove("hidden");
    } catch (err) {
      if (spinner) spinner.classList.add("hidden");
      showError(`Network/Server error during batch scoring: ${err.message}`);
    }
  };

  const showError = msg => {
    if (errorMsg) errorMsg.textContent = msg;
    if (errorBox) errorBox.classList.remove("hidden");
  };

  const hideError = () => {
    if (errorBox) errorBox.classList.add("hidden");
  };

  // Drag & drop events
  dropzone.addEventListener("dragover", e => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", e => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", e => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });
}
"""

if "/* 7. ADVANCED VISUALIZATIONS & FEATURES IMPLEMENTATION */" not in js:
    js = js + "\n" + advanced_js
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("Added advanced JS functions to app.js")
else:
    print("Advanced JS functions already present.")
