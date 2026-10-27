import urllib.request
import os

os.makedirs('data/external/trai', exist_ok=True)

trai_pdf_url = "https://www.trai.gov.in/sites/default/files/2026-09/PR_No125of2026_0.pdf"
out_pdf = "data/external/trai/trai_press_release_subscription_sep2026.pdf"

print(f"Downloading TRAI official report from {trai_pdf_url}...")
try:
    req = urllib.request.Request(trai_pdf_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()
        with open(out_pdf, 'wb') as f:
            f.write(content)
        print(f"Downloaded TRAI PDF ({len(content)} bytes) to {out_pdf}!")
except Exception as e:
    print(f"Failed downloading {trai_pdf_url}: {e}")
