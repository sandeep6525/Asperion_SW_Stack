// @ts-ignore
import { loadInfrastructure, switchInfraTab } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const InfrastructureView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('passkeys');
  useEffect(() => {
    try {
      loadInfrastructure();
    } catch (e) {
      console.error('Error in loadInfrastructure:', e);
    }
  }, []);

  useEffect(() => {
    try {
      switchInfraTab(activeTab);
    } catch (e) {
      console.error('Error in switchInfraTab:', e);
    }
  }, [activeTab]);

  return (
    <div className="w-full">
      <section id="view-infrastructure" className="module-view ">
                <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 border border-indigo-200">
                                <i className="fa-solid fa-fingerprint mr-1"></i> FIDO2 / WebAuthn Level 3
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                <i className="fa-solid fa-shield-halved mr-1"></i> Zero-Trust Network Access
                            </span>
                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                                <i className="fa-solid fa-server mr-1"></i> ISO 22301 Active DR
                            </span>
                        </div>
                        <h2 className="text-2xl font-bold text-slate-900">IT, Cloud & Passkey Access Infrastructure</h2>
                        <p className="text-sm text-slate-500">Hardware assets, multi-region cloud workloads, passwordless biometric passkeys, ZTNA access gates, and DR simulation drills for <span className="font-medium text-slate-700">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</span>.</p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                        <button onClick={() => {}} className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-key"></i> Enroll Passkey
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-shield-cat"></i> New ZTNA Policy
                        </button>
                        <button onClick={() => {}} className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
                            <i className="fa-solid fa-rotate"></i> Run DR Drill
                        </button>
                    </div>
                </div>

                {/* Executive Infrastructure & Zero-Trust KPI Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">Hardware Fleet</span>
                            <i className="fa-solid fa-laptop text-blue-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="infra-kpi-hardware">1 Active</div>
                        <div className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                            <span className="text-emerald-600 font-semibold"><i className="fa-solid fa-lock"></i> 100% Encrypted</span> (BitLocker/FileVault)
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">Cloud Infrastructure</span>
                            <i className="fa-solid fa-cloud text-sky-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="infra-kpi-cloud">₹32,400 / mo</div>
                        <div className="text-xs text-slate-500 mt-1">
                            AWS ap-south-1 (Mumbai) & ap-south-2 (Warm Standby)
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">FIDO2 Passkeys</span>
                            <i className="fa-solid fa-fingerprint text-indigo-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="infra-kpi-passkeys">4 Enrolled</div>
                        <div className="text-xs text-indigo-600 font-semibold mt-1 flex items-center gap-1">
                            <i className="fa-solid fa-check-double"></i> WebAuthn Hardware Bound
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-500 mb-2">
                            <span className="text-xs uppercase font-bold tracking-wider">DR Drill Posture</span>
                            <i className="fa-solid fa-heart-pulse text-emerald-600 text-base"></i>
                        </div>
                        <div className="text-2xl font-black text-slate-900" id="infra-kpi-dr">RTO 18.5m</div>
                        <div className="text-xs text-emerald-600 font-semibold mt-1">
                            <i className="fa-solid fa-circle-check"></i> RPO 2.1m | Zero Data Loss (ISO 22301)
                        </div>
                    </div>
                </div>

                {/* Navigation Tabs for Infrastructure */}
                <div className="flex border-b border-slate-200 mb-6 bg-slate-50/70 p-1 rounded-lg gap-1 overflow-x-auto">
                    <button className="infra-tab-btn px-4 py-2 text-xs font-semibold rounded-md bg-white text-indigo-700 shadow-sm border border-slate-200" onClick={() => setActiveTab('passkeys')}>
                        <i className="fa-solid fa-fingerprint mr-1 text-indigo-600"></i> FIDO2 Passkeys Directory
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('ztna')}>
                        <i className="fa-solid fa-shield-halved mr-1 text-emerald-600"></i> Zero-Trust Policies (ZTNA)
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('dr')}>
                        <i className="fa-solid fa-arrows-spin mr-1 text-blue-600"></i> DR Simulation Drills (RTO/RPO)
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('hardware')}>
                        <i className="fa-solid fa-laptop mr-1 text-slate-600"></i> Hardware Fleet
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('cloud')}>
                        <i className="fa-solid fa-cloud mr-1 text-sky-600"></i> Cloud Workloads & Budgets
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('certs')}>
                        <i className="fa-solid fa-certificate mr-1 text-amber-600"></i> SSL/TLS Certificates & Secrets
                    </button>
                    <button className="infra-tab-btn px-4 py-2 text-xs font-medium rounded-md text-slate-600 hover:text-slate-900" onClick={() => setActiveTab('checklists')}>
                        <i className="fa-solid fa-list-check mr-1 text-purple-600"></i> IT Provisioning
                    </button>
                </div>

                {/* Tab 1: FIDO2 Passkeys Directory */}
                <div id="infra-tab-content-passkeys" style={{ display: activeTab === 'passkeys' ? 'block' : 'none' }} className="infra-tab-panel">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-fingerprint text-indigo-600"></i> FIDO2 / WebAuthn Hardware Passkeys Directory
                                </h3>
                                <p className="text-xs text-slate-500">Phishing-resistant cryptographic public key credentials bound to hardware security keys & device biometrics.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-indigo-50 text-indigo-700 font-semibold border border-indigo-200">
                                Clone Detection Enabled (Sign Counter Validation)
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Passkey ID / Credential</th>
                                        <th className="p-3">Stakeholder & Email</th>
                                        <th className="p-3">Authenticator Hardware</th>
                                        <th className="p-3">Sign Count (Cloning Guard)</th>
                                        <th className="p-3">Last Verified</th>
                                        <th className="p-3">Zero-Trust Posture</th>
                                    </tr>
                                </thead>
                                <tbody id="table-passkeys-directory"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 2: Zero-Trust Network Access Policies */}
                <div id="infra-tab-content-ztna" style={{ display: activeTab === 'ztna' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-shield-halved text-emerald-600"></i> Zero-Trust Network Access (ZTNA) Guardrail Policies
                                </h3>
                                <p className="text-xs text-slate-500">Explicit verification rules enforcing FIDO2 passkeys, full disk encryption, and WireGuard mesh routing for high-privilege workloads.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                                Enforcement: Active Blocking
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Policy Code</th>
                                        <th className="p-3">Policy Name & Resource</th>
                                        <th className="p-3">Privilege Tier</th>
                                        <th className="p-3">FIDO2 & Encryption</th>
                                        <th className="p-3">Allowed Ingress & Session TTL</th>
                                        <th className="p-3">Mode</th>
                                    </tr>
                                </thead>
                                <tbody id="table-ztna-policies"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 3: Disaster Recovery Simulation Drills (ISO 22301) */}
                <div id="infra-tab-content-dr" style={{ display: activeTab === 'dr' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
                            <div>
                                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                    <i className="fa-solid fa-arrows-spin text-blue-600"></i> Disaster Recovery (DR) Simulation Drills & RTO/RPO SLA Tracking
                                </h3>
                                <p className="text-xs text-slate-500">Automated failover exercises, standby cluster validation, and point-in-time recovery audits meeting ISO 22301 business continuity requirements.</p>
                            </div>
                            <span className="text-xs px-2.5 py-1 rounded bg-blue-50 text-blue-700 font-semibold border border-blue-200">
                                Target SLAs: RTO &le; 60m | RPO &le; 15m
                            </span>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Drill Code & Type</th>
                                        <th className="p-3">Target Cluster & Scenario</th>
                                        <th className="p-3">Actual vs Target RTO</th>
                                        <th className="p-3">Actual vs Target RPO</th>
                                        <th className="p-3">Data Integrity</th>
                                        <th className="p-3">Outcome & Auditor</th>
                                    </tr>
                                </thead>
                                <tbody id="table-dr-simulations"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 4: Hardware Fleet */}
                <div id="infra-tab-content-hardware" style={{ display: activeTab === 'hardware' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-laptop text-blue-600"></i> IT Hardware Asset Inventory
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Tag</th>
                                        <th className="p-3">Model & Serial</th>
                                        <th className="p-3">Assigned User</th>
                                        <th className="p-3">Disk Encryption</th>
                                        <th className="p-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-assets"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 5: Cloud Workloads */}
                <div id="infra-tab-content-cloud" style={{ display: activeTab === 'cloud' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-cloud text-sky-600"></i> Cloud Subscriptions & Budgets
                            </h3>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                        <tr>
                                            <th className="p-3">Cloud ID</th>
                                            <th className="p-3">Provider / Env</th>
                                            <th className="p-3">Region</th>
                                            <th className="p-3">Spend / Budget</th>
                                            <th className="p-3">Security</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-cloud"></tbody>
                                </table>
                            </div>
                        </div>

                        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                            <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                                <i className="fa-solid fa-key text-purple-600"></i> IAM Access & Passkey Posture
                            </h3>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                        <tr>
                                            <th className="p-3">ID</th>
                                            <th className="p-3">User</th>
                                            <th className="p-3">System & Role</th>
                                            <th className="p-3">Passkey Status</th>
                                            <th className="p-3">Review</th>
                                        </tr>
                                    </thead>
                                    <tbody id="table-iam"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab 6: SSL/TLS Certificates */}
                <div id="infra-tab-content-certs" style={{ display: activeTab === 'certs' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-certificate text-emerald-600"></i> SSL/TLS Certificates & Secret Expiration Tracking
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                                    <tr>
                                        <th className="p-2.5">Item Type</th>
                                        <th className="p-2.5">Identifier / Hostname</th>
                                        <th className="p-2.5">Issuer</th>
                                        <th className="p-2.5">Expiry Date</th>
                                        <th className="p-2.5">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-certs"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Tab 7: Provisioning Checklists */}
                <div id="infra-tab-content-checklists" style={{ display: activeTab === 'checklists' ? 'block' : 'none' }} className="infra-tab-panel ">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-list-check text-purple-600"></i> IT Employee Provisioning & Deprovisioning Checklists
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Employee</th>
                                        <th className="p-3">Process</th>
                                        <th className="p-3">Google Workspace</th>
                                        <th className="p-3">GitHub Org</th>
                                        <th className="p-3">AWS IAM SSO</th>
                                        <th className="p-3">FIDO2 Passkey</th>
                                        <th className="p-3">Signoff</th>
                                    </tr>
                                </thead>
                                <tbody id="table-provisioning-checklists"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>





            {/* 9. SecOps View */}
    </div>
  );
};

export default InfrastructureView;
