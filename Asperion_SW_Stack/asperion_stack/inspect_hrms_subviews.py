import re

with open('extracted_views/view-hrms.html', 'r', encoding='utf-8') as f:
    text = f.read()

subviews = re.findall(r'id=[\'"](hrms-subview-[^\'"]+)[\'"]', text)
print(f"Total HRMS Subviews: {len(subviews)}")
for s in subviews:
    print(f" - {s}")
