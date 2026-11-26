import os

APP_JS_PATH = r"asperion_stack/app/static/js/app.js"

with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Replace loadHRMS() implementation
old_load_hrms_start = "// 5. HRMS\nasync function loadHRMS() {"
old_load_hrms_end = "async function loadSalaryStatements(cycle = \"JUN-2026\") {"

assert old_load_hrms_start in code, "Could not find loadHRMS start"
assert old_load_hrms_end in code, "Could not find loadSalaryStatements start"

new_load_hrms = '''// 5. HRMS & Human Capital Suite (Comprehensive Enterprise Controller)
let cachedHRMSEmployees = [];

async function loadHRMS() {
    try {
        const [
            resMetrics, resEmployees, resCandidates, resLetters,
            resLeaves, resSeparations, resPOSH
        ] = await Promise.all([
            fetch(`${API_BASE}/hrms/overview-metrics`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/hrms/employees`).then(r => r.json()),
            fetch(`${API_BASE}/hrms/candidates`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/hrms/letters`).then(r => r.json()),
            fetch(`${API_BASE}/hrms/leaves`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/hrms/separation-clearances`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/hrms/posh-cases`).then(r => r.json()).catch(() => [])
        ]);

        cachedHRMSEmployees = resEmployees;

        // 1. Populate Executive KPI Cards
        if (resMetrics) {
            const elHeadcount = document.getElementById('hrms-stat-headcount');
            if (elHeadcount) elHeadcount.innerText = `${resMetrics.active_headcount} Active`;

            const elGross = document.getElementById('hrms-stat-payroll-gross');
            if (elGross) elGross.innerText = formatINR(resMetrics.monthly_payroll_outflow);

            const elAnnual = document.getElementById('hrms-stat-payroll-annual');
            if (elAnnual) elAnnual.innerText = formatINR(resMetrics.annual_payroll_run_rate);

            const elStat = document.getElementById('hrms-stat-statutory-outflow');
            if (elStat) elStat.innerText = formatINR(resMetrics.statutory_pf_outflow_monthly + resMetrics.statutory_pt_outflow_monthly);

            const elCand = document.getElementById('hrms-stat-candidates');
            if (elCand) elCand.innerText = `${resMetrics.talent_pipeline_candidates} In Pipeline`;

            const elPosh = document.getElementById('hrms-stat-posh-compliance');
            if (elPosh) elPosh.innerText = `${resMetrics.posh_compliance_index_pct}% SLA`;
        }

        // 2. Populate Employees Directory Table
        renderHRMSEmployees(resEmployees);

        // 3. Populate Modal Employee Select Dropdowns
        const leaveEmpSelect = document.getElementById('leave-emp-id');
        const sepEmpSelect = document.getElementById('sep-emp-id');
        const empOptionsHtml = resEmployees.map(e => `
            <option value="${e.id}">${e.emp_code} - ${e.full_name} (${e.designation})</option>
        `).join('');
        if (leaveEmpSelect) leaveEmpSelect.innerHTML = empOptionsHtml;
        if (sepEmpSelect) sepEmpSelect.innerHTML = empOptionsHtml;

        // 4. Populate ATS Candidates Table
        const candTable = document.getElementById('table-hrms-candidates');
        if (candTable) {
            if (resCandidates.length === 0) {
                candTable.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-slate-400">No candidates currently in talent pipeline.</td></tr>`;
            } else {
                candTable.innerHTML = resCandidates.map(c => {
                    const isHired = c.stage === 'Hired';
                    const hireButton = isHired 
                        ? `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold"><i class="fa-solid fa-check mr-1"></i>Onboarded</span>`
                        : `<button onclick="handleHireCandidate(${c.id})" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-bold text-[11px] transition shadow flex items-center gap-1 mx-auto" title="Convert to Employee, Create Salary Structure & Issue Offer Letter">
                            <i class="fa-solid fa-user-check"></i> Hire & Offer
                           </button>`;

                    const stages = ['Applied', 'Screening', 'Technical Round', 'Founder Round', 'Offered', 'Hired'];
                    const stageDropdown = isHired 
                        ? `<span class="font-semibold text-emerald-700">${c.stage}</span>`
                        : `<select onchange="handleAdvanceCandidateStage(${c.id}, this.value)" class="text-[11px] border rounded px-1.5 py-0.5 bg-white font-medium text-slate-700">
                            ${stages.map(st => `<option value="${st}" ${st === c.stage ? 'selected' : ''}>${st}</option>`).join('')}
                           </select>`;

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${c.full_name}</div>
                                <div class="text-[11px] text-slate-400 font-mono">${c.email}</div>
                            </td>
                            <td class="p-3">
                                <div class="font-medium text-slate-800">${c.target_role}</div>
                                <div class="text-[10px] text-slate-500">${c.department}</div>
                            </td>
                            <td class="p-3 font-semibold text-slate-700">${c.total_experience_years} yrs</td>
                            <td class="p-3 font-mono font-bold text-slate-800">${formatINR(c.expected_ctc)}</td>
                            <td class="p-3 text-slate-600">${c.notice_period_days} days</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
                                    c.stage === 'Hired' ? 'bg-emerald-100 text-emerald-800' :
                                    c.stage === 'Offered' ? 'bg-purple-100 text-purple-800' :
                                    c.stage === 'Founder Round' ? 'bg-indigo-100 text-indigo-800' :
                                    c.stage === 'Technical Round' ? 'bg-blue-100 text-blue-800' :
                                    'bg-slate-100 text-slate-700'
                                }">${c.stage}</span>
                            </td>
                            <td class="p-3 text-center">${stageDropdown}</td>
                            <td class="p-3 text-center">${hireButton}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 5. Populate Leaves Table with Approve/Reject Actions
        const leaveTable = document.getElementById('table-leaves');
        if (leaveTable) {
            if (resLeaves.length === 0) {
                leaveTable.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-400">No leave applications registered.</td></tr>`;
            } else {
                leaveTable.innerHTML = resLeaves.map(lv => {
                    const isPending = lv.status === 'PENDING' || lv.status === 'Applied';
                    const actions = isPending ? `
                        <div class="flex items-center justify-center gap-1.5">
                            <button onclick="handleUpdateLeaveStatus(${lv.id}, 'APPROVED')" class="px-2 py-0.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-bold transition">
                                <i class="fa-solid fa-check"></i> Approve
                            </button>
                            <button onclick="handleUpdateLeaveStatus(${lv.id}, 'REJECTED')" class="px-2 py-0.5 bg-rose-600 hover:bg-rose-500 text-white rounded text-[10px] font-bold transition">
                                <i class="fa-solid fa-xmark"></i> Reject
                            </button>
                        </div>
                    ` : `<span class="text-[10px] text-slate-400 font-mono">Reviewed</span>`;

                    const badgeClass = lv.status === 'APPROVED' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                        lv.status === 'REJECTED' ? 'bg-rose-50 text-rose-700 border-rose-200' :
                        'bg-amber-50 text-amber-700 border-amber-200';

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3 font-semibold text-slate-800">${lv.employee_name}</td>
                            <td class="p-3 text-slate-600 font-medium">${lv.leave_type}</td>
                            <td class="p-3 font-mono font-bold text-slate-800">${lv.total_days} days</td>
                            <td class="p-3 text-slate-500">${formatDate(lv.start_date)} to ${formatDate(lv.end_date)}</td>
                            <td class="p-3 text-slate-600 max-w-xs truncate" title="${lv.reason}">${lv.reason}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badgeClass}">${lv.status}</span>
                            </td>
                            <td class="p-3 text-center">${actions}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 6. Populate Separation & F&F Clearances Table
        const sepTable = document.getElementById('table-hrms-separations');
        if (sepTable) {
            if (resSeparations.length === 0) {
                sepTable.innerHTML = `<tr><td colspan="9" class="p-4 text-center text-slate-400">No active employee separations or pending F&F clearances.</td></tr>`;
            } else {
                sepTable.innerHTML = resSeparations.map(s => {
                    const itStatus = s.it_assets_returned 
                        ? `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]"><i class="fa-solid fa-check mr-1"></i>Returned</span>`
                        : `<button onclick="handleUpdateSeparationClearance(${s.id}, 'it_assets_returned', true)" class="px-2 py-0.5 bg-slate-200 hover:bg-emerald-500 hover:text-white rounded text-[10px] font-bold transition">Mark Returned</button>`;

                    const finStatus = s.finance_no_dues 
                        ? `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]"><i class="fa-solid fa-check mr-1"></i>No Dues</span>`
                        : `<button onclick="handleUpdateSeparationClearance(${s.id}, 'finance_no_dues', true)" class="px-2 py-0.5 bg-slate-200 hover:bg-emerald-500 hover:text-white rounded text-[10px] font-bold transition">Mark Cleared</button>`;

                    const ktStatus = s.knowledge_transfer_complete 
                        ? `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]"><i class="fa-solid fa-check mr-1"></i>Complete</span>`
                        : `<button onclick="handleUpdateSeparationClearance(${s.id}, 'knowledge_transfer_complete', true)" class="px-2 py-0.5 bg-slate-200 hover:bg-emerald-500 hover:text-white rounded text-[10px] font-bold transition">Mark Done</button>`;

                    const isProcessed = s.status === 'PROCESSED';
                    const settleAction = isProcessed 
                        ? `<span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">F&F Settled</span>`
                        : `<button onclick="handleProcessFF(${s.id})" class="px-2.5 py-1 bg-purple-600 hover:bg-purple-500 text-white rounded font-bold text-[11px] transition shadow">
                            <i class="fa-solid fa-file-invoice-dollar mr-1"></i> Process F&F
                           </button>`;

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${s.employee_name}</div>
                                <div class="text-[10px] text-slate-400 font-mono">${s.employee_code || '-'}</div>
                            </td>
                            <td class="p-3 text-slate-600">${formatDate(s.resignation_date)}</td>
                            <td class="p-3 text-slate-800 font-semibold">${formatDate(s.last_working_day)}</td>
                            <td class="p-3">${itStatus}</td>
                            <td class="p-3">${finStatus}</td>
                            <td class="p-3">${ktStatus}</td>
                            <td class="p-3 text-right font-mono font-bold text-slate-900">${formatINR(s.settlement_amount_inr || 0)}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isProcessed ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${s.status}</span>
                            </td>
                            <td class="p-3 text-center">${settleAction}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 7. Populate Workplace Ethics & POSH Cases Table
        const poshTable = document.getElementById('table-hrms-posh');
        if (poshTable) {
            if (resPOSH.length === 0) {
                poshTable.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-slate-400">No workplace ethics or POSH cases logged. 100% compliance.</td></tr>`;
            } else {
                poshTable.innerHTML = resPOSH.map(p => {
                    const isConcluded = p.status === 'CONCLUDED';
                    const actionBtn = isConcluded 
                        ? `<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-600 text-[10px] font-semibold">Concluded</span>`
                        : `<button onclick="handleConcludePOSH(${p.id})" class="px-2.5 py-1 bg-rose-600 hover:bg-rose-500 text-white rounded text-[10px] font-bold transition shadow">
                            <i class="fa-solid fa-gavel mr-1"></i> Conclude Inquiry
                           </button>`;

                    const daysBadge = isConcluded 
                        ? `<span class="text-slate-400 text-[10px]">Inquiry Complete</span>`
                        : `<span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-mono font-bold text-[10px]">${p.statutory_inquiry_deadline_days_remaining} Days Left</span>`;

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3 font-mono font-bold text-rose-700">${p.case_number}</td>
                            <td class="p-3 font-semibold text-slate-800">${p.complainant_name}</td>
                            <td class="p-3 text-slate-700 font-medium">${p.accused_name}</td>
                            <td class="p-3 text-slate-500">${formatDate(p.incident_date)}</td>
                            <td class="p-3">${daysBadge}</td>
                            <td class="p-3 text-slate-600">${p.presiding_officer}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isConcluded ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">${p.status}</span>
                            </td>
                            <td class="p-3 text-center">${actionBtn}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 8. Populate Issued Letters Table
        const letterTable = document.getElementById('table-letters');
        if (letterTable) {
            letterTable.innerHTML = resLetters.map(l => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-mono text-xs text-purple-700 font-semibold">${l.letter_code}</td>
                    <td class="p-3 font-medium text-slate-800">${l.letter_title}</td>
                    <td class="p-3"><span class="px-2 py-0.5 text-[10px] font-bold rounded bg-slate-100 text-slate-700">${l.category}</span></td>
                    <td class="p-3 text-slate-700">${l.recipient_name}</td>
                    <td class="p-3 text-slate-500">${formatDate(l.issue_date)}</td>
                    <td class="p-3 text-center whitespace-nowrap">
                        <button onclick="previewLetterById(${l.id})" class="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition">Preview</button>
                        <a href="${API_BASE}/hrms/letters/${l.id}/docx" target="_blank" class="px-2 py-1 text-xs bg-indigo-600 hover:bg-indigo-700 text-white rounded transition ml-1 inline-flex items-center gap-1"><i class="fa-solid fa-file-word"></i> DOCX</a>
                    </td>
                </tr>
            `).join('');
        }

        // 9. Load auxiliary sub-modules
        populateLetterTemplateDropdown();
        loadSalaryStatements();
        loadSmartAttendance();
    } catch (err) {
        console.error('Error loading comprehensive HRMS:', err);
    }
}

function renderHRMSEmployees(employees) {
    const empTable = document.getElementById('table-employees');
    if (!empTable) return;
    if (employees.length === 0) {
        empTable.innerHTML = `<tr><td colspan="9" class="p-4 text-center text-slate-400">No employees found.</td></tr>`;
        return;
    }
    empTable.innerHTML = employees.map(e => `
        <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
            <td class="p-3 font-mono text-xs text-blue-700 font-bold">${e.emp_code}</td>
            <td class="p-3 font-semibold text-slate-900">${e.full_name} <br><span class="text-[11px] font-normal text-slate-400 font-mono">${e.official_email}</span></td>
            <td class="p-3 text-slate-700 font-medium">${e.designation}</td>
            <td class="p-3 text-slate-600">${e.department}</td>
            <td class="p-3 text-slate-500 font-mono">${formatDate(e.date_of_joining)}</td>
            <td class="p-3 font-mono font-bold text-slate-900">${formatINR(e.annual_ctc || 1200000)}</td>
            <td class="p-3 text-slate-500 font-mono text-[11px]">
                PAN: <span class="font-bold text-slate-700">${e.pan_number || '-'}</span><br>
                UAN: <span class="font-bold text-slate-700">${e.uan_number || '-'}</span>
            </td>
            <td class="p-3"><span class="px-2 py-0.5 text-[10px] rounded font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${e.employment_status}</span></td>
            <td class="p-3 text-center whitespace-nowrap">
                <button onclick="viewEmployeeProfile(${e.id})" class="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-bold transition flex items-center gap-1 mx-auto">
                    <i class="fa-solid fa-address-card"></i> Profile
                </button>
            </td>
        </tr>
    `).join('');
}

function filterHRMSEmployees(query) {
    if (!query) {
        renderHRMSEmployees(cachedHRMSEmployees);
        return;
    }
    const q = query.toLowerCase();
    const filtered = cachedHRMSEmployees.filter(e => 
        (e.full_name && e.full_name.toLowerCase().includes(q)) ||
        (e.emp_code && e.emp_code.toLowerCase().includes(q)) ||
        (e.designation && e.designation.toLowerCase().includes(q)) ||
        (e.department && e.department.toLowerCase().includes(q))
    );
    renderHRMSEmployees(filtered);
}

function switchHRMSTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.hrms-tab-content').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`hrms-subview-${tabId}`);
    if (target) target.classList.remove('hidden');

    // Update pill buttons
    document.querySelectorAll('.hrms-tab-pill').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white', 'shadow-sm');
        btn.classList.add('bg-slate-100', 'text-slate-700');
    });
    const activeBtn = document.getElementById(`hrms-btn-${tabId}`);
    if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('bg-blue-600', 'text-white', 'shadow-sm');
    }
}

function openHRMSModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('hidden');
}

function closeHRMSModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('hidden');
}

// Handler: Create Employee
async function handleCreateEmployee(e) {
    e.preventDefault();
    try {
        const body = {
            emp_code: document.getElementById('new-emp-code').value.trim(),
            full_name: document.getElementById('new-emp-name').value.trim(),
            official_email: document.getElementById('new-emp-email').value.trim(),
            phone_number: document.getElementById('new-emp-phone').value.trim() || null,
            designation: document.getElementById('new-emp-designation').value.trim(),
            department: document.getElementById('new-emp-dept').value,
            date_of_joining: document.getElementById('new-emp-doj').value,
            employment_status: "ACTIVE",
            annual_ctc: parseFloat(document.getElementById('new-emp-ctc').value) || 1200000,
            pan_number: document.getElementById('new-emp-pan').value.trim() || null,
            uan_number: document.getElementById('new-emp-uan').value.trim() || null,
            bank_account_number: document.getElementById('new-emp-bank-acc').value.trim() || null,
            bank_ifsc: document.getElementById('new-emp-bank-ifsc').value.trim() || null
        };

        const res = await fetch(`${API_BASE}/hrms/employees`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Employee successfully added to Asperion corporate roster!");
            closeHRMSModal('modal-hrms-employee');
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Error adding employee: " + (err.detail || "Validation failed"));
        }
    } catch (err) {
        alert("Error creating employee: " + err.message);
    }
}

// Handler: Create Candidate
async function handleCreateCandidate(e) {
    e.preventDefault();
    try {
        const body = {
            full_name: document.getElementById('cand-name').value.trim(),
            email: document.getElementById('cand-email').value.trim(),
            target_role: document.getElementById('cand-role').value.trim(),
            department: document.getElementById('cand-dept').value,
            total_experience_years: parseFloat(document.getElementById('cand-exp').value) || 0,
            expected_ctc: parseFloat(document.getElementById('cand-ctc').value) || 1200000,
            notice_period_days: parseInt(document.getElementById('cand-notice').value) || 30,
            current_company: document.getElementById('cand-company').value.trim() || null
        };

        const res = await fetch(`${API_BASE}/hrms/candidates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Candidate successfully added to talent pipeline!");
            closeHRMSModal('modal-hrms-candidate');
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Error adding candidate: " + (err.detail || "Validation failed"));
        }
    } catch (err) {
        alert("Error creating candidate: " + err.message);
    }
}

// Handler: Advance Candidate Stage
async function handleAdvanceCandidateStage(candidateId, newStage) {
    try {
        const res = await fetch(`${API_BASE}/hrms/candidates/${candidateId}/stage`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stage: newStage })
        });
        if (res.ok) {
            loadHRMS();
        } else {
            alert("Failed to advance candidate stage.");
        }
    } catch (err) {
        alert("Error advancing stage: " + err.message);
    }
}

// Handler: Hire Candidate (One-Click Conversion)
async function handleHireCandidate(candidateId) {
    if (!confirm("Are you sure you want to hire this candidate?\\nThis will convert them to an Active Employee, compute their statutory Wage Code salary structure, and automatically issue an official HR-ONB-01 Offer Letter with corporate branding.")) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/hrms/candidates/${candidateId}/hire`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                date_of_joining: "2026-06-01",
                basic_pct: 0.50,
                hra_pct: 0.50
            })
        });

        if (res.ok) {
            const data = await res.json();
            alert(`🎉 Candidate successfully hired!\\nNew Employee: ${data.full_name} (${data.emp_code})\\nOffer Letter Issued: Letter #${data.offer_letter_id}\\nOfficial Email: ${data.official_email}`);
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Failed to hire candidate: " + (err.detail || "Error occurred"));
        }
    } catch (err) {
        alert("Error hiring candidate: " + err.message);
    }
}

// Handler: Apply Leave
async function handleApplyLeave(e) {
    e.preventDefault();
    try {
        const empId = parseInt(document.getElementById('leave-emp-id').value);
        const startDate = document.getElementById('leave-start-date').value;
        const endDate = document.getElementById('leave-end-date').value;

        // Calculate days
        const d1 = new Date(startDate);
        const d2 = new Date(endDate);
        const diffTime = Math.abs(d2 - d1);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

        const body = {
            employee_id: empId,
            leave_type: document.getElementById('leave-type').value,
            start_date: startDate,
            end_date: endDate,
            total_days: diffDays,
            reason: document.getElementById('leave-reason').value.trim()
        };

        const res = await fetch(`${API_BASE}/hrms/leaves`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Leave request submitted successfully!");
            closeHRMSModal('modal-hrms-leave');
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Error submitting leave: " + (err.detail || "Validation failed"));
        }
    } catch (err) {
        alert("Error applying leave: " + err.message);
    }
}

// Handler: Update Leave Status (Approve / Reject)
async function handleUpdateLeaveStatus(leaveId, status) {
    try {
        const res = await fetch(`${API_BASE}/hrms/leaves/${leaveId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status })
        });
        if (res.ok) {
            alert(`Leave marked as ${status}.`);
            loadHRMS();
        } else {
            alert("Failed to update leave status.");
        }
    } catch (err) {
        alert("Error updating leave: " + err.message);
    }
}

// Handler: Initiate Separation
async function handleInitiateSeparation(e) {
    e.preventDefault();
    try {
        const body = {
            employee_id: parseInt(document.getElementById('sep-emp-id').value),
            resignation_date: document.getElementById('sep-resig-date').value,
            last_working_day: document.getElementById('sep-lwd-date').value,
            reason: document.getElementById('sep-reason').value.trim() || "Voluntary Resignation",
            separation_type: document.getElementById('sep-type').value
        };

        const res = await fetch(`${API_BASE}/hrms/separations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Separation workflow initiated with multi-department clearance checklist!");
            closeHRMSModal('modal-hrms-separation');
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Error initiating separation: " + (err.detail || "Validation failed"));
        }
    } catch (err) {
        alert("Error initiating separation: " + err.message);
    }
}

// Handler: Update Separation Clearance
async function handleUpdateSeparationClearance(separationId, field, value) {
    try {
        const payload = {};
        payload[field] = value;
        const res = await fetch(`${API_BASE}/hrms/separations/${separationId}/clearance`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            loadHRMS();
        } else {
            alert("Failed to update clearance status.");
        }
    } catch (err) {
        alert("Error updating clearance: " + err.message);
    }
}

// Handler: Process F&F
async function handleProcessFF(separationId) {
    if (!confirm("Confirm Full & Final (F&F) Settlement processing?\\nThis will verify no-dues, compute encashments, and finalize relieving status.")) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/hrms/separations/${separationId}/clearance`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: "PROCESSED",
                it_assets_returned: true,
                finance_no_dues: true,
                knowledge_transfer_complete: true
            })
        });
        if (res.ok) {
            alert("✅ Full & Final Settlement marked as PROCESSED! Relieving letter can now be generated.");
            loadHRMS();
        } else {
            alert("Failed to process F&F.");
        }
    } catch (err) {
        alert("Error processing F&F: " + err.message);
    }
}

// Handler: Create POSH Case
async function handleCreatePOSHCase(e) {
    e.preventDefault();
    try {
        const body = {
            complainant_name: document.getElementById('posh-complainant').value.trim(),
            accused_name: document.getElementById('posh-accused').value.trim(),
            incident_date: document.getElementById('posh-date').value,
            incident_location: document.getElementById('posh-loc').value.trim() || "Headquarters",
            allegation_summary: document.getElementById('posh-desc').value.trim()
        };

        const res = await fetch(`${API_BASE}/hrms/posh-cases`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ Confidential POSH complaint lodged under Case ID [${data.case_number}]!\\nInternal Committee notified. Statutory 90-day inquiry clock initiated.`);
            closeHRMSModal('modal-hrms-posh');
            loadHRMS();
        } else {
            const err = await res.json();
            alert("Error lodging POSH complaint: " + (err.detail || "Validation failed"));
        }
    } catch (err) {
        alert("Error creating POSH case: " + err.message);
    }
}

// Handler: Conclude POSH Case
async function handleConcludePOSH(caseId) {
    const outcome = prompt("Enter Internal Committee Inquiry Outcome Summary:", "Inquiry completed per POSH Act 2013 rules with formal ICC recommendations.");
    if (!outcome) return;

    try {
        const res = await fetch(`${API_BASE}/hrms/posh-cases/${caseId}/conclude`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                outcome_summary: outcome,
                action_taken: "Formal recommendation recorded and compliance documented."
            })
        });

        if (res.ok) {
            alert("✅ POSH inquiry concluded and formal closure record sealed.");
            loadHRMS();
        } else {
            alert("Failed to conclude POSH inquiry.");
        }
    } catch (err) {
        alert("Error concluding POSH case: " + err.message);
    }
}

// Handler: View 360-Degree Employee Profile
async function viewEmployeeProfile(empId) {
    try {
        const res = await fetch(`${API_BASE}/hrms/employees/${empId}/profile`);
        if (!res.ok) throw new Error("Failed to load employee profile");
        const p = await res.json();
        const e = p.employee;
        const sal = p.salary_structure;

        document.getElementById('profile-emp-name').innerText = e.full_name;
        document.getElementById('profile-emp-role').innerText = `${e.designation} | ${e.department} (${e.emp_code})`;

        const modalBody = document.getElementById('profile-modal-body');
        modalBody.innerHTML = `
            <div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Official Email</span>
                    <span class="font-bold text-slate-800 font-mono text-xs">${e.official_email}</span>
                </div>
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Date of Joining</span>
                    <span class="font-bold text-slate-800">${formatDate(e.date_of_joining)}</span>
                </div>
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Statutory Identifiers</span>
                    <span class="text-slate-700">PAN: <strong class="font-mono text-slate-900">${e.pan_number || '-'}</strong> | UAN: <strong class="font-mono text-slate-900">${e.uan_number || '-'}</strong></span>
                </div>
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Bank Account & IFSC</span>
                    <span class="text-slate-700"><strong class="font-mono">${e.bank_account_number || '-'}</strong> (${e.bank_ifsc || '-'})</span>
                </div>
            </div>

            <!-- Wage Code Salary Structure Card -->
            <div class="p-3 bg-blue-50/50 rounded-xl border border-blue-200">
                <div class="flex justify-between items-center mb-2 pb-1.5 border-b border-blue-200">
                    <span class="font-bold text-blue-950 text-xs flex items-center gap-1.5">
                        <i class="fa-solid fa-calculator text-blue-600"></i> Wage Code 2019 Statutory Compensation
                    </span>
                    <span class="font-mono font-bold text-xs text-blue-900">Annual CTC: ${formatINR(sal.annual_ctc)}</span>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                    <div>Basic: <strong class="text-slate-900 font-mono">${formatINR(sal.monthly_basic)}/m</strong></div>
                    <div>HRA: <strong class="text-slate-900 font-mono">${formatINR(sal.monthly_hra)}/m</strong></div>
                    <div>Special: <strong class="text-slate-900 font-mono">${formatINR(sal.monthly_special_allowance)}/m</strong></div>
                    <div>Monthly Gross: <strong class="text-emerald-700 font-mono font-bold">${formatINR(sal.monthly_gross)}/m</strong></div>
                    <div>EPFO PF (12%): <strong class="text-rose-700 font-mono">${formatINR(sal.monthly_employee_pf)}/m</strong></div>
                    <div>Karnataka PT: <strong class="text-purple-700 font-mono font-bold">₹200/m</strong></div>
                    <div>Net Take-Home: <strong class="text-emerald-600 font-mono font-bold">${formatINR(sal.monthly_net_take_home)}/m</strong></div>
                    <div>Annual In-Hand: <strong class="text-emerald-600 font-mono font-bold">${formatINR(sal.annual_net_take_home)}</strong></div>
                </div>
            </div>

            <!-- Leave Balances -->
            <div class="p-3 bg-amber-50/50 rounded-xl border border-amber-200">
                <span class="font-bold text-amber-950 text-xs block mb-2 flex items-center gap-1.5">
                    <i class="fa-solid fa-calendar-check text-amber-600"></i> Leave Balances (Annual Entitlement)
                </span>
                <div class="grid grid-cols-4 gap-2 text-center text-[11px]">
                    <div class="p-2 bg-white rounded-lg border border-amber-200">
                        <span class="text-slate-400 block text-[10px]">Casual (CL)</span>
                        <strong class="text-slate-900 font-bold">${p.leave_balances.casual_leave_remaining} / 12</strong>
                    </div>
                    <div class="p-2 bg-white rounded-lg border border-amber-200">
                        <span class="text-slate-400 block text-[10px]">Sick (SL)</span>
                        <strong class="text-slate-900 font-bold">${p.leave_balances.sick_leave_remaining} / 12</strong>
                    </div>
                    <div class="p-2 bg-white rounded-lg border border-amber-200">
                        <span class="text-slate-400 block text-[10px]">Earned (EL)</span>
                        <strong class="text-slate-900 font-bold">${p.leave_balances.earned_leave_remaining} / 15</strong>
                    </div>
                    <div class="p-2 bg-white rounded-lg border border-amber-200">
                        <span class="text-slate-400 block text-[10px]">Leaves Taken</span>
                        <strong class="text-blue-700 font-bold">${p.leave_balances.total_leaves_taken} days</strong>
                    </div>
                </div>
            </div>

            <!-- Issued Letters -->
            <div class="p-3 bg-purple-50/50 rounded-xl border border-purple-200">
                <span class="font-bold text-purple-950 text-xs block mb-2 flex items-center gap-1.5">
                    <i class="fa-solid fa-envelopes-bulk text-purple-600"></i> Issued Corporate Letters (${p.issued_letters.length})
                </span>
                <div class="space-y-1.5 max-h-36 overflow-y-auto">
                    ${p.issued_letters.length === 0 ? '<span class="text-slate-400 text-[11px]">No letters issued yet.</span>' :
                        p.issued_letters.map(l => `
                            <div class="flex items-center justify-between p-1.5 bg-white rounded border border-purple-100 text-[11px]">
                                <div>
                                    <span class="font-mono text-purple-700 font-bold mr-1">[${l.letter_code}]</span>
                                    <span class="font-medium text-slate-800">${l.letter_title}</span>
                                </div>
                                <div class="flex items-center gap-1">
                                    <button onclick="previewLetterById(${l.id})" class="px-2 py-0.5 bg-blue-600 text-white rounded text-[10px]">HTML</button>
                                    <a href="${API_BASE}/hrms/letters/${l.id}/docx" target="_blank" class="px-2 py-0.5 bg-indigo-600 text-white rounded text-[10px]">DOCX</a>
                                </div>
                            </div>
                        `).join('')
                    }
                </div>
            </div>
        `;

        openHRMSModal('modal-hrms-profile');
    } catch (err) {
        alert("Error loading employee profile: " + err.message);
    }
}

'''

idx_start = code.find(old_load_hrms_start)
idx_end = code.find(old_load_hrms_end)

new_code = code[:idx_start] + new_load_hrms + code[idx_end:]

with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(new_code)

print("Successfully updated app.js with comprehensive HRMS suite functions!")
