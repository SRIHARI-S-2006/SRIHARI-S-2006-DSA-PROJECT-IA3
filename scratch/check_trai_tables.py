from bs4 import BeautifulSoup

with open('scratch/trai_page.html', 'w', encoding='utf-8') as out_f:
    import urllib.request
    url = "https://www.trai.gov.in/release-publication/reports/telecom-subscriptions-reports"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        out_f.write(content)

soup = BeautifulSoup(content, 'html.parser')
rows = soup.find_all('tr')
print(f"Found {len(rows)} table rows")
for row in rows[:15]:
    cols = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
    links = [a['href'] for a in row.find_all('a', href=True)]
    print(cols, links)
