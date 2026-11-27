// @ts-ignore
import { loadGuardrails, switchGuardrailTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const GuardrailsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('rules');
  useEffect(() => {
    try {
      loadGuardrails();
    } catch (e) {
      console.error('Error in loadGuardrails:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchGuardrailTab(activeTab);
    } catch (e) {
      console.error('Error in switchGuardrailTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <div id="view-guardrails" className="module-view  space-y-6">
                {/* Top Header Banner */}
                <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 gap-4">
                    <div>
                        <div className="flex items-center gap-3">
                            <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                                <i className="fa-solid fa-shield-virus text-teal-600"></i>
                                Enterprise Guardrails & Architectural Integrity Cockpit
                            </h2>
                            <span className="bg-teal-100 text-teal-800 border border-teal-300 px-2.5 py-0.5 rounded-full text-xs font-semibold">
                                Active Runtime Enforcement
                            </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                            Autonomous verification across FinOps 3-Way Match, MSMED 45-Day Priority, DPDP 2023 DPA, Smart Geofencing, DevSecOps Quality Gates, and CERT-In 6-Hour Timers.
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button onClick={() => {}} className="px-3 py-1.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow">
                            <i className="fa-solid fa-play"></i> Trigger Live Scan
                        </button>
                        <button onClick={() => {}} className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 border rounded-lg text-xs font-semibold transition flex items-center gap-1.5">
                            <i className="fa-solid fa-arrows-rotate"></i> Refresh
                        </button>
                    </div>
                </div>

                {/* Telemetry KPI Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Compliance Index</div>
                            <div id="guardrail-kpi-score" className="text-2xl font-black text-emerald-600 mt-1">--%</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">Statutory & IFC Pass Ratio</div>
                        </div>
                        <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 text-xl border border-emerald-100">
                            <i className="fa-solid fa-award"></i>
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Active Guardrail Rules</div>
                            <div id="guardrail-kpi-active" className="text-2xl font-black text-blue-600 mt-1">--</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">Automated Gate Policies</div>
                        </div>
                        <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 text-xl border border-blue-100">
                            <i className="fa-solid fa-shield-halved"></i>
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Total Evaluations</div>
                            <div id="guardrail-kpi-evals" className="text-2xl font-black text-indigo-600 mt-1">--</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">Scans across 20 Pillars</div>
                        </div>
                        <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 text-xl border border-indigo-100">
                            <i className="fa-solid fa-calculator"></i>
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Violations Blocked</div>
                            <div id="guardrail-kpi-blocked" className="text-2xl font-black text-rose-600 mt-1">--</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">Active Hard Stops Enforced</div>
                        </div>
                        <div className="w-12 h-12 bg-rose-50 rounded-xl flex items-center justify-center text-rose-600 text-xl border border-rose-100">
                            <i className="fa-solid fa-ban"></i>
                        </div>
                    </div>
                </div>

                {/* Navigation Tabs inside Guardrails */}
                <div className="flex border-b border-slate-200 gap-6 text-sm font-semibold">
                    <button id="tab-guardrail-rules" onClick={() => setActiveTab('rules')} className="py-2 border-b-2 border-teal-600 text-teal-700 flex items-center gap-2">
                        <i className="fa-solid fa-list-check"></i> Active Policy Rules
                    </button>
                    <button id="tab-guardrail-flowcharts" onClick={() => setActiveTab('flowcharts')} className="py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2">
                        <i className="fa-solid fa-diagram-project"></i> Interactive Process Flowcharts (6)
                    </button>
                    <button id="tab-guardrail-blueprints" onClick={() => setActiveTab('blueprints')} className="py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2">
                        <i className="fa-solid fa-compass-drafting"></i> System Architecture Blueprints
                    </button>
                    <button id="tab-guardrail-logs" onClick={() => setActiveTab('logs')} className="py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2">
                        <i className="fa-solid fa-receipt"></i> Enforcement Audit Logs
                    </button>
                    <button id="tab-guardrail-docs" onClick={() => setActiveTab('docs')} className="py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2">
                        <i className="fa-solid fa-book-bookmark"></i> Technical Architecture Documents
                    </button>
                </div>

                {/* TAB 1: ACTIVE RULES TABLE */}
                <div id="guardrail-panel-rules" style={{ display: activeTab === 'rules' ? 'block' : 'none' }} className="space-y-4">
                    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                        <div className="p-3 bg-slate-50 border-b flex justify-between items-center text-xs">
                            <span className="font-bold text-slate-700 uppercase">Operational & Regulatory Guardrails Matrix</span>
                            <span className="text-slate-500">Autonomous Gate Mode</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr className="bg-slate-100 text-slate-600 border-b">
                                        <th className="p-3 font-semibold">Rule Code</th>
                                        <th className="p-3 font-semibold">Name & Category</th>
                                        <th className="p-3 font-semibold">Regulatory Framework</th>
                                        <th className="p-3 font-semibold">Severity / Mode</th>
                                        <th className="p-3 font-semibold">Evaluations</th>
                                        <th className="p-3 font-semibold">Passed</th>
                                        <th className="p-3 font-semibold">Blocked / Healed</th>
                                        <th className="p-3 font-semibold">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="guardrail-rules-table-body" className="divide-y divide-slate-100">
                                    <tr><td colSpan={8} className="p-4 text-center text-slate-400">Loading enterprise guardrails...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 2: INTERACTIVE PROCESS FLOWCHARTS */}
                <div id="guardrail-panel-flowcharts" style={{ display: activeTab === 'flowcharts' ? 'block' : 'none' }} className=" space-y-4">
                    <div className="flex flex-wrap gap-2 pb-2 border-b border-slate-200" id="flowchart-selector-buttons">
                        {/* Populated by JS */}
                    </div>
                    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b pb-3">
                            <div>
                                <h3 id="flowchart-active-title" className="text-base font-bold text-slate-800">Flowchart Viewer</h3>
                                <div id="flowchart-active-standard" className="text-xs text-teal-600 font-semibold mt-0.5">Regulatory Standard</div>
                            </div>
                            <div id="flowchart-active-guardrails" className="flex flex-wrap gap-1"></div>
                        </div>
                        {/* Mermaid Visual Representation Pre/Code Block */}
                        <div>
                            <div className="text-xs font-semibold text-slate-700 mb-1 flex items-center gap-1.5">
                                <i className="fa-solid fa-code text-teal-600"></i> Mermaid Architecture Graph Definition
                            </div>
                            <pre id="flowchart-mermaid-code" className="bg-slate-900 text-teal-300 font-mono text-[11px] p-4 rounded-xl overflow-x-auto whitespace-pre leading-relaxed border border-slate-800"></pre>
                        </div>
                        {/* Step-by-Step Structured Process Walkthrough */}
                        <div>
                            <div className="text-xs font-semibold text-slate-700 mb-2">Detailed Multi-Stage Process Lifecycle</div>
                            <div id="flowchart-steps-container" className="space-y-2"></div>
                        </div>
                    </div>
                </div>

                {/* TAB 3: SYSTEM ARCHITECTURE BLUEPRINTS */}
                <div id="guardrail-panel-blueprints" style={{ display: activeTab === 'blueprints' ? 'block' : 'none' }} className=" space-y-4">
                    <div id="blueprints-grid-container" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Populated by JS */}
                    </div>
                </div>

                {/* TAB 4: ENFORCEMENT AUDIT LOGS */}
                <div id="guardrail-panel-logs" style={{ display: activeTab === 'logs' ? 'block' : 'none' }} className=" space-y-4">
                    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                        <div className="p-3 bg-slate-50 border-b flex justify-between items-center text-xs">
                            <span className="font-bold text-slate-700 uppercase">Live Enforcement & Intervention Log</span>
                            <span className="text-slate-500">Immutable Audit Trail</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr className="bg-slate-100 text-slate-600 border-b">
                                        <th className="p-3 font-semibold">Exec ID</th>
                                        <th className="p-3 font-semibold">Rule Code</th>
                                        <th className="p-3 font-semibold">Module</th>
                                        <th className="p-3 font-semibold">Entity Reference</th>
                                        <th className="p-3 font-semibold">Result</th>
                                        <th className="p-3 font-semibold">Trigger / Violation Details</th>
                                        <th className="p-3 font-semibold">Action Taken</th>
                                        <th className="p-3 font-semibold">Evaluated At</th>
                                    </tr>
                                </thead>
                                <tbody id="guardrail-logs-table-body" className="divide-y divide-slate-100">
                                    <tr><td colSpan={8} className="p-4 text-center text-slate-400">Loading audit logs...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 5: TECHNICAL ARCHITECTURE DOCUMENTS */}
                <div id="guardrail-panel-docs" style={{ display: activeTab === 'docs' ? 'block' : 'none' }} className=" space-y-4">
                    <div id="documents-grid-container" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Populated by JS */}
                    </div>
                </div>
            </div>

        


            {/* VIEW: AI APIS, MCPs, MULTI-CLOUD TOPOLOGY & AUTHENTICITY */}
    </div>
  );
};

export default GuardrailsView;
