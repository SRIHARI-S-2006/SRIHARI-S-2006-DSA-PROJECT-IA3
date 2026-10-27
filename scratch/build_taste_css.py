css_content = """/* ==============================================================================
   CCPRA — Customer Churn Prediction & Retention Analytics
   Enterprise SaaS Analytics Design System (Taste Skill Frontend Architecture)
   ============================================================================== */

:root {
  /* Core Obsidian / Deep Slate Palette (references/app-screens.md) */
  --bg-body: #080c14;
  --bg-sidebar: #0b101b;
  --bg-topbar: rgba(11, 16, 27, 0.88);
  --bg-panel: #0f1726;
  --bg-panel-elevated: #141f33;
  --bg-input: #121c2d;
  --bg-active: rgba(56, 189, 248, 0.12);

  /* Precise 1px Separation (Flat Surfaces, No Muddy Shadow Blur) */
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-panel: rgba(255, 255, 255, 0.08);
  --border-control: rgba(255, 255, 255, 0.13);
  --border-highlight: rgba(56, 189, 248, 0.4);

  /* High-Contrast Typography */
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-dim: #475569;

  /* Data-Driven Semantic Palette (Colour goes on data, not chrome) */
  --accent-cyan: #38bdf8;
  --accent-cyan-border: rgba(56, 189, 248, 0.35);
  --accent-cyan-subtle: rgba(56, 189, 248, 0.1);
  --accent-teal: #2dd4bf;
  --accent-amber: #f59e0b;
  --accent-purple: #a855f7;

  --color-success: #10b981;
  --color-success-bg: rgba(16, 185, 129, 0.12);
  --color-success-border: rgba(16, 185, 129, 0.3);

  --color-danger: #f43f5e;
  --color-danger-bg: rgba(244, 63, 94, 0.12);
  --color-danger-border: rgba(244, 63, 94, 0.35);

  --color-warning: #f59e0b;
  --color-warning-bg: rgba(245, 158, 11, 0.12);
  --color-warning-border: rgba(245, 158, 11, 0.3);

  --color-purple: #c084fc;
  --color-purple-bg: rgba(192, 132, 252, 0.12);
  --color-purple-border: rgba(192, 132, 252, 0.3);

  /* Typography Stacks */
  --font-main: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

  /* Dimensions & Radius */
  --sidebar-width: 250px;
  --sidebar-collapsed-width: 70px;
  --topbar-height: 64px;
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 0.14s ease;
  --transition-normal: 0.22s ease;
}

/* ==============================================================================
   RESET & FOUNDATIONS
   ============================================================================== */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 14px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: var(--font-main);
  background-color: var(--bg-body);
  color: var(--text-primary);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

.num, table, .kpi-metric-value, .step-math {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;
}

/* ==============================================================================
   LAYOUT SHELL
   ============================================================================== */
.app-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

/* Sidebar Navigation */
.app-sidebar {
  width: var(--sidebar-width);
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  transition: width var(--transition-normal);
}

.app-sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-brand {
  height: var(--topbar-height);
  padding: 0 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.brand-logo-mark {
  width: 32px;
  height: 32px;
  min-width: 32px;
  background: var(--accent-cyan);
  color: #040810;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}

.brand-titles {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  white-space: nowrap;
}

.brand-name {
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ffffff;
}

.brand-accent {
  color: var(--accent-cyan);
}

.brand-meta {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}

.sidebar-collapsed .brand-titles,
.app-sidebar.collapsed .brand-titles {
  display: none;
}

.sidebar-nav {
  padding: 16px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  overflow-y: auto;
}

.nav-group-label {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-dim);
  padding: 12px 12px 6px;
}

.sidebar-collapsed .nav-group-label,
.app-sidebar.collapsed .nav-group-label {
  display: none;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  transition: var(--transition-fast);
  white-space: nowrap;
  position: relative;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.04);
  color: #ffffff;
}

.nav-item.active {
  background: var(--bg-active);
  color: #ffffff;
  font-weight: 600;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 18%;
  bottom: 18%;
  width: 3px;
  background: var(--accent-cyan);
  border-radius: 0 2px 2px 0;
}

.nav-svg {
  min-width: 18px;
  color: inherit;
  stroke-width: 1.8;
}

.sidebar-collapsed .nav-text,
.app-sidebar.collapsed .nav-text {
  display: none;
}

/* Sidebar Footer Box */
.sidebar-status-box {
  margin: 12px 10px 16px;
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sidebar-collapsed .sidebar-status-box,
.app-sidebar.collapsed .sidebar-status-box {
  display: none;
}

.status-indicator-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulse-indicator {
  width: 7px;
  height: 7px;
  background-color: var(--color-success);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--color-success);
}

.status-name {
  font-size: 0.74rem;
  font-weight: 600;
  color: #ffffff;
}

.status-model-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.model-metric {
  color: var(--accent-cyan);
  font-family: var(--font-mono);
}

/* Workspace Canvas */
.app-workspace {
  margin-left: var(--sidebar-width);
  width: calc(100% - var(--sidebar-width));
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left var(--transition-normal), width var(--transition-normal);
}

.sidebar-collapsed .app-workspace,
.app-layout.sidebar-collapsed .app-workspace {
  margin-left: var(--sidebar-collapsed-width);
  width: calc(100% - var(--sidebar-collapsed-width));
}

/* Topbar Header */
.app-topbar {
  height: var(--topbar-height);
  position: sticky;
  top: 0;
  z-index: 90;
  background-color: var(--bg-topbar);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.btn-sidebar-toggle {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
}

.btn-sidebar-toggle:hover {
  background: var(--bg-panel-elevated);
  color: #ffffff;
  border-color: var(--border-panel);
}

.page-title-block {
  display: flex;
  flex-direction: column;
}

.page-main-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: #ffffff;
  line-height: 1.2;
}

.page-sub-title {
  font-size: 0.76rem;
  color: var(--text-muted);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meta-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-size: 0.74rem;
  color: var(--text-secondary);
  font-weight: 500;
  font-family: var(--font-mono);
}

.badge-dot-green {
  width: 6px;
  height: 6px;
  background-color: var(--color-success);
  border-radius: 50%;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 5px 12px;
  color: var(--text-secondary);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-fast);
}

.btn-refresh:hover:not(:disabled) {
  background: var(--bg-panel-elevated);
  border-color: var(--accent-cyan);
  color: #ffffff;
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Workspace Scrollable Body */
.workspace-content {
  padding: 24px 28px 60px;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
}

.content-section {
  display: none;
}

.content-section.active {
  display: block;
  animation: fadeIn 0.18s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ==============================================================================
   EXECUTIVE OVERVIEW: 5-COLUMN KPI STRIP
   ============================================================================== */
.metrics-kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

@media (max-width: 1300px) {
  .metrics-kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 800px) {
  .metrics-kpi-grid {
    grid-template-columns: 1fr;
  }
}

.kpi-panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 110px;
  transition: var(--transition-fast);
}

.kpi-panel:hover {
  border-color: rgba(255, 255, 255, 0.18);
  background: var(--bg-panel-elevated);
}

.kpi-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.kpi-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.kpi-meta-badge {
  font-size: 0.68rem;
  font-family: var(--font-mono);
  color: var(--text-dim);
}

.kpi-metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #ffffff;
  line-height: 1.1;
  font-family: var(--font-mono);
}

.kpi-metric-value.value-rose {
  color: var(--color-danger);
}

.kpi-metric-value.value-danger {
  color: #fb7185;
}

.kpi-metric-value.text-teal {
  color: var(--accent-teal);
}

.kpi-metric-value.value-amber {
  color: var(--accent-amber);
}

.kpi-panel-footer {
  margin-top: 10px;
  font-size: 0.72rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.indicator-positive { color: var(--color-success); font-weight: 600; }
.indicator-negative { color: var(--color-danger); font-weight: 600; }
.indicator-warning { color: var(--color-warning); font-weight: 600; }
.indicator-danger { color: #fb7185; font-weight: 600; }
.footer-meta { color: var(--text-muted); }
.meta-separator { color: var(--text-dim); }

/* Status Pills */
.status-pill {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  white-space: nowrap;
  font-family: var(--font-mono);
}

.pill-neutral { background: rgba(255, 255, 255, 0.06); color: var(--text-secondary); border: 1px solid var(--border-subtle); }
.pill-cyan { background: var(--accent-cyan-subtle); color: var(--accent-cyan); border: 1px solid var(--accent-cyan-border); }
.pill-success { background: var(--color-success-bg); color: var(--color-success); border: 1px solid var(--color-success-border); }
.pill-warning { background: var(--color-warning-bg); color: var(--color-warning); border: 1px solid var(--color-warning-border); }
.pill-danger { background: var(--color-danger-bg); color: #fb7185; border: 1px solid var(--color-danger-border); }
.pill-purple { background: var(--color-purple-bg); color: var(--color-purple); border: 1px solid var(--color-purple-border); }

/* Key Insights Summary Strip */
.insights-summary-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

@media (max-width: 900px) {
  .insights-summary-strip { grid-template-columns: 1fr; }
}

.insight-badge-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-panel);
  border-left: 3px solid var(--accent-cyan);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.insight-badge-card:nth-child(2) { border-left-color: var(--accent-amber); }
.insight-badge-card:nth-child(3) { border-left-color: var(--color-danger); }

.insight-icon-box {
  display: flex;
  align-items: center;
  color: var(--accent-cyan);
}

.insight-body {
  font-size: 0.78rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.insight-body strong {
  color: #ffffff;
}

/* ==============================================================================
   DASHBOARD PANELS & CHART CONTAINERS
   ============================================================================== */
.dashboard-panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.dashboard-panel .panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.panel-title {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
}

.panel-subtitle {
  font-size: 0.74rem;
  color: var(--text-muted);
  display: block;
  margin-top: 2px;
}

/* Grid Layouts */
.grid-layout-2col {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.grid-layout-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 1100px) {
  .grid-layout-3col { grid-template-columns: 1fr; }
  .grid-layout-2col { grid-template-columns: 1fr; }
}

.mt-3 { margin-top: 16px; }
.mt-4 { margin-top: 22px; }

/* Fixed & Responsive Chart Boxes */
.chart-box-compact {
  height: 220px;
  position: relative;
  width: 100%;
}

.chart-box-standard {
  height: 260px;
  position: relative;
  width: 100%;
}

.chart-box-medium {
  height: 300px;
  position: relative;
  width: 100%;
}

.custom-chart-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.legend-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.73rem;
  color: var(--text-secondary);
}

.chip-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-emerald { background-color: var(--color-success); }
.dot-rose { background-color: var(--color-danger); }
.dot-cyan { background-color: var(--accent-cyan); }
.dot-purple { background-color: var(--color-purple); }
.dot-amber { background-color: var(--accent-amber); }

/* ==============================================================================
   WORKSPACE 2: CHURN ANALYTICS & INTERACTIVE HEATMAP
   ============================================================================== */
.interactive-filter-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  background: var(--bg-panel);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.filter-controls-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-chip-unit {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-chip-unit label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-muted);
}

.filter-dropdown-sm, .filter-dropdown {
  background: var(--bg-input);
  border: 1px solid var(--border-control);
  color: #ffffff;
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.78rem;
  cursor: pointer;
  outline: none;
}

.filter-dropdown-sm:focus, .filter-dropdown:focus {
  border-color: var(--accent-cyan);
}

.btn-filter-reset {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  cursor: pointer;
}

.btn-filter-reset:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.analytics-view-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
}

.toggle-caption {
  font-size: 0.72rem;
  color: var(--text-muted);
  text-transform: uppercase;
  font-weight: 600;
}

.btn-toggle-metric, .btn-metric-pill {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  cursor: pointer;
  transition: var(--transition-fast);
}

.btn-toggle-metric.active, .btn-metric-pill.active {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
  border-color: var(--accent-cyan);
}

.active-filter-indicator-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  background: rgba(56, 189, 248, 0.06);
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-radius: var(--radius-sm);
  font-size: 0.78rem;
  margin-bottom: 16px;
}

.cohort-sep {
  margin: 0 6px;
  color: var(--text-dim);
}

.btn-drilldown-action {
  background: transparent;
  border: none;
  color: var(--accent-cyan);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-drilldown-action:hover {
  text-decoration: underline;
}

/* Heatmap Grid */
.heatmap-container {
  display: grid;
  grid-template-columns: 140px repeat(3, 1fr);
  gap: 8px;
  margin-top: 8px;
}

.heatmap-header-col {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 8px;
  text-align: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-xs);
}

.heatmap-header-row {
  font-size: 0.78rem;
  font-weight: 600;
  color: #ffffff;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--radius-xs);
}

.heatmap-cell {
  border-radius: var(--radius-sm);
  padding: 12px 8px;
  text-align: center;
  cursor: pointer;
  transition: transform var(--transition-fast), filter var(--transition-fast);
  border: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 3px;
}

.heatmap-cell:hover {
  transform: translateY(-2px);
  filter: brightness(1.2);
  border-color: var(--accent-cyan);
}

.heatmap-rate {
  font-size: 1.15rem;
  font-weight: 800;
  font-family: var(--font-mono);
}

.heatmap-count {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.heatmap-legend-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--border-subtle);
  flex-wrap: wrap;
}

.heatmap-legend-label {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted);
}

.heatmap-gradient-swatch {
  width: 140px;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right, rgba(16, 185, 129, 0.3), rgba(245, 158, 11, 0.5), rgba(244, 63, 94, 0.8));
}

.heatmap-legend-ticks {
  display: flex;
  justify-content: space-between;
  flex: 1;
  font-size: 0.7rem;
  color: var(--text-muted);
}

/* ==============================================================================
   WORKSPACE 3: CUSTOMER SEGMENTS & COMPARISON
   ============================================================================== */
.enterprise-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  text-align: left;
}

.table-responsive-box {
  overflow-x: auto;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}

.enterprise-table th {
  background: #111a2c;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-panel);
  white-space: nowrap;
}

.enterprise-table td {
  padding: 11px 14px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  white-space: nowrap;
}

.enterprise-table tr:hover td {
  background-color: rgba(255, 255, 255, 0.02);
  color: #ffffff;
}

.btn-matrix-drilldown {
  background: transparent;
  border: 1px solid var(--border-control);
  color: var(--accent-cyan);
  padding: 3px 8px;
  border-radius: var(--radius-xs);
  font-size: 0.72rem;
  cursor: pointer;
}

.btn-matrix-drilldown:hover {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
}

/* Segment Comparison Tool */
.segment-compare-selectors {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.compare-selector-box {
  flex: 1;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.compare-selector-box label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-muted);
}

.form-select, .table-search-input, .form-input {
  background: var(--bg-input);
  border: 1px solid var(--border-control);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  outline: none;
}

.form-select:focus, .form-input:focus {
  border-color: var(--accent-cyan);
}

.compare-vs-badge {
  font-weight: 900;
  font-size: 0.95rem;
  color: var(--accent-cyan);
  padding: 4px 10px;
  background: rgba(56, 189, 248, 0.1);
  border-radius: var(--radius-full);
  margin-top: 14px;
}

.segment-compare-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.compare-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.compare-card-title {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-muted);
}

.compare-metric-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-top: 6px;
}

.compare-val-a { color: var(--accent-cyan); font-size: 1.1rem; font-weight: 700; font-family: var(--font-mono); }
.compare-val-b { color: var(--color-purple); font-size: 1.1rem; font-weight: 700; font-family: var(--font-mono); }

.compare-delta-pill {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-top: 4px;
  font-family: var(--font-mono);
}

.delta-danger { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
.delta-success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.delta-neutral { background: rgba(148, 163, 184, 0.15); color: #94a3b8; }

.segments-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 14px;
  margin-top: 12px;
}

.segment-summary-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.seg-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.seg-name {
  font-size: 0.92rem;
  font-weight: 700;
  color: #ffffff;
}

.seg-desc {
  font-size: 0.74rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.seg-metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 10px 0;
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 12px;
}

.seg-metric-box {
  display: flex;
  flex-direction: column;
}

.seg-metric-label {
  font-size: 0.68rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.seg-metric-val {
  font-size: 0.92rem;
  font-weight: 700;
  font-family: var(--font-mono);
  color: #ffffff;
}

.btn-card-drilldown {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-control);
  color: var(--accent-cyan);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  cursor: pointer;
  text-align: center;
}

.btn-card-drilldown:hover {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
}

/* ==============================================================================
   WORKSPACE 4: REVENUE INTELLIGENCE & THRESHOLD SIMULATOR
   ============================================================================== */
.revenue-tiers-breakdown {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 8px 0;
}

.tier-breakdown-row {
  display: grid;
  grid-template-columns: 130px 1fr 160px;
  align-items: center;
  gap: 14px;
}

.tier-name { font-size: 0.84rem; font-weight: 600; }
.tier-rule { font-size: 0.68rem; color: var(--text-muted); display: block; }
.tier-progress-track { background: rgba(255, 255, 255, 0.06); height: 8px; border-radius: 4px; overflow: hidden; }
.tier-progress-fill { height: 100%; border-radius: 4px; }
.fill-danger { background-color: var(--color-danger); }
.fill-warning { background-color: var(--accent-amber); }
.fill-success { background-color: var(--color-success); }
.tier-revenue-amount { font-family: var(--font-mono); font-weight: 700; font-size: 0.88rem; display: block; color: #ffffff; }
.tier-sub-stats { font-size: 0.7rem; color: var(--text-muted); }

.pareto-methodology-note {
  margin-top: 12px;
  font-size: 0.75rem;
  color: var(--text-secondary);
  line-height: 1.45;
  background: rgba(255, 255, 255, 0.02);
  padding: 8px 12px;
  border-left: 3px solid var(--accent-amber);
  border-radius: var(--radius-xs);
}

.simulator-range-slider {
  width: 100%;
  accent-color: var(--accent-cyan);
  cursor: pointer;
  height: 6px;
  background: #1e293b;
  border-radius: 3px;
}

.slider-scale-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
  margin-top: 4px;
}

.simulator-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 14px;
}

@media (max-width: 900px) {
  .simulator-metrics-grid { grid-template-columns: repeat(2, 1fr); }
}

.sim-metric-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.sim-metric-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--text-muted);
}

.sim-metric-num {
  font-size: 1.35rem;
  font-weight: 800;
  margin-top: 4px;
  font-family: var(--font-mono);
  color: #ffffff;
}

.sim-metric-sub {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.simulator-guidance-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  background: rgba(56, 189, 248, 0.06);
  border: 1px solid rgba(56, 189, 248, 0.2);
  padding: 8px 12px;
  border-radius: var(--radius-xs);
  font-size: 0.74rem;
  color: var(--text-secondary);
}

.calc-steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 10px;
}

@media (max-width: 800px) {
  .calc-steps-grid { grid-template-columns: 1fr; }
}

.calc-step-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
}

.step-tag { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; }
.step-math { font-size: 1.35rem; font-weight: 800; font-family: var(--font-mono); color: #ffffff; margin-top: 4px; }
.step-label { font-size: 0.72rem; color: var(--text-muted); margin-top: 2px; }

/* ==============================================================================
   WORKSPACE 5: CUSTOMER EXPLORER
   ============================================================================== */
.explorer-filter-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-input);
  border: 1px solid var(--border-control);
  padding: 0 10px;
  border-radius: var(--radius-sm);
  flex: 1;
  min-width: 240px;
}

.search-svg {
  color: var(--text-muted);
}

.table-search-input {
  background: transparent;
  border: none;
  padding: 6px 0;
  width: 100%;
}

.filter-group-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-unit {
  display: flex;
  align-items: center;
  gap: 4px;
}

.filter-label {
  font-size: 0.72rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.btn-action-primary {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  border: none;
  font-size: 0.78rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-action-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-control);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.78rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.table-legend-strip {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.badge-pill-danger { color: #fb7185; }
.badge-pill-warning { color: var(--accent-amber); }
.badge-pill-success { color: var(--color-success); }
.badge-pill-critical { color: var(--color-purple); }

.table-pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.btn-page-ctrl {
  background: var(--bg-input);
  border: 1px solid var(--border-control);
  color: #ffffff;
  padding: 4px 10px;
  border-radius: var(--radius-xs);
  cursor: pointer;
}

.btn-page-ctrl:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Customer Inspector Slide-Out Drawer */
.customer-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 200;
  display: none;
}

.customer-drawer-backdrop.open { display: block; }

.customer-inspector-drawer {
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  width: 480px;
  max-width: 100vw;
  background: #0d1424;
  border-left: 1px solid var(--border-panel);
  z-index: 210;
  transform: translateX(100%);
  transition: transform var(--transition-normal);
  display: flex;
  flex-direction: column;
}

.customer-inspector-drawer.open {
  transform: translateX(0);
}

.drawer-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.drawer-cust-id {
  font-size: 1.15rem;
  font-weight: 700;
  font-family: var(--font-mono);
}

.btn-close-drawer {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1.2rem;
  cursor: pointer;
}

.drawer-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

/* ==============================================================================
   WORKSPACE 6: PREDICTION LAB & BATCH ENGINE
   ============================================================================== */
.predict-tab-bar {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 18px;
}

.btn-predict-tab {
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  padding: 8px 16px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-fast);
}

.btn-predict-tab:hover {
  color: #ffffff;
}

.btn-predict-tab.active {
  color: var(--accent-cyan);
  border-bottom-color: var(--accent-cyan);
}

.predict-subtab-view {
  display: none;
}

.predict-subtab-view.active {
  display: block;
}

.predict-workspace-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 18px;
  align-items: start;
}

@media (max-width: 1000px) {
  .predict-workspace-grid { grid-template-columns: 1fr; }
}

.form-section-header {
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 14px 0 8px;
}

.section-num-badge {
  width: 18px;
  height: 18px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.68rem;
  color: #ffffff;
}

.form-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.form-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }

@media (max-width: 800px) {
  .form-grid-4, .form-grid-3, .form-grid-2 { grid-template-columns: 1fr; }
}

.form-control-unit {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-control-unit label {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.btn-predict-action {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-sm);
  padding: 10px 20px;
  font-size: 0.88rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
}

.btn-preset-pill {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-control);
  color: var(--text-secondary);
  padding: 3px 8px;
  border-radius: var(--radius-xs);
  font-size: 0.72rem;
  cursor: pointer;
}

.btn-preset-pill:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

/* Batch Prediction Dropzone */
.batch-upload-dropzone {
  border: 2px dashed rgba(56, 189, 248, 0.35);
  border-radius: var(--radius-md);
  padding: 36px 20px;
  text-align: center;
  background: rgba(15, 23, 42, 0.4);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-top: 10px;
}

.batch-upload-dropzone:hover, .batch-upload-dropzone.dragover {
  border-color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.08);
}

.dropzone-icon { color: var(--accent-cyan); margin-bottom: 8px; }
.dropzone-content h4 { font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
.dropzone-content p { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 12px; }

.btn-upload-browse {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
  padding: 6px 16px;
  border-radius: var(--radius-sm);
  border: none;
  font-size: 0.78rem;
  cursor: pointer;
}

.hidden-file-input { display: none; }

.batch-validation-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  background: rgba(244, 63, 94, 0.12);
  border: 1px solid rgba(244, 63, 94, 0.35);
  color: #fca5a5;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
}

.batch-loading-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  padding: 10px 14px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  color: var(--accent-cyan);
}

.batch-summary-kpis {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-top: 14px;
}

@media (max-width: 900px) {
  .batch-summary-kpis { grid-template-columns: repeat(2, 1fr); }
}

.batch-kpi-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
}

.batch-kpi-label { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; }
.batch-kpi-num { font-size: 1.3rem; font-weight: 800; font-family: var(--font-mono); margin-top: 2px; color: #ffffff; }

.btn-batch-download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--color-success);
  color: #ffffff;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 4px;
}

/* Confusion Matrix Diagnostics */
.confusion-matrix-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.cm-quadrant {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
}

.cm-quad-label { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; }
.cm-quad-count { font-size: 1.5rem; font-weight: 800; font-family: var(--font-mono); color: #ffffff; margin-top: 2px; }
.cm-quad-rate { font-size: 0.75rem; color: var(--accent-cyan); font-family: var(--font-mono); }
.cm-quad-meaning { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

.cm-derived-metrics-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 12px;
}

@media (max-width: 800px) {
  .cm-derived-metrics-list { grid-template-columns: repeat(2, 1fr); }
}

.cm-metric-pill {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
}

.cm-pill-title { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; }
.cm-pill-val { font-size: 1.1rem; font-weight: 700; font-family: var(--font-mono); color: #ffffff; }

/* Utilities */
.hidden { display: none !important; }
"""

with open(r"website\static\style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Regenerated website/static/style.css with Taste Skill Enterprise Architecture.")
