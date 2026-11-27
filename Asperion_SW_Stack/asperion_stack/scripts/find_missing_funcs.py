import re

with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/utils/dataLoaders.js", "r", encoding="utf-8") as f:
    code = f.read()

# Find all function definitions
defined = set(re.findall(r"(?:function\s+([a-zA-Z0-9_$]+)|let\s+([a-zA-Z0-9_$]+)|const\s+([a-zA-Z0-9_$]+)|var\s+([a-zA-Z0-9_$]+))", code))
defined_names = set()
for g in defined:
    for name in g:
        if name:
            defined_names.add(name)

# Find all potential function calls like name(...)
called = set(re.findall(r"([a-zA-Z0-9_$]+)\s*\(", code))

# Exclude JS builtins and keywords
builtins = {
    'if', 'for', 'while', 'catch', 'switch', 'return', 'function', 'import', 'export',
    'fetch', 'Promise', 'all', 'then', 'catch', 'json', 'map', 'join', 'filter', 'find',
    'forEach', 'push', 'slice', 'splice', 'trim', 'split', 'replace', 'toLowerCase', 'toUpperCase',
    'getElementById', 'querySelector', 'querySelectorAll', 'setAttribute', 'getAttribute', 'addEventListener',
    'removeEventListener', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval', 'alert', 'confirm',
    'prompt', 'parseInt', 'parseFloat', 'isNaN', 'isFinite', 'encodeURIComponent', 'decodeURIComponent',
    'console', 'log', 'warn', 'error', 'info', 'table', 'dir', 'String', 'Number', 'Boolean', 'Array',
    'Object', 'keys', 'values', 'entries', 'assign', 'Math', 'round', 'floor', 'ceil', 'abs', 'max', 'min',
    'random', 'Date', 'now', 'getTime', 'toISOString', 'toLocaleDateString', 'toLocaleString', 'JSON',
    'stringify', 'parse', 'RegExp', 'Error', 'TypeError', 'ReferenceError', 'URLSearchParams', 'FormData',
    'Blob', 'FileReader', 'Headers', 'Request', 'Response', 'btoa', 'atob', 'crypto', 'subtle', 'digest',
    'getRandomValues', 'importKey', 'exportKey', 'sign', 'verify', 'encrypt', 'decrypt', 'Uint8Array',
    'ArrayBuffer', 'DataView', 'TextEncoder', 'TextDecoder', 'padStart', 'padEnd', 'includes', 'indexOf',
    'lastIndexOf', 'startsWith', 'endsWith', 'some', 'every', 'reduce', 'reduceRight', 'flat', 'flatMap',
    'concat', 'toString', 'valueOf', 'formatINR', 'formatDate', 'safeRenderChart', 'escapeHtml'
}

missing = []
for c in sorted(called):
    if c not in defined_names and c not in builtins:
        missing.append(c)

print("Undefined calls in dataLoaders.js:")
for m in missing:
    print(" -", m)
