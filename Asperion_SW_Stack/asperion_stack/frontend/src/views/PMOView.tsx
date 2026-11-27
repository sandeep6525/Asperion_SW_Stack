import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const PMOView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('portfolio');
  const [projects, setProjects] = useState<any[]>([]);
  const [intakes, setIntakes] = useState<any[]>([]);
  const [charters, setCharters] = useState<any[]>([]);
  const [capacity, setCapacity] = useState<any[]>([]);
  const [steerco, setSteerco] = useState<any[]>([]);
  const [uatSignoffs, setUatSignoffs] = useState<any[]>([]);
  const [raidLogs, setRaidLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadPMOData() {
      setLoading(true);
      try {
        const [projRes, intRes, charRes] = await Promise.all([
          axios.get('/api/v1/pmo/projects').catch(() => ({ data: [] })),
          axios.get('/api/v1/pmo/intakes').catch(() => ({ data: [] })),
          axios.get('/api/v1/pmo/charters').catch(() => ({ data: [] })),
        ]);
        setProjects(Array.isArray(projRes.data) ? projRes.data : []);
        setIntakes(Array.isArray(intRes.data) ? intRes.data : []);
        setCharters(Array.isArray(charRes.data) ? charRes.data : []);

        // Demo sample capacity, steerco, uat, raid
        setCapacity([
          { role: 'Staff React Engineer', allocated: '100%', project: 'Zenith Omni-Channel Commerce', billable: '100% Billable' },
          { role: 'Backend FastAPI Architect', allocated: '100%', project: 'Core Enterprise OS v1.0', billable: '100% Billable' },
          { role: 'DevSecOps & SRE Lead', allocated: '80%', project: 'CERT-In Statutory Sentinel', billable: 'Internal Security' },
        ]);

        setSteerco([
          { ref: 'SC-DEC-2026-01', decision: 'Approval of React 19 Frontend Migration', owner: 'Sole Director (Varadi Vijay)', date: '2026-03-01', status: 'EXECUTED' },
          { ref: 'SC-DEC-2026-02', decision: 'ISO 27001 Surveillance Audit Budget Allocation', owner: 'CISO / Lead Architect', date: '2026-03-15', status: 'APPROVED' },
        ]);

        setUatSignoffs([
          { prj: 'Zenith Global Commerce', milestone: 'Milestone 1: Core API & Microservices', signoffDate: '2026-02-15', clientRep: 'Zenith VP Tech', status: 'SIGNED_OFF' },
          { prj: 'Zenith Global Commerce', milestone: 'Milestone 2: B2B Commerce & Payments', signoffDate: '2026-03-31', clientRep: 'Zenith VP Tech', status: 'IN_UAT' },
        ]);

        setRaidLogs([
          { type: 'RISK', desc: 'Potential 45-day MSME payment delay from vendor side', severity: 'MEDIUM', mitigation: 'Automated Chapter XVII-B TDS and Samadhaan check', owner: 'Finance Lead' },
          { type: 'DEPENDENCY', desc: 'CERT-In NTP time-sync lock on multi-cloud hosts', severity: 'HIGH', mitigation: 'NPL India atomic clock primary and secondary NTP daemons', owner: 'SRE Lead' },
        ]);
      } catch (err) {
        console.error('PMO Load Error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadPMOData();
  }, []);

  const formatINR = (val: number) =>
    new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val || 0);

  return (
    <section id="view-pmo" className="module-view space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 p-6 rounded-2xl border border-slate-800 text-white shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40">
              PRINCE2 & STAGE-GATE GOVERNANCE
            </span>
            <span className="text-xs text-slate-400">Fixed-Price & T&M Client Engineering Delivery</span>
          </div>
          <h2 className="text-2xl font-black text-white flex items-center gap-2.5">
            <i className="fa-solid fa-diagram-project text-blue-400"></i> PMO & Enterprise Delivery Command
          </h2>
          <p className="text-xs text-slate-300 mt-0.5">
            End-to-end delivery framework: 5 Stage-Gates, sprint velocity, resource utilization, SteerCo governance, and client UAT sign-offs.
          </p>
        </div>
        <div className="flex gap-2">
          <button onClick={() => alert('New Project Intake')} className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-lg transition shadow flex items-center gap-1.5">
            <i className="fa-solid fa-plus"></i> New Project Intake
          </button>
        </div>
      </div>

      {/* Sub-Tabs */}
      <div className="bg-white p-2 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex flex-wrap items-center gap-1.5">
          {[
            { id: 'portfolio', label: '1. Projects Portfolio', icon: 'fa-folder-open' },
            { id: 'sprint', label: '2. Sprint Execution Board', icon: 'fa-bars-staggered' },
            { id: 'stage1', label: '3. Stage-Gate 1: Intake', icon: 'fa-inbox' },
            { id: 'stage2', label: '4. Stage-Gate 2: Charters', icon: 'fa-file-contract' },
            { id: 'capacity', label: '5. Resource Capacity Plan', icon: 'fa-people-arrows' },
            { id: 'steerco', label: '6. SteerCo Action Register', icon: 'fa-gavel' },
            { id: 'uat', label: '7. Stage-Gate 4: UAT Sign-off', icon: 'fa-clipboard-check' },
            { id: 'raid', label: '8. RAID Log (Risks/Issues)', icon: 'fa-shield-halved' },
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

      {/* Tab Content */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-5">
        {activeTab === 'portfolio' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-folder-open text-blue-600"></i> Active Projects Portfolio & Financial Health
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Project Code</th>
                  <th className="p-3">Project Name & Client</th>
                  <th className="p-3">Contract Value</th>
                  <th className="p-3">Progress</th>
                  <th className="p-3">Delivery Lead</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {[
                  { code: 'PRJ-ZENITH-2026', name: 'Zenith Global Omni-Channel Commerce', client: 'Zenith Global Retail Ltd', value: 4500000, prog: 78, pm: 'Arjun Sharma', status: 'ON_TRACK' },
                  { code: 'PRJ-APEX-02', name: 'Apex Logistics Freight IoT Gateway', client: 'Apex Logistics India', value: 2800000, prog: 45, pm: 'Priya Nair', status: 'ON_TRACK' },
                  { code: 'PRJ-FINTECH-03', name: 'Micro-Lending Credit Risk Engine', client: 'FinTech Capital', value: 3600000, prog: 90, pm: 'Rohan Verma', status: 'UAT_PHASE' },
                ].map((p, idx) => (
                  <tr key={idx} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-mono font-bold text-blue-600">{p.code}</td>
                    <td className="p-3">
                      <div className="font-bold text-slate-900">{p.name}</div>
                      <div className="text-[11px] text-slate-400">{p.client}</div>
                    </td>
                    <td className="p-3 font-semibold text-slate-800">{formatINR(p.value)}</td>
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <div className="w-24 bg-slate-200 h-1.5 rounded-full overflow-hidden">
                          <div className="bg-blue-600 h-full rounded-full" style={{ width: `${p.prog}%` }}></div>
                        </div>
                        <span className="font-bold text-slate-700">{p.prog}%</span>
                      </div>
                    </td>
                    <td className="p-3 text-slate-700">{p.pm}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{p.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'sprint' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-bars-staggered text-blue-600"></i> Sprint Execution Board (Sprint 1 - Core Foundations)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                <div className="font-bold text-xs text-slate-700 uppercase mb-3 flex justify-between">
                  <span>To Do (Backlog)</span>
                  <span className="bg-slate-200 text-slate-700 px-2 py-0.5 rounded text-[10px]">2 Items</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="bg-white p-3 rounded-lg border shadow-xs">
                    <span className="text-[10px] font-mono font-bold text-blue-600">WBS 2.4</span>
                    <div className="font-semibold text-slate-800 mt-1">Multi-Cloud Terraform Script Validation</div>
                    <div className="text-[10px] text-slate-400 mt-1">Assigned: DevSecOps Lead</div>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-200">
                <div className="font-bold text-xs text-blue-900 uppercase mb-3 flex justify-between">
                  <span>In Progress</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-0.5 rounded text-[10px]">3 Items</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="bg-white p-3 rounded-lg border border-blue-200 shadow-xs">
                    <span className="text-[10px] font-mono font-bold text-blue-600">WBS 1.2</span>
                    <div className="font-semibold text-slate-800 mt-1">Full React 19 Frontend Migration & Hardening</div>
                    <div className="text-[10px] text-emerald-600 font-bold mt-1">95% Completed</div>
                  </div>
                </div>
              </div>

              <div className="bg-emerald-50/50 p-4 rounded-xl border border-emerald-200">
                <div className="font-bold text-xs text-emerald-900 uppercase mb-3 flex justify-between">
                  <span>Done / Verified</span>
                  <span className="bg-emerald-200 text-emerald-800 px-2 py-0.5 rounded text-[10px]">8 Items</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="bg-white p-3 rounded-lg border border-emerald-200 shadow-xs">
                    <span className="text-[10px] font-mono font-bold text-emerald-600">WBS 1.1</span>
                    <div className="font-semibold text-slate-800 mt-1">FastAPI Backend Pytest Suite (235/235 Passed)</div>
                    <div className="text-[10px] text-slate-400 mt-1">Verified on SQLite WAL</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'stage1' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-inbox text-blue-600"></i> Stage-Gate 1: Project Intake & Business Cases
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Intake Code</th>
                  <th className="p-3">Proposed Initiative</th>
                  <th className="p-3">Sponsor / Client</th>
                  <th className="p-3">Strategic Alignment</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {[
                  { code: 'INT-2026-01', title: 'Autonomous Swarm AI for Supply Chain', sponsor: 'Directorate', align: 'Strategic Innovation', status: 'GATE_1_PASSED' },
                  { code: 'INT-2026-02', title: 'Open Banking Account Aggregator Integration', sponsor: 'FinTech Capital', align: 'Revenue Growth', status: 'UNDER_REVIEW' },
                ].map((item, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-mono font-bold text-blue-600">{item.code}</td>
                    <td className="p-3 font-semibold text-slate-800">{item.title}</td>
                    <td className="p-3 text-slate-600">{item.sponsor}</td>
                    <td className="p-3 text-slate-500">{item.align}</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{item.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'capacity' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-people-arrows text-purple-600"></i> Resource Capacity & Skills Allocation Plan
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Role / Skill Domain</th>
                  <th className="p-3">Allocation %</th>
                  <th className="p-3">Active Project Assignment</th>
                  <th className="p-3">Billability</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {capacity.map((c, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-bold text-slate-800">{c.role}</td>
                    <td className="p-3 font-bold text-emerald-600 font-mono">{c.allocated}</td>
                    <td className="p-3 text-slate-700">{c.project}</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">{c.billable}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'steerco' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-gavel text-amber-600"></i> SteerCo Action & Decision Register
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Decision Ref</th>
                  <th className="p-3">Decision Subject</th>
                  <th className="p-3">Authorizing Officer</th>
                  <th className="p-3">Date</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {steerco.map((s, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-mono font-bold text-amber-700">{s.ref}</td>
                    <td className="p-3 font-semibold text-slate-800">{s.decision}</td>
                    <td className="p-3 text-slate-600">{s.owner}</td>
                    <td className="p-3 text-slate-500">{s.date}</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{s.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'uat' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-clipboard-check text-emerald-600"></i> Stage-Gate 4: Quality & UAT Acceptance Sign-Offs
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">Project</th>
                  <th className="p-3">Milestone Subject</th>
                  <th className="p-3">Client Representative</th>
                  <th className="p-3">Sign-off Date</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {uatSignoffs.map((u, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-bold text-slate-900">{u.prj}</td>
                    <td className="p-3 text-slate-800 font-semibold">{u.milestone}</td>
                    <td className="p-3 text-slate-600">{u.clientRep}</td>
                    <td className="p-3 text-slate-500">{u.signoffDate}</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{u.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'raid' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <i className="fa-solid fa-shield-halved text-rose-600"></i> RAID Log (Risks, Assumptions, Issues, Dependencies)
            </h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] border-b">
                <tr>
                  <th className="p-3">RAID Classification</th>
                  <th className="p-3">Description & Impact</th>
                  <th className="p-3">Severity</th>
                  <th className="p-3">Mitigation Action</th>
                  <th className="p-3">Owner</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {raidLogs.map((r, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-bold font-mono text-purple-700">{r.type}</td>
                    <td className="p-3 text-slate-800">{r.desc}</td>
                    <td className="p-3"><span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">{r.severity}</span></td>
                    <td className="p-3 text-slate-600">{r.mitigation}</td>
                    <td className="p-3 font-medium text-slate-700">{r.owner}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
};

export default PMOView;
