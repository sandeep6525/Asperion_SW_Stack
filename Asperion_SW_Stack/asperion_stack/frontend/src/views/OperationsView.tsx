// @ts-ignore
import { loadOperations, switchOperationsTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const OperationsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('ledger');
  useEffect(() => {
    try {
      loadOperations();
    } catch (e) {
      console.error('Error in loadOperations:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchOperationsTab(activeTab);
    } catch (e) {
      console.error('Error in switchOperationsTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-operations" className="module-view  space-y-6">
                {/* Header Banner */}
                <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 p-6 rounded-2xl border border-slate-700/80 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-wider mb-1">
                            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                            Core Engine &bull; Module 22 &bull; ISO 27001 A.12.4 &bull; SOC 2 CC7.2 &bull; DPDP Act 2023
                        </div>
                        <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
                            <i className="fa-solid fa-cube text-cyan-400"></i> Enterprise Operations, BCP/DR & Cryptographic Event Ledger
                        </h2>
                        <p className="text-sm text-slate-300 mt-1 max-w-3xl">
                            Tamper-evident SHA-256 event sourcing ledger, automated hot-standby BCP/DR restore drill simulators, statutory India DPDP Act 2023 consent records, and SRE database optimization watchdog.
                        </p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                        <button onClick={() => {}} className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold transition shadow-lg flex items-center gap-2">
                            <i className="fa-solid fa-shield-halved"></i> Verify Cryptographic Ledger
                        </button>
                        <button onClick={() => {}} className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold transition shadow-lg flex items-center gap-2">
                            <i className="fa-solid fa-cloud-arrow-up"></i> Create Hot Snapshot
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-500/30 rounded-xl text-xs font-semibold transition flex items-center gap-1.5">
                            <i className="fa-solid fa-broom"></i> Checkpoint & Vacuum
                        </button>
                    </div>
                </div>

                {/* Executive Operational Telemetry Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Cryptographic Ledger</div>
                        <div id="ops-stat-events-count" className="text-2xl font-black text-white mt-1">--</div>
                        <div id="ops-stat-ledger-status" className="text-[11px] font-mono text-emerald-400 mt-0.5 flex items-center gap-1">
                            <i className="fa-solid fa-circle-check"></i> SHA-256 Chained
                        </div>
                    </div>
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Recovery Point (RPO)</div>
                        <div className="text-2xl font-black text-cyan-400 mt-1">&lt; 15m</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">Continuous WAL Sync</div>
                    </div>
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Recovery Time (RTO)</div>
                        <div className="text-2xl font-black text-emerald-400 mt-1">&lt; 5m</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">Automated Sandbox Mount</div>
                    </div>
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Total BCP Snapshots</div>
                        <div id="ops-stat-snapshots-count" className="text-2xl font-black text-indigo-400 mt-1">--</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">AES-256 Encrypted</div>
                    </div>
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">DPDP Statutory Consents</div>
                        <div id="ops-stat-consents-count" className="text-2xl font-black text-amber-400 mt-1">--</div>
                        <div className="text-[11px] text-slate-400 mt-0.5">India DPDP Act 2023</div>
                    </div>
                    <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl shadow">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">DB Size & Latency</div>
                        <div id="ops-stat-db-size" className="text-xl font-black text-white mt-1">--</div>
                        <div id="ops-stat-latency" className="text-[11px] font-mono text-purple-400 mt-0.5">Query: -- ms</div>
                    </div>
                </div>

                {/* Navigation Tabs */}
                <div className="border-b border-slate-800 flex items-center justify-between">
                    <div className="flex gap-2">
                        <button onClick={() => setActiveTab('ledger')} id="btn-ops-tab-ledger" className="px-4 py-2.5 text-xs font-bold border-b-2 border-cyan-500 text-cyan-400 flex items-center gap-2">
                            <i className="fa-solid fa-link"></i> Cryptographic Event Ledger
                        </button>
                        <button onClick={() => setActiveTab('bcp-dr')} id="btn-ops-tab-bcp-dr" className="px-4 py-2.5 text-xs font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2">
                            <i className="fa-solid fa-cloud-arrow-up"></i> BCP/DR Snapshots & Drills
                        </button>
                        <button onClick={() => setActiveTab('dpdp')} id="btn-ops-tab-dpdp" className="px-4 py-2.5 text-xs font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2">
                            <i className="fa-solid fa-user-shield"></i> DPDP Consent Register
                        </button>
                        <button onClick={() => setActiveTab('telemetry')} id="btn-ops-tab-telemetry" className="px-4 py-2.5 text-xs font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2">
                            <i className="fa-solid fa-gauge-high"></i> SRE Telemetry & Maintenance
                        </button>
                    </div>
                    <div className="flex items-center gap-2 py-1">
                        <span id="ops-last-verified-tag" className="text-[11px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
                            Genesis: 0000000000000000...
                        </span>
                    </div>
                </div>

                {/* TAB 1: Cryptographic Event Ledger */}
                <div id="ops-tab-ledger" style={{ display: activeTab === 'ledger' ? 'block' : 'none' }} className="space-y-4">
                    <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                        <div className="flex items-center gap-2 text-slate-300">
                            <i className="fa-solid fa-fingerprint text-cyan-400 text-base"></i>
                            <div>
                                <span className="font-bold text-white">SHA-256 Hash Chain Integrity:</span>
                                <span className="text-slate-400 ml-1">Each block derives its signature from the previous block hash, immutable payload JSON, and timestamp.</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <select id="ops-filter-aggregate-type" onChange={() => {}} className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-cyan-500">
                                <option value="">All Aggregates</option>
                                <option value="SYSTEM">SYSTEM</option>
                                <option value="BOARD_GOVERNANCE">BOARD_GOVERNANCE</option>
                                <option value="STATUTORY_FINANCE">STATUTORY_FINANCE</option>
                                <option value="ITSM_CHANGE">ITSM_CHANGE</option>
                                <option value="CLIENT_DELIVERY">CLIENT_DELIVERY</option>
                                <option value="BCP_DR_SNAPSHOT">BCP_DR_SNAPSHOT</option>
                                <option value="DPDP_CONSENT">DPDP_CONSENT</option>
                                <option value="SRE_MAINTENANCE">SRE_MAINTENANCE</option>
                            </select>
                            <button onClick={() => {}} className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium">
                                <i className="fa-solid fa-arrows-rotate"></i>
                            </button>
                        </div>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr className="bg-slate-950 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                                        <th className="py-3 px-4">Event Code</th>
                                        <th className="py-3 px-4">Aggregate Target</th>
                                        <th className="py-3 px-4">Event Type</th>
                                        <th className="py-3 px-4">Initiated By / Role</th>
                                        <th className="py-3 px-4 font-mono">Current SHA-256 Hash</th>
                                        <th className="py-3 px-4 font-mono">Prev Hash</th>
                                        <th className="py-3 px-4">Timestamp (UTC)</th>
                                        <th className="py-3 px-4 text-right">Payload</th>
                                    </tr>
                                </thead>
                                <tbody id="ops-ledger-table-body" className="divide-y divide-slate-800/60 font-mono text-slate-300">
                                    <tr>
                                        <td colSpan={8} className="text-center py-8 text-slate-500">Loading tamper-evident event stream...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 2: BCP/DR Snapshots & Drills */}
                <div id="ops-tab-bcp-dr" style={{ display: activeTab === 'bcp-dr' ? 'block' : 'none' }} className=" space-y-4">
                    <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                        <div className="flex items-center gap-2 text-slate-300">
                            <i className="fa-solid fa-shield-virus text-indigo-400 text-base"></i>
                            <div>
                                <span className="font-bold text-white">Disaster Recovery SLA Commitment:</span>
                                <span className="text-slate-400 ml-1">RPO &le; 15 mins (WAL incremental log checkpoints), RTO &le; 5 mins (hot sandbox restore test).</span>
                            </div>
                        </div>
                        <button onClick={() => {}} className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5">
                            <i className="fa-solid fa-plus"></i> New Snapshot
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="ops-snapshots-grid">
                        <div className="p-6 text-center text-slate-500 col-span-3">Loading disaster recovery snapshots...</div>
                    </div>
                </div>

                {/* TAB 3: DPDP Consent Register */}
                <div id="ops-tab-dpdp" style={{ display: activeTab === 'dpdp' ? 'block' : 'none' }} className=" space-y-4">
                    <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                        <div className="flex items-center gap-2 text-slate-300">
                            <i className="fa-solid fa-scale-balanced text-amber-400 text-base"></i>
                            <div>
                                <span className="font-bold text-white">India DPDP Act 2023 Statutory Consent Register:</span>
                                <span className="text-slate-400 ml-1">Affirmative consent records for employees, client sponsors, and vendor representatives.</span>
                            </div>
                        </div>
                        <button onClick={() => {}} className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5">
                            <i className="fa-solid fa-plus"></i> Record New Consent
                        </button>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse text-xs">
                                <thead>
                                    <tr className="bg-slate-950 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                                        <th className="py-3 px-4">Consent Ref</th>
                                        <th className="py-3 px-4">Principal Name & Type</th>
                                        <th className="py-3 px-4">Identifier / Contact</th>
                                        <th className="py-3 px-4">Purpose Category</th>
                                        <th className="py-3 px-4">Notice Reference</th>
                                        <th className="py-3 px-4">Status</th>
                                        <th className="py-3 px-4">Granted At (UTC)</th>
                                        <th className="py-3 px-4">DPO Officer</th>
                                    </tr>
                                </thead>
                                <tbody id="ops-dpdp-table-body" className="divide-y divide-slate-800/60 text-slate-300">
                                    <tr>
                                        <td colSpan={8} className="text-center py-8 text-slate-500">Loading DPDP statutory consent records...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 4: SRE Telemetry & Maintenance */}
                <div id="ops-tab-telemetry" style={{ display: activeTab === 'telemetry' ? 'block' : 'none' }} className=" space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Host Database Telemetry */}
                        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
                            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-database text-purple-400"></i> SQLite Host Telemetry & Storage Engine
                                </h3>
                                <button onClick={() => {}} className="text-xs text-purple-400 hover:text-purple-300 font-mono">
                                    <i className="fa-solid fa-arrows-rotate"></i> Refresh
                                </button>
                            </div>
                            <div className="space-y-3 text-xs">
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                    <span className="text-slate-400 font-medium">Primary SQLite Database Size</span>
                                    <span id="tel-db-size" className="font-mono font-bold text-white">--</span>
                                </div>
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                    <span className="text-slate-400 font-medium">Write-Ahead Log (WAL) Buffer</span>
                                    <span id="tel-wal-size" className="font-mono font-bold text-cyan-400">--</span>
                                </div>
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                    <span className="text-slate-400 font-medium">WAL Checkpoint Mode</span>
                                    <span id="tel-wal-mode" className="font-mono text-emerald-400 font-bold">OPTIMAL_WAL_MODE</span>
                                </div>
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                    <span className="text-slate-400 font-medium">Real-Time Query Latency (SELECT 1)</span>
                                    <span id="tel-query-latency" className="font-mono font-bold text-emerald-300">-- ms</span>
                                </div>
                                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                    <span className="text-slate-400 font-medium">Resident Memory Footprint (RSS)</span>
                                    <span id="tel-memory-rss" className="font-mono font-bold text-indigo-300">-- MB</span>
                                </div>
                            </div>
                        </div>

                        {/* Maintenance & Vacuum Actions */}
                        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-4">
                            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-wrench text-amber-400"></i> Autonomous SRE Storage Maintenance
                                </h3>
                                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Auto-Managed</span>
                            </div>
                            <p className="text-xs text-slate-300 leading-relaxed">
                                Executing a database vacuum forces SQLite to truncate its Write-Ahead Log (<code className="bg-slate-950 px-1 py-0.5 rounded text-cyan-300">PRAGMA wal_checkpoint(TRUNCATE)</code>), reclaims unallocated file pages, and guarantees zero lock contention across concurrent read/write threads.
                            </p>
                            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2 text-xs">
                                <div className="font-semibold text-slate-200">Zero-Downtime Guarantee:</div>
                                <div className="text-slate-400 text-[11px]">
                                    Vacuum runs asynchronously inside an isolated transaction block. All open HTTP sessions and WebSocket streams remain 100% operational with sub-5ms query response times.
                                </div>
                            </div>
                            <div className="pt-2">
                                <button onClick={() => {}} className="w-full py-2.5 bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white font-bold rounded-xl text-xs transition shadow-lg flex items-center justify-center gap-2">
                                    <i className="fa-solid fa-broom"></i> Execute Instant Database Vacuum & WAL Checkpoint
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* OPERATIONS MODAL 1: Create Backup Snapshot */}
            <div id="modal-create-backup-snapshot" className="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                <div className="bg-slate-900 rounded-2xl shadow-2xl border border-slate-700 max-w-lg w-full overflow-hidden">
                    <div className="p-4 bg-gradient-to-r from-blue-900 to-indigo-950 text-white flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <i className="fa-solid fa-cloud-arrow-up text-cyan-400"></i>
                            <h3 className="font-bold text-sm">Create Hot BCP/DR Snapshot</h3>
                        </div>
                        <button onClick={() => {}} className="text-slate-400 hover:text-white p-1">
                            <i className="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onSubmit={(e) => e.preventDefault()} className="p-5 space-y-4 text-xs">
                        <div>
                            <label className="block font-medium text-slate-300 mb-1">Backup Type</label>
                            <select id="ops-new-snapshot-type" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500">
                                <option value="Full SQLite Hot Backup">Full SQLite Hot Backup</option>
                                <option value="Incremental WAL Snapshot">Incremental WAL Snapshot</option>
                                <option value="Cold Disaster Recovery Archive">Cold Disaster Recovery Archive</option>
                            </select>
                        </div>
                        <div>
                            <label className="block font-medium text-slate-300 mb-1">Operational Notes / Reason</label>
                            <textarea id="ops-new-snapshot-notes" rows={3} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500" placeholder="e.g. Scheduled pre-deployment production snapshot for enterprise release v2.0"></textarea>
                        </div>
                        <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-[11px] text-slate-400 space-y-1">
                            <div className="text-cyan-400 font-semibold">Automatic Integrity Guarantees:</div>
                            <div>&bull; Real-time SHA-256 binary hash digest generated upon disk write.</div>
                            <div>&bull; Envelope encrypted under AES-256-GCM.</div>
                            <div>&bull; Recorded to tamper-evident cryptographic event ledger.</div>
                        </div>
                        <div className="flex items-center justify-end gap-2 pt-2">
                            <button type="button" onClick={() => {}} className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium">Cancel</button>
                            <button type="submit" className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold transition flex items-center gap-1.5">
                                <i className="fa-solid fa-cloud-arrow-up"></i> Generate Snapshot
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            {/* OPERATIONS MODAL 2: Record DPDP Consent */}
            <div id="modal-record-dpdp-consent" className="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                <div className="bg-slate-900 rounded-2xl shadow-2xl border border-slate-700 max-w-lg w-full overflow-hidden">
                    <div className="p-4 bg-gradient-to-r from-amber-900 to-slate-900 text-white flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <i className="fa-solid fa-scale-balanced text-amber-400"></i>
                            <h3 className="font-bold text-sm">Record India DPDP Act 2023 Consent</h3>
                        </div>
                        <button onClick={() => {}} className="text-slate-400 hover:text-white p-1">
                            <i className="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onSubmit={(e) => e.preventDefault()} className="p-5 space-y-4 text-xs">
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="block font-medium text-slate-300 mb-1">Principal Name</label>
                                <input type="text" id="ops-dpdp-name" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500" placeholder="e.g. Rahul Verma" />
                            </div>
                            <div>
                                <label className="block font-medium text-slate-300 mb-1">Principal Type</label>
                                <select id="ops-dpdp-type" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                    <option value="Employee">Employee</option>
                                    <option value="Client Sponsor">Client Sponsor</option>
                                    <option value="Vendor Contact">Vendor Contact</option>
                                    <option value="Job Candidate">Job Candidate</option>
                                </select>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="block font-medium text-slate-300 mb-1">Identifier (Email / Code)</label>
                                <input type="text" id="ops-dpdp-identifier" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500" placeholder="e.g. rahul.v@asperion.in" />
                            </div>
                            <div>
                                <label className="block font-medium text-slate-300 mb-1">Purpose Category</label>
                                <select id="ops-dpdp-purpose" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500">
                                    <option value="Statutory Payroll & Wage Code Processing">Statutory Payroll & Wage Code Processing</option>
                                    <option value="Client Contract Execution & Billing">Client Contract Execution & Billing</option>
                                    <option value="Biometric Geofence & Webcam Verification">Biometric Geofence & Webcam Verification</option>
                                    <option value="Vendor Sourcing & AP Remittance">Vendor Sourcing & AP Remittance</option>
                                    <option value="Statutory Directorship & MCA Filings">Statutory Directorship & MCA Filings</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label className="block font-medium text-slate-300 mb-1">Notice Reference</label>
                            <input type="text" id="ops-dpdp-notice" defaultValue="ADT/DPDP/NOTICE/2026/V1" className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-amber-500" />
                        </div>
                        <div>
                            <label className="block font-medium text-slate-300 mb-1">Attestation / Audit Notes</label>
                            <textarea id="ops-dpdp-notes" rows={2} className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500" placeholder="Affirmative clickwrap consent registered with IP attestation."></textarea>
                        </div>
                        <div className="flex items-center justify-end gap-2 pt-2">
                            <button type="button" onClick={() => {}} className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium">Cancel</button>
                            <button type="submit" className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-bold transition flex items-center gap-1.5">
                                <i className="fa-solid fa-check"></i> Register Statutory Consent
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            {/* OPERATIONS MODAL 3: Event Payload Viewer */}
            {/* ========================================== */}
            {/* 23. CRYPTOGRAPHIC & PKI TOOLS WORKBENCH VIEW  */}
            {/* ========================================== */}
    </div>
  );
};

export default OperationsView;
