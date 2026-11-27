export interface NavItem {
  target: string;
  label: string;
  icon: string;
  badge?: {
    id: string;
    text: string;
    className: string;
  };
  endpoint?: string;
  category: 'Operating Modules' | 'Dedicated Portals';
}

export const ALL_NAV_ITEMS: NavItem[] = [
  // 24 Operating Modules
  { target: 'dashboard', label: 'Executive MIS', icon: 'fa-solid fa-chart-pie', category: 'Operating Modules', endpoint: '/api/v1/analytics/executive-ratios' },
  { target: 'governance', label: 'Governance & OPC', icon: 'fa-solid fa-scale-balanced', category: 'Operating Modules', endpoint: '/api/v1/governance/entities' },
  { target: 'crm', label: 'CRM & Contracting', icon: 'fa-solid fa-handshake', category: 'Operating Modules', endpoint: '/api/v1/crm-enterprise/pipeline-summary' },
  { target: 'finance', label: 'Finance, Tax & AP/AR', icon: 'fa-solid fa-file-invoice-dollar', category: 'Operating Modules', endpoint: '/api/v1/finance/invoices' },
  { target: 'hrms', label: 'HRMS & CTC Engine', icon: 'fa-solid fa-users-gear', category: 'Operating Modules', endpoint: '/api/v1/hrms/employees' },
  { target: 'pmo', label: 'PMO & Delivery', icon: 'fa-solid fa-diagram-project', category: 'Operating Modules', endpoint: '/api/v1/pmo/projects' },
  { target: 'sdlc', label: 'SDLC & DevSecOps', icon: 'fa-solid fa-code-branch text-cyan-400', category: 'Operating Modules', endpoint: '/api/v1/sdlc/repositories' },
  { target: 'procurement', label: 'Vendor Procurement', icon: 'fa-solid fa-truck-ramp-box', category: 'Operating Modules', endpoint: '/api/v1/procurement/vendors' },
  { target: 'guardrails', label: 'Guardrails & Architectures', icon: 'fa-solid fa-shield-virus text-teal-400', category: 'Operating Modules', endpoint: '/api/v1/guardrails/rules' },
  { target: 'iso-standards', label: 'ISO Standards & QMS', icon: 'fa-solid fa-certificate text-amber-400', category: 'Operating Modules', endpoint: '/api/v1/iso/standards' },
  { target: 'ai-cloud', label: 'AI APIs, MCPs & Multi-Cloud', icon: 'fa-solid fa-microchip text-violet-400', category: 'Operating Modules', endpoint: '/api/v1/ai-cloud/endpoints' },
  { target: 'agentic-ai', label: 'Agentic AI & Swarm', icon: 'fa-solid fa-robot text-purple-400', category: 'Operating Modules', badge: { id: 'agentic-ai-sidebar-badge', text: 'SWARM', className: 'bg-purple-500/30 text-purple-300 border-purple-500/40' }, endpoint: '/api/v1/agentic-ai/agents' },
  { target: 'operations', label: 'Operations & BCP/DR Ledger', icon: 'fa-solid fa-cube text-cyan-400', category: 'Operating Modules', badge: { id: 'operations-sidebar-badge', text: 'SHA256', className: 'bg-cyan-500/30 text-cyan-300 border-cyan-500/40' }, endpoint: '/api/v1/operations/bcp-plans' },
  { target: 'crypto-tools', label: 'Cryptography & PKI Tools', icon: 'fa-solid fa-key text-emerald-400', category: 'Operating Modules', badge: { id: 'crypto-sidebar-badge', text: 'FIPS', className: 'bg-emerald-500/30 text-emerald-300 border-emerald-500/40' }, endpoint: '/api/v1/crypto/keys' },
  { target: 'infrastructure', label: 'IT, Cloud & Passkeys', icon: 'fa-solid fa-server', category: 'Operating Modules', endpoint: '/api/v1/infrastructure/assets' },
  { target: 'secops', label: 'SecOps & CERT-In War Room', icon: 'fa-solid fa-shield-halved', category: 'Operating Modules', endpoint: '/api/v1/secops/incidents' },
  { target: 'vault', label: 'Master Document Vault', icon: 'fa-solid fa-folder-tree text-amber-400', category: 'Operating Modules', endpoint: '/api/v1/vault/documents' },
  { target: 'strategy', label: 'Strategy, KPIs & Decisions', icon: 'fa-solid fa-chess text-cyan-400', category: 'Operating Modules', endpoint: '/api/v1/strategy/kpis' },
  { target: 'analytics', label: 'Visual Intelligence Hub', icon: 'fa-solid fa-chart-line text-emerald-400', category: 'Operating Modules', endpoint: '/api/v1/analytics/executive-ratios' },
  { target: 'internal-support', label: 'Internal Service Desk & Alerts', icon: 'fa-solid fa-headset text-purple-400', category: 'Operating Modules', endpoint: '/api/v1/tickets/' },
  { target: 'itsm', label: 'ITSM & CMDB Operations', icon: 'fa-solid fa-network-wired text-cyan-400', category: 'Operating Modules', badge: { id: 'itsm-sidebar-badge', text: 'ITIL v4', className: 'bg-cyan-500/30 text-cyan-300 border-cyan-500/40' }, endpoint: '/api/v1/itsm/incidents' },
  { target: 'teams', label: 'Asperion Teams & Chat', icon: 'fa-solid fa-comments text-indigo-400', category: 'Operating Modules', badge: { id: 'teams-sidebar-badge', text: 'LIVE', className: 'bg-indigo-500/30 text-indigo-300 border-indigo-500/40' }, endpoint: '/api/v1/communications/channels' },
  { target: 'sharepoint', label: 'Asperion SharePoint & SOPs', icon: 'fa-solid fa-shapes text-teal-400', category: 'Operating Modules', badge: { id: 'sharepoint-sidebar-badge', text: 'HUB', className: 'bg-teal-500/30 text-teal-300 border-teal-500/40' }, endpoint: '/api/v1/sharepoint/articles' },
  { target: 'training', label: 'Training & Joinee Academy', icon: 'fa-solid fa-graduation-cap text-amber-400', category: 'Operating Modules', badge: { id: 'training-sidebar-badge', text: 'LMS', className: 'bg-amber-500/30 text-amber-300 border-amber-500/40' }, endpoint: '/api/v1/training/tracks' },

  // 3 Dedicated Portals
  { target: 'portal-employee', label: 'Employee Portal (ESS)', icon: 'fa-solid fa-user-tie text-blue-400', category: 'Dedicated Portals', endpoint: '/api/v1/portals/employee/dashboard-data?emp_code=EMP001' },
  { target: 'portal-client', label: 'Client SLA Portal', icon: 'fa-solid fa-handshake-angle text-emerald-400', category: 'Dedicated Portals', endpoint: '/api/v1/portals/client/overview' },
  { target: 'portal-vendor', label: 'Vendor Sourcing Portal', icon: 'fa-solid fa-truck-moving text-amber-400', category: 'Dedicated Portals', endpoint: '/api/v1/portals/vendor/overview' },
];
