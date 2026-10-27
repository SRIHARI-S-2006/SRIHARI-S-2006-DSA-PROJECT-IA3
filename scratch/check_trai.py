import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.trai.gov.in/release-publication/reports/telecom-subscriptions-reports"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Page fetched successfully. Length:", len(html))
        # Find report titles and pdf/excel links
        soup = BeautifulSoup(html, 'html.parser')
        views = soup.find_all('div', class_=re.compile(r'views-row|field-content'))
        reports = []
        for a in soup.find_all('a'):
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if 'subscription' in text.lower() or 'telecom subscription data' in text.lower() or 'press release' in text.lower():
                reports.append((text, href))
        print("Found matching report links:", len(reports))
        for r in reports[:10]:
            print(" - ", r[0], "-->", r[1])
except Exception as e:
    print("Error:", e)
