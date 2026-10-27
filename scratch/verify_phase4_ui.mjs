import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function verifyUI() {
  console.log("Launching headless browser to verify Phase 3/4 UI elements...");
  const browser = await Browser.launch({ width: 1440, height: 900 });
  const page = await browser.newPage({ width: 1440, height: 900 });
  try {
    page.browser.on(page.sessionId, 'Runtime.consoleAPICalled', (params) => {
      if (params.type === 'error') {
        console.error(`   [Browser Console Error]:`, params.args.map(a => a.value || a.description).join(' '));
      }
    });

    console.log("Navigating to http://127.0.0.1:5000/ ...");
    await page.goto('http://127.0.0.1:5000/', { settleMs: 2000 });

    // 1. Churn Analytics Workspace
    console.log("Testing Churn Analytics workspace...");
    await page.eval(() => window.navigateToSection('analytics'));
    await sleep(1500);

    const analyticsCheck = await page.eval(() => {
      const lc = document.getElementById('lifecycleRetentionChart');
      const box = document.getElementById('distributionBoxPlotChart');
      return {
        hasLifecycle: !!lc && lc.tagName.toLowerCase() === 'canvas',
        hasBoxPlot: !!box && box.tagName.toLowerCase() === 'canvas',
        boxMetricActive: document.getElementById('btn-box-charges')?.classList.contains('active')
      };
    });
    console.log("Analytics Charts Check:", analyticsCheck);
    if (!analyticsCheck.hasLifecycle || !analyticsCheck.hasBoxPlot) {
      throw new Error("Lifecycle retention or box plot canvas missing in Analytics workspace!");
    }

    // Toggle Box Plot Metric
    await page.eval(() => window.switchBoxMetric('tenure'));
    await sleep(400);
    const tenureActive = await page.eval(() => document.getElementById('btn-box-tenure')?.classList.contains('active'));
    console.log("Box Plot Tenure Toggle Active:", tenureActive);

    // 2. Customer Segments Workspace (Mendeley Card)
    console.log("Testing Customer Segments & Mendeley Card...");
    await page.eval(() => window.navigateToSection('segments'));
    await sleep(1000);
    const mendeleyCheck = await page.eval(() => {
      const text = document.body.innerText;
      return {
        hasMendeleyTitle: text.includes('Dataset Expansion & Cross-Market External Validation Research'),
        hasIndianTelcoCount: text.includes('2,026'),
        hasAnomaliesNotice: text.includes('59 Neg Data, 52 Neg Calls, 62 Neg SMS')
      };
    });
    console.log("Mendeley Comparison Card Check:", mendeleyCheck);
    if (!mendeleyCheck.hasMendeleyTitle || !mendeleyCheck.hasIndianTelcoCount) {
      throw new Error("Mendeley comparative card missing in Segments workspace!");
    }

    // 3. Prediction Lab -> Model Evaluation Diagnostics
    console.log("Testing Prediction Lab & Evaluation Diagnostics...");
    await page.eval(() => {
      window.navigateToSection('predict');
      const btn = document.querySelector('.btn-predict-tab[data-subtab="model-evaluation"]');
      if (btn) btn.click();
    });
    await sleep(1500);

    const evalCheck = await page.eval(() => {
      const gains = document.getElementById('cumulativeGainsChart');
      const cal = document.getElementById('calibrationCurveChart');
      const pr = document.getElementById('precisionRecallChart');
      return {
        hasCumulativeGains: !!gains && gains.tagName.toLowerCase() === 'canvas',
        hasCalibration: !!cal && cal.tagName.toLowerCase() === 'canvas',
        hasPrecisionRecall: !!pr && pr.tagName.toLowerCase() === 'canvas'
      };
    });
    console.log("Evaluation Diagnostic Charts Check:", evalCheck);
    if (!evalCheck.hasCumulativeGains || !evalCheck.hasCalibration || !evalCheck.hasPrecisionRecall) {
      throw new Error("Diagnostic charts (Gains, Calibration, or PR curve) missing in Model Evaluation subtab!");
    }

    // 4. Threshold Simulator in Revenue Workspace
    console.log("Testing Threshold Simulator in Revenue Workspace...");
    await page.eval(() => window.navigateToSection('revenue'));
    await sleep(1000);

    const simCheck = await page.eval(() => {
      const p = document.getElementById('sim-precision')?.textContent;
      const r = document.getElementById('sim-recall')?.textContent;
      return { precision: p, recall: r };
    });
    console.log("Threshold Simulator PR Linkage Check:", simCheck);
    if (!simCheck.precision || !simCheck.recall) {
      throw new Error("Precision/Recall cards missing in Threshold Simulator!");
    }

    console.log("\nALL BROWSER HEADLESS UI INSPECTION CHECKS PASSED WITH FLYING COLORS!");
  } finally {
    await browser.close();
  }
}

verifyUI().catch(err => {
  console.error("UI Verification failed:", err);
  process.exit(1);
});
