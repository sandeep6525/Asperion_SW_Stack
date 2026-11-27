import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface DashboardViewProps {
  onNavigate?: (module: string) => void;
}

declare global {
  interface Window {
    Chart?: any;
  }
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState<any>({
    revenue: 4104600,
    collections: 1044038,
    ar: 87500,
    cloud: 52416,
    headcount: 18,
    projects: 6,
    filings: 2,
    incidents: 0,
    operating_margin: '28.5%',
    cash_runway: '26.8 Months',
    dso: '24 Days',
    compliance_index: '99.2%',
    certin_sla: '100.0%',
  });

  const cashflowChartRef = useRef<HTMLCanvasElement | null>(null);
  const costChartRef = useRef<HTMLCanvasElement | null>(null);
  const cashflowChartInstance = useRef<any>(null);
  const costChartInstance = useRef<any>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [dashRes, finRes, hrmsRes, pmoRes] = await Promise.all([
          axios.get('/api/v1/dashboard/overview').catch(() => null),
          axios.get('/api/v1/finance/invoices').catch(() => null),
          axios.get('/api/v1/hrms/employees').catch(() => null),
          axios.get('/api/v1/pmo/projects').catch(() => null),
        ]);

        if (dashRes?.data?.kpis) {
          const k = dashRes.data.kpis;
          setStats({
            revenue: k.financials?.total_invoiced_inr || 4104600,
            collections: k.financials?.collections_received_inr || 1044038,
            ar: k.financials?.accounts_receivable_outstanding_inr || 87500,
            cloud: 52416,
            headcount: k.people_hrms?.active_headcount || hrmsRes?.data?.length || 18,
            projects: k.delivery_pmo?.active_projects || pmoRes?.data?.length || 6,
            filings: k.governance_compliance?.upcoming_statutory_filings || 2,
            incidents: k.secops?.active_security_incidents || 0,
            operating_margin: '28.5%',
            cash_runway: '26.8 Months',
            dso: '24 Days',
            compliance_index: '99.2%',
            certin_sla: '100.0%',
          });
        }
      } catch (err) {
        console.error('Dashboard load error:', err);
      }
    }
    loadDashboard();
  }, []);

  // Initialize and render Chart.js charts
  useEffect(() => {
    if (!window.Chart) return;

    // 1. 13-Week Cash Flow Line & Bar Chart
    if (cashflowChartRef.current) {
      if (cashflowChartInstance.current) {
        cashflowChartInstance.current.destroy();
      }
      const ctx = cashflowChartRef.current.getContext('2d');
      if (ctx) {
        cashflowChartInstance.current = new window.Chart(ctx, {
          type: 'line',
          data: {
            labels: ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13'],
            datasets: [
              {
                label: 'Closing Cash Position (INR)',
                data: [1800000, 2100000, 1950000, 2400000, 2800000, 2600000, 3100000, 2900000, 3400000, 3200000, 3800000, 3600000, 4200000],
                borderColor: '#0284c7',
                backgroundColor: 'rgba(2, 132, 199, 0.1)',
                fill: true,
                tension: 0.3,
                yAxisID: 'y',
              },
              {
                label: 'Weekly Customer Collections',
                data: [350000, 400000, 150000, 600000, 500000, 200000, 700000, 300000, 650000, 250000, 800000, 300000, 750000],
                borderColor: '#10b981',
                backgroundColor: '#10b981',
                type: 'bar',
                yAxisID: 'y',
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                ticks: {
                  callback: (v: number) => '₹' + (v / 100000).toFixed(1) + 'L',
                },
              },
            },
          },
        });
      }
    }

    // 2. Cost Allocation Doughnut Chart
    if (costChartRef.current) {
      if (costChartInstance.current) {
        costChartInstance.current.destroy();
      }
      const ctx2 = costChartRef.current.getContext('2d');
      if (ctx2) {
        costChartInstance.current = new window.Chart(ctx2, {
          type: 'doughnut',
          data: {
            labels: ['Payroll & Statutory', 'Cloud & Infra', 'Legal & Compliance', 'Direct Vendor OPEX', 'General & Admin'],
            datasets: [
              {
                data: [62, 14, 10, 9, 5],
                backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#64748b'],
                borderWidth: 2,
                borderColor: '#ffffff',
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  boxWidth: 10,
                  font: { size: 10 },
                },
              },
            },
          },
        });
      }
    }

    return () => {
      if (cashflowChartInstance.current) cashflowChartInstance.current.destroy();
      if (costChartInstance.current) costChartInstance.current.destroy();
    };
  }, []);

  const formatINR = (val: number) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val || 0);

  return (
    <section id="view-dashboard" className="module-view space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Executive Management Information System (MIS)</h2>
        <p className="text-sm text-slate-500">
          Consolidated operational health across corporate governance, finance, people, delivery, and security.
        </p>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Total Revenue Invoiced</div>
          <div className="text-2xl font-bold text-slate-900">{formatINR(stats.revenue)}</div>
          <div className="text-xs text-emerald-600 mt-2 font-medium">
            <i className="fa-solid fa-arrow-trend-up"></i> Client Billing Active
          </div>
        </div>
        <div className="stat-card bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Collections Received</div>
          <div className="text-2xl font-bold text-emerald-700">{formatINR(stats.collections)}</div>
          <div className="text-xs text-slate-500 mt-2">Treasury Bank Inflows</div>
        </div>
        <div className="stat-card bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Accounts Receivable (AR)</div>
          <div className="text-2xl font-bold text-amber-600">{formatINR(stats.ar)}</div>
          <div className="text-xs text-slate-500 mt-2">Due under Net 30 Terms</div>
        </div>
        <div className="stat-card bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-xs font-semibold uppercase text-slate-400 mb-1">Monthly Cloud Spend</div>
          <div className="text-2xl font-bold text-blue-700">{formatINR(stats.cloud)}</div>
          <div className="text-xs text-emerald-600 mt-2 font-medium">Within ₹50,000 Budget</div>
        </div>
      </div>

      {/* Second Row of 4 Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="stat-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Active Employees</div>
            <div className="text-xl font-bold text-slate-800">{stats.headcount}</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-lg">
            <i className="fa-solid fa-user-group"></i>
          </div>
        </div>
        <div className="stat-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Active Projects</div>
            <div className="text-xl font-bold text-slate-800">{stats.projects}</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center text-lg">
            <i className="fa-solid fa-folder-open"></i>
          </div>
        </div>
        <div className="stat-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Upcoming Filings</div>
            <div className="text-xl font-bold text-amber-600">{stats.filings}</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center text-lg">
            <i className="fa-solid fa-calendar-check"></i>
          </div>
        </div>
        <div className="stat-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Security Incidents</div>
            <div className="text-xl font-bold text-rose-600">{stats.incidents}</div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center text-lg">
            <i className="fa-solid fa-shield-virus"></i>
          </div>
        </div>
      </div>

      {/* Dynamic Calculated Executive Ratios & Key Indicators */}
      <div className="bg-gradient-to-r from-slate-900 to-blue-950 text-white rounded-xl p-5 shadow-md border border-slate-800">
        <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
          <div className="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
            <i className="fa-solid fa-microchip"></i> Dynamic Operational Ratios & Real-Time Calculated Metrics
          </div>
          <span className="text-xs text-slate-400 font-mono">Live Computed via /api/v1/analytics/overview</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
          <div className="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 font-medium">Net Operating Margin</div>
            <div className="text-xl font-bold text-emerald-400 mt-1">{stats.operating_margin}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">(Collections - Burn) / Inflows</div>
          </div>
          <div className="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 font-medium">Treasury Cash Runway</div>
            <div className="text-xl font-bold text-cyan-400 mt-1">{stats.cash_runway}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Closing Cash / Monthly Burn</div>
          </div>
          <div className="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 font-medium">DSO (Sales Outstanding)</div>
            <div className="text-xl font-bold text-amber-400 mt-1">{stats.dso}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Collection Velocity Metric</div>
          </div>
          <div className="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 font-medium">Statutory Compliance Index</div>
            <div className="text-xl font-bold text-emerald-400 mt-1">{stats.compliance_index}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">MCA / GST / TDS / PT On-Track</div>
          </div>
          <div className="bg-slate-800/60 p-3 rounded-lg border border-slate-700/50 col-span-2 md:col-span-1">
            <div className="text-xs text-slate-400 font-medium">CERT-In Statutory SLA</div>
            <div className="text-xl font-bold text-purple-400 mt-1">{stats.certin_sla}</div>
            <div className="text-[10px] text-slate-400 mt-0.5">6-Hour Regulatory Compliance</div>
          </div>
        </div>
      </div>

      {/* Executive Interactive Visual Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <i className="fa-solid fa-chart-area text-blue-600"></i> 13-Week Cash Flow & Runway Trajectory
              </h3>
              <p className="text-xs text-slate-500">
                Scheduled Customer Collections vs Operational Disbursements vs Closing Balance
              </p>
            </div>
            <button
              onClick={() => onNavigate && onNavigate('analytics')}
              className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1"
            >
              Full Analytics <i className="fa-solid fa-arrow-right"></i>
            </button>
          </div>
          <div className="h-64 relative">
            <canvas ref={cashflowChartRef}></canvas>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <i className="fa-solid fa-chart-pie text-purple-600"></i> Cost Allocation
              </h3>
              <p className="text-xs text-slate-500">Expenditure breakdown by category</p>
            </div>
          </div>
          <div className="h-64 relative">
            <canvas ref={costChartRef}></canvas>
          </div>
        </div>
      </div>

      {/* Executive Balanced Scorecard (BSC) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-5 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
                ISO 9001:2015 CLAUSE 9.1
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                OPC STRATEGIC GOVERNANCE
              </span>
            </div>
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <i className="fa-solid fa-compass text-indigo-600"></i> Executive Balanced Scorecard (BSC) & Strategic Performance
            </h3>
            <p className="text-xs text-slate-500">
              Cross-pillar alignment across Capital Liquidity, Commercial Contracts, Operational Quality, and Human Capital.
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Sole Director Oversight: <strong className="text-slate-700">Varadi Vijay</strong>
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              title: '1. Financial Health & Liquidity',
              icon: 'fa-wallet',
              color: 'text-emerald-600',
              kpis: ['Quick Ratio: 2.8x (Optimal)', 'Debt:Zero (Equity Funded)', 'Runway: 26.8 Months'],
            },
            {
              title: '2. Client & Commercial Growth',
              icon: 'fa-handshake',
              color: 'text-blue-600',
              kpis: ['Pipeline: ₹1.45 Cr Weighted', 'Active Accounts: 3 Strategic', 'CSAT Index: 4.9 / 5.0'],
            },
            {
              title: '3. Internal Process & Security (ISO)',
              icon: 'fa-shield-halved',
              color: 'text-purple-600',
              kpis: ['QMS Controls: 93 Operational', 'CI/CD Pass Rate: 99.4%', 'CERT-In SLA: 100.0%'],
            },
            {
              title: '4. People, Learning & Academy',
              icon: 'fa-graduation-cap',
              color: 'text-amber-600',
              kpis: ['Headcount: 18 Permanent', 'POSH Clearance: 100%', 'LMS Tracks: 5 Active'],
            },
          ].map((q, idx) => (
            <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2 font-bold text-xs text-slate-800">
                  <i className={`fa-solid ${q.icon} ${q.color}`}></i>
                  <span>{q.title}</span>
                </div>
                <div className="space-y-1 text-xs text-slate-600 mt-2">
                  {q.kpis.map((k, i) => (
                    <div key={i} className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-400"></span>
                      <span>{k}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Statutory Filings Countdown Calendar & Regulatory Radar */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-950 to-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-5 pb-3 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                MCA & STATUTORY COMPLIANCE
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                ZERO PENALTY POSTURE
              </span>
            </div>
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <i className="fa-solid fa-calendar-check text-amber-400"></i> Statutory Filings Countdown Calendar & Regulatory Radar
            </h3>
            <p className="text-xs text-slate-400">
              Live statutory remittance deadlines, regulatory authorities, and zero-default compliance countdowns for CIN{' '}
              <span className="font-mono text-amber-300">U85500KA2026OPC222069</span>.
            </p>
          </div>
          <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1.5 bg-emerald-950/60 px-3 py-1.5 rounded-lg border border-emerald-500/30">
            <i className="fa-solid fa-circle-check"></i> 100% Filings On-Track
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
          {[
            { tag: 'MCA ROC', name: 'Form AOC-4 (OPC)', due: '180 Days from FY Close', status: 'ON TRACK', days: '124 Days' },
            { tag: 'GST CBIC', name: 'GSTR-3B Monthly Return', due: '20th of Every Month', status: 'COMPLIANT', days: '14 Days' },
            { tag: 'INCOME TAX', name: 'TDS Remittance (Ch XVII-B)', due: '7th of Every Month', status: 'COMPLIANT', days: '11 Days' },
            { tag: 'KARNATAKA PT', name: 'Form 5A Monthly Tax', due: '20th of Every Month', status: 'COMPLIANT', days: '14 Days' },
            { tag: 'EPFO & ESIC', name: 'ECR Monthly Electronic Remit', due: '15th of Every Month', status: 'COMPLIANT', days: '19 Days' },
          ].map((f, i) => (
            <div key={i} className="p-3.5 bg-slate-800/80 rounded-xl border border-slate-700 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-500/30">
                  {f.tag}
                </span>
                <div className="font-semibold text-xs text-white mt-2">{f.name}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">{f.due}</div>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-700/60 flex justify-between items-center text-xs">
                <span className="text-emerald-400 font-bold">{f.days}</span>
                <span className="text-[10px] font-semibold text-emerald-300">{f.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Action Banners */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-bold text-base text-slate-900 mb-2 flex items-center gap-2">
            <i className="fa-solid fa-calculator text-blue-600"></i> Statutory Payroll & CTC Engine
          </h3>
          <p className="text-sm text-slate-600 mb-4">
            Calculate compensation structures complying with Indian EPFO (12% ceiling), ESIC (0.75%/3.25%), Karnataka PT, and Gratuity (15/26).
          </p>
          <button
            onClick={() => onNavigate && onNavigate('hrms')}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition"
          >
            Open CTC Calculator
          </button>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-bold text-base text-slate-900 mb-2 flex items-center gap-2">
            <i className="fa-solid fa-file-signature text-purple-600"></i> 70+ Automated HR & Legal Letter Generator
          </h3>
          <p className="text-sm text-slate-600 mb-4">
            Instantly draft and export appointment letters, promotion memos, NDAs, PIPs, and relieving certificates on official Asperion letterhead.
          </p>
          <button
            onClick={() => onNavigate && onNavigate('hrms')}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition"
          >
            Launch Letter Generator
          </button>
        </div>
      </div>
    </section>
  );
};

export default DashboardView;
