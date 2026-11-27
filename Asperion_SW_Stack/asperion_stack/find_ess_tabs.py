import re

with open('extracted_views/view-portal-employee.html', 'r', encoding='utf-8') as f:
    text = f.read()

buttons = re.findall(r'<button\s+([^>]*switchESSTab[^\'"]*[\'"][^>]*)>(.*?)</button>', text, re.DOTALL)
print(f"ESS tabs ({len(buttons)}):")
for b in buttons:
    print(" -", re.sub(r'<[^>]+>', '', b[1]).strip())
