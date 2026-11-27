import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { NavItem } from '../types/modules';

interface GenericModuleViewProps {
  moduleMeta: NavItem;
  endpoint?: string;
}

export const GenericModuleView: React.FC<GenericModuleViewProps> = ({ moduleMeta, endpoint }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function loadData() {
      if (!endpoint) {
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await axios.get(endpoint);
        if (isMounted) setData(res.data);
      } catch (err: any) {
        if (isMounted) setError(err.message || 'Error fetching module data');
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadData();
    return () => {
      isMounted = false;
    };
  }, [endpoint]);

  return (
    <div className="space-y-6">
      {/* 2-Column Balanced Header */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-800 text-white shadow-md">
        <div className="lg:col-span-8 flex flex-col justify-between gap-4">
          <div className="flex items-start sm:items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-slate-950 border border-cyan-500/30 p-1.5 flex items-center justify-center shrink-0 shadow-sm">
              <img src="/static/img/logo.png" alt="Asperion Brand" className="w-full h-full object-contain" />
            </div>
            <div className="min-w-0">
              <h2 className="text-lg sm:text-2xl font-bold text-white tracking-tight">{moduleMeta.label}</h2>
              <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
                Asperion Enterprise Operating System &bull; Live Connected Module &bull; Module ID: {moduleMeta.target}
              </p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-cyan-300 border border-cyan-500/30">
              FASTAPI REST INTEGRATED
            </span>
            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-emerald-300 border border-emerald-500/30">
              SQLITE PRODUCTION DB
            </span>
            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-purple-300 border border-purple-500/30">
              ROLE PROTECTED
            </span>
          </div>
        </div>

        <div className="lg:col-span-4 bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between gap-3">
          <div className="text-xs text-slate-300 font-semibold border-b border-slate-800/80 pb-2 flex items-center justify-between">
            <span>Module Status</span>
            <span className="text-[10px] font-mono text-cyan-400">ONLINE</span>
          </div>
          <div className="text-xs text-slate-400">
            {endpoint ? `API: ${endpoint}` : 'Connected through master backend services'}
          </div>
        </div>
      </div>

      {/* Main Content Card */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
          <i className={`${moduleMeta.icon}`}></i> {moduleMeta.label} Live Data
        </h3>

        {loading && <div className="text-xs text-slate-400 py-6 text-center">Loading live records from database...</div>}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg">
            Backend API message: {error}
          </div>
        )}
        {!loading && !error && data && (
          <div className="space-y-4">
            <div className="text-xs text-slate-500">
              Records received: <strong className="text-slate-800">{Array.isArray(data) ? data.length : 1}</strong>
            </div>
            <pre className="text-xs bg-slate-950 text-emerald-300 p-4 rounded-xl overflow-auto max-h-96 font-mono">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
export default GenericModuleView;
