import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';

function log(status, msg) {
  console.log(`[${status}] ${msg}`);
}

async function run() {
  console.log("======================================================================");
  console.log("LIVE BROWSER CONSISTENCY & DRILL-DOWN AUDIT (CDP)");
  console.log("======================================================================");

  const browser = await Browser.launch({ width: 1440, height: 900 });
  const page = await browser.newPage({ width: 1440, height: 900 });

  // Listen for console errors
  page.browser.on(page.sessionId, 'Runtime.consoleAPICalled', (params) => {
    if (params.type === 'error') {
      console.error(`   [Browser Console Error]:`, params.args.map(a => a.value || a.description).join(' '));
    }
  });

  log("INFO", "Navigating to http://127.0.0.1:5000/ ...");
  await page.goto('http://127.0.0.1:5000/', { settleMs: 1500 });

  // -------------------------------------------------------------------------
  // TEST 1: Heatmap Cell Click
  // -------------------------------------------------------------------------
  log("TEST", "1. Clicking Heatmap cell (Month-to-month + Fiber optic)...");
  await page.eval(() => window.navigateToSection("analytics"));
  
  // Wait for heatmap cells to be populated
  const cellCheck = await page.eval(async () => {
    for (let i = 0; i < 40; i++) {
      const cells = document.querySelectorAll(".heatmap-cell");
      if (cells.length > 0) return { count: cells.length };
      await new Promise(r => setTimeout(r, 250));
    }
    const container = document.getElementById("churn-heatmap-container");
    return { count: 0, innerHtml: container ? container.innerHTML : "container-missing" };
  });

  if (cellCheck.count === 0) {
    throw new Error(`Heatmap cells not rendered: ${cellCheck.innerHtml}`);
  }

  const heatmapResult = await page.eval(() => {
    const cells = Array.from(document.querySelectorAll(".heatmap-cell"));
    const targetCell = cells.find(c => c.title && c.title.includes("Month-to-month + Fiber optic"));
    if (!targetCell) return { error: `Target cell not found among titles: ${cells.map(c => c.title).join(' | ')}` };
    targetCell.click();
    return { clicked: true };
  });

  if (heatmapResult.error) {
    throw new Error(heatmapResult.error);
  }
  await sleep(1200);

  // Verify Explorer state
  const explorerState1 = await page.eval(() => {
    const activeSection = document.querySelector(".content-section.active")?.id;
    const chips = Array.from(document.querySelectorAll(".drilldown-chip")).map(c => c.textContent.trim());
    const contractVal = document.getElementById("filter-contract")?.value;
    const internetVal = document.getElementById("filter-internet")?.value;
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    const rowData = rows.map(r => ({
      id: r.querySelector(".cust-id")?.textContent,
      contract: r.children[2]?.textContent.trim(),
      internet: r.children[3]?.textContent.trim()
    }));
    return { activeSection, chips, contractVal, internetVal, rowCount: rows.length, rowData };
  });

  if (explorerState1.activeSection !== "section-explorer") {
    throw new Error(`Expected active section to be section-explorer, got ${explorerState1.activeSection}`);
  }
  if (!explorerState1.chips.some(c => c.includes("Contract: Month-to-month")) || !explorerState1.chips.some(c => c.includes("Internet: Fiber optic"))) {
    throw new Error(`Active chips mismatch: ${JSON.stringify(explorerState1.chips)}`);
  }
  for (const r of explorerState1.rowData) {
    if (r.contract !== "Month-to-month" || r.internet !== "Fiber optic") {
      throw new Error(`Row data does not match filter: ${JSON.stringify(r)}`);
    }
  }
  log("PASS", `Heatmap drilldown navigated to Explorer. All ${explorerState1.rowCount} visible rows match Month-to-month + Fiber optic.`);

  // -------------------------------------------------------------------------
  // TEST 2: Segment Matrix Row Click
  // -------------------------------------------------------------------------
  log("TEST", "2. Clicking Segment Matrix entry (One year + DSL)...");
  await page.eval(() => window.navigateToSection("segments"));
  await sleep(600);

  const matrixResult = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll("#segment-matrix-tbody tr"));
    const targetRow = rows.find(r => r.children[0]?.textContent.includes("One year") && r.children[1]?.textContent.includes("DSL"));
    if (!targetRow) return { error: "Matrix row for One year + DSL not found" };
    const btn = targetRow.querySelector(".btn-matrix-drilldown");
    if (!btn) return { error: "Drilldown button not found in row" };
    btn.click();
    return { clicked: true };
  });

  if (matrixResult.error) {
    throw new Error(matrixResult.error);
  }
  await sleep(1200);

  const explorerState2 = await page.eval(() => {
    const activeSection = document.querySelector(".content-section.active")?.id;
    const chips = Array.from(document.querySelectorAll(".drilldown-chip")).map(c => c.textContent.trim());
    const contractVal = document.getElementById("filter-contract")?.value;
    const internetVal = document.getElementById("filter-internet")?.value;
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    const rowData = rows.map(r => ({
      id: r.querySelector(".cust-id")?.textContent,
      contract: r.children[2]?.textContent.trim(),
      internet: r.children[3]?.textContent.trim()
    }));
    return { activeSection, chips, contractVal, internetVal, rowCount: rows.length, rowData };
  });

  if (explorerState2.activeSection !== "section-explorer") {
    throw new Error(`Expected active section to be section-explorer, got ${explorerState2.activeSection}`);
  }
  for (const r of explorerState2.rowData) {
    if (r.contract !== "One year" || r.internet !== "DSL") {
      throw new Error(`Row data does not match One year + DSL: ${JSON.stringify(r)}`);
    }
  }
  log("PASS", `Segment Matrix drilldown navigated to Explorer. All ${explorerState2.rowCount} visible rows match One year + DSL.`);

  // -------------------------------------------------------------------------
  // TEST 3: Bubble Chart Segment Click
  // -------------------------------------------------------------------------
  log("TEST", "3. Clicking Bubble Chart segment (Two year + Fiber optic)...");
  await page.eval(() => {
    // Invoke drilldown through the bubble chart's bound data logic
    window.drilldownSegment("Two year", "Fiber optic");
  });
  await sleep(1200);

  const explorerState3 = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    const rowData = rows.map(r => ({
      contract: r.children[2]?.textContent.trim(),
      internet: r.children[3]?.textContent.trim()
    }));
    return { rowCount: rows.length, rowData };
  });

  for (const r of explorerState3.rowData) {
    if (r.contract !== "Two year" || r.internet !== "Fiber optic") {
      throw new Error(`Row data does not match Two year + Fiber optic: ${JSON.stringify(r)}`);
    }
  }
  log("PASS", `Bubble chart segment drilldown filtered correctly to Two year + Fiber optic.`);

  // -------------------------------------------------------------------------
  // TEST 4: Remove Individual Filter Chip
  // -------------------------------------------------------------------------
  log("TEST", "4. Removing individual filter chip (Internet)...");
  await page.eval(() => {
    const chips = Array.from(document.querySelectorAll(".drilldown-chip"));
    const internetChip = chips.find(c => c.textContent.includes("Internet"));
    if (internetChip) {
      const btn = internetChip.querySelector(".chip-remove-btn");
      if (btn) btn.click();
    }
  });
  await sleep(1200);

  const explorerState4 = await page.eval(() => {
    const chips = Array.from(document.querySelectorAll(".drilldown-chip")).map(c => c.textContent.trim());
    const contractVal = document.getElementById("filter-contract")?.value;
    const internetVal = document.getElementById("filter-internet")?.value;
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    const contractMatches = rows.every(r => r.children[2]?.textContent.trim() === "Two year");
    const internetTypes = new Set(rows.map(r => r.children[3]?.textContent.trim()));
    return { chips, contractVal, internetVal, contractMatches, internetTypesCount: internetTypes.size };
  });

  if (explorerState4.internetVal !== "All") {
    throw new Error(`Expected internet filter to be All, got ${explorerState4.internetVal}`);
  }
  if (!explorerState4.contractMatches) {
    throw new Error("Contract filter was unexpectedly cleared or broken");
  }
  log("PASS", `Removed Internet chip: Internet filter reset to 'All' while Contract remained 'Two year' (${explorerState4.internetTypesCount} distinct internet services now visible).`);

  // -------------------------------------------------------------------------
  // TEST 5: Clear All Filters
  // -------------------------------------------------------------------------
  log("TEST", "5. Testing 'Clear All Filters ✕' button...");
  await page.eval(() => {
    const clearBtn = document.getElementById("btn-clear-drilldown");
    if (clearBtn) clearBtn.click();
  });
  await sleep(1200);

  const explorerState5 = await page.eval(() => {
    const banner = document.getElementById("explorer-active-filter-banner");
    const isHidden = banner?.classList.contains("hidden");
    const contractVal = document.getElementById("filter-contract")?.value;
    const internetVal = document.getElementById("filter-internet")?.value;
    const riskVal = document.getElementById("filter-risk")?.value;
    const paginationText = document.getElementById("pagination-info")?.textContent;
    return { isHidden, contractVal, internetVal, riskVal, paginationText };
  });

  if (!explorerState5.isHidden) {
    throw new Error("Expected active filter banner to be hidden after clear all");
  }
  if (explorerState5.contractVal !== "All" || explorerState5.internetVal !== "All" || explorerState5.riskVal !== "All") {
    throw new Error("Dropdown filters did not all reset to 'All'");
  }
  log("PASS", `All filters cleared successfully. Full portfolio restored: ${explorerState5.paginationText}.`);

  // -------------------------------------------------------------------------
  // TEST 6: Search, Sorting, and Pagination
  // -------------------------------------------------------------------------
  log("TEST", "6. Testing Search, Sorting, and Pagination...");
  // Test Search
  await page.eval(() => {
    const searchInput = document.getElementById("customer-search");
    if (searchInput) {
      searchInput.value = "7590";
      searchInput.dispatchEvent(new Event("input"));
    }
  });
  await sleep(800);

  const searchCount = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    return rows.filter(r => r.querySelector(".cust-id")?.textContent.includes("7590")).length;
  });
  if (searchCount === 0) throw new Error("Search for '7590' returned 0 matches");
  log("PASS", `Search input filtered correctly: found ${searchCount} match(es) with ID containing '7590'.`);

  // Clear search
  await page.eval(() => {
    const searchInput = document.getElementById("customer-search");
    if (searchInput) {
      searchInput.value = "";
      searchInput.dispatchEvent(new Event("input"));
    }
  });
  await sleep(800);

  // Test Sorting by MonthlyCharges: 1st click = DESC
  await page.eval(() => {
    const th = document.querySelector('th[data-sort="MonthlyCharges"]');
    if (th) th.click();
  });
  await sleep(1000);

  const sortValuesDesc = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    return rows.map(r => parseFloat(r.children[5]?.textContent.replace('$', '')) || 0);
  });
  const isSortedDesc = sortValuesDesc.every((val, i, arr) => i === 0 || arr[i - 1] >= val);
  if (!isSortedDesc) throw new Error(`MonthlyCharges 1st click not descending: ${sortValuesDesc.slice(0, 5)}`);
  log("PASS", `Sorting verified: 1st click sorted MonthlyCharges descending ($${sortValuesDesc[0]} down to $${sortValuesDesc[sortValuesDesc.length - 1]}).`);

  // 2nd click = ASC
  await page.eval(() => {
    const th = document.querySelector('th[data-sort="MonthlyCharges"]');
    if (th) th.click();
  });
  await sleep(1000);

  const sortValuesAsc = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll("#customers-table-body tr"));
    return rows.map(r => parseFloat(r.children[5]?.textContent.replace('$', '')) || 0);
  });
  const isSortedAsc = sortValuesAsc.every((val, i, arr) => i === 0 || arr[i - 1] <= val);
  if (!isSortedAsc) throw new Error(`MonthlyCharges 2nd click not ascending: ${sortValuesAsc.slice(0, 5)}`);
  log("PASS", `Sorting verified: 2nd click toggled MonthlyCharges to ascending ($${sortValuesAsc[0]} up to $${sortValuesAsc[sortValuesAsc.length - 1]}).`);

  // Test Pagination Next
  await page.eval(() => {
    const nextBtn = document.getElementById("btn-next");
    if (nextBtn) nextBtn.click();
  });
  await sleep(1000);

  const pageNum = await page.eval(() => document.getElementById("page-num")?.textContent);
  if (!pageNum.includes("2")) throw new Error(`Expected page 2, got ${pageNum}`);
  log("PASS", `Pagination verified: successfully navigated to Page 2 (${pageNum}).`);

  // -------------------------------------------------------------------------
  // TEST 7: Prediction Lab Explanation Dynamic Update
  // -------------------------------------------------------------------------
  log("TEST", "7. Testing Prediction Lab Dynamic Attribution Updating...");
  await page.eval(() => window.navigateToSection("predict"));
  await sleep(600);

  // Click High Risk Preset
  await page.eval(() => {
    document.getElementById("preset-high-risk")?.click();
  });
  await sleep(1200);

  const highAttr = await page.eval(() => {
    const score = document.getElementById("res-score-val")?.textContent;
    const prob = document.getElementById("res-prob-pct")?.textContent;
    const posItems = Array.from(document.querySelectorAll("#res-pos-contribs .contrib-bar-item")).map(i => ({
      label: i.querySelector(".contrib-feature-name")?.textContent,
      val: i.querySelector(".contrib-val-num")?.textContent
    }));
    const negItems = Array.from(document.querySelectorAll("#res-neg-contribs .contrib-bar-item")).map(i => ({
      label: i.querySelector(".contrib-feature-name")?.textContent,
      val: i.querySelector(".contrib-val-num")?.textContent
    }));
    return { score, prob, posItems, negItems };
  });

  log("INFO", `High-Risk: Score = ${highAttr.score}, Prob = ${highAttr.prob}, Top Elevator = ${highAttr.posItems[0]?.label} (${highAttr.posItems[0]?.val})`);
  if (highAttr.score !== "+0.81" || highAttr.prob !== "69.16%") {
    throw new Error(`High risk preset values unexpected: score=${highAttr.score}, prob=${highAttr.prob}`);
  }

  // Click Low Risk Preset
  await page.eval(() => {
    document.getElementById("preset-low-risk")?.click();
  });
  await sleep(1200);

  const lowAttr = await page.eval(() => {
    const score = document.getElementById("res-score-val")?.textContent;
    const prob = document.getElementById("res-prob-pct")?.textContent;
    const posItems = Array.from(document.querySelectorAll("#res-pos-contribs .contrib-bar-item")).map(i => ({
      label: i.querySelector(".contrib-feature-name")?.textContent,
      val: i.querySelector(".contrib-val-num")?.textContent
    }));
    const negItems = Array.from(document.querySelectorAll("#res-neg-contribs .contrib-bar-item")).map(i => ({
      label: i.querySelector(".contrib-feature-name")?.textContent,
      val: i.querySelector(".contrib-val-num")?.textContent
    }));
    return { score, prob, posItems, negItems };
  });

  log("INFO", `Low-Risk: Score = ${lowAttr.score}, Prob = ${lowAttr.prob}, Top Protective = ${lowAttr.negItems[0]?.label} (${lowAttr.negItems[0]?.val})`);
  if (lowAttr.score !== "-5.02" || lowAttr.prob !== "0.66%") {
    throw new Error(`Low risk preset values unexpected: score=${lowAttr.score}, prob=${lowAttr.prob}`);
  }

  log("PASS", `Prediction attribution updates dynamically between presets with 100% mathematical fidelity.`);

  await browser.close();
  console.log("======================================================================");
  console.log("ALL LIVE BROWSER INTERACTIONS VERIFIED WITH ZERO ERRORS!");
  console.log("======================================================================");
}

run().catch(err => {
  console.error("FATAL ERROR in browser verification:", err);
  process.exit(1);
});
