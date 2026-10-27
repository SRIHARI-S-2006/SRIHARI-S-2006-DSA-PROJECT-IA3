import os
import re

html_path = r"website\templates\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update section-analytics: Add Heatmap, Scatter plot, 100% stacked, and Histograms
analytics_addition = """
          <!-- Ground Truth Churn Heatmap: Contract Type vs Internet Service -->
          <div class="dashboard-panel mt-3">
            <div class="panel-header">
              <div>
                <h3 class="panel-title">Contract × Internet Service Ground Truth Churn Heatmap</h3>
                <span class="panel-subtitle">Historical churn rate intensity across contract terms and internet infrastructure. Click any cell to drill down into Customer Explorer.</span>
              </div>
              <span class="status-pill pill-cyan">Interactive Heatmap</span>
            </div>
            <div class="heatmap-container" id="churn-heatmap-container">
              <!-- Rendered dynamically via JS -->
            </div>
            <div class="heatmap-legend-bar">
              <span class="heatmap-legend-label">Historical Churn Intensity:</span>
              <div class="heatmap-gradient-swatch"></div>
              <div class="heatmap-legend-ticks">
                <span>Low (&lt;10%)</span>
                <span>Moderate (20-30%)</span>
                <span>Elevated (35-45%)</span>
                <span>Severe (&gt;50%)</span>
              </div>
            </div>
          </div>

          <!-- 2-Column Row: Customer Scatter Plot & 100% Stacked Proportion -->
          <div class="grid-layout-2col mt-3">
            <div class="dashboard-panel">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">Customer Scatter: Tenure vs. Monthly Charges</h3>
                  <span class="panel-subtitle">Stratified 700-account sample distinguishing historical churners from retained subscribers</span>
                </div>
                <span class="status-pill pill-neutral">Stratified n=700</span>
              </div>
              <div class="chart-box-medium">
                <canvas id="scatterTenureChargesChart"></canvas>
              </div>
              <div class="custom-chart-legend">
                <div class="legend-chip"><span class="chip-dot dot-emerald"></span> Retained Subscriber</div>
                <div class="legend-chip"><span class="chip-dot dot-rose"></span> Churned Subscriber</div>
              </div>
            </div>

            <div class="dashboard-panel">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">100% Stacked Churn Proportion</h3>
                  <span class="panel-subtitle">Observed historical outcomes normalized to 100% of cohort</span>
                </div>
                <div class="btn-group-sm">
                  <button class="btn-metric-pill active" id="btn-stacked-contract" onclick="switchStackedDim('contract')">Contract</button>
                  <button class="btn-metric-pill" id="btn-stacked-payment" onclick="switchStackedDim('payment')">Payment</button>
                  <button class="btn-metric-pill" id="btn-stacked-tech" onclick="switchStackedDim('tech')">Tech Support</button>
                </div>
              </div>
              <div class="chart-box-medium">
                <canvas id="stackedProportionChart"></canvas>
              </div>
              <div class="custom-chart-legend">
                <div class="legend-chip"><span class="chip-dot dot-emerald"></span> Retained %</div>
                <div class="legend-chip"><span class="chip-dot dot-rose"></span> Churned %</div>
              </div>
            </div>
          </div>

          <!-- 2-Column Row: Distribution Histograms (Tenure & Monthly Charges) -->
          <div class="grid-layout-2col mt-3">
            <div class="dashboard-panel">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">Tenure Distribution Histogram</h3>
                  <span class="panel-subtitle">Explicit 12-month tenure bins split by historical churn status</span>
                </div>
                <span class="status-pill pill-cyan">Numeric Bins</span>
              </div>
              <div class="chart-box-medium">
                <canvas id="tenureHistogramChart"></canvas>
              </div>
              <div class="custom-chart-legend">
                <div class="legend-chip"><span class="chip-dot dot-emerald"></span> Retained</div>
                <div class="legend-chip"><span class="chip-dot dot-rose"></span> Churned</div>
              </div>
            </div>

            <div class="dashboard-panel">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">Monthly Charges Distribution Histogram</h3>
                  <span class="panel-subtitle">Explicit billing range bins ($) split by historical churn status</span>
                </div>
                <span class="status-pill pill-cyan">Numeric Bins</span>
              </div>
              <div class="chart-box-medium">
                <canvas id="chargesHistogramChart"></canvas>
              </div>
              <div class="custom-chart-legend">
                <div class="legend-chip"><span class="chip-dot dot-emerald"></span> Retained</div>
                <div class="legend-chip"><span class="chip-dot dot-rose"></span> Churned</div>
              </div>
            </div>
          </div>
"""

# Insert analytics_addition before 6 Deep-Dive Analytical Charts
target_analytics_marker = "<!-- 6 Deep-Dive Analytical Charts -->"
if target_analytics_marker in html:
    html = html.replace(target_analytics_marker, analytics_addition + "\n          " + target_analytics_marker)
    print("Added analytics visualizations.")
else:
    print("Warning: target_analytics_marker not found!")

# 2. Update section-segments: Add Segment Bubble Chart and Interactive Segment Comparison Tool
segments_addition = """
          <!-- Segment Bubble Chart: Charges vs Churn Rate (Size: Accounts) -->
          <div class="dashboard-panel mt-3">
            <div class="panel-header">
              <div>
                <h3 class="panel-title">Multi-Segment Bubble Matrix: Charges vs Historical Churn</h3>
                <span class="panel-subtitle">X: Avg Monthly Charges ($) • Y: Historical Churn Rate (%) • Bubble Radius: Subscriber Count. Click any bubble to explore.</span>
              </div>
              <span class="status-pill pill-cyan">9 Core Segments</span>
            </div>
            <div class="chart-box-medium">
              <canvas id="segmentBubbleChart"></canvas>
            </div>
          </div>

          <!-- Interactive Segment Comparison Tool -->
          <div class="dashboard-panel mt-4">
            <div class="panel-header">
              <div>
                <h3 class="panel-title">Interactive Segment Comparison Tool</h3>
                <span class="panel-subtitle">Select any two customer segments to evaluate head-to-head operational metrics and risk disparities</span>
              </div>
              <span class="status-pill pill-purple">Cohort Benchmarking</span>
            </div>

            <div class="segment-compare-selectors">
              <div class="compare-selector-box">
                <label for="seg-compare-select-a">Segment A (Baseline):</label>
                <select id="seg-compare-select-a" class="form-select"></select>
              </div>
              <div class="compare-vs-badge">VS</div>
              <div class="compare-selector-box">
                <label for="seg-compare-select-b">Segment B (Comparison):</label>
                <select id="seg-compare-select-b" class="form-select"></select>
              </div>
            </div>

            <div class="segment-compare-results-grid" id="segment-compare-grid">
              <!-- Populated via JS -->
            </div>
          </div>
"""

target_segments_marker = '<!-- Core Actionable Segments Grid -->'
if target_segments_marker in html:
    html = html.replace(target_segments_marker, segments_addition + "\n          " + target_segments_marker)
    print("Added segments visualizations.")
else:
    print("Warning: target_segments_marker not found!")

# 3. Update section-revenue: Add Revenue-Risk Pareto Chart and Operational Risk Threshold Simulator
revenue_addition = """
          <!-- Revenue-Risk Pareto Analysis -->
          <div class="dashboard-panel mt-3">
            <div class="panel-header">
              <div>
                <h3 class="panel-title">High-Risk Revenue Pareto Analysis (80/20 Rule)</h3>
                <span class="panel-subtitle">Bars: High-Risk MRR Exposure by Billing Channel ($) • Line: Cumulative Percentage of Exposure (%) with 80% Threshold</span>
              </div>
              <span class="status-pill pill-amber">Pareto Exposure</span>
            </div>
            <div class="chart-box-medium">
              <canvas id="revenueParetoChart"></canvas>
            </div>
            <div class="pareto-methodology-note">
              <strong>Calculation Methodology:</strong> High-risk monthly charges are summed per payment channel for accounts with predicted churn probability &ge; 60% ($85,546.25 total). Channels are sorted descending, and cumulative exposure share is computed. Note: Electronic check billing alone accounts for <strong>$70,566.90 (82.49%)</strong> of total high-risk exposure.
            </div>
          </div>

          <!-- Operational Risk Threshold Simulator -->
          <div class="dashboard-panel mt-4">
            <div class="panel-header">
              <div>
                <h3 class="panel-title">Operational Risk Threshold Simulator</h3>
                <span class="panel-subtitle">Simulate shifting the triage decision boundary to calibrate retention team workload and flagged revenue coverage</span>
              </div>
              <span class="status-pill pill-cyan">Interactive Simulation</span>
            </div>

            <div class="threshold-simulator-container">
              <div class="simulator-slider-row">
                <div class="slider-label-group">
                  <span class="slider-title">Flagging Threshold (Probability):</span>
                  <span class="slider-value-badge" id="sim-threshold-val">0.60 (60%)</span>
                </div>
                <input type="range" id="sim-threshold-slider" min="0.10" max="0.90" step="0.05" value="0.60" class="simulator-range-slider">
                <div class="slider-scale-ticks">
                  <span>0.10 (Sensitive)</span>
                  <span>0.30</span>
                  <span>0.50 (Default Binary)</span>
                  <span>0.60 (High-Risk Base)</span>
                  <span>0.80</span>
                  <span>0.90 (Critical Triage)</span>
                </div>
              </div>

              <div class="simulator-metrics-grid">
                <div class="sim-metric-card">
                  <span class="sim-metric-label">Flagged Accounts</span>
                  <div class="sim-metric-num" id="sim-flagged-count">1,039</div>
                  <span class="sim-metric-sub" id="sim-flagged-pct">14.75% of portfolio (7,043)</span>
                </div>

                <div class="sim-metric-card">
                  <span class="sim-metric-label">Flagged Monthly Revenue</span>
                  <div class="sim-metric-num text-danger" id="sim-flagged-mrr">$85,546.25</div>
                  <span class="sim-metric-sub" id="sim-flagged-mrr-pct">18.76% of monthly MRR</span>
                </div>

                <div class="sim-metric-card">
                  <span class="sim-metric-label">Annualized Exposure Run-Rate</span>
                  <div class="sim-metric-num text-purple" id="sim-annual-exposure">$1.03M / yr</div>
                  <span class="sim-metric-sub">Flagged Monthly &times; 12</span>
                </div>

                <div class="sim-metric-card">
                  <span class="sim-metric-label">Operational Delta vs Baseline</span>
                  <div class="sim-metric-num text-teal" id="sim-delta-count">0 accounts</div>
                  <span class="sim-metric-sub" id="sim-delta-mrr">$0.00 / mo vs 0.60 threshold</span>
                </div>
              </div>

              <div class="simulator-guidance-alert">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                <span><strong>Data Science Rigor Notice:</strong> Adjusting this operational cutoff reallocates campaign intervention resources across the subscriber base. It does <em>not</em> retrain or alter the underlying statistical model weights or change its intrinsic holdout discrimination metrics.</span>
              </div>
            </div>
          </div>
"""

target_revenue_marker = '<!-- Verified 25% Retention Scenario -->'
if target_revenue_marker in html:
    html = html.replace(target_revenue_marker, revenue_addition + "\n          " + target_revenue_marker)
    print("Added revenue visualizations.")
else:
    print("Warning: target_revenue_marker not found!")

# 4. Update section-predict: Add Batch Prediction tab and Predicted-Risk Histogram
old_predict_tabs = """          <div class="predict-tab-bar">
            <button class="btn-predict-tab active" data-subtab="live-predictor">Real-Time Churn Predictor</button>
            <button class="btn-predict-tab" data-subtab="model-evaluation">Model Performance & Evaluation</button>
          </div>"""

new_predict_tabs = """          <div class="predict-tab-bar">
            <button class="btn-predict-tab active" data-subtab="live-predictor">Real-Time Churn Predictor</button>
            <button class="btn-predict-tab" data-subtab="batch-predictor">Batch Customer Prediction (CSV)</button>
            <button class="btn-predict-tab" data-subtab="model-evaluation">Model Performance & Evaluation</button>
          </div>"""

if old_predict_tabs in html:
    html = html.replace(old_predict_tabs, new_predict_tabs)
    print("Updated predict tab bar.")

batch_subtab_html = """
          <!-- Subtab 2: Batch Customer Prediction (CSV Engine) -->
          <div id="subtab-batch-predictor" class="predict-subtab-view hidden">
            <div class="dashboard-panel">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">Batch Customer Inference Engine</h3>
                  <span class="panel-subtitle">Upload subscriber CSV files for automated feature validation, pipeline inference, and prescriptive action tagging</span>
                </div>
                <div class="batch-header-actions">
                  <a href="/api/predict-batch/template" class="btn-action-secondary" download="sample_churn_batch_template.csv">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    <span>Download Sample CSV Template</span>
                  </a>
                </div>
              </div>

              <!-- Upload Dropzone -->
              <div class="batch-upload-dropzone" id="batch-dropzone">
                <input type="file" id="batch-file-input" accept=".csv" class="hidden-file-input">
                <div class="dropzone-content">
                  <div class="dropzone-icon">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  </div>
                  <h4>Drag & Drop Customer CSV or Click to Browse</h4>
                  <p>Requires standard subscriber features. Target label <code>Churn</code> is strictly excluded from inference inputs.</p>
                  <button type="button" class="btn-upload-browse" onclick="document.getElementById('batch-file-input').click()">Select CSV File</button>
                </div>
              </div>

              <!-- Validation Alert -->
              <div class="batch-validation-alert hidden" id="batch-error-box">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <div id="batch-error-msg">Validation error details</div>
              </div>

              <!-- Loading State -->
              <div class="batch-loading-indicator hidden" id="batch-spinner">
                <span class="pulse-indicator"></span>
                <span>Executing pre-trained model pipeline inference across batch records...</span>
              </div>

              <!-- Batch Results Container -->
              <div class="batch-results-wrapper hidden" id="batch-results-container">
                <div class="batch-summary-kpis">
                  <div class="batch-kpi-card">
                    <span class="batch-kpi-label">Total Records Scored</span>
                    <div class="batch-kpi-num" id="batch-kpi-total">0</div>
                  </div>
                  <div class="batch-kpi-card">
                    <span class="batch-kpi-label">Predicted Churners</span>
                    <div class="batch-kpi-num text-danger" id="batch-kpi-churners">0</div>
                  </div>
                  <div class="batch-kpi-card">
                    <span class="batch-kpi-label">Predicted Churn Rate</span>
                    <div class="batch-kpi-num value-amber" id="batch-kpi-rate">0.0%</div>
                  </div>
                  <div class="batch-kpi-card">
                    <span class="batch-kpi-label">High-Risk Accounts (&ge;60%)</span>
                    <div class="batch-kpi-num text-purple" id="batch-kpi-high-risk">0</div>
                  </div>
                  <div class="batch-kpi-card">
                    <span class="batch-kpi-label">Export Scored Batch</span>
                    <a href="/api/predict-batch/download" id="btn-batch-download-csv" class="btn-batch-download" download="batch_scored_predictions.csv">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                      <span>Download Scored CSV</span>
                    </a>
                  </div>
                </div>

                <div class="table-responsive-box mt-3">
                  <table class="enterprise-table" id="batch-results-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Customer ID</th>
                        <th>Contract</th>
                        <th>Internet</th>
                        <th>Monthly ($)</th>
                        <th>Predicted Risk</th>
                        <th>Classification</th>
                        <th>Risk Tier</th>
                        <th>Prescribed Retention Playbook</th>
                      </tr>
                    </thead>
                    <tbody id="batch-results-tbody"></tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
"""

target_subtab2_marker = '<!-- Subtab 2: Model Performance & Evaluation -->'
if target_subtab2_marker in html:
    html = html.replace(target_subtab2_marker, batch_subtab_html + "\n          " + target_subtab2_marker)
    print("Added batch prediction subtab.")
else:
    print("Warning: target_subtab2_marker not found!")

risk_hist_addition = """
            <!-- Predicted-Risk Distribution Histogram -->
            <div class="dashboard-panel mt-3">
              <div class="panel-header">
                <div>
                  <h3 class="panel-title">Model Predicted-Risk Distribution & Operational Risk Tiers</h3>
                  <span class="panel-subtitle">Frequency distribution of continuous churn probabilities across the full subscriber portfolio with decision boundaries marked</span>
                </div>
                <span class="status-pill pill-cyan">Full Portfolio (n=7,043)</span>
              </div>
              <div class="chart-box-medium">
                <canvas id="predictedRiskHistChart"></canvas>
              </div>
              <div class="panel-footer-insight">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                <span><strong>Probability Definition:</strong> Values represent predicted churn probabilities generated by the Logistic Regression pipeline. They are uncalibrated operational scores utilized for subscriber tiering and triage ranking.</span>
              </div>
            </div>
"""

target_cm_marker = '<!-- Confusion Matrix Diagnostics -->'
if target_cm_marker in html:
    html = html.replace(target_cm_marker, risk_hist_addition + "\n            " + target_cm_marker)
    print("Added predicted-risk histogram.")
else:
    print("Warning: target_cm_marker not found!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html successfully.")
