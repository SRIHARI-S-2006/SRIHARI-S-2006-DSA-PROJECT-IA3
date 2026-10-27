with open("data/external/trai/trai_extracted_full_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/trai_safe_lines.txt", "w", encoding="utf-8") as out:
    for i, l in enumerate(lines[:350]):
        out.write(f"[{i:03d}] {l.strip()}\n")

print("Wrote first 350 lines to scratch/trai_safe_lines.txt")
