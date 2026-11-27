with open('extracted_views/view-iso-standards.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
panels = re.findall(r'<div[^>]*id=\"iso-panel-[^\"]*\"[^>]*>(.*?)</div>\s*<!-- Tab', c, re.DOTALL)
print(f"Found {len(panels)} panels in ISO HTML")
lines = c.splitlines()
for i, l in enumerate(lines[:120]):
    print(f"{i+1}: {l}")
