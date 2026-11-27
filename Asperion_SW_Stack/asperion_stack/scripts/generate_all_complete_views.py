import os
import re

VIEWS_CONFIG = {
    'view-analytics.html': {
        'comp': 'AnalyticsView',
        'file': 'AnalyticsView.tsx',
        'tab_switch_fn': 'switchAnalyticsTab',
        'default_tab': 'fin',
        'tabs': ['fin', 'pmo', 'talent', 'secops', 'strategy', 'sim', 'datascience', 'decision', 'montecarlo', 'infographics'],
        'pane_prefix': 'analytics-pane-',
        'btn_prefix': 'btn-tab-'
    },
    'view-secops.html': {
        'comp': 'SecOpsView',
        'file': 'SecOpsView.tsx',
        'tab_switch_fn': 'switchSecOpsTab',
        'default_tab': 'incidents',
        'tabs': ['incidents', 'alerts', 'evidence', 'threat-intel', 'playbooks', 'vulns', 'drills', 'cert-in'],
        'pane_prefix': 'secops-tab-content-',
        'btn_prefix': 'secops-tab-btn-'
    },
    'view-infrastructure.html': {
        'comp': 'InfrastructureView',
        'file': 'InfrastructureView.tsx',
        'tab_switch_fn': 'switchInfraTab',
        'default_tab': 'passkeys',
        'tabs': ['passkeys', 'ztna', 'dr', 'hardware', 'cloud', 'certs', 'checklists'],
        'pane_prefix': 'infra-tab-content-',
        'btn_prefix': 'infra-tab-btn-'
    },
    'view-itsm.html': {
        'comp': 'ITSMView',
        'file': 'ITSMView.tsx',
        'tab_switch_fn': 'switchITSMTab',
        'default_tab': 'cmdb',
        'tabs': ['cmdb', 'problems', 'cab', 'runbooks', 'loi'],
        'pane_prefix': 'itsm-subview-',
        'btn_prefix': 'itsm-tab-btn-'
    },
    'view-operations.html': {
        'comp': 'OperationsView',
        'file': 'OperationsView.tsx',
        'tab_switch_fn': 'switchOperationsTab',
        'default_tab': 'ledger',
        'tabs': ['ledger', 'bcp-dr', 'dpdp', 'telemetry'],
        'pane_prefix': 'ops-tab-',
        'btn_prefix': 'ops-tab-btn-'
    },
    'view-crypto-tools.html': {
        'comp': 'CryptoToolsView',
        'file': 'CryptoToolsView.tsx',
        'tab_switch_fn': 'switchCryptoTab',
        'default_tab': 'hashing',
        'tabs': ['hashing', 'aes-gcm', 'signatures', 'merkle'],
        'pane_prefix': 'crypto-tab-',
        'btn_prefix': 'crypto-tab-btn-'
    },
    'view-portal-client.html': {
        'comp': 'ClientPortalView',
        'file': 'ClientPortalView.tsx',
        'tab_switch_fn': 'switchClientPortalTab',
        'default_tab': 'deliverables',
        'tabs': ['deliverables', 'billing', 'sla-tickets', 'change-orders', 'contracts'],
        'pane_prefix': 'client-tab-content-',
        'btn_prefix': 'tab-btn-client-'
    },
    'view-portal-employee.html': {
        'comp': 'EmployeePortalView',
        'file': 'EmployeePortalView.tsx',
        'tab_switch_fn': 'switchESSTab',
        'default_tab': 'cockpit',
        'tabs': ['cockpit', 'compensation', 'attendance', 'leaves', 'learning', 'assets'],
        'pane_prefix': 'ess-tab-',
        'btn_prefix': 'tab-btn-ess-'
    },
    'view-portal-vendor.html': {
        'comp': 'VendorPortalView',
        'file': 'VendorPortalView.tsx',
        'tab_switch_fn': 'switchVendorPortalTab',
        'default_tab': 'pos',
        'tabs': ['pos', 'grns', 'bills', 'rfx', 'contracts', 'scorecards'],
        'pane_prefix': 'vendor-tab-content-',
        'btn_prefix': 'vendor-tab-btn-'
    },
    'view-training.html': {
        'comp': 'TrainingView',
        'file': 'TrainingView.tsx',
        'tab_switch_fn': 'switchTrainingTab',
        'default_tab': 'tracks',
        'tabs': ['tracks', 'catalog', 'materials', 'enrolled', 'probation', 'intelligence'],
        'pane_prefix': 'trn-tab-content-',
        'btn_prefix': 'trn-tab-btn-'
    },
    'view-sharepoint.html': {
        'comp': 'SharePointView',
        'file': 'SharePointView.tsx',
        'tab_switch_fn': 'switchSharePointTab',
        'default_tab': 'sops',
        'tabs': ['sops', 'thoughts', 'methods', 'qa', 'documents'],
        'pane_prefix': 'sp-tab-content-',
        'btn_prefix': 'sp-tab-btn-'
    },
    'view-guardrails.html': {
        'comp': 'GuardrailsView',
        'file': 'GuardrailsView.tsx',
        'tab_switch_fn': 'switchGuardrailTab',
        'default_tab': 'rules',
        'tabs': ['rules', 'flowcharts', 'blueprints', 'logs', 'docs'],
        'pane_prefix': 'guardrail-panel-',
        'btn_prefix': 'tab-guardrail-'
    },
    'view-iso-standards.html': {
        'comp': 'ISOStandardsView',
        'file': 'ISOStandardsView.tsx',
        'tab_switch_fn': 'switchISOTab',
        'default_tab': 'certs',
        'tabs': ['certs', 'controls', 'audits', 'capas', 'grievances'],
        'pane_prefix': 'iso-panel-',
        'btn_prefix': 'tab-iso-'
    },
}

print(f"Configured {len(VIEWS_CONFIG)} rich tabbed views.")
