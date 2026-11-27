import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

m = re.search(r'function\s+loadDashboardCharts\s*\(.*?\)\s*\{(.*?)\n\}', js, re.DOTALL)
if m:
    print("loadDashboardCharts found:")
    print(m.group(0)[:1500])
else:
    # search where chart-exec-cashflow is used
    m2 = re.search(r'chart-exec-cashflow.*?\n\}', js, re.DOTALL)
    if m2:
        print("chart-exec-cashflow found:")
        print(m2.group(0)[:1000])
