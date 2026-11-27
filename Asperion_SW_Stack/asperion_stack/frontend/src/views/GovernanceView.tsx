// @ts-ignore
import { loadGovernance } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const GovernanceView: React.FC = () => {
  useEffect(() => {
    try {
      loadGovernance();
    } catch (e) {
      console.error('Error in loadGovernance:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-governance" className="module-view ">
                <div className="mb-6 flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900">Corporate Governance & OPC Registers</h2>
                        <p className="text-sm text-slate-500">Board resolutions, MCA/ROC filings, compliance calendar, and delegation of authority.</p>
                    </div>
                </div>
                
                <div className="grid grid-cols-1 gap-6">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-gavel text-blue-600"></i> Board / Sole Director Resolutions
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Resolution No</th>
                                        <th className="p-3">Title / Subject</th>
                                        <th className="p-3">Category</th>
                                        <th className="p-3">Date Passed</th>
                                        <th className="p-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-resolutions"></tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-calendar-days text-amber-600"></i> Statutory Compliance Calendar (MCA / GST / TDS / PT)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Compliance Item</th>
                                        <th className="p-3">Statutory Authority</th>
                                        <th className="p-3">Form / Return</th>
                                        <th className="p-3">Due Date</th>
                                        <th className="p-3">Frequency</th>
                                        <th className="p-3">Penalty Risk</th>
                                    </tr>
                                </thead>
                                <tbody id="table-compliance"></tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-shield-halved text-purple-600"></i> Corporate Policy Catalog
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Policy Code</th>
                                        <th className="p-3">Policy Name</th>
                                        <th className="p-3">Category</th>
                                        <th className="p-3">Effective Date</th>
                                        <th className="p-3">Scope / Summary</th>
                                    </tr>
                                </thead>
                                <tbody id="table-policies"></tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-clock-rotate-left text-indigo-600"></i> Enterprise Audit Trail (Immutable Activity Records)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Timestamp</th>
                                        <th className="p-3">Module</th>
                                        <th className="p-3">Severity</th>
                                        <th className="p-3">Event Type</th>
                                        <th className="p-3">Description</th>
                                        <th className="p-3">Actor</th>
                                    </tr>
                                </thead>
                                <tbody id="table-audit-logs"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>





            {/* 3. CRM View */}
    </div>
  );
};

export default GovernanceView;
