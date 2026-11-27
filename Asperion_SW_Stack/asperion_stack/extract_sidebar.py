import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'(<aside\s+id=[\'"]main-sidebar[\'"].*?</aside>)'
m = re.search(pattern, html, re.DOTALL)
if m:
    with open('extracted_sidebar.html', 'w', encoding='utf-8') as out:
        out.write(m.group(1))
    print("Found sidebar! Length:", len(m.group(1)))
else:
    print("Sidebar not found")
