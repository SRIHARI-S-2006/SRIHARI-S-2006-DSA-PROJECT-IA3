import re
import json

with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect paragraphs mentioning subscribers, market share, wireline, wireless, MNP
sections = {}

# 1. Total Telephone Subscribers (Wireline + Wireless)
# Look for overall numbers
m_total = re.search(r"total telephone subscribers.*?increased.*?from\s+([\d\.,]+)\s+million.*?to\s+([\d\.,]+)\s+million", text, re.I)
if m_total:
    sections['total_subscribers_trend'] = {'from_million': m_total.group(1), 'to_million': m_total.group(2)}

# 2. Wireless subscribers
m_wireless = re.search(r"Total wireless subscribers.*?from\s+([\d\.,]+)\s+million.*?to\s+([\d\.,]+)\s+million", text, re.I)
if m_wireless:
    sections['wireless_subscribers_trend'] = {'from_million': m_wireless.group(1), 'to_million': m_wireless.group(2)}

# 3. Wireline subscribers
m_wireline = re.search(r"Wireline subscribers.*?from\s+([\d\.,]+)\s+million.*?to\s+([\d\.,]+)\s+million", text, re.I)
if m_wireline:
    sections['wireline_subscribers_trend'] = {'from_million': m_wireline.group(1), 'to_million': m_wireline.group(2)}

# 4. Service provider market share
# Look for market share percentages
print("Searching for operator market shares...")
matches = re.findall(r"(Reliance Jio|Bharti Airtel|Vodafone Idea|BSNL|MTNL).*?(\d{1,2}\.\d{1,2})\s*%", text)
print("Matches found:", len(matches))
print(matches[:15])

# Print lines mentioning 'Market Share'
lines = text.split('\n')
for i, l in enumerate(lines):
    if 'market share' in l.lower() or 'mnp' in l.lower() or 'mobile number portability' in l.lower():
        print(f"L{i}: {l[:100]}")
