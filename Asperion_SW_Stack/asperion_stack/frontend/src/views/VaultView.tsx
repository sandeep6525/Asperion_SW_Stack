// @ts-ignore
import { loadVault } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const VaultView: React.FC = () => {
  useEffect(() => {
    try {
      loadVault();
    } catch (e) {
      console.error('Error in loadVault:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-vault" className="module-view ">
                <div className="mb-6 flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
                            <i className="fa-solid fa-folder-tree text-amber-500"></i> Enterprise Knowledge & Document Vault
                        </h2>
                        <p className="text-sm text-slate-500">260+ authentic operational handbooks, SOPs, legal templates, founder strategy packs, and 65+ HR letter templates.</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <span id="vault-total-badge" className="px-3 py-1 bg-amber-100 text-amber-800 font-bold text-xs rounded-full border border-amber-200">260+ Documents Indexed</span>
                    </div>
                </div>

                {/* Category Filters & Search */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mb-6">
                    <div className="flex flex-col md:flex-row gap-4 justify-between items-center mb-4">
                        <div className="relative w-full md:w-96">
                            <i className="fa-solid fa-magnifying-glass absolute left-3 top-3 text-slate-400 text-sm"></i>
                            <input id="vault-search-input" onInput={() => {}} type="text" placeholder="Search templates, SOPs, policies, letters..." className="w-full pl-9 pr-4 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500" />
                        </div>
                        <div className="flex items-center gap-2 text-xs">
                            <span className="text-slate-500">Filter Format:</span>
                            <button onClick={() => {}} className="format-filter-btn px-2.5 py-1 rounded bg-slate-800 text-white font-medium" data-fmt="">All</button>
                            <button onClick={() => {}} className="format-filter-btn px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200" data-fmt="docx">DOCX</button>
                            <button onClick={() => {}} className="format-filter-btn px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200" data-fmt="pdf">PDF</button>
                            <button onClick={() => {}} className="format-filter-btn px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200" data-fmt="xlsx">XLSX</button>
                        </div>
                    </div>

                    {/* Category Pills */}
                    <div id="vault-category-pills" className="flex flex-wrap gap-2 text-xs"></div>
                </div>

                {/* Documents Table */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2">
                            <i className="fa-solid fa-file-lines text-blue-600"></i> Corporate Documents & Template Repository
                        </h3>
                        <span id="vault-showing-count" className="text-xs text-slate-500">Showing all documents</span>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs border-b">
                                <tr>
                                    <th className="p-3">Category</th>
                                    <th className="p-3">Document Title / File Name</th>
                                    <th className="p-3">Format</th>
                                    <th className="p-3">File Size</th>
                                    <th className="p-3 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="table-vault-docs"></tbody>
                        </table>
                    </div>
                </div>
            </section>





            {/* 11. Strategy, Functions, KPIs & Executive Thoughts View */}
    </div>
  );
};

export default VaultView;
