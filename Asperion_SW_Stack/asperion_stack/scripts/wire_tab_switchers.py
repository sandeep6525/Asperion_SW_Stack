import os
import re

views_to_update = [
    ("OperationsView.tsx", "loadOperations", "switchOperationsTab"),
    ("ITSMView.tsx", "loadITSM", "switchITSMTab"),
    ("InfrastructureView.tsx", "loadInfrastructure", "switchInfraTab"),
    ("SecOpsView.tsx", "loadSecOps", "switchSecOpsTab"),
    ("CryptoToolsView.tsx", "loadCryptoTools", "switchCryptoTab"),
    ("SharePointView.tsx", "loadSharePoint", "switchSharePointTab"),
    ("TrainingView.tsx", "loadTraining", "switchTrainingTab"),
    ("GuardrailsView.tsx", "loadGuardrails", "switchGuardrailTab"),
    ("AnalyticsView.tsx", "loadAnalyticsHub", "switchAnalyticsTab"),
    ("EmployeePortalView.tsx", "loadEmployeePortal", "switchESSTab"),
    ("VendorPortalView.tsx", "loadVendorPortal", "switchVendorPortalTab"),
    ("ClientPortalView.tsx", "loadClientPortal", "switchClientPortalTab"),
]

base_dir = "E:/Asperion_SW_Stack/Asperion_SW_Stack/Asperion_SW_Stack/asperion_stack/frontend/src/views"

for fname, load_fn, switch_fn in views_to_update:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update import
    old_import_pat = r"//\s*@ts-ignore\s*\nimport\s*\{[^}]*\}\s*from\s*['\"]\.\./utils/dataLoaders\.js['\"];?"
    new_import = f"// @ts-ignore\nimport {{ {load_fn}, {switch_fn} }} from '../utils/dataLoaders.js';"
    
    if re.search(old_import_pat, content):
        content = re.sub(old_import_pat, new_import, content, count=1)
    else:
        content = new_import + "\n" + content

    # 2. Add or update activeTab useEffect
    if f"{switch_fn}(activeTab)" not in content:
        pat2 = r"(useEffect\(\(\)\s*=>\s*\{[\s\S]*?" + load_fn + r"[\s\S]*?\}\s*,\s*\[\]\);)"
        tab_hook = f"\n\n  useEffect(() => {{\n    try {{\n      {switch_fn}(activeTab);\n    }} catch (e) {{\n      console.error('Error in {switch_fn}:', e);\n    }}\n  }}, [activeTab]);"
        content = re.sub(pat2, r"\1" + tab_hook, content, count=1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {fname} with {switch_fn}(activeTab)")

print("Completed updating tab switchers in views.")
