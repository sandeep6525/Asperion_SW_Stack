import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace API_BASE with '/api/v1'
# Add import of formatINR and formatDate
header = """// Unified Live Data Loaders for Asperion Enterprise OS
import { formatINR, formatDate } from './formatters.ts';

const API_BASE = '/api/v1';

// Global placeholder for window.Chart if needed
declare const Chart: any;
"""

# Let's extract the load functions
loader_names = [
    'loadGovernance',
    'loadFinance',
    'loadSecOps',
    'loadInfrastructure',
    'loadProcurement',
    'loadSDLC',
    'loadStrategy',
    'loadVault',
    'loadAnalyticsHub',
    'loadInternalSupport',
    'loadITSM',
    'loadOperations',
    'loadTraining',
    'loadSharePoint',
    'loadGuardrails',
    'loadISOStandardsModule',
    'loadClientPortal',
    'loadVendorPortal',
    'loadEmployeePortal',
    'loadTeams',
    'loadCryptoTools',
]

extracted_blocks = []

for name in loader_names:
    pattern = re.compile(rf'(?:async\s+)?function\s+{name}\s*\([^)]*\)\s*\{{', re.DOTALL)
    m = pattern.search(js)
    if not m:
        print(f"Loader {name} not found!")
        continue
    start = m.start()
    
    # Count braces to find end of function
    brace_count = 0
    in_str = None
    end = start
    for i in range(m.end() - 1, len(js)):
        ch = js[i]
        if in_str:
            if ch == in_str and js[i-1] != '\\':
                in_str = None
        else:
            if ch in ('"', "'", '`'):
                in_str = ch
            elif ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
    
    func_code = js[start:end]
    # Ensure export async function
    func_code = re.sub(r'^(?:async\s+)?function\s+', 'export async function ', func_code)
    extracted_blocks.append(func_code)
    print(f"Extracted {name} ({len(func_code)} chars)")

with open('frontend/src/utils/dataLoaders.ts', 'w', encoding='utf-8') as f:
    f.write(header + '\n\n' + '\n\n'.join(extracted_blocks) + '\n')

print("Created frontend/src/utils/dataLoaders.ts successfully.")
