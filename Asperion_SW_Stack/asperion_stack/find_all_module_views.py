import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

views = re.findall(r'<(?:div|section)\s+id=[\'"](view-[^\'"]+)[\'"]', text)
print(f"Total views found in index.html: {len(views)}")
for v in views:
    print(f" - {v}")
