import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")

print("=== PAGE 17 & 18 (MNP Porting & Churn Dynamics) ===")
print(pages[17][:1500])
print("---")
print(pages[18][:1500])

print("\n=== PAGE 20 (Wireless Operators & Market Share) ===")
print(pages[20][:1500])
