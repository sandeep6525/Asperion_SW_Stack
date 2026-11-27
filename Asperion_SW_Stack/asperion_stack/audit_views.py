import re

index_path = r"E:\Asperion_SW_Stack\Asperion_SW_Stack\Asperion_SW_Stack\asperion_stack\app\static\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

sections = re.findall(r'<section\s+id=[\'"](view-[^\'"]+)[\'"].*?</section>', content, re.DOTALL)
print(f"Total sections matched: {len(sections)}")

# Let's inspect each section's titles and buttons
view_blocks = re.findall(r'<section\s+id=[\'"](view-[^\'"]+)[\'"](.*?)<!-- \d+\. |<section\s+id=[\'"](view-[^\'"]+)[\'"](.*?)</section>', content, re.DOTALL)
print(f"Blocks: {len(view_blocks)}")

# Let's write a targeted script to extract all view IDs, headings, tables, modals and buttons
results = []
pattern = r'<section\s+id=[\'"](view-[^\'"]+)[\'"]>(.*?)</section>'
for m in re.finditer(r'<section\s+id=[\'"](view-[^\'"]+)[\'"]\s+class=[\'"][^\'"]*[\'"]>(.*?)(?=(?:<section\s+id=[\'"]view-|\Z))', content, re.DOTALL):
    vid = m.group(1)
    body = m.group(2)
    h2 = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.DOTALL)
    h3 = re.findall(r'<h3[^>]*>(.*?)</h3>', body, re.DOTALL)
    tables = re.findall(r'<table[^>]*>.*?<tbody\s+id=[\'"]([^\'"]+)[\'"]', body, re.DOTALL)
    buttons = re.findall(r'<button\s+[^>]*onclick=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</button>', body, re.DOTALL)
    
    results.append({
        "view": vid,
        "title": h2[0].strip() if h2 else "",
        "subsections": [h.strip() for h in h3[:5]],
        "table_ids": tables,
        "buttons": [b[0].split('(')[0] for b in buttons[:8]]
    })

for r in results:
    print(f"\n[{r['view']}] - {r['title'][:50]}")
    print(f"  Subsections: {r['subsections']}")
    print(f"  Tables: {r['table_ids']}")
    print(f"  Key Actions: {list(set(r['buttons']))}")
