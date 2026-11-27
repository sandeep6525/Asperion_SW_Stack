import re, json

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find all endpoints in app.js
api_calls = sorted(list(set(re.findall(r'[\'\"`](/api/v1/[^\'\"`\s\?]+)', js))))
print(f"Total unique /api/v1/ endpoints found in app.js: {len(api_calls)}")

# Find switchModule implementation in app.js
switch_mod_match = re.search(r'function switchModule\s*\(moduleId\)\s*\{(.*?)\n\}', js, re.DOTALL)
if switch_mod_match:
    print("switchModule found:")
    print(switch_mod_match.group(0)[:1000])

# Find which functions load each view
loaders = re.findall(r'(?:async\s+)?function\s+(load[A-Za-z0-9_]+)\s*\(', js)
print(f"\nLoaders found in app.js: {len(loaders)}")
for l in sorted(set(loaders)):
    print(f" - {l}")
