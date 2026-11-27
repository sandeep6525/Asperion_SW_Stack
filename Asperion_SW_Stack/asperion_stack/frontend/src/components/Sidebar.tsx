import React from 'react';
import { NavItem } from '../types/modules';

interface SidebarProps {
  navItems: NavItem[];
  activeModule: string;
  onSelectModule: (target: string) => void;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
  user?: {
    name: string;
    role: string;
  };
}

export const Sidebar: React.FC<SidebarProps> = ({
  navItems,
  activeModule,
  onSelectModule,
  isOpenMobile,
  onCloseMobile,
  user = { name: 'Director Varadi Vijay', role: 'Sole Member • OPC' },
}) => {
  const operatingModules = navItems.filter((i) => i.category === 'Operating Modules');
  const dedicatedPortals = navItems.filter((i) => i.category === 'Dedicated Portals');

  const renderItem = (item: NavItem) => {
    const isActive = activeModule === item.target;
    return (
      <button
        key={item.target}
        data-target={item.target}
        onClick={() => {
          onSelectModule(item.target);
          onCloseMobile();
        }}
        className={`nav-btn w-full text-left flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition relative ${
          isActive ? 'bg-blue-800 text-white' : 'text-slate-300 hover:bg-slate-800'
        }`}
      >
        <i className={`${item.icon} w-5 text-center`} />
        <span className="truncate">{item.label}</span>
        {item.badge && (
          <span
            id={item.badge.id}
            className={`ml-auto px-1.5 py-0.5 rounded-full text-[9px] font-bold border font-mono ${item.badge.className}`}
          >
            {item.badge.text}
          </span>
        )}
      </button>
    );
  };

  return (
    <>
      {isOpenMobile && (
        <div
          id="sidebar-backdrop"
          onClick={onCloseMobile}
          className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-30 lg:hidden"
        />
      )}

      <aside
        id="main-sidebar"
        className={`fixed lg:static inset-y-0 left-0 z-40 w-64 bg-slate-900 border-r border-slate-800 flex flex-col shrink-0 overflow-y-auto transform transition-transform duration-200 ease-in-out ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="px-4 pt-4 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
          <span>Operating Modules</span>
          <button
            onClick={onCloseMobile}
            className="lg:hidden text-slate-400 hover:text-white p-1"
            aria-label="Close navigation"
          >
            <i className="fa-solid fa-xmark" />
          </button>
        </div>

        <nav className="flex-1 px-3 pb-4 space-y-1.5">
          {operatingModules.map(renderItem)}

          <div className="pt-2 pb-1 border-t border-slate-800 text-[10px] font-bold text-slate-500 uppercase px-3">
            Dedicated Portals
          </div>

          {dedicatedPortals.map(renderItem)}
        </nav>

        <div className="p-3.5 border-t border-slate-800 text-xs text-slate-400 flex items-center gap-3 bg-slate-950/60">
          <img
            src="/static/img/logo.png"
            alt="Asperion"
            className="w-8 h-8 rounded-full border border-cyan-500/30 object-contain bg-slate-900 p-0.5 shrink-0"
          />
          <div className="min-w-0">
            <div className="text-slate-200 font-semibold truncate">{user.name}</div>
            <div className="text-[10px] text-cyan-400 font-mono">{user.role}</div>
          </div>
        </div>
      </aside>
    </>
  );
};
export default Sidebar;
