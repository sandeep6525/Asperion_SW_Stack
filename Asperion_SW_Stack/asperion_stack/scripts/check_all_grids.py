import glob
import re

for fpath in glob.glob('frontend/src/views/*.tsx'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    found = []
    for idx, line in enumerate(lines):
        if 'style={{ display:' in line and 'grid' in line:
            found.append((idx + 1, line.strip()))
    if found:
        print(f"=== {fpath} ===")
        for lnum, ltext in found:
            print(f"  Line {lnum}: {ltext[:120]}")
