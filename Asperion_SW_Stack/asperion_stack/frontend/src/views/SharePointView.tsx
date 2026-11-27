// @ts-ignore
import { loadSharePoint, switchSharePointTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const SharePointView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('sops');
  useEffect(() => {
    try {
      loadSharePoint();
    } catch (e) {
      console.error('Error in loadSharePoint:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchSharePointTab(activeTab);
    } catch (e) {
      console.error('Error in switchSharePointTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-sharepoint" className="module-view ">
                {/* Balanced Two-Column Enterprise Knowledge Hub Header */}
                <div className="mb-5 grid grid-cols-1 lg:grid-cols-12 gap-4 bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-800 text-white shadow-md">
                    {/* Main Content Area (~67% width on desktop) */}
                    <div className="lg:col-span-8 flex flex-col justify-between gap-4">
                        <div className="flex items-start sm:items-center gap-4">
                            <div className="w-12 h-12 rounded-xl bg-slate-950 border border-cyan-500/30 p-1.5 flex items-center justify-center shrink-0 shadow-sm">
                                <img src="/static/img/logo.png" alt="Asperion Brand" className="w-full h-full object-contain" />
                            </div>
                            <div className="min-w-0">
                                <h2 className="text-lg sm:text-2xl font-bold text-white tracking-tight">
                                    Asperion SharePoint &amp; Knowledge Management Hub
                                </h2>
                                <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
                                    Official centralized repository for Standard Operating Procedures (SOPs), execution mechanisms, employee thoughts, architectural blueprints, and collaborative community problem-solving.
                                </p>
                            </div>
                        </div>
                        <div className="flex flex-wrap items-center gap-2 pt-1">
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-teal-300 border border-teal-500/30">ISO 9001:2015 CERTIFIED</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-emerald-300 border border-emerald-500/30">ZERO TRUST BLUEPRINTS</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-blue-300 border border-blue-500/30">PROCEDURES &amp; SOPS</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-purple-300 border border-purple-500/30">PEER THOUGHTS &amp; Q&amp;A</span>
                        </div>
                    </div>

                    {/* Right-Side Information & Actions Panel (~33% width on desktop) */}
                    <div className="lg:col-span-4 bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between gap-3">
                        <div className="text-xs text-slate-300 font-semibold border-b border-slate-800/80 pb-2 flex items-center justify-between">
                            <span>Knowledge Actions</span>
                            <span className="text-[10px] font-mono text-cyan-400">SHAREPOINT HUB</span>
                        </div>
                        <div className="flex flex-col gap-2">
                            <button onClick={() => {}} className="w-full px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                                <i className="fa-solid fa-feather"></i> Publish Article / SOP / Thought
                            </button>
                            <button onClick={() => {}} className="w-full px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                                <i className="fa-solid fa-circle-question"></i> Ask Community Q&amp;A
                            </button>
                        </div>
                    </div>
                </div>

                {/* 5 KPI Metric Cards */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3.5 mb-5">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Processes & SOPs</span>
                            <i className="fa-solid fa-list-check text-blue-500"></i>
                        </div>
                        <div id="sp-kpi-sops" className="text-2xl font-black text-slate-800 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">ISO 9001 & 27001 Certified</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Employee Thoughts</span>
                            <i className="fa-solid fa-lightbulb text-amber-500"></i>
                        </div>
                        <div id="sp-kpi-thoughts" className="text-2xl font-black text-amber-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Ideas, reflections & posts</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Methods & Blueprints</span>
                            <i className="fa-solid fa-network-wired text-purple-500"></i>
                        </div>
                        <div id="sp-kpi-mechanisms" className="text-2xl font-black text-purple-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Technical & ops frameworks</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Community Q&A</span>
                            <i className="fa-solid fa-comments-question-check text-emerald-500"></i>
                        </div>
                        <div id="sp-kpi-questions" className="text-2xl font-black text-emerald-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Crowdsourced solutions</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Document Assets</span>
                            <i className="fa-solid fa-file-shield text-teal-500"></i>
                        </div>
                        <div id="sp-kpi-documents" className="text-2xl font-black text-teal-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Templates, DOCX & PDFs</div>
                    </div>
                </div>

                {/* Interactive Filter & Sub-Nav Bar */}
                <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-sm mb-5 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
                    {/* Tab Pills */}
                    <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0" id="sharepoint-nav-tabs">
                        <button onClick={() => setActiveTab('sops')} className="sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-teal-50 text-teal-700 border border-teal-200" data-tab="sops">
                            <i className="fa-solid fa-list-check mr-1"></i> SOPs & Procedures
                        </button>
                        <button onClick={() => setActiveTab('thoughts')} className="sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="thoughts">
                            <i className="fa-solid fa-lightbulb mr-1"></i> Employee Thoughts
                        </button>
                        <button onClick={() => setActiveTab('methods')} className="sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="methods">
                            <i className="fa-solid fa-network-wired mr-1"></i> Methods & Mechanisms
                        </button>
                        <button onClick={() => setActiveTab('community')} className="sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="community">
                            <i className="fa-solid fa-comments mr-1"></i> Community Q&A
                        </button>
                        <button onClick={() => setActiveTab('documents')} className="sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="documents">
                            <i className="fa-solid fa-folder-open mr-1"></i> Document Library
                        </button>
                    </div>

                    {/* Search & Department Filter */}
                    <div className="flex items-center gap-2">
                        <div className="relative flex-1 md:w-56">
                            <i className="fa-solid fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                            <input id="sp-search-input" onInput={() => {}} type="text" placeholder="Search knowledge..." className="w-full pl-8 pr-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-teal-500 bg-slate-50" />
                        </div>
                        <select id="sp-dept-filter" onChange={() => {}} className="text-xs border border-slate-200 rounded-lg px-2.5 py-1.5 bg-slate-50 text-slate-700 font-medium">
                            <option value="All">All Departments</option>
                            <option value="Engineering">Engineering</option>
                            <option value="Cybersecurity">Cybersecurity</option>
                            <option value="HR & Talent">HR & Talent</option>
                            <option value="Finance & Ops">Finance & Ops</option>
                            <option value="Executive & Strategy">Executive & Strategy</option>
                        </select>
                    </div>
                </div>

                {/* Dynamic Content Panes */}
                {/* Tab 1: SOPs & Procedures Pane */}
                <div id="sp-pane-sops" className="sp-tab-pane">
                    <div id="sp-list-sops" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Tab 2: Employee Thoughts & Perspectives Pane */}
                <div id="sp-pane-thoughts" className="sp-tab-pane hidden">
                    <div id="sp-list-thoughts" className="space-y-4 max-w-4xl mx-auto">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Tab 3: Methods & Mechanisms Pane */}
                <div id="sp-pane-methods" className="sp-tab-pane hidden">
                    <div id="sp-list-methods" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Tab 4: Community Q&A Pane */}
                <div id="sp-pane-community" className="sp-tab-pane hidden">
                    <div id="sp-list-community" className="space-y-4 max-w-4xl mx-auto">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Tab 5: Document Library Pane */}
                <div id="sp-pane-documents" className="sp-tab-pane hidden">
                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                            <div>
                                <h3 className="font-bold text-sm text-slate-800">Enterprise Digital Assets & Templates</h3>
                                <p className="text-xs text-slate-500">Official corporate templates, blueprints, models, and policy guides for Asperion employees.</p>
                            </div>
                            <span className="text-xs font-mono text-slate-400">Total Files: <strong id="sp-doc-lib-count">0</strong></span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs text-slate-600">
                                <thead className="bg-slate-100/70 text-slate-700 font-bold uppercase text-[10px]">
                                    <tr>
                                        <th className="p-3">Doc Code</th>
                                        <th className="p-3">Document Name</th>
                                        <th className="p-3">Format</th>
                                        <th className="p-3">Category</th>
                                        <th className="p-3">Department</th>
                                        <th className="p-3">Version</th>
                                        <th className="p-3">Uploaded By</th>
                                        <th className="p-3 text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="sp-table-documents" className="divide-y divide-slate-100">
                                    {/* Rendered by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            {/* 14C. Asperion Training Academy & New Joinee Curriculum View */}
    </div>
  );
};

export default SharePointView;
