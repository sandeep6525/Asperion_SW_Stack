with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for fn in ['loadGovernance', 'loadFinance', 'loadSecOps']:
    idx = js.find(f'function {fn}(')
    if idx != -1:
        end = js.find('function ', idx + 10)
        print(f"=== {fn} ===")
        print(js[idx:idx+800])
        print("...\n")
