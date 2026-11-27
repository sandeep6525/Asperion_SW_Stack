import re

with open('extracted_views/view-crm.html', 'r', encoding='utf-8') as f:
    text = f.read()

subsections = re.findall(r'<h3[^>]*>(.*?)</h3>', text, re.DOTALL)
print(f"CRM Subsections ({len(subsections)}):")
for s in subsections:
    print(f" - {re.sub(r'<[^>]+>', '', s).strip()}")

tables = re.findall(r'<tbody\s+id=[\'"]([^\'"]+)[\'"]', text)
print(f"\nCRM Tables ({len(tables)}):")
for t in tables:
    print(f" - {t}")
