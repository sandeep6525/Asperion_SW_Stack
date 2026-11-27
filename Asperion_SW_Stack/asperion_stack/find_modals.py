import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all modals (id="modal-...")
modals = re.findall(r'id=[\'"](modal-[^\'"]+)[\'"]', html)
print(f"Total modals found: {len(modals)}")
for m in modals:
    print(f" - {m}")
