// @ts-ignore
import { loadITSM, switchITSMTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const ITSMView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('cmdb');
  const [metrics, setMetrics] = useState({
    nodes: '33 CIs',
    health: '100.0%',
    kedb: '28 Fixed',
    cab: '26 Sched',
    fixes: '62 Auto',
    loi: '₹6.52 Cr',
  });

  useEffect(() => {
    axios
      .get('/api/v1/itsm/overview')
      .then((res) => {
        if (res.data?.metrics) {
          const m = res.data.metrics;
          setMetrics({
            nodes: `${m.total_configuration_items || 33} CIs`,
            health: `${m.cmdb_health_index_pct || 100.0}%`,
            kedb: `${m.kedb_published_solutions || 28} Fixed`,
            cab: `${m.approved_scheduled_changes || 26} Sched`,
            fixes: `${m.automated_self_healing_executions || 62} Auto`,
            loi: '₹6.52 Cr',
          });
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    try {
      loadITSM();
    } catch (e) {
      console.error('Error in loadITSM:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchITSMTab(activeTab);
    } catch (e) {
      console.error('Error in switchITSMTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-itsm" className="module-view  space-y-6">
                {/* Executive Header Banner */}
                <div className="mb-5 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gradient-to-r from-slate-900 via-cyan-950 to-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl">
                    <div className="flex items-center gap-4">
                        <div className="w-13 h-13 rounded-2xl bg-cyan-500/20 border-2 border-cyan-400/40 shadow-lg flex items-center justify-center text-cyan-300 text-2xl shrink-0 p-3">
                            <i className="fa-solid fa-network-wired"></i>
                        </div>
                        <div>
                            <div className="flex flex-wrap items-center gap-2 mb-1.5">
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-mono tracking-wider">ITIL v4 & ISO 20000</span>
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">99.98% Service Uptime</span>
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">Zero-Outage Architecture</span>
                            </div>
                            <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                                ITSM & CMDB Operations Control Tower
                            </h2>
                            <p className="text-xs text-slate-300 mt-0.5">
                                <strong>ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</strong> &bull; Founder & Sole Director: <strong>Varadi Vijay</strong> &bull; CIN: <span className="font-mono text-cyan-300">U85500KA2026OPC222069</span>
                            </p>
                        </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                        <button onClick={() => {}} className="px-3 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow">
                            <i className="fa-solid fa-plus"></i> Register CI Node
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow">
                            <i className="fa-solid fa-code-compare"></i> New Change Request
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow">
                            <i className="fa-solid fa-file-signature"></i> Draft Procurement LOI
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-semibold transition flex items-center gap-1.5">
                            <i className="fa-solid fa-arrows-rotate"></i>
                        </button>
                    </div>
                </div>

                {/* 6 Top Summary KPI Cards */}
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">CMDB Active Nodes</div>
                        <div id="itsm-stat-nodes" className="text-xl font-bold font-mono text-slate-900 mt-1">{metrics.nodes}</div>
                        <div className="text-[10px] text-emerald-600 mt-0.5"><i className="fa-solid fa-circle-check"></i> 100% Tracked</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">CMDB Health Index</div>
                        <div id="itsm-stat-health" className="text-xl font-bold font-mono text-emerald-600 mt-1">{metrics.health}</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Telemetry Normalized</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">KEDB Solutions</div>
                        <div id="itsm-stat-kedb" className="text-xl font-bold font-mono text-indigo-600 mt-1">{metrics.kedb}</div>
                        <div className="text-[10px] text-indigo-700 mt-0.5">Known Error Database</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">CAB Changes</div>
                        <div id="itsm-stat-cab" className="text-xl font-bold font-mono text-blue-600 mt-1">{metrics.cab}</div>
                        <div className="text-[10px] text-blue-700 mt-0.5">Approved & Tested</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Self-Healing Runs</div>
                        <div id="itsm-stat-fixes" className="text-xl font-bold font-mono text-purple-600 mt-1">{metrics.fixes}</div>
                        <div className="text-[10px] text-purple-700 mt-0.5">MTTR: 18.5 Mins</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Procurement LOIs</div>
                        <div id="itsm-stat-loi" className="text-xl font-bold font-mono text-cyan-700 mt-1">{metrics.loi}</div>
                        <div className="text-[10px] text-cyan-800 mt-0.5">Active Commitments</div>
                    </div>
                </div>

                {/* Sub-Module Navigation Pills */}
                <div className="flex overflow-x-auto border-b border-slate-200 gap-2 text-xs font-semibold">
                    <button onClick={() => setActiveTab('cmdb')} id="itsm-tab-btn-cmdb" className="itsm-tab-btn px-4 py-2.5 border-b-2 border-cyan-600 text-cyan-700 font-bold flex items-center gap-2 whitespace-nowrap bg-cyan-50/50 rounded-t-lg">
                        <i className="fa-solid fa-server text-cyan-600"></i> CMDB Nodes & Topology
                    </button>
                    <button onClick={() => setActiveTab('problems')} id="itsm-tab-btn-problems" className="itsm-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-triangle-exclamation text-amber-500"></i> Problem KEDB & 5-Whys
                    </button>
                    <button onClick={() => setActiveTab('cab')} id="itsm-tab-btn-cab" className="itsm-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-code-compare text-blue-500"></i> CAB Change Enablement
                    </button>
                    <button onClick={() => setActiveTab('runbooks')} id="itsm-tab-btn-runbooks" className="itsm-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-wand-magic-sparkles text-purple-500"></i> Self-Healing Runbooks
                    </button>
                    <button onClick={() => setActiveTab('loi')} id="itsm-tab-btn-loi" className="itsm-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-file-contract text-emerald-500"></i> Procurement LOIs & SLAs
                    </button>
                </div>

                {/* SUB-VIEW 1: CMDB NODES & TOPOLOGY */}
                <div id="itsm-subview-cmdb" style={{ display: activeTab === 'cmdb' ? 'block' : 'none' }} className="itsm-subview space-y-5">
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-database text-cyan-600"></i> Configuration Management Database (CMDB) Node Inventory
                                </h3>
                                <p className="text-xs text-slate-500">Live operational topology tracking compute servers, databases, microservices, and network firewalls.</p>
                            </div>
                            <div className="flex flex-wrap gap-2 items-center text-xs">
                                <select id="itsm-filter-env" onChange={() => {}} className="px-2.5 py-1.5 border rounded-lg bg-slate-50 text-slate-700">
                                    <option value="ALL">All Environments</option>
                                    <option value="Production">Production</option>
                                    <option value="Staging">Staging</option>
                                    <option value="Disaster Recovery">Disaster Recovery</option>
                                </select>
                                <select id="itsm-filter-cat" onChange={() => {}} className="px-2.5 py-1.5 border rounded-lg bg-slate-50 text-slate-700">
                                    <option value="ALL">All Categories</option>
                                    <option value="Compute">Compute</option>
                                    <option value="Database">Database</option>
                                    <option value="Network">Network</option>
                                    <option value="Security">Security</option>
                                </select>
                            </div>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">CI Code & Name</th>
                                        <th className="p-3">Type & Tier</th>
                                        <th className="p-3">IP / FQDN</th>
                                        <th className="p-3">Cloud Region</th>
                                        <th className="p-3">Utilization (CPU/RAM)</th>
                                        <th className="p-3">Health Score</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-itsm-ci-nodes" className="divide-y divide-slate-100">
                                    {/* Populated via app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* CMDB Dependency Topology Visualization Card */}
                    <div className="bg-gradient-to-r from-slate-900 via-slate-950 to-slate-900 text-white p-5 rounded-2xl border border-slate-800 shadow-lg">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-sm text-cyan-300 flex items-center gap-2">
                                <i className="fa-solid fa-diagram-project"></i> Infrastructure Service Dependency Graph
                            </h3>
                            <span className="text-xs text-slate-400 font-mono">Directed Upstream / Downstream Impact Flow</span>
                        </div>
                        <div id="cmdb-topology-container" className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
                            {/* Populated via app.js */}
                        </div>
                    </div>
                </div>

                {/* SUB-VIEW 2: PROBLEM MANAGEMENT & KEDB */}
                <div id="itsm-subview-problems" style={{ display: activeTab === 'problems' ? 'block' : 'none' }} className="itsm-subview space-y-5">
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-triangle-exclamation text-amber-500"></i> Known Error Database (KEDB) & 5-Whys Root Cause Investigations
                                </h3>
                                <p className="text-xs text-slate-500">Documented root causes, validated temporary workarounds, and permanent architectural fixes.</p>
                            </div>
                            <span className="px-2.5 py-1 bg-amber-50 text-amber-800 border border-amber-200 rounded text-xs font-bold font-mono">
                                ITIL Problem Registry
                            </span>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Problem Code & Title</th>
                                        <th className="p-3">Category</th>
                                        <th className="p-3">Priority</th>
                                        <th className="p-3">Root Cause Analysis (5-Whys)</th>
                                        <th className="p-3">Workaround / Permanent Fix</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3 text-center">KEDB</th>
                                    </tr>
                                </thead>
                                <tbody id="table-itsm-problems" className="divide-y divide-slate-100">
                                    {/* Populated via app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* SUB-VIEW 3: CAB CHANGE ENABLEMENT */}
                <div id="itsm-subview-cab" style={{ display: activeTab === 'cab' ? 'block' : 'none' }} className="itsm-subview space-y-5">
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-code-compare text-blue-600"></i> Change Advisory Board (CAB) & Release Governance
                                </h3>
                                <p className="text-xs text-slate-500">Formal review and authorization of production changes with mandatory rollback plans.</p>
                            </div>
                            <button onClick={() => {}} className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold transition flex items-center gap-1 shadow">
                                <i className="fa-solid fa-plus"></i> Submit CR
                            </button>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">CR Code & Title</th>
                                        <th className="p-3">Type</th>
                                        <th className="p-3">Impact Scope</th>
                                        <th className="p-3">Risk Level</th>
                                        <th className="p-3">Scheduled Window</th>
                                        <th className="p-3">Rollback Plan</th>
                                        <th className="p-3">CAB Status</th>
                                        <th className="p-3 text-center">CAB Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-itsm-changes" className="divide-y divide-slate-100">
                                    {/* Populated via app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* SUB-VIEW 4: SELF-HEALING RUNBOOKS */}
                <div id="itsm-subview-runbooks" style={{ display: activeTab === 'runbooks' ? 'block' : 'none' }} className="itsm-subview space-y-5">
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-wand-magic-sparkles text-purple-600"></i> Autonomous Self-Healing Runbooks & Fix Procedures
                                </h3>
                                <p className="text-xs text-slate-500">Supervised 1-click and fully automated remediation playbooks to reduce Mean Time to Repair (MTTR).</p>
                            </div>
                            <span className="text-xs text-slate-500">Avg MTTR Reduction: <strong className="text-purple-700 font-mono">24.5 Mins</strong></span>
                        </div>

                        <div id="grid-itsm-runbooks" className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Populated via app.js */}
                        </div>

                        {/* Live Console Log Drawer */}
                        <div className="mt-5 p-4 bg-slate-950 text-slate-300 rounded-xl border border-slate-800 font-mono text-xs">
                            <div className="flex justify-between items-center text-[11px] text-slate-400 mb-2 border-b border-slate-800 pb-1.5">
                                <span className="flex items-center gap-1.5 text-cyan-400">
                                    <i className="fa-solid fa-terminal"></i> Self-Healing Remediation Stream
                                </span>
                                <span>Daemon: Active</span>
                            </div>
                            <div id="itsm-runbook-console" className="space-y-1 text-slate-300 max-h-40 overflow-y-auto text-[11px]">
                                <div className="text-slate-500">[IDLE] All nodes operating within healthy thresholds. Waiting for telemetry trigger...</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* SUB-VIEW 5: PROCUREMENT LOIs & SLAs */}
                <div id="itsm-subview-loi" style={{ display: activeTab === 'loi' ? 'block' : 'none' }} className="itsm-subview space-y-5">
                    {/* Procurement Letters of Intent (LOIs) Table */}
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-file-signature text-emerald-600"></i> IT Infrastructure Letters of Intent (LOIs)
                                </h3>
                                <p className="text-xs text-slate-500">Official legal procurement commitments, hardware reservations, and commercial milestones.</p>
                            </div>
                            <button onClick={() => {}} className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition flex items-center gap-1 shadow">
                                <i className="fa-solid fa-plus"></i> Draft New LOI
                            </button>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">LOI Number</th>
                                        <th className="p-3">Vendor Name</th>
                                        <th className="p-3">Asset Category</th>
                                        <th className="p-3">Contract Value</th>
                                        <th className="p-3">Delivery SLA</th>
                                        <th className="p-3">Valid Until</th>
                                        <th className="p-3">Signatory</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-itsm-lois" className="divide-y divide-slate-100">
                                    {/* Populated via app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Operational SLAs Table */}
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-900 text-sm mb-3 flex items-center gap-2">
                            <i className="fa-solid fa-handshake-angle text-blue-600"></i> Operational Service Level Agreements (SLAs)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Service Code & Name</th>
                                        <th className="p-3">Tier</th>
                                        <th className="p-3">Uptime Target</th>
                                        <th className="p-3">Current Month</th>
                                        <th className="p-3">P1 Resolution SLA</th>
                                        <th className="p-3">P2 Resolution SLA</th>
                                        <th className="p-3">Penalty / Remedy Clause</th>
                                        <th className="p-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-itsm-slas" className="divide-y divide-slate-100">
                                    {/* Populated via app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            {/* 14. Asperion Teams & Enterprise Communications Hub View */}
    </div>
  );
};

export default ITSMView;
