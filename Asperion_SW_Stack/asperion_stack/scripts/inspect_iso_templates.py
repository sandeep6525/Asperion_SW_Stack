with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for fn in ['loadISOCertificationsGrid', 'loadISOControlsTable', 'loadISOAuditsGrid', 'loadISOCapasContainer', 'loadISOGrievancesTable']:
    idx = js.find(f'function {fn}(')
    if idx != -1:
        print(f"=== {fn} ===")
        print(js[idx:idx+1500])
        print("...\n")
