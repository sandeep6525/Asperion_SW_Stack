// @ts-ignore
import { loadFinance } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const FinanceView: React.FC = () => {
  useEffect(() => {
    try {
      loadFinance();
    } catch (e) {
      console.error('Error in loadFinance:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-finance" className="module-view ">
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-slate-900">Finance, Invoicing, Tax & AP/AR</h2>
                    <p className="text-sm text-slate-500">Accounts Receivable (GST bifurcated), Accounts Payable (with TDS deduction), 13-Week Cashflow, and Chart of Accounts.</p>
                </div>

                {/* 13-Week Cashflow Forecast Widget */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2">
                            <i className="fa-solid fa-chart-line text-blue-600"></i> 13-Week Direct Cash Flow Forecast
                        </h3>
                        <div className="flex gap-4 text-xs font-semibold">
                            <span className="text-slate-500">Closing Cash: <strong id="cf-closing-val" className="text-emerald-700 font-bold">-</strong></span>
                            <span className="text-slate-500">Estimated Runway: <strong id="cf-runway-val" className="text-blue-700 font-bold">-</strong></span>
                        </div>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-xs">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                                <tr>
                                    <th className="p-2.5">Forecast Period</th>
                                    <th className="p-2.5 text-right">Opening Cash</th>
                                    <th className="p-2.5 text-right">Inflows (Collections)</th>
                                    <th className="p-2.5 text-right">Payroll Outflow</th>
                                    <th className="p-2.5 text-right">Vendor Outflow</th>
                                    <th className="p-2.5 text-right">Statutory Taxes</th>
                                    <th className="p-2.5 text-right">Closing Cash</th>
                                </tr>
                            </thead>
                            <tbody id="table-cashflow-13wk"></tbody>
                        </table>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-6 mb-6">
                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-receipt text-emerald-600"></i> Invoices Register (Accounts Receivable - AR)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Invoice No</th>
                                        <th className="p-3">Customer</th>
                                        <th className="p-3">Date</th>
                                        <th className="p-3">Taxable Value</th>
                                        <th className="p-3">GST Total</th>
                                        <th className="p-3">Gross Total</th>
                                        <th className="p-3">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="table-invoices"></tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-file-invoice text-rose-600"></i> Vendor Bills & TDS Control (Accounts Payable - AP)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Bill No</th>
                                        <th className="p-3">Vendor</th>
                                        <th className="p-3">Taxable Amount</th>
                                        <th className="p-3">TDS Deducted</th>
                                        <th className="p-3">Net Payable</th>
                                        <th className="p-3">3-Way Match</th>
                                        <th className="p-3">Approval</th>
                                    </tr>
                                </thead>
                                <tbody id="table-ap-bills"></tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                            <i className="fa-solid fa-list-ol text-blue-600"></i> Chart of Accounts (COA)
                        </h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm">
                                <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                    <tr>
                                        <th className="p-3">Account Code</th>
                                        <th className="p-3">Account Name</th>
                                        <th className="p-3">Group</th>
                                        <th className="p-3">Normal Balance</th>
                                        <th className="p-3">Cost Center</th>
                                    </tr>
                                </thead>
                                <tbody id="table-coa"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>





            {/* 5. HRMS & Workforce Governance Portal */}
    </div>
  );
};

export default FinanceView;
