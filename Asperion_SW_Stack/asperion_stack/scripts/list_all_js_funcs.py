import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

funcs = re.findall(r'(?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(', js)
print(f"Total functions in app.js: {len(funcs)}")

loaders = [fn for fn in funcs if fn.startswith('load') or fn.startswith('render') or fn.startswith('switch')]
print(f"Loaders/Renderers/Switchers: {len(loaders)}")
for l in loaders:
    print("  ", l)
