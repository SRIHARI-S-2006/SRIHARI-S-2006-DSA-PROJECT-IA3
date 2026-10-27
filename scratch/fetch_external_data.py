import urllib.request
import json
import os
import zipfile
import io

os.makedirs('data/external', exist_ok=True)

# 1. Test UCI Iranian Churn
print("--- 1. Testing UCI Iranian Churn Dataset ---")
uci_urls = [
    "https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip",
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iranian_churn.csv",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00563/Customer%20Churn.csv"
]

uci_downloaded = False
for u in uci_urls:
    try:
        print(f"Trying {u}...")
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            if u.endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(content)) as z:
                    print("Zip contents:", z.namelist())
                    for fname in z.namelist():
                        if fname.endswith('.csv'):
                            with open(os.path.join('data/external', os.path.basename(fname)), 'wb') as f:
                                f.write(z.read(fname))
                            print(f"Extracted {fname} to data/external/{os.path.basename(fname)}")
                            uci_downloaded = True
            else:
                out_path = os.path.join('data/external', 'iranian_churn.csv')
                with open(out_path, 'wb') as f:
                    f.write(content)
                print(f"Saved {out_path} ({len(content)} bytes)")
                uci_downloaded = True
            if uci_downloaded:
                break
    except Exception as e:
        print(f"Failed {u}: {e}")

# 2. Test FCC Consumer Complaints Open Data (Socrata API)
print("\n--- 2. Testing FCC Consumer Complaints Open Data ---")
fcc_urls = [
    "https://opendata.fcc.gov/resource/3xyp-aqkj.json?$limit=5000&$order=ticket_created%20DESC",
    "https://opendata.fcc.gov/resource/3xyp-aqkj.json?$limit=5000"
]

fcc_downloaded = False
for u in fcc_urls:
    try:
        print(f"Trying FCC Socrata API {u}...")
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Fetched {len(data)} FCC complaint records!")
            out_path = os.path.join('data/external', 'fcc_consumer_complaints_sample.json')
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {out_path}")
            fcc_downloaded = True
            break
    except Exception as e:
        print(f"Failed {u}: {e}")

# 3. Test TRAI Telecom Subscription Data
print("\n--- 3. Testing TRAI Telecom Subscription Data ---")
trai_urls = [
    "https://www.trai.gov.in/release-publication/reports/telecom-subscriptions-reports"
]
for u in trai_urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"TRAI webpage loaded ({len(html)} chars)")
            # Look for press releases / data links
            import re
            links = re.findall(r'href=[\'"]([^\'"]+subscription[^\'"]*)[\'"]', html, re.I)
            print(f"Found {len(links)} links matching 'subscription':", links[:5])
    except Exception as e:
        print(f"Failed TRAI {u}: {e}")
