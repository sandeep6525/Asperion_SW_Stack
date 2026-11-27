import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the modals section at the bottom of index.html
# Usually after </main> or after the last view
m = re.search(r'(<!-- =* MODALS.*?)(?=</body>|\Z)', html, re.DOTALL | re.IGNORECASE)
if m:
    modals_html = m.group(1)
    with open('extracted_views/all_modals.html', 'w', encoding='utf-8') as out:
        out.write(modals_html)
    print(f"Extracted all modals! Length: {len(modals_html)} bytes")
else:
    # search where id="modal-" starts
    idx = html.find('id="modal-')
    if idx != -1:
        start = html.rfind('<div', 0, idx)
        modals_html = html[start:]
        with open('extracted_views/all_modals.html', 'w', encoding='utf-8') as out:
            out.write(modals_html)
        print(f"Extracted all modals from first modal! Length: {len(modals_html)} bytes")
