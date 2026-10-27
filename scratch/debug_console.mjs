import { Browser, sleep } from '../.agents/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function debugErrors() {
  const browser = await Browser.launch({ width: 1440, height: 960 });
  const page = await browser.newPage({ width: 1440, height: 960 });

  page.browser.on(page.sessionId, 'Runtime.consoleAPICalled', (params) => {
    console.log(`[Browser Console ${params.type}]:`, params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' '));
  });

  page.browser.on(page.sessionId, 'Runtime.exceptionThrown', (params) => {
    console.error(`[Browser Exception]:`, params.exceptionDetails);
  });

  await page.goto('http://127.0.0.1:5000/', { settleMs: 3000 });
  await sleep(2000);

  const html = await page.eval(() => {
    return {
      funnelHtml: document.getElementById('retention-funnel-container')?.innerHTML,
      matrixHtml: document.getElementById('service-contract-matrix-container')?.innerHTML,
      corrHtml: document.getElementById('correlation-matrix-container')?.innerHTML
    };
  });
  console.log("HTML contents:", html);
  await browser.close();
}

debugErrors().catch(console.error);
