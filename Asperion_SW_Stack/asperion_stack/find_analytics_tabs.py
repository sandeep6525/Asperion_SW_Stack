import re

with open('extracted_views/view-analytics.html', 'r', encoding='utf-8') as f:
    text = f.read()

buttons = re.findall(r'<button\s+([^>]*switchAnalyticsTab[^\'"]*[\'"][^>]*)>(.*?)</button>', text, re.DOTALL)
print(f"Analytics tabs ({len(buttons)}):")
for b in buttons:
    print(" -", re.sub(r'<[^>]+>', '', b[1]).strip())
