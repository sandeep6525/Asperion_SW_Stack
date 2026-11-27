import glob
import re

for filepath in glob.glob("E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/views/*.tsx"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match elements with style={{ display: activeTab ... }} and className containing 'hidden'
    # e.g. className="infra-tab-panel hidden" -> className="infra-tab-panel"
    # e.g. className="hidden space-y-4" -> className="space-y-4"
    # e.g. className="hidden" -> className=""
    
    def replacer(match):
        full = match.group(0)
        # remove standalone 'hidden' word from className inside this tag
        cleaned = re.sub(r'className=(["\'])(.*?)\bhidden\b(.*?)\1', lambda m: f'className={m.group(1)}{m.group(2).strip()} {m.group(3).strip()}{m.group(1)}'.replace('  ', ' ').replace('className=""', ''), full)
        return cleaned

    # Match opening tag containing style={{ display: activeTab ... }}
    pattern = r'<div[^>]*style=\{\{\s*display:\s*activeTab[^>]*>[^<]*'
    new_content = re.sub(pattern, replacer, content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Cleaned hidden class from: {filepath}")

print("Done cleaning hidden classes.")
