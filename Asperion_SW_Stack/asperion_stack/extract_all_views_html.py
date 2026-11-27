import re, os

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find each view boundary
views_list = [
    'view-dashboard', 'view-governance', 'view-crm', 'view-finance',
    'view-hrms', 'view-pmo', 'view-sdlc', 'view-procurement',
    'view-infrastructure', 'view-secops', 'view-vault', 'view-strategy',
    'view-analytics', 'view-internal-support', 'view-itsm', 'view-teams',
    'view-sharepoint', 'view-training', 'view-portal-employee',
    'view-portal-client', 'view-portal-vendor', 'view-guardrails',
    'view-ai-cloud', 'view-iso-standards', 'view-agentic-ai',
    'view-operations', 'view-crypto-tools'
]

os.makedirs('extracted_views', exist_ok=True)

for vid in views_list:
    # Pattern to match from <section/div id="vid" until next view or main close
    pattern = rf'(<(?:div|section)\s+id=[\'"]{vid}[\'"].*?)(?=(?:<(?:div|section)\s+id=[\'"]view-|</main>|\Z))'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        content = m.group(1).strip()
        with open(f'extracted_views/{vid}.html', 'w', encoding='utf-8') as out:
            out.write(content)
        print(f"Extracted {vid}: {len(content)} bytes")
    else:
        print(f"FAILED TO EXTRACT {vid}")
