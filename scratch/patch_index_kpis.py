# Python script to regenerate index.html with the Taste Skill enterprise design structure
html_path = r"website\templates\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    orig = f.read()

# Let's inspect what lines in index.html define the executive KPI cards
old_kpi_block = """          <!-- KPI Cards Grid -->
          <div class="metrics-kpi-grid">
            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Total Customer Base</span>
                <span class="kpi-icon-wrap icon-cyan">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </span>
              </div>
              <div class="kpi-metric-value" id="kpi-total-cust">7,043</div>
              <div class="kpi-panel-footer">
                <span class="indicator-positive">100% Unique Accounts</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta">Full Portfolio</span>
              </div>
            </div>

            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Actual Churn Rate</span>
                <span class="kpi-icon-wrap icon-rose">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>
                </span>
              </div>
              <div class="kpi-metric-value value-rose" id="kpi-churn-rate">26.54%</div>
              <div class="kpi-panel-footer">
                <span class="indicator-negative" id="kpi-churn-count">1,869 Churned</span>
                <span class="meta-separator">•</span>
                <span class="indicator-positive" id="kpi-retain-count">5,174 Retained</span>
              </div>
            </div>

            <div class="kpi-panel highlight-panel-red">
              <div class="kpi-panel-header">
                <span class="kpi-label">High-Risk Customers</span>
                <span class="status-pill pill-danger">Prob ≥ 60%</span>
              </div>
              <div class="kpi-metric-value value-danger" id="kpi-high-risk">1,039</div>
              <div class="kpi-panel-footer">
                <span class="indicator-danger" id="kpi-critical">49 Critical (≥80%)</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta">14.75% of Base</span>
              </div>
            </div>

            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Portfolio Monthly Charges</span>
                <span class="kpi-icon-wrap icon-teal">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
                </span>
              </div>
              <div class="kpi-metric-value text-teal" id="kpi-total-mrr">$456,116.60</div>
              <div class="kpi-panel-footer">
                <span class="footer-meta" id="kpi-avg-charges">Avg $64.76 / subscriber</span>
              </div>
            </div>

            <div class="kpi-panel highlight-panel-amber">
              <div class="kpi-panel-header">
                <span class="kpi-label">High-Risk Monthly Charges</span>
                <span class="status-pill pill-warning">At Risk</span>
              </div>
              <div class="kpi-metric-value value-amber" id="kpi-revenue-risk">$85,546.25</div>
              <div class="kpi-panel-footer">
                <span class="indicator-warning" id="kpi-revenue-share">18.76% of Monthly MRR</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta" id="kpi-annual-risk">$1.03M / yr</span>
              </div>
            </div>
          </div>"""

new_kpi_block = """          <!-- Unified 5-Column Executive KPI Strip (No Icons on KPIs, Tabular Numbers) -->
          <div class="metrics-kpi-grid">
            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Total Customer Base</span>
                <span class="kpi-meta-badge">Verified Base</span>
              </div>
              <div class="kpi-metric-value num" id="kpi-total-cust">7,043</div>
              <div class="kpi-panel-footer">
                <span class="indicator-positive">100% Unique Accounts</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta">Full Portfolio</span>
              </div>
            </div>

            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Actual Churn Rate</span>
                <span class="status-pill pill-danger">Historical</span>
              </div>
              <div class="kpi-metric-value value-rose num" id="kpi-churn-rate">26.54%</div>
              <div class="kpi-panel-footer">
                <span class="indicator-negative" id="kpi-churn-count">1,869 Churned</span>
                <span class="meta-separator">•</span>
                <span class="indicator-positive" id="kpi-retain-count">5,174 Retained</span>
              </div>
            </div>

            <div class="kpi-panel highlight-panel-red">
              <div class="kpi-panel-header">
                <span class="kpi-label">High-Risk Customers</span>
                <span class="status-pill pill-danger">Prob ≥ 60%</span>
              </div>
              <div class="kpi-metric-value value-danger num" id="kpi-high-risk">1,039</div>
              <div class="kpi-panel-footer">
                <span class="indicator-danger" id="kpi-critical">49 Critical (≥80%)</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta">14.75% of Base</span>
              </div>
            </div>

            <div class="kpi-panel">
              <div class="kpi-panel-header">
                <span class="kpi-label">Portfolio Monthly Charges</span>
                <span class="kpi-meta-badge">Base MRR</span>
              </div>
              <div class="kpi-metric-value text-teal num" id="kpi-total-mrr">$456,116.60</div>
              <div class="kpi-panel-footer">
                <span class="footer-meta" id="kpi-avg-charges">Avg $64.76 / subscriber</span>
              </div>
            </div>

            <div class="kpi-panel highlight-panel-amber">
              <div class="kpi-panel-header">
                <span class="kpi-label">High-Risk Monthly Charges</span>
                <span class="status-pill pill-warning">18.76% of MRR</span>
              </div>
              <div class="kpi-metric-value value-amber num" id="kpi-revenue-risk">$85,546.25</div>
              <div class="kpi-panel-footer">
                <span class="indicator-warning" id="kpi-revenue-share">18.76% Monthly Share</span>
                <span class="meta-separator">•</span>
                <span class="footer-meta" id="kpi-annual-risk">$1.03M / yr</span>
              </div>
            </div>
          </div>"""

if old_kpi_block in orig:
    orig = orig.replace(old_kpi_block, new_kpi_block)
    print("Replaced old KPI block in index.html")
else:
    print("Warning: old_kpi_block not found in index.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(orig)

print("HTML updated.")
