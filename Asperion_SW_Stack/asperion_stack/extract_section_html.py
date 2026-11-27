import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_section(section_id):
    pattern = rf'(<section\s+id=[\'"]{section_id}[\'"].*?)(?=(?:<section\s+id=[\'"]view-|\Z))'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        return m.group(1)
    return "NOT FOUND"

dash_html = get_section("view-dashboard")
with open("extracted_dashboard.html", "w", encoding="utf-8") as f:
    f.write(dash_html[:20000])

ai_html = get_section("view-ai-cloud")
with open("extracted_ai_cloud.html", "w", encoding="utf-8") as f:
    f.write(ai_html[:20000])

print("Dashboard snippet length:", len(dash_html))
print("AI snippet length:", len(ai_html))
