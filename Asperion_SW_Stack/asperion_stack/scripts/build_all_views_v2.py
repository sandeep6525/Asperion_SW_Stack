import os
import subprocess
from html_to_jsx_lib_v2 import convert_html_robust

VIEWS = [
    {
        'html': 'view-analytics.html',
        'comp': 'AnalyticsView',
        'file': 'AnalyticsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchAnalyticsTab',
            'default_tab': 'fin',
            'tabs': ['fin', 'pmo', 'talent', 'secops', 'strategy', 'sim', 'datascience', 'decision', 'montecarlo', 'infographics'],
            'pane_prefix': 'analytics-pane-'
        }
    },
    {
        'html': 'view-secops.html',
        'comp': 'SecOpsView',
        'file': 'SecOpsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchSecOpsTab',
            'default_tab': 'incidents',
            'tabs': ['incidents', 'alerts', 'evidence', 'threat-intel', 'playbooks', 'vulns', 'drills', 'cert-in'],
            'pane_prefix': 'secops-tab-content-'
        }
    },
    {
        'html': 'view-infrastructure.html',
        'comp': 'InfrastructureView',
        'file': 'InfrastructureView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchInfraTab',
            'default_tab': 'passkeys',
            'tabs': ['passkeys', 'ztna', 'dr', 'hardware', 'cloud', 'certs', 'checklists'],
            'pane_prefix': 'infra-tab-content-'
        }
    },
    {
        'html': 'view-itsm.html',
        'comp': 'ITSMView',
        'file': 'ITSMView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchITSMTab',
            'default_tab': 'cmdb',
            'tabs': ['cmdb', 'problems', 'cab', 'runbooks', 'loi'],
            'pane_prefix': 'itsm-subview-'
        }
    },
    {
        'html': 'view-operations.html',
        'comp': 'OperationsView',
        'file': 'OperationsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchOperationsTab',
            'default_tab': 'ledger',
            'tabs': ['ledger', 'bcp-dr', 'dpdp', 'telemetry'],
            'pane_prefix': 'ops-tab-'
        }
    },
    {
        'html': 'view-crypto-tools.html',
        'comp': 'CryptoToolsView',
        'file': 'CryptoToolsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchCryptoTab',
            'default_tab': 'hashing',
            'tabs': ['hashing', 'aes-gcm', 'signatures', 'merkle'],
            'pane_prefix': 'crypto-tab-'
        }
    },
    {
        'html': 'view-portal-client.html',
        'comp': 'ClientPortalView',
        'file': 'ClientPortalView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchClientPortalTab',
            'default_tab': 'deliverables',
            'tabs': ['deliverables', 'billing', 'sla-tickets', 'change-orders', 'contracts'],
            'pane_prefix': 'client-tab-content-'
        }
    },
    {
        'html': 'view-portal-employee.html',
        'comp': 'EmployeePortalView',
        'file': 'EmployeePortalView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchESSTab',
            'default_tab': 'cockpit',
            'tabs': ['cockpit', 'compensation', 'attendance', 'leaves', 'learning', 'assets'],
            'pane_prefix': 'ess-tab-'
        }
    },
    {
        'html': 'view-portal-vendor.html',
        'comp': 'VendorPortalView',
        'file': 'VendorPortalView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchVendorPortalTab',
            'default_tab': 'pos',
            'tabs': ['pos', 'grns', 'bills', 'rfx', 'contracts', 'scorecards'],
            'pane_prefix': 'vendor-tab-content-'
        }
    },
    {
        'html': 'view-training.html',
        'comp': 'TrainingView',
        'file': 'TrainingView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchTrainingTab',
            'default_tab': 'tracks',
            'tabs': ['tracks', 'catalog', 'materials', 'enrolled', 'probation', 'intelligence'],
            'pane_prefix': 'trn-tab-content-'
        }
    },
    {
        'html': 'view-sharepoint.html',
        'comp': 'SharePointView',
        'file': 'SharePointView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchSharePointTab',
            'default_tab': 'sops',
            'tabs': ['sops', 'thoughts', 'methods', 'qa', 'documents'],
            'pane_prefix': 'sp-tab-content-'
        }
    },
    {
        'html': 'view-guardrails.html',
        'comp': 'GuardrailsView',
        'file': 'GuardrailsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchGuardrailTab',
            'default_tab': 'rules',
            'tabs': ['rules', 'flowcharts', 'blueprints', 'logs', 'docs'],
            'pane_prefix': 'guardrail-panel-'
        }
    },
    {
        'html': 'view-iso-standards.html',
        'comp': 'ISOStandardsView',
        'file': 'ISOStandardsView.tsx',
        'cfg': {
            'tab_switch_fn': 'switchISOTab',
            'default_tab': 'certs',
            'tabs': ['certs', 'controls', 'audits', 'capas', 'grievances'],
            'pane_prefix': 'iso-panel-'
        }
    },
    {
        'html': 'view-crm.html',
        'comp': 'CRMView',
        'file': 'CRMView.tsx',
        'cfg': None
    },
    {
        'html': 'view-finance.html',
        'comp': 'FinanceView',
        'file': 'FinanceView.tsx',
        'cfg': None
    },
    {
        'html': 'view-governance.html',
        'comp': 'GovernanceView',
        'file': 'GovernanceView.tsx',
        'cfg': None
    },
    {
        'html': 'view-procurement.html',
        'comp': 'ProcurementView',
        'file': 'ProcurementView.tsx',
        'cfg': None
    },
    {
        'html': 'view-sdlc.html',
        'comp': 'SDLCView',
        'file': 'SDLCView.tsx',
        'cfg': None
    },
    {
        'html': 'view-strategy.html',
        'comp': 'StrategyView',
        'file': 'StrategyView.tsx',
        'cfg': None
    },
    {
        'html': 'view-teams.html',
        'comp': 'TeamsView',
        'file': 'TeamsView.tsx',
        'cfg': None
    },
    {
        'html': 'view-internal-support.html',
        'comp': 'InternalSupportView',
        'file': 'InternalSupportView.tsx',
        'cfg': None
    },
    {
        'html': 'view-vault.html',
        'comp': 'VaultView',
        'file': 'VaultView.tsx',
        'cfg': None
    }
]

out_dir = 'frontend/src/views'

for item in VIEWS:
    html_file = os.path.join('extracted_views', item['html'])
    if not os.path.exists(html_file):
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        raw_html = f.read()
    
    comp_name = item['comp']
    cfg = item['cfg']
    
    jsx_body = convert_html_robust(raw_html, cfg)
    
    default_tab = cfg.get('default_tab', '') if cfg else ''
    tab_state_code = f"  const [activeTab, setActiveTab] = useState<string>('{default_tab}');\n" if default_tab else ""
    
    template = f"""import React, {{ useState, useEffect }} from 'react';
import axios from 'axios';

export const {comp_name}: React.FC = () => {{
{tab_state_code}  useEffect(() => {{
    // Live module data integration
  }}, []);

  return (
    <div className="w-full">
      {jsx_body}
    </div>
  );
}};

export default {comp_name};
"""
    
    out_file = os.path.join(out_dir, item['file'])
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Generated {item['file']}")

print("All views converted.")
