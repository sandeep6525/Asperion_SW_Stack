import re, json

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

def get_function(name):
    pattern = rf'(?:async\s+)?function\s+{name}\s*\([^)]*\)\s*\{{'
    m = re.search(pattern, js)
    if not m:
        return None
    start = m.start()
    brace_count = 0
    in_fn = False
    for i in range(start, len(js)):
        if js[i] == '{':
            brace_count += 1
            in_fn = True
        elif js[i] == '}':
            brace_count -= 1
            if in_fn and brace_count == 0:
                return js[start:i+1]
    return js[start:start+1000]

target_loaders = [
    'loadGovernance', 'loadSDLC', 'loadProcurement', 'loadGuardrails',
    'loadISOStandardsModule', 'loadAICloudModule', 'loadAgenticAI',
    'loadOperations', 'loadCryptoTools', 'loadInfrastructure', 'loadSecOps',
    'loadVault', 'loadStrategy', 'loadAnalyticsHub', 'loadInternalSupport',
    'loadITSM', 'loadTeams', 'loadSharePoint', 'loadTraining',
    'loadClientPortal', 'loadVendorPortal'
]

results = {}
for name in target_loaders:
    code = get_function(name)
    if code:
        urls = list(set(re.findall(r'[\'\"`](/api/v1/[^\'\"`\s\?]+|\$\{API_BASE\}/[^\'\"`\s\?]+)', code)))
        results[name] = {
            "found": True,
            "urls": urls,
            "lines": len(code.splitlines()),
            "preview": code[:500]
        }
    else:
        results[name] = {"found": False}

print(json.dumps(results, indent=2))
