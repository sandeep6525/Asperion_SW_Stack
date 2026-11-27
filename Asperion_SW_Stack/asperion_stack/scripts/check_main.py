with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<main[^>]*>', text)
if m:
    print('Original main:', m.group(0))

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_text = f.read()

m_app = re.search(r'<main[^>]*>', app_text)
if m_app:
    print('React App main:', m_app.group(0))
