import re

views_to_check = [
    'view-agentic-ai.html',
    'view-analytics.html',
    'view-crm.html',
    'view-crypto-tools.html',
    'view-guardrails.html',
    'view-infrastructure.html',
    'view-iso-standards.html',
    'view-itsm.html',
    'view-operations.html',
    'view-portal-client.html',
    'view-portal-employee.html',
    'view-portal-vendor.html',
    'view-secops.html',
    'view-sharepoint.html',
    'view-training.html',
    'view-internal-support.html',
    'view-strategy.html',
    'view-teams.html',
    'view-vault.html',
]

for v in views_to_check:
    path = f'extracted_views/{v}'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Find all buttons with onclick
    onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', c)
    switch_calls = [o for o in onclicks if 'switch' in o.lower()]
    tab_ids = re.findall(r'id=["\'](tab-[^"\']+)["\']', c)
    panel_ids = re.findall(r'id=["\']([^"\']*(?:subview|panel|tab-content|view-)[^"\']*)["\']', c)
    
    print(f"=== {v} ===")
    print(f"  Switches ({len(switch_calls)}): {set(switch_calls)}")
    print(f"  Tab IDs ({len(tab_ids)}): {tab_ids[:6]}")
    print(f"  Panel IDs ({len(panel_ids)}): {panel_ids[:8]}")
