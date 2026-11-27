// @ts-ignore
import { loadTraining, switchTrainingTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const TrainingView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('tracks');
  useEffect(() => {
    try {
      loadTraining();
    } catch (e) {
      console.error('Error in loadTraining:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchTrainingTab(activeTab);
    } catch (e) {
      console.error('Error in switchTrainingTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-training" className="module-view ">
                {/* Balanced Two-Column Enterprise LMS Header */}
                <div className="mb-5 grid grid-cols-1 lg:grid-cols-12 gap-4 bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-800 text-white shadow-md">
                    {/* Main Content Area (~67% width on desktop) */}
                    <div className="lg:col-span-8 flex flex-col justify-between gap-4">
                        <div className="flex items-start sm:items-center gap-4">
                            <div className="w-12 h-12 rounded-xl bg-slate-950 border border-cyan-500/30 p-1.5 flex items-center justify-center shrink-0 shadow-sm">
                                <img src="/static/img/logo.png" alt="Asperion Brand" className="w-full h-full object-contain" />
                            </div>
                            <div className="min-w-0">
                                <h2 className="text-lg sm:text-2xl font-bold text-white tracking-tight">
                                    Asperion Enterprise Onboarding &amp; Training Academy
                                </h2>
                                <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
                                    Structured role-based onboarding tracks, minimum &amp; maximum learning hours, interactive assessment quizzes, statutory certifications, and probation clearance governance.
                                </p>
                            </div>
                        </div>
                        <div className="flex flex-wrap items-center gap-2 pt-1">
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-amber-300 border border-amber-500/30">ROLE-BASED CURRICULUM</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-emerald-300 border border-emerald-500/30">MIN/MAX HOURS DEFINED</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-blue-300 border border-blue-500/30">ISO 9001 CLAUSE 7.2 COMPETENCE</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-purple-300 border border-purple-500/30">AUTOMATED CERTIFICATION</span>
                        </div>
                    </div>

                    {/* Right-Side Information & Actions Panel (~33% width on desktop) */}
                    <div className="lg:col-span-4 bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between gap-3">
                        <div className="text-xs text-slate-300 font-semibold border-b border-slate-800/80 pb-2 flex items-center justify-between">
                            <span>Academy Controls</span>
                            <span className="text-[10px] font-mono text-cyan-400">LMS &amp; ONBOARDING</span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <button onClick={() => {}} className="w-full px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-1.5">
                                <i className="fa-solid fa-plus-circle"></i> Add Material
                            </button>
                            <button onClick={() => {}} className="w-full px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-1.5">
                                <i className="fa-solid fa-book-medical"></i> Create Module
                            </button>
                            <button onClick={() => {}} className="sm:col-span-2 w-full px-3 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-1.5">
                                <i className="fa-solid fa-id-badge"></i> My Probation &amp; Certificates
                            </button>
                        </div>
                    </div>
                </div>

                {/* 6 KPI Metric Cards */}
                <div className="grid grid-cols-2 md:grid-cols-6 gap-3.5 mb-5">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Curriculum Tracks</span>
                            <i className="fa-solid fa-route text-amber-500"></i>
                        </div>
                        <div id="trn-kpi-tracks" className="text-2xl font-black text-slate-800 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Role Pathways</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Training Modules</span>
                            <i className="fa-solid fa-book-bookmark text-blue-500"></i>
                        </div>
                        <div id="trn-kpi-modules" className="text-2xl font-black text-blue-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Lessons & Quizzes</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Materials & Playbooks</span>
                            <i className="fa-solid fa-book-journal-whills text-emerald-500"></i>
                        </div>
                        <div id="trn-kpi-materials" className="text-2xl font-black text-emerald-600 font-mono">0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Handbooks & SOPs</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Min Training Hours</span>
                            <i className="fa-solid fa-hourglass-start text-purple-500"></i>
                        </div>
                        <div className="text-2xl font-black text-purple-600 font-mono">16.0 hrs</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Probation Threshold</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Max Training Hours</span>
                            <i className="fa-solid fa-hourglass-end text-indigo-500"></i>
                        </div>
                        <div className="text-2xl font-black text-indigo-600 font-mono">40.0 hrs</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Advanced Mastery Cap</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Hours Delivered</span>
                            <i className="fa-solid fa-award text-amber-500"></i>
                        </div>
                        <div id="trn-kpi-hours" className="text-2xl font-black text-amber-600 font-mono">0.0</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Completed Learnings</div>
                    </div>
                </div>

                {/* Interactive Filter & Sub-Nav Bar */}
                <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-sm mb-5 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
                    {/* Tab Pills */}
                    <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0" id="training-nav-tabs">
                        <button onClick={() => setActiveTab('tracks')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-amber-50 text-amber-800 border border-amber-200" data-tab="tracks">
                            <i className="fa-solid fa-route mr-1"></i> Curriculum Tracks
                        </button>
                        <button onClick={() => setActiveTab('catalog')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="catalog">
                            <i className="fa-solid fa-book-open mr-1"></i> Course Catalog
                        </button>
                        <button onClick={() => setActiveTab('materials')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="materials">
                            <i className="fa-solid fa-book-journal-whills mr-1 text-emerald-600"></i> Materials & Playbooks
                        </button>
                        <button onClick={() => setActiveTab('my-learning')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="my-learning">
                            <i className="fa-solid fa-user-graduate mr-1"></i> My Enrolled Courses
                        </button>
                        <button onClick={() => setActiveTab('compliance')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="compliance">
                            <i className="fa-solid fa-chart-pie mr-1"></i> Probation & Compliance
                        </button>
                        <button onClick={() => setActiveTab('analytics')} className="trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100" data-tab="analytics">
                            <i className="fa-solid fa-chart-line mr-1 text-purple-600"></i> Learning Intelligence & Radar
                        </button>
                    </div>

                    {/* Search & Department Filter */}
                    <div className="flex items-center gap-2">
                        <div className="relative flex-1 md:w-56">
                            <i className="fa-solid fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                            <input id="trn-search-input" onInput={() => {}} type="text" placeholder="Search courses or topics..." className="w-full pl-8 pr-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-amber-500 bg-slate-50" />
                        </div>
                        <select id="trn-dept-filter" onChange={() => {}} className="text-xs border border-slate-200 rounded-lg px-2.5 py-1.5 bg-slate-50 text-slate-700 font-medium">
                            <option value="All">All Departments</option>
                            <option value="Engineering">Engineering</option>
                            <option value="Cybersecurity">Cybersecurity</option>
                            <option value="HR & Talent">HR & Talent</option>
                            <option value="Finance & Ops">Finance & Ops</option>
                            <option value="PMO & Delivery">PMO & Delivery</option>
                            <option value="All Company">All Company</option>
                        </select>
                    </div>
                </div>

                {/* Dynamic Content Panes */}
                {/* Pane 1: Role-Based Curriculum Tracks */}
                <div id="trn-pane-tracks" className="trn-tab-pane">
                    <div id="trn-list-tracks" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Pane 2: Course Modules Catalog */}
                <div id="trn-pane-catalog" className="trn-tab-pane hidden">
                    <div id="trn-list-catalog" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Pane 3: My Enrolled Learnings */}
                <div id="trn-pane-my-learning" className="trn-tab-pane hidden">
                    <div id="trn-list-my-learning" className="space-y-4 max-w-4xl mx-auto">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Pane 4: Probation & Compliance Matrix */}
                <div id="trn-pane-compliance" className="trn-tab-pane hidden">
                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                            <div>
                                <h3 className="font-bold text-sm text-slate-800">New Joinee Probation Training Clearance Matrix</h3>
                                <p className="text-xs text-slate-500">Tracks minimum 16.0 hours mandatory compliance requirement for full probation signoff.</p>
                            </div>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs text-slate-600">
                                <thead className="bg-slate-100/70 text-slate-700 font-bold uppercase text-[10px]">
                                    <tr>
                                        <th className="p-3">Employee Name</th>
                                        <th className="p-3">Designation</th>
                                        <th className="p-3">Department</th>
                                        <th className="p-3">Enrolled</th>
                                        <th className="p-3">Completed</th>
                                        <th className="p-3">Training Hours</th>
                                        <th className="p-3">Min Required</th>
                                        <th className="p-3">Probation Clearance</th>
                                    </tr>
                                </thead>
                                <tbody id="trn-table-compliance" className="divide-y divide-slate-100">
                                    {/* Rendered by app.js */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Pane 5: Training Materials, Handbooks & Access Guides */}
                <div id="trn-pane-materials" className="trn-tab-pane hidden">
                    <div id="trn-list-materials" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {/* Rendered by app.js */}
                    </div>
                </div>

                {/* Pane 6: Learning Analytics & Competency Radar */}
                <div id="trn-pane-analytics" className="trn-tab-pane hidden space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h4 className="font-bold text-slate-800 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-chart-bar text-amber-600"></i> Department Learning Hours vs Minimum 16.0h Threshold
                            </h4>
                            <p className="text-xs text-slate-500 mb-4">Completed training hours across teams against probation threshold</p>
                            <div className="h-64 relative">
                                <canvas id="chart-trn-dept-hours"></canvas>
                            </div>
                        </div>

                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h4 className="font-bold text-slate-800 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-chart-pie text-emerald-600"></i> Role-Based Curriculum Track Completion Rates
                            </h4>
                            <p className="text-xs text-slate-500 mb-4">Percentage completion across active enterprise pathways</p>
                            <div className="h-64 relative">
                                <canvas id="chart-trn-track-completion"></canvas>
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h4 className="font-bold text-slate-800 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-award text-blue-600"></i> Assessment Score Distribution
                            </h4>
                            <p className="text-xs text-slate-500 mb-4">Quiz evaluation results (80% passing threshold)</p>
                            <div className="h-64 relative">
                                <canvas id="chart-trn-quiz-scores"></canvas>
                            </div>
                        </div>

                        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex items-center justify-between mb-3">
                                <div>
                                    <h4 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                        <i className="fa-solid fa-fire text-rose-600"></i> Top Read Playbooks & Operational Guides
                                    </h4>
                                    <p className="text-xs text-slate-500">Most referenced handbooks and SOPs across the company</p>
                                </div>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-xs text-slate-600">
                                    <thead className="bg-slate-50 text-slate-700 font-bold uppercase text-[10px]">
                                        <tr>
                                            <th className="p-2.5">Code</th>
                                            <th className="p-2.5">Title & Topic</th>
                                            <th className="p-2.5">Category</th>
                                            <th className="p-2.5">Type</th>
                                            <th className="p-2.5 text-center">Readers</th>
                                        </tr>
                                    </thead>
                                    <tbody id="trn-top-materials-table" className="divide-y divide-slate-100">
                                        {/* Rendered by JS */}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* 15. Employee Self-Service (ESS) Dedicated Portal View */}
    </div>
  );
};

export default TrainingView;
