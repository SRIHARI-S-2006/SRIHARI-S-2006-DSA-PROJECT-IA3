import pypdf
import json

pdf_path = "data/external/trai/trai_press_release_subscription_sep2026.pdf"
reader = pypdf.PdfReader(pdf_path)
print(f"Total Pages in TRAI PDF: {len(reader.pages)}")

full_text = ""
for idx in range(len(reader.pages)):
    page_text = reader.pages[idx].extract_text() or ""
    full_text += f"\n--- PAGE {idx+1} ---\n" + page_text

with open("data/external/trai/trai_extracted_full_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("Saved all 25 pages to data/external/trai/trai_extracted_full_text.txt")
