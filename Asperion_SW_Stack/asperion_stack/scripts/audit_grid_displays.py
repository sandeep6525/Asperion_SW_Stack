import glob
import re
import os

print("CWD:", os.getcwd())
for fpath in glob.glob('frontend/src/views/*.tsx'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'style=\{\{\s*display:\s*activeTab\s*===[^}]+\}\}'
    found = re.findall(pattern, content)
    if found:
        print(f'{fpath}: {len(found)} occurrences')
        # check how many of these elements also have grid
        lines = content.split('\n')
        for i, l in enumerate(lines):
            if 'style={{ display: activeTab ===' in l and 'grid' in l:
                print(f'   Line {i+1}: {l.strip()[:100]}')
