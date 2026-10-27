import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';
import { writeFileSync } from 'node:fs';

async function capture() {
  console.log("Launching headless browser for post-redesign inspection...");
  const browser = await Browser.launch();
  try {
    const page = await browser.newPage({ width: 1440, height: 900 });
    console.log("Navigating to http://127.0.0.1:5000 ...");
    await page.navigate("http://127.0.0.1:5000");
    await sleep(2500); // Wait for Chart.js and API data

    const buf = await page.screenshot({ format: "jpeg", quality: 85 });
    writeFileSync(".taste-skill/inspect/after_redesign.jpg", buf);
    console.log("Saved post-redesign screenshot to .taste-skill/inspect/after_redesign.jpg");
  } finally {
    await browser.close();
  }
}

capture().catch(err => {
  console.error("Screenshot capture failed:", err);
  process.exit(1);
});
