/**
 * Customer Churn Prediction & Retention Analytics (CCPRA)
 * Enterprise Dashboard Interactive Logic
 */

document.addEventListener("DOMContentLoaded", () => {
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
});

/* ==============================================================================
   GLOBAL STATE & CHART INSTANCES
   ============================================================================== */
let chartInstances = {};
let currentAnalyticsMetric = "rate"; // 'rate' | 'count' | 'stacked'

/* ==============================================================================
   1. NAVIGATION SYSTEM (6 WORKSPACES)
   ============================================================================== */
function initNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  const sections = document.querySelectorAll(".content-section");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const titleMap = {
    overview: "Executive Overview",
    analytics: "Churn Analytics",
    segments: "Customer Segments",
    revenue: "Revenue Intelligence",
    explorer: "Customer Explorer",
    predict: "Prediction Lab"
  };

  const subtitleMap = {
    overview: "Subscriber portfolio health, churn velocity, and strategic risk distribution",
    analytics: "Interactive multidimensional cohort drill-down and behavioral attrition drivers",
    segments: "Cross-tabulated segment comparisons and operational risk cohorts",
    revenue: "Granular quantification of portfolio MRR, high-risk exposure, and expected loss",
    explorer: "Searchable subscriber registry with multidimensional filters and detailed profile inspector",
    predict: "Real-time individual inference engine and holdout model evaluation diagnostics"
  };

  window.navigateToSection = function(sectionKey) {
    navItems.forEach(n => n.classList.remove("active"));
    sections.forEach(s => s.classList.remove("active"));

    const targetNav = document.querySelector(`.nav-item[data-section="${sectionKey}"]`);
    if (targetNav) targetNav.classList.add("active");

    const targetElem = document.getElementById(`section-${sectionKey}`);
    if (targetElem) targetElem.classList.add("active");

    if (titleMap[sectionKey] && pageTitle) pageTitle.textContent = titleMap[sectionKey];
    if (subtitleMap[sectionKey] && pageSubtitle) pageSubtitle.textContent = subtitleMap[sectionKey];

    // Re-layout any Chart.js canvases that were hidden
    setTimeout(() => {
      Object.values(chartInstances).forEach(chart => {
        if (chart && typeof chart.resize === "function") chart.resize();
      });
    }, 60);

    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  navItems.forEach(item => {
    item.addEventListener("click", e => {
      e.preventDefault();
      const targetSection = item.getAttribute("data-section");
      window.navigateToSection(targetSection);
    });
  });

  // Sidebar Toggle
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const sidebar = document.getElementById("app-sidebar");
  const appLayout = document.querySelector(".app-layout");
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
      if (appLayout) appLayout.classList.toggle("sidebar-collapsed");
      setTimeout(() => {
        Object.values(chartInstances).forEach(chart => {
          if (chart && typeof chart.resize === "function") chart.resize();
        });
      }, 200);
    });
  }

  // Refresh Sync Button
  const btnRefresh = document.getElementById("btn-refresh-data");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", async () => {
      btnRefresh.disabled = true;
      const originalText = btnRefresh.innerHTML;
      btnRefresh.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin-icon"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/></svg><span>Syncing...</span>`;
      try {
        await Promise.all([loadOverview(), loadAnalyticsCharts(), loadCustomerSegments()]);
        if (typeof fetchCustomers === "function") await fetchCustomers();
      } catch (err) {
        console.error("Refresh error:", err);
      } finally {
        btnRefresh.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Synced</span>`;
        setTimeout(() => {
          btnRefresh.innerHTML = originalText;
          btnRefresh.disabled = false;
        }, 1500);
      }
    });
  }
}

/* ==============================================================================
   2. EXECUTIVE OVERVIEW & REVENUE INTELLIGENCE
   ============================================================================== */
async function loadOverview() {
  try {
    const res = await fetch("/api/overview");
    const data = await res.json();
    if (data.error) return;

    // Overview KPIs
    const elCust = document.getElementById("kpi-total-cust");
    if (elCust) elCust.textContent = data.total_customers.toLocaleString();

    const elChurnRate = document.getElementById("kpi-churn-rate");
    if (elChurnRate) elChurnRate.textContent = `${data.churn_rate_pct}%`;

    const elChurnCount = document.getElementById("kpi-churn-count");
    if (elChurnCount) elChurnCount.textContent = `${data.actual_churned.toLocaleString()} Churned`;

    const elRetainCount = document.getElementById("kpi-retain-count");
    if (elRetainCount) elRetainCount.textContent = `${data.actual_retained.toLocaleString()} Retained`;

    const elHighRisk = document.getElementById("kpi-high-risk");
    if (elHighRisk) elHighRisk.textContent = data.predicted_high_risk.toLocaleString();

    const elCritical = document.getElementById("kpi-critical");
    if (elCritical) elCritical.textContent = `${data.predicted_critical} Critical (≥80%)`;

    const fmtCurrency = (v) => {
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
    }

    // Chart.js Default Styling - Taste Skill Enterprise Palette
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
    Chart.defaults.plugins.tooltip.bodyFont = { family: "'JetBrains Mono', monospace", size: 11 };

    // Overview Chart 1: Ground Truth Churn Donut
    renderDonutChart(
      "overviewChurnChart",
      ["Retained (No)", "Churned (Yes)"],
      [data.actual_retained, data.actual_churned],
      ["#10b981", "#ef4444"]
    );

    // Overview Chart 2: Contract Churn Rate Bar
    renderSimpleBar(
      "overviewContractChart",
      ["Month-to-month", "One year", "Two year"],
      [42.71, 11.27, 2.83],
      ["#06b6d4", "#a855f7", "#10b981"],
      "%"
    );

    // Overview Chart 3: Monthly Revenue Exposure Donut
    const lowRev = data.low_risk_revenue || 250408.95;
    const medRev = data.medium_risk_revenue || 120161.40;
    const highRev = data.monthly_revenue_at_risk || 85546.25;
    renderDonutChart(
      "overviewRevenueRiskChart",
      ["Low Risk", "Medium Risk", "High Risk"],
      [lowRev, medRev, highRev],
      ["#10b981", "#f59e0b", "#ef4444"],
      "$"
    );

    // Revenue Section Chart: High-Risk MRR by Payment Method
    if (data.high_risk_revenue_by_payment) {
      const payLabels = Object.keys(data.high_risk_revenue_by_payment);
      const payValues = Object.values(data.high_risk_revenue_by_payment);
      renderHorizontalBar(
        "revPaymentRiskChart",
        payLabels,
        payValues,
        "#f59e0b"
      );
    }
  } catch (err) {
    console.error("Error in loadOverview:", err);
  }
}

/* ==============================================================================
   3. CHURN ANALYTICS WORKSPACE & INTERACTIVE FILTERS
   ============================================================================== */
let analyticsFilters = {
  contract: "All",
  internet: "All",
  payment: "All",
  tenure: "All"
};

function initAnalyticsWorkspace() {
  const contractSel = document.getElementById("analytics-contract-filter");
  const internetSel = document.getElementById("analytics-internet-filter");
  const paymentSel = document.getElementById("analytics-payment-filter");
  const tenureSel = document.getElementById("analytics-tenure-filter");
  const resetBtn = document.getElementById("btn-reset-analytics-filters");
  const metricToggles = document.querySelectorAll(".btn-toggle-metric");
  const drilldownBtn = document.getElementById("btn-drilldown-to-explorer");

  const applyFilters = () => {
    analyticsFilters.contract = contractSel ? contractSel.value : "All";
    analyticsFilters.internet = internetSel ? internetSel.value : "All";
    analyticsFilters.payment = paymentSel ? paymentSel.value : "All";
    analyticsFilters.tenure = tenureSel ? tenureSel.value : "All";
    loadAnalyticsCharts();
  };

  if (contractSel) contractSel.addEventListener("change", applyFilters);
  if (internetSel) internetSel.addEventListener("change", applyFilters);
  if (paymentSel) paymentSel.addEventListener("change", applyFilters);
  if (tenureSel) tenureSel.addEventListener("change", applyFilters);

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (contractSel) contractSel.value = "All";
      if (internetSel) internetSel.value = "All";
      if (paymentSel) paymentSel.value = "All";
      if (tenureSel) tenureSel.value = "All";
      applyFilters();
    });
  }

  metricToggles.forEach(btn => {
    btn.addEventListener("click", () => {
      metricToggles.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentAnalyticsMetric = btn.getAttribute("data-metric");
      loadAnalyticsCharts();
    });
  });

  if (drilldownBtn) {
    drilldownBtn.addEventListener("click", () => {
      // Transfer active analytics filters to Customer Explorer
      const expContract = document.getElementById("filter-contract");
      const expInternet = document.getElementById("filter-internet");
      if (expContract && analyticsFilters.contract !== "All") expContract.value = analyticsFilters.contract;
      if (expInternet && analyticsFilters.internet !== "All") expInternet.value = analyticsFilters.internet;

      window.navigateToSection("explorer");
      if (typeof fetchCustomers === "function") fetchCustomers();
    });
  }

  loadAnalyticsCharts();
}

async function loadAnalyticsCharts() {
  try {
    const params = new URLSearchParams(analyticsFilters);
    const res = await fetch(`/api/analytics-data?${params.toString()}`);
    const data = await res.json();
    if (data.error) return;

    // Update cohort indicator
    const cohortCount = document.getElementById("analytics-cohort-count");
    if (cohortCount) cohortCount.textContent = (data.total_filtered || 7043).toLocaleString();

    const cohortLabel = document.getElementById("analytics-cohort-label");
    if (cohortLabel) {
      const activeParts = [];
      if (analyticsFilters.contract !== "All") activeParts.push(analyticsFilters.contract);
      if (analyticsFilters.internet !== "All") activeParts.push(analyticsFilters.internet);
      if (analyticsFilters.payment !== "All") activeParts.push(analyticsFilters.payment);
      if (analyticsFilters.tenure !== "All") activeParts.push(analyticsFilters.tenure);

      if (activeParts.length > 0) {
        cohortLabel.textContent = `Filtered by: ${activeParts.join(" • ")}`;
      } else {
        cohortLabel.textContent = "Viewing entire subscriber portfolio";
      }
    }

    // Render 6 Cohort Charts based on currentAnalyticsMetric
    renderCohortChart("contractChart", data.contracts, "#06b6d4");
    renderCohortChart("tenureChart", data.tenure_groups, "#a855f7");
    renderCohortChart("internetChart", data.internet_services, "#3b82f6");
    renderCohortChart("paymentChart", data.payment_methods, "#f59e0b");
    renderCohortChart("techSupportChart", data.tech_support, "#10b981");
    renderCohortChart("chargesBinChart", data.monthly_charges_bins, "#ec4899");
  } catch (err) {
    console.error("Error loading analytics charts:", err);
  }
}

function renderCohortChart(canvasId, datasetObj, baseColor) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !datasetObj || !datasetObj.labels) return;

  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  if (currentAnalyticsMetric === "rate") {
    // Churn Rate (%)
    chartInstances[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: datasetObj.labels,
        datasets: [{
          label: "Churn Rate (%)",
          data: datasetObj.churn_rates,
          backgroundColor: baseColor,
          borderRadius: 4,
          maxBarThickness: 34
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: "rgba(51, 65, 85, 0.3)" },
            ticks: { callback: v => `${v}%` }
          },
          x: { grid: { display: false } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => `Churn Rate: ${c.parsed.y}% (${datasetObj.churn_counts[c.dataIndex]} / ${datasetObj.totals[c.dataIndex]} accounts)`
            }
          }
        }
      }
    });
  } else if (currentAnalyticsMetric === "count") {
    // Churn Count
    chartInstances[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: datasetObj.labels,
        datasets: [{
          label: "Churned Customers",
          data: datasetObj.churn_counts,
          backgroundColor: "#ef4444",
          borderRadius: 4,
          maxBarThickness: 34
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: "rgba(51, 65, 85, 0.3)" }
          },
          x: { grid: { display: false } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => `Churned: ${c.parsed.y.toLocaleString()} accounts`
            }
          }
        }
      }
    });
  } else {
    // Stacked Breakdown (Retained vs Churned)
    chartInstances[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: datasetObj.labels,
        datasets: [
          {
            label: "Retained",
            data: datasetObj.retained_counts,
            backgroundColor: "#10b981",
            borderRadius: 4,
            maxBarThickness: 34
          },
          {
            label: "Churned",
            data: datasetObj.churn_counts,
            backgroundColor: "#ef4444",
            borderRadius: 4,
            maxBarThickness: 34
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false } },
          y: { stacked: true, beginAtZero: true, grid: { color: "rgba(51, 65, 85, 0.3)" } }
        },
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 10, padding: 8 } },
          tooltip: {
            callbacks: {
              label: c => `${c.dataset.label}: ${c.parsed.y.toLocaleString()} accounts`
            }
          }
        }
      }
    });
  }
}

/* ==============================================================================
   4. CUSTOMER SEGMENTS WORKSPACE
   ============================================================================== */
async function loadCustomerSegments() {
  try {
    const res = await fetch("/api/segments");
    const data = await res.json();
    if (data.error) return;

    // 1. Render 2D Cross-Tabulation Matrix
    const matrixTbody = document.getElementById("segment-matrix-tbody");
    if (matrixTbody && data.matrix) {
      matrixTbody.innerHTML = "";
      data.matrix.forEach(row => {
        const tr = document.createElement("tr");

        // Rate pill styling
        let rateBadge = `<span class="badge-risk-low">${row.churn_rate}%</span>`;
        if (row.churn_rate >= 40) {
          rateBadge = `<span class="badge-risk-high">${row.churn_rate}%</span>`;
        } else if (row.churn_rate >= 20) {
          rateBadge = `<span class="badge-risk-medium">${row.churn_rate}%</span>`;
        }

        tr.innerHTML = `
          <td><strong>${row.contract}</strong></td>
          <td>${row.internet}</td>
          <td><strong>${row.count.toLocaleString()}</strong></td>
          <td>${rateBadge}</td>
          <td>${row.avg_tenure} mo</td>
          <td>$${row.avg_monthly_charges.toFixed(2)}</td>
          <td><strong style="color: ${row.avg_predicted_risk >= 50 ? '#f87171' : '#34d399'};">${row.avg_predicted_risk}%</strong></td>
          <td>${row.high_risk_count.toLocaleString()} accounts</td>
          <td>
            <button class="btn-matrix-drilldown" onclick="drilldownSegment('${row.contract}', '${row.internet}')">
              Explore →
            </button>
          </td>
        `;
        matrixTbody.appendChild(tr);
      });
    }

    // 2. Render Core Actionable Segment Cards
    const coreGrid = document.getElementById("core-segments-grid");
    if (coreGrid && data.core_segments) {
      coreGrid.innerHTML = "";
      data.core_segments.forEach(seg => {
        const card = document.createElement("div");
        card.className = "segment-summary-card";

        let riskTagClass = "badge-risk-low";
        if (seg.churn_rate >= 45) riskTagClass = "badge-risk-high";
        else if (seg.churn_rate >= 20) riskTagClass = "badge-risk-medium";

        card.innerHTML = `
          <div class="seg-card-header">
            <div>
              <h4 class="seg-name">${seg.name}</h4>
              <p class="seg-desc">${seg.description}</p>
            </div>
            <span class="${riskTagClass}">${seg.churn_rate}% Churn</span>
          </div>

          <div class="seg-metrics-row">
            <div class="seg-metric-box">
              <span class="seg-metric-label">Subscribers</span>
              <strong class="seg-metric-val">${seg.count.toLocaleString()}</strong>
            </div>
            <div class="seg-metric-box">
              <span class="seg-metric-label">Avg Monthly $</span>
              <strong class="seg-metric-val">$${seg.avg_monthly_charges.toFixed(2)}</strong>
            </div>
            <div class="seg-metric-box">
              <span class="seg-metric-label">High-Risk Base</span>
              <strong class="seg-metric-val text-danger">${seg.high_risk_count.toLocaleString()}</strong>
            </div>
            <div class="seg-metric-box">
              <span class="seg-metric-label">Monthly MRR</span>
              <strong class="seg-metric-val text-teal">$${seg.total_mrr.toLocaleString()}</strong>
            </div>
          </div>

          <div class="seg-card-footer">
            <button class="btn-card-drilldown" onclick="drilldownByName('${seg.name}')">
              Open Matching Customers in Explorer →
            </button>
          </div>
        `;
        coreGrid.appendChild(card);
      });
    }
  } catch (err) {
    console.error("Error loading segments:", err);
  }
}

// Global drilldown helpers
window.drilldownSegment = function(contract, internet) {
  const expContract = document.getElementById("filter-contract");
  const expInternet = document.getElementById("filter-internet");
  if (expContract) expContract.value = contract;
  if (expInternet) expInternet.value = internet;

  window.navigateToSection("explorer");
  if (typeof fetchCustomers === "function") fetchCustomers();
};

window.drilldownByName = function(name) {
  const expContract = document.getElementById("filter-contract");
  const expInternet = document.getElementById("filter-internet");
  const expRisk = document.getElementById("filter-risk");

  if (name.includes("Month-to-Month + Fiber Optic")) {
    if (expContract) expContract.value = "Month-to-month";
    if (expInternet) expInternet.value = "Fiber optic";
  } else if (name.includes("Long-Term Contracts")) {
    if (expContract) expContract.value = "Two year";
  } else if (name.includes("High-Value Fiber Optic")) {
    if (expInternet) expInternet.value = "Fiber optic";
  }

  window.navigateToSection("explorer");
  if (typeof fetchCustomers === "function") fetchCustomers();
};

/* ==============================================================================
   5. CUSTOMER EXPLORER & DETAIL DRAWER
   ============================================================================== */
let currentPage = 1;
let currentSearch = "";
let currentRisk = "All";
let currentContract = "All";
let currentInternet = "All";
let currentChurn = "All";
let currentSortBy = "customerID";
let currentSortDir = "asc";
let currentCustomerItems = [];

function initCustomerExplorer() {
  const searchInput = document.getElementById("customer-search");
  const filterRisk = document.getElementById("filter-risk");
  const filterContract = document.getElementById("filter-contract");
  const filterInternet = document.getElementById("filter-internet");
  const filterChurn = document.getElementById("filter-churn");
  const btnReset = document.getElementById("btn-reset-table-filters");
  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");
  const btnExport = document.getElementById("btn-export-csv");
  const sortHeaders = document.querySelectorAll(".sortable-th");

  // Drawer Elements
  const drawer = document.getElementById("customer-drawer");
  const drawerBackdrop = document.getElementById("drawer-backdrop");
  const btnCloseDrawer = document.getElementById("btn-close-drawer");

  const closeDrawer = () => {
    if (drawer) drawer.classList.remove("open");
    if (drawerBackdrop) drawerBackdrop.classList.remove("open");
  };

  if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeDrawer();
  });

  // Search input debounce
  let debounceTimer = null;
  if (searchInput) {
    searchInput.addEventListener("input", e => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        currentSearch = e.target.value.trim();
        currentPage = 1;
        fetchCustomers();
      }, 280);
    });
  }

  const applyTableFilters = () => {
    currentRisk = filterRisk ? filterRisk.value : "All";
    currentContract = filterContract ? filterContract.value : "All";
    currentInternet = filterInternet ? filterInternet.value : "All";
    currentChurn = filterChurn ? filterChurn.value : "All";
    currentPage = 1;
    fetchCustomers();
  };

  if (filterRisk) filterRisk.addEventListener("change", applyTableFilters);
  if (filterContract) filterContract.addEventListener("change", applyTableFilters);
  if (filterInternet) filterInternet.addEventListener("change", applyTableFilters);
  if (filterChurn) filterChurn.addEventListener("change", applyTableFilters);

  if (btnReset) {
    btnReset.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (filterRisk) filterRisk.value = "All";
      if (filterContract) filterContract.value = "All";
      if (filterInternet) filterInternet.value = "All";
      if (filterChurn) filterChurn.value = "All";
      currentSearch = "";
      applyTableFilters();
    });
  }

  if (btnPrev) {
    btnPrev.addEventListener("click", () => {
      if (currentPage > 1) {
        currentPage--;
        fetchCustomers();
      }
    });
  }

  if (btnNext) {
    btnNext.addEventListener("click", () => {
      currentPage++;
      fetchCustomers();
    });
  }

  if (btnExport) {
    btnExport.addEventListener("click", () => {
      const query = new URLSearchParams({
        search: currentSearch,
        risk: currentRisk,
        contract: currentContract,
        internet: currentInternet,
        churn: currentChurn,
        sort_by: currentSortBy,
        sort_dir: currentSortDir
      });
      window.location.href = `/api/customers/export?${query.toString()}`;
    });
  }

  // Sortable table headers
  sortHeaders.forEach(th => {
    th.addEventListener("click", () => {
      const col = th.getAttribute("data-sort");
      if (!col) return;

      if (currentSortBy === col) {
        currentSortDir = currentSortDir === "asc" ? "desc" : "asc";
      } else {
        currentSortBy = col;
        currentSortDir = (col === "MonthlyCharges" || col === "Predicted_Churn_Probability") ? "desc" : "asc";
      }

      sortHeaders.forEach(h => {
        h.classList.remove("active-sort");
        const icon = h.querySelector(".sort-icon");
        if (icon) icon.textContent = "↕";
      });

      th.classList.add("active-sort");
      const activeIcon = th.querySelector(".sort-icon");
      if (activeIcon) activeIcon.textContent = currentSortDir === "asc" ? "▲" : "▼";

      currentPage = 1;
      fetchCustomers();
    });
  });

  fetchCustomers();
}

async function fetchCustomers() {
  const tbody = document.getElementById("customers-table-body");
  const pageIndicator = document.getElementById("page-num");
  const paginationInfo = document.getElementById("pagination-info");
  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");

  if (tbody) {
    tbody.innerHTML = `<tr><td colspan="10" class="table-loading-cell">Loading verified customer intelligence records...</td></tr>`;
  }

  try {
    const query = new URLSearchParams({
      page: currentPage,
      per_page: 15,
      search: currentSearch,
      risk: currentRisk,
      contract: currentContract,
      internet: currentInternet,
      churn: currentChurn,
      sort_by: currentSortBy,
      sort_dir: currentSortDir
    });

    const res = await fetch(`/api/customers?${query.toString()}`);
    const data = await res.json();

    if (data.error || !data.items || data.items.length === 0) {
      if (tbody) {
        tbody.innerHTML = `<tr><td colspan="10" class="table-loading-cell" style="color: #94a3b8;">No matching customer records found for the applied filters.</td></tr>`;
      }
      if (paginationInfo) paginationInfo.textContent = "Showing 0 matching records";
      if (pageIndicator) pageIndicator.textContent = `Page 1 / 1`;
      if (btnPrev) btnPrev.disabled = true;
      if (btnNext) btnNext.disabled = true;
      currentCustomerItems = [];
      return;
    }

    currentCustomerItems = data.items;
    if (tbody) tbody.innerHTML = "";

    data.items.forEach((row, idx) => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";

      // Risk badge
      let riskBadge = `<span class="pill-badge pill-green"><span class="badge-dot"></span>Low Risk</span>`;
      if (row.Churn_Risk_Category === "High Risk") {
        riskBadge = `<span class="pill-badge pill-red"><span class="badge-dot"></span>High Risk</span>`;
      } else if (row.Churn_Risk_Category === "Medium Risk") {
        riskBadge = `<span class="pill-badge pill-yellow"><span class="badge-dot"></span>Medium Risk</span>`;
      }

      // Priority tag
      let priorityBadge = `<span class="priority-tag tag-low">${row.Retention_Priority || "P4 - Low"}</span>`;
      if (row.Retention_Priority && row.Retention_Priority.includes("Critical")) {
        priorityBadge = `<span class="priority-tag tag-critical">★ P1 - Critical</span>`;
      } else if (row.Retention_Priority && row.Retention_Priority.includes("High")) {
        priorityBadge = `<span class="priority-tag tag-high">P2 - High</span>`;
      } else if (row.Retention_Priority && row.Retention_Priority.includes("Medium")) {
        priorityBadge = `<span class="priority-tag tag-med">P3 - Medium</span>`;
      }

      // Actual churn status
      const churnBadge = row.Churn === "Yes"
        ? `<span class="status-churned">Yes</span>`
        : `<span class="status-retained">No</span>`;

      // Probability percentage
      const prob = row.Predicted_Churn_Probability !== null ? (row.Predicted_Churn_Probability * 100) : 0;
      let probColor = "#10b981";
      if (prob >= 60) probColor = "#ef4444";
      else if (prob >= 30) probColor = "#f59e0b";

      tr.innerHTML = `
        <td><strong class="cust-id">${row.customerID}</strong></td>
        <td>${row.tenure} mo</td>
        <td>${row.Contract}</td>
        <td>${row.InternetService || "—"}</td>
        <td><span class="pay-method">${row.PaymentMethod}</span></td>
        <td><strong>$${Number(row.MonthlyCharges).toFixed(2)}</strong></td>
        <td>${churnBadge}</td>
        <td><strong style="color: ${probColor};">${prob.toFixed(1)}%</strong></td>
        <td>${riskBadge}</td>
        <td>${priorityBadge}</td>
      `;

      tr.addEventListener("click", () => openCustomerDrawer(row));
      tbody.appendChild(tr);
    });

    const startRecord = (data.page - 1) * data.per_page + 1;
    const endRecord = Math.min(data.page * data.per_page, data.total);
    if (paginationInfo) {
      paginationInfo.textContent = `Showing ${startRecord.toLocaleString()} to ${endRecord.toLocaleString()} of ${data.total.toLocaleString()} matching records`;
    }
    if (pageIndicator) pageIndicator.textContent = `Page ${data.page} / ${data.pages}`;
    if (btnPrev) btnPrev.disabled = data.page <= 1;
    if (btnNext) btnNext.disabled = data.page >= data.pages;
  } catch (err) {
    console.error("Error fetching customers:", err);
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="10" class="table-loading-cell" style="color: #ef4444;">Error fetching customer data.</td></tr>`;
    }
  }
}

function openCustomerDrawer(cust) {
  const drawer = document.getElementById("customer-drawer");
  const backdrop = document.getElementById("drawer-backdrop");
  const custIdEl = document.getElementById("drawer-cust-id");
  const riskBadgeEl = document.getElementById("drawer-risk-badge");
  const bodyEl = document.getElementById("drawer-body");

  if (!drawer || !cust) return;

  if (custIdEl) custIdEl.textContent = cust.customerID;
  if (riskBadgeEl) {
    riskBadgeEl.textContent = cust.Churn_Risk_Category || "Low Risk";
    riskBadgeEl.className = `drawer-badge ${cust.Churn_Risk_Category === 'High Risk' ? 'badge-danger' : cust.Churn_Risk_Category === 'Medium Risk' ? 'badge-warning' : 'badge-success'}`;
  }

  const prob = (cust.Predicted_Churn_Probability !== null) ? (cust.Predicted_Churn_Probability * 100).toFixed(1) : "0.0";
  const probNum = parseFloat(prob);
  let barColor = "#10b981";
  if (probNum >= 60) barColor = "#ef4444";
  else if (probNum >= 30) barColor = "#f59e0b";

  if (bodyEl) {
    bodyEl.innerHTML = `
      <!-- Probability Gauge Box -->
      <div class="drawer-gauge-card">
        <div class="gauge-label-row">
          <span class="gauge-caption">Predicted Churn Probability</span>
          <span class="gauge-number" style="color: ${barColor};">${prob}%</span>
        </div>
        <div class="gauge-track">
          <div class="gauge-fill-bar" style="width: ${prob}%; background-color: ${barColor};"></div>
        </div>
        <div class="drawer-kpi-subrow">
          <span>Actual Ground Truth: <strong style="color: ${cust.Churn === 'Yes' ? '#f87171' : '#34d399'};">${cust.Churn === 'Yes' ? 'Churned (Yes)' : 'Retained (No)'}</strong></span>
          <span>Risk Score: <strong>${cust.Churn_Risk_Score || Math.round(probNum)} / 100</strong></span>
        </div>
      </div>

      <!-- Prescribed Retention Playbook -->
      <div class="drawer-action-box">
        <div class="action-panel-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
          <span>Recommended Retention Playbook:</span>
        </div>
        <div class="action-panel-text">${cust.Retention_Action || "Maintain ongoing satisfaction"}</div>
      </div>

      <!-- Demographics Section -->
      <div class="drawer-section">
        <h4 class="drawer-sec-title">Subscriber Profile</h4>
        <div class="drawer-grid-2">
          <div class="drawer-kv-card">
            <span class="kv-label">Gender</span>
            <strong class="kv-val">${cust.gender || '—'}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Senior Citizen</span>
            <strong class="kv-val">${cust.SeniorCitizen === 1 ? 'Yes (Senior)' : 'No (Under 65)'}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Partner Attached</span>
            <strong class="kv-val">${cust.Partner || '—'}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Dependents</span>
            <strong class="kv-val">${cust.Dependents || '—'}</strong>
          </div>
        </div>
      </div>

      <!-- Account & Billing Section -->
      <div class="drawer-section">
        <h4 class="drawer-sec-title">Account & Billing</h4>
        <div class="drawer-grid-2">
          <div class="drawer-kv-card">
            <span class="kv-label">Tenure Length</span>
            <strong class="kv-val">${cust.tenure} Months</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Contract Term</span>
            <strong class="kv-val">${cust.Contract || '—'}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Monthly Charges</span>
            <strong class="kv-val text-teal">$${Number(cust.MonthlyCharges).toFixed(2)}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Total Lifetime Charges</span>
            <strong class="kv-val">$${Number(cust.TotalCharges || 0).toFixed(2)}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Payment Channel</span>
            <strong class="kv-val">${cust.PaymentMethod || '—'}</strong>
          </div>
          <div class="drawer-kv-card">
            <span class="kv-label">Paperless Billing</span>
            <strong class="kv-val">${cust.PaperlessBilling || '—'}</strong>
          </div>
        </div>
      </div>

      <!-- Subscribed Services Section -->
      <div class="drawer-section">
        <h4 class="drawer-sec-title">Subscribed Telecom Services</h4>
        <div class="drawer-grid-3">
          <div class="drawer-service-chip ${cust.PhoneService === 'Yes' ? 'chip-active' : ''}">
            Phone Service: <strong>${cust.PhoneService || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.MultipleLines === 'Yes' ? 'chip-active' : ''}">
            Multiple Lines: <strong>${cust.MultipleLines || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.InternetService !== 'No' ? 'chip-active' : ''}">
            Internet: <strong>${cust.InternetService || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.OnlineSecurity === 'Yes' ? 'chip-active' : ''}">
            Security: <strong>${cust.OnlineSecurity || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.OnlineBackup === 'Yes' ? 'chip-active' : ''}">
            Backup: <strong>${cust.OnlineBackup || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.DeviceProtection === 'Yes' ? 'chip-active' : ''}">
            Protection: <strong>${cust.DeviceProtection || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.TechSupport === 'Yes' ? 'chip-active' : ''}">
            Tech Support: <strong>${cust.TechSupport || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.StreamingTV === 'Yes' ? 'chip-active' : ''}">
            Streaming TV: <strong>${cust.StreamingTV || 'No'}</strong>
          </div>
          <div class="drawer-service-chip ${cust.StreamingMovies === 'Yes' ? 'chip-active' : ''}">
            Movies: <strong>${cust.StreamingMovies || 'No'}</strong>
          </div>
        </div>
      </div>
    `;
  }

  drawer.classList.add("open");
  if (backdrop) backdrop.classList.add("open");
}

/* ==============================================================================
   6. PREDICTION LAB & MODEL EVALUATION
   ============================================================================== */
function initPredictionLab() {
  const form = document.getElementById("prediction-form");
  const presetHigh = document.getElementById("preset-high-risk");
  const presetLow = document.getElementById("preset-low-risk");
  const subtabBtns = document.querySelectorAll(".btn-predict-tab");

  // Subtab Switching (Live Predictor vs Model Evaluation)
  subtabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      subtabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const targetSubtab = btn.getAttribute("data-subtab");
      document.querySelectorAll(".predict-subtab-view").forEach(v => {
        v.classList.remove("active");
        v.classList.add("hidden");
      });

      const activeView = document.getElementById(`subtab-${targetSubtab}`);
      if (activeView) {
        activeView.classList.remove("hidden");
        activeView.classList.add("active");
      }

      if (targetSubtab === "model-evaluation") {
        renderModelComparisonChart();
      }
    });
  });

  // Presets
  if (presetHigh) {
    presetHigh.addEventListener("click", () => {
      setFormValues({
        gender: "Female",
        SeniorCitizen: "0",
        Partner: "No",
        Dependents: "No",
        tenure: "2",
        Contract: "Month-to-month",
        PaperlessBilling: "Yes",
        PaymentMethod: "Electronic check",
        PhoneService: "Yes",
        MultipleLines: "No",
        InternetService: "Fiber optic",
        OnlineSecurity: "No",
        OnlineBackup: "No",
        DeviceProtection: "No",
        TechSupport: "No",
        StreamingTV: "No",
        StreamingMovies: "No",
        MonthlyCharges: "70.70",
        TotalCharges: "151.65"
      });
    });
  }

  if (presetLow) {
    presetLow.addEventListener("click", () => {
      setFormValues({
        gender: "Male",
        SeniorCitizen: "0",
        Partner: "Yes",
        Dependents: "Yes",
        tenure: "48",
        Contract: "Two year",
        PaperlessBilling: "No",
        PaymentMethod: "Credit card (automatic)",
        PhoneService: "Yes",
        MultipleLines: "Yes",
        InternetService: "DSL",
        OnlineSecurity: "Yes",
        OnlineBackup: "Yes",
        DeviceProtection: "Yes",
        TechSupport: "Yes",
        StreamingTV: "No",
        StreamingMovies: "No",
        MonthlyCharges: "60.25",
        TotalCharges: "2892.00"
      });
    });
  }

  // Live Inference Form Submission
  if (form) {
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const btnSubmit = document.getElementById("btn-predict");
      if (btnSubmit) {
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = `<span>Running Inference Pipeline...</span>`;
      }

      const formData = new FormData(form);
      const payload = {};
      formData.forEach((value, key) => {
        payload[key] = value;
      });

      try {
        const res = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.status === "success" && data.prediction) {
          displayPredictionResult(data.prediction);
        } else {
          alert(`Prediction Error: ${data.message || "Failed to calculate prediction"}`);
        }
      } catch (err) {
        console.error("Prediction API error:", err);
        alert("Failed to connect to the prediction server endpoint.");
      } finally {
        if (btnSubmit) {
          btnSubmit.disabled = false;
          btnSubmit.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            <span>Execute Predictive Inference</span>
          `;
        }
      }
    });
  }
}

function setFormValues(values) {
  Object.keys(values).forEach(key => {
    const field = document.getElementById(key);
    if (field) field.value = values[key];
  });
}

function displayPredictionResult(pred) {
  const placeholder = document.getElementById("result-placeholder");
  const content = document.getElementById("result-content");
  const badge = document.getElementById("res-badge");

  const probPct = document.getElementById("res-prob-pct");
  const progressFill = document.getElementById("res-progress-fill");
  const predictedClass = document.getElementById("res-predicted-class");
  const riskTier = document.getElementById("res-risk-tier");
  const priority = document.getElementById("res-priority");
  const highRiskFlag = document.getElementById("res-high-risk-flag");
  const actionText = document.getElementById("res-action");
  const retainPct = document.getElementById("res-retain-pct");
  const riskScore = document.getElementById("res-risk-score");

  if (placeholder) placeholder.classList.add("hidden");
  if (content) content.classList.remove("hidden");

  if (badge) {
    badge.textContent = "Inference Complete";
    badge.className = "status-pill pill-success";
  }

  if (probPct) probPct.textContent = `${pred.churn_risk_percentage}%`;
  if (progressFill) progressFill.style.width = `${pred.churn_risk_percentage}%`;

  let riskColor = "#10b981";
  if (pred.churn_risk_category === "High Risk") riskColor = "#ef4444";
  else if (pred.churn_risk_category === "Medium Risk") riskColor = "#f59e0b";

  if (probPct) probPct.style.color = riskColor;
  if (progressFill) progressFill.style.backgroundColor = riskColor;
  if (riskTier) {
    riskTier.textContent = pred.churn_risk_category;
    riskTier.style.color = riskColor;
  }

  if (predictedClass) {
    predictedClass.textContent = pred.predicted_churn === "Yes" ? "Churn Likely (Yes)" : "Retention Likely (No)";
    predictedClass.style.color = pred.predicted_churn === "Yes" ? "#ef4444" : "#10b981";
  }

  if (priority) priority.textContent = pred.retention_priority;
  if (highRiskFlag) {
    highRiskFlag.textContent = pred.high_risk_flag;
    highRiskFlag.style.color = pred.high_risk_flag === "Yes" ? "#ef4444" : "#10b981";
  }

  if (actionText) actionText.textContent = pred.retention_action;
  if (retainPct) retainPct.textContent = `${(pred.retain_probability * 100).toFixed(1)}%`;
  if (riskScore) riskScore.textContent = `${pred.churn_risk_score} / 100`;
}

function renderModelComparisonChart() {
  const ctx = document.getElementById("modelComparisonChart");
  if (!ctx) return;

  if (chartInstances["modelComparisonChart"]) {
    chartInstances["modelComparisonChart"].destroy();
  }

  chartInstances["modelComparisonChart"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["ROC-AUC", "Accuracy", "Precision", "Recall", "F1-Score"],
      datasets: [
        {
          label: "Logistic Regression (Selected)",
          data: [84.21, 80.55, 65.72, 55.88, 60.40],
          backgroundColor: "#06b6d4",
          borderRadius: 4,
          maxBarThickness: 26
        },
        {
          label: "Random Forest (Benchmark)",
          data: [81.93, 78.71, 62.67, 48.93, 54.96],
          backgroundColor: "#475569",
          borderRadius: 4,
          maxBarThickness: 26
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          min: 40,
          max: 95,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}%` }
        },
        x: { grid: { display: false } }
      },
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, padding: 10 } },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${c.parsed.y}%`
          }
        }
      }
    }
  });
}

/* ==============================================================================
   UTILITY CHART HELPERS
   ============================================================================== */
function renderDonutChart(canvasId, labels, data, colors, prefix = "") {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  chartInstances[canvasId] = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderColor: "#0f1626",
        borderWidth: 2,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: context => {
              const val = context.parsed;
              return prefix === "$" ? `${context.label}: $${val.toLocaleString()}` : `${context.label}: ${val.toLocaleString()}`;
            }
          }
        }
      }
    }
  });
}

function renderSimpleBar(canvasId, labels, data, colors, unit = "") {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  chartInstances[canvasId] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderRadius: 4,
        maxBarThickness: 34
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `${v}${unit}` }
        },
        x: { grid: { display: false } }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `${c.label}: ${c.parsed.y}${unit}`
          }
        }
      }
    }
  });
}

function renderHorizontalBar(canvasId, labels, data, color) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  chartInstances[canvasId] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "High-Risk Charges ($)",
        data: data,
        backgroundColor: color,
        borderRadius: 4,
        maxBarThickness: 22
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          beginAtZero: true,
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { callback: v => `$${(v / 1000).toFixed(0)}k` }
        },
        y: { grid: { display: false } }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `High-Risk Exposure: $${c.parsed.x.toLocaleString()}`
          }
        }
      }
    }
  });
}


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
  cornerHeader.textContent = "Contract \ Internet";
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
        cellDiv.title = `${contract} + ${internet}\nChurn Rate: ${rate}% (${churned.toLocaleString()} / ${count.toLocaleString()} churned)\nClick to drill down into Explorer`;

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
