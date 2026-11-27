with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/utils/dataLoaders.js", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.finditer(r"export function switch([a-zA-Z0-9]+Tab)\(([^)]+)\)\s*\{", text)

for m in matches:
    name = m.group(1)
    args = m.group(2)
    start = m.start()
    end = text.find("}\n\n", start)
    if end == -1: end = start + 800
    print(f"=== {name}({args}) ===")
    print(text[start:end])
    print()
