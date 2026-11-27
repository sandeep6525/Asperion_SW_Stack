import os
import re

html_dir = 'extracted_views'
for f in sorted(os.listdir(html_dir)):
    if not f.startswith('view-'):
        continue
    path = os.path.join(html_dir, f)
    with open(path, 'r', encoding='utf-8') as fp:
        html = fp.read()
    
    # Check for tab buttons and panels
    tabs = re.findall(r'id=["\'](tab-[^"\']+)["\']|onclick=["\']([^"\']*switch[^"\']*)["\']', html, re.IGNORECASE)
    panels = re.findall(r'id=["\']([^"\']*(?:panel|subview|tab-content)[^"\']*)["\']', html, re.IGNORECASE)
    
    print(f"{f:28s} (len={len(html):6d}) -> {len(tabs):2d} tabs, {len(panels):2d} panels")
    for t in tabs[:4]:
        name = t[0] if t[0] else t[1]
        print(f"   tab: {name}")
    for p in panels[:4]:
        print(f"   pnl: {p}")
