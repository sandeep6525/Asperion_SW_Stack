import re

with open('extracted_views/view-secops.html', 'r', encoding='utf-8') as f:
    text = f.read()

subsections = re.findall(r'<h3[^>]*>(.*?)</h3>', text, re.DOTALL)
print(f"SecOps Subsections ({len(subsections)}):")
for s in subsections:
    print(f" - {re.sub(r'<[^>]+>', '', s).strip()}")

tabs = re.findall(r'onclick=[\'"](switchSecOpsTab\([^\'"]+\))[\'"][^>]*>(.*?)</button>', text, re.DOTALL)
print(f"\nSecOps Tabs ({len(tabs)}):")
for t in tabs:
    print(f" - {t[0]}: {re.sub(r'<[^>]+>', '', t[1]).strip()}")
