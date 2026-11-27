import re

with open('app/static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's find all function declarations
pattern = re.compile(r'((?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{)', re.DOTALL)

matches = list(pattern.finditer(js))
print(f"Total function declarations found: {len(matches)}")

extracted = []
exported_names = []

for idx, m in enumerate(matches):
    fn_name = m.group(2)
    start = m.start()
    
    # Only extract relevant functions (loaders, renderers, switchers, filters, calculators, helpers)
    # Actually, we can extract any function starting with load, render, switch, filter, populate, handle
    prefixes = ('load', 'render', 'switch', 'filter', 'populate', 'format', 'show', 'toggle', 'calculate')
    if not any(fn_name.startswith(p) for p in prefixes):
        continue
    
    # Find matching closing brace
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
                    
    body = js[start:end]
    # Make it an export
    body = re.sub(r'^(?:async\s+)?function\s+', 'export async function ', body)
    extracted.append(body)
    exported_names.append(fn_name)

print(f"Extracted {len(extracted)} complete functions!")

# Also extract global variables defined in app.js like cached... or current...
vars_pattern = re.compile(r'^(?:let|var|const)\s+([a-zA-Z0-9_]+)\s*=[^;\n]+;', re.MULTILINE)
global_vars = []
for vm in vars_pattern.finditer(js):
    var_line = vm.group(0)
    var_name = vm.group(1)
    if any(var_name.startswith(p) for p in ('cached', 'current', 'active', 'API_BASE', 'teams', 'iso', 'guardrail')):
        if 'API_BASE' in var_name:
            continue
        global_vars.append(f"export let {var_name} = null;")

header = """// Unified Complete Live Data Loaders for Asperion Enterprise OS
import { formatINR, formatDate } from './formatters';

const API_BASE = '/api/v1';

""" + '\n'.join(set(global_vars)) + "\n\n"

with open('frontend/src/utils/dataLoaders.js', 'w', encoding='utf-8') as f:
    f.write(header + '\n\n' + '\n\n'.join(extracted) + '\n')

print(f"Written frontend/src/utils/dataLoaders.js ({len(exported_names)} exports)")
