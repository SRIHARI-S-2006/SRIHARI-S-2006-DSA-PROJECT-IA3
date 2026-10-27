import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
for p_idx, page in enumerate(pages[1:], 1):
    keywords = []
    if "Jio" in page: keywords.append("Jio")
    if "MNP" in page: keywords.append("MNP")
    if "Broadband" in page: keywords.append("Broadband")
    if "Wireline" in page: keywords.append("Wireline")
    if "Wireless" in page: keywords.append("Wireless")
    if "Portability" in page: keywords.append("Portability")
    print(f"Page {p_idx:02d}: {', '.join(keywords)}")
