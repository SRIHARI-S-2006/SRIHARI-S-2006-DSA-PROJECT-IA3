import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function checkElements() {
  const browser = await Browser.launch({ width: 1440, height: 960 });
  const page = await browser.newPage({ width: 1440, height: 960 });

  await page.goto('http://127.0.0.1:5000/', { settleMs: 3000 });
  await sleep(1500);

  const res = await page.eval(() => {
    const funnelEl = document.getElementById('retention-funnel-container');
    const matrixEl = document.getElementById('service-contract-matrix-container');
    return {
      funnelLength: funnelEl ? funnelEl.innerHTML.length : -1,
      funnelChildren: funnelEl ? Array.from(funnelEl.children).map(c => c.className) : [],
      matrixLength: matrixEl ? matrixEl.innerHTML.length : -1,
      matrixChildren: matrixEl ? Array.from(matrixEl.children).map(c => c.className) : [],
    };
  });
  console.log("Containers info:", JSON.stringify(res, null, 2));
  await browser.close();
}

checkElements().catch(console.error);
