import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'</aside>(.*?)<section\s+id=[\'"]view-dashboard[\'"]', text, re.DOTALL)
if m:
    print("Between sidebar and dashboard:")
    print(m.group(1)[:2000])
