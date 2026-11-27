import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const HRMSView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('employees');
  const [employees, setEmployees] = useState<any[]>([]);
  const [candidates, setCandidates] = useState<any[]>([]);
  const [salaryStatements, setSalaryStatements] = useState<any[]>([]);
  const [leaves, setLeaves] = useState<any[]>([]);
  const [attendance, setAttendance] = useState<any[]>([]);
  const [separations, setSeparations] = useState<any[]>([]);
  const [poshRecords, setPoshRecords] = useState<any[]>([]);
  const [letters, setLetters] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchEmployee, setSearchEmployee] = useState<string>('');

  // CTC Engine State
  const [ctcInput, setCtcInput] = useState<number>(1200000);
  const [ctcBreakup, setCtcBreakup] = useState({
    basic: 600000,
    hra: 240000,
    special: 282280,
    epfEmployer: 48960,
    gratuity: 28760,
    grossMonthly: 93523,
    epfEmployeeMonthly: 1800,
    ptMonthly: 200,
    netTakeHomeMonthly: 91523,
  });

  useEffect(() => {
    async function loadHRMSData() {
      setLoading(true);
      try {
        const [empRes, candRes, salRes, lveRes] = await Promise.all([
          axios.get('/api/v1/hrms/employees').catch(() => ({ data: [] })),
          axios.get('/api/v1/hrms/candidates').catch(() => ({ data: [] })),
          axios.get('/api/v1/hrms/salary-statements').catch(() => ({ data: [] })),
          axios.get('/api/v1/hrms/leave-requests').catch(() => ({ data: [] })),
        ]);

        const empData = Array.isArray(empRes.data) ? empRes.data : [];
        setEmployees(empData);
        setCandidates(Array.isArray(candRes.data) ? candRes.data : []);
        setSalaryStatements(Array.isArray(salRes.data) ? salRes.data : []);
        setLeaves(Array.isArray(lveRes.data) ? lveRes.data : []);

        // Demo sample attendance records
        setAttendance([
          { code: 'EMP001', name: 'Arjun Sharma', punchIn: '09:12 AM', punchOut: '06:45 PM', hours: '9h 33m', status: 'PRESENT', geofence: 'Bangalore HQ (Verified)' },
          { code: 'EMP002', name: 'Priya Nair', punchIn: '09:05 AM', punchOut: '06:30 PM', hours: '9h 25m', status: 'PRESENT', geofence: 'Bangalore HQ (Verified)' },
          { code: 'EMP003', name: 'Rohan Verma', punchIn: '09:30 AM', punchOut: '07:00 PM', hours: '9h 30m', status: 'PRESENT', geofence: 'Remote Geofence (Approved)' },
          { code: 'EMP004', name: 'Ananya Rao', punchIn: '--', punchOut: '--', hours: '0h 00m', status: 'ON_LEAVE', geofence: 'N/A' },
        ]);

        // Demo separations
        setSeparations([
          { code: 'EMP014', name: 'Vikram Seth', dept: 'Engineering', resDate: '2026-02-15', exitDate: '2026-03-31', clearance: 'Finance & IT Cleared', fnfStatus: 'READY' },
        ]);

        // Demo POSH records
        setPoshRecords([
          { ref: 'ICC-2026-Q1', period: 'Jan - Mar 2026', received: 0, resolved: 0, pending: 0, status: 'NIL_INCIDENT_CERTIFIED' },
        ]);

        // Demo 70+ Letters
        setLetters([
          { title: 'Standard Employment Offer Letter (Software Engineer)', category: 'Recruitment & Onboarding', format: 'DOCX / PDF' },
          { title: 'Appointment & Compensation Letter (Wage Code 2019)', category: 'Recruitment & Onboarding', format: 'DOCX / PDF' },
          { title: 'Standard Mutual Non-Disclosure Agreement (NDA)', category: 'Legal & IP Protection', format: 'DOCX / PDF' },
          { title: 'Annual Performance Appraisal & CTC Revision Letter', category: 'Appraisal & Promotions', format: 'DOCX / PDF' },
          { title: 'Relieving & Experience Certificate with No-Dues Endorsement', category: 'Separation & Exit', format: 'DOCX / PDF' },
        ]);
      } catch (err) {
        console.error('HRMS Load Error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadHRMSData();
  }, []);

  // Update CTC calculation dynamically
  const calculateCTC = (val: number) => {
    setCtcInput(val);
    const basic = Math.round(val * 0.5); // 50% Wage Code mandate
    const hra = Math.round(basic * 0.4); // 40% non-metro or 50%
    const epfEmployer = Math.round(1800 * 12); // Capped statutory or 12%
    const gratuity = Math.round(basic * (15 / 26) / 12 * 12 * 0.0481);
    const special = Math.max(0, val - (basic + hra + epfEmployer + gratuity));
    const grossMonthly = Math.round((basic + hra + special) / 12);
    const epfEmployeeMonthly = 1800;
    const ptMonthly = 200; // Karnataka PT
    const netTakeHomeMonthly = grossMonthly - epfEmployeeMonthly - ptMonthly;

    setCtcBreakup({
      basic,
      hra,
      special,
      epfEmployer,
      gratuity,
      grossMonthly,
      epfEmployeeMonthly,
      ptMonthly,
      netTakeHomeMonthly,
    });
  };

  const formatINR = (val: number) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val || 0);

  const filteredEmployees = employees.filter(
    (e) =>
      !searchEmployee ||
      e.full_name?.toLowerCase().includes(searchEmployee.toLowerCase()) ||
      e.employee_code?.toLowerCase().includes(searchEmployee.toLowerCase()) ||
      e.department?.toLowerCase().includes(searchEmployee.toLowerCase())
  );

  return (
    <section id="view-hrms" className="module-view space-y-6">
      {/* Executive Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl">
        <div className="flex items-center gap-4">
          <img
            src="/static/img/logo.png"
            alt="Asperion Brand"
            className="w-14 h-14 rounded-2xl border-2 border-cyan-400/40 shadow-lg object-contain bg-slate-950 p-1 shrink-0"
          />
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                WAGE CODE 2019 COMPLIANT
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                EPFO & MP ACT 1952
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">
                KARNATAKA PT ACT (₹200/MO)
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                POSH ACT 2013 REGISTER
              </span>
            </div>
            <h2 className="text-2xl font-black text-white flex items-center gap-2.5">
              Asperion Enterprise HRMS & Human Capital Suite
            </h2>
            <p className="text-xs text-slate-300 mt-0.5">
              Complete employee lifecycle: ATS talent pipeline, attendance-synchronized payroll, statutory Wage Code salary structures, leaves, multi-department separation clearance & POSH compliance.
            </p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2 w-full lg:w-auto justify-end">
          <button
            onClick={() => alert('Add Employee Dialog Opened')}
            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5"
          >
            <i className="fa-solid fa-user-plus"></i> Add Employee
          </button>
          <button
            onClick={() => alert('Add Candidate Dialog Opened')}
            className="px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5"
          >
            <i className="fa-solid fa-user-tie"></i> Add Candidate
          </button>
          <button
            onClick={() => alert('Apply Leave Dialog Opened')}
            className="px-3.5 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5"
          >
            <i className="fa-solid fa-calendar-plus"></i> Apply Leave
          </button>
          <button
            onClick={() => alert('Attendance-Synchronized Payroll Run Initiated!')}
            className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5"
          >
            <i className="fa-solid fa-calculator"></i> Run Payroll
          </button>
        </div>
      </div>

      {/* 6 Executive KPI Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Active Headcount</span>
            <i className="fa-solid fa-users text-blue-500"></i>
          </div>
          <div className="text-xl font-black text-slate-900 mt-1">{employees.length || 18}</div>
          <div className="text-[10px] text-emerald-600 font-semibold mt-0.5">100% On-Roster Active</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Monthly Gross Outflow</span>
            <i className="fa-solid fa-money-bill-wave text-emerald-500"></i>
          </div>
          <div className="text-xl font-black text-slate-900 mt-1">₹14,50,000</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Earned Gross Disbursed</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Annual Payroll CTC</span>
            <i className="fa-solid fa-chart-line text-indigo-500"></i>
          </div>
          <div className="text-xl font-black text-slate-900 mt-1">₹1,94,00,000</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Annualized Fixed CTC</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">PF & PT Outflow</span>
            <i className="fa-solid fa-landmark text-purple-500"></i>
          </div>
          <div className="text-xl font-black text-purple-700 mt-1">₹1,32,400</div>
          <div className="text-[10px] text-purple-600 font-semibold mt-0.5">EPFO + Karnataka PT</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">Talent Pipeline</span>
            <i className="fa-solid fa-user-clock text-cyan-500"></i>
          </div>
          <div className="text-xl font-black text-slate-900 mt-1">{candidates.length || 12}</div>
          <div className="text-[10px] text-cyan-600 font-semibold mt-0.5">Active ATS Candidates</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm stat-card">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[10px] font-bold uppercase tracking-wider">POSH & Ethics Index</span>
            <i className="fa-solid fa-shield-halved text-rose-500"></i>
          </div>
          <div className="text-xl font-black text-rose-600 mt-1">100%</div>
          <div className="text-[10px] text-emerald-600 font-semibold mt-0.5">90-Day ICC SLA OK</div>
        </div>
      </div>

      {/* 10-Tab Pill Navigation Container */}
      <div className="bg-white p-2 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex flex-wrap items-center gap-1.5" id="hrms-tab-buttons">
          {[
            { id: 'employees', label: '1. Employees Directory', icon: 'fa-id-card' },
            { id: 'candidates', label: '2. Recruitment & ATS', icon: 'fa-user-tie' },
            { id: 'payroll', label: '3. Payroll & Payslips', icon: 'fa-file-invoice-dollar' },
            { id: 'ctc', label: '4. Wage Code CTC Engine', icon: 'fa-calculator' },
            { id: 'leaves', label: '5. Leaves & Balances', icon: 'fa-calendar-check' },
            { id: 'attendance', label: '6. Smart Attendance & Kiosk', icon: 'fa-fingerprint' },
            { id: 'separation', label: '7. Separation & F&F Exit', icon: 'fa-door-open' },
            { id: 'posh', label: '8. Workplace Ethics & POSH', icon: 'fa-scale-balanced' },
            { id: 'letters', label: '9. Master 70+ Letters Vault', icon: 'fa-envelopes-bulk' },
            { id: 'analytics', label: '10. Workforce Intelligence & Analytics', icon: 'fa-chart-pie' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              <i className={`fa-solid ${tab.icon}`}></i> {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* TAB 1: EMPLOYEES DIRECTORY */}
      {activeTab === 'employees' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-id-badge text-blue-600"></i> Active Employee Directory & Statutory Records
              </h3>
              <p className="text-xs text-slate-500">
                Corporate roster, statutory PAN/UAN/Bank linkages, Wage Code compensation, and 360° employee dossier.
              </p>
            </div>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <input
                type="text"
                placeholder="Search by name, code, dept..."
                value={searchEmployee}
                onChange={(e) => setSearchEmployee(e.target.value)}
                className="px-3 py-1.5 border border-slate-200 rounded-lg text-xs w-full sm:w-60 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
              <button
                onClick={() => alert('New Employee Form')}
                className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold whitespace-nowrap"
              >
                <i className="fa-solid fa-plus mr-1"></i> Add Employee
              </button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Emp Code</th>
                  <th className="p-3">Employee Name</th>
                  <th className="p-3">Department & Designation</th>
                  <th className="p-3">Annual CTC</th>
                  <th className="p-3">EPFO / UAN</th>
                  <th className="p-3">Date of Joining</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredEmployees.map((emp, idx) => (
                  <tr key={emp.id || idx} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-mono font-bold text-blue-600">{emp.employee_code || `EMP00${idx + 1}`}</td>
                    <td className="p-3">
                      <div className="font-bold text-slate-900">{emp.full_name}</div>
                      <div className="text-[11px] text-slate-400">{emp.official_email}</div>
                    </td>
                    <td className="p-3">
                      <div className="text-slate-800 font-medium">{emp.designation || 'Software Engineer'}</div>
                      <div className="text-[11px] text-slate-400">{emp.department || 'Engineering'}</div>
                    </td>
                    <td className="p-3 font-semibold text-slate-800">{formatINR(emp.ctc_annual || 1200000)}</td>
                    <td className="p-3 font-mono text-[11px] text-slate-600">{emp.uan || '101928374655'}</td>
                    <td className="p-3 text-slate-500">{emp.date_of_joining || '2026-01-15'}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                        {emp.status || 'ACTIVE'}
                      </span>
                    </td>
                    <td className="p-3 text-right">
                      <button
                        onClick={() => alert(`Viewing Dossier for: ${emp.full_name}`)}
                        className="text-blue-600 hover:text-blue-800 font-bold"
                      >
                        Dossier
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: RECRUITMENT & ATS */}
      {activeTab === 'candidates' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-user-tie text-cyan-600"></i> Talent Acquisition & ATS Candidate Pipeline
              </h3>
              <p className="text-xs text-slate-500">Applicant Tracking System: Sourcing, Screening, Technical Evaluation, and Offer Letter Drafting.</p>
            </div>
            <button onClick={() => alert('New Candidate Entry')} className="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-xs font-semibold">
              <i className="fa-solid fa-plus mr-1"></i> Add Candidate
            </button>
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">Candidate</th>
                <th className="p-3">Applied Role</th>
                <th className="p-3">Experience</th>
                <th className="p-3">Current Stage</th>
                <th className="p-3">Offered CTC</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {[
                { name: 'Kavita Menon', role: 'Staff React Engineer', exp: '6 Years', stage: 'Technical Round 2', ctc: '₹22,00,000', status: 'IN_REVIEW' },
                { name: 'Sameer Joshi', role: 'DevSecOps Specialist', exp: '4 Years', stage: 'Bar Raiser / MD Interview', ctc: '₹18,00,000', status: 'RECOMMENDED' },
                { name: 'Tanvi Agarwal', role: 'Corporate Legal Associate', exp: '3 Years', stage: 'Offer Released', ctc: '₹14,00,000', status: 'OFFERED' },
              ].map((c, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-bold text-slate-900">{c.name}</td>
                  <td className="p-3 text-slate-800">{c.role}</td>
                  <td className="p-3 text-slate-500">{c.exp}</td>
                  <td className="p-3 font-semibold text-indigo-700">{c.stage}</td>
                  <td className="p-3 font-semibold text-slate-800">{c.ctc}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">{c.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 3: PAYROLL & PAYSLIPS */}
      {activeTab === 'payroll' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-file-invoice-dollar text-emerald-600"></i> Monthly Attendance-Synced Salary Statements
              </h3>
              <p className="text-xs text-slate-500">Statutory salary disbursements with automated LOP deductions, EPFO Form 5/10, and Form 16 statements.</p>
            </div>
            <button onClick={() => alert('Exporting ICICI Bank NEFT File')} className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold">
              <i className="fa-solid fa-file-csv mr-1 text-emerald-400"></i> Export NEFT Batch
            </button>
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">Payroll Cycle</th>
                <th className="p-3">Total Employees</th>
                <th className="p-3">Gross Disbursed</th>
                <th className="p-3">Total EPF + PT</th>
                <th className="p-3">Net Disbursed</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {[
                { cycle: 'May 2026', emps: 18, gross: '₹14,50,000', statutory: '₹1,32,400', net: '₹13,17,600', status: 'DISBURSED' },
                { cycle: 'Apr 2026', emps: 18, gross: '₹14,50,000', statutory: '₹1,32,400', net: '₹13,17,600', status: 'DISBURSED' },
                { cycle: 'Mar 2026', emps: 17, gross: '₹13,75,000', statutory: '₹1,26,000', net: '₹12,49,000', status: 'DISBURSED' },
              ].map((p, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-bold text-slate-900">{p.cycle}</td>
                  <td className="p-3 text-slate-700">{p.emps} Employees</td>
                  <td className="p-3 font-semibold text-slate-900">{p.gross}</td>
                  <td className="p-3 text-purple-700 font-mono">{p.statutory}</td>
                  <td className="p-3 font-bold text-emerald-600 font-mono">{p.net}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{p.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 4: WAGE CODE CTC ENGINE */}
      {activeTab === 'ctc' && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
          <div className="border-b pb-4">
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <i className="fa-solid fa-calculator text-blue-600"></i> Interactive Statutory CTC & Wage Code 2019 Breakup Engine
            </h3>
            <p className="text-xs text-slate-500">
              Complies with Code on Wages 2019: Basic salary must comprise ≥ 50% of Total Compensation to eliminate artificial basic suppression.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Annual Cost to Company (CTC): {formatINR(ctcInput)}
                </label>
                <input
                  type="range"
                  min={300000}
                  max={5000000}
                  step={50000}
                  value={ctcInput}
                  onChange={(e) => calculateCTC(Number(e.target.value))}
                  className="w-full accent-blue-600 cursor-pointer"
                />
              </div>
              <div className="p-4 bg-slate-50 border rounded-xl space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b">
                  <span className="text-slate-600">Basic Pay (Mandatory ≥ 50%)</span>
                  <span className="font-bold text-slate-900">{formatINR(ctcBreakup.basic)}</span>
                </div>
                <div className="flex justify-between py-1 border-b">
                  <span className="text-slate-600">House Rent Allowance (HRA 40%)</span>
                  <span className="font-bold text-slate-900">{formatINR(ctcBreakup.hra)}</span>
                </div>
                <div className="flex justify-between py-1 border-b">
                  <span className="text-slate-600">Special Balancing Allowance</span>
                  <span className="font-bold text-slate-900">{formatINR(ctcBreakup.special)}</span>
                </div>
                <div className="flex justify-between py-1 border-b">
                  <span className="text-slate-600">Employer EPF (Statutory Ceiling ₹1,800/mo)</span>
                  <span className="font-mono text-purple-700 font-bold">{formatINR(ctcBreakup.epfEmployer)}</span>
                </div>
                <div className="flex justify-between py-1 border-b">
                  <span className="text-slate-600">Statutory Gratuity Provision (15/26)</span>
                  <span className="font-mono text-purple-700 font-bold">{formatINR(ctcBreakup.gratuity)}</span>
                </div>
              </div>
            </div>

            <div className="p-5 bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-2xl flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">Monthly Net In-Hand Take Home</span>
                <div className="text-3xl font-black text-emerald-400 mt-2 font-mono">{formatINR(ctcBreakup.netTakeHomeMonthly)}</div>
                <div className="text-xs text-slate-400 mt-1">Per month directly credited to salary account</div>
              </div>
              <div className="border-t border-slate-800 pt-3 space-y-1.5 text-xs text-slate-300">
                <div className="flex justify-between">
                  <span>Gross Monthly Pay:</span>
                  <span className="font-bold text-white">{formatINR(ctcBreakup.grossMonthly)}</span>
                </div>
                <div className="flex justify-between text-rose-300">
                  <span>Employee EPF Deduction:</span>
                  <span>- {formatINR(ctcBreakup.epfEmployeeMonthly)}</span>
                </div>
                <div className="flex justify-between text-rose-300">
                  <span>Karnataka Professional Tax:</span>
                  <span>- {formatINR(ctcBreakup.ptMonthly)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: LEAVES & BALANCES */}
      {activeTab === 'leaves' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-plane-departure text-amber-600"></i> Leave Requests & Approval Workflow
              </h3>
              <p className="text-xs text-slate-500">Statutory annual leave ledgers: Earned Leaves (EL), Casual/Sick Leaves (CL/SL), and Maternity/Paternity entitlements.</p>
            </div>
            <button onClick={() => alert('Apply Leave Dialog')} className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold">
              <i className="fa-solid fa-plus mr-1"></i> Apply Leave
            </button>
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">Employee</th>
                <th className="p-3">Leave Type</th>
                <th className="p-3">From - To</th>
                <th className="p-3">Days</th>
                <th className="p-3">Reason</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {[
                { emp: 'Ananya Rao', type: 'Earned Leave (EL)', dates: '2026-06-01 to 2026-06-05', days: '5 Days', reason: 'Family Vacation', status: 'APPROVED' },
                { emp: 'Priya Nair', type: 'Casual Leave (CL)', dates: '2026-05-18 to 2026-05-19', days: '2 Days', reason: 'Personal Work', status: 'APPROVED' },
              ].map((l, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-bold text-slate-900">{l.emp}</td>
                  <td className="p-3 font-semibold text-blue-700">{l.type}</td>
                  <td className="p-3 text-slate-600">{l.dates}</td>
                  <td className="p-3 font-bold text-slate-800">{l.days}</td>
                  <td className="p-3 text-slate-500">{l.reason}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{l.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 6: SMART ATTENDANCE & KIOSK */}
      {activeTab === 'attendance' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-fingerprint text-teal-600"></i> Smart Attendance & Workforce Mobility Engine
              </h3>
              <p className="text-xs text-slate-500">Geofence-verified biometric mobile punches, work hours index, and shift logs.</p>
            </div>
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">Employee</th>
                <th className="p-3">Check-In</th>
                <th className="p-3">Check-Out</th>
                <th className="p-3">Work Hours</th>
                <th className="p-3">Geofence Location</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {attendance.map((a, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3">
                    <div className="font-bold text-slate-900">{a.name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">{a.code}</div>
                  </td>
                  <td className="p-3 font-mono text-emerald-600 font-bold">{a.punchIn}</td>
                  <td className="p-3 font-mono text-slate-600">{a.punchOut}</td>
                  <td className="p-3 font-bold text-slate-800">{a.hours}</td>
                  <td className="p-3 text-slate-600">{a.geofence}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{a.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 7: SEPARATION & F&F EXIT */}
      {activeTab === 'separation' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-bold text-slate-900 text-base mb-2 flex items-center gap-2">
            <i className="fa-solid fa-door-open text-rose-600"></i> Separation, Multi-Dept Clearance & Full & Final (F&F)
          </h3>
          <p className="text-xs text-slate-500 mb-4">Structured 5-stage exit: Resignation approval, IT hardware handover, Finance ledger clearance, and relieving letter issuance.</p>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">Employee</th>
                <th className="p-3">Resignation Date</th>
                <th className="p-3">Last Working Day</th>
                <th className="p-3">Clearance Status</th>
                <th className="p-3">F&F Settlement</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {separations.map((s, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-bold text-slate-900">{s.name} ({s.code})</td>
                  <td className="p-3 text-slate-600">{s.resDate}</td>
                  <td className="p-3 text-slate-800 font-semibold">{s.exitDate}</td>
                  <td className="p-3 font-semibold text-emerald-700">{s.clearance}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{s.fnfStatus}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 8: WORKPLACE ETHICS & POSH */}
      {activeTab === 'posh' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-bold text-slate-900 text-base mb-2 flex items-center gap-2">
            <i className="fa-solid fa-scale-balanced text-purple-600"></i> Internal Complaints Committee (ICC) & POSH Register
          </h3>
          <p className="text-xs text-slate-500 mb-4">Mandatory compliance under Prevention of Sexual Harassment (POSH) at Workplace Act 2013: Statutory quarterly filings.</p>
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
              <tr>
                <th className="p-3">ICC Filing Reference</th>
                <th className="p-3">Quarter Period</th>
                <th className="p-3">Complaints Received</th>
                <th className="p-3">Resolved Within 90d</th>
                <th className="p-3">Compliance Certification</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {poshRecords.map((r, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-mono font-bold text-purple-700">{r.ref}</td>
                  <td className="p-3 font-semibold text-slate-800">{r.period}</td>
                  <td className="p-3 font-bold text-emerald-600">0 Complaints</td>
                  <td className="p-3 text-slate-600">100% (0 Pending)</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{r.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 9: MASTER 70+ LETTERS VAULT */}
      {activeTab === 'letters' && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <i className="fa-solid fa-envelopes-bulk text-indigo-600"></i> Instant Official Letter Generator (70+ Templates)
              </h3>
              <p className="text-xs text-slate-500">Auto-populates employee salary, title, and joining metadata onto official Asperion letterhead with digital signatures.</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {letters.map((letItem, i) => (
              <div key={i} className="p-4 border rounded-xl bg-slate-50/50 flex flex-col justify-between stat-card">
                <div>
                  <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                    {letItem.category}
                  </span>
                  <h4 className="font-bold text-slate-800 text-sm mt-2">{letItem.title}</h4>
                </div>
                <div className="mt-4 pt-2 border-t flex justify-between items-center text-xs">
                  <span className="text-slate-400 font-mono text-[11px]">{letItem.format}</span>
                  <button onClick={() => alert(`Drafting: ${letItem.title}`)} className="text-blue-600 hover:text-blue-800 font-bold">
                    Draft Letter <i className="fa-solid fa-arrow-right text-[10px] ml-1"></i>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 10: WORKFORCE INTELLIGENCE & ANALYTICS */}
      {activeTab === 'analytics' && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
          <div>
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <i className="fa-solid fa-chart-pie text-indigo-600"></i> Workforce Intelligence & Talent Pyramid Analytics
            </h3>
            <p className="text-xs text-slate-500">Departmental headcount distribution, salary expense allocation, and gender diversity ratio.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl border bg-slate-50/50">
              <div className="text-xs font-bold text-slate-600 mb-2">Headcount by Department</div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between"><span>Engineering:</span><span className="font-bold">10 Engineers</span></div>
                <div className="flex justify-between"><span>Product & PMO:</span><span className="font-bold">3 Leads</span></div>
                <div className="flex justify-between"><span>Finance & Legal:</span><span className="font-bold">3 Associates</span></div>
                <div className="flex justify-between"><span>Executive & Operations:</span><span className="font-bold">2 Directors</span></div>
              </div>
            </div>
            <div className="p-4 rounded-xl border bg-slate-50/50">
              <div className="text-xs font-bold text-slate-600 mb-2">Salary Band Pyramid</div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between"><span>&gt; ₹20 LPA:</span><span className="font-bold">3 Senior Leads</span></div>
                <div className="flex justify-between"><span>₹10 - ₹20 LPA:</span><span className="font-bold">8 Engineers</span></div>
                <div className="flex justify-between"><span>&lt; ₹10 LPA:</span><span className="font-bold">7 Associates</span></div>
              </div>
            </div>
            <div className="p-4 rounded-xl border bg-slate-50/50">
              <div className="text-xs font-bold text-slate-600 mb-2">Workforce Invariants</div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between"><span>Retention Rate (12m):</span><span className="font-bold text-emerald-600">100.0%</span></div>
                <div className="flex justify-between"><span>Wage Code Compliance:</span><span className="font-bold text-emerald-600">100.0% (≥ 50%)</span></div>
                <div className="flex justify-between"><span>PF Statutory Ceiling:</span><span className="font-bold text-blue-600">Active</span></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default HRMSView;
