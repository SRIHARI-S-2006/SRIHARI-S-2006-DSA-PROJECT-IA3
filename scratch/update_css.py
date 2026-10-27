css_path = r"website\static\style.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

new_styles = """
/* ==============================================================================
   ADVANCED VISUALIZATION UPGRADES & NEW FEATURES
   ============================================================================== */
.chart-box-medium {
  height: 320px;
  position: relative;
  width: 100%;
}

/* Heatmap Component */
.heatmap-container {
  display: grid;
  grid-template-columns: 140px repeat(3, 1fr);
  gap: 8px;
  margin-top: 12px;
}

.heatmap-header-col {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 8px;
  text-align: center;
  background: rgba(15, 23, 42, 0.4);
  border-radius: var(--radius-xs);
}

.heatmap-header-row {
  font-size: 0.8rem;
  font-weight: 600;
  color: #ffffff;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: rgba(15, 23, 42, 0.3);
  border-radius: var(--radius-xs);
}

.heatmap-cell {
  border-radius: var(--radius-sm);
  padding: 14px 10px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
}

.heatmap-cell:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45);
  filter: brightness(1.15);
  border-color: rgba(56, 189, 248, 0.5);
}

.heatmap-rate {
  font-size: 1.15rem;
  font-weight: 800;
  font-family: var(--font-mono);
  letter-spacing: -0.02em;
}

.heatmap-count {
  font-size: 0.72rem;
  color: #cbd5e1;
}

.heatmap-legend-bar {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 14px;
  padding-top: 10px;
  border-top: 1px solid var(--border-subtle);
  flex-wrap: wrap;
}

.heatmap-legend-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
}

.heatmap-gradient-swatch {
  width: 140px;
  height: 10px;
  border-radius: 4px;
  background: linear-gradient(to right, rgba(16, 185, 129, 0.3), rgba(245, 158, 11, 0.5), rgba(239, 68, 68, 0.7), rgba(225, 29, 72, 0.95));
}

.heatmap-legend-ticks {
  display: flex;
  justify-content: space-between;
  flex: 1;
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* Segment Comparison Tool */
.segment-compare-selectors {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.compare-selector-box {
  flex: 1;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.compare-selector-box label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
}

.compare-vs-badge {
  font-weight: 900;
  font-size: 1.1rem;
  color: var(--accent-cyan);
  padding: 6px 12px;
  background: rgba(56, 189, 248, 0.1);
  border-radius: var(--radius-full);
  border: 1px solid rgba(56, 189, 248, 0.25);
  margin-top: 18px;
}

.segment-compare-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
}

.compare-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.compare-card-title {
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
}

.compare-metric-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.compare-val-a, .compare-val-b {
  font-size: 1rem;
  font-weight: 700;
}

.compare-val-a {
  color: #38bdf8;
}

.compare-val-b {
  color: #c084fc;
}

.compare-delta-pill {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: var(--radius-xs);
  display: inline-block;
  align-self: flex-start;
  margin-top: 4px;
}

.delta-danger {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.delta-success {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.delta-neutral {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.3);
}

/* Pareto Methodology Box */
.pareto-methodology-note {
  margin-top: 14px;
  font-size: 0.76rem;
  color: var(--text-secondary);
  line-height: 1.5;
  background: rgba(15, 23, 42, 0.7);
  padding: 10px 14px;
  border-left: 3px solid var(--accent-amber);
  border-radius: var(--radius-xs);
}

/* Threshold Simulator */
.threshold-simulator-container {
  padding: 4px 0;
}

.simulator-slider-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slider-label-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
}

.slider-value-badge {
  background: var(--accent-cyan);
  color: #040810;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-weight: 800;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.simulator-range-slider {
  width: 100%;
  accent-color: var(--accent-cyan);
  cursor: pointer;
  height: 6px;
  border-radius: 3px;
  background: #1e293b;
}

.slider-scale-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.simulator-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.sim-metric-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.sim-metric-label {
  font-size: 0.74rem;
  color: var(--text-muted);
}

.sim-metric-num {
  font-size: 1.35rem;
  font-weight: 800;
  margin-top: 4px;
  font-family: var(--font-mono);
}

.sim-metric-sub {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.simulator-guidance-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 14px;
  background: rgba(56, 189, 248, 0.08);
  border: 1px solid rgba(56, 189, 248, 0.25);
  padding: 9px 14px;
  border-radius: var(--radius-xs);
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Batch Prediction Dropzone */
.batch-upload-dropzone {
  border: 2px dashed rgba(56, 189, 248, 0.4);
  border-radius: var(--radius-md);
  padding: 36px 20px;
  text-align: center;
  background: rgba(15, 23, 42, 0.45);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 12px;
}

.batch-upload-dropzone:hover,
.batch-upload-dropzone.dragover {
  border-color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.1);
  box-shadow: 0 0 16px rgba(56, 189, 248, 0.15);
}

.dropzone-icon {
  color: var(--accent-cyan);
  margin-bottom: 8px;
}

.dropzone-content h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 4px;
}

.dropzone-content p {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 14px;
}

.btn-upload-browse {
  background: var(--accent-cyan);
  color: #040810;
  font-weight: 700;
  padding: 7px 18px;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  font-size: 0.82rem;
  transition: transform 0.15s ease;
}

.btn-upload-browse:hover {
  transform: scale(1.03);
}

.hidden-file-input {
  display: none;
}

.batch-validation-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 14px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #fca5a5;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
}

.batch-loading-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 14px;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--accent-cyan);
}

.batch-summary-kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.batch-kpi-card {
  background: var(--bg-panel-elevated);
  border: 1px solid var(--border-panel);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.batch-kpi-label {
  font-size: 0.74rem;
  color: var(--text-muted);
}

.batch-kpi-num {
  font-size: 1.35rem;
  font-weight: 800;
  margin-top: 4px;
  font-family: var(--font-mono);
}

.btn-batch-download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: #10b981;
  color: #ffffff;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 600;
  transition: background 0.18s;
  margin-top: 6px;
}

.btn-batch-download:hover {
  background: #059669;
}
"""

if "/* ADVANCED VISUALIZATION UPGRADES & NEW FEATURES */" not in css:
    css = css + "\n" + new_styles
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Added advanced styles to style.css.")
else:
    print("Styles already present.")
