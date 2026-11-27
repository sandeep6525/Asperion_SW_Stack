import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'(<(?:div|section)\s+id=[\'"]view-ai-cloud[\'"].*?)(?=(?:<(?:div|section)\s+id=[\'"]view-|\Z))'
m = re.search(pattern, html, re.DOTALL)
if m:
    with open('extracted_ai_cloud.html', 'w', encoding='utf-8') as out:
        out.write(m.group(1))
    print("Found view-ai-cloud! Length:", len(m.group(1)))
else:
    print("Not found")
