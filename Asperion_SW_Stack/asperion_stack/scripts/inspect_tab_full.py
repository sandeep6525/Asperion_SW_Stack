with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for fn in ['switchAnalyticsTab', 'switchClientPortalTab', 'switchESSTab', 'switchSharePointTab', 'switchTrainingTab']:
    idx = js.find(f'function {fn}(')
    if idx != -1:
        end = js.find('function ', idx + 10)
        chunk = js[idx:end if end != -1 else idx+1500]
        print(f"=== {fn} ===")
        print(chunk[:500])
