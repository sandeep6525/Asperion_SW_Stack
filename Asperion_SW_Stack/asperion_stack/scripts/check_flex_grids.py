import glob
import re

for fpath in glob.glob('frontend/src/views/*.tsx'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    found = []
    for idx, line in enumerate(lines):
        if 'style={{ display:' in line:
            # check what display class it has
            m = re.search(r'className=["\']([^"\']+)["\']', line)
            classes = m.group(1) if m else ''
            if any(k in classes for k in ['grid', 'flex', 'inline']):
                found.append((idx + 1, classes, line.strip()))
    if found:
        print(f"=== {fpath} ===")
        for lnum, cls, ltext in found:
            print(f"  Line {lnum} ({cls[:30]}): {ltext[:100]}")
