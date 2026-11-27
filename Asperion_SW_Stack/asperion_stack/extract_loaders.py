import re, json

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

loader_names = [
    'loadGovernance', 'loadSDLC', 'loadProcurement', 'loadGuardrails',
    'loadISOStandardsModule', 'loadAICloudModule', 'loadAgenticAI',
    'loadOperations', 'loadCryptoTools', 'loadInfrastructure', 'loadSecOps',
    'loadVault', 'loadStrategy', 'loadAnalyticsHub', 'loadInternalSupport',
    'loadITSM', 'loadTeams', 'loadSharePoint', 'loadTraining',
    'loadClientPortal', 'loadVendorPortal'
]

summary = {}
for name in loader_names:
    pattern = rf'(async\s+function\s+{name}\s*\(.*?\)\s*\{{.*?\n\}})'
    match = re.search(pattern, js, re.DOTALL)
    if match:
        body = match.group(0)
        # Find fetch calls or axios or endpoints
        endpoints = re.findall(r'[\'\"`](/api/v1/[^\'\"`\s\?]+)', body)
        # Find DOM element IDs manipulated
        el_ids = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', body)
        summary[name] = {
            "endpoints": sorted(list(set(endpoints))),
            "element_ids": sorted(list(set(el_ids)))[:10],
            "body_snippet": body[:300] + "..."
        }
    else:
        summary[name] = "NOT_FOUND"

with open('loaders_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

print("Extracted loader summaries to loaders_summary.json")
