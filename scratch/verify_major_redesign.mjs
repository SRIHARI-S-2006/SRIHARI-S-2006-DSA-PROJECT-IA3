import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';
import fs from 'fs';
import path from 'path';

async function verifyMajorRedesign() {
  console.log("=== Launching Headless CDP Browser for Major Redesign Verification ===");
  const browser = await Browser.launch({ width: 1440, height: 960 });
  const page = await browser.newPage({ width: 1440, height: 960 });

  const consoleErrors = [];
  page.browser.on(page.sessionId, 'Runtime.consoleAPICalled', (params) => {
    if (params.type === 'error') {
      const msg = params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' ');
      consoleErrors.push(msg);
      console.error(`   [Browser Console Error]:`, msg);
    }
  });

  try {
    console.log("\n1. Navigating to CCPRA Web Application at http://127.0.0.1:5000/ ...");
    await page.goto('http://127.0.0.1:5000/', { settleMs: 2500 });
    await sleep(1500);

    // Verify Title & Subtitle
    const headerInfo = await page.eval(() => ({
      title: document.querySelector('.header-title h1')?.textContent.trim(),
      subtitle: document.querySelector('.header-title p')?.textContent.trim(),
      navItems: Array.from(document.querySelectorAll('.nav-item')).map(el => ({
        section: el.getAttribute('data-section'),
        text: el.querySelector('span')?.textContent.trim()
      }))
    }));
    console.log("Navigation & Header Info:", headerInfo);

    // -------------------------------------------------------------
    // WORKSPACE 1: Executive Intelligence (overview)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 1: Executive Intelligence ---");
    await page.eval(() => window.navigateToSection('overview'));
    await sleep(1200);

    const execCheck = await page.eval(() => {
      const gauge = document.getElementById('portfolioHealthGaugeChart');
      const funnel = document.getElementById('retention-funnel-container');
      const matrix = document.getElementById('service-contract-matrix-container');
      const funnelStages = funnel ? funnel.querySelectorAll('.funnel-stage-card').length : 0;
      const matrixCells = matrix ? matrix.querySelectorAll('.matrix-2d-cell').length : 0;
      return {
        hasGauge: !!gauge && gauge.tagName.toLowerCase() === 'canvas',
        hasFunnel: !!funnel && funnelStages >= 5,
        funnelStageCount: funnelStages,
        hasMatrix: !!matrix && matrixCells >= 9,
        matrixCellCount: matrixCells
      };
    });
    console.log("Executive Intelligence Elements:", execCheck);
    if (!execCheck.hasGauge || !execCheck.hasFunnel || !execCheck.hasMatrix) {
      throw new Error(`Workspace 1 Executive Intelligence failed check: ${JSON.stringify(execCheck)}`);
    }

    // -------------------------------------------------------------
    // WORKSPACE 2: Customer Behavior Lab (analytics)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 2: Customer Behavior Lab ---");
    await page.eval(() => window.navigateToSection('analytics'));
    await sleep(1200);

    const behaviorCheck = await page.eval(() => {
      const corr = document.getElementById('correlation-matrix-container');
      const corrCells = corr ? corr.querySelectorAll('.corr-cell').length : 0;
      const lifecycle = document.getElementById('lifecycleRetentionChart');
      const box = document.getElementById('distributionBoxPlotChart');
      const scatter = document.getElementById('scatterTenureChargesChart');
      return {
        hasCorrMatrix: !!corr && corrCells >= 49,
        corrCellCount: corrCells,
        hasLifecycle: !!lifecycle && lifecycle.tagName.toLowerCase() === 'canvas',
        hasBoxPlot: !!box && box.tagName.toLowerCase() === 'canvas',
        hasScatter: !!scatter && scatter.tagName.toLowerCase() === 'canvas'
      };
    });
    console.log("Customer Behavior Lab Elements:", behaviorCheck);
    if (!behaviorCheck.hasCorrMatrix || !behaviorCheck.hasLifecycle || !behaviorCheck.hasBoxPlot || !behaviorCheck.hasScatter) {
      throw new Error(`Workspace 2 Customer Behavior Lab failed check: ${JSON.stringify(behaviorCheck)}`);
    }

    // -------------------------------------------------------------
    // WORKSPACE 3: Market Intelligence (segments)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 3: Market Intelligence ---");
    await page.eval(() => window.navigateToSection('segments'));
    await sleep(1200);

    const marketCheck = await page.eval(() => {
      const traiShare = document.getElementById('traiMarketShareChart');
      const traiMnp = document.getElementById('traiMnpCircleChart');
      const fccGrievance = document.getElementById('fccMethodIssueChart');
      const mendeleyCard = document.getElementById('mendeley-research-panel');
      return {
        hasTraiShare: !!traiShare && traiShare.tagName.toLowerCase() === 'canvas',
        hasTraiMnp: !!traiMnp && traiMnp.tagName.toLowerCase() === 'canvas',
        hasFccGrievance: !!fccGrievance && fccGrievance.tagName.toLowerCase() === 'canvas',
        hasMendeleyCard: !!mendeleyCard && mendeleyCard.innerText.includes('Mendeley')
      };
    });
    console.log("Market Intelligence Elements:", marketCheck);
    if (!marketCheck.hasTraiShare || !marketCheck.hasTraiMnp || !marketCheck.hasFccGrievance || !marketCheck.hasMendeleyCard) {
      throw new Error(`Workspace 3 Market Intelligence failed check: ${JSON.stringify(marketCheck)}`);
    }

    // -------------------------------------------------------------
    // WORKSPACE 4: Revenue Strategy (revenue)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 4: Revenue Strategy ---");
    await page.eval(() => window.navigateToSection('revenue'));
    await sleep(1200);

    const revCheck = await page.eval(() => {
      const treemap = document.getElementById('financial-treemap-container');
      const treemapNodes = treemap ? treemap.querySelectorAll('.treemap-tile').length : 0;
      const pareto = document.getElementById('revenueParetoChart');
      const simPrecision = document.getElementById('sim-precision')?.textContent.trim();
      const simRecall = document.getElementById('sim-recall')?.textContent.trim();
      return {
        hasTreemap: !!treemap && treemapNodes >= 3,
        treemapNodeCount: treemapNodes,
        hasPareto: !!pareto && pareto.tagName.toLowerCase() === 'canvas',
        simPrecision,
        simRecall
      };
    });
    console.log("Revenue Strategy Elements:", revCheck);
    if (!revCheck.hasTreemap || !revCheck.hasPareto || !revCheck.simPrecision) {
      throw new Error(`Workspace 4 Revenue Strategy failed check: ${JSON.stringify(revCheck)}`);
    }

    // -------------------------------------------------------------
    // WORKSPACE 5: Model Science Lab (predict)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 5: Model Science Lab ---");
    await page.eval(() => {
      window.navigateToSection('predict');
      const evalTab = document.querySelector('.btn-predict-tab[data-subtab="model-evaluation"]');
      if (evalTab) evalTab.click();
    });
    await sleep(1500);

    const modelCheck = await page.eval(() => {
      const uciChart = document.getElementById('uciBenchmarkChart');
      const gains = document.getElementById('cumulativeGainsChart');
      const cal = document.getElementById('calibrationCurveChart');
      const pr = document.getElementById('precisionRecallChart');
      return {
        hasUciChart: !!uciChart && uciChart.tagName.toLowerCase() === 'canvas',
        hasGains: !!gains && gains.tagName.toLowerCase() === 'canvas',
        hasCalibration: !!cal && cal.tagName.toLowerCase() === 'canvas',
        hasPRCurve: !!pr && pr.tagName.toLowerCase() === 'canvas'
      };
    });
    console.log("Model Science Lab Elements:", modelCheck);
    if (!modelCheck.hasUciChart || !modelCheck.hasGains || !modelCheck.hasCalibration || !modelCheck.hasPRCurve) {
      throw new Error(`Workspace 5 Model Science Lab failed check: ${JSON.stringify(modelCheck)}`);
    }

    // -------------------------------------------------------------
    // WORKSPACE 6: Customer Operations (explorer)
    // -------------------------------------------------------------
    console.log("\n--- Checking Workspace 6: Customer Operations ---");
    await page.eval(() => window.navigateToSection('explorer'));
    await sleep(1200);

    const opsCheck = await page.eval(() => {
      const prov = document.getElementById('provenance-cards-container');
      const provCards = prov ? prov.querySelectorAll('.provenance-card').length : 0;
      const tableRows = document.querySelectorAll('#customers-table-body tr').length;
      return {
        hasProvenanceRegistry: !!prov && provCards >= 4,
        provenanceCardCount: provCards,
        tableRowCount: tableRows
      };
    });
    console.log("Customer Operations Elements:", opsCheck);
    if (!opsCheck.hasProvenanceRegistry || opsCheck.tableRowCount === 0) {
      throw new Error(`Workspace 6 Customer Operations failed check: ${JSON.stringify(opsCheck)}`);
    }

    // Check Console Errors
    if (consoleErrors.length > 0) {
      console.warn(`WARNING: Encountered ${consoleErrors.length} console errors during browser session:`, consoleErrors);
    } else {
      console.log("\nZERO BROWSER CONSOLE ERRORS DETECTED!");
    }

    // Capture visual artifacts of the workspaces
    const artifactsDir = path.resolve('scratch/workspaces_redesign');
    if (!fs.existsSync(artifactsDir)) {
      fs.mkdirSync(artifactsDir, { recursive: true });
    }

    console.log("\nCapturing visual screenshots of all 6 redesigned workspaces...");
    for (const sec of ['overview', 'analytics', 'segments', 'revenue', 'predict', 'explorer']) {
      await page.eval((s) => window.navigateToSection(s), sec);
      await sleep(1000);
      const screenshotBuf = await page.screenshot({ format: 'png' });
      fs.writeFileSync(path.join(artifactsDir, `${sec}.png`), screenshotBuf);
      console.log(`Saved screenshot: scratch/workspaces_redesign/${sec}.png`);
    }

    console.log("\n=======================================================");
    console.log("ALL 6 WORKSPACES FULLY VERIFIED IN HEADLESS BROWSER!");
    console.log("=======================================================");

  } finally {
    await browser.close();
  }
}

verifyMajorRedesign().catch(err => {
  console.error("Redesign Verification failed:", err);
  process.exit(1);
});
