with open('extracted_views/view-agentic-ai.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
lines = c.splitlines()
for i, l in enumerate(lines[60:130]):
    print(f"{i+61}: {l}")
