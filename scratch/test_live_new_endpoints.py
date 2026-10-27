import urllib.request
import json
import time

base = "http://127.0.0.1:5000"
endpoints = [
    "/api/behavioral-intelligence",
    "/api/external-market-intelligence",
    "/api/uci-benchmark",
    "/api/provenance",
    "/api/model-diagnostics",
    "/api/lifecycle-retention",
    "/api/distribution-comparison"
]

time.sleep(1) # wait for Flask debug reload

for ep in endpoints:
    url = base + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[SUCCESS] {ep} returned {len(str(data))} bytes. Keys: {list(data.keys())[:5]}")
    except Exception as e:
        print(f"[FAIL] {ep}: {e}")
