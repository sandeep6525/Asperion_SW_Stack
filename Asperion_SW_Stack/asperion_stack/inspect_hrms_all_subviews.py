import re

with open('extracted_views/view-hrms.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find each hrms-subview- block
subviews = re.findall(r'<div\s+id=[\'"](hrms-subview-[^\'"]+)[\'"].*?>(.*?)(?=(?:<div\s+id=[\'"]hrms-subview-|</section>|\Z))', text, re.DOTALL)
for s in subviews:
    h3 = re.findall(r'<h3[^>]*>(.*?)</h3>', s[1], re.DOTALL)
    title = re.sub(r'<[^>]+>', '', h3[0]).strip() if h3 else s[0]
    tables = re.findall(r'<tbody\s+id=[\'"]([^\'"]+)[\'"]', s[1])
    print(f"[{s[0]}] - {title}")
    print(f"   Tables: {tables}")
