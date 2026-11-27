import re

with open('frontend/src/views/ISOStandardsView.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

ids = re.findall(r'id=["\']([^"\']+)["\']', c)
for i in ids:
    print(' ', i)
