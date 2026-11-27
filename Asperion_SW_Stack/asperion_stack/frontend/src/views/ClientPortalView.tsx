// @ts-ignore
import { loadClientPortal, switchClientPortalTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const ClientPortalView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('deliverables');
  useEffect(() => {
    try {
      loadClientPortal();
    } catch (e) {
      console.error('Error in loadClientPortal:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchClientPortalTab(activeTab);
    } catch (e) {
      console.error('Error in switchClientPortalTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-portal-client" className="module-view ">
                {/* Top Header & Client Switcher */}
                <div className="mb-6 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gradient-to-r from-slate-900 via-slate-800 to-emerald-950 p-6 rounded-2xl text-white shadow-xl border border-emerald-900/40">
                    <div>
                        <div className="flex flex-wrap items-center gap-2 mb-2">
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 uppercase tracking-wider">
                                <i className="fa-solid fa-handshake-angle mr-1"></i> Authorized Client SLA Portal
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40">
                                <i className="fa-solid fa-file-contract mr-1"></i> Active MSA & Retainer
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">
                                <i className="fa-solid fa-shield-check mr-1"></i> 99.98% SLA Availability (0 Breaches)
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                                <i className="fa-solid fa-certificate mr-1"></i> GSTIN B2B Verified
                            </span>
                        </div>
                        <div className="flex items-center gap-3.5">
                            <img src="/static/img/logo.png" alt="Asperion" className="w-12 h-12 rounded-full border border-emerald-400/40 shadow-lg object-contain bg-slate-950 p-0.5 shrink-0" />
                            <div>
                                <h2 className="text-2xl font-black text-white">Client Project Delivery, Billing & SLA Portal</h2>
                                <p className="text-xs text-slate-300 mt-0.5">
                                    Agile SOW delivery progress, UAT milestone sign-offs, commercial B2B tax invoices, change orders & 24x7 SLA support.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-2.5 self-stretch lg:self-auto justify-end">
                        {/* Client Persona Switcher */}
                        <div className="flex items-center gap-1.5 bg-slate-800/90 border border-slate-700 px-3 py-1.5 rounded-xl shadow-inner">
                            <i className="fa-solid fa-building text-emerald-400 text-xs"></i>
                            <select id="client-portal-selector" onChange={() => {}} className="bg-transparent text-white text-xs font-semibold focus:outline-none cursor-pointer">
                                <option value="Zenith Global Corp" className="bg-slate-900 text-white" selected>Zenith Global Corp (Enterprise Retainer)</option>
                                <option value="Nexus Fintech Solutions India Pvt Ltd" className="bg-slate-900 text-white">Nexus Fintech Solutions India Pvt Ltd</option>
                                <option value="Helios Cloud Technologies Pvt Ltd" className="bg-slate-900 text-white">Helios Cloud Technologies Pvt Ltd</option>
                            </select>
                        </div>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-plus-circle"></i> Log Support Ticket
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-slate-700/80 hover:bg-slate-700 text-white font-bold text-xs rounded-xl transition shadow flex items-center gap-1.5 border border-slate-600">
                            <i className="fa-solid fa-file-invoice"></i> Statement of Account (SOA)
                        </button>
                    </div>
                </div>

                {/* Executive KPI Ribbon (6 Cards) */}
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Contracted SLA</div>
                        <div id="kpi-client-sla-uptime" className="text-xl font-black text-emerald-600 mt-1">99.98%</div>
                        <div id="kpi-client-p1-response" className="text-[10px] text-slate-500 mt-0.5">P1 &lt; 1.0h (Avg: 18m)</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Active SOW Budget</div>
                        <div id="kpi-client-sow-val" className="text-xl font-black text-blue-600 mt-1">₹36,00,000</div>
                        <div className="text-[10px] text-blue-600 mt-0.5">Master Services (MSA)</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Invoiced & Billed</div>
                        <div id="kpi-client-billed-val" className="text-xl font-black text-slate-800 mt-1">₹33,98,400</div>
                        <div id="kpi-client-remitted-val" className="text-[10px] text-emerald-600 font-semibold mt-0.5">₹23,36,400 Remitted</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Balance Due</div>
                        <div id="kpi-client-balance-val" className="text-xl font-black text-amber-600 mt-1">₹10,62,000</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Net 30 Days Terms</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Milestone Progress</div>
                        <div id="kpi-client-progress-pct" className="text-xl font-black text-purple-600 mt-1">50.0%</div>
                        <div id="kpi-client-active-sprint" className="text-[10px] text-purple-600 mt-0.5 truncate">Sprint 14 Active</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Executive SPOC</div>
                        <div className="text-sm font-black text-slate-900 mt-1 truncate">Varadi Vijay</div>
                        <div className="text-[10px] text-purple-700 font-semibold mt-0.5">Director (24x7 Direct)</div>
                    </div>
                </div>

                {/* Sub-Navigation Tabs */}
                <div className="flex items-center gap-2 border-b border-slate-200 pb-3 mb-6 overflow-x-auto text-xs font-bold">
                    <button onClick={() => setActiveTab('deliverables')} id="tab-btn-client-deliverables" className="client-tab-btn active px-4 py-2 rounded-lg bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm">
                        <i className="fa-solid fa-diagram-project"></i> Project Deliverables & UAT Milestones
                    </button>
                    <button onClick={() => setActiveTab('billing')} id="tab-btn-client-billing" className="client-tab-btn px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5">
                        <i className="fa-solid fa-file-invoice-dollar"></i> Commercial Billing & Tax Invoices
                    </button>
                    <button onClick={() => setActiveTab('sla-tickets')} id="tab-btn-client-sla-tickets" className="client-tab-btn px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5">
                        <i className="fa-solid fa-headset"></i> 24x7 SLA Service Desk
                    </button>
                    <button onClick={() => setActiveTab('change-orders')} id="tab-btn-client-change-orders" className="client-tab-btn px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5">
                        <i className="fa-solid fa-code-branch"></i> Scope Change Requests (CRs)
                    </button>
                    <button onClick={() => setActiveTab('contracts')} id="tab-btn-client-contracts" className="client-tab-btn px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5">
                        <i className="fa-solid fa-file-signature"></i> Legal Contracts & Compliance
                    </button>
                </div>

                {/* TAB 1: Deliverables & Milestones */}
                <div id="client-subtab-deliverables" className="client-tab-view space-y-6">
                    {/* Project Overview Card */}
                    <div id="client-project-banner" className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <span id="client-proj-code" className="font-mono text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">ADT-PRJ-2026-002</span>
                                <span id="client-proj-status" className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Active / In Sprint 14</span>
                            </div>
                            <h3 id="client-proj-name" className="font-bold text-slate-900 text-base">Zenith Global Omni-Channel Commerce & Logistics Engine</h3>
                            <p className="text-xs text-slate-500 mt-0.5">Lead Architect: <span id="client-proj-pm" className="font-semibold text-slate-700">Arjun Sharma</span> &bull; Schedule: <span id="client-proj-dates" className="font-mono text-slate-600">2026-06-15 to 2026-12-20</span></p>
                        </div>
                        <div className="text-right">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Total Contract Value</div>
                            <div id="client-proj-budget" className="text-2xl font-black text-slate-900">₹36,00,000</div>
                        </div>
                    </div>

                    {/* Milestone UAT Acceptance Table */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-list-check text-emerald-600"></i> Phase Milestones & Client UAT Sign-off Registry
                            </h3>
                            <span className="text-xs text-slate-500">Deliverable linked billing with mandatory client sign-off</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Phase / Milestone Deliverable</th>
                                        <th className="p-3">Target Date</th>
                                        <th className="p-3">Payment Weight</th>
                                        <th className="p-3 text-right">Billing (INR)</th>
                                        <th className="p-3">UAT Status</th>
                                        <th className="p-3">Sign-off Details</th>
                                        <th className="p-3 text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-milestones" className="divide-y divide-slate-100">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Active Sprint & WBS Tasks */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 text-sm mb-3 flex items-center gap-2">
                            <i className="fa-solid fa-bars-progress text-blue-600"></i> Active Sprint Epics & WBS Engineering Tasks
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">WBS Code</th>
                                        <th className="p-2.5">Task / Epic Summary</th>
                                        <th className="p-2.5">Sprint</th>
                                        <th className="p-2.5">Assignee</th>
                                        <th className="p-2.5">Progress</th>
                                        <th className="p-2.5">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-wbs-tasks" className="divide-y divide-slate-100">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 2: Commercial Billing & Invoices */}
                <div id="client-subtab-billing" className="client-tab-view hidden space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] font-bold text-slate-400 uppercase">Gross Billed to Date</div>
                            <div id="client-bill-gross" className="text-xl font-bold text-slate-800 mt-1">₹33,98,400</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">3 Tax Invoices Issued</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] font-bold text-slate-400 uppercase">Remittances Received</div>
                            <div id="client-bill-received" className="text-xl font-bold text-emerald-600 mt-1">₹23,36,400</div>
                            <div className="text-[10px] text-emerald-600 mt-0.5">NEFT / RTGS Reconciled</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] font-bold text-slate-400 uppercase">Outstanding Balance Due</div>
                            <div id="client-bill-outstanding" className="text-xl font-bold text-amber-600 mt-1">₹10,62,000</div>
                            <div className="text-[10px] text-amber-600 mt-0.5">Due on 15-Dec-2026</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] font-bold text-slate-400 uppercase">Applicable GST SAC</div>
                            <div className="text-xl font-bold text-purple-700 mt-1">998314</div>
                            <div className="text-[10px] text-slate-500 mt-0.5">IT Software Design & Architecture</div>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-file-invoice-dollar text-emerald-600"></i> Official Commercial B2B Tax Invoices
                            </h3>
                            <button onClick={() => {}} className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-lg transition flex items-center gap-1.5 shadow">
                                <i className="fa-solid fa-print"></i> Print Statement of Account (SOA)
                            </button>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Invoice #</th>
                                        <th className="p-3">Issue Date</th>
                                        <th className="p-3">Due Date</th>
                                        <th className="p-3 text-right">Taxable (INR)</th>
                                        <th className="p-3 text-right">GST (INR)</th>
                                        <th className="p-3 text-right font-bold text-slate-900">Total (INR)</th>
                                        <th className="p-3 text-right">Received</th>
                                        <th className="p-3 text-right">Balance Due</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-invoices" className="divide-y divide-slate-100 font-mono">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 3: 24x7 SLA Service Desk */}
                <div id="client-subtab-sla-tickets" className="client-tab-view hidden space-y-6">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                        <div className="flex items-center gap-3">
                            <div className="p-2.5 bg-emerald-100 text-emerald-800 rounded-xl">
                                <i className="fa-solid fa-headset text-lg"></i>
                            </div>
                            <div>
                                <h3 className="font-bold text-slate-900 text-sm">24x7 Mission-Critical SLA Support Registry</h3>
                                <p className="text-xs text-slate-500">Target response: P1 &lt; 1.0h, P2 &lt; 4.0h &bull; Zero SLA breaches recorded</p>
                            </div>
                        </div>
                        <button onClick={() => {}} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-plus-circle"></i> Log Support Incident
                        </button>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Ticket #</th>
                                        <th className="p-3">Severity</th>
                                        <th className="p-3">Category</th>
                                        <th className="p-3">Subject / Incident Summary</th>
                                        <th className="p-3">SLA Commitment</th>
                                        <th className="p-3">Assigned SRE Lead</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3">Resolution Summary</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-tickets" className="divide-y divide-slate-100">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 4: Scope Change Requests (CRs) */}
                <div id="client-subtab-change-orders" className="client-tab-view hidden space-y-6">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-code-branch text-blue-600"></i> Scope Change Order Management (ISO 27001 / PMBOK)
                            </h3>
                            <p className="text-xs text-slate-500">Track and review commercial cost impacts and schedule deltas before contract baselining.</p>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">CR #</th>
                                        <th className="p-3">Title & Scope Modification</th>
                                        <th className="p-3">Business Rationale</th>
                                        <th className="p-3 text-right">Cost Impact (INR)</th>
                                        <th className="p-3">Schedule Delta</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3">Decision / Signatory</th>
                                        <th className="p-3 text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-crs" className="divide-y divide-slate-100">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* TAB 5: Legal Contracts & Compliance */}
                <div id="client-subtab-contracts" className="client-tab-view hidden space-y-6">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-file-contract text-purple-600"></i> Executed Master Services Agreement (MSA) & SOWs
                            </h3>
                            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Courts of Bengaluru, Karnataka Jurisdiction</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Contract Ref</th>
                                        <th className="p-3">Agreement Type</th>
                                        <th className="p-3">Effective - Expiry</th>
                                        <th className="p-3 text-right">Contract Value (INR)</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3">Stamp Duty</th>
                                        <th className="p-3">Key Terms & IP Ownership</th>
                                    </tr>
                                </thead>
                                <tbody id="table-client-contracts" className="divide-y divide-slate-100">
                                    {/* Injected by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            {/* 17. Vendor Sourcing & Procurement Dedicated Portal View */}
    </div>
  );
};

export default ClientPortalView;
