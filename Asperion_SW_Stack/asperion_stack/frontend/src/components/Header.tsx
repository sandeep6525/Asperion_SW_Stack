import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface HeaderProps {
  onToggleMobileSidebar: () => void;
  persona: string;
  onSwitchPersona: (p: string) => void;
  onNavigate?: (module: string) => void;
}

interface CommandItem {
  category: string;
  title: string;
  target: string;
  icon: string;
  badge?: string;
}

const COMMAND_LIST: CommandItem[] = [
  // Primary Operating Modules
  { category: 'Operating Modules', title: 'Executive MIS & Board Telemetry', target: 'dashboard', icon: 'fa-chart-pie', badge: 'Core' },
  { category: 'Operating Modules', title: 'Corporate Governance & Statutory OPC', target: 'governance', icon: 'fa-scale-balanced', badge: 'MCA21' },
  { category: 'Operating Modules', title: 'Enterprise CRM, Pipeline & Contracting', target: 'crm', icon: 'fa-handshake', badge: 'Revenue' },
  { category: 'Operating Modules', title: 'Finance, AP/AR & Statutory Compliance', target: 'finance', icon: 'fa-file-invoice-dollar', badge: 'GST/TDS' },
  { category: 'Operating Modules', title: 'HRMS, Wage Code & CTC Engine', target: 'hrms', icon: 'fa-users-gear', badge: 'People' },
  { category: 'Operating Modules', title: 'PMO, Project Delivery & EVM', target: 'pmo', icon: 'fa-diagram-project', badge: 'Agile' },
  { category: 'Operating Modules', title: 'SDLC, DevSecOps & CI/CD Pipelines', target: 'sdlc', icon: 'fa-code-branch', badge: 'DevSecOps' },
  { category: 'Operating Modules', title: 'Vendor Procurement & Sourcing', target: 'procurement', icon: 'fa-truck-ramp-box', badge: 'Procure' },
  { category: 'Operating Modules', title: 'Guardrails & Architectural Flowcharts', target: 'guardrails', icon: 'fa-shield-halved', badge: 'Rules' },
  { category: 'Operating Modules', title: 'ISO Standards & QMS Quality Assurance', target: 'iso-standards', icon: 'fa-award', badge: '5x ISO' },
  { category: 'Operating Modules', title: 'AI APIs, MCP Tool Bridges & Multi-Cloud', target: 'ai-cloud', icon: 'fa-microchip', badge: 'MCP/Cloud' },
  { category: 'Operating Modules', title: 'Agentic AI Swarm & Autonomous Execution', target: 'agentic-ai', icon: 'fa-robot', badge: 'Level 4' },
  { category: 'Operating Modules', title: 'Operations & BCP/DR Cryptographic Ledger', target: 'operations', icon: 'fa-cube', badge: 'SHA-256' },
  { category: 'Operating Modules', title: 'Cryptography, PKI & Attestation Tools', target: 'crypto-tools', icon: 'fa-key', badge: 'FIPS 140-3' },
  { category: 'Operating Modules', title: 'IT, Cloud Infrastructure & Passkeys', target: 'infrastructure', icon: 'fa-server', badge: 'FIDO2' },
  { category: 'Operating Modules', title: 'Cybersecurity & CERT-In 6h War Room', target: 'secops', icon: 'fa-shield-virus', badge: 'CERT-In 6h' },
  { category: 'Operating Modules', title: 'Master Document Vault & Categories', target: 'vault', icon: 'fa-folder-closed', badge: 'AES-256' },
  { category: 'Operating Modules', title: 'Strategic Roadmap, Decisions & KPIs', target: 'strategy', icon: 'fa-chess-king', badge: 'OKRs' },
  { category: 'Operating Modules', title: 'Visual Intelligence & Analytical Hub', target: 'analytics', icon: 'fa-chart-line', badge: 'Charts' },
  { category: 'Operating Modules', title: 'Internal Service Desk, Tickets & Alerts', target: 'internal-support', icon: 'fa-headset', badge: 'ITSM' },
  { category: 'Operating Modules', title: 'ITSM & CMDB Operations Control Tower', target: 'itsm', icon: 'fa-network-wired', badge: 'ITIL v4' },
  { category: 'Operating Modules', title: 'Asperion Teams, Instant Chat & Huddle', target: 'teams', icon: 'fa-comments', badge: 'Live Chat' },
  { category: 'Operating Modules', title: 'Asperion SharePoint & SOP Knowledge Base', target: 'sharepoint', icon: 'fa-book-bookmark', badge: 'SOP Hub' },
  { category: 'Operating Modules', title: 'Training & Employee Joinee Academy', target: 'training', icon: 'fa-graduation-cap', badge: 'Academy' },
  // Portals
  { category: 'Dedicated Portals', title: 'Employee Self-Service (ESS) Portal', target: 'portal-employee', icon: 'fa-id-badge', badge: 'ESS' },
  { category: 'Dedicated Portals', title: 'Client SLA & Statement of Account Portal', target: 'portal-client', icon: 'fa-briefcase', badge: 'Client' },
  { category: 'Dedicated Portals', title: 'Vendor Sourcing, RFX & AP Bill Portal', target: 'portal-vendor', icon: 'fa-boxes-packing', badge: 'Vendor' },
];

export const Header: React.FC<HeaderProps> = ({
  onToggleMobileSidebar,
  persona,
  onSwitchPersona,
  onNavigate,
}) => {
  const [istTime, setIstTime] = useState('--:--:-- IST');
  const [adminMenuOpen, setAdminMenuOpen] = useState(false);
  const [notifDropdownOpen, setNotifDropdownOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isStakeholderModalOpen, setIsStakeholderModalOpen] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([
    {
      id: 1,
      title: 'CERT-In Statutory 6-Hour SLA Countdown Active',
      department: 'Cybersecurity SOC',
      severity: 'CRITICAL',
      time: '12m ago',
      unread: true,
    },
    {
      id: 2,
      title: 'Monthly AI Token Quota 76.8% Consumed',
      department: 'AI & Cloud Infrastructure',
      severity: 'WARNING',
      time: '45m ago',
      unread: false,
    },
    {
      id: 3,
      title: 'MCA21 Annual Return Filing Invariant Satisfied',
      department: 'Corporate Governance',
      severity: 'INFO',
      time: '2h ago',
      unread: false,
    },
  ]);

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      const ist = now.toLocaleTimeString('en-IN', {
        timeZone: 'Asia/Kolkata',
        hour12: false,
      });
      setIstTime(`${ist} IST`);
    };
    updateClock();
    const timer = setInterval(updateClock, 1000);
    return () => clearInterval(timer);
  }, []);

  // Keyboard shortcut Ctrl+K to open search command palette
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      } else if (e.key === 'Escape') {
        setIsSearchOpen(false);
        setIsStakeholderModalOpen(false);
        setNotifDropdownOpen(false);
        setAdminMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Fetch real notifications on mount
  useEffect(() => {
    axios
      .get('/api/v1/internal-support/notifications?limit=10')
      .then((res) => {
        if (Array.isArray(res.data) && res.data.length > 0) {
          setNotifications(
            res.data.map((n: any) => ({
              id: n.id,
              title: n.title,
              department: n.department || 'Enterprise Ops',
              severity: n.severity || 'INFO',
              time: 'Just now',
              unread: !n.is_read,
            }))
          );
        }
      })
      .catch(() => {});
  }, []);

  const unreadCount = notifications.filter((n) => n.unread).length || 1;

  const filteredCommands = COMMAND_LIST.filter(
    (c) =>
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.badge && c.badge.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const handleCommandSelect = (target: string) => {
    setIsSearchOpen(false);
    setSearchQuery('');
    if (onNavigate) {
      onNavigate(target);
    }
  };

  const handleStakeholderQuickLogin = (email: string, targetModule?: string) => {
    onSwitchPersona(email);
    setIsStakeholderModalOpen(false);
    if (targetModule && onNavigate) {
      onNavigate(targetModule);
    }
  };

  return (
    <div className="shrink-0 z-30">
      {/* 1. Primary Top Header */}
      <header className="bg-slate-900 text-white border-b border-slate-800 px-4 sm:px-6 py-3 flex items-center justify-between gap-4 shadow-md">
        {/* Left Section: Mobile Menu + Spacious Company Branding */}
        <div className="flex items-center gap-3.5 min-w-0">
          <button
            onClick={onToggleMobileSidebar}
            className="lg:hidden p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/80 transition shrink-0"
            title="Toggle Navigation Menu"
          >
            <i className="fa-solid fa-bars text-base" />
          </button>
          <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-xl bg-slate-950 border border-cyan-500/35 p-1.5 flex items-center justify-center shrink-0 shadow-lg">
            <img
              src="/static/img/logo.png"
              alt="Asperion Digital Technologies Logo"
              className="w-full h-full object-contain"
            />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2.5 flex-wrap">
              <h1 className="text-sm sm:text-lg font-bold tracking-tight text-white truncate">
                ASPERION DIGITAL TECHNOLOGIES
              </h1>
              <span className="hidden sm:inline-flex items-center text-[11px] font-medium text-cyan-300 bg-slate-950 px-2 py-0.5 rounded border border-cyan-500/30 font-mono">
                CIN: U85500KA2026OPC222069
              </span>
            </div>
            <p className="text-[11px] sm:text-xs text-slate-400 truncate mt-0.5">
              (OPC) Private Limited &bull; Bangalore North, Karnataka &bull; Enterprise OS v1.0
            </p>
          </div>
        </div>

        {/* Center Section: Global Search (Ctrl+K) & Live Clock Badge */}
        <div className="hidden xl:flex items-center gap-3 flex-1 max-w-xl justify-center">
          <button
            onClick={() => setIsSearchOpen(true)}
            className="flex items-center justify-between w-full max-w-sm bg-slate-950/90 hover:bg-slate-800/90 text-slate-400 hover:text-slate-200 px-3.5 py-2 rounded-lg border border-slate-700/80 text-xs transition shadow-inner group"
            title="Universal Command Palette (Ctrl+K)"
          >
            <span className="flex items-center gap-2.5">
              <i className="fa-solid fa-magnifying-glass text-cyan-400 text-xs group-hover:scale-110 transition-transform"></i>
              <span className="text-slate-300">Search modules, POs, actions...</span>
            </span>
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] font-mono border border-slate-700 text-slate-400">
              Ctrl+K
            </kbd>
          </button>

          <div className="flex items-center gap-2 text-xs bg-slate-950/80 px-3 py-2 rounded-lg border border-slate-800 shrink-0">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span id="live-ist-clock" className="font-mono text-cyan-300 font-semibold tracking-wider">
              {istTime}
            </span>
            <span className="text-slate-600">|</span>
            <span id="role-badge" className="text-slate-300 font-medium">
              Director Role
            </span>
          </div>
        </div>

        {/* Right Section: Persona Selector, Stakeholder Login, Notifications & Admin Menu */}
        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          <button
            onClick={() => setIsSearchOpen(true)}
            className="xl:hidden p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition border border-transparent hover:border-slate-700"
            title="Search (Ctrl+K)"
          >
            <i className="fa-solid fa-magnifying-glass text-sm"></i>
          </button>

          <div className="hidden md:flex items-center gap-2">
            <select
              value={persona}
              onChange={(e) => onSwitchPersona(e.target.value)}
              className="text-xs bg-slate-800 text-white font-medium px-2.5 py-1.5 rounded-lg border border-slate-700 focus:outline-none focus:ring-1 focus:ring-cyan-500 max-w-[200px]"
            >
              <option value="director@asperion.in">Varadi Vijay (Director / SuperAdmin)</option>
              <option value="finance@asperion.in">Finance Head</option>
              <option value="hr@asperion.in">People &amp; HR Lead</option>
              <option value="delivery@asperion.in">PMO Delivery Lead</option>
              <option value="soc@asperion.in">CISO / SOC Lead</option>
              <option value="employee@asperion.in">Arjun Sharma (Employee Self-Service)</option>
              <option value="client@zenith.com">Zenith Global (Client Portal)</option>
              <option value="vendor@nexuscables.in">Nexus Micro (Vendor Sourcing Portal)</option>
            </select>
          </div>

          {/* Stakeholder Secure Login Action Button */}
          <button
            onClick={() => setIsStakeholderModalOpen(true)}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white border border-blue-500/80 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow-sm"
            title="Sign In as Dedicated Stakeholder (Employee, Client, Vendor)"
          >
            <i className="fa-solid fa-lock text-blue-100"></i>
            <span className="hidden sm:inline">Stakeholder Login</span>
          </button>

          {/* Omni-Channel Notification Center Bell */}
          <div className="relative">
            <button
              id="btn-notif-bell"
              onClick={() => setNotifDropdownOpen(!notifDropdownOpen)}
              className="relative p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition border border-transparent hover:border-slate-700"
              title="Omni-Channel Alerts"
            >
              <i className="fa-solid fa-bell text-base"></i>
              <span
                id="notif-badge"
                className="absolute -top-1 -right-1 bg-red-600 text-white text-[10px] font-bold px-1.5 py-0.2 rounded-full min-w-[18px] text-center shadow"
              >
                {unreadCount}
              </span>
            </button>

            {/* Notification Dropdown */}
            {notifDropdownOpen && (
              <div
                id="notif-dropdown"
                className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-xl shadow-2xl border border-slate-200 z-50 text-slate-800 overflow-hidden"
              >
                <div className="p-3 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <i className="fa-solid fa-bell text-blue-400"></i>
                    <span className="font-semibold text-sm">Cross-Group Alerts</span>
                    <span className="text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full font-medium">
                      {unreadCount} Unread
                    </span>
                  </div>
                  <button
                    onClick={() => {
                      setNotifications(notifications.map((n) => ({ ...n, unread: false })));
                    }}
                    className="text-xs text-blue-400 hover:text-blue-300 underline font-medium"
                  >
                    Mark all read
                  </button>
                </div>
                <div className="max-h-80 overflow-y-auto divide-y divide-slate-100">
                  {notifications.map((item) => (
                    <div
                      key={item.id}
                      className={`p-3.5 hover:bg-slate-50 transition cursor-pointer ${
                        item.unread ? 'bg-blue-50/50' : ''
                      }`}
                      onClick={() => {
                        setNotifDropdownOpen(false);
                        if (onNavigate) onNavigate('internal-support');
                      }}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <span className="text-xs font-bold text-slate-900">{item.title}</span>
                        <span
                          className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                            item.severity === 'CRITICAL'
                              ? 'bg-rose-100 text-rose-800'
                              : item.severity === 'WARNING'
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}
                        >
                          {item.severity}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-[11px] text-slate-500 mt-1">
                        <span>{item.department}</span>
                        <span>{item.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="p-2.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs">
                  <button
                    onClick={() => alert('Syncing latest alerts...')}
                    className="text-slate-600 hover:text-slate-900 font-medium flex items-center gap-1"
                  >
                    <i className="fa-solid fa-arrows-rotate"></i> Sync System Alerts
                  </button>
                  <button
                    onClick={() => {
                      setNotifDropdownOpen(false);
                      if (onNavigate) onNavigate('internal-support');
                    }}
                    className="text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1"
                  >
                    <span>Open Service Desk</span> <i className="fa-solid fa-arrow-right"></i>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Admin & Secondary Actions Dropdown */}
          <div className="relative">
            <button
              onClick={() => setAdminMenuOpen(!adminMenuOpen)}
              className="p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition border border-slate-700/70"
              title="Admin Tools & System Actions"
            >
              <i className="fa-solid fa-ellipsis-vertical text-sm" />
            </button>
            {adminMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-200 py-1.5 z-50 text-slate-700 text-xs">
                <button
                  onClick={() => {
                    setAdminMenuOpen(false);
                    alert('Triggering enterprise auto-fix diagnostic and cache revalidation...');
                  }}
                  className="w-full text-left px-4 py-2 hover:bg-slate-100 flex items-center gap-2.5 font-medium"
                >
                  <i className="fa-solid fa-wand-magic-sparkles text-indigo-600 w-4 text-center"></i>
                  <span>Auto-Fix &amp; Self-Heal</span>
                </button>
                <button
                  onClick={() => {
                    setAdminMenuOpen(false);
                    setIsSearchOpen(true);
                  }}
                  className="w-full text-left px-4 py-2 hover:bg-slate-100 flex items-center gap-2.5 font-medium"
                >
                  <i className="fa-solid fa-keyboard text-slate-500 w-4 text-center"></i>
                  <span>Keyboard Shortcuts (Ctrl+K)</span>
                </button>
                <div className="my-1 border-t border-slate-100"></div>
                <a
                  href="/docs"
                  target="_blank"
                  rel="noreferrer"
                  className="w-full text-left px-4 py-2 hover:bg-slate-100 flex items-center gap-2.5 font-medium text-blue-600"
                >
                  <i className="fa-solid fa-code w-4 text-center" />
                  <span>OpenAPI Documentation</span>
                </a>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* 2. Real-Time Live Enterprise Status Ticker Sub-Bar */}
      <div className="bg-slate-950 text-slate-300 border-b border-slate-800/80 px-4 sm:px-6 py-1.5 text-xs flex items-center justify-between overflow-hidden select-none shadow-sm">
        <div className="flex items-center gap-4 overflow-x-auto whitespace-nowrap scrollbar-none py-0.5">
          <span className="inline-flex items-center gap-1.5 font-semibold text-slate-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            <span>ASPERION OS 2.0</span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="inline-flex items-center gap-1 text-slate-400">
            <i className="fa-solid fa-building-columns text-blue-400"></i>
            <span>
              CIN: <strong className="text-slate-200 font-mono">U85500KA2026OPC222069</strong>
            </span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="inline-flex items-center gap-1 text-slate-400">
            <i className="fa-solid fa-certificate text-amber-400"></i>
            <span>
              ISO Certified: <strong className="text-emerald-400">9001 &bull; 27001 &bull; 42001 &bull; 20000-1 &bull; 22301</strong>
            </span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="inline-flex items-center gap-1 text-slate-400">
            <i className="fa-solid fa-fingerprint text-indigo-400"></i>
            <span>
              FIDO2 / ZTNA: <strong className="text-cyan-300">100% Bound</strong>
            </span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="inline-flex items-center gap-1 text-slate-400">
            <i className="fa-solid fa-server text-sky-400"></i>
            <span>
              Multi-Region DR: <strong className="text-emerald-400">RTO 18.5m &bull; Zero Data Loss</strong>
            </span>
          </span>
          <span className="text-slate-600">|</span>
          <span className="inline-flex items-center gap-1 text-slate-400">
            <i className="fa-solid fa-shield-virus text-rose-400"></i>
            <span>
              CERT-In War Room: <strong className="text-rose-300">6h SLA Active</strong>
            </span>
          </span>
        </div>
        <div className="hidden xl:flex items-center gap-3 text-[11px] font-mono text-slate-400 shrink-0 pl-4 border-l border-slate-800">
          <span>
            Horamavu HQ: <strong className="text-emerald-400">ONLINE</strong>
          </span>
          <span>
            IoT Sensing Canary: <strong className="text-indigo-400">10s SYNC</strong>
          </span>
        </div>
      </div>

      {/* 3. Universal Command Palette Search Modal (Ctrl+K) */}
      {isSearchOpen && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-xs z-50 flex items-start justify-center pt-20 p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-100">
            <div className="p-4 border-b border-slate-200 flex items-center gap-3 bg-slate-50">
              <i className="fa-solid fa-magnifying-glass text-cyan-600 text-lg"></i>
              <input
                type="text"
                autoFocus
                placeholder="Search all 27 modules, POs, statutory filings, or actions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-transparent border-none text-slate-800 text-sm focus:outline-none placeholder-slate-400 font-medium"
              />
              <kbd className="px-2 py-0.5 rounded bg-slate-200 text-slate-600 text-[10px] font-mono font-bold">
                ESC
              </kbd>
            </div>
            <div className="max-h-96 overflow-y-auto p-2 divide-y divide-slate-100">
              {filteredCommands.length === 0 ? (
                <div className="p-8 text-center text-slate-400 text-xs">
                  No matching module or action found for &quot;{searchQuery}&quot;
                </div>
              ) : (
                filteredCommands.map((cmd, idx) => (
                  <div
                    key={idx}
                    onClick={() => handleCommandSelect(cmd.target)}
                    className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-100 cursor-pointer transition group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-slate-100 group-hover:bg-cyan-50 flex items-center justify-center text-slate-600 group-hover:text-cyan-700 transition">
                        <i className={`fa-solid ${cmd.icon} text-sm`}></i>
                      </div>
                      <div>
                        <div className="text-xs font-bold text-slate-900">{cmd.title}</div>
                        <div className="text-[10px] text-slate-400">{cmd.category}</div>
                      </div>
                    </div>
                    {cmd.badge && (
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 text-slate-600 border border-slate-200">
                        {cmd.badge}
                      </span>
                    )}
                  </div>
                ))
              )}
            </div>
            <div className="p-3 bg-slate-50 border-t border-slate-200 flex justify-between items-center text-[11px] text-slate-500">
              <span>Navigation: Click or Enter to Select</span>
              <span>27 Enterprise Modules Ready</span>
            </div>
          </div>
        </div>
      )}

      {/* 4. Stakeholder Secure Authentication Modal */}
      {isStakeholderModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md border border-slate-100 space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <div className="flex items-center gap-2.5">
                <img
                  src="/static/img/logo.png"
                  alt="Asperion Logo"
                  className="w-10 h-10 rounded-full border border-cyan-500/30 shadow-md object-contain p-0.5 bg-slate-900 shrink-0"
                />
                <div>
                  <h3 className="font-bold text-sm text-slate-900">Stakeholder Secure Authentication</h3>
                  <p className="text-[11px] text-slate-500">Official Portal Access &bull; Asperion OS 2.0</p>
                </div>
              </div>
              <button
                onClick={() => setIsStakeholderModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <i className="fa-solid fa-xmark text-lg"></i>
              </button>
            </div>

            <div>
              <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                Quick-Select Stakeholder Role
              </label>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => handleStakeholderQuickLogin('director@asperion.in', 'dashboard')}
                  className="p-3 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 text-left transition"
                >
                  <div className="font-bold text-slate-800">Sole Director</div>
                  <div className="text-[10px] text-slate-400 font-mono">Varadi Vijay</div>
                </button>
                <button
                  type="button"
                  onClick={() => handleStakeholderQuickLogin('employee@asperion.in', 'portal-employee')}
                  className="p-3 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 text-left transition"
                >
                  <div className="font-bold text-slate-800">Employee Portal</div>
                  <div className="text-[10px] text-slate-400 font-mono">Arjun Sharma</div>
                </button>
                <button
                  type="button"
                  onClick={() => handleStakeholderQuickLogin('client@zenith.com', 'portal-client')}
                  className="p-3 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 text-left transition"
                >
                  <div className="font-bold text-slate-800">Client SLA Portal</div>
                  <div className="text-[10px] text-slate-400 font-mono">Zenith Global</div>
                </button>
                <button
                  type="button"
                  onClick={() => handleStakeholderQuickLogin('vendor@nexuscables.in', 'portal-vendor')}
                  className="p-3 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 text-left transition"
                >
                  <div className="font-bold text-slate-800">Vendor Sourcing</div>
                  <div className="text-[10px] text-slate-400 font-mono">Nexus Micro</div>
                </button>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t">
              <button
                type="button"
                onClick={() => setIsStakeholderModalOpen(false)}
                className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg text-xs font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Header;
