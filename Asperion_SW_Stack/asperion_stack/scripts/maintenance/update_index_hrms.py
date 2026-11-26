import os

INDEX_PATH = r"asperion_stack/app/static/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Verify markers
start_marker = '<!-- 5. HRMS & CTC Engine View -->'
end_marker = '<!-- 6. PMO & Agile Delivery Operations View -->'

assert start_marker in content, "Could not find start marker"
assert end_marker in content, "Could not find end marker"

hrms_view_html = '''<!-- 5. HRMS & Workforce Governance Portal -->
            <section id="view-hrms" class="module-view hidden">
                <!-- Executive Header -->
                <div class="mb-6 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl">
                    <div class="flex items-center gap-4">
                        <img src="/static/img/logo.png" alt="Asperion Brand" class="w-14 h-14 rounded-2xl border-2 border-cyan-400/40 shadow-lg object-contain bg-slate-950 p-1 flex-shrink-0">
                        <div>
                            <div class="flex flex-wrap items-center gap-2 mb-1.5">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">WAGE CODE 2019 COMPLIANT</span>
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">EPFO & MP ACT 1952</span>
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">KARNATAKA PT ACT (₹200/MO)</span>
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">POSH ACT 2013 REGISTER</span>
                            </div>
                            <h2 class="text-2xl font-black text-white flex items-center gap-2.5">
                                Asperion Enterprise HRMS & Human Capital Suite
                            </h2>
                            <p class="text-xs text-slate-300 mt-0.5">
                                Complete employee lifecycle: ATS talent pipeline, attendance-synchronized payroll, statutory Wage Code salary structures, leaves, multi-department separation clearance & POSH compliance.
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto justify-end">
                        <button onclick="openHRMSModal('modal-hrms-employee')" class="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-user-plus"></i> Add Employee
                        </button>
                        <button onclick="openHRMSModal('modal-hrms-candidate')" class="px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-user-tie"></i> Add Candidate
                        </button>
                        <button onclick="openHRMSModal('modal-hrms-leave')" class="px-3.5 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-calendar-plus"></i> Apply Leave
                        </button>
                        <button onclick="handleRunAttendancePayroll(false)" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-calculator"></i> Run Payroll
                        </button>
                        <a href="/api/v1/hrms/salary-statement/bank-neft-file?cycle=JUN-2026" target="_blank" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white font-bold text-xs rounded-lg transition border border-slate-700 shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-file-csv text-emerald-400"></i> ICICI NEFT
                        </a>
                    </div>
                </div>

                <!-- 6 Executive KPI Stat Cards -->
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5 mb-6">
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">Active Headcount</span>
                            <i class="fa-solid fa-users text-blue-500"></i>
                        </div>
                        <div id="hrms-stat-headcount" class="text-xl font-black text-slate-900 mt-1">--</div>
                        <div class="text-[10px] text-emerald-600 font-semibold mt-0.5">100% On-Roster Active</div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">Monthly Gross Outflow</span>
                            <i class="fa-solid fa-money-bill-wave text-emerald-500"></i>
                        </div>
                        <div id="hrms-stat-payroll-gross" class="text-xl font-black text-slate-900 mt-1">₹--</div>
                        <div class="text-[10px] text-slate-500 mt-0.5">Earned Gross Disbursed</div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">Annual Payroll CTC</span>
                            <i class="fa-solid fa-chart-line text-indigo-500"></i>
                        </div>
                        <div id="hrms-stat-payroll-annual" class="text-xl font-black text-slate-900 mt-1">₹--</div>
                        <div class="text-[10px] text-slate-500 mt-0.5">Annualized Fixed CTC</div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">PF & PT Outflow</span>
                            <i class="fa-solid fa-landmark text-purple-500"></i>
                        </div>
                        <div id="hrms-stat-statutory-outflow" class="text-xl font-black text-purple-700 mt-1">₹--</div>
                        <div class="text-[10px] text-purple-600 font-semibold mt-0.5">EPFO + Karnataka PT</div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">Talent Pipeline</span>
                            <i class="fa-solid fa-user-clock text-cyan-500"></i>
                        </div>
                        <div id="hrms-stat-candidates" class="text-xl font-black text-slate-900 mt-1">--</div>
                        <div class="text-[10px] text-cyan-600 font-semibold mt-0.5">Active ATS Candidates</div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex items-center justify-between text-slate-400 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider">POSH & Ethics Index</span>
                            <i class="fa-solid fa-shield-halved text-rose-500"></i>
                        </div>
                        <div id="hrms-stat-posh-compliance" class="text-xl font-black text-rose-600 mt-1">100%</div>
                        <div class="text-[10px] text-emerald-600 font-semibold mt-0.5">90-Day ICC SLA OK</div>
                    </div>
                </div>

                <!-- 8-Tab Pill Navigation Container -->
                <div class="bg-white p-2 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <div class="flex flex-wrap items-center gap-1.5" id="hrms-tab-buttons">
                        <button onclick="switchHRMSTab('employees')" id="hrms-btn-employees" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-blue-600 text-white shadow-sm">
                            <i class="fa-solid fa-id-card"></i> 1. Employees Directory
                        </button>
                        <button onclick="switchHRMSTab('candidates')" id="hrms-btn-candidates" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-user-tie"></i> 2. Recruitment & ATS
                        </button>
                        <button onclick="switchHRMSTab('payroll')" id="hrms-btn-payroll" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-file-invoice-dollar"></i> 3. Payroll & Payslips
                        </button>
                        <button onclick="switchHRMSTab('ctc')" id="hrms-btn-ctc" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-calculator"></i> 4. Wage Code CTC Engine
                        </button>
                        <button onclick="switchHRMSTab('leaves')" id="hrms-btn-leaves" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-calendar-check"></i> 5. Leaves & Balances
                        </button>
                        <button onclick="switchHRMSTab('attendance')" id="hrms-btn-attendance" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-fingerprint"></i> 6. Smart Attendance & Kiosk
                        </button>
                        <button onclick="switchHRMSTab('separation')" id="hrms-btn-separation" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-door-open"></i> 7. Separation & F&F Exit
                        </button>
                        <button onclick="switchHRMSTab('posh')" id="hrms-btn-posh" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-scale-balanced"></i> 8. Workplace Ethics & POSH
                        </button>
                        <button onclick="switchHRMSTab('letters')" id="hrms-btn-letters" class="hrms-tab-pill px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700">
                            <i class="fa-solid fa-envelopes-bulk"></i> 9. Master 70+ Letters Vault
                        </button>
                    </div>
                </div>

                <!-- SUB-VIEW 1: EMPLOYEES DIRECTORY -->
                <div id="hrms-subview-employees" class="hrms-tab-content">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-id-badge text-blue-600"></i> Active Employee Directory & Statutory Records
                                </h3>
                                <p class="text-xs text-slate-500">Corporate roster, statutory PAN/UAN/Bank linkages, Wage Code compensation, and 360° employee dossier.</p>
                            </div>
                            <div class="flex items-center gap-2 w-full sm:w-auto">
                                <input id="hrms-search-employees" oninput="filterHRMSEmployees(this.value)" type="text" placeholder="Search by name, code, dept..." class="px-3 py-1.5 border border-slate-200 rounded-lg text-xs w-full sm:w-60 focus:outline-none focus:ring-1 focus:ring-blue-500">
                                <button onclick="openHRMSModal('modal-hrms-employee')" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold whitespace-nowrap">
                                    <i class="fa-solid fa-plus mr-1"></i> Add Employee
                                </button>
                            </div>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Emp Code</th>
                                        <th class="p-3">Employee Name</th>
                                        <th class="p-3">Designation</th>
                                        <th class="p-3">Department</th>
                                        <th class="p-3">Date of Joining</th>
                                        <th class="p-3">Statutory CTC</th>
                                        <th class="p-3">PAN & UAN</th>
                                        <th class="p-3">Status</th>
                                        <th class="p-3 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-employees" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 2: CANDIDATES & ATS RECRUITMENT -->
                <div id="hrms-subview-candidates" class="hrms-tab-content hidden">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-user-tie text-cyan-600"></i> Talent Acquisition & ATS Candidate Pipeline
                                </h3>
                                <p class="text-xs text-slate-500">End-to-end recruitment lifecycle from Application to Offer Letter generation & One-Click Onboarding.</p>
                            </div>
                            <div class="flex items-center gap-2">
                                <button onclick="openHRMSModal('modal-hrms-candidate')" class="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-xs font-semibold">
                                    <i class="fa-solid fa-plus mr-1"></i> Add Candidate
                                </button>
                            </div>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Candidate</th>
                                        <th class="p-3">Target Role</th>
                                        <th class="p-3">Experience</th>
                                        <th class="p-3">Expected CTC</th>
                                        <th class="p-3">Notice Period</th>
                                        <th class="p-3">Stage</th>
                                        <th class="p-3 text-center">Stage Progression</th>
                                        <th class="p-3 text-center">One-Click Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-hrms-candidates" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 3: PAYROLL & STATUTORY STATEMENTS -->
                <div id="hrms-subview-payroll" class="hrms-tab-content hidden">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-4">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-file-invoice-dollar text-emerald-600"></i> Monthly Attendance-Synced Salary Statements & Statutory Ledger
                                </h3>
                                <p class="text-xs text-slate-500 mt-0.5">Calculated based on actual Smart Attendance payable days, Karnataka PT (₹200), and EPFO 12% PF.</p>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="text-xs text-slate-500 font-semibold">Cycle:</span>
                                <span class="text-xs font-mono font-bold bg-blue-50 text-blue-700 px-2.5 py-1 rounded border border-blue-200">JUN-2026</span>
                                <button onclick="handleRunAttendancePayroll(false)" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg transition shadow">
                                    <i class="fa-solid fa-calculator mr-1"></i> Recalculate
                                </button>
                                <button onclick="handleRunAttendancePayroll(true)" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition shadow">
                                    <i class="fa-solid fa-building-columns mr-1"></i> Disburse Bank
                                </button>
                            </div>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Emp Code</th>
                                        <th class="p-3">Employee Name</th>
                                        <th class="p-3">Designation</th>
                                        <th class="p-3 text-right">Payable / LOP</th>
                                        <th class="p-3 text-right">Earned Gross</th>
                                        <th class="p-3 text-right">PF (12%)</th>
                                        <th class="p-3 text-right">Karnataka PT</th>
                                        <th class="p-3 text-right">TDS Tax</th>
                                        <th class="p-3 text-right font-bold text-slate-900">Net Take-Home</th>
                                        <th class="p-3">Bank UTR / Payout</th>
                                        <th class="p-3 text-center">Payslip</th>
                                    </tr>
                                </thead>
                                <tbody id="table-salary-statements" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 4: WAGE CODE CTC ENGINE -->
                <div id="hrms-subview-ctc" class="hrms-tab-content hidden">
                    <div class="bg-gradient-to-r from-blue-950 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl mb-6 border border-slate-800">
                        <div class="flex items-center justify-between mb-4 pb-3 border-b border-blue-800/60">
                            <div>
                                <h3 class="text-lg font-bold flex items-center gap-2">
                                    <i class="fa-solid fa-calculator text-cyan-400"></i> Interactive Statutory CTC & Wage Code 2019 Breakup Engine
                                </h3>
                                <p class="text-xs text-blue-200 mt-0.5">Complies with the 50% Basic Salary threshold under Indian Wage Code 2019, EPFO ceiling & Karnataka PT Slabs.</p>
                            </div>
                            <span class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-400/20 text-cyan-300 border border-cyan-400/40">STATUTORY V2.0</span>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                            <div>
                                <label class="block text-xs uppercase tracking-wider text-blue-200 mb-1">Annual Fixed CTC (INR)</label>
                                <input id="calc-ctc-input" type="number" value="1200000" class="w-full px-3 py-2 rounded bg-blue-950 border border-blue-700 text-white font-bold focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm">
                            </div>
                            <div>
                                <label class="block text-xs uppercase tracking-wider text-blue-200 mb-1">Basic % of CTC</label>
                                <select id="calc-basic-pct" class="w-full px-3 py-2 rounded bg-blue-950 border border-blue-700 text-white focus:outline-none text-sm">
                                    <option value="0.50" selected>50% (Recommended for Wage Code)</option>
                                    <option value="0.40">40% (Standard Minimum)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs uppercase tracking-wider text-blue-200 mb-1">HRA % of Basic</label>
                                <select id="calc-hra-pct" class="w-full px-3 py-2 rounded bg-blue-950 border border-blue-700 text-white focus:outline-none text-sm">
                                    <option value="0.50" selected>50% (Metro / Bangalore)</option>
                                    <option value="0.40">40% (Non-Metro)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs uppercase tracking-wider text-blue-200 mb-1">State / PT Slabs</label>
                                <select id="calc-state" class="w-full px-3 py-2 rounded bg-blue-950 border border-blue-700 text-white focus:outline-none text-sm">
                                    <option value="Karnataka" selected>Karnataka (₹200/mo)</option>
                                    <option value="Maharashtra">Maharashtra (₹200/₹300)</option>
                                </select>
                            </div>
                        </div>
                        <button onclick="calculateLiveCTC()" class="px-5 py-2.5 bg-blue-500 hover:bg-blue-400 text-white font-bold text-sm rounded-lg transition shadow flex items-center gap-2">
                            <i class="fa-solid fa-arrows-rotate"></i> Compute Statutory Breakup
                        </button>

                        <!-- Computed Breakdown Card -->
                        <div class="mt-6 bg-white text-slate-800 p-5 rounded-xl shadow-lg">
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm border-b pb-4 mb-4">
                                <div>
                                    <span class="text-xs text-slate-400 font-semibold">Monthly Gross Salary:</span>
                                    <div id="res-gross-monthly" class="text-xl font-black text-slate-900">-</div>
                                </div>
                                <div>
                                    <span class="text-xs text-slate-400 font-semibold">Annual Gross Salary:</span>
                                    <div id="res-gross-annual" class="text-xl font-black text-slate-900">-</div>
                                </div>
                                <div>
                                    <span class="text-xs text-slate-400 font-semibold">Estimated Monthly Take-Home:</span>
                                    <div id="res-net-monthly" class="text-xl font-black text-emerald-600">-</div>
                                </div>
                                <div>
                                    <span class="text-xs text-slate-400 font-semibold">Annual Net Take-Home:</span>
                                    <div id="res-net-annual" class="text-xl font-black text-emerald-600">-</div>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs text-slate-600">
                                <div>Basic (Monthly): <strong id="res-basic-monthly" class="text-slate-900 font-mono">-</strong></div>
                                <div>HRA (Monthly): <strong id="res-hra-monthly" class="text-slate-900 font-mono">-</strong></div>
                                <div>Special Allowance: <strong id="res-special-monthly" class="text-slate-900 font-mono">-</strong></div>
                                <div>Employer PF (12%): <strong id="res-emp-pf-monthly" class="text-indigo-700 font-mono">-</strong></div>
                                <div>Gratuity Accrual (4.81%): <strong id="res-gratuity-monthly" class="text-slate-900 font-mono">-</strong></div>
                                <div>Employee PF (12%): <strong id="res-ded-pf-monthly" class="text-rose-700 font-mono">-</strong></div>
                                <div>Karnataka PT: <strong id="res-ded-pt-monthly" class="text-purple-700 font-mono font-bold">-</strong></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 5: LEAVES & BALANCES -->
                <div id="hrms-subview-leaves" class="hrms-tab-content hidden">
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-3.5 mb-6">
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Casual Leave (CL)</span>
                            <div class="text-lg font-black text-slate-900 mt-1">12 Days / Year</div>
                            <div class="text-[10px] text-slate-500">1 day credited monthly</div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Sick / Medical Leave (SL)</span>
                            <div class="text-lg font-black text-slate-900 mt-1">12 Days / Year</div>
                            <div class="text-[10px] text-slate-500">Self-certified or Medical Cert</div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Earned / Privilege Leave (EL)</span>
                            <div class="text-lg font-black text-slate-900 mt-1">15 Days / Year</div>
                            <div class="text-[10px] text-slate-500">Encashable on Separation</div>
                        </div>
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Maternity Benefit Act</span>
                            <div class="text-lg font-black text-purple-700 mt-1">26 Weeks Paid</div>
                            <div class="text-[10px] text-purple-600">Statutory 182 calendar days</div>
                        </div>
                    </div>

                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-plane-departure text-amber-600"></i> Leave Requests & Approval Workflow
                                </h3>
                                <p class="text-xs text-slate-500">Real-time leave balance tracking, manager approvals and payroll deduction sync.</p>
                            </div>
                            <button onclick="openHRMSModal('modal-hrms-leave')" class="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold">
                                <i class="fa-solid fa-plus mr-1"></i> Apply Leave
                            </button>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Employee</th>
                                        <th class="p-3">Leave Type</th>
                                        <th class="p-3">Duration</th>
                                        <th class="p-3">Dates</th>
                                        <th class="p-3">Reason</th>
                                        <th class="p-3">Status</th>
                                        <th class="p-3 text-center">Manager Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-leaves" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 6: SMART ATTENDANCE & BIOMETRIC KIOSK -->
                <div id="hrms-subview-attendance" class="hrms-tab-content hidden">
                    <div class="bg-gradient-to-r from-slate-900 to-indigo-950 text-white p-6 rounded-2xl shadow-xl mb-6 border border-slate-800">
                        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 pb-4 border-b border-slate-800">
                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">AI BIOMETRICS & IOT</span>
                                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">META WHATSAPP CLOUD API</span>
                                    <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">HAVERSINE GEOFENCING</span>
                                </div>
                                <h3 class="text-xl font-bold mt-2 flex items-center gap-2.5">
                                    <i class="fa-solid fa-fingerprint text-emerald-400"></i> Smart Attendance & Workforce Mobility Engine
                                </h3>
                                <p class="text-xs text-slate-300 mt-1">
                                    Geofence Location Verification (Horamavu Bangalore HQ: 13.035820, 77.653410), 3D Facial Liveness Matching, WhatsApp Bot Check-In, and Self-Healing Anomaly Auto-Fixing.
                                </p>
                            </div>
                            <div class="flex items-center gap-3">
                                <button onclick="handleTriggerAutoFixAttendance()" class="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition shadow-md flex items-center gap-2">
                                    <i class="fa-solid fa-wand-magic-sparkles"></i> Run Self-Healing Auto-Fix
                                </button>
                                <button onclick="openWhatsAppModal()" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition shadow-md flex items-center gap-2">
                                    <i class="fa-brands fa-whatsapp text-sm"></i> WhatsApp Bot Simulator
                                </button>
                            </div>
                        </div>

                        <!-- Attendance Real-Time KPI Cards -->
                        <div class="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6 text-center">
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Total Headcount</div>
                                <div id="att-stat-headcount" class="text-lg font-bold text-white mt-0.5">--</div>
                                <div class="text-[9px] text-slate-400">Active Roster</div>
                            </div>
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Present Today</div>
                                <div id="att-stat-present" class="text-lg font-bold text-emerald-400 mt-0.5">--</div>
                                <div class="text-[9px] text-emerald-400/80">In-Office + WFH</div>
                            </div>
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Biometric Match</div>
                                <div id="att-stat-biometric" class="text-lg font-bold text-cyan-400 mt-0.5">--%</div>
                                <div class="text-[9px] text-cyan-400/80">Face Liveness Rate</div>
                            </div>
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Late Marks (>9:30)</div>
                                <div id="att-stat-late" class="text-lg font-bold text-amber-400 mt-0.5">--</div>
                                <div class="text-[9px] text-amber-400/80">Grace Period Passed</div>
                            </div>
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Remote / WFH</div>
                                <div id="att-stat-wfh" class="text-lg font-bold text-purple-400 mt-0.5">--</div>
                                <div class="text-[9px] text-purple-400/80">Outside Geofence</div>
                            </div>
                            <div class="bg-slate-800/70 p-3 rounded-xl border border-slate-700/60">
                                <div class="text-[10px] text-slate-400 uppercase font-bold">Auto-Healed</div>
                                <div id="att-stat-healed" class="text-lg font-bold text-blue-400 mt-0.5">--</div>
                                <div class="text-[9px] text-blue-400/80">Missing Punches Fixed</div>
                            </div>
                        </div>

                        <!-- Clock In/Out Live Biometric Terminal -->
                        <div class="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50 mb-6">
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                                    <i class="fa-solid fa-camera-viewfinder text-blue-400"></i> Live Biometric Facial Kiosk & Geofence Punch Terminal
                                </span>
                                <span id="geo-live-indicator" class="text-[11px] font-mono text-emerald-400 flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> GPS Geofence Locked: Horamavu Bangalore HQ (0.8m)
                                </span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 items-center">
                                <div>
                                    <label class="block text-[10px] text-slate-400 uppercase font-semibold mb-1">Select Employee</label>
                                    <select id="att-employee-select" class="w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-blue-500"></select>
                                </div>
                                <div>
                                    <label class="block text-[10px] text-slate-400 uppercase font-semibold mb-1">Authentication Mode</label>
                                    <select id="att-source-select" class="w-full bg-slate-900 border border-slate-700 text-white rounded-lg px-3 py-2 text-xs focus:outline-none">
                                        <option value="FACIAL_KIOSK">Biometric Facial Recognition (AI Liveness)</option>
                                        <option value="WHATSAPP">WhatsApp Cloud API Check-In</option>
                                        <option value="WEB">Enterprise Web Portal</option>
                                        <option value="MOBILE_APP">Mobile GPS Geotagged App</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-[10px] text-slate-400 uppercase font-semibold mb-1">Biometric Selfie Camera</label>
                                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-300">
                                        <i class="fa-solid fa-circle-user text-emerald-400 text-sm"></i>
                                        <span class="truncate">Live Feed Active (3D Pose Ok)</span>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 pt-4">
                                    <button onclick="handleClockIn()" class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center justify-center gap-1.5">
                                        <i class="fa-solid fa-right-to-bracket"></i> CLOCK IN
                                    </button>
                                    <button onclick="handleClockOut()" class="flex-1 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center justify-center gap-1.5">
                                        <i class="fa-solid fa-right-from-bracket"></i> CLOCK OUT
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Attendance Daily Logs Table -->
                        <div class="bg-slate-900/80 rounded-xl border border-slate-800 overflow-hidden">
                            <div class="p-3.5 bg-slate-800/60 border-b border-slate-800 flex justify-between items-center">
                                <span class="text-xs font-bold text-slate-300 flex items-center gap-2">
                                    <i class="fa-solid fa-clock-rotate-left text-purple-400"></i> Real-Time Multi-Modal Attendance Ledger
                                </span>
                                <span class="text-[11px] text-slate-400 font-mono">Auto-Calculated Hours, Late Deductions & Self-Healing Audit</span>
                            </div>
                            <div class="overflow-x-auto">
                                <table class="w-full text-left text-xs">
                                    <thead class="bg-slate-800/90 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                                        <tr>
                                            <th class="p-3">Emp ID</th>
                                            <th class="p-3">Employee Name</th>
                                            <th class="p-3">Date</th>
                                            <th class="p-3">Clock In</th>
                                            <th class="p-3">Clock Out</th>
                                            <th class="p-3 text-right">Total Hours</th>
                                            <th class="p-3 text-right">Effective Hours</th>
                                            <th class="p-3">Status</th>
                                            <th class="p-3">Geofence Status</th>
                                            <th class="p-3">Biometric Face %</th>
                                            <th class="p-3">Channel</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-attendance-records" class="divide-y divide-slate-800 text-slate-300"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 7: SEPARATION & F&F CLEARANCE -->
                <div id="hrms-subview-separation" class="hrms-tab-content hidden">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-door-open text-rose-600"></i> Employee Resignation, Multi-Dept Clearance & Full & Final (F&F) Settlement
                                </h3>
                                <p class="text-xs text-slate-500">Statutory F&F timeline, IT asset recovery, Finance no-dues, Gratuity/EL encashment & Relieving Letters.</p>
                            </div>
                            <button onclick="openHRMSModal('modal-hrms-separation')" class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold">
                                <i class="fa-solid fa-user-xmark mr-1"></i> Initiate Exit
                            </button>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Employee</th>
                                        <th class="p-3">Resignation Date</th>
                                        <th class="p-3">Last Working Day</th>
                                        <th class="p-3">IT Assets Clearance</th>
                                        <th class="p-3">Finance Clearance</th>
                                        <th class="p-3">Knowledge Transfer</th>
                                        <th class="p-3 text-right">F&F Settlement INR</th>
                                        <th class="p-3">Status</th>
                                        <th class="p-3 text-center">Settlement Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-hrms-separations" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 8: WORKPLACE ETHICS & POSH REGISTER -->
                <div id="hrms-subview-posh" class="hrms-tab-content hidden">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4 pb-3 border-b border-slate-100">
                            <div>
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-200">STATUTORY POSH ACT 2013</span>
                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800 border border-slate-200">90-DAY INQUIRY MANDATE</span>
                                </div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-scale-balanced text-rose-600"></i> Internal Complaints Committee (ICC) & POSH Register
                                </h3>
                                <p class="text-xs text-slate-500">Confidential workplace harassment grievances register, statutory inquiry committee timeline, and compliance records.</p>
                            </div>
                            <button onclick="openHRMSModal('modal-hrms-posh')" class="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold">
                                <i class="fa-solid fa-file-shield mr-1"></i> Lodge Grievance
                            </button>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Case ID</th>
                                        <th class="p-3">Complainant</th>
                                        <th class="p-3">Accused</th>
                                        <th class="p-3">Incident Date</th>
                                        <th class="p-3">Statutory 90-Day SLA</th>
                                        <th class="p-3">Presiding Officer</th>
                                        <th class="p-3">Status</th>
                                        <th class="p-3 text-center">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-hrms-posh" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- SUB-VIEW 9: MASTER 70+ HR & LEGAL LETTERS VAULT -->
                <div id="hrms-subview-letters" class="hrms-tab-content hidden">
                    <!-- Letter Generation Form -->
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                            <div>
                                <h3 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    <i class="fa-solid fa-file-circle-plus text-purple-600"></i> Instant Official Letter Generator (70+ Templates)
                                </h3>
                                <p class="text-xs text-slate-500">Generates branded HTML and .docx documents with official Asperion corporate letterhead and registered seal.</p>
                            </div>
                            <img src="/static/img/logo.png" alt="Asperion Seal" class="w-10 h-10 object-contain rounded-lg p-0.5 bg-slate-900">
                        </div>
                        <form onsubmit="handleGenerateLetter(event)" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div class="md:col-span-2">
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Letter Template (Select from 70+ Templates)</label>
                                <select id="gen-letter-code" class="w-full px-3 py-2 border rounded-lg text-xs bg-white font-medium text-slate-700"></select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Recipient Full Name</label>
                                <input id="gen-recipient-name" type="text" required placeholder="Full Name" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Designation</label>
                                <input id="gen-designation" type="text" value="Senior Software Engineer" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Annual CTC (INR)</label>
                                <input id="gen-ctc" type="number" value="1200000" class="w-full px-3 py-2 border rounded-lg text-xs">
                            </div>
                            <div class="md:col-span-3 flex items-end justify-end">
                                <button type="submit" class="px-5 py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-medium text-xs rounded-lg transition shadow flex items-center gap-1.5">
                                    <i class="fa-solid fa-file-export"></i> Generate Official Document (.DOCX + HTML)
                                </button>
                            </div>
                        </form>
                    </div>

                    <!-- Issued Letters History Table -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2">
                            <i class="fa-solid fa-envelopes-bulk text-purple-600"></i> Issued HR & Legal Letters Ledger
                        </h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead class="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                                    <tr>
                                        <th class="p-3">Letter Code</th>
                                        <th class="p-3">Title</th>
                                        <th class="p-3">Category</th>
                                        <th class="p-3">Recipient</th>
                                        <th class="p-3">Date</th>
                                        <th class="p-3 text-center">Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-letters" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>
'''

# Replace section
idx_start = content.find(start_marker)
idx_end = content.find(end_marker)
new_content = content[:idx_start] + hrms_view_html + '\n\n\n\n            ' + content[idx_end:]

# Now add the 6 modals right before `<!-- Enterprise Toast Notification Container -->`
toast_marker = '<!-- Enterprise Toast Notification Container -->'
assert toast_marker in new_content, "Could not find toast marker"

modals_html = '''<!-- ============================================================== -->
            <!-- HRMS MODALS: EMPLOYEE, CANDIDATE, LEAVE, SEPARATION, POSH, PROFILE -->
            <!-- ============================================================== -->

            <!-- 1. Add Employee Modal -->
            <div id="modal-hrms-employee" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-2xl w-full overflow-hidden">
                    <div class="p-4 bg-gradient-to-r from-blue-900 to-indigo-900 text-white flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <img src="/static/img/logo.png" alt="Asperion" class="w-8 h-8 rounded-lg object-contain bg-slate-950 p-0.5">
                            <div>
                                <h3 class="font-bold text-sm">Add New Employee</h3>
                                <p class="text-[11px] text-blue-200">Statutory Roster, Wage Code & Bank Profile</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-employee')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onsubmit="handleCreateEmployee(event)" class="p-5 max-h-[75vh] overflow-y-auto space-y-3 text-xs">
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Employee Code *</label>
                                <input id="new-emp-code" type="text" required placeholder="e.g. ADT-EMP-005" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Full Legal Name *</label>
                                <input id="new-emp-name" type="text" required placeholder="Firstname Lastname" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Official Email *</label>
                                <input id="new-emp-email" type="email" required placeholder="name@asperion.in" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Phone Number</label>
                                <input id="new-emp-phone" type="text" placeholder="+91 98765 43210" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Designation *</label>
                                <input id="new-emp-designation" type="text" required placeholder="e.g. Full Stack Engineer" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Department</label>
                                <select id="new-emp-dept" class="w-full px-3 py-2 border rounded-lg bg-white">
                                    <option value="Engineering">Engineering</option>
                                    <option value="Product">Product</option>
                                    <option value="Operations">Operations</option>
                                    <option value="Finance & Accounts">Finance & Accounts</option>
                                    <option value="Security & Compliance">Security & Compliance</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Date of Joining</label>
                                <input id="new-emp-doj" type="date" value="2026-06-01" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Annual Fixed CTC (INR) *</label>
                                <input id="new-emp-ctc" type="number" required value="1200000" class="w-full px-3 py-2 border rounded-lg font-bold">
                            </div>
                        </div>
                        <div class="border-t pt-3">
                            <span class="font-bold text-slate-800 text-[11px] uppercase tracking-wider block mb-2">Statutory Identifiers & Banking</span>
                            <div class="grid grid-cols-2 gap-3">
                                <div>
                                    <label class="block font-semibold text-slate-700 mb-1">PAN Card Number</label>
                                    <input id="new-emp-pan" type="text" placeholder="ABCDE1234F" class="w-full px-3 py-2 border rounded-lg uppercase">
                                </div>
                                <div>
                                    <label class="block font-semibold text-slate-700 mb-1">EPFO UAN Number</label>
                                    <input id="new-emp-uan" type="text" placeholder="101234567890" class="w-full px-3 py-2 border rounded-lg">
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-3 mt-3">
                                <div>
                                    <label class="block font-semibold text-slate-700 mb-1">Bank Account Number</label>
                                    <input id="new-emp-bank-acc" type="text" placeholder="ICICI / HDFC Account" class="w-full px-3 py-2 border rounded-lg">
                                </div>
                                <div>
                                    <label class="block font-semibold text-slate-700 mb-1">Bank IFSC Code</label>
                                    <input id="new-emp-bank-ifsc" type="text" placeholder="ICIC0000001" class="w-full px-3 py-2 border rounded-lg uppercase">
                                </div>
                            </div>
                        </div>
                        <div class="flex justify-end gap-2 pt-3 border-t">
                            <button type="button" onclick="closeHRMSModal('modal-hrms-employee')" class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
                            <button type="submit" class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition shadow">Save Employee</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- 2. Add Candidate Modal -->
            <div id="modal-hrms-candidate" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden">
                    <div class="p-4 bg-gradient-to-r from-cyan-900 to-blue-900 text-white flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <i class="fa-solid fa-user-tie text-cyan-300"></i>
                            <div>
                                <h3 class="font-bold text-sm">Add ATS Candidate</h3>
                                <p class="text-[11px] text-cyan-200">Talent Acquisition & Stage Pipeline</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-candidate')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onsubmit="handleCreateCandidate(event)" class="p-5 space-y-3 text-xs">
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Full Name *</label>
                                <input id="cand-name" type="text" required placeholder="Candidate Name" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Email Address *</label>
                                <input id="cand-email" type="email" required placeholder="candidate@example.com" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Target Role *</label>
                                <input id="cand-role" type="text" required placeholder="e.g. Lead Architect" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Department</label>
                                <select id="cand-dept" class="w-full px-3 py-2 border rounded-lg bg-white">
                                    <option value="Engineering">Engineering</option>
                                    <option value="Product">Product</option>
                                    <option value="Operations">Operations</option>
                                    <option value="Finance & Accounts">Finance & Accounts</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Total Experience (Years)</label>
                                <input id="cand-exp" type="number" step="0.5" value="4.0" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Expected CTC (INR)</label>
                                <input id="cand-ctc" type="number" value="1800000" class="w-full px-3 py-2 border rounded-lg font-bold">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Notice Period (Days)</label>
                                <input id="cand-notice" type="number" value="30" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Current Company</label>
                                <input id="cand-company" type="text" placeholder="Current Employer" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="flex justify-end gap-2 pt-3 border-t">
                            <button type="button" onclick="closeHRMSModal('modal-hrms-candidate')" class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
                            <button type="submit" class="px-5 py-2 bg-cyan-600 hover:bg-cyan-700 text-white font-bold rounded-lg transition shadow">Add to Pipeline</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- 3. Apply Leave Modal -->
            <div id="modal-hrms-leave" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-md w-full overflow-hidden">
                    <div class="p-4 bg-gradient-to-r from-amber-700 to-amber-900 text-white flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <i class="fa-solid fa-calendar-plus text-amber-200"></i>
                            <div>
                                <h3 class="font-bold text-sm">Apply for Leave</h3>
                                <p class="text-[11px] text-amber-200">Time-off request and manager approval</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-leave')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onsubmit="handleApplyLeave(event)" class="p-5 space-y-3 text-xs">
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Employee *</label>
                            <select id="leave-emp-id" required class="w-full px-3 py-2 border rounded-lg bg-white"></select>
                        </div>
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Leave Type *</label>
                            <select id="leave-type" class="w-full px-3 py-2 border rounded-lg bg-white">
                                <option value="Casual Leave">Casual Leave (CL)</option>
                                <option value="Sick Leave">Sick / Medical Leave (SL)</option>
                                <option value="Earned Leave">Earned / Privilege Leave (EL)</option>
                                <option value="Maternity Leave">Maternity Leave (26 Weeks Paid)</option>
                                <option value="Paternity Leave">Paternity Leave</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Start Date *</label>
                                <input id="leave-start-date" type="date" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">End Date *</label>
                                <input id="leave-end-date" type="date" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Reason for Leave *</label>
                            <textarea id="leave-reason" rows="2" required placeholder="Specify reason..." class="w-full px-3 py-2 border rounded-lg"></textarea>
                        </div>
                        <div class="flex justify-end gap-2 pt-3 border-t">
                            <button type="button" onclick="closeHRMSModal('modal-hrms-leave')" class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
                            <button type="submit" class="px-5 py-2 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-lg transition shadow">Submit Request</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- 4. Initiate Separation Modal -->
            <div id="modal-hrms-separation" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-md w-full overflow-hidden">
                    <div class="p-4 bg-gradient-to-r from-rose-900 to-slate-900 text-white flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <i class="fa-solid fa-door-open text-rose-300"></i>
                            <div>
                                <h3 class="font-bold text-sm">Initiate Employee Separation</h3>
                                <p class="text-[11px] text-rose-200">Resignation & Exit Clearance Workflow</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-separation')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onsubmit="handleInitiateSeparation(event)" class="p-5 space-y-3 text-xs">
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Select Employee *</label>
                            <select id="sep-emp-id" required class="w-full px-3 py-2 border rounded-lg bg-white"></select>
                        </div>
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Separation Type</label>
                            <select id="sep-type" class="w-full px-3 py-2 border rounded-lg bg-white">
                                <option value="Resignation">Voluntary Resignation</option>
                                <option value="Mutual Separation">Mutual Separation Agreement</option>
                                <option value="End of Contract">Contract Expiration</option>
                                <option value="Retirement">Retirement</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Resignation Date *</label>
                                <input id="sep-resig-date" type="date" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Last Working Day *</label>
                                <input id="sep-lwd-date" type="date" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Reason for Leaving</label>
                            <textarea id="sep-reason" rows="2" placeholder="e.g. Higher studies, career growth..." class="w-full px-3 py-2 border rounded-lg"></textarea>
                        </div>
                        <div class="flex justify-end gap-2 pt-3 border-t">
                            <button type="button" onclick="closeHRMSModal('modal-hrms-separation')" class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
                            <button type="submit" class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-lg transition shadow">Initiate Separation</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- 5. Lodge POSH Grievance Modal -->
            <div id="modal-hrms-posh" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full overflow-hidden">
                    <div class="p-4 bg-gradient-to-r from-rose-950 via-slate-900 to-indigo-950 text-white flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <i class="fa-solid fa-scale-balanced text-rose-400"></i>
                            <div>
                                <h3 class="font-bold text-sm">Lodge POSH & Ethics Grievance</h3>
                                <p class="text-[11px] text-rose-200">Strictly Confidential Statutory ICC Register</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-posh')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <form onsubmit="handleCreatePOSHCase(event)" class="p-5 space-y-3 text-xs">
                        <div class="p-2.5 bg-rose-50 border border-rose-200 rounded-lg text-rose-800 text-[11px]">
                            <i class="fa-solid fa-shield-halved mr-1 text-rose-600"></i>
                            <strong>Statutory Mandate:</strong> As per Sexual Harassment of Women at Workplace Act 2013, the Internal Committee conducts confidential inquiry completed within 90 days.
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Complainant Name *</label>
                                <input id="posh-complainant" type="text" required placeholder="Name (kept confidential)" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Accused Person Name *</label>
                                <input id="posh-accused" type="text" required placeholder="Accused Name" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Incident Date *</label>
                                <input id="posh-date" type="date" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block font-semibold text-slate-700 mb-1">Location / Channel</label>
                                <input id="posh-loc" type="text" placeholder="Horamavu Office / Virtual Meet" class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div>
                            <label class="block font-semibold text-slate-700 mb-1">Detailed Description of Incident *</label>
                            <textarea id="posh-desc" rows="3" required placeholder="Detailed factual description..." class="w-full px-3 py-2 border rounded-lg"></textarea>
                        </div>
                        <div class="flex justify-end gap-2 pt-3 border-t">
                            <button type="button" onclick="closeHRMSModal('modal-hrms-posh')" class="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg">Cancel</button>
                            <button type="submit" class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-lg transition shadow">Lodge Confidentially</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- 6. 360-Degree Employee Profile Modal -->
            <div id="modal-hrms-profile" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
                <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-2xl w-full overflow-hidden">
                    <div class="p-4 bg-slate-900 text-white flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <img src="/static/img/logo.png" alt="Asperion" class="w-10 h-10 rounded-xl object-contain bg-slate-950 p-1 border border-cyan-500/40">
                            <div>
                                <h3 id="profile-emp-name" class="font-bold text-sm">Employee Name</h3>
                                <p id="profile-emp-role" class="text-[11px] text-cyan-300">Designation | Dept</p>
                            </div>
                        </div>
                        <button onclick="closeHRMSModal('modal-hrms-profile')" class="text-slate-300 hover:text-white p-1">
                            <i class="fa-solid fa-xmark text-sm"></i>
                        </button>
                    </div>
                    <div id="profile-modal-body" class="p-5 max-h-[75vh] overflow-y-auto space-y-4 text-xs">
                        <!-- Populated dynamically by viewEmployeeProfile(id) -->
                    </div>
                    <div class="p-3 bg-slate-50 border-t border-slate-200 text-right">
                        <button onclick="closeHRMSModal('modal-hrms-profile')" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold">Close Profile</button>
                    </div>
                </div>
            </div>

            '''

idx_toast = new_content.find(toast_marker)
final_content = new_content[:idx_toast] + modals_html + new_content[idx_toast:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Successfully updated index.html with complete HRMS view and modals!")
