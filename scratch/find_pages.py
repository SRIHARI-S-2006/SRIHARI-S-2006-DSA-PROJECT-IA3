with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
print(f"Total pages parsed: {len(pages)-1}")
for p_idx, page in enumerate(pages[1:], 1):
    if "Jio" in page or "MNP" in page:
        safe_p = page[:250].replace('\n', ' ').strip()
        print(f"Page {p_idx}: {safe_p[:120]}")
