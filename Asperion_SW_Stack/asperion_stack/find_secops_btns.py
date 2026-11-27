import re

with open('extracted_views/view-secops.html', 'r', encoding='utf-8') as f:
    text = f.read()

buttons = re.findall(r'<button\s+([^>]*onclick=[\'"][^\'"]*switch[^\'"]*[\'"][^>]*)>(.*?)</button>', text, re.DOTALL)
print(f"Buttons with switch: {len(buttons)}")
for b in buttons:
    print(b[0][:100], "-->", re.sub(r'<[^>]+>', '', b[1]).strip())
