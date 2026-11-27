// @ts-ignore
import { loadSecOps, switchSecOpsTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const SecOpsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('incidents');
  useEffect(() => {
    try {
      loadSecOps();
    } catch (e) {
      console.error('Error in loadSecOps:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchSecOpsTab(activeTab);
    } catch (e) {
      console.error('Error in switchSecOpsTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-secops" className="module-view ">
                <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200 animate-pulse">
                                <i className="fa-solid fa-radiation mr-1"></i> CERT-In 6-Hour SLA Active
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 border border-indigo-200">
                                <i className="fa-solid fa-clock mr-1"></i> NTP Sync Locked (NPL India)
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                <i className="fa-solid fa-fingerprint mr-1"></i> DPDP Act 2023 DPA Gate
                            </span>
                        </div>
                        <h2 className="text-2xl font-bold text-slate-900">Cybersecurity, Incident Management & CERT-In War Room</h2>
                        <p className="text-sm text-slate-500">Real-time SecOps triage, live CERT-In 6h statutory reporting, forensic evidence chain-of-custody, SIEM threat ingestion, and crisis playbooks for <span className="font-medium text-slate-700">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</span>.</p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                        <button onClick={() => {}} className="px-3 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-headset"></i> P1 War Room Bridge
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-triangle-exclamation"></i> Report Incident
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-bell"></i> Ingest Alert
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-shield-virus"></i> Block Threat IOC
                        </button>
                    </div>
                </div>

                {/* Executive SecOps & War Room KPI Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">Active Incident Queue</span>
                            <i className="fa-solid fa-shield-virus text-rose-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="secops-kpi-active-incidents">1 Active</div>
                        <div className="text-xs text-rose-600 font-semibold mt-1 flex items-center gap-1">
                            <i className="fa-solid fa-triangle-exclamation"></i> P1/P2 Under Active Containment
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">CERT-In 6-Hour SLA</span>
                            <i className="fa-solid fa-stopwatch text-amber-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="secops-kpi-certin-sla">1 Pending</div>
                        <div className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                            <span className="text-emerald-600 font-semibold"><i className="fa-solid fa-check"></i> 100% On-Time</span> Statutory Reporting
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">Threat Intel & IOCs</span>
                            <i className="fa-solid fa-ban text-indigo-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="secops-kpi-threat-iocs">4 Blocked</div>
                        <div className="text-xs text-indigo-600 font-semibold mt-1">
                            WAF & Perimeter WireGuard Drops
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">Forensic Evidence</span>
                            <i className="fa-solid fa-box-archive text-emerald-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="secops-kpi-evidence-count">3 Artifacts</div>
                        <div className="text-xs text-emerald-600 font-semibold mt-1">
                            <i className="fa-solid fa-lock"></i> SHA-256 S3 Object Lock
                        </div>
                    </div>
                </div>

                {/* Navigation Tabs for SecOps War Room */}
                <div className="flex border-b border-slate-200 mb-6 bg-slate-50/70 p-1 rounded-lg gap-1 overflow-x-auto">
                    <button className="secops-tab-btn px-4 py-2 text-xs font-semibold rounded-md bg-white text-rose-700 shadow-sm border border-slate-200" onClick={() => setActiveTab('incidents')}>
                        <i className="fa-solid fa-shield-virus mr-1 text-rose-600"></i> Active Incidents & War Room
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('alerts')}>
                        <i className="fa-solid fa-bell mr-1 text-indigo-600"></i> SIEM Alerts & Threat Signals
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('evidence')}>
                        <i className="fa-solid fa-box-archive mr-1 text-emerald-600"></i> Forensic Evidence Locker
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('threat-intel')}>
                        <i className="fa-solid fa-shield-halved mr-1 text-purple-600"></i> Threat Intel & Blocked IOCs
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('playbooks')}>
                        <i className="fa-solid fa-book-skull mr-1 text-blue-600"></i> NIST Playbook Library
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('vulns')}>
                        <i className="fa-solid fa-bug mr-1 text-amber-600"></i> Vulnerability & CVSS Patches
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('drills')}>
                        <i className="fa-solid fa-person-running mr-1 text-teal-600"></i> Tabletop Cyber Drills
                    </button>
                    <button className="secops-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('certin-reports')}>
                        <i className="fa-solid fa-file-contract mr-1 text-slate-700"></i> CERT-In Regulatory Filings
                    </button>
                </div>

                {/* Tab 1: Active Incidents & War Room Queue */}
                <div id="secops-tab-content-incidents" style={{ display: activeTab === 'incidents' ? 'block' : 'none' }} className="secops-tab-panel">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-shield-virus text-rose-600"></i> Active Security Incidents Queue & Statutory Triage
                                </h3>
                                <p className="text-xs text-slate-500">Real-time incident response queue, mandatory 6-hour CERT-In countdown, and War Room video bridge.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-rose-50 text-rose-700 font-semibold border border-rose-200">
                                6-Hour SLA Countdown Active
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Incident ID & Severity</th>
                                        <th className="p-3">Title & Category</th>
                                        <th className="p-3">Affected Systems & Ingress</th>
                                        <th className="p-3">Status & Commander</th>
                                        <th className="p-3">CERT-In 6h SLA</th>
                                        <th className="p-3">War Room & Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="table-incidents"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 2: SIEM Threat Alerts */}
                <div id="secops-tab-content-alerts" style={{ display: activeTab === 'alerts' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-bell text-indigo-600"></i> SIEM Security Threat Ingestion & Signal Correlation
                                </h3>
                                <p className="text-xs text-slate-500">Automated alerts ingested from AWS GuardDuty, GitHub Secret Scanning, and CrowdStrike EDR agents.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-indigo-50 text-indigo-700 font-semibold border border-indigo-200">
                                Direct Escalation Enabled
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Alert ID</th>
                                        <th className="p-3">Source & Rule</th>
                                        <th className="p-3">Signal Summary</th>
                                        <th className="p-3">Severity</th>
                                        <th className="p-3">Investigation Status</th>
                                        <th className="p-3">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-alerts"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 3: Forensic Evidence Locker */}
                <div id="secops-tab-content-evidence" style={{ display: activeTab === 'evidence' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-box-archive text-emerald-600"></i> Forensic Evidence Locker & Chain of Custody
                                </h3>
                                <p className="text-xs text-slate-500">Tamper-evident evidence storage with cryptographic SHA-256 verification and AWS S3 Object Lock compliance.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                                RFC 3161 Timestamped
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Evidence ID</th>
                                        <th className="p-3">Artifact Name & Source</th>
                                        <th className="p-3">SHA-256 Hash</th>
                                        <th className="p-3">Storage URI & Custody</th>
                                        <th className="p-3">Preserved Date</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-evidence"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 4: Threat Intelligence & Blocked IOCs */}
                <div id="secops-tab-content-threat-intel" style={{ display: activeTab === 'threat-intel' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-shield-halved text-purple-600"></i> Threat Intelligence Indicators of Compromise (IOCs)
                                </h3>
                                <p className="text-xs text-slate-500">Malicious IP addresses, file hashes, domains, and URLs actively dropped at Cloudflare WAF and perimeter gateways.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-purple-50 text-purple-700 font-semibold border border-purple-200">
                                MITRE ATT&CK Mapped
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">IOC ID & Type</th>
                                        <th className="p-3">Indicator Value</th>
                                        <th className="p-3">Threat Actor & Feed</th>
                                        <th className="p-3">Confidence & Technique</th>
                                        <th className="p-3">Enforcement Action</th>
                                        <th className="p-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-iocs"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 5: NIST Incident Playbooks */}
                <div id="secops-tab-content-playbooks" style={{ display: activeTab === 'playbooks' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-book-skull text-blue-600"></i> NIST SP 800-61 Incident Response Playbooks
                                </h3>
                                <p className="text-xs text-slate-500">Step-by-step procedures for containment, eradication, and post-incident recovery across critical threat vectors.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-blue-50 text-blue-700 font-semibold border border-blue-200">
                                6 Active Playbooks
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Code</th>
                                        <th className="p-3">Playbook Name & Category</th>
                                        <th className="p-3">Immediate Containment Steps</th>
                                        <th className="p-3">Investigation & Eradication</th>
                                        <th className="p-3">Regulatory Mandate</th>
                                    </tr>
                                </thead>
                                <tbody id="table-playbooks"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 6: Vulnerability & CVSS Patches */}
                <div id="secops-tab-content-vulns" style={{ display: activeTab === 'vulns' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-bug text-amber-600"></i> Vulnerability Management & CVSS Patch Registry
                                </h3>
                                <p className="text-xs text-slate-500">Security flaw tracking, CVSS v3.1 scoring, affected infrastructure assets, and remediation SLA deadlines.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-amber-50 text-amber-700 font-semibold border border-amber-200">
                                CISA KEV Tracked
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">CVE ID & CVSS</th>
                                        <th className="p-3">Affected Asset & Component</th>
                                        <th className="p-3">Severity</th>
                                        <th className="p-3">Patch Available</th>
                                        <th className="p-3">Remediation Due Date</th>
                                        <th className="p-3">Status & Lead</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-vulns"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 7: Tabletop Cyber Drills */}
                <div id="secops-tab-content-drills" style={{ display: activeTab === 'drills' ? 'block' : 'none' }} className="secops-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-person-running text-teal-600"></i> Tabletop Cyber Crisis Drills & Executive Preparedness
                                </h3>
                                <p className="text-xs text-slate-500">Simulated cyber crises, ransomware isolation exercises, and CERT-In regulatory drills.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-teal-50 text-teal-700 font-semibold border border-teal-200">
                                High Preparedness Rating
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Drill Code</th>
                                        <th className="p-3">Exercise Title & Scenario</th>
                                        <th className="p-3">Target vs Actual Containment</th>
                                        <th className="p-3">Key Lessons Learned</th>
                                        <th className="p-3">Rating & Date</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-drills"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 8: CERT-In Regulatory Filings */}
                <div id="secops-tab-content-certin-reports" className="secops-tab-panel hidden">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-file-contract text-slate-700"></i> Statutory CERT-In Regulatory Filings Ledger
                                </h3>
                                <p className="text-xs text-slate-500">Formal regulatory notifications lodged with the Indian Computer Emergency Response Team (CERT-In).</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-slate-100 text-slate-700 font-semibold border border-slate-200">
                                100% Statutory Adherence
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Report Reference</th>
                                        <th className="p-3">Incident ID</th>
                                        <th className="p-3">CERT-In Ack Number</th>
                                        <th className="p-3">Submission Timestamp</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3">Documents</th>
                                    </tr>
                                </thead>
                                <tbody id="table-secops-certin-reports"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>





            {/* 10. Enterprise Document & Knowledge Vault View */}
    </div>
  );
};

export default SecOpsView;
