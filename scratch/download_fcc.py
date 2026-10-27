import subprocess
import json
import os

os.makedirs('data/external', exist_ok=True)
out_file = 'data/external/fcc_consumer_complaints_sample.json'

cmd = [
    'curl.exe', '-s',
    '--resolve', 'opendata.fcc.gov:443:52.206.140.199',
    'https://opendata.fcc.gov/resource/3xyp-aqkj.json?$limit=5000'
]

print("Fetching 5000 FCC complaints from SODA API...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
if res.returncode == 0 and res.stdout.strip().startswith('['):
    data = json.loads(res.stdout)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully downloaded {len(data)} FCC complaints to {out_file}!")
else:
    print(f"Curl failed or non-JSON returned. Code: {res.returncode}, Err: {res.stderr[:200]}")
