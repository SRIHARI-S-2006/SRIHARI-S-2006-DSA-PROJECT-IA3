import re

with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Look for wireless market share
p = re.compile(r"Wireless\s+Telephony\s+Service\s+Providers|Market\s+Share\s+of\s+Wireless|Wireless\s+Subscribers\s+as\s+on", re.I)
for m in p.finditer(text):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 1000)
    print("--- MATCH ---")
    print(text[start:end].encode('ascii', errors='replace').decode('ascii'))
