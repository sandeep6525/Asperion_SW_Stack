import re

with open("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/utils/dataLoaders.js", "r", encoding="utf-8") as f:
    content = f.read()

matches = re.findall(r"fetch\([`'\"](\$\{API_BASE\}|/api/v1)([^`'\"]+)[`'\"]\)", content)
unique_eps = sorted(set(m[1] for m in matches))
print(f"Total unique fetch endpoints in dataLoaders.js: {len(unique_eps)}")
for ep in unique_eps:
    print(ep)
