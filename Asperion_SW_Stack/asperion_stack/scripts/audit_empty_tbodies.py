import os
import re

views_dir = 'frontend/src/views'
for f in sorted(os.listdir(views_dir)):
    if not f.endswith('.tsx'):
        continue
    path = os.path.join(views_dir, f)
    with open(path, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    empty_tbodies = re.findall(r'<tbody\b[^>]*>\s*</tbody>', c)
    has_fetch = 'axios.get' in c or 'fetch(' in c
    print(f"{f:25s} -> {len(empty_tbodies):2d} empty tbodies, has API fetch: {has_fetch}")
