/* ==============================================================================
   8. MAJOR PRODUCT REDESIGN: ENTERPRISE ANALYTICAL LABS IMPLEMENTATION
   ============================================================================== */

/**
 * Workspace 1: Executive Portfolio Health Dial Gauge
 */
function loadPortfolioHealthGauge() {
  const canvas = document.getElementById("portfolioHealthGaugeChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (chartInstances.portfolioHealthGauge) chartInstances.portfolioHealthGauge.destroy();

  chartInstances.portfolioHealthGauge = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Safe Zone (<20%)", "Industry Warning (20–25%)", "Elevated Danger (25–35%)", "Remainder"],
      datasets: [{
        data: [20, 5, 10, 65],
        backgroundColor: [
          "rgba(16, 185, 129, 0.85)",
          "rgba(245, 158, 11, 0.85)",
          "rgba(244, 63, 94, 0.85)",
          "rgba(255, 255, 255, 0.04)"
        ],
        borderWidth: 0,
        circumference: 180,
        rotation: -90
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `${c.label}: ${c.raw}%`
          }
        }
      },
      cutout: "75%"
    }
  });

  const numEl = document.getElementById("gauge-churn-num");
  if (numEl) numEl.textContent = "26.54%";
}

/**
 * Workspace 1: Retention Pipeline Progression Funnel
 */
function loadRetentionFunnel() {
  const container = document.getElementById("retention-funnel-container");
  if (!container) return;

  const stages = [
    { title: "1. Verified Active Base", count: 7043, pct: 100.0, color: "#38bdf8", sub: "Total customer portfolio" },
    { title: "2. Retained Core Base", count: 5174, pct: 73.46, color: "#10b981", sub: "Actual retained subscribers" },
    { title: "3. Low-Risk Steady Base", count: 3760, pct: 53.39, color: "#34d399", sub: "Prob < 30% (Stable ARR)" },
    { title: "4. Medium-Risk Watchlist", count: 1414, pct: 20.08, color: "#f59e0b", sub: "30% ≤ Prob < 60%" },
    { title: "5. High-Risk Action Pool", count: 1039, pct: 14.75, color: "#fb7185", sub: "Prob ≥ 60% ($85.5K MRR)" },
    { title: "6. Critical Immediate Outreach", count: 49, pct: 0.70, color: "#e11d48", sub: "Prob ≥ 80% ($4.1K MRR)" }
  ];

  container.innerHTML = stages.map(s => `
    <div class="funnel-stage-card">
      <div class="funnel-stage-header">
        <span class="funnel-stage-title">${s.title}</span>
        <span class="funnel-stage-stats" style="color: ${s.color};">${s.count.toLocaleString()} accounts (${s.pct.toFixed(1)}%)</span>
      </div>
      <div class="funnel-track">
        <div class="funnel-fill" style="width: ${Math.max(4, s.pct)}%; background: ${s.color};"></div>
      </div>
    </div>
  `).join('');
}

/**
 * Workspace 1: 2D Service x Contract Churn Rate Matrix Heatmap
 */
async function loadServiceContractMatrix() {
  const container = document.getElementById("service-contract-matrix-container");
  if (!container) return;

  try {
    const res = await fetch("/api/behavioral-intelligence");
    const data = await res.json();
    const rows = data.service_contract_matrix || [];

    // Group by Service
    const services = ["Fiber optic", "DSL", "No"];
    const contracts = ["Month-to-month", "One year", "Two year"];

    let html = `
      <table class="matrix-2d-grid">
        <thead>
          <tr>
            <th class="matrix-2d-th text-left">Internet Infrastructure</th>
            ${contracts.map(c => `<th class="matrix-2d-th">${c}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
    `;

    services.forEach(svc => {
      const svcLabel = svc === "No" ? "No Internet" : svc;
      html += `<tr><td class="matrix-2d-rowhead">${svcLabel}</td>`;
      contracts.forEach(contract => {
        const item = rows.find(r => r.InternetService === svc && r.Contract === contract) || {
          churn_rate: 0, churns: 0, total: 0, avg_mrr: 0
        };
        // Compute color by churn rate
        let bg = "rgba(16, 185, 129, 0.15)";
        let textCol = "#34d399";
        let borderCol = "rgba(16, 185, 129, 0.3)";
        if (item.churn_rate > 40) {
          bg = "rgba(244, 63, 94, 0.35)";
          textCol = "#fb7185";
          borderCol = "rgba(244, 63, 94, 0.6)";
        } else if (item.churn_rate > 20) {
          bg = "rgba(245, 158, 11, 0.25)";
          textCol = "#fbbf24";
          borderCol = "rgba(245, 158, 11, 0.5)";
        } else if (item.churn_rate > 8) {
          bg = "rgba(56, 189, 248, 0.18)";
          textCol = "#38bdf8";
          borderCol = "rgba(56, 189, 248, 0.35)";
        }

        html += `
          <td class="matrix-2d-cell" style="background: ${bg}; border-color: ${borderCol};"
              onclick="drillDownToExplorer({ contract: '${contract}', internet: '${svc}' })"
              title="Click to view ${item.total} subscribers in Customer Explorer">
            <div class="cell-rate-big" style="color: ${textCol};">${item.churn_rate}%</div>
            <div class="cell-sub-metrics">${item.churns} / ${item.total} Churned</div>
            <div class="cell-sub-metrics" style="color: #94a3b8;">Avg $${item.avg_mrr.toFixed(2)}/mo</div>
          </td>
        `;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
  } catch (err) {
    console.error("Error loading service contract matrix:", err);
  }
}

/**
 * Workspace 2: Multivariate Behavioral Correlation Matrix Heatmap
 */
async function loadCorrelationMatrix() {
  const container = document.getElementById("correlation-matrix-container");
  if (!container) return;

  try {
    const res = await fetch("/api/behavioral-intelligence");
    const data = await res.json();
    const corr = data.correlation;
    if (!corr || !corr.variables) return;

    const vars = corr.variables;
    const matrix = corr.matrix;

    let html = `
      <table class="correlation-table">
        <thead>
          <tr>
            <th class="corr-head text-left">Feature Variable</th>
            ${vars.map(v => `<th class="corr-head">${v}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
    `;

    vars.forEach((v1, i) => {
      html += `<tr><td class="matrix-2d-rowhead">${v1}</td>`;
      vars.forEach((v2, j) => {
        const val = matrix[i][j];
        let bg = "rgba(255, 255, 255, 0.02)";
        let col = "#e2e8f0";
        if (i === j) {
          bg = "rgba(255, 255, 255, 0.08)";
          col = "#ffffff";
        } else if (val > 0) {
          const alpha = Math.min(0.7, val * 0.8 + 0.05);
          bg = `rgba(244, 63, 94, ${alpha})`;
          col = val > 0.4 ? "#ffffff" : "#fb7185";
        } else if (val < 0) {
          const alpha = Math.min(0.7, Math.abs(val) * 0.8 + 0.05);
          bg = `rgba(56, 189, 248, ${alpha})`;
          col = val < -0.3 ? "#ffffff" : "#7dd3fc";
        }

        html += `
          <td class="corr-cell" style="background: ${bg}; color: ${col};"
              title="${v1} vs ${v2}: Pearson r = ${val}">
            ${val > 0 ? "+" : ""}${val.toFixed(2)}
          </td>
        `;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
  } catch (err) {
    console.error("Error loading correlation matrix:", err);
  }
}

/**
 * Workspace 4: Financial Exposure Hierarchy Treemap
 */
async function loadFinancialTreemap() {
  const container = document.getElementById("financial-treemap-container");
  if (!container) return;

  try {
    const res = await fetch("/api/behavioral-intelligence");
    const data = await res.json();
    const tiers = data.financial_hierarchy || [];

    const colors = {
      "Low Risk": { border: "#10b981", bg: "rgba(16, 185, 129, 0.08)", text: "#34d399" },
      "Medium Risk": { border: "#f59e0b", bg: "rgba(245, 158, 11, 0.08)", text: "#fbbf24" },
      "High Risk": { border: "#f43f5e", bg: "rgba(244, 63, 94, 0.12)", text: "#fb7185" }
    };

    container.innerHTML = tiers.map(t => {
      const c = colors[t.name] || colors["Low Risk"];
      return `
        <div class="treemap-tile" style="border-color: ${c.border}; background: ${c.bg};">
          <div>
            <div class="treemap-tile-header">
              <span style="color: ${c.text};">${t.name}</span>
              <span style="color: #94a3b8; font-family: var(--font-mono);">${t.total_customers.toLocaleString()} accounts</span>
            </div>
            <div class="treemap-mrr-big" style="color: #ffffff;">$${t.total_mrr.toLocaleString()}</div>
            <span style="font-size: 0.70rem; color: #94a3b8;">Monthly Recurring Revenue</span>
          </div>
          <div class="treemap-sub-breakdown">
            ${(t.children || []).map(child => `
              <div class="treemap-sub-row">
                <span>${child.name}</span>
                <span style="font-family: var(--font-mono); font-weight: 600;">$${child.mrr.toLocaleString()} (${child.churn_rate}%)</span>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error("Error loading financial treemap:", err);
  }
}

/**
 * Workspace 3: Macro Telecom Market Intelligence (TRAI & FCC)
 */
async function loadExternalMarketIntelligence() {
  try {
    const res = await fetch("/api/external-market-intelligence");
    const data = await res.json();

    // 1. TRAI Broadband Market Share (Polar Area)
    const traiShareCanvas = document.getElementById("traiMarketShareChart");
    if (traiShareCanvas && data.trai && data.trai.broadband_market_share) {
      const ctx = traiShareCanvas.getContext("2d");
      if (chartInstances.traiMarketShare) chartInstances.traiMarketShare.destroy();

      const items = data.trai.broadband_market_share;
      chartInstances.traiMarketShare = new Chart(ctx, {
        type: "polarArea",
        data: {
          labels: items.map(i => i.operator),
          datasets: [{
            data: items.map(i => i.subscribers_million),
            backgroundColor: [
              "rgba(56, 189, 248, 0.75)",
              "rgba(192, 132, 252, 0.75)",
              "rgba(251, 113, 133, 0.75)",
              "rgba(245, 158, 11, 0.75)",
              "rgba(148, 163, 184, 0.75)"
            ],
            borderWidth: 1,
            borderColor: "rgba(255, 255, 255, 0.1)"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              grid: { color: "rgba(51, 65, 85, 0.3)" },
              ticks: { display: false }
            }
          },
          plugins: {
            legend: { position: "right", labels: { boxWidth: 10, padding: 8 } },
            tooltip: {
              callbacks: {
                label: c => `${c.label}: ${c.raw}M subscribers (${items[c.dataIndex].share_pct}%)`
              }
            }
          }
        }
      });
    }

    // 2. TRAI MNP Circle Churn Intensity Bar Chart
    const mnpCanvas = document.getElementById("traiMnpCircleChart");
    if (mnpCanvas && data.trai && data.trai.top_mnp_circles) {
      const ctx = mnpCanvas.getContext("2d");
      if (chartInstances.traiMnp) chartInstances.traiMnp.destroy();

      const circles = data.trai.top_mnp_circles;
      chartInstances.traiMnp = new Chart(ctx, {
        type: "bar",
        data: {
          labels: circles.map(c => c.circle),
          datasets: [{
            label: "Monthly Porting Requests (Millions)",
            data: circles.map(c => (c.monthly_porting_requests / 1e6).toFixed(2)),
            backgroundColor: "rgba(251, 113, 133, 0.8)",
            borderRadius: 4
          }]
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true,
              grid: { color: "rgba(51, 65, 85, 0.25)" },
              ticks: { callback: v => `${v}M` },
              title: { display: true, text: "Porting Volume (Millions / Month)", color: "#94a3b8" }
            },
            y: {
              grid: { display: false }
            }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: c => `${c.raw} Million requests (${circles[c.dataIndex].zone})`
              }
            }
          }
        }
      });
    }

    // 3. FCC Consumer Complaints Delivery Method vs Issues (Stacked Bar)
    const fccCanvas = document.getElementById("fccMethodIssueChart");
    if (fccCanvas && data.fcc && data.fcc.method_issue_matrix) {
      const ctx = fccCanvas.getContext("2d");
      if (chartInstances.fccComplaints) chartInstances.fccComplaints.destroy();

      const matrix = data.fcc.method_issue_matrix;
      const methods = Object.keys(matrix);
      const issues = ["Unwanted Calls", "Billing", "Availability (including rural call completion)"];

      chartInstances.fccComplaints = new Chart(ctx, {
        type: "bar",
        data: {
          labels: methods,
          datasets: [
            {
              label: "Unwanted Calls",
              data: methods.map(m => matrix[m]["Unwanted Calls"] || 0),
              backgroundColor: "rgba(244, 63, 94, 0.85)"
            },
            {
              label: "Billing Disputes",
              data: methods.map(m => matrix[m]["Billing"] || 0),
              backgroundColor: "rgba(245, 158, 11, 0.85)"
            },
            {
              label: "Availability / Outages",
              data: methods.map(m => matrix[m]["Availability (including rural call completion)"] || matrix[m]["Availability"] || 0),
              backgroundColor: "rgba(56, 189, 248, 0.85)"
            }
          ]
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              grid: { color: "rgba(51, 65, 85, 0.25)" },
              title: { display: true, text: "Complaint Tickets (n = 5,000 SODA Sample)", color: "#94a3b8" }
            },
            y: {
              stacked: true,
              grid: { display: false }
            }
          },
          plugins: {
            legend: { position: "top", labels: { boxWidth: 10, padding: 8 } }
          }
        }
      });
    }
  } catch (err) {
    console.error("Error loading external market intelligence:", err);
  }
}

/**
 * Workspace 5: Independent UCI Iranian Telecom Churn Benchmark Experiment
 */
async function loadUciBenchmark() {
  const canvas = document.getElementById("uciBenchmarkChart");
  if (!canvas) return;

  try {
    const res = await fetch("/api/uci-benchmark");
    const data = await res.json();
    if (!data.models) return;

    const ctx = canvas.getContext("2d");
    if (chartInstances.uciBenchmark) chartInstances.uciBenchmark.destroy();

    const metrics = ["Accuracy", "ROC-AUC", "Precision", "Recall", "F1-Score"];
    const lr = data.models["Logistic Regression"];
    const rf = data.models["Random Forest"];

    chartInstances.uciBenchmark = new Chart(ctx, {
      type: "bar",
      data: {
        labels: metrics,
        datasets: [
          {
            label: "Logistic Regression (Linear Benchmark)",
            data: [
              (lr.accuracy * 100).toFixed(1),
              (lr.roc_auc * 100).toFixed(1),
              (lr.precision * 100).toFixed(1),
              (lr.recall * 100).toFixed(1),
              (lr.f1 * 100).toFixed(1)
            ],
            backgroundColor: "rgba(56, 189, 248, 0.85)",
            borderRadius: 4
          },
          {
            label: "Random Forest (Nonlinear Telemetry)",
            data: [
              (rf.accuracy * 100).toFixed(1),
              (rf.roc_auc * 100).toFixed(1),
              (rf.precision * 100).toFixed(1),
              (rf.recall * 100).toFixed(1),
              (rf.f1 * 100).toFixed(1)
            ],
            backgroundColor: "rgba(192, 132, 252, 0.85)",
            borderRadius: 4
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
            title: { display: true, text: "Evaluation Metric (%)", color: "#94a3b8" }
          },
          x: {
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: "top", labels: { boxWidth: 10, padding: 10 } },
          tooltip: {
            callbacks: {
              label: c => `${c.dataset.label}: ${c.raw}%`
            }
          }
        }
      }
    });
  } catch (err) {
    console.error("Error loading UCI benchmark:", err);
  }
}

/**
 * Workspace 6: Multi-Source Data Provenance & Verification Registry
 */
async function loadProvenanceRegistry() {
  const container = document.getElementById("provenance-cards-container");
  if (!container) return;

  try {
    const res = await fetch("/api/provenance");
    const data = await res.json();
    const datasets = data.datasets || [];

    container.innerHTML = datasets.map(d => `
      <div class="provenance-card">
        <div class="prov-card-header">
          <span class="prov-card-title">${d.title}</span>
          <span class="status-pill pill-success">${d.quality_status.includes("Cleaned") || d.quality_status.includes("Verified") ? "Verified" : "Audited"}</span>
        </div>
        <div class="prov-meta-row">
          <span>Publisher:</span>
          <span class="prov-meta-val">${d.publisher}</span>
        </div>
        <div class="prov-meta-row">
          <span>License:</span>
          <span class="prov-meta-val">${d.license}</span>
        </div>
        <div class="prov-meta-row">
          <span>Records & Features:</span>
          <span class="prov-meta-val">${typeof d.records === "number" ? d.records.toLocaleString() : d.records} rows • ${d.features}</span>
        </div>
        <div class="prov-meta-row">
          <span>Coverage Period:</span>
          <span class="prov-meta-val">${d.coverage}</span>
        </div>
        <p class="prov-desc">${d.role}</p>
        <a href="${d.source_url}" target="_blank" rel="noopener noreferrer" class="prov-link-badge">
          <span>Official Public Source URL &rarr;</span>
        </a>
      </div>
    `).join('');
  } catch (err) {
    console.error("Error loading provenance registry:", err);
  }
}
