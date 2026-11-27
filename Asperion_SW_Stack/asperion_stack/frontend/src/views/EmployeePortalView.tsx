// @ts-ignore
import { loadEmployeePortal, switchESSTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const EmployeePortalView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('cockpit');
  useEffect(() => {
    try {
      loadEmployeePortal();
    } catch (e) {
      console.error('Error in loadEmployeePortal:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchESSTab(activeTab);
    } catch (e) {
      console.error('Error in switchESSTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-portal-employee" className="module-view ">
                {/* Top Enterprise Header with Profile Switcher & Action Center */}
                <div className="mb-6 bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white shadow-xl">
                    <div className="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4">
                        <div className="flex items-center gap-4">
                            <div className="relative">
                                <div id="ess-emp-avatar" className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center text-white text-xl font-bold shadow-lg border border-white/20">
                                    AS
                                </div>
                                <span className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 border-2 border-slate-900 rounded-full" title="Online & Geofence Verified"></span>
                            </div>
                            <div>
                                <div className="flex flex-wrap items-center gap-2 mb-1">
                                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-400/30">DIGITAL WORKPLACE & ESS</span>
                                    <span className="text-[11px] font-mono text-slate-400">ASPERION DIGITAL TECHNOLOGIES (OPC) PVT LTD &bull; CIN: U85500KA2026OPC222069</span>
                                </div>
                                <div className="flex flex-wrap items-center gap-3">
                                    <h2 id="ess-emp-name" className="text-2xl font-bold tracking-tight text-white">Arjun Sharma</h2>
                                    <span id="ess-emp-code" className="text-xs font-mono px-2 py-0.5 bg-slate-800 rounded text-cyan-400 border border-slate-700">ADT-EMP-001</span>
                                    <span id="ess-emp-designation" className="text-xs text-slate-300 font-medium">Principal Cloud Architect</span>
                                    <span className="text-slate-500">&bull;</span>
                                    <span id="ess-emp-department" className="text-xs text-slate-400">Cloud & DevSecOps</span>
                                </div>
                            </div>
                        </div>

                        {/* Employee Profile Switcher & Action Buttons */}
                        <div className="flex flex-wrap items-center gap-2 w-full xl:w-auto justify-start xl:justify-end">
                            <div className="flex items-center gap-1.5 bg-slate-800/90 border border-slate-700 rounded-lg px-2.5 py-1.5">
                                <i className="fa-solid fa-user-gear text-slate-400 text-xs"></i>
                                <label htmlFor="ess-employee-selector" className="text-[10px] text-slate-400 uppercase font-bold mr-1">Switch Staff:</label>
                                <select id="ess-employee-selector" onChange={() => {}} className="bg-transparent text-xs text-white font-semibold focus:outline-none cursor-pointer">
                                    <option value="ADT-EMP-001" className="bg-slate-900 text-white">ADT-EMP-001 &bull; Arjun Sharma</option>
                                    <option value="ADT-EMP-002" className="bg-slate-900 text-white">ADT-EMP-002 &bull; Priya Nair</option>
                                    <option value="ADT-EMP-003" className="bg-slate-900 text-white">ADT-EMP-003 &bull; Vikram Rathore</option>
                                    <option value="ADT-EMP-004" className="bg-slate-900 text-white">ADT-EMP-004 &bull; Sneha Rao</option>
                                </select>
                            </div>

                            <button onClick={() => {}} className="px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition shadow-md flex items-center gap-1.5">
                                <i className="fa-solid fa-fingerprint"></i> Quick Punch In / Out
                            </button>
                            <button onClick={() => {}} className="px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg transition shadow-md flex items-center gap-1.5">
                                <i className="fa-solid fa-calendar-plus"></i> Apply Leave
                            </button>
                            <button onClick={() => {}} className="px-3 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-lg transition shadow-md flex items-center gap-1.5">
                                <i className="fa-solid fa-headset"></i> Raise Ticket
                            </button>
                            <button onClick={() => {}} className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-bold text-xs rounded-lg border border-slate-700 transition shadow-sm flex items-center gap-1.5">
                                <i className="fa-solid fa-id-card"></i> Digital ID Card
                            </button>
                        </div>
                    </div>

                    {/* Security & Identity Posture Strip */}
                    <div className="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between text-xs gap-3">
                        <div className="flex flex-wrap items-center gap-2">
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950/80 text-emerald-400 border border-emerald-800/50 flex items-center gap-1">
                                <i className="fa-solid fa-shield-halved text-[9px]"></i> FIDO2 Passkey Bound
                            </span>
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-950/80 text-blue-400 border border-blue-800/50 flex items-center gap-1">
                                <i className="fa-solid fa-network-wired text-[9px]"></i> Zero Trust ZTNA Active
                            </span>
                            <span id="ess-badge-geofence" className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-950/80 text-purple-400 border border-purple-800/50 flex items-center gap-1">
                                <i className="fa-solid fa-location-dot text-[9px]"></i> Horamavu HQ Geofenced (200m)
                            </span>
                            <span id="ess-badge-probation" className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-950/80 text-cyan-400 border border-cyan-800/50 flex items-center gap-1">
                                <i className="fa-solid fa-certificate text-[9px]"></i> Confirmed Permanent
                            </span>
                        </div>
                        <div className="text-[11px] text-slate-400">
                            Authorized Reporting: <strong className="text-slate-200">Varadi Vijay (Sole Director)</strong> &bull; Bangalore HQ
                        </div>
                    </div>
                </div>

                {/* 6 Top KPI Metrics */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Fixed Annual CTC</div>
                        <div id="ess-kpi-annual-ctc" className="text-lg font-black text-slate-900 mt-1">₹1,440,000</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Gross/Mo: <strong id="ess-kpi-monthly-gross" className="text-slate-700">₹120,000</strong></div>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Disbursed Take-Home</div>
                        <div id="ess-kpi-net-takehome" className="text-lg font-black text-emerald-600 mt-1">₹115,296</div>
                        <div className="text-[10px] text-emerald-600 mt-0.5">NEFT Credit: <strong id="ess-kpi-bank-account" className="text-emerald-700">ICICI Bank</strong></div>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Attendance Index</div>
                        <div id="ess-kpi-attendance-pct" className="text-lg font-black text-blue-600 mt-1">98.4%</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Avg Work: <strong id="ess-kpi-avg-hours" className="text-slate-700">8.5 hrs/day</strong></div>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Leave Balance</div>
                        <div id="ess-kpi-leave-balance" className="text-lg font-black text-indigo-600 mt-1">26.0 Days</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Consumed: <strong id="ess-kpi-leave-consumed" className="text-slate-700">4.0 Days</strong></div>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Learning Academy</div>
                        <div id="ess-kpi-learning-hours" className="text-lg font-black text-purple-600 mt-1">24.5 Hrs</div>
                        <div className="text-[10px] text-purple-600 mt-0.5"><strong id="ess-kpi-certs-count">3 Certificates</strong> (16h Req)</div>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:shadow transition">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">IT Hardware & Passkeys</div>
                        <div id="ess-kpi-assets-count" className="text-lg font-black text-cyan-700 mt-1">2 Hardware</div>
                        <div className="text-[10px] text-cyan-700 mt-0.5">BitLocker Encrypted &bull; FIDO2</div>
                    </div>
                </div>

                {/* 6-Tab Navigation Bar */}
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-1.5 mb-6 flex flex-wrap gap-1" id="ess-tab-buttons">
                    <button onClick={() => setActiveTab('cockpit')} id="tab-btn-ess-cockpit" className="ess-nav-tab active px-3.5 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-sm flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-chart-pie"></i> Cockpit & Analytics
                    </button>
                    <button onClick={() => setActiveTab('compensation')} id="tab-btn-ess-compensation" className="ess-nav-tab px-3.5 py-2 text-xs font-bold rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-indian-rupee-sign"></i> Wage Code Compensation
                    </button>
                    <button onClick={() => setActiveTab('attendance')} id="tab-btn-ess-attendance" className="ess-nav-tab px-3.5 py-2 text-xs font-bold rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-clock"></i> Attendance & Geofence
                    </button>
                    <button onClick={() => setActiveTab('leaves')} id="tab-btn-ess-leaves" className="ess-nav-tab px-3.5 py-2 text-xs font-bold rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-plane-departure"></i> Leaves & Holidays
                    </button>
                    <button onClick={() => setActiveTab('learning')} id="tab-btn-ess-learning" className="ess-nav-tab px-3.5 py-2 text-xs font-bold rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-graduation-cap"></i> Academy & Certifications
                    </button>
                    <button onClick={() => setActiveTab('assets')} id="tab-btn-ess-assets" className="ess-nav-tab px-3.5 py-2 text-xs font-bold rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition">
                        <i className="fa-solid fa-laptop-code"></i> IT Assets & Helpdesk
                    </button>
                </div>

                {/* ================= TAB 1: COCKPIT & VISUAL ANALYTICS ================= */}
                <div id="ess-tab-cockpit" style={{ display: activeTab === 'cockpit' ? 'block' : 'none' }} className="ess-tab-pane">
                    {/* Charts Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        {/* Chart 1: Compensation Composition */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-1.5">
                                    <i className="fa-solid fa-chart-pie text-blue-600"></i> Wage Code 2019 Breakup
                                </h3>
                                <span className="text-[10px] text-slate-400">Monthly</span>
                            </div>
                            <div className="h-56 relative flex items-center justify-center">
                                <canvas id="chart-ess-compensation"></canvas>
                            </div>
                            <div className="mt-3 pt-3 border-t border-slate-100 text-[11px] flex justify-between text-slate-600">
                                <span>Basic: <strong className="text-slate-900" id="ess-chart-basic">₹48,000</strong></span>
                                <span>HRA: <strong className="text-slate-900" id="ess-chart-hra">₹19,200</strong></span>
                                <span>Allowances: <strong className="text-slate-900" id="ess-chart-allow">₹52,800</strong></span>
                            </div>
                        </div>

                        {/* Chart 2: Attendance Punch Pattern */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-1.5">
                                    <i className="fa-solid fa-chart-column text-emerald-600"></i> Recent Work Hours
                                </h3>
                                <span className="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded">Standard 8.5h</span>
                            </div>
                            <div className="h-56 relative">
                                <canvas id="chart-ess-attendance"></canvas>
                            </div>
                            <div className="mt-3 pt-3 border-t border-slate-100 text-[11px] flex justify-between text-slate-600">
                                <span>Geofence Compliance: <strong className="text-emerald-600" id="ess-chart-geofence">98.4%</strong></span>
                                <span>Liveness Match: <strong className="text-blue-600">98.5%</strong></span>
                            </div>
                        </div>

                        {/* Chart 3: Leave Utilization */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-1.5">
                                    <i className="fa-solid fa-chart-donut text-indigo-600"></i> Leave Utilization
                                </h3>
                                <span className="text-[10px] text-slate-400">Annual 30 Days</span>
                            </div>
                            <div className="h-56 relative flex items-center justify-center">
                                <canvas id="chart-ess-leaves"></canvas>
                            </div>
                            <div className="mt-3 pt-3 border-t border-slate-100 text-[11px] flex justify-between text-slate-600">
                                <span>Earned (EL): <strong className="text-indigo-600" id="ess-chart-el">18.0</strong></span>
                                <span>Casual/Sick: <strong className="text-amber-600" id="ess-chart-cl">12.0</strong></span>
                                <span>Taken: <strong className="text-slate-900" id="ess-chart-taken">4.0</strong></span>
                            </div>
                        </div>
                    </div>

                    {/* Bottom Grid: Statutory Dossier & Quick Handbooks */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        {/* Statutory Profile Dossier */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-xs uppercase tracking-wider mb-4 flex items-center gap-1.5">
                                <i className="fa-solid fa-id-card-clip text-blue-600"></i> Statutory & Personnel Dossier
                            </h3>
                            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">PAN Number</div>
                                    <div id="ess-stat-pan" className="font-mono font-bold text-slate-800 mt-1">AAACA1234D</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">Aadhaar (Masked)</div>
                                    <div id="ess-stat-aadhaar" className="font-mono font-bold text-slate-800 mt-1">•••• •••• 9012</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">EPFO UAN</div>
                                    <div id="ess-stat-uan" className="font-mono font-bold text-slate-800 mt-1">101928374650</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">ESIC IP Number</div>
                                    <div id="ess-stat-esic" className="font-mono font-bold text-slate-800 mt-1">55001234560010001</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">Salary Bank & IFSC</div>
                                    <div id="ess-stat-bank" className="font-semibold text-slate-800 mt-1 truncate">ICICI Bank &bull; ICIC0001234</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">Joining & Confirmation</div>
                                    <div id="ess-stat-doj" className="font-semibold text-slate-800 mt-1">2026-01-15 (Confirmed)</div>
                                </div>
                            </div>
                        </div>

                        {/* Enterprise SOPs, Handbooks & Playbooks */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-xs uppercase tracking-wider mb-4 flex items-center gap-1.5">
                                <i className="fa-solid fa-book-bookmark text-indigo-600"></i> Corporate Handbooks & Playbooks
                            </h3>
                            <div className="space-y-2.5 text-xs" id="ess-handbooks-container">
                                <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg hover:bg-slate-100 transition border border-slate-100">
                                    <div className="flex items-center gap-2.5">
                                        <i className="fa-solid fa-file-shield text-blue-600"></i>
                                        <div>
                                            <div className="font-bold text-slate-800">Information Security & Acceptable Use Policy</div>
                                            <div className="text-[10px] text-slate-500">ISO 27001:2022 &bull; ZTNA & FIDO2 passkey controls</div>
                                        </div>
                                    </div>
                                    <button onClick={() => {}} className="text-blue-600 hover:text-blue-800 text-[11px] font-bold">Read &bull; 15 min</button>
                                </div>
                                <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg hover:bg-slate-100 transition border border-slate-100">
                                    <div className="flex items-center gap-2.5">
                                        <i className="fa-solid fa-hand-holding-hand text-pink-600"></i>
                                        <div>
                                            <div className="font-bold text-slate-800">POSH & Anti-Harassment Enterprise Charter</div>
                                            <div className="text-[10px] text-slate-500">Statutory POSH Act 2013 Internal Complaints Committee</div>
                                        </div>
                                    </div>
                                    <button onClick={() => {}} className="text-blue-600 hover:text-blue-800 text-[11px] font-bold">Read &bull; 10 min</button>
                                </div>
                                <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg hover:bg-slate-100 transition border border-slate-100">
                                    <div className="flex items-center gap-2.5">
                                        <i className="fa-solid fa-laptop-house text-emerald-600"></i>
                                        <div>
                                            <div className="font-bold text-slate-800">Remote Work, Attendance & Geofencing SOP</div>
                                            <div className="text-[10px] text-slate-500">Horamavu HQ 200m perimeter & approved telecommute</div>
                                        </div>
                                    </div>
                                    <button onClick={() => {}} className="text-blue-600 hover:text-blue-800 text-[11px] font-bold">Read &bull; 12 min</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* ================= TAB 2: COMPENSATION & PAYSLIPS ================= */}
                <div id="ess-tab-compensation" style={{ display: activeTab === 'compensation' ? 'block' : 'none' }} className="ess-tab-pane ">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        {/* Wage Code 2019 Statutory Breakdown */}
                        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-4">
                                <div>
                                    <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                        <i className="fa-solid fa-scale-balanced text-blue-600"></i> Code on Wages 2019 Structured Earnings
                                    </h3>
                                    <p className="text-[11px] text-slate-500 mt-0.5">Compliant with Section 115BAC (New Tax Regime - Nil Tax up to ₹7.75 Lakhs with Standard Deduction).</p>
                                </div>
                                <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-[10px] font-bold">
                                    Basic ≥ 40% Compliance
                                </span>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                {/* Gross Earnings */}
                                <div>
                                    <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 pb-1 border-b">Gross Earnings (Monthly)</h4>
                                    <table className="w-full text-xs">
                                        <tbody className="divide-y divide-slate-100">
                                            <tr>
                                                <td className="py-2 text-slate-600">Basic Salary (40%)</td>
                                                <td id="comp-basic" className="py-2 text-right font-bold text-slate-800">₹48,000</td>
                                            </tr>
                                            <tr>
                                                <td className="py-2 text-slate-600">House Rent Allowance (HRA)</td>
                                                <td id="comp-hra" className="py-2 text-right font-bold text-slate-800">₹19,200</td>
                                            </tr>
                                            <tr>
                                                <td className="py-2 text-slate-600">Special / Flexi Allowance</td>
                                                <td id="comp-special" className="py-2 text-right font-bold text-slate-800">₹52,800</td>
                                            </tr>
                                            <tr className="bg-slate-50 font-bold text-slate-900">
                                                <td className="py-2.5 px-2">Total Monthly Gross</td>
                                                <td id="comp-gross" className="py-2.5 px-2 text-right text-blue-600">₹120,000</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                {/* Deductions & Statutory Contributions */}
                                <div>
                                    <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 pb-1 border-b">Deductions & Contributions</h4>
                                    <table className="w-full text-xs">
                                        <tbody className="divide-y divide-slate-100">
                                            <tr>
                                                <td className="py-2 text-slate-600">Employee EPF (12% of Basic)</td>
                                                <td id="comp-pf-ee" className="py-2 text-right font-bold text-red-600">-₹1,800</td>
                                            </tr>
                                            <tr>
                                                <td className="py-2 text-slate-600">Karnataka Professional Tax (PT)</td>
                                                <td id="comp-pt" className="py-2 text-right font-bold text-red-600">-₹200</td>
                                            </tr>
                                            <tr>
                                                <td className="py-2 text-slate-600">Income Tax (TDS u/s 115BAC)</td>
                                                <td id="comp-tds" className="py-2 text-right font-bold text-red-600">-₹2,704</td>
                                            </tr>
                                            <tr className="bg-emerald-50 font-bold text-emerald-900">
                                                <td className="py-2.5 px-2">Net Disbursed In-Hand</td>
                                                <td id="comp-net" className="py-2.5 px-2 text-right text-emerald-700 font-black">₹115,296</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-3 text-xs bg-slate-50 p-3 rounded-lg">
                                <div>
                                    <span className="text-slate-500">Employer EPF (12% Matching):</span>
                                    <strong id="comp-pf-er" className="text-slate-800 ml-1">₹1,800 / mo</strong>
                                </div>
                                <div>
                                    <span className="text-slate-500">Gratuity Provision (4.81% Basic):</span>
                                    <strong id="comp-gratuity" className="text-slate-800 ml-1">₹2,308 / mo</strong>
                                </div>
                            </div>
                        </div>

                        {/* Income Tax & Form 16 Card */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                            <div>
                                <h3 className="font-bold text-slate-800 text-sm mb-2 flex items-center gap-2">
                                    <i className="fa-solid fa-file-invoice-dollar text-purple-600"></i> Tax Compliance (115BAC)
                                </h3>
                                <p className="text-xs text-slate-500 mb-4">Direct tax computed as per Finance Act default tax slab. Standard deduction of ₹75,000 applied.</p>
                                
                                <div className="space-y-2 text-xs">
                                    <div className="flex justify-between p-2 bg-slate-50 rounded">
                                        <span className="text-slate-600">Annual Taxable Gross:</span>
                                        <strong id="tax-annual-gross" className="font-mono text-slate-800">₹1,440,000</strong>
                                    </div>
                                    <div className="flex justify-between p-2 bg-slate-50 rounded">
                                        <span className="text-slate-600">Standard Deduction:</span>
                                        <strong className="font-mono text-emerald-600">₹75,000</strong>
                                    </div>
                                    <div className="flex justify-between p-2 bg-slate-50 rounded">
                                        <span className="text-slate-600">Health & Edu Cess:</span>
                                        <strong className="font-mono text-slate-800">4%</strong>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-4 pt-3 border-t border-slate-100">
                                <button onClick={() => {}} className="w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs rounded-lg transition flex items-center justify-center gap-1.5">
                                    <i className="fa-solid fa-download"></i> Download Form 16 (TRACES)
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Official Downloadable Salary Slips Table */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-receipt text-blue-600"></i> Official Disbursed Payslips & Salary Statements
                            </h3>
                            <span className="text-xs text-slate-400">Company Seal & Director Signature Verified</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Salary Cycle</th>
                                        <th className="p-3 text-right">Earned Gross</th>
                                        <th className="p-3 text-right">Total Deductions</th>
                                        <th className="p-3 text-right font-bold text-slate-800">Net Take-Home</th>
                                        <th className="p-3">Bank UTR Reference</th>
                                        <th className="p-3 text-center">Formal Payslip</th>
                                    </tr>
                                </thead>
                                <tbody id="table-ess-payslips" className="divide-y divide-slate-100 font-mono">
                                    {/* Rendered dynamically */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* ================= TAB 3: ATTENDANCE & GEOFENCING ================= */}
                <div id="ess-tab-attendance" style={{ display: activeTab === 'attendance' ? 'block' : 'none' }} className="ess-tab-pane ">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        {/* Geofence & Liveness Live Verification Card */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 text-sm mb-2 flex items-center gap-2">
                                <i className="fa-solid fa-satellite-dish text-emerald-600"></i> Live Geofence & Liveness Radar
                            </h3>
                            <p className="text-xs text-slate-500 mb-4">Official Horamavu HQ Coordinates & Real-Time Haversine Boundary Distance.</p>

                            <div className="space-y-3 text-xs mb-4">
                                <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                                    <div className="text-[10px] uppercase font-bold text-slate-400">Registered HQ Location</div>
                                    <div className="font-bold text-slate-800 mt-0.5">Lakshith Properties, Horamavu Bangalore</div>
                                    <div className="font-mono text-[10px] text-slate-500">13.035820° N, 77.653410° E</div>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-[10px] uppercase font-bold text-slate-400">Geofence Perimeter</div>
                                        <div className="font-bold text-slate-800 mt-0.5">200.0 Meters Radius</div>
                                    </div>
                                    <span className="px-2 py-1 bg-emerald-100 text-emerald-800 font-bold text-[10px] rounded-full">Active In-Range</span>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                                    <div>
                                        <div className="text-[10px] uppercase font-bold text-slate-400">Current Measured Distance</div>
                                        <div id="ess-geo-distance" className="font-bold font-mono text-emerald-600 mt-0.5">14.8 Meters from Desk</div>
                                    </div>
                                    <span className="text-xs font-bold text-emerald-600"><i className="fa-solid fa-circle-check"></i> Passed</span>
                                </div>
                            </div>

                            <button onClick={() => {}} className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow transition flex items-center justify-center gap-2">
                                <i className="fa-solid fa-fingerprint text-base"></i> Trigger Instant Biometric Punch
                            </button>
                        </div>

                        {/* Punch Log Table */}
                        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-calendar-check text-blue-600"></i> Biometric Attendance Punch History
                                </h3>
                                <span className="text-xs text-slate-400">Real-time Kiosk, Portal & Facial Sync</span>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-xs">
                                    <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                        <tr>
                                            <th className="p-2.5">Date</th>
                                            <th className="p-2.5">Clock In</th>
                                            <th className="p-2.5">Clock Out</th>
                                            <th className="p-2.5 text-right">Work Hours</th>
                                            <th className="p-2.5">Channel</th>
                                            <th className="p-2.5">Status</th>
                                            <th className="p-2.5">Geofence</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-ess-attendance" className="divide-y divide-slate-100 font-mono">
                                        {/* Rendered dynamically */}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                {/* ================= TAB 4: LEAVES & HOLIDAYS ================= */}
                <div id="ess-tab-leaves" style={{ display: activeTab === 'leaves' ? 'block' : 'none' }} className="ess-tab-pane ">
                    {/* 4 Balance Cards */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-start">
                                <div>
                                    <div className="text-[10px] font-bold text-slate-400 uppercase">Earned Leave (EL)</div>
                                    <div id="ess-leave-el" className="text-2xl font-black text-blue-600 mt-1">16.0</div>
                                </div>
                                <span className="text-xs px-2 py-0.5 bg-blue-50 text-blue-700 rounded font-bold">18 Annual</span>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-2">Cumulative Privilege / Annual Leave</div>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-start">
                                <div>
                                    <div className="text-[10px] font-bold text-slate-400 uppercase">Casual & Sick (CL/SL)</div>
                                    <div id="ess-leave-cl" className="text-2xl font-black text-amber-600 mt-1">10.0</div>
                                </div>
                                <span className="text-xs px-2 py-0.5 bg-amber-50 text-amber-700 rounded font-bold">12 Annual</span>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-2">Personal Emergency & Medical Leave</div>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-start">
                                <div>
                                    <div className="text-[10px] font-bold text-slate-400 uppercase">Compensatory Off</div>
                                    <div id="ess-leave-comp" className="text-2xl font-black text-purple-600 mt-1">0.0</div>
                                </div>
                                <span className="text-xs px-2 py-0.5 bg-purple-50 text-purple-700 rounded font-bold">Weekend</span>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-2">Credited against weekend deliveries</div>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-start">
                                <div>
                                    <div className="text-[10px] font-bold text-slate-400 uppercase">Total Available</div>
                                    <div id="ess-leave-total" className="text-2xl font-black text-emerald-600 mt-1">26.0</div>
                                </div>
                                <button onClick={() => {}} className="text-xs px-2 py-0.5 bg-emerald-600 text-white rounded font-bold hover:bg-emerald-700 transition">
                                    + Apply
                                </button>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-2">Ready for planned application</div>
                        </div>
                    </div>

                    {/* Leaves Grid: History & 2026 Karnataka Statutory Holidays */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        {/* Application History */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-list-check text-blue-600"></i> Leave Application History
                                </h3>
                                <button onClick={() => {}} className="text-xs text-blue-600 hover:text-blue-800 font-bold">+ New Leave Request</button>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-xs">
                                    <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                        <tr>
                                            <th className="p-2.5">Leave Type</th>
                                            <th className="p-2.5">Date Span</th>
                                            <th className="p-2.5 text-right">Days</th>
                                            <th className="p-2.5">Reason</th>
                                            <th className="p-2.5">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-ess-leaves-history" className="divide-y divide-slate-100">
                                        {/* Rendered dynamically */}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* 2026 Karnataka Statutory Holidays */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-calendar-days text-emerald-600"></i> Karnataka 2026 Statutory Holidays
                                </h3>
                                <span className="text-[10px] text-slate-400">10 Official Holidays</span>
                            </div>
                            <div className="overflow-x-auto max-h-72">
                                <table className="w-full text-left text-xs">
                                    <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b sticky top-0">
                                        <tr>
                                            <th className="p-2.5">Date</th>
                                            <th className="p-2.5">Day</th>
                                            <th className="p-2.5">Holiday Name</th>
                                            <th className="p-2.5">Type</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-ess-holidays" className="divide-y divide-slate-100">
                                        {/* Rendered dynamically */}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                {/* ================= TAB 5: TRAINING & ACADEMY ================= */}
                <div id="ess-tab-learning" style={{ display: activeTab === 'learning' ? 'block' : 'none' }} className="ess-tab-pane ">
                    {/* Probation Clearance Gate */}
                    <div className="bg-gradient-to-r from-blue-900 to-indigo-900 p-6 rounded-2xl text-white shadow-md mb-6">
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                            <div>
                                <div className="flex items-center gap-2 mb-1">
                                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-400/30">PROBATION STATUTORY GATE</span>
                                    <span id="ess-probation-status-pill" className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">Confirmed Permanent</span>
                                </div>
                                <h3 className="text-xl font-bold">Mandatory Learning & Competency Threshold</h3>
                                <p className="text-xs text-slate-300 mt-1 max-w-xl">Every engineer must complete a minimum of 16.0 hours of role-specific security, architecture, and compliance modules for probation clearance.</p>
                            </div>
                            <div className="text-right">
                                <div className="text-2xl font-black font-mono text-cyan-300" id="ess-learning-progress-label">24.5 / 16.0 Hrs</div>
                                <div className="text-xs text-emerald-400 font-bold mt-0.5"><i className="fa-solid fa-circle-check"></i> Statutory Threshold Cleared</div>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="w-full bg-slate-800/80 rounded-full h-3 mt-4 overflow-hidden border border-white/10">
                            <div id="ess-learning-progress-bar" className="bg-gradient-to-r from-cyan-400 to-blue-500 h-3 rounded-full transition-all duration-500" style={{ width: '100%' }}></div>
                        </div>
                    </div>

                    {/* Enrolled Courses Grid */}
                    <div className="mb-6">
                        <h3 className="font-bold text-slate-800 text-sm mb-3 flex items-center gap-2">
                            <i className="fa-solid fa-graduation-cap text-blue-600"></i> My Enrolled Academy Modules & Progress
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="grid-ess-enrolled-courses">
                            {/* Rendered dynamically */}
                        </div>
                    </div>

                    {/* Verifiable Certificates Table */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <i className="fa-solid fa-award text-amber-500"></i> Verifiable Corporate Training Certificates
                            </h3>
                            <span className="text-xs text-slate-400">Authenticated with CIN U85500KA2026OPC222069</span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-3">Certificate ID</th>
                                        <th className="p-3">Module Name</th>
                                        <th className="p-3 text-center">Quiz Score</th>
                                        <th className="p-3">Completed On</th>
                                        <th className="p-3 text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-ess-certificates" className="divide-y divide-slate-100 font-mono">
                                    {/* Rendered dynamically */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* ================= TAB 6: IT ASSETS, PASSKEYS & HELPDESK ================= */}
                <div id="ess-tab-assets" style={{ display: activeTab === 'assets' ? 'block' : 'none' }} className="ess-tab-pane ">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                        {/* Assigned IT Hardware Assets */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-laptop text-blue-600"></i> Assigned Workstations & Hardware Assets
                                </h3>
                                <span className="text-xs text-slate-400">ZTNA Managed</span>
                            </div>
                            <div className="space-y-3" id="grid-ess-it-assets">
                                {/* Rendered dynamically */}
                            </div>
                        </div>

                        {/* FIDO2 Hardware Passkeys */}
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-key text-emerald-600"></i> Registered FIDO2 Hardware Passkeys
                                </h3>
                                <span className="text-xs text-slate-400">WebAuthn Bound</span>
                            </div>
                            <div className="space-y-3" id="grid-ess-passkeys">
                                {/* Rendered dynamically */}
                            </div>
                        </div>
                    </div>

                    {/* Internal Helpdesk & Support Tickets */}
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex justify-between items-center mb-3">
                            <div>
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-headset text-indigo-600"></i> My Internal Helpdesk Tickets
                                </h3>
                                <p className="text-xs text-slate-500">Track internal requests across IT, HR, Finance, SecOps & PMO.</p>
                            </div>
                            <button onClick={() => {}} className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-lg transition shadow-sm flex items-center gap-1.5">
                                <i className="fa-solid fa-plus"></i> Raise New Ticket
                            </button>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-500 uppercase text-[10px] border-b">
                                    <tr>
                                        <th className="p-2.5">Ticket #</th>
                                        <th className="p-2.5">Department</th>
                                        <th className="p-2.5">Priority</th>
                                        <th className="p-2.5">Subject</th>
                                        <th className="p-2.5">Status</th>
                                        <th className="p-2.5">Target SLA</th>
                                    </tr>
                                </thead>
                                <tbody id="table-ess-tickets" className="divide-y divide-slate-100 font-mono">
                                    {/* Rendered dynamically */}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* ================= MODAL: APPLY LEAVE ================= */}
                <div id="modal-ess-apply-leave" className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
                    <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
                        <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-100">
                            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                                <i className="fa-solid fa-calendar-plus text-indigo-600"></i> Submit Leave Application
                            </h3>
                            <button onClick={() => {}} className="text-slate-400 hover:text-slate-600 text-lg">&times;</button>
                        </div>
                        <form id="form-ess-apply-leave" onSubmit={(e) => e.preventDefault()} className="space-y-4 text-xs">
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Leave Type</label>
                                <select id="ess-leave-input-type" className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none">
                                    <option value="Earned Leave">Earned Leave (EL) &bull; Annual Privilege</option>
                                    <option value="Casual Leave">Casual Leave (CL) &bull; Personal Urgency</option>
                                    <option value="Sick Leave">Sick Leave (SL) &bull; Medical Necessity</option>
                                </select>
                            </div>
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Start Date</label>
                                    <input type="date" id="ess-leave-input-start" required className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
                                </div>
                                <div>
                                    <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">End Date</label>
                                    <input type="date" id="ess-leave-input-end" required className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
                                </div>
                            </div>
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Total Days</label>
                                <input type="number" id="ess-leave-input-days" step="0.5" min="0.5" defaultValue="1.0" required className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
                            </div>
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Reason for Leave</label>
                                <textarea id="ess-leave-input-reason" rows={3} required placeholder="Specify detailed reason for supervisor and director notification..." className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"></textarea>
                            </div>
                            <div className="flex justify-end gap-2 pt-2">
                                <button type="button" onClick={() => {}} className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition">Cancel</button>
                                <button type="submit" className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg shadow transition">Submit Application</button>
                            </div>
                        </form>
                    </div>
                </div>

                {/* ================= MODAL: RAISE TICKET ================= */}
                <div id="modal-ess-raise-ticket" className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
                    <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
                        <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-100">
                            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                                <i className="fa-solid fa-headset text-amber-600"></i> Raise Internal Support Ticket
                            </h3>
                            <button onClick={() => {}} className="text-slate-400 hover:text-slate-600 text-lg">&times;</button>
                        </div>
                        <form id="form-ess-raise-ticket" onSubmit={(e) => e.preventDefault()} className="space-y-4 text-xs">
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Target Department</label>
                                    <select id="ess-tkt-input-dept" className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:outline-none">
                                        <option value="IT_INFRASTRUCTURE">IT & Infrastructure</option>
                                        <option value="HR_PEOPLE">HR & People Operations</option>
                                        <option value="FINANCE_ACCOUNTS">Finance & Accounts</option>
                                        <option value="SECOPS_CYBER">Cybersecurity & SecOps</option>
                                        <option value="ADMIN_WORKPLACE">Workplace & Admin</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Priority SLA</label>
                                    <select id="ess-tkt-input-priority" className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:outline-none">
                                        <option value="P2-High">P2-High (8-Hour Target SLA)</option>
                                        <option value="P3-Medium" selected>P3-Medium (24-Hour Target SLA)</option>
                                        <option value="P4-Low">P4-Low (48-Hour Target SLA)</option>
                                        <option value="P1-Critical">P1-Critical (2-Hour Target SLA)</option>
                                    </select>
                                </div>
                            </div>
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Issue Category</label>
                                <input type="text" id="ess-tkt-input-cat" required defaultValue="Hardware & Peripheral Support" className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:outline-none" />
                            </div>
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Subject</label>
                                <input type="text" id="ess-tkt-input-sub" required placeholder="Brief summary of request or impediment..." className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:outline-none" />
                            </div>
                            <div>
                                <label className="block font-bold text-slate-700 uppercase text-[10px] mb-1">Detailed Description</label>
                                <textarea id="ess-tkt-input-desc" rows={3} required placeholder="Provide context, workstation serial or error message..." className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:outline-none"></textarea>
                            </div>
                            <div className="flex justify-end gap-2 pt-2">
                                <button type="button" onClick={() => {}} className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition">Cancel</button>
                                <button type="submit" className="px-5 py-2 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-lg shadow transition">File Support Ticket</button>
                            </div>
                        </form>
                    </div>
                </div>

                {/* ================= MODAL: DIGITAL ID CARD ================= */}
                <div id="modal-ess-id-card" className="fixed inset-0 bg-slate-900/70 backdrop-blur-sm z-50 flex items-center justify-center hidden">
                    <div className="bg-white rounded-3xl max-w-md w-full overflow-hidden shadow-2xl border border-slate-300 flex flex-col max-h-[90vh]">
                        <div className="flex justify-between items-center p-4 bg-slate-900 text-white">
                            <div className="text-xs font-bold flex items-center gap-2">
                                <i className="fa-solid fa-id-badge text-cyan-400"></i> Corporate Digital Identity Credential
                            </div>
                            <button onClick={() => {}} className="text-slate-400 hover:text-white text-lg">&times;</button>
                        </div>
                        <div className="flex-1 overflow-auto bg-slate-950 p-4 flex justify-center">
                            <iframe id="iframe-ess-id-card" src="about:blank" className="w-full h-[580px] border-0 rounded-2xl"></iframe>
                        </div>
                        <div className="p-3 bg-slate-900 border-t border-slate-800 flex justify-between items-center">
                            <span className="text-[10px] text-slate-400 font-mono">CIN: U85500KA2026OPC222069</span>
                            <div className="flex gap-2">
                                <button onClick={() => {}} className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-lg transition flex items-center gap-1">
                                    <i className="fa-solid fa-print"></i> Print Card
                                </button>
                                <button onClick={() => {}} className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-lg transition">
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* 16. Client Project & SLA Dedicated Portal View */}
    </div>
  );
};

export default EmployeePortalView;
