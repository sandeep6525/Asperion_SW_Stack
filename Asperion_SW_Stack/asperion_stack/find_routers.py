import re

with open('app/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

routers = re.findall(r'app\.include_router\(([^)]+)\)', text)
for r in routers:
    print(r.strip())
