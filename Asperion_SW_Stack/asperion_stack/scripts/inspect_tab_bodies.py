with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for fn in [
    'switchOperationsTab', 'switchCryptoTab', 'switchAnalyticsTab',
    'switchSharePointTab', 'switchTrainingTab', 'switchESSTab', 'switchClientPortalTab'
]:
    m = re.search(rf'function\s+{fn}\s*\([^)]*\)\s*\{{([^}}]*)\}}', js)
    if m:
        print(f"=== {fn} ===")
        print(m.group(1).strip()[:400])
        print("...")
