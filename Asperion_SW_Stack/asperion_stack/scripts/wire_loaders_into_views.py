import os
import re

MAPPING = {
    'FinanceView.tsx': 'loadFinance',
    'GovernanceView.tsx': 'loadGovernance',
    'SecOpsView.tsx': 'loadSecOps',
    'InfrastructureView.tsx': 'loadInfrastructure',
    'ProcurementView.tsx': 'loadProcurement',
    'SDLCView.tsx': 'loadSDLC',
    'StrategyView.tsx': 'loadStrategy',
    'VaultView.tsx': 'loadVault',
    'AnalyticsView.tsx': 'loadAnalyticsHub',
    'InternalSupportView.tsx': 'loadInternalSupport',
    'ITSMView.tsx': 'loadITSM',
    'OperationsView.tsx': 'loadOperations',
    'TrainingView.tsx': 'loadTraining',
    'SharePointView.tsx': 'loadSharePoint',
    'GuardrailsView.tsx': 'loadGuardrails',
    'ISOStandardsView.tsx': 'loadISOStandardsModule',
    'ClientPortalView.tsx': 'loadClientPortal',
    'VendorPortalView.tsx': 'loadVendorPortal',
    'EmployeePortalView.tsx': 'loadEmployeePortal',
    'TeamsView.tsx': 'loadTeams',
    'CryptoToolsView.tsx': 'loadCryptoTools',
}

views_dir = 'frontend/src/views'

for filename, loader in MAPPING.items():
    filepath = os.path.join(views_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add import if not present
    if loader not in content:
        import_stmt = f"// @ts-ignore\nimport {{ {loader} }} from '../utils/dataLoaders.js';\n"
        content = import_stmt + content
        
        # 2. Add loader call in useEffect
        pattern = re.compile(r'useEffect\(\(\)\s*=>\s*\{([^}]*)\},\s*\[\]\);', re.DOTALL)
        m = pattern.search(content)
        if m:
            old_body = m.group(0)
            new_body = f"useEffect(() => {{\n    try {{\n      {loader}();\n    }} catch (e) {{\n      console.error('Error in {loader}:', e);\n    }}\n  }}, []);"
            content = content.replace(old_body, new_body, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Wired {loader} into {filename}")
    else:
        print(f"{loader} already in {filename}")

print("Wiring completed.")
