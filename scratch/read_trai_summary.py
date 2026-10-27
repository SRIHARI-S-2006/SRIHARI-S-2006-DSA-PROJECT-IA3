with open("scratch/trai_extracted_summary.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines[:60]:
    # safe print
    safe_line = line.encode('ascii', errors='replace').decode('ascii').strip()
    if safe_line:
        print(safe_line)
