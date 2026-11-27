import re

input_path = "E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/app/static/js/app.js"
output_path = "E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/utils/dataLoaders.js"

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Wrap DOMContentLoaded in an exportable function so it DOES NOT execute at module import time
text = text.replace(
    "document.addEventListener('DOMContentLoaded', () => {",
    "export function initLegacyApp() {\n    // In React, components invoke their own loaders upon mounting in useEffect\n    if (typeof document === 'undefined') return;"
)
text = text.replace(
    "        );\n    }, 1200);\n});",
    "        );\n    }, 1200);\n}"
)

# Guard bare document.addEventListener('click'
text = text.replace(
    "document.addEventListener('click', (e) => {",
    "if (typeof document !== 'undefined') document.addEventListener('click', (e) => {"
)
text = text.replace(
    "    if (bellBtn && dropdown && !bellBtn.contains(e.target) && !dropdown.contains(e.target)) {\n        dropdown.classList.add('hidden');\n    }\n});",
    "    if (bellBtn && dropdown && !bellBtn.contains(e.target) && !dropdown.contains(e.target)) {\n        dropdown.classList.add('hidden');\n    }\n});\n"
)

# Fix bare `event && event.currentTarget`
text = re.sub(
    r"\bif\s*\(\s*event\s*&&\s*event\.currentTarget\s*\)",
    "if (typeof window !== 'undefined' && window.event && window.event.currentTarget)",
    text
)

# Initialize tab variables to default values instead of null
text = text.replace("let currentITSMTab = null;", "let currentITSMTab = 'cmdb';")
text = text.replace("let currentTrainingTab = null;", "let currentTrainingTab = 'tracks';")
text = text.replace("let currentCryptoTab = null;", "let currentCryptoTab = 'hashing';")
text = text.replace("let currentAnalyticsTab = null;", "let currentAnalyticsTab = 'fin';")

# 2. Extract all function names to export and attach to window
func_matches = re.findall(r"^(?:async\s+)?function\s+([a-zA-Z0-9_$]+)\s*\(", text, re.MULTILINE)
let_matches = re.findall(r"^let\s+([a-zA-Z0-9_$]+)\s*=", text, re.MULTILINE)

all_funcs = sorted(set(func_matches))
all_lets = sorted(set(let_matches))

# 3. Add export to functions and lets and formatters
text = re.sub(r"^(async\s+function\s+)", r"export \1", text, flags=re.MULTILINE)
text = re.sub(r"^(function\s+)", r"export \1", text, flags=re.MULTILINE)
text = re.sub(r"^(let\s+)", r"export \1", text, flags=re.MULTILINE)
text = re.sub(r"^(const\s+formatINR\s*=)", r"export \1", text, flags=re.MULTILINE)
text = re.sub(r"^(const\s+formatDate\s*=)", r"export \1", text, flags=re.MULTILINE)

# 4. Header with explanation
header = """// Unified Complete Live Data Loaders for Asperion Enterprise OS
// Complete implementation of all 27 enterprise operating modules & portals

"""

text = header + text

# 5. Append window bindings at the end so all inline onclick handlers in HTML/JSX can find them
footer = "\n\n// Expose all functions to global window for template event handlers\n"
footer += "if (typeof window !== 'undefined') {\n"
for fn in all_funcs:
    footer += f"    window.{fn} = {fn};\n"
for l in all_lets:
    footer += f"    window.{l} = {l};\n"
footer += "    window.formatINR = formatINR;\n"
footer += "    window.formatDate = formatDate;\n"
footer += "}\n"

text += footer

with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully generated {output_path} with {len(text.splitlines())} lines.")
