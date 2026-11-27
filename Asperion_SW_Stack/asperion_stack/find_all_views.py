import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<section\s+id=[\'"](view-[^\'"]+)[\'"]', text)
print("All view IDs in index.html:")
for m in matches:
    print(f" - {m}")
