import os
import re

html_dir = 'extracted_views'
event_attrs = set()

for f in os.listdir(html_dir):
    if not f.startswith('view-'):
        continue
    with open(os.path.join(html_dir, f), 'r', encoding='utf-8') as fp:
        c = fp.read()
    found = re.findall(r'\b(on[a-z]+)=', c, re.IGNORECASE)
    for ev in found:
        event_attrs.add(ev.lower())

print(f"All event handler attributes found in HTML: {event_attrs}")
