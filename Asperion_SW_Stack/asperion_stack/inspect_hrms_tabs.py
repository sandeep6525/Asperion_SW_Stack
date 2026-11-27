import re

with open('extracted_views/view-hrms.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all tab buttons and panels in view-hrms
tab_btns = re.findall(r'<button\s+id=[\'"](tab-hrms-[^\'"]+)[\'"].*?onclick=[\'"]switchHRMSTab\([\'"]([^\'"]+)[\'"]\).*?>(.*?)</button>', text, re.DOTALL)
print(f"HRMS Tabs found: {len(tab_btns)}")
for b in tab_btns:
    title = re.sub(r'<[^>]+>', '', b[2]).strip()
    print(f" - {b[1]}: {title}")

# Find all panels (id="hrms-panel-...")
panels = re.findall(r'id=[\'"](hrms-panel-[^\'"]+)[\'"]', text)
print(f"\nHRMS Panels found: {len(panels)}")
for p in panels:
    print(f" - {p}")
