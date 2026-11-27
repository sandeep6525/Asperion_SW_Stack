// @ts-ignore
import { loadAnalyticsHub, switchAnalyticsTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const AnalyticsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('fin');
  useEffect(() => {
    try {
      loadAnalyticsHub();
    } catch (e) {
      console.error('Error in loadAnalyticsHub:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchAnalyticsTab(activeTab);
    } catch (e) {
      console.error('Error in switchAnalyticsTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-analytics" className="module-view ">
                <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
                            <i className="fa-solid fa-chart-line text-emerald-600"></i> Visual Intelligence & Multi-Capable Analytics Hub
                        </h2>
                        <p className="text-sm text-slate-500">Dynamic calculated metrics, multi-axis organizational radar, time-series projections, and interactive simulation sandbox.</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button onClick={() => {}} className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 border border-slate-300">
                            <i className="fa-solid fa-arrows-rotate"></i> Refresh Feeds
                        </button>
                        <button onClick={() => {}} className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition flex items-center gap-1.5 shadow-sm">
                            <i className="fa-solid fa-file-arrow-down"></i> Export Report
                        </button>
                    </div>
                </div>

                {/* Sub-Module Tabs */}
                <div className="flex overflow-x-auto border-b border-slate-200 mb-6 gap-2 text-xs font-semibold">
                    <button onClick={() => setActiveTab('fin')} id="btn-tab-fin" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-emerald-600 text-emerald-700 flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-wallet"></i> Financial & Treasury
                    </button>
                    <button onClick={() => setActiveTab('pmo')} id="btn-tab-pmo" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-diagram-project"></i> PMO & Delivery Velocity
                    </button>
                    <button onClick={() => setActiveTab('talent')} id="btn-tab-talent" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-users"></i> Talent & CTC Distribution
                    </button>
                    <button onClick={() => setActiveTab('secops')} id="btn-tab-secops" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-shield-halved"></i> SecOps & CERT-In Radar
                    </button>
                    <button onClick={() => setActiveTab('strategy')} id="btn-tab-strategy" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap">
                        <i className="fa-solid fa-compass"></i> Org Maturity Spider
                    </button>
                    <button onClick={() => setActiveTab('sim')} id="btn-tab-sim" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap bg-emerald-50 rounded-t-lg">
                        <i className="fa-solid fa-sliders text-emerald-600"></i> What-If Simulator Sandbox
                    </button>
                    <button onClick={() => setActiveTab('datascience')} id="btn-tab-datascience" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap bg-indigo-50/70 rounded-t-lg">
                        <i className="fa-solid fa-brain text-indigo-600"></i> Data Science & ML Engine
                    </button>
                    <button onClick={() => setActiveTab('decision')} id="btn-tab-decision" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap bg-blue-50/70 rounded-t-lg">
                        <i className="fa-solid fa-scale-balanced text-blue-600"></i> Decision Tower & MCDA
                    </button>
                    <button onClick={() => setActiveTab('montecarlo')} id="btn-tab-montecarlo" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap bg-purple-50/70 rounded-t-lg">
                        <i className="fa-solid fa-dice-d20 text-purple-600"></i> Monte Carlo Risk Sim
                    </button>
                    <button onClick={() => setActiveTab('infographics')} id="btn-tab-infographics" className="analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 flex items-center gap-2 whitespace-nowrap bg-teal-50/70 rounded-t-lg">
                        <i className="fa-solid fa-chart-pie text-teal-600"></i> Executive Infographics
                    </button>
                </div>

                {/* Tab 1: Financial & Treasury Intelligence */}
                <div id="analytics-pane-fin" style={{ display: activeTab === 'fin' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Total Revenue Invoiced</div>
                            <div id="v-fin-invoiced" className="text-xl font-bold text-slate-900 mt-1">₹0</div>
                            <div className="text-[11px] text-emerald-600 mt-1"><i className="fa-solid fa-circle-check"></i> Client Contracts Active</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Accounts Receivable (AR)</div>
                            <div id="v-fin-ar" className="text-xl font-bold text-amber-600 mt-1">₹0</div>
                            <div className="text-[11px] text-slate-500 mt-1">Net 30 Days Due Term</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Accounts Payable (AP)</div>
                            <div id="v-fin-ap" className="text-xl font-bold text-blue-700 mt-1">₹0</div>
                            <div className="text-[11px] text-slate-500 mt-1">Vendor & Cloud Obligations</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Treasury Cash Runway</div>
                            <div id="v-fin-runway" className="text-xl font-bold text-emerald-700 mt-1">-- Months</div>
                            <div className="text-[11px] text-emerald-600 mt-1">Based on monthly burn rate</div>
                        </div>
                    </div>

                    {/* 13-Week Cashflow Chart */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div>
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-money-bill-trend-up text-emerald-600"></i> 13-Week Direct Cash Flow & Balance Forecast
                                </h3>
                                <p className="text-xs text-slate-500">Weekly Customer Inflows vs Operational Disbursements vs Closing Treasury Position</p>
                            </div>
                        </div>
                        <div className="h-80 relative">
                            <canvas id="chart-fin-cashflow"></canvas>
                        </div>
                    </div>

                    {/* Aging Analysis and Tax Ledger */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-3 flex items-center gap-2">
                                <i className="fa-solid fa-clock-rotate-left text-amber-600"></i> Working Capital: AR vs AP Aging Analysis
                            </h3>
                            <div className="h-64 relative">
                                <canvas id="chart-fin-aging"></canvas>
                            </div>
                        </div>
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-3 flex items-center gap-2">
                                <i className="fa-solid fa-file-invoice text-blue-600"></i> Statutory Tax Matrix (GST & TDS)
                            </h3>
                            <div className="space-y-4">
                                <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-xs text-slate-500 font-medium">Output GST Invoiced (18%)</div>
                                        <div id="tax-output-gst" className="text-base font-bold text-slate-900">₹0</div>
                                    </div>
                                    <span className="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800 font-semibold">Liability</span>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-xs text-slate-500 font-medium">Input Tax Credit (ITC Available)</div>
                                        <div id="tax-itc" className="text-base font-bold text-emerald-700">₹0</div>
                                    </div>
                                    <span className="px-2 py-1 text-xs rounded bg-emerald-100 text-emerald-800 font-semibold">Credit</span>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-xs text-slate-500 font-medium">Net GST Cash Remittance Due</div>
                                        <div id="tax-net-gst" className="text-base font-bold text-rose-700">₹0</div>
                                    </div>
                                    <span className="px-2 py-1 text-xs rounded bg-rose-100 text-rose-800 font-semibold">Challan PMT-06</span>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-50 border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-xs text-slate-500 font-medium">TDS Withheld u/s 194C & 194J</div>
                                        <div id="tax-tds-due" className="text-base font-bold text-purple-700">₹0</div>
                                    </div>
                                    <span className="px-2 py-1 text-xs rounded bg-purple-100 text-purple-800 font-semibold">Challan 281</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 2: PMO & Delivery Velocity */}
                <div id="analytics-pane-pmo" style={{ display: activeTab === 'pmo' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-chart-column text-indigo-600"></i> Sprint Velocity & Story Point Throughput
                            </h3>
                            <div className="h-72 relative">
                                <canvas id="chart-pmo-velocity"></canvas>
                            </div>
                        </div>
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-list-check text-blue-600"></i> Task Pipeline Status
                            </h3>
                            <div className="h-72 relative">
                                <canvas id="chart-pmo-tasks"></canvas>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-triangle-exclamation text-amber-600"></i> RAID Matrix Severity vs Probability Heatmap
                        </h3>
                        <div className="h-64 relative">
                            <canvas id="chart-pmo-raid"></canvas>
                        </div>
                    </div>
                </div>

                {/* Tab 3: Talent & CTC Distribution */}
                <div id="analytics-pane-talent" style={{ display: activeTab === 'talent' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-chart-pie text-blue-600"></i> Department Headcount Allocation
                            </h3>
                            <div className="h-64 relative">
                                <canvas id="chart-talent-dept"></canvas>
                            </div>
                        </div>
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-layer-group text-purple-600"></i> Compensation Pyramid (CTC Slabs)
                            </h3>
                            <div className="h-64 relative">
                                <canvas id="chart-talent-slabs"></canvas>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-coins text-emerald-600"></i> Statutory CTC Cost Breakdown (Base ₹12 LPA Standard)
                        </h3>
                        <div className="h-64 relative">
                            <canvas id="chart-talent-components"></canvas>
                        </div>
                    </div>
                </div>

                {/* Tab 4: SecOps & CERT-In Defense Radar */}
                <div id="analytics-pane-secops" style={{ display: activeTab === 'secops' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">CERT-In SLA Compliance</div>
                            <div className="text-xl font-bold text-emerald-600 mt-1">100.0%</div>
                            <div className="text-[11px] text-slate-500 mt-1">Under statutory 6-hour mandate</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">Average Triage SLA</div>
                            <div className="text-xl font-bold text-blue-700 mt-1">22.5 Minutes</div>
                            <div className="text-[11px] text-slate-500 mt-1">Automated containment playbooks</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-xs text-slate-400 font-semibold uppercase">FIDO2 Passkey Adoption</div>
                            <div id="v-secops-fido2" className="text-xl font-bold text-purple-700 mt-1">66.7%</div>
                            <div className="text-[11px] text-purple-600 mt-1">Hardware & Biometric tokens</div>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-shield-virus text-rose-600"></i> Security Threat Vectors & Incident Types
                            </h3>
                            <div className="h-72 relative">
                                <canvas id="chart-secops-vectors"></canvas>
                            </div>
                        </div>
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-key text-emerald-600"></i> IAM Credential Security & Passkey Posture
                            </h3>
                            <div className="h-72 relative">
                                <canvas id="chart-secops-iam"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 5: Org Maturity Spider & Strategy Matrix */}
                <div id="analytics-pane-strategy" style={{ display: activeTab === 'strategy' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-spider text-cyan-600"></i> 6-Pillar Enterprise Organizational Maturity Radar
                            </h3>
                            <div className="h-80 relative">
                                <canvas id="chart-strategy-radar"></canvas>
                            </div>
                        </div>
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-chart-pie text-emerald-600"></i> Enterprise KPI Health & Attainment
                            </h3>
                            <div className="h-80 relative">
                                <canvas id="chart-strategy-kpis"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 6: Dynamic What-If Cashflow Simulator Sandbox */}
                <div id="analytics-pane-sim" style={{ display: activeTab === 'sim' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-slate-950 text-white rounded-xl p-6 shadow-md border border-emerald-900/50">
                        <div className="flex items-center justify-between mb-4 border-b border-emerald-800/40 pb-3">
                            <div>
                                <h3 className="text-base font-bold text-emerald-400 flex items-center gap-2">
                                    <i className="fa-solid fa-sliders"></i> Dynamic Multi-Factor What-If Cash Flow Simulator
                                </h3>
                                <p className="text-xs text-slate-400">Model strategic operational decisions in real time to assess impact on treasury liquidity and runway.</p>
                            </div>
                            <span className="text-xs bg-emerald-900 text-emerald-300 px-3 py-1 rounded-full font-mono">Live Interactive Model</span>
                        </div>

                        {/* Sliders Controls */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                            <div className="bg-slate-800/70 p-4 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-2">
                                    <label className="text-xs font-semibold text-slate-300">Collection Acceleration</label>
                                    <span id="slider-val-coll" className="text-xs font-bold font-mono text-emerald-400">+15%</span>
                                </div>
                                <input id="slider-coll" type="range" min="0" max="50" step="5" defaultValue="15" onInput={() => {}} className="w-full accent-emerald-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Accelerates client milestone payments</div>
                            </div>
                            <div className="bg-slate-800/70 p-4 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-2">
                                    <label className="text-xs font-semibold text-slate-300">Expense Optimization</label>
                                    <span id="slider-val-exp" className="text-xs font-bold font-mono text-cyan-400">-10%</span>
                                </div>
                                <input id="slider-exp" type="range" min="0" max="30" step="5" defaultValue="10" onInput={() => {}} className="w-full accent-cyan-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Reduces cloud & vendor operating costs</div>
                            </div>
                            <div className="bg-slate-800/70 p-4 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-2">
                                    <label className="text-xs font-semibold text-slate-300">New Monthly Retainer</label>
                                    <span id="slider-val-ret" className="text-xs font-bold font-mono text-purple-400">₹3,00,000</span>
                                </div>
                                <input id="slider-ret" type="range" min="0" max="1000000" step="100000" defaultValue="300000" onInput={() => {}} className="w-full accent-purple-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Additional recurring client retainer</div>
                            </div>
                        </div>

                        {/* Real-Time Impact Metric Cards */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-xs text-slate-400 font-medium">Baseline Ending Cash</div>
                                <div id="sim-base-cash" className="text-base font-bold text-slate-300 mt-1">₹76,80,000</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-xs text-emerald-400 font-medium">Simulated Ending Cash</div>
                                <div id="sim-result-cash" className="text-base font-bold text-emerald-400 mt-1">₹92,40,000</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-xs text-cyan-400 font-medium">Net Treasury Delta</div>
                                <div id="sim-cash-delta" className="text-base font-bold text-cyan-400 mt-1">+₹15,60,000</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-xs text-purple-400 font-medium">Simulated Runway</div>
                                <div id="sim-runway-months" className="text-base font-bold text-purple-400 mt-1">28.4 Months</div>
                            </div>
                        </div>
                    </div>

                    {/* Dynamic Simulation Chart */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <div>
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-chart-line text-emerald-600"></i> Simulated 13-Week Cash Flow Trajectory
                                </h3>
                                <p className="text-xs text-slate-500">Live updated curve reflecting adjusted collection velocity, expense savings, and retainers.</p>
                            </div>
                        </div>
                        <div className="h-80 relative">
                            <canvas id="chart-sim-cashflow"></canvas>
                        </div>
                    </div>
                </div>

                {/* Tab 7: Data Science & Predictive ML Engine */}
                <div id="analytics-pane-datascience" style={{ display: activeTab === 'datascience' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    {/* Top Metric Cards */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="bg-gradient-to-br from-indigo-950 to-slate-900 text-white p-4 rounded-xl border border-indigo-900/60 shadow-sm">
                            <div className="text-[11px] text-indigo-300 font-semibold uppercase tracking-wider">6-Mo Projected ARR</div>
                            <div id="ds-kpi-arr" className="text-2xl font-bold font-mono text-white mt-1">₹3,75,00,000</div>
                            <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
                                <i className="fa-solid fa-arrow-trend-up"></i> +59.5% Forecast Trajectory
                            </div>
                        </div>
                        <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-4 rounded-xl border border-indigo-900/60 shadow-sm">
                            <div className="text-[11px] text-indigo-300 font-semibold uppercase tracking-wider">ML Accuracy & ROC-AUC</div>
                            <div id="ds-kpi-acc" className="text-2xl font-bold font-mono text-cyan-300 mt-1">94.8% / 0.972</div>
                            <div className="text-[11px] text-slate-300 mt-1 flex items-center gap-1">
                                <i className="fa-solid fa-circle-check text-emerald-400"></i> F1-Score: 0.946 &bull; XGBoost
                            </div>
                        </div>
                        <div className="bg-gradient-to-br from-slate-900 to-slate-950 text-white p-4 rounded-xl border border-slate-800 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">Net Revenue Retention (NRR)</div>
                            <div id="ds-kpi-nrr" className="text-2xl font-bold font-mono text-emerald-400 mt-1">118.5%</div>
                            <div className="text-[11px] text-slate-400 mt-1">Top-Decile SaaS Expansion Rate</div>
                        </div>
                        <div className="bg-gradient-to-br from-slate-900 to-slate-950 text-white p-4 rounded-xl border border-slate-800 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">Inference Latency & Drift</div>
                            <div id="ds-kpi-latency" className="text-2xl font-bold font-mono text-purple-300 mt-1">18.4ms (P99)</div>
                            <div className="text-[11px] text-emerald-400 mt-1">PSI: 0.021 (Zero Concept Drift)</div>
                        </div>
                    </div>

                    {/* Row 1: Time-Series Revenue Forecast with 95% Confidence Bands & Churn Feature Importance */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-8 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-4">
                                <div>
                                    <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                        <i className="fa-solid fa-chart-line text-indigo-600"></i> Predictive Revenue Forecast with 95% Confidence Interval Band (ARIMA / Holt-Winters)
                                    </h3>
                                    <p className="text-xs text-slate-500">Historical 6-Month Actuals vs. 6-Month Projected Mean with &plusmn;1.96&sigma; Statistical Upper & Lower Boundaries</p>
                                </div>
                                <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded text-[11px] font-bold font-mono">
                                    CMGR: +8.5%
                                </span>
                            </div>
                            <div className="h-80 relative">
                                <canvas id="chart-ds-revenue-forecast"></canvas>
                            </div>
                        </div>
                        <div className="lg:col-span-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-900 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-chart-simple text-amber-600"></i> Churn Feature Importance
                            </h3>
                            <p className="text-xs text-slate-500 mb-3">XGBoost Feature Gini Weights</p>
                            <div className="h-80 relative">
                                <canvas id="chart-ds-churn-features"></canvas>
                            </div>
                        </div>
                    </div>

                    {/* Row 2: Customer Churn Probability Matrix & ML Confusion Matrix */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-8 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex items-center justify-between mb-3">
                                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-users-viewfinder text-blue-600"></i> Predictive Client Retention & Churn Propensity Scoring
                                </h3>
                                <span className="text-xs text-slate-500">Avg Churn Probability: <strong className="text-slate-800">23.1%</strong></span>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-xs">
                                    <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                        <tr>
                                            <th className="p-2.5">Enterprise Client</th>
                                            <th className="p-2.5">Annual ARR</th>
                                            <th className="p-2.5">Churn Probability</th>
                                            <th className="p-2.5">Risk Tier</th>
                                            <th className="p-2.5">NPS</th>
                                            <th className="p-2.5">DSO Lag</th>
                                            <th className="p-2.5 text-center">Intervention</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-ds-churn-clients" className="divide-y divide-slate-100">
                                        {/* Loaded via JS */}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div className="lg:col-span-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                                <i className="fa-solid fa-microchip text-purple-600"></i> ML Confusion Matrix & ROC
                            </h3>
                            <div className="p-3 bg-slate-950 text-white rounded-xl font-mono text-[11px] mb-3">
                                <div className="grid grid-cols-2 gap-2 text-center">
                                    <div className="p-2 bg-emerald-950/60 border border-emerald-500/40 rounded">
                                        <div className="text-[9px] text-emerald-400">True Positive (TP)</div>
                                        <div className="text-base font-bold text-emerald-300">420</div>
                                    </div>
                                    <div className="p-2 bg-rose-950/60 border border-rose-500/40 rounded">
                                        <div className="text-[9px] text-rose-400">False Positive (FP)</div>
                                        <div className="text-base font-bold text-rose-300">22</div>
                                    </div>
                                    <div className="p-2 bg-amber-950/60 border border-amber-500/40 rounded">
                                        <div className="text-[9px] text-amber-400">False Negative (FN)</div>
                                        <div className="text-base font-bold text-amber-300">17</div>
                                    </div>
                                    <div className="p-2 bg-blue-950/60 border border-blue-500/40 rounded">
                                        <div className="text-[9px] text-blue-400">True Negative (TN)</div>
                                        <div className="text-base font-bold text-blue-300">341</div>
                                    </div>
                                </div>
                            </div>
                            <div className="h-44 relative">
                                <canvas id="chart-ds-roc-curve"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 8: Decision Tower & Multi-Criteria Decision Analysis (MCDA) */}
                <div id="analytics-pane-decision" style={{ display: activeTab === 'decision' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    {/* Executive Header Banner */}
                    <div className="p-5 bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 text-white rounded-2xl border border-blue-800/40 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                        <div>
                            <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase tracking-wider">Analytic Hierarchy Process (AHP)</span>
                            <h3 className="text-lg font-bold mt-1 text-white flex items-center gap-2">
                                <i className="fa-solid fa-scale-balanced text-cyan-400"></i> Executive Decision-Making Control Tower & Strategic Scoring
                            </h3>
                            <p className="text-xs text-slate-300 mt-0.5">
                                ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED &bull; Founder & Sole Director: <strong>Varadi Vijay</strong> &bull; CIN: <span className="font-mono text-cyan-300">U85500KA2026OPC222069</span>
                            </p>
                        </div>
                        <div className="text-right">
                            <div className="text-[10px] text-slate-400 uppercase font-semibold">Bayes Factor Confidence</div>
                            <div className="text-xl font-bold font-mono text-emerald-400 mt-0.5">BF = 2.45 (Decisive Evidence)</div>
                        </div>
                    </div>

                    {/* MCDA Strategic Matrix & Radar Chart */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-8 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-900 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-ranking-star text-amber-600"></i> Strategic Initiatives Scoring Matrix (Multi-Criteria AHP)
                            </h3>
                            <p className="text-xs text-slate-500 mb-3">Weighted criteria: Financial ROI (30%), Strategic Alignment (25%), Execution Feasibility (20%), Compliance & Cyber (15%), Scalability (10%)</p>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-xs">
                                    <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                        <tr>
                                            <th className="p-2.5">Rank</th>
                                            <th className="p-2.5">Strategic Initiative</th>
                                            <th className="p-2.5">Budget</th>
                                            <th className="p-2.5">Expected NPV</th>
                                            <th className="p-2.5">Composite Score</th>
                                            <th className="p-2.5">Risk Tier</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-mcda-initiatives" className="divide-y divide-slate-100 font-medium">
                                        {/* Loaded via JS */}
                                    </tbody>
                                </table>
                            </div>

                            {/* Recommendation Callout */}
                            <div className="mt-4 p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl flex items-start gap-3">
                                <i className="fa-solid fa-circle-check text-emerald-600 text-base mt-0.5"></i>
                                <div className="text-xs text-emerald-950">
                                    <div className="font-bold text-emerald-900">Recommended Executive Decision:</div>
                                    <div id="mcda-recommendation-text" className="text-emerald-800 mt-0.5">
                                        ISO 42001 AI Management System Certification yields the highest composite score (92.4/100) with low regulatory friction and decisive customer trust dividend.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                                <i className="fa-solid fa-crosshairs text-blue-600"></i> Initiative Multi-Axis Radar
                            </h3>
                            <div className="h-72 relative">
                                <canvas id="chart-mcda-radar"></canvas>
                            </div>
                        </div>
                    </div>

                    {/* Capital Allocation & Growth Sensitivity Sandbox */}
                    <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 shadow-xl border border-indigo-900/40">
                        <div className="flex items-center justify-between mb-4 border-b border-indigo-800/40 pb-3">
                            <div>
                                <h3 className="text-base font-bold text-cyan-300 flex items-center gap-2">
                                    <i className="fa-solid fa-sliders"></i> Multi-Variable Capital Allocation & Unit Economics Simulator
                                </h3>
                                <p className="text-xs text-slate-300">Model strategic headcount hiring, AI GPU compute, and pricing elasticity to evaluate Rule of 40 and treasury runway.</p>
                            </div>
                            <span className="text-xs bg-indigo-900 text-cyan-300 px-3 py-1 rounded-full font-mono">Live Strategic Engine</span>
                        </div>

                        {/* 4 Sliders */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                            <div className="bg-slate-800/70 p-3.5 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-1.5">
                                    <label className="text-xs font-semibold text-slate-300">Headcount Additions</label>
                                    <span id="slider-val-cap-head" className="text-xs font-bold font-mono text-cyan-400">+4 Engineers</span>
                                </div>
                                <input id="slider-cap-head" type="range" min="0" max="10" step="1" defaultValue="4" onInput={() => {}} className="w-full accent-cyan-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">₹1.05L avg monthly cost/head</div>
                            </div>

                            <div className="bg-slate-800/70 p-3.5 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-1.5">
                                    <label className="text-xs font-semibold text-slate-300">AI Compute / GPU Cloud</label>
                                    <span id="slider-val-cap-gpu" className="text-xs font-bold font-mono text-purple-400">₹3,00,000/m</span>
                                </div>
                                <input id="slider-cap-gpu" type="range" min="50000" max="1000000" step="50000" defaultValue="300000" onInput={() => {}} className="w-full accent-purple-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Model fine-tuning & inference</div>
                            </div>

                            <div className="bg-slate-800/70 p-3.5 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-1.5">
                                    <label className="text-xs font-semibold text-slate-300">Enterprise Sales Spend</label>
                                    <span id="slider-val-cap-sales" className="text-xs font-bold font-mono text-emerald-400">₹2,00,000/m</span>
                                </div>
                                <input id="slider-cap-sales" type="range" min="50000" max="500000" step="50000" defaultValue="200000" onInput={() => {}} className="w-full accent-emerald-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Drives new MRR pipeline</div>
                            </div>

                            <div className="bg-slate-800/70 p-3.5 rounded-xl border border-slate-700">
                                <div className="flex justify-between items-center mb-1.5">
                                    <label className="text-xs font-semibold text-slate-300">Pricing Tier Adjustment</label>
                                    <span id="slider-val-cap-price" className="text-xs font-bold font-mono text-amber-400">+15%</span>
                                </div>
                                <input id="slider-cap-price" type="range" min="-10" max="30" step="5" defaultValue="15" onInput={() => {}} className="w-full accent-amber-500 cursor-pointer" />
                                <div className="text-[10px] text-slate-400 mt-1">Enterprise contract price elasticity</div>
                            </div>
                        </div>

                        {/* Real-Time Metrics Output Grid */}
                        <div className="grid grid-cols-2 md:grid-cols-6 gap-3 text-center mb-4">
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-slate-400 font-medium">New Monthly Burn</div>
                                <div id="cap-sim-burn" className="text-sm font-bold text-slate-200 mt-1 font-mono">₹12,70,000</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-purple-400 font-medium">Simulated Runway</div>
                                <div id="cap-sim-runway" className="text-sm font-bold text-purple-300 mt-1 font-mono">22.4 Months</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-emerald-400 font-medium">Projected ARR</div>
                                <div id="cap-sim-arr" className="text-sm font-bold text-emerald-300 mt-1 font-mono">₹1.27 Cr</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-cyan-400 font-medium">Rule of 40 Score</div>
                                <div id="cap-sim-rule40" className="text-sm font-bold text-cyan-300 mt-1 font-mono">54.2% (Pass)</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-amber-400 font-medium">LTV : CAC Ratio</div>
                                <div id="cap-sim-ltvcac" className="text-sm font-bold text-amber-300 mt-1 font-mono">1 : 4.8</div>
                            </div>
                            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                                <div className="text-[10px] text-rose-400 font-medium">Payback Period</div>
                                <div id="cap-sim-payback" className="text-sm font-bold text-rose-300 mt-1 font-mono">5.2 Months</div>
                            </div>
                        </div>

                        {/* Guidance Banner */}
                        <div id="cap-sim-guidance" className="p-3 bg-indigo-900/50 border border-indigo-700/50 rounded-xl text-xs text-indigo-200 flex items-center justify-between">
                            <span className="flex items-center gap-2">
                                <i className="fa-solid fa-circle-check text-emerald-400"></i>
                                <span><strong>OPTIMAL_EXPANSION:</strong> Robust unit economics and sustainable treasury runway. Approved for strategic execution.</span>
                            </span>
                            <span className="font-mono text-[11px] text-slate-400">Varadi Vijay, Director</span>
                        </div>
                    </div>
                </div>

                {/* Tab 9: Monte Carlo Risk & Delivery Simulation */}
                <div id="analytics-pane-montecarlo" style={{ display: activeTab === 'montecarlo' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase">P50 Expected Duration</div>
                            <div id="mc-kpi-p50" className="text-2xl font-bold font-mono text-slate-900 mt-1">82.5 Days</div>
                            <div className="text-[11px] text-slate-500 mt-1">Median Statistical Delivery</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase">P80 High-Confidence Target</div>
                            <div id="mc-kpi-p80" className="text-2xl font-bold font-mono text-blue-700 mt-1">88.0 Days</div>
                            <div className="text-[11px] text-blue-600 mt-1">80% Probability of Early/On-Time</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase">P95 Contractual SLA Target</div>
                            <div id="mc-kpi-p95" className="text-2xl font-bold font-mono text-emerald-700 mt-1">94.5 Days</div>
                            <div className="text-[11px] text-emerald-600 mt-1">Zero-Failure SLA Boundary</div>
                        </div>
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="text-[11px] text-slate-400 font-semibold uppercase">Budget Value at Risk (VaR 95%)</div>
                            <div id="mc-kpi-var" className="text-2xl font-bold font-mono text-rose-700 mt-1">₹4,20,000</div>
                            <div className="text-[11px] text-emerald-600 mt-1">Contingency Reserve: 107% Covered</div>
                        </div>
                    </div>

                    {/* Monte Carlo Bell Curve & CDF Chart */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-8 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex items-center justify-between mb-3">
                                <div>
                                    <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                        <i className="fa-solid fa-dice-d20 text-purple-600"></i> 1,000-Iteration Monte Carlo Schedule Probability Distribution (Days)
                                    </h3>
                                    <p className="text-xs text-slate-500">Stochastic Beta-PERT modeling task duration uncertainties, critical paths, and resource dependencies</p>
                                </div>
                                <span className="px-2.5 py-1 bg-purple-50 text-purple-700 border border-purple-200 rounded text-[11px] font-bold font-mono">1,000 Trials</span>
                            </div>
                            <div className="h-80 relative">
                                <canvas id="chart-mc-distribution"></canvas>
                            </div>
                        </div>
                        <div className="lg:col-span-4 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-900 text-sm mb-1 flex items-center gap-2">
                                <i className="fa-solid fa-wave-square text-indigo-600"></i> Cumulative Probability (CDF)
                            </h3>
                            <p className="text-xs text-slate-500 mb-3">Likelihood of project completion by day</p>
                            <div className="h-80 relative">
                                <canvas id="chart-mc-cdf"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 10: Executive Infographics & Board Intelligence Brief */}
                <div id="analytics-pane-infographics" style={{ display: activeTab === 'infographics' ? 'block' : 'none' }} className="analytics-pane space-y-6">
                    {/* Board Brief Header */}
                    <div className="p-6 bg-gradient-to-r from-slate-900 via-teal-950 to-slate-900 text-white rounded-2xl border border-teal-800/40 shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                        <div>
                            <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30 uppercase tracking-wider">Board Intelligence Brief</span>
                            <h3 className="text-xl font-bold mt-1 text-white flex items-center gap-2">
                                <i className="fa-solid fa-shapes text-teal-400"></i> Executive Decision Infographics & Corporate Health Matrix
                            </h3>
                            <p className="text-xs text-slate-300 mt-1">
                                <strong>ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</strong> &bull; CIN: <span className="font-mono text-teal-300">U85500KA2026OPC222069</span> &bull; Director: <strong>Varadi Vijay</strong>
                            </p>
                        </div>
                        <div className="text-right p-3 bg-white/5 rounded-xl border border-white/10">
                            <div className="text-[10px] text-teal-300 uppercase font-bold">Enterprise Health Composite Index</div>
                            <div className="text-2xl font-bold font-mono text-emerald-400 mt-0.5">96.4 / 100</div>
                            <div className="text-[10px] text-slate-300">Grade: Elite A+ &bull; Top 2% SaaS Benchmark</div>
                        </div>
                    </div>

                    {/* 6 High-Impact Visual Infographic Cards Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                        {/* Card 1: Rule of 40 */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-600 text-lg">
                                    <i className="fa-solid fa-chart-line-up"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">Exceeds Benchmark</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">Rule of 40 SaaS Index</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">58.5%</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                34.2% ARR Growth + 24.3% Operating Margin. Target &gt; 40%.
                            </div>
                        </div>

                        {/* Card 2: LTV:CAC */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center text-blue-600 text-lg">
                                    <i className="fa-solid fa-sack-dollar"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">Top-Quartile</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">LTV : CAC Unit Economics</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">1 : 5.2</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                Payback Period: 5.8 Months. Exceptionally capital-efficient.
                            </div>
                        </div>

                        {/* Card 3: Zero-Trust Security */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center text-purple-600 text-lg">
                                    <i className="fa-solid fa-shield-halved"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">Zero Critical CVEs</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">Zero-Trust Posture</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">99.4%</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                100% Passkey/MFA adoption &bull; CERT-In 6-Hour SLA verified.
                            </div>
                        </div>

                        {/* Card 4: Human Capital Efficiency */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-indigo-100 flex items-center justify-center text-indigo-600 text-lg">
                                    <i className="fa-solid fa-brain-circuit"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">+18.2% YoY</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">Talent Productivity</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">₹28.5L / Head</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                68.4% AI-assisted workflow automation multiplier.
                            </div>
                        </div>

                        {/* Card 5: Statutory Governance */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-teal-100 flex items-center justify-center text-teal-600 text-lg">
                                    <i className="fa-solid fa-scale-balanced"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-700 border border-teal-200">Zero Penalties</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">Statutory Compliance</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">100.0%</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                MCA, GST, EPFO PF, PT & Secretarial clean ledger.
                            </div>
                        </div>

                        {/* Card 6: Sprint Execution */}
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
                            <div className="flex items-center justify-between mb-3">
                                <div className="w-10 h-10 rounded-xl bg-cyan-100 flex items-center justify-center text-cyan-600 text-lg">
                                    <i className="fa-solid fa-crosshairs"></i>
                                </div>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-50 text-cyan-700 border border-cyan-200">High Predictability</span>
                            </div>
                            <div className="text-xs text-slate-400 font-semibold uppercase">Sprint Execution Ratio</div>
                            <div className="text-2xl font-bold font-mono text-slate-900 mt-1">95.6%</div>
                            <div className="text-xs text-slate-500 mt-1.5 border-t pt-2">
                                Story points committed vs delivered completion velocity.
                            </div>
                        </div>
                    </div>

                    {/* Core Decision-Making Principles Callout */}
                    <div className="p-5 bg-slate-900 text-white rounded-2xl border border-slate-800">
                        <h4 className="font-bold text-sm text-cyan-300 mb-2 flex items-center gap-2">
                            <i className="fa-solid fa-compass"></i> Core Analytical Decision-Making Principles
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
                            <div className="p-3 bg-slate-800/60 rounded-xl border border-slate-700/60">
                                <strong className="text-white block mb-1">1. Bayes Evidence Threshold</strong>
                                Require Bayes Factor BF &gt; 2.0 and positive expected NPV before approving major capital or infrastructure outlays.
                            </div>
                            <div className="p-3 bg-slate-800/60 rounded-xl border border-slate-700/60">
                                <strong className="text-white block mb-1">2. Zero-Debt Treasury</strong>
                                Maintain 100% self-sustaining operations funded purely by retained client revenue and positive net cash flow.
                            </div>
                            <div className="p-3 bg-slate-800/60 rounded-xl border border-slate-700/60">
                                <strong className="text-white block mb-1">3. Automated Verification</strong>
                                Continuous automated test suites (190+ green tests) ensuring zero functional regressions across enterprise systems.
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            
            {/* 13. Internal Cross-Departmental Service Desk & Alerts */}
    </div>
  );
};

export default AnalyticsView;
