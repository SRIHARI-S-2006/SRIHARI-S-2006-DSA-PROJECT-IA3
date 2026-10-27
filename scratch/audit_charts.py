import re
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_path = os.path.join(base_dir, 'website', 'templates', 'index.html')
js_path = os.path.join(base_dir, 'website', 'static', 'app.js')
app_py_path = os.path.join(base_dir, 'website', 'app.py')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\'][^>]*>', html)
print(f"Total canvas tags found in HTML: {len(canvases)}")
for i, c in enumerate(canvases, 1):
    # Find which section it belongs to in html
    pos = html.find(f'id="{c}"')
    if pos == -1:
        pos = html.find(f"id='{c}'")
    sec = "Unknown"
    if pos != -1:
        prev_secs = re.findall(r'<section[^>]*id=["\']section-([^"\']+)["\']', html[:pos])
        if prev_secs:
            sec = prev_secs[-1]
    # find parent title
    parent_chunk = html[max(0, pos-1000):pos]
    titles = re.findall(r'<h3[^>]*class=["\']panel-title["\'][^>]*>(.*?)</h3>', parent_chunk)
    title = titles[-1] if titles else "Unknown"
    subtitles = re.findall(r'<span[^>]*class=["\']panel-subtitle["\'][^>]*>(.*?)</span>', parent_chunk)
    sub = subtitles[-1] if subtitles else ""
    print(f"{i:2d}. Workspace: {sec:<12} | Canvas ID: {c:<28} | Title: {title} ({sub})")

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

print("\n--- Charts instantiated in app.js ---")
charts = re.findall(r'chartInstances\[["\']([^"\']+)["\']\]\s*=\s*new\s+Chart\s*\(\s*([^,]+),\s*\{', js)
for ckey, target in charts:
    print(f"Instance key: {ckey:<25} on {target.strip()}")

print("\n--- Other new Chart occurrences ---")
all_charts = re.findall(r'new\s+Chart\s*\(\s*([^,]+),\s*\{', js)
print(f"Total new Chart() calls in app.js: {len(all_charts)}")
