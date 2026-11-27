import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

funcs = re.findall(r'function\s+(switch\w+Tab)\s*\(([^)]*)\)\s*\{([^}]*)\}', js)
print(f"Found {len(funcs)} switchTab functions in app.js:")
for name, args, body in funcs:
    print(f"\n--- {name}({args}) ---")
    lines = [l.strip() for l in body.splitlines() if l.strip()][:6]
    for l in lines:
        print("  ", l)
