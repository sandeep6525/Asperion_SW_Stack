with open('extracted_views/view-agentic-ai.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
lines = c.splitlines()
print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines[:60]):
    print(f"{i+1}: {l}")
