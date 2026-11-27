// @ts-ignore
import { loadSDLC } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const SDLCView: React.FC = () => {
  useEffect(() => {
    try {
      loadSDLC();
    } catch (e) {
      console.error('Error in loadSDLC:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-sdlc" className="module-view ">
                <div className="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-100 text-cyan-800 border border-cyan-200">ISO 27001 A.14 / A.8.25-A.8.34</span>
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-100 text-purple-800 border border-purple-200">DEVSECOPS QUALITY GATES</span>
                            <span className="text-xs font-mono text-slate-500">IEEE 12207 / OWASP SAMM</span>
                        </div>
                        <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                            <i className="fa-solid fa-code-branch text-cyan-600"></i> SDLC & DevSecOps Engineering Cockpit
                        </h2>
                        <p className="text-sm text-slate-500">Full lifecycle software engineering: SRS requirements & RTM traceability, ADR architectural records, Git PR code reviews, CI/CD automated test gates, defect tracking, releases, and SRE error budgets.</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button onClick={() => {}} className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-file-circle-plus"></i> New Requirement (SRS)
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-bug"></i> Log Defect (IEEE 1044)
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-2 bg-indigo-700 hover:bg-indigo-800 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i className="fa-solid fa-rocket"></i> Run CI/CD Pipeline
                        </button>
                    </div>
                </div>

                {/* SDLC & DevSecOps 7-Stage Telemetry KPI Cards */}
                <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6 text-center">
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-blue-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">SRS Requirements</div>
                        <div id="sdlc-stat-reqs" className="text-xl font-extrabold text-blue-700 mt-0.5">5</div>
                        <div className="text-[9px] text-slate-500">100% RTM Traceability</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-indigo-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">Accepted ADRs</div>
                        <div id="sdlc-stat-adrs" className="text-xl font-extrabold text-indigo-700 mt-0.5">3</div>
                        <div className="text-[9px] text-indigo-600">Architectural Decisions</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-emerald-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">CI/CD Quality Gate</div>
                        <div id="sdlc-stat-pipeline-gate" className="text-xl font-extrabold text-emerald-600 mt-0.5">PASSED</div>
                        <div className="text-[9px] text-emerald-700 font-semibold">SAST & SCA Clean (0 CVE)</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-purple-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">PyTest Test Coverage</div>
                        <div id="sdlc-stat-coverage" className="text-xl font-extrabold text-purple-700 mt-0.5">94.8%</div>
                        <div className="text-[9px] text-slate-500">94 Automated Tests</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-amber-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">Production Release</div>
                        <div id="sdlc-stat-release" className="text-xl font-extrabold text-slate-800 mt-0.5">v1.0.0</div>
                        <div className="text-[9px] text-emerald-600">Zero Downtime Deploy</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm border-t-4 border-t-cyan-500">
                        <div className="text-[10px] font-bold text-slate-400 uppercase">p95 API Latency</div>
                        <div id="sdlc-stat-latency" className="text-xl font-extrabold text-cyan-600 mt-0.5">7.8 ms</div>
                        <div className="text-[9px] text-cyan-700 font-semibold">SRE Error Budget: 92.4%</div>
                    </div>
                </div>

                {/* Stage 1 & Stage 2: SRS Requirements Matrix & Architecture Decisions (ADR) */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    {/* SRS Requirements & RTM Table */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-list-ol text-blue-600"></i> Stage 1: Software Requirements Specification & RTM
                            </h3>
                            <span className="text-[10px] font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">ISO 27001 A.8.25</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">Req Code</th>
                                        <th className="p-2.5">Title & Specification</th>
                                        <th className="p-2.5">Category</th>
                                        <th className="p-2.5">Priority</th>
                                        <th className="p-2.5">Verification</th>
                                        <th className="p-2.5">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-reqs" className="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>

                    {/* Architecture Decision Records (ADR) Table */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-monument text-indigo-600"></i> Stage 2: Architecture Decision Records (ADRs)
                            </h3>
                            <span className="text-[10px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">IEEE / Nygard Standard</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">ADR #</th>
                                        <th className="p-2.5">Decision Title</th>
                                        <th className="p-2.5">Context & Forces</th>
                                        <th className="p-2.5">Author</th>
                                        <th className="p-2.5">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-adrs" className="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Stage 3 & Stage 4: Pull Request Peer Reviews & CI/CD DevSecOps Quality Gates */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    {/* Pull Request Reviews */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-code-pull-request text-purple-600"></i> Stage 3: Git Pull Requests & Peer Code Review
                            </h3>
                            <span className="text-[10px] font-semibold text-purple-600 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">4-Eyes Review Principle</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">PR #</th>
                                        <th className="p-2.5">Branch & Title</th>
                                        <th className="p-2.5">Author</th>
                                        <th className="p-2.5">Peer Reviewers</th>
                                        <th className="p-2.5">Sec Sign-Off</th>
                                        <th className="p-2.5">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-prs" className="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>

                    {/* CI/CD Pipelines & Quality Gates */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-shield-halved text-emerald-600"></i> Stage 4: CI/CD DevSecOps Automated Quality Gates
                            </h3>
                            <span className="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">OWASP SAMM & SAST</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">Pipeline Code</th>
                                        <th className="p-2.5">Commit SHA</th>
                                        <th className="p-2.5 text-right">Tests Passed</th>
                                        <th className="p-2.5 text-right">Coverage</th>
                                        <th className="p-2.5">SAST / SCA Status</th>
                                        <th className="p-2.5">Gate Result</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-pipelines" className="divide-y divide-slate-100 font-mono"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Stage 5, 6 & 7: Defect Tracking, Production Releases & SRE Telemetry */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                    {/* Defects / Bug Tracking */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-bug text-rose-600"></i> Stage 5: Defect Tracking (IEEE 1044)
                            </h3>
                            <span className="text-[10px] font-semibold text-rose-600">Zero Critical</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2">Bug ID</th>
                                        <th className="p-2">Title</th>
                                        <th className="p-2">Sev</th>
                                        <th className="p-2">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-bugs" className="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>

                    {/* Production Release Deployments */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-box-archive text-blue-600"></i> Stage 6: Semantic Releases & CAB
                            </h3>
                            <span className="text-[10px] font-semibold text-emerald-600">Blue-Green Active</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2">Tag</th>
                                        <th className="p-2">Strategy</th>
                                        <th className="p-2">CAB Approval</th>
                                        <th className="p-2">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-sdlc-releases" className="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>

                    {/* SRE Telemetry & Observability */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-gauge-high text-cyan-600"></i> Stage 7: SRE Error Budgets & SLO
                            </h3>
                            <span className="text-[10px] font-semibold text-cyan-700">99.98% 30d Uptime</span>
                        </div>
                        <div className="space-y-2.5 text-xs">
                            <div className="flex justify-between p-2 rounded bg-slate-50 border">
                                <span className="text-slate-600 font-medium">p95 / p99 Latency:</span>
                                <span className="font-mono font-bold text-cyan-700"><span id="sre-p95-val">7.8</span>ms / <span id="sre-p99-val">13.4</span>ms</span>
                            </div>
                            <div className="flex justify-between p-2 rounded bg-slate-50 border">
                                <span className="text-slate-600 font-medium">HTTP 5xx Error Rate:</span>
                                <span className="font-mono font-bold text-emerald-600"><span id="sre-error-rate-val">0.01</span>%</span>
                            </div>
                            <div className="flex justify-between p-2 rounded bg-slate-50 border">
                                <span className="text-slate-600 font-medium">SLO Error Budget:</span>
                                <span className="font-mono font-bold text-emerald-600"><span id="sre-budget-val">92.4</span>% remaining</span>
                            </div>
                            <div className="flex justify-between p-2 rounded bg-slate-50 border">
                                <span className="text-slate-600 font-medium">Memory / CPU:</span>
                                <span className="font-mono text-slate-800"><span id="sre-mem-val">176.2</span> MB / <span id="sre-cpu-val">11.8</span>%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* 7. Comprehensive Vendor Management & Strategic Sourcing View */}
    </div>
  );
};

export default SDLCView;
