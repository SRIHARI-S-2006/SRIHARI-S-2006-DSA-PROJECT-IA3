import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';
import { mkdirSync } from 'node:fs';

async function run() {
  mkdirSync('.taste-skill/post-improvements', { recursive: true });
  console.log("Launching headless browser via CDP...");
  const browser = await Browser.launch({ width: 1440, height: 900 });
  const page = await browser.newPage({ width: 1440, height: 900 });

  console.log("Navigating to http://127.0.0.1:5000/ ...");
  await page.goto('http://127.0.0.1:5000/', { settleMs: 1500 });

  // 1. Drilldown Interaction: Heatmap / Matrix segment click
  console.log("Triggering drilldown to Month-to-month + Fiber optic...");
  await page.eval(() => {
    window.drilldownSegment("Month-to-month", "Fiber optic");
  });
  await sleep(1500);
  await page.screenshot({ path: '.taste-skill/post-improvements/explorer-drilldown.jpg', format: 'jpeg', quality: 85 });
  console.log("Saved explorer-drilldown.jpg");

  // 2. Open Customer Drawer to inspect contextual benchmarks
  console.log("Opening customer detail drawer...");
  await page.eval(() => {
    const row = document.querySelector("#customers-table-body tr");
    if (row) row.click();
  });
  await sleep(1000);
  await page.screenshot({ path: '.taste-skill/post-improvements/customer-drawer.jpg', format: 'jpeg', quality: 85 });
  console.log("Saved customer-drawer.jpg");

  // Close drawer
  await page.eval(() => {
    const btn = document.getElementById("btn-close-drawer");
    if (btn) btn.click();
  });
  await sleep(500);

  // 3. Navigate to Prediction Lab and test High Risk preset
  console.log("Testing Prediction Lab with High Risk Preset...");
  await page.eval(() => {
    window.navigateToSection("predict");
    const highBtn = document.getElementById("preset-high-risk");
    if (highBtn) highBtn.click();
  });
  await sleep(1500);
  await page.screenshot({ path: '.taste-skill/post-improvements/prediction-high-risk.jpg', format: 'jpeg', quality: 85 });
  console.log("Saved prediction-high-risk.jpg");

  // 4. Test Low Risk preset
  console.log("Testing Prediction Lab with Low Risk Preset...");
  await page.eval(() => {
    const lowBtn = document.getElementById("preset-low-risk");
    if (lowBtn) lowBtn.click();
  });
  await sleep(1500);
  await page.screenshot({ path: '.taste-skill/post-improvements/prediction-low-risk.jpg', format: 'jpeg', quality: 85 });
  console.log("Saved prediction-low-risk.jpg");

  await browser.close();
  console.log("All screenshots captured successfully!");
}

run().catch(err => {
  console.error("Error in capture:", err);
  process.exit(1);
});
