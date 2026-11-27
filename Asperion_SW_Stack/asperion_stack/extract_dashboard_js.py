import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

for fn in ['loadDashboard', 'loadBalancedScorecard', 'loadStatutoryFilingsRadar']:
    m = re.search(rf'(async\s+)?function\s+{fn}\s*\(.*?\)\s*\{{.*?\n\}}', js, re.DOTALL)
    if m:
        print(f"=== {fn} ===")
        print(m.group(0)[:1200])
