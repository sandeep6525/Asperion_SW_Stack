// @ts-ignore
import { loadInternalSupport } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const InternalSupportView: React.FC = () => {
  useEffect(() => {
    try {
      loadInternalSupport();
    } catch (e) {
      console.error('Error in loadInternalSupport:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-internal-support" className="module-view ">
                <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
                            <i className="fa-solid fa-headset text-purple-600"></i> Internal Service Desk & Cross-Group Alerts
                        </h2>
                        <p className="text-sm text-slate-500">
                            Unified employee helpdesk, SLA tracking, incident triage, and omni-channel alert bus across all enterprise departments.
                        </p>
                    </div>
                    <div className="flex items-center gap-3">
                        <button onClick={() => {}} className="text-xs font-semibold px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-300 transition flex items-center gap-1.5 shadow-sm">
                            <i className="fa-solid fa-arrows-rotate"></i> Sync System Alerts
                        </button>
                        <button onClick={() => {}} className="text-xs font-semibold px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition flex items-center gap-1.5 shadow">
                            <i className="fa-solid fa-plus"></i> Create Internal Ticket
                        </button>
                    </div>
                </div>

                {/* Service Desk Stat Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Total Service Tickets</div>
                        <div id="srv-total-tickets" className="text-2xl font-bold text-slate-900">0</div>
                        <div className="text-xs text-slate-500 mt-2">Across 7 Functional Units</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Open / In Progress</div>
                        <div id="srv-open-tickets" className="text-2xl font-bold text-amber-600">0</div>
                        <div className="text-xs text-amber-600 mt-2 font-medium"><i className="fa-solid fa-clock"></i> Active Queue</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">SLA Compliance Rate</div>
                        <div id="srv-sla-rate" className="text-2xl font-bold text-emerald-600">100.0%</div>
                        <div className="text-xs text-emerald-600 mt-2 font-medium"><i className="fa-solid fa-circle-check"></i> Standard Adherence</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Critical P1 Tickets</div>
                        <div id="srv-p1-tickets" className="text-2xl font-bold text-red-600">0</div>
                        <div className="text-xs text-red-600 mt-2 font-medium">2h SLA Window</div>
                    </div>
                </div>

                {/* Department Quick Breakdown Bar */}
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center justify-between">
                        <span>Departmental Service Desk Load</span>
                        <span className="text-[11px] font-normal text-slate-400">Click department tab below to filter</span>
                    </div>
                    <div id="dept-summary-cards" className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3 text-center">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Main Service Desk Workspace */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mb-8">
                    {/* Filters & Search Toolbar */}
                    <div className="p-4 bg-slate-50/70 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3">
                        {/* Department Tabs */}
                        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0" id="ticket-dept-filter-tabs">
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-600 text-white shadow-sm" data-dept="ALL">
                                All Departments
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="IT_INFRASTRUCTURE">
                                IT & Infrastructure
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="HR_PEOPLE">
                                HR & People
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="FINANCE_ACCOUNTS">
                                Finance & Tax
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="LEGAL_COMPLIANCE">
                                Legal
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="SECOPS_CYBER">
                                SecOps
                            </button>
                            <button onClick={() => {}} className="tkt-tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-200" data-dept="PMO_ENGINEERING">
                                PMO & Dev
                            </button>
                        </div>
                        {/* Priority & Status Dropdowns */}
                        <div className="flex items-center gap-2">
                            <select id="filter-ticket-priority" onChange={() => {}} className="text-xs bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 font-medium text-slate-700">
                                <option value="ALL">All Priorities</option>
                                <option value="P1-Critical">P1-Critical</option>
                                <option value="P2-High">P2-High</option>
                                <option value="P3-Medium">P3-Medium</option>
                                <option value="P4-Low">P4-Low</option>
                            </select>
                            <select id="filter-ticket-status" onChange={() => {}} className="text-xs bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 font-medium text-slate-700">
                                <option value="ALL">All Statuses</option>
                                <option value="Open">Open</option>
                                <option value="In Progress">In Progress</option>
                                <option value="Resolved">Resolved</option>
                            </select>
                        </div>
                    </div>

                    {/* Tickets Table */}
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-xs border-collapse">
                            <thead>
                                <tr className="bg-slate-100 text-slate-600 font-bold border-b border-slate-200">
                                    <th className="p-3.5">Ticket #</th>
                                    <th className="p-3.5">Department</th>
                                    <th className="p-3.5">Category & Subject</th>
                                    <th className="p-3.5">Priority</th>
                                    <th className="p-3.5">Requester</th>
                                    <th className="p-3.5">Assignee</th>
                                    <th className="p-3.5">SLA Target</th>
                                    <th className="p-3.5">Status</th>
                                    <th className="p-3.5 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="internal-tickets-tbody" className="divide-y divide-slate-100">
                                <tr>
                                    <td colSpan={9} className="p-8 text-center text-slate-400">Loading service desk tickets...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Cross-Functional System Alert Feed */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5">
                    <div className="flex items-center justify-between mb-4 border-b pb-3">
                        <div>
                            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-tower-broadcast text-blue-600"></i> Omni-Channel Cross-Group Notification Center
                            </h3>
                            <p className="text-xs text-slate-500">Live operational alerts across Governance, Finance, HRMS, SecOps, and Infrastructure.</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <button onClick={() => {}} className="text-xs px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded font-medium transition">
                                Mark All Read
                            </button>
                        </div>
                    </div>
                    <div id="full-notifications-feed" className="space-y-3">
                        {/* Dynamic notification items injected by app.js */}
                    </div>
                </div>
            </section>

            {/* ============================================================== */}
            {/* 13B. COMPREHENSIVE IT SERVICE MANAGEMENT (ITSM) SUITE */}
            {/* ============================================================== */}
    </div>
  );
};

export default InternalSupportView;
