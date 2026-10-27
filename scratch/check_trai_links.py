import re
from bs4 import BeautifulSoup

with open('scratch/trai_page.html', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'\.pdf|\.xlsx|\.csv|press-release', re.I))
print(f"Found {len(links)} resource links")
for a in links[:15]:
    print(a.get_text(strip=True)[:60], "-->", a.get('href'))
