import re
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js_path = os.path.join(base_dir, 'website', 'static', 'app.js')

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Let's find every getElementById('...') that gets passed to Chart
canvas_ids = re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', js)
canvas_in_js = [c for c in canvas_ids if 'Chart' in c or 'chart' in c.lower()]
print("Canvas IDs referenced in app.js:")
for c in set(canvas_in_js):
    print("  -", c)

# Let's find each function that creates charts
functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{', js)
print("\nFunctions in app.js related to charts:")
for fn in functions:
    if 'chart' in fn.lower() or 'render' in fn.lower() or 'viz' in fn.lower():
        print("  -", fn)
