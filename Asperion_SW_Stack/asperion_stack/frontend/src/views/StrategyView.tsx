// @ts-ignore
import { loadStrategy } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const StrategyView: React.FC = () => {
  useEffect(() => {
    try {
      loadStrategy();
    } catch (e) {
      console.error('Error in loadStrategy:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-strategy" className="module-view ">
                <div className="mb-6 flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
                            <i className="fa-solid fa-chess text-cyan-600"></i> Corporate Strategy, Function Matrix & Dynamic KPIs
                        </h2>
                        <p className="text-sm text-slate-500">Operating function maturity, capacity planning, executive decision journal, and real-time enterprise KPIs.</p>
                    </div>
                    <div className="flex gap-2">
                        <button onClick={() => {}} className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-lightbulb"></i> Log Thought / Decision
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-plus"></i> Add New KPI
                        </button>
                    </div>
                </div>

                {/* Strategy Metrics Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Operating Functions</div>
                        <div id="stat-functions-count" className="text-2xl font-bold text-slate-900">-</div>
                        <div className="text-xs text-blue-600 mt-2 font-medium">Mapped to ISO 9001 Cadence</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">KPI Health Score</div>
                        <div id="stat-kpi-health" className="text-2xl font-bold text-emerald-600">100%</div>
                        <div className="text-xs text-slate-500 mt-2">Metrics On Track / Achieved</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Executive Decisions Logged</div>
                        <div id="stat-decisions-count" className="text-2xl font-bold text-purple-700">-</div>
                        <div className="text-xs text-slate-500 mt-2">Sole Director Governance</div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Active Roadmap Milestones</div>
                        <div id="stat-roadmap-count" className="text-2xl font-bold text-amber-600">-</div>
                        <div className="text-xs text-slate-500 mt-2">Execution Workstreams</div>
                    </div>
                </div>

                {/* Dynamic Enterprise KPIs Table */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2">
                            <i className="fa-solid fa-chart-line text-emerald-600"></i> Enterprise Performance KPI Dashboard (Real-Time Metrics)
                        </h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">KPI Code</th>
                                    <th className="p-3">Category</th>
                                    <th className="p-3">Metric Name</th>
                                    <th className="p-3">Target</th>
                                    <th className="p-3">Actual Value</th>
                                    <th className="p-3">Variance</th>
                                    <th className="p-3">Status</th>
                                    <th className="p-3">Owner</th>
                                </tr>
                            </thead>
                            <tbody id="table-enterprise-kpis"></tbody>
                        </table>
                    </div>
                </div>

                {/* Strategic Functions & Capability Maturity Matrix */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <i className="fa-solid fa-sitemap text-blue-600"></i> Operating Functions & Capability Maturity Matrix (L0-L4)
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">Operating Function</th>
                                    <th className="p-3">Function Owner</th>
                                    <th className="p-3">Core Capabilities</th>
                                    <th className="p-3">Key Document Reference</th>
                                    <th className="p-3">Cadence</th>
                                    <th className="p-3">Maturity</th>
                                </tr>
                            </thead>
                            <tbody id="table-strategic-functions"></tbody>
                        </table>
                    </div>
                </div>

                {/* Capability Capacity Constraints */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <i className="fa-solid fa-gauge-high text-amber-600"></i> Capability Capacity & Bottleneck Analysis
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">Capability</th>
                                    <th className="p-3">Current Capacity</th>
                                    <th className="p-3">Target Capacity</th>
                                    <th className="p-3">Primary Constraint</th>
                                    <th className="p-3">People Requirement</th>
                                    <th className="p-3">Priority</th>
                                </tr>
                            </thead>
                            <tbody id="table-capability-capacity"></tbody>
                        </table>
                    </div>
                </div>

                {/* Executive Thought Journal & Decision Log */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <i className="fa-solid fa-brain text-purple-600"></i> Executive Decision Log & Strategic Founder Theses
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">Date</th>
                                    <th className="p-3">Entry Type</th>
                                    <th className="p-3">Title / Strategic Initiative</th>
                                    <th className="p-3">Author</th>
                                    <th className="p-3">Decision Rationale & Thesis</th>
                                    <th className="p-3">Tags</th>
                                    <th className="p-3">Status</th>
                                </tr>
                            </thead>
                            <tbody id="table-strategic-thoughts"></tbody>
                        </table>
                    </div>
                </div>

                {/* Strategic Implementation Roadmap */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <i className="fa-solid fa-road text-cyan-600"></i> Strategic Implementation Roadmap
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">Workstream</th>
                                    <th className="p-3">Action Item</th>
                                    <th className="p-3">Owner</th>
                                    <th className="p-3">Timeline</th>
                                    <th className="p-3">Progress</th>
                                    <th className="p-3">Status</th>
                                </tr>
                            </thead>
                            <tbody id="table-strategy-roadmap"></tbody>
                        </table>
                    </div>
                </div>
            </section>



            



                        {/* 12. Visual Intelligence & Analytics Hub View */}
    </div>
  );
};

export default StrategyView;
