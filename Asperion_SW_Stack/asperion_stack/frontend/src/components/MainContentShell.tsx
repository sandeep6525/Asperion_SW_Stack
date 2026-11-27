import React from 'react';

interface MainContentShellProps {
  category?: string;
  moduleTitle?: string;
  autoSyncSeconds?: string;
  onAutoSyncChange?: (freq: string) => void;
  onSyncNow?: (trigger: boolean) => void;
  onOpenCommandPalette?: () => void;
  onTriggerSelfHeal?: () => void;
  alertBanner?: { title: string; message: string } | null;
  onAlertAction?: () => void;
  onDismissAlert?: () => void;
  children: React.ReactNode;
}

export const MainContentShell: React.FC<MainContentShellProps> = ({
  category = 'Executive MIS',
  moduleTitle = 'Executive Dashboard',
  autoSyncSeconds = '30s',
  onAutoSyncChange,
  onSyncNow,
  onOpenCommandPalette,
  onTriggerSelfHeal,
  alertBanner = null,
  onAlertAction,
  onDismissAlert,
  children,
}) => {
  return (
    <main className="flex-1 overflow-y-auto bg-slate-50 p-4 sm:p-6">
      {/* Enterprise Breadcrumbs & Active Module Bar */}
      <div
        id="enterprise-breadcrumb-bar"
        className="mb-5 flex flex-wrap items-center justify-between gap-3 bg-white/95 backdrop-blur-md p-3.5 rounded-xl border border-slate-200 shadow-sm"
      >
        <div className="flex items-center gap-2 text-xs text-slate-600">
          <span className="inline-flex items-center gap-1.5 font-bold text-slate-900 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200">
            <img src="/static/img/logo.png" alt="Asperion" className="w-4 h-4 rounded-full object-contain" />
            <span>Asperion OS</span>
          </span>
          <i className="fa-solid fa-chevron-right text-[10px] text-slate-400" />
          <span id="breadcrumb-category" className="font-medium text-slate-500">
            {category}
          </span>
          <i className="fa-solid fa-chevron-right text-[10px] text-slate-400" />
          <span
            id="breadcrumb-module"
            className="font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200/60"
          >
            {moduleTitle}
          </span>
        </div>

        <div className="flex items-center gap-2 text-xs flex-wrap">
          {/* Live Sync Indicator & Controls */}
          <div className="inline-flex items-center gap-1.5 text-[11px] bg-slate-50 px-2.5 py-1 rounded-md border border-slate-200 shadow-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span id="auto-sync-status-text" className="text-slate-600">
              Auto-Sync:{' '}
              <strong id="auto-sync-countdown" className="text-slate-800 font-mono">
                {autoSyncSeconds}
              </strong>
            </span>
            <select
              onChange={(e) => onAutoSyncChange?.(e.target.value)}
              defaultValue="30"
              className="text-[10px] bg-white border border-slate-200 rounded px-1.5 py-0.5 text-slate-700 font-medium cursor-pointer"
            >
              <option value="30">30s</option>
              <option value="10">10s</option>
              <option value="60">60s</option>
              <option value="0">Pause</option>
            </select>
          </div>

          {/* Instant Sync Button */}
          <button
            id="btn-global-sync"
            onClick={() => onSyncNow?.(true)}
            className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-md shadow transition text-[11px]"
            title="Instantly Synchronize All Modules (Live DB State)"
          >
            <i id="icon-global-sync" className="fa-solid fa-arrows-rotate text-[11px]" />
            <span>Sync Now</span>
          </button>

          {/* Quick Command Palette Pill */}
          <button
            onClick={onOpenCommandPalette}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-md border border-slate-300 transition text-[11px]"
            title="Open Command Palette (Ctrl+K)"
          >
            <i className="fa-solid fa-terminal text-blue-600" />
            <span>Commands</span>
            <kbd className="kbd-pill text-[9px]">Ctrl+K</kbd>
          </button>

          {/* Quick Self-Heal Pill */}
          <button
            onClick={onTriggerSelfHeal}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold rounded-md border border-indigo-200 transition text-[11px]"
            title="Run Autonomous Self-Healing Diagnostic Scan (Alt+S)"
          >
            <i className="fa-solid fa-wand-magic-sparkles text-indigo-600" />
            <span>Self-Heal</span>
          </button>
        </div>
      </div>

      {/* Global Critical Alert Banner */}
      {alertBanner && (
        <div
          id="system-alert-banner"
          className="mb-6 p-4 bg-red-50 border-l-4 border-red-600 rounded-r-xl shadow-sm flex items-center justify-between"
        >
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-red-600 text-white flex items-center justify-center font-bold text-sm shrink-0 shadow">
              <i className="fa-solid fa-triangle-exclamation" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider bg-red-200 text-red-900 px-2 py-0.5 rounded">
                  High Severity
                </span>
                <h4 id="alert-banner-title" className="text-sm font-bold text-red-900">
                  {alertBanner.title || 'Critical System Alert'}
                </h4>
              </div>
              <p id="alert-banner-msg" className="text-xs text-red-700 mt-0.5">
                {alertBanner.message || 'Immediate operational attention required.'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              id="alert-banner-btn"
              onClick={onAlertAction}
              className="text-xs font-semibold px-3.5 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-sm transition"
            >
              Inspect
            </button>
            <button
              onClick={onDismissAlert}
              className="text-slate-400 hover:text-slate-600 px-2 py-1 text-sm"
              title="Dismiss Alert"
            >
              <i className="fa-solid fa-xmark" />
            </button>
          </div>
        </div>
      )}

      {/* Active Module Content */}
      {children}
    </main>
  );
};
export default MainContentShell;
