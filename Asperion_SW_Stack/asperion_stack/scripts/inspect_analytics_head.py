with open('extracted_views/view-analytics.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
lines = c.splitlines()
print(f"Total lines in view-analytics.html: {len(lines)}")
for i, l in enumerate(lines[:80]):
    print(f"{i+1}: {l}")
