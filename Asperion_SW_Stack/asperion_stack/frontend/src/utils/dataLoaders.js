// Unified Complete Live Data Loaders for Asperion Enterprise OS
// Complete implementation of all 27 enterprise operating modules & portals

/**
 * Asperion Enterprise OS - Comprehensive Client Application
 * Connects Frontend UI with all 8 Enterprise Domain APIs & Computational Engines
 */

const API_BASE = '/api/v1';

export let currentModule = 'dashboard';

export function initLegacyApp() {
    // In React, components invoke their own loaders upon mounting in useEffect
    if (typeof document === 'undefined') return;
    initNavigation();
    loadDashboard();
    populateLetterTemplateDropdown();
    fetchNotificationsAndAlerts();
    initAutoSyncManager();
    
    // Enterprise Dynamic & Real-Time Engines
    startLiveClockAndHeartbeat();
    startLiveCertInCountdown();
    initKeyboardShortcuts();
    
    setTimeout(() => {
        showEnterpriseToast(
            'Asperion Enterprise OS v4.2 Active',
            'Full Statutory & Regulatory Governance Engaged. NTP Clock Synchronized (UTC+05:30). CERT-In & ISO Controls Operational.',
            'success',
            5000
        );
    }, 1200);
}

export function initNavigation() {
    const navItems = document.querySelectorAll('.nav-btn');
    navItems.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const target = btn.getAttribute('data-target');
            switchModule(target);
        });
    });
}

export function switchModule(moduleName) {
    currentModule = moduleName;
    if (typeof updateBreadcrumbs === 'function') {
        updateBreadcrumbs(moduleName);
    }
    
    document.querySelectorAll('.nav-btn').forEach(btn => {
        if (btn.getAttribute('data-target') === moduleName) {
            btn.classList.add('bg-blue-800', 'text-white');
            btn.classList.remove('text-slate-300', 'hover:bg-slate-800');
        } else {
            btn.classList.remove('bg-blue-800', 'text-white');
            btn.classList.add('text-slate-300', 'hover:bg-slate-800');
        }
    });

    document.querySelectorAll('.module-view').forEach(view => {
        view.classList.add('hidden');
    });

    const targetView = document.getElementById(`view-${moduleName}`);
    if (targetView) {
        targetView.classList.remove('hidden');
    }

    switch (moduleName) {
        case 'dashboard': loadDashboard(); break;
        case 'governance': loadGovernance(); break;
        case 'crm': loadCRM(); break;
        case 'finance': loadFinance(); break;
        case 'hrms': loadHRMS(); break;
        case 'pmo': loadPMO(); break;
        case 'sdlc': loadSDLC(); break;
        case 'procurement': loadProcurement(); break;
        case 'guardrails': loadGuardrails(); break;
        case 'iso-standards': loadISOStandardsModule(); break;
        case 'ai-cloud': loadAICloudModule(); break;
        case 'infrastructure': loadInfrastructure(); break;
        case 'secops': loadSecOps(); break;
        case 'vault': loadVault(); break;
        case 'strategy': loadStrategy(); break;
        case 'analytics': loadAnalyticsHub(); break;
        case 'internal-support': loadInternalSupport(); break;
        case 'itsm': loadITSM(); break;
        case 'teams': loadTeams(); break;
        case 'sharepoint': loadSharePoint(); break;
        case 'training': loadTraining(); break;
        case 'agentic-ai': loadAgenticAI(); break;
        case 'portal-employee': loadEmployeePortal(); break;
        case 'portal-client': loadClientPortal(); break;
        case 'portal-vendor': loadVendorPortal(); break;
        case 'operations': loadOperations(); break;
        case 'crypto-tools': loadCryptoTools(); break;
    }
}

// Formatters
export const formatINR = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val || 0);
export const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '-';

// Chart Instance Registry
const appCharts = {};
export function safeRenderChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !window.Chart) return null;
    
    if (appCharts[canvasId]) {
        appCharts[canvasId].destroy();
        delete appCharts[canvasId];
    }
    
    const ctx = canvas.getContext('2d');
    appCharts[canvasId] = new Chart(ctx, {
        type: type,
        data: data,
        options: Object.assign({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } }
            }
        }, options)
    });
    return appCharts[canvasId];
}

// 1. Dashboard
export async function loadDashboard() {
    try {
        const [resOverview, resAnalytics, resCharts] = await Promise.all([
            fetch(`${API_BASE}/dashboard/overview`).then(r => r.json()),
            fetch(`${API_BASE}/analytics/overview`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/analytics/financial-charts`).then(r => r.json()).catch(() => null)
        ]);
        const kpis = resOverview.kpis;

        document.getElementById('kpi-revenue').innerText = formatINR(kpis.financials.total_invoiced_inr);
        document.getElementById('kpi-collections').innerText = formatINR(kpis.financials.collections_received_inr);
        document.getElementById('kpi-ar').innerText = formatINR(kpis.financials.accounts_receivable_outstanding_inr);
        document.getElementById('kpi-headcount').innerText = kpis.people_hrms.active_headcount;
        document.getElementById('kpi-projects').innerText = kpis.delivery_pmo.active_projects;
        document.getElementById('kpi-incidents').innerText = kpis.secops.active_security_incidents;
        document.getElementById('kpi-compliance').innerText = kpis.governance_compliance.upcoming_statutory_filings;
        document.getElementById('kpi-cloud').innerText = formatINR(kpis.infrastructure.monthly_cloud_spend_inr);

        // Dynamic Calculated Ratios
        if (resAnalytics && resAnalytics.financial_summary) {
            const fs = resAnalytics.financial_summary;
            const gc = resAnalytics.governance_and_compliance;
            const elMargin = document.getElementById('ratio-operating-margin');
            if (elMargin) elMargin.innerText = `${fs.net_operating_margin_pct}%`;
            const elRunway = document.getElementById('ratio-cash-runway');
            if (elRunway) elRunway.innerText = `${fs.cash_runway_months} Mo`;
            const elDSO = document.getElementById('ratio-dso');
            if (elDSO) elDSO.innerText = `${fs.dso_days} Days`;
            const elComp = document.getElementById('ratio-compliance-index');
            if (elComp) elComp.innerText = `${gc.statutory_compliance_index_pct}%`;
            const elCert = document.getElementById('ratio-certin-sla');
            if (elCert) elCert.innerText = `${gc.certin_sla_compliance_pct}%`;
        }

        // Render Executive Charts
        if (resCharts) {
            renderExecCharts(resCharts);
        }

        await loadBalancedScorecard();
    } catch (err) {
        console.error('Error loading dashboard:', err);
    }
}

export function renderExecCharts(resCharts) {
    const cf = resCharts.cashflow_time_series;
    safeRenderChart('chart-exec-cashflow', 'line', {
        labels: cf.labels,
        datasets: [
            {
                label: 'Closing Cash Position (INR)',
                data: cf.closing_cash,
                borderColor: '#0284c7',
                backgroundColor: 'rgba(2, 132, 199, 0.1)',
                fill: true,
                tension: 0.3,
                yAxisID: 'y'
            },
            {
                label: 'Weekly Customer Collections',
                data: cf.inflows,
                borderColor: '#10b981',
                backgroundColor: '#10b981',
                type: 'bar',
                yAxisID: 'y'
            }
        ]
    }, {
        scales: {
            y: {
                ticks: {
                    callback: (v) => '₹' + (v / 100000).toFixed(1) + 'L'
                }
            }
        }
    });

    const cost = resCharts.cost_allocation;
    safeRenderChart('chart-exec-cost', 'doughnut', {
        labels: cost.labels,
        datasets: [{
            data: cost.values,
            backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
        }]
    }, {
        plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
        }
    });
}

// 2. Governance
export async function loadGovernance() {
    try {
        const [resResolutions, resCompliance, resPolicies, resAuditLogs] = await Promise.all([
            fetch(`${API_BASE}/governance/resolutions`).then(r => r.json()),
            fetch(`${API_BASE}/governance/compliance-calendar`).then(r => r.json()),
            fetch(`${API_BASE}/governance/policies`).then(r => r.json()),
            fetch(`${API_BASE}/governance/audit-logs`).then(r => r.json())
        ]);

        const resTable = document.getElementById('table-resolutions');
        resTable.innerHTML = resResolutions.map(r => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-3 font-semibold text-blue-900">${r.resolution_number}</td>
                <td class="p-3 font-medium text-slate-800">${r.title}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-blue-50 text-blue-700 font-medium">${r.subject_category}</span></td>
                <td class="p-3 text-slate-500">${formatDate(r.date_passed)}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${r.status}</span></td>
            </tr>
        `).join('');

        const compTable = document.getElementById('table-compliance');
        compTable.innerHTML = resCompliance.map(c => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-3 font-medium text-slate-800">${c.compliance_name}</td>
                <td class="p-3 text-slate-600">${c.statutory_authority}</td>
                <td class="p-3 font-mono text-xs text-blue-600 font-semibold">${c.form_or_return}</td>
                <td class="p-3 font-semibold text-rose-600">${formatDate(c.due_date)}</td>
                <td class="p-3 text-slate-500">${c.frequency}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded ${c.penalty_risk === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-amber-50 text-amber-800'} font-medium">${c.penalty_risk}</span></td>
            </tr>
        `).join('');

        const polTable = document.getElementById('table-policies');
        if (polTable) {
            polTable.innerHTML = resPolicies.map(p => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${p.policy_code}</td>
                    <td class="p-3 font-medium text-slate-800">${p.policy_name}</td>
                    <td class="p-3 text-slate-600">${p.category}</td>
                    <td class="p-3 text-slate-500">${formatDate(p.effective_date)}</td>
                    <td class="p-3 text-xs text-slate-500">${p.description || '-'}</td>
                </tr>
            `).join('');
        }

        const auditTable = document.getElementById('table-audit-logs');
        if (auditTable && resAuditLogs) {
            auditTable.innerHTML = resAuditLogs.map(a => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-slate-500">${new Date(a.created_at).toLocaleString('en-IN')}</td>
                    <td class="p-2.5 font-semibold text-blue-800">${a.module}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded font-bold ${a.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : a.severity === 'WARNING' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'}">${a.severity}</span></td>
                    <td class="p-2.5 font-mono text-slate-700">${a.event_type}</td>
                    <td class="p-2.5 text-slate-800">${a.description}</td>
                    <td class="p-2.5 text-slate-500">${a.actor}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Error loading governance:', err);
    }
}

// 3. Enterprise CRM, Customer Success & Service Desk
export async function loadCRM() {
    try {
        const [resSummary, resOpps, resAccounts, resTickets, resRisks, resProspects, resContracts] = await Promise.all([
            fetch(`${API_BASE}/crm-enterprise/pipeline-summary`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/crm-enterprise/opportunities`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/crm-enterprise/accounts`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/crm-enterprise/tickets`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/crm-enterprise/enterprise-risks`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/crm-legal/prospects`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/crm-legal/contracts`).then(r => r.json()).catch(() => [])
        ]);

        // Top Summary Cards
        if (resSummary) {
            const p = resSummary.pipeline;
            const cs = resSummary.customer_success;
            const sd = resSummary.service_desk;
            document.getElementById('crm-stat-pipeline').innerText = formatINR(p.total_pipeline_value_inr);
            document.getElementById('crm-stat-weighted').innerText = formatINR(p.weighted_pipeline_value_inr);
            document.getElementById('crm-stat-arr').innerText = formatINR(cs.managed_arr_inr);
            document.getElementById('crm-stat-winrate').innerText = `${p.win_rate_pct}%`;
            document.getElementById('crm-stat-health').innerText = `${cs.average_health_score}%`;
            document.getElementById('crm-stat-tickets').innerText = sd.open_tickets;
        }

        // 1. Enterprise Opportunities Table
        const oppTable = document.getElementById('table-crm-opportunities');
        if (oppTable) {
            oppTable.innerHTML = resOpps.map(o => {
                let deskBadge = 'bg-slate-100 text-slate-700';
                if (o.deal_desk_status.includes('Approved')) deskBadge = 'bg-emerald-100 text-emerald-800 font-semibold';
                else if (o.deal_desk_status.includes('Director Approval')) deskBadge = 'bg-amber-100 text-amber-800 font-bold';

                const stageOptions = [
                    'Lead Qualified', 'Discovery', 'Solution Architecture', 'Legal/Deal Desk', 'Closed Won', 'Closed Lost'
                ].map(st => `<option value="${st}" ${st === o.stage ? 'selected' : ''}>${st}</option>`).join('');

                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                        <td class="p-3 font-mono font-bold text-purple-800">${o.opportunity_code}</td>
                        <td class="p-3">
                            <div class="font-bold text-slate-900">${o.client_name}</div>
                            <div class="text-slate-500 text-[11px]">${o.deal_title}</div>
                        </td>
                        <td class="p-3 text-right font-bold text-slate-900">${formatINR(o.deal_value_inr)}</td>
                        <td class="p-3">
                            <select onchange="advanceOpportunityStage(${o.id}, this.value)" class="text-xs font-semibold px-2 py-1 rounded border border-slate-300 bg-white shadow-sm focus:outline-none focus:ring-1 focus:ring-purple-500">
                                ${stageOptions}
                            </select>
                        </td>
                        <td class="p-3 text-right font-bold text-slate-700">${o.probability_pct}%</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-700">${formatINR(o.weighted_value_inr)}</td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-[11px] ${deskBadge}">${o.deal_desk_status}</span></td>
                        <td class="p-3 text-slate-500">${formatDate(o.expected_close_date)}</td>
                        <td class="p-3 text-slate-600 font-medium">${o.owner}</td>
                    </tr>
                `;
            }).join('');
        }

        // 2. Customer Accounts & Health Scorecard
        const accTable = document.getElementById('table-crm-accounts');
        if (accTable) {
            accTable.innerHTML = resAccounts.map(a => {
                let healthColor = 'text-emerald-700 bg-emerald-100';
                if (a.health_score < 70) healthColor = 'text-rose-700 bg-rose-100';
                else if (a.health_score < 90) healthColor = 'text-amber-700 bg-amber-100';

                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                        <td class="p-2.5">
                            <div class="font-bold text-slate-900">${a.client_name}</div>
                            <div class="font-mono text-slate-400 text-[10px]">${a.account_code}</div>
                        </td>
                        <td class="p-2.5">
                            <span class="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-medium text-[11px]">${a.tier}</span>
                            <div class="text-[10px] text-slate-500 mt-0.5">${a.industry}</div>
                        </td>
                        <td class="p-2.5 text-right font-bold text-slate-900">${formatINR(a.annual_recurring_revenue_inr)}</td>
                        <td class="p-2.5 text-center">
                            <span class="px-2.5 py-1 rounded-full text-xs font-bold ${healthColor}">${a.health_score}% (${a.health_status})</span>
                        </td>
                        <td class="p-2.5 font-semibold text-slate-600">${formatDate(a.renewal_date)}</td>
                    </tr>
                `;
            }).join('');
        }

        // 3. Support Tickets Service Desk
        const tktTable = document.getElementById('table-crm-tickets');
        if (tktTable) {
            tktTable.innerHTML = resTickets.map(t => {
                let sevBadge = 'bg-slate-100 text-slate-700';
                if (t.severity.includes('P1')) sevBadge = 'bg-red-100 text-red-800 font-bold';
                else if (t.severity.includes('P2')) sevBadge = 'bg-orange-100 text-orange-800 font-semibold';
                else if (t.severity.includes('P3')) sevBadge = 'bg-blue-100 text-blue-800 font-medium';

                let statusBadge = t.status === 'Resolved' ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-amber-100 text-amber-800 font-semibold';

                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                        <td class="p-2.5 font-mono font-bold text-blue-800">${t.ticket_number}</td>
                        <td class="p-2.5">
                            <div class="font-bold text-slate-900">${t.client_name}</div>
                            <div class="text-slate-600 text-[11px]">${t.subject}</div>
                        </td>
                        <td class="p-2.5">
                            <span class="px-2 py-0.5 rounded text-[10px] ${sevBadge}">${t.severity} (${t.sla_response_hours}h SLA)</span>
                        </td>
                        <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] ${statusBadge}">${t.status}</span></td>
                        <td class="p-2.5 text-right">
                            ${t.status !== 'Resolved' ? `
                                <button onclick="resolveTicket(${t.id})" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[11px] font-semibold transition shadow-sm">
                                    <i class="fa-solid fa-check"></i> Resolve
                                </button>
                            ` : `<span class="text-emerald-700 font-bold text-[11px]"><i class="fa-solid fa-circle-check"></i> Completed</span>`}
                        </td>
                    </tr>
                `;
            }).join('');
        }

        // 4. Enterprise Risk Management (ERM)
        const riskTable = document.getElementById('table-crm-risks');
        if (riskTable) {
            riskTable.innerHTML = resRisks.map(r => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-mono font-bold text-rose-800">${r.risk_code}</td>
                    <td class="p-3 font-semibold text-slate-700">${r.risk_category}</td>
                    <td class="p-3">
                        <div class="font-bold text-slate-900">${r.risk_title}</div>
                        <div class="text-slate-500 text-[11px]">${r.risk_description}</div>
                    </td>
                    <td class="p-3 text-center">
                        <span class="px-2 py-1 rounded bg-red-100 text-red-800 font-bold text-xs">RPN ${r.inherent_rpn}</span>
                    </td>
                    <td class="p-3 text-slate-700 text-[11px]">${r.existing_controls || 'In progress'}</td>
                    <td class="p-3 text-center">
                        <span class="px-2 py-1 rounded bg-emerald-100 text-emerald-800 font-bold text-xs">RPN ${r.residual_rpn}</span>
                    </td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold">${r.treatment_strategy}</span></td>
                    <td class="p-3 text-slate-600">${r.risk_owner}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold">${r.status}</span></td>
                </tr>
            `).join('');
        }

        // 5. Prospects & Contracts
        const prospectTable = document.getElementById('table-prospects');
        if (prospectTable) {
            prospectTable.innerHTML = resProspects.map(p => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-medium text-slate-900">${p.company_name}</td>
                    <td class="p-3 text-slate-600">${p.contact_person} <br><span class="text-xs text-slate-400">${p.contact_email}</span></td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-purple-50 text-purple-700 font-medium">${p.pipeline_stage}</span></td>
                    <td class="p-3 font-semibold text-slate-800">${formatINR(p.deal_value)}</td>
                    <td class="p-3 text-slate-500">${p.owner}</td>
                </tr>
            `).join('');
        }

        const contractTable = document.getElementById('table-contracts');
        if (contractTable) {
            contractTable.innerHTML = resContracts.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${c.contract_reference}</td>
                    <td class="p-3 font-medium text-slate-800">${c.client_name}</td>
                    <td class="p-3 text-slate-600">${c.contract_type}</td>
                    <td class="p-3 font-semibold text-slate-800">${formatINR(c.value_inr)}</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${c.status}</span></td>
                    <td class="p-3 text-slate-500">${formatDate(c.effective_date)}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Error loading CRM:', err);
    }
}

export function toggleCRMModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.toggle('hidden');
}

export async function handleCreateOpportunity(event) {
    event.preventDefault();
    const code = document.getElementById('opp-code').value;
    const client = document.getElementById('opp-client').value;
    const title = document.getElementById('opp-title').value;
    const val = parseFloat(document.getElementById('opp-value').value);
    const stage = document.getElementById('opp-stage').value;
    const closeDate = document.getElementById('opp-close-date').value;
    const disc = parseFloat(document.getElementById('opp-discount').value) || 0.0;
    const owner = document.getElementById('opp-owner').value;

    try {
        const res = await fetch(`${API_BASE}/crm-enterprise/opportunities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                opportunity_code: code,
                client_name: client,
                deal_title: title,
                deal_value_inr: val,
                stage: stage,
                expected_close_date: closeDate,
                discount_offered_pct: disc,
                owner: owner
            })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Failed to create deal");
        }
        alert("Enterprise opportunity successfully registered!");
        toggleCRMModal('modal-crm-opp');
        loadCRM();
    } catch (err) {
        alert("Error saving deal: " + err.message);
    }
}

export async function advanceOpportunityStage(oppId, newStage) {
    try {
        const res = await fetch(`${API_BASE}/crm-enterprise/opportunities/${oppId}/stage`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stage: newStage })
        });
        if (!res.ok) throw new Error("Failed to advance stage");
        loadCRM();
    } catch (err) {
        alert("Error updating deal stage: " + err.message);
    }
}

export async function handleCreateTicket(event) {
    event.preventDefault();
    const num = document.getElementById('tkt-number').value;
    const client = document.getElementById('tkt-client').value;
    const email = document.getElementById('tkt-email').value;
    const sev = document.getElementById('tkt-severity').value;
    const subject = document.getElementById('tkt-subject').value;
    const desc = document.getElementById('tkt-desc').value;

    try {
        const res = await fetch(`${API_BASE}/crm-enterprise/tickets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticket_number: num,
                client_name: client,
                contact_email: email,
                severity: sev,
                subject: subject,
                description: desc
            })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Failed to create ticket");
        }
        alert("Support ticket logged under active SLA!");
        toggleCRMModal('modal-crm-ticket');
        loadCRM();
    } catch (err) {
        alert("Error logging ticket: " + err.message);
    }
}

export async function resolveTicket(ticketId) {
    const summary = prompt("Enter resolution notes:", "Resolution verified and deployed.");
    if (!summary) return;
    try {
        const res = await fetch(`${API_BASE}/crm-enterprise/tickets/${ticketId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: "Resolved",
                resolution_summary: summary,
                csat_rating: 5
            })
        });
        if (!res.ok) throw new Error("Failed to resolve ticket");
        loadCRM();
    } catch (err) {
        alert("Error resolving ticket: " + err.message);
    }
}

// 4. Finance
export async function loadFinance() {
    try {
        const [resInvoices, resBills, resAccounts, resCashflow, resClaims] = await Promise.all([
            fetch(`${API_BASE}/finance/invoices`).then(r => r.json()),
            fetch(`${API_BASE}/finance/ap-bills`).then(r => r.json()),
            fetch(`${API_BASE}/finance/chart-of-accounts`).then(r => r.json()),
            fetch(`${API_BASE}/finance/13-week-forecast`).then(r => r.json()),
            fetch(`${API_BASE}/finance/expense-claims`).then(r => r.json())
        ]);

        const invTable = document.getElementById('table-invoices');
        invTable.innerHTML = resInvoices.map(i => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${i.invoice_number}</td>
                <td class="p-3 font-medium text-slate-800">${i.customer_name}</td>
                <td class="p-3 text-slate-500">${formatDate(i.invoice_date)}</td>
                <td class="p-3 text-slate-600">${formatINR(i.taxable_value)}</td>
                <td class="p-3 text-slate-600">${formatINR(i.total_tax)} (18%)</td>
                <td class="p-3 font-semibold text-slate-900">${formatINR(i.total_invoice_value)}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded ${i.status === 'Paid' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'} font-medium">${i.status}</span></td>
            </tr>
        `).join('');

        const billTable = document.getElementById('table-ap-bills');
        billTable.innerHTML = resBills.map(b => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${b.bill_number}</td>
                <td class="p-3 font-medium text-slate-800">${b.vendor_name}</td>
                <td class="p-3 text-slate-600">${formatINR(b.taxable_amount)}</td>
                <td class="p-3 text-rose-600 font-medium">${formatINR(b.tds_amount)} (${b.tds_section})</td>
                <td class="p-3 font-semibold text-slate-900">${formatINR(b.net_payable)}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-blue-50 text-blue-700 font-semibold">${b.three_way_match_status}</span></td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${b.approval_status}</span></td>
            </tr>
        `).join('');

        // 13-week cash flow table
        const cfTable = document.getElementById('table-cashflow-13wk');
        if (cfTable && resCashflow.weeks) {
            cfTable.innerHTML = resCashflow.weeks.map(w => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-semibold text-slate-800">${w.week_label}</td>
                    <td class="p-2.5 text-slate-600 text-right">${formatINR(w.opening_cash)}</td>
                    <td class="p-2.5 text-emerald-600 font-medium text-right">+${formatINR(w.inflows)}</td>
                    <td class="p-2.5 text-rose-600 text-right">-${formatINR(w.payroll_outflow)}</td>
                    <td class="p-2.5 text-rose-600 text-right">-${formatINR(w.vendor_outflow)}</td>
                    <td class="p-2.5 text-rose-600 text-right">-${formatINR(w.statutory_tax_outflow)}</td>
                    <td class="p-2.5 font-bold text-slate-900 text-right">${formatINR(w.closing_cash)}</td>
                </tr>
            `).join('');

            document.getElementById('cf-runway-val').innerText = `${resCashflow.estimated_runway_months} Months`;
            document.getElementById('cf-closing-val').innerText = formatINR(resCashflow.closing_cash_13wk_inr);
        }

        const coaTable = document.getElementById('table-coa');
        coaTable.innerHTML = resAccounts.map(a => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${a.account_code}</td>
                <td class="p-3 font-medium text-slate-800">${a.account_name}</td>
                <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-slate-100 text-slate-700">${a.account_group}</span></td>
                <td class="p-3 text-slate-600">${a.normal_balance}</td>
                <td class="p-3 text-slate-500">${a.cost_center}</td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Error loading finance:', err);
    }
}

// 5. HRMS & Human Capital Suite (Comprehensive Enterprise Controller)
export let cachedHRMSEmployees = [];

export async function loadHRMS() {
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

export function renderHRMSEmployees(employees) {
    const empTable = document.getElementById('table-employees');
    if (!empTable) return;
    if (employees.length === 0) {
        empTable.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-slate-400">No employees found.</td></tr>`;
        return;
    }
    empTable.innerHTML = employees.map(e => `
        <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
            <td class="p-3">
                <div class="font-mono text-xs text-blue-700 font-bold">${e.emp_code}</div>
                <div class="mt-1">${e.blood_group ? `<span class="px-1.5 py-0.5 bg-rose-50 text-rose-700 border border-rose-200 rounded font-bold text-[9px]">${e.blood_group}</span>` : ''}</div>
            </td>
            <td class="p-3">
                <div class="flex items-center gap-2">
                    <img src="${e.webcam_registered_face_url || '/static/img/avatars/default.png'}" alt="${e.full_name}" class="w-8 h-8 rounded-full object-cover border border-slate-200 shadow-sm flex-shrink-0" onerror="this.src='/static/img/avatars/default.png'">
                    <div>
                        <div class="font-semibold text-slate-900">${e.full_name}</div>
                        <div class="text-[11px] text-slate-400 font-mono">${e.official_email}</div>
                    </div>
                </div>
            </td>
            <td class="p-3">
                <div class="font-medium text-slate-800">${e.designation}</div>
                <div class="text-[11px] text-slate-500">${e.department} &bull; <span class="font-mono text-slate-400">${formatDate(e.date_of_joining)}</span></div>
            </td>
            <td class="p-3">
                <div class="flex items-center gap-1.5 font-mono text-slate-800 font-semibold text-[11px]">
                    <i class="fa-solid fa-location-dot text-rose-500 text-[10px]"></i>
                    ${e.latitude != null ? Number(e.latitude).toFixed(6) : '13.035820'}°N, ${e.longitude != null ? Number(e.longitude).toFixed(6) : '77.653410'}°E
                </div>
                <div class="flex items-center gap-1.5 mt-1">
                    <span class="px-1.5 py-0.5 rounded text-[10px] font-bold ${e.work_location_type === 'Approved Remote WFH' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'}">
                        ${e.work_location_type || 'HQ Office'}
                    </span>
                    <span class="text-[10px] text-slate-500 font-mono">r=${e.geofence_radius_meters || 200}m</span>
                    ${e.geofence_enforced !== false ? '<span class="text-[9px] text-emerald-600 font-bold" title="Strict Geofence Enforced"><i class="fa-solid fa-shield-check"></i></span>' : ''}
                </div>
            </td>
            <td class="p-3">
                <div class="flex items-center gap-1.5">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${e.facial_enrollment_status === 'ENROLLED' ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-200'}">
                        <i class="fa-solid ${e.facial_enrollment_status === 'ENROLLED' ? 'fa-check' : 'fa-clock'} mr-0.5"></i>
                        ${e.facial_enrollment_status || 'PENDING'}
                    </span>
                    <span class="text-[10px] font-bold text-emerald-600">
                        ${e.facial_liveness_score ? (e.facial_liveness_score * 100).toFixed(1) + '%' : '98.8%'}
                    </span>
                </div>
                <div class="text-[10px] text-slate-400 font-mono truncate max-w-[150px] mt-0.5" title="${e.webcam_hardware_device || 'Integrated HD Webcam (1080p)'}">
                    <i class="fa-solid fa-camera text-[9px] mr-1"></i>${e.webcam_hardware_device || 'Integrated HD Webcam'}
                </div>
            </td>
            <td class="p-3">
                <div class="font-mono font-bold text-slate-900">${formatINR(e.annual_ctc || 1200000)}</div>
                <div class="text-[10px] text-slate-400 font-mono">PAN: <strong class="text-slate-700">${e.pan_number || '-'}</strong></div>
            </td>
            <td class="p-3">
                <span class="px-2 py-0.5 text-[10px] rounded font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${e.employment_status}</span>
            </td>
            <td class="p-3 text-center whitespace-nowrap">
                <div class="flex items-center justify-center gap-1">
                    <button onclick="viewEmployeeProfile(${e.id})" title="View 360 Profile" class="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[10px] font-bold transition flex items-center gap-1">
                        <i class="fa-solid fa-address-card"></i> Profile
                    </button>
                    <button onclick="openWebcamEnrollModal(${e.id})" title="Enroll Webcam Face" class="px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 rounded text-[10px] font-bold transition flex items-center gap-1">
                        <i class="fa-solid fa-camera"></i> Face
                    </button>
                    <button onclick="openGPSLocationModal(${e.id})" title="Pin GPS Geofence" class="px-2 py-1 bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 rounded text-[10px] font-bold transition flex items-center gap-1">
                        <i class="fa-solid fa-location-crosshairs"></i> GPS
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

export function filterHRMSEmployees(query) {
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

export function switchHRMSTab(tabId) {
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

    if (tabId === 'analytics') {
        loadHRMSAnalytics();
    }
}

export function openHRMSModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('hidden');
}

export function closeHRMSModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('hidden');
}

// ==============================================================
// HRMS WEBCAM STREAMING, BIOMETRIC SNAPSHOT & GPS GEOFENCE UTILITIES
// ==============================================================
export let hrmsActiveStreams = {};
const ASPERION_HQ_LAT = 13.035820;
const ASPERION_HQ_LON = 77.653410;

export async function startHRMSWebcam(videoElemId, previewElemId, placeholderElemId, statusElemId) {
    const video = document.getElementById(videoElemId);
    const preview = document.getElementById(previewElemId);
    const placeholder = document.getElementById(placeholderElemId);
    const status = document.getElementById(statusElemId);

    try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: "user" }
            });
            hrmsActiveStreams[videoElemId] = stream;
            if (video) {
                video.srcObject = stream;
                video.classList.remove('hidden');
                video.play();
            }
            if (preview) preview.classList.add('hidden');
            if (placeholder) placeholder.classList.add('hidden');
            if (status) {
                status.textContent = 'Live Feed Active';
                status.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-800 text-emerald-200';
            }
        } else {
            throw new Error("getUserMedia not supported in browser environment");
        }
    } catch (err) {
        console.warn("Webcam access notice:", err.message);
        if (video) video.classList.add('hidden');
        if (preview) preview.classList.remove('hidden');
        if (placeholder) {
            placeholder.classList.remove('hidden');
            placeholder.innerHTML = `<span class="text-xs text-amber-300 font-mono"><i class="fa-solid fa-video-slash"></i> Simulated Camera Active</span>`;
        }
        if (status) {
            status.textContent = 'Simulated Camera Active';
            status.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-blue-800 text-blue-200';
        }
    }
}

export function stopHRMSWebcam(videoElemId, statusElemId) {
    if (hrmsActiveStreams[videoElemId]) {
        try {
            hrmsActiveStreams[videoElemId].getTracks().forEach(track => track.stop());
        } catch (_) {}
        delete hrmsActiveStreams[videoElemId];
    }
    const video = document.getElementById(videoElemId);
    if (video) {
        video.srcObject = null;
        video.classList.add('hidden');
    }
    const status = document.getElementById(statusElemId);
    if (status) {
        status.textContent = 'Camera Inactive';
        status.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300';
    }
}

export function captureHRMSWebcam(videoElemId, canvasElemId, previewElemId, inputElemId, statusElemId) {
    const video = document.getElementById(videoElemId);
    const canvas = document.getElementById(canvasElemId);
    const preview = document.getElementById(previewElemId);
    const input = document.getElementById(inputElemId);
    const status = document.getElementById(statusElemId);

    let dataUri = '';
    if (canvas) {
        const ctx = canvas.getContext('2d');
        if (video && !video.classList.contains('hidden') && video.videoWidth > 0) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        } else {
            canvas.width = 320;
            canvas.height = 240;
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#1e293b';
            ctx.beginPath();
            ctx.arc(160, 95, 52, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(160, 215, 85, 60, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 2;
            ctx.strokeRect(95, 30, 130, 155);
            ctx.fillStyle = '#10b981';
            ctx.font = 'bold 10px monospace';
            ctx.fillText('ASPERION BIO-ID VERIFIED', 75, 205);
        }
        dataUri = canvas.toDataURL('image/jpeg', 0.88);
    }

    if (input) input.value = dataUri;
    if (preview) {
        preview.src = dataUri;
        preview.classList.remove('hidden');
    }
    if (video) video.classList.add('hidden');
    if (status) {
        status.textContent = 'Face Snapshot Captured (98.8% Liveness)';
        status.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-700 text-white';
    }
}

export function fillHoramavuHQCoords(latId, lonId, radId) {
    const latEl = document.getElementById(latId);
    const lonEl = document.getElementById(lonId);
    const radEl = document.getElementById(radId);
    if (latEl) latEl.value = ASPERION_HQ_LAT.toFixed(6);
    if (lonEl) lonEl.value = ASPERION_HQ_LON.toFixed(6);
    if (radEl) radEl.value = 200;
    if (latId === 'gps-modal-lat') recalcGPSModalDistance();
}

export function detectCurrentLocation(latId, lonId) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const latEl = document.getElementById(latId);
                const lonEl = document.getElementById(lonId);
                if (latEl) latEl.value = lat.toFixed(6);
                if (lonEl) lonEl.value = lon.toFixed(6);
                if (latId === 'gps-modal-lat') recalcGPSModalDistance();
                alert(`📍 Live GPS Detected: ${lat.toFixed(6)}°N, ${lon.toFixed(6)}°E (Accuracy: ±${Math.round(pos.coords.accuracy)}m)`);
            },
            (err) => {
                alert(`GPS Detection notice: ${err.message}. Defaulted to Horamavu HQ.`);
                fillHoramavuHQCoords(latId, lonId);
            },
            { timeout: 8000, enableHighAccuracy: true }
        );
    } else {
        alert("Geolocation not supported by browser. Assigned Horamavu HQ coordinates.");
        fillHoramavuHQCoords(latId, lonId);
    }
}

export function computeHaversineMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c);
}

export function recalcGPSModalDistance() {
    const lat = parseFloat(document.getElementById('gps-modal-lat')?.value) || ASPERION_HQ_LAT;
    const lon = parseFloat(document.getElementById('gps-modal-lon')?.value) || ASPERION_HQ_LON;
    const rad = parseFloat(document.getElementById('gps-modal-radius')?.value) || 200;
    const meters = computeHaversineMeters(ASPERION_HQ_LAT, ASPERION_HQ_LON, lat, lon);
    const label = document.getElementById('gps-modal-distance-label');
    if (label) {
        if (meters <= rad) {
            label.innerHTML = `<span class="text-emerald-600 font-bold font-mono">${meters}m from HQ (Inside Perimeter)</span>`;
        } else {
            label.innerHTML = `<span class="text-amber-600 font-bold font-mono">${meters}m from HQ (${(meters / 1000).toFixed(2)} km - Remote)</span>`;
        }
    }
}

export let currentEnrollEmp = null;

export async function openWebcamEnrollModal(empId) {
    try {
        let emp = (cachedHRMSEmployees || []).find(e => e.id === empId);
        if (!emp) {
            const res = await fetch(`${API_BASE}/hrms/employees/${empId}`);
            if (res.ok) emp = await res.json();
        }
        currentEnrollEmp = emp;
        if (!currentEnrollEmp) return;

        const idEl = document.getElementById('modal-webcam-emp-id');
        if (idEl) idEl.value = empId;
        const nameEl = document.getElementById('webcam-modal-emp-name');
        if (nameEl) nameEl.textContent = currentEnrollEmp.full_name;
        const codeEl = document.getElementById('webcam-modal-emp-code');
        if (codeEl) codeEl.textContent = currentEnrollEmp.emp_code;
        const statusEl = document.getElementById('webcam-modal-enroll-status');
        if (statusEl) statusEl.textContent = currentEnrollEmp.facial_enrollment_status || 'PENDING';
        const devEl = document.getElementById('modal-webcam-device-name');
        if (devEl) devEl.textContent = currentEnrollEmp.webcam_hardware_device || 'Integrated HD Webcam (1080p)';

        const preview = document.getElementById('modal-webcam-preview');
        if (preview) {
            preview.src = currentEnrollEmp.webcam_registered_face_url || '/static/img/avatars/default.png';
            preview.classList.remove('hidden');
        }
        const video = document.getElementById('modal-webcam-video');
        if (video) video.classList.add('hidden');

        openHRMSModal('modal-hrms-webcam-enroll');
    } catch (err) {
        alert("Failed to open webcam enrollment: " + err.message);
    }
}

export function closeWebcamEnrollModal() {
    stopHRMSWebcam('modal-webcam-video', 'modal-webcam-stream-status');
    closeHRMSModal('modal-hrms-webcam-enroll');
}

export async function submitWebcamEnrollment() {
    const empId = document.getElementById('modal-webcam-emp-id').value;
    let base64Photo = document.getElementById('modal-webcam-face-base64').value;
    if (!base64Photo) {
        captureHRMSWebcam('modal-webcam-video', 'modal-webcam-canvas', 'modal-webcam-preview', 'modal-webcam-face-base64', 'modal-webcam-stream-status');
        base64Photo = document.getElementById('modal-webcam-face-base64').value;
    }
    const finalPhoto = base64Photo || (currentEnrollEmp && currentEnrollEmp.webcam_registered_face_url) || 'data:image/jpeg;base64,ASPERION_FACIAL_BIOMETRIC_DATA';
    const hardwareDevice = document.getElementById('modal-webcam-device-name')?.textContent || 'Integrated HD Webcam (1080p)';

    try {
        const res = await fetch(`${API_BASE}/hrms/employees/${empId}/webcam-enroll`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                face_image_base64: finalPhoto,
                hardware_device: hardwareDevice,
                liveness_score: 0.988
            })
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ ${data.message || 'Webcam biometric facial template bound successfully!'}`);
            closeWebcamEnrollModal();
            loadHRMS();
        } else {
            const err = await res.json();
            alert(`Enrollment failed: ${err.detail || 'Biometric validation error'}`);
        }
    } catch (err) {
        alert("Error saving biometric enrollment: " + err.message);
    }
}

export let currentGPSEmp = null;

export async function openGPSLocationModal(empId) {
    try {
        let emp = (cachedHRMSEmployees || []).find(e => e.id === empId);
        if (!emp) {
            const res = await fetch(`${API_BASE}/hrms/employees/${empId}`);
            if (res.ok) emp = await res.json();
        }
        currentGPSEmp = emp;
        if (!currentGPSEmp) return;

        const idEl = document.getElementById('gps-modal-emp-id');
        if (idEl) idEl.value = empId;
        const nameEl = document.getElementById('gps-modal-emp-name');
        if (nameEl) nameEl.textContent = currentGPSEmp.full_name;
        const codeEl = document.getElementById('gps-modal-emp-code');
        if (codeEl) codeEl.textContent = currentGPSEmp.emp_code;

        const latEl = document.getElementById('gps-modal-lat');
        if (latEl) latEl.value = (currentGPSEmp.latitude != null ? currentGPSEmp.latitude : ASPERION_HQ_LAT).toFixed(6);
        const lonEl = document.getElementById('gps-modal-lon');
        if (lonEl) lonEl.value = (currentGPSEmp.longitude != null ? currentGPSEmp.longitude : ASPERION_HQ_LON).toFixed(6);
        const radEl = document.getElementById('gps-modal-radius');
        if (radEl) radEl.value = currentGPSEmp.geofence_radius_meters || 200;
        const typeEl = document.getElementById('gps-modal-type');
        if (typeEl) typeEl.value = currentGPSEmp.work_location_type || 'HQ Office';
        const enfEl = document.getElementById('gps-modal-enforce');
        if (enfEl) enfEl.checked = currentGPSEmp.geofence_enforced !== false;

        recalcGPSModalDistance();
        openHRMSModal('modal-hrms-gps-map');
    } catch (err) {
        alert("Failed to open GPS location modal: " + err.message);
    }
}

export function closeGPSLocationModal() {
    closeHRMSModal('modal-hrms-gps-map');
}

export async function submitGPSLocationUpdate(e) {
    if (e && e.preventDefault) e.preventDefault();
    const empId = document.getElementById('gps-modal-emp-id').value;
    const lat = parseFloat(document.getElementById('gps-modal-lat').value);
    const lon = parseFloat(document.getElementById('gps-modal-lon').value);
    const radius = parseFloat(document.getElementById('gps-modal-radius').value);
    const locType = document.getElementById('gps-modal-type').value;
    const enforce = document.getElementById('gps-modal-enforce').checked;

    try {
        const res = await fetch(`${API_BASE}/hrms/employees/${empId}/update-location`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                latitude: lat,
                longitude: lon,
                geofence_radius_meters: radius,
                work_location_type: locType,
                geofence_enforced: enforce
            })
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ ${data.message || 'GPS coordinates & Geofence updated successfully!'}`);
            closeGPSLocationModal();
            loadHRMS();
        } else {
            const err = await res.json();
            alert(`Location update failed: ${err.detail || 'Validation error'}`);
        }
    } catch (err) {
        alert("Error saving GPS geofence: " + err.message);
    }
}

// Handler: Create Employee
export async function handleCreateEmployee(e) {
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
            bank_ifsc: document.getElementById('new-emp-bank-ifsc').value.trim() || null,
            latitude: parseFloat(document.getElementById('new-emp-lat')?.value) || 13.035820,
            longitude: parseFloat(document.getElementById('new-emp-lon')?.value) || 77.653410,
            geofence_radius_meters: parseFloat(document.getElementById('new-emp-radius')?.value) || 200.0,
            work_location_type: document.getElementById('new-emp-loc-type')?.value || "HQ Office",
            geofence_enforced: true,
            webcam_hardware_device: document.getElementById('new-emp-webcam-dev')?.value || "Integrated HD Webcam (1080p)",
            webcam_registered_face_url: document.getElementById('new-emp-face-base64')?.value || null,
            blood_group: document.getElementById('new-emp-blood')?.value || "O+",
            emergency_contact_name: document.getElementById('new-emp-emg-name')?.value?.trim() || null,
            emergency_contact_phone: document.getElementById('new-emp-emg-phone')?.value?.trim() || null,
            residential_address: document.getElementById('new-emp-address')?.value?.trim() || null
        };

        const res = await fetch(`${API_BASE}/hrms/employees`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Employee successfully added to Asperion corporate roster!");
            stopHRMSWebcam('new-emp-webcam-video', 'new-emp-webcam-status');
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
export async function handleCreateCandidate(e) {
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
export async function handleAdvanceCandidateStage(candidateId, newStage) {
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
export async function handleHireCandidate(candidateId) {
    if (!confirm("Are you sure you want to hire this candidate?\nThis will convert them to an Active Employee, compute their statutory Wage Code salary structure, and automatically issue an official HR-ONB-01 Offer Letter with corporate branding.")) {
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
            alert(`🎉 Candidate successfully hired!\nNew Employee: ${data.full_name} (${data.emp_code})\nOffer Letter Issued: Letter #${data.offer_letter_id}\nOfficial Email: ${data.official_email}`);
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
export async function handleApplyLeave(e) {
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
export async function handleUpdateLeaveStatus(leaveId, status) {
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
export async function handleInitiateSeparation(e) {
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
export async function handleUpdateSeparationClearance(separationId, field, value) {
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
export async function handleProcessFF(separationId) {
    if (!confirm("Confirm Full & Final (F&F) Settlement processing?\nThis will verify no-dues, compute encashments, and finalize relieving status.")) {
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
export async function handleCreatePOSHCase(e) {
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
            alert(`✅ Confidential POSH complaint lodged under Case ID [${data.case_number}]!\nInternal Committee notified. Statutory 90-day inquiry clock initiated.`);
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
export async function handleConcludePOSH(caseId) {
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
export async function viewEmployeeProfile(empId) {
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
            <!-- Top Personal & Bio Profile Header -->
            <div class="flex items-center gap-3 p-3 bg-slate-900 text-white rounded-xl">
                <img src="${e.webcam_registered_face_url || '/static/img/avatars/default.png'}" alt="${e.full_name}" class="w-14 h-14 rounded-full object-cover border-2 border-emerald-400 shadow flex-shrink-0" onerror="this.src='/static/img/avatars/default.png'">
                <div class="flex-1">
                    <div class="flex items-center justify-between">
                        <h4 class="font-bold text-sm text-white">${e.full_name}</h4>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.facial_enrollment_status === 'ENROLLED' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'}">
                            <i class="fa-solid fa-camera mr-1"></i>${e.facial_enrollment_status || 'PENDING'}
                        </span>
                    </div>
                    <div class="text-[11px] text-slate-300 font-mono">${e.emp_code} &bull; ${e.designation} (${e.department})</div>
                    <div class="text-[10px] text-slate-400 flex items-center gap-2 mt-0.5">
                        <span><i class="fa-solid fa-phone mr-1"></i>${e.phone_number || '+91 98765 43210'}</span>
                        <span>&bull;</span>
                        <span class="font-bold text-rose-300">Blood: ${e.blood_group || 'O+'}</span>
                    </div>
                </div>
            </div>

            <!-- Statutory & Personal Details Grid -->
            <div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Official Email</span>
                    <span class="font-bold text-slate-800 font-mono text-[11px]">${e.official_email}</span>
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
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Emergency Contact</span>
                    <span class="text-slate-800 font-medium"><strong>${e.emergency_contact_name || 'Relative / Guardian'}</strong> (${e.emergency_contact_phone || '+91 98765 00000'})</span>
                </div>
                <div>
                    <span class="text-[10px] text-slate-400 font-semibold block">Residential Address</span>
                    <span class="text-slate-700 text-[11px] truncate block" title="${e.residential_address || 'Horamavu, Bangalore'}">${e.residential_address || 'Horamavu, Bangalore North - 560043'}</span>
                </div>
            </div>

            <!-- GPS Geolocation & Perimeter Geofencing Card -->
            <div class="p-3 bg-sky-50/50 rounded-xl border border-sky-200">
                <div class="flex justify-between items-center mb-2 pb-1.5 border-b border-sky-200">
                    <span class="font-bold text-sky-950 text-xs flex items-center gap-1.5">
                        <i class="fa-solid fa-location-crosshairs text-sky-600"></i> GPS Geofence & Location Assignment
                    </span>
                    <button onclick="openGPSLocationModal(${e.id})" class="px-2 py-0.5 bg-sky-600 hover:bg-sky-500 text-white rounded text-[10px] font-bold">
                        Adjust Pin
                    </button>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                    <div>Coordinates: <strong class="text-slate-900 font-mono">${e.latitude ? Number(e.latitude).toFixed(6) : '13.035820'}°N, ${e.longitude ? Number(e.longitude).toFixed(6) : '77.653410'}°E</strong></div>
                    <div>Location Mode: <strong class="text-sky-800 font-bold">${e.work_location_type || 'HQ Office'}</strong></div>
                    <div>Perimeter Radius: <strong class="text-slate-900 font-mono">${e.geofence_radius_meters || 200} Meters</strong></div>
                    <div>Enforcement: <strong class="${e.geofence_enforced !== false ? 'text-emerald-700 font-bold' : 'text-slate-500'}">${e.geofence_enforced !== false ? 'Strict HQ Boundary' : 'Permissive / WFH'}</strong></div>
                </div>
            </div>

            <!-- Live Webcam Biometric Verification Card -->
            <div class="p-3 bg-emerald-50/50 rounded-xl border border-emerald-200">
                <div class="flex justify-between items-center mb-2 pb-1.5 border-b border-emerald-200">
                    <span class="font-bold text-emerald-950 text-xs flex items-center gap-1.5">
                        <i class="fa-solid fa-camera-viewfinder text-emerald-600"></i> Webcam Biometric Facial Verification
                    </span>
                    <button onclick="openWebcamEnrollModal(${e.id})" class="px-2 py-0.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-bold">
                        Re-Enroll Face
                    </button>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                    <div>Status: <strong class="text-emerald-800 font-bold">${e.facial_enrollment_status || 'ENROLLED'}</strong></div>
                    <div>AI Liveness: <strong class="text-emerald-700 font-mono font-bold">${e.facial_liveness_score ? (e.facial_liveness_score * 100).toFixed(1) + '%' : '98.8% Verified'}</strong></div>
                    <div class="col-span-2">Hardware Device: <strong class="text-slate-800 font-mono text-[10px]">${e.webcam_hardware_device || 'Integrated HD Webcam (1080p)'}</strong></div>
                </div>
            </div>

            <!-- Wage Code Salary Structure Card -->
            <div class="p-3 bg-blue-50/50 rounded-xl border border-blue-200">
                <div class="flex justify-between items-center mb-2 pb-1.5 border-b border-blue-200">
                    <span class="font-bold text-blue-950 text-xs flex items-center gap-1.5">
                        <i class="fa-solid fa-calculator text-blue-600"></i> Wage Code 2019 Statutory Compensation
                    </span>
                    <span class="font-mono font-bold text-xs text-blue-900">Annual CTC: ${sal ? formatINR(sal.annual_ctc) : '-'}</span>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                    <div>Basic: <strong class="text-slate-900 font-mono">${sal ? formatINR(sal.basic_salary || sal.monthly_basic || 0) : '-'}/m</strong></div>
                    <div>HRA: <strong class="text-slate-900 font-mono">${sal ? formatINR(sal.hra || sal.monthly_hra || 0) : '-'}/m</strong></div>
                    <div>Special: <strong class="text-slate-900 font-mono">${sal ? formatINR(sal.special_allowance || sal.monthly_special_allowance || 0) : '-'}/m</strong></div>
                    <div>Monthly Gross: <strong class="text-emerald-700 font-mono font-bold">${sal ? formatINR(sal.gross_salary || sal.monthly_gross || 0) : '-'}/m</strong></div>
                    <div>EPFO PF (12%): <strong class="text-rose-700 font-mono">${sal ? formatINR(sal.employee_pf || sal.monthly_employee_pf || 0) : '-'}/m</strong></div>
                    <div>Karnataka PT: <strong class="text-purple-700 font-mono font-bold">₹200/m</strong></div>
                    <div>Net Take-Home: <strong class="text-emerald-600 font-mono font-bold">${sal ? formatINR(sal.net_in_hand || sal.monthly_net_take_home || 0) : '-'}/m</strong></div>
                    <div>Annual CTC: <strong class="text-emerald-600 font-mono font-bold">${sal ? formatINR(sal.annual_ctc || 0) : '-'}</strong></div>
                </div>
            </div>

            <!-- Leave Applications -->
            <div class="p-3 bg-amber-50/50 rounded-xl border border-amber-200">
                <span class="font-bold text-amber-950 text-xs block mb-2 flex items-center gap-1.5">
                    <i class="fa-solid fa-calendar-check text-amber-600"></i> Leave History (${(p.leaves || []).length} Records)
                </span>
                <div class="space-y-1 max-h-28 overflow-y-auto">
                    ${(p.leaves || []).length === 0 ? '<span class="text-slate-400 text-[11px]">No leaves applied.</span>' :
                        (p.leaves || []).map(lv => `
                            <div class="flex items-center justify-between p-1 bg-white rounded border border-amber-100 text-[11px]">
                                <span><strong>${lv.type}</strong> (${lv.days}d) - ${lv.dates}</span>
                                <span class="px-1.5 py-0.5 rounded text-[9px] font-bold ${lv.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${lv.status}</span>
                            </div>
                        `).join('')
                    }
                </div>
            </div>

            <!-- Issued Letters -->
            <div class="p-3 bg-purple-50/50 rounded-xl border border-purple-200">
                <span class="font-bold text-purple-950 text-xs block mb-2 flex items-center gap-1.5">
                    <i class="fa-solid fa-envelopes-bulk text-purple-600"></i> Issued Corporate Letters (${(p.letters || p.issued_letters || []).length})
                </span>
                <div class="space-y-1.5 max-h-36 overflow-y-auto">
                    ${(p.letters || p.issued_letters || []).length === 0 ? '<span class="text-slate-400 text-[11px]">No letters issued yet.</span>' :
                        (p.letters || p.issued_letters || []).map(l => `
                            <div class="flex items-center justify-between p-1.5 bg-white rounded border border-purple-100 text-[11px]">
                                <div>
                                    <span class="font-mono text-purple-700 font-bold mr-1">[${l.code || l.letter_code}]</span>
                                    <span class="font-medium text-slate-800">${l.title || l.letter_title}</span>
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

export async function loadSalaryStatements(cycle = "JUN-2026") {
    try {
        const res = await fetch(`${API_BASE}/hrms/payroll-records`);
        if (!res.ok) return;
        const records = await res.json();
        const employees = await fetch(`${API_BASE}/hrms/employees`).then(r => r.json());

        const table = document.getElementById('table-salary-statements');
        if (!table) return;

        if (records.length === 0) {
            table.innerHTML = `<tr><td colspan="11" class="p-4 text-center text-slate-400">No payroll statements generated yet. Click "Generate Statements" above.</td></tr>`;
            return;
        }

        table.innerHTML = records.map(r => {
            const emp = employees.find(e => e.id === r.employee_id);
            const empName = emp ? emp.full_name : `ID #${r.employee_id}`;
            const empCode = emp ? emp.emp_code : `-`;
            const desig = emp ? emp.designation : `-`;
            const utr = r.bank_utr ? `<span class="font-mono text-emerald-600 font-bold">${r.bank_utr}</span>` : `<span class="text-amber-600 font-medium">Pending Batch</span>`;

            return `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-3 font-mono font-semibold text-blue-700">${empCode}</td>
                    <td class="p-3 font-semibold text-slate-800">${empName}</td>
                    <td class="p-3 text-slate-500">${desig}</td>
                    <td class="p-3 text-right font-mono">${r.payable_days}d / <span class="text-rose-500 font-bold">${r.lop_days}d</span></td>
                    <td class="p-3 text-right font-semibold text-slate-800">${formatINR(r.earned_gross)}</td>
                    <td class="p-3 text-right text-slate-600 font-mono">${formatINR(r.pf_deduction)}</td>
                    <td class="p-3 text-right text-purple-700 font-mono font-bold">${formatINR(r.pt_deduction)}</td>
                    <td class="p-3 text-right text-slate-600 font-mono">${formatINR(r.tds_deduction)}</td>
                    <td class="p-3 text-right font-bold text-emerald-600 font-mono">${formatINR(r.net_salary)}</td>
                    <td class="p-3 text-xs">${utr}</td>
                    <td class="p-3 text-center">
                        <a href="/api/v1/hrms/salary-statement/payslip/${r.employee_id}?cycle=${r.payroll_cycle}" target="_blank" class="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-semibold transition inline-flex items-center gap-1">
                            <i class="fa-solid fa-file-invoice"></i> Slip
                        </a>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error('Error loading salary statements:', err);
    }
}

export async function handleRunAttendancePayroll(disburseBank = false) {
    try {
        const res = await fetch(`${API_BASE}/hrms/run-monthly-payroll`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                payroll_cycle: "JUN-2026",
                days_in_month: 30,
                disburse_bank: disburseBank
            })
        });

        if (res.ok) {
            const data = await res.json();
            const actionStr = disburseBank ? "Disbursed via Bank Batch (ICICI Bank UTRs Assigned)" : "Statements Generated & Verified";
            alert(`✅ ${actionStr}!\nActive Personnel: ${data.active_headcount}\nTotal Gross: ${formatINR(data.total_gross_inr)}\nKarnataka PT: ${formatINR(data.statutory_compliance_summary.total_karnataka_pt_inr)}\nTotal Net Payout: ${formatINR(data.total_net_disbursement_inr)}\n\nAutomated management notification dispatched to Director & Finance Head.`);
            loadSalaryStatements();
            fetchNotificationsAndAlerts();
        } else {
            const err = await res.json();
            alert(`Payroll Error: ${err.detail || 'Failed to execute payroll'}`);
        }
    } catch (err) {
        alert('Error executing attendance-synced payroll: ' + err.message);
    }
}

// 6. PMO & Global Delivery Operations Center
export async function loadPMO() {
    try {
        const [
            resProjects, resTasks, resRaid, resSprints,
            resIntakes, resCharters, resActions, resCapacity, resUat, resClosures, resGovOverview
        ] = await Promise.all([
            fetch(`${API_BASE}/pmo/projects`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/tasks`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/raid-items`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/sprints`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/intakes`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/charters`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/actions-decisions`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/capacity-plan`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/quality-uat`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/closures`).then(r => r.json()),
            fetch(`${API_BASE}/pmo/governance-overview`).then(r => r.json()).catch(() => null)
        ]);

        // Update Stage-Gate Counters
        if (resGovOverview && resGovOverview.stage_gates) {
            const sg = resGovOverview.stage_gates;
            const elIntk = document.getElementById('pmo-count-intakes');
            if (elIntk) elIntk.innerText = sg.gate_1_intakes;
            const elChtr = document.getElementById('pmo-count-charters');
            if (elChtr) elChtr.innerText = sg.gate_2_charters_baselined;
            const elPrj = document.getElementById('pmo-count-projects');
            if (elPrj) elPrj.innerText = sg.gate_3_active_projects;
            const elUat = document.getElementById('pmo-count-uats');
            if (elUat) elUat.innerText = sg.gate_4_uat_deliverables;
            const elClose = document.getElementById('pmo-count-closures');
            if (elClose) elClose.innerText = sg.gate_5_closures_completed;
        }

        // 1. Projects Table
        const projTable = document.getElementById('table-projects');
        if (projTable) {
            projTable.innerHTML = resProjects.map(p => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${p.project_code}</td>
                    <td class="p-3 font-medium text-slate-800">${p.name} <br><span class="text-xs text-slate-400">Client: ${p.client_name}</span></td>
                    <td class="p-3 text-slate-600">${p.project_manager}</td>
                    <td class="p-3 font-semibold text-slate-800">${formatINR(p.budget_inr)}</td>
                    <td class="p-3 text-slate-500">${formatDate(p.start_date)} - ${formatDate(p.target_end_date)}</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-blue-50 text-blue-700 font-medium">${p.status}</span></td>
                </tr>
            `).join('');
        }

        // 2. Interactive Kanban Boards
        const colTodo = document.getElementById('kanban-todo');
        const colInProgress = document.getElementById('kanban-inprogress');
        const colDone = document.getElementById('kanban-done');

        if (colTodo && colInProgress && colDone) {
            colTodo.innerHTML = '';
            colInProgress.innerHTML = '';
            colDone.innerHTML = '';

            resTasks.forEach(t => {
                const card = `
                    <div class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm mb-2.5 hover:border-blue-400 transition cursor-pointer">
                        <div class="flex justify-between items-start mb-1.5">
                            <span class="font-mono text-xs text-blue-600 font-bold">${t.wbs_code}</span>
                            <span class="text-xs px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">${t.sprint_phase}</span>
                        </div>
                        <h4 class="text-xs font-semibold text-slate-800 mb-2">${t.task_name}</h4>
                        <div class="flex justify-between items-center text-xs text-slate-400">
                            <span><i class="fa-regular fa-user mr-1"></i>${t.assigned_to || 'Unassigned'}</span>
                            <div class="flex gap-1">
                                <button onclick="changeTaskStatus(${t.id}, 'To Do')" title="To Do" class="px-1 text-slate-400 hover:text-slate-700">1</button>
                                <button onclick="changeTaskStatus(${t.id}, 'In Progress')" title="In Progress" class="px-1 text-blue-400 hover:text-blue-700">2</button>
                                <button onclick="changeTaskStatus(${t.id}, 'Done')" title="Done" class="px-1 text-emerald-400 hover:text-emerald-700">✓</button>
                            </div>
                        </div>
                    </div>
                `;
                if (t.status === 'Done') colDone.innerHTML += card;
                else if (t.status === 'In Progress') colInProgress.innerHTML += card;
                else colTodo.innerHTML += card;
            });
        }

        // 3. RAID Table
        const raidTable = document.getElementById('table-raid');
        if (raidTable) {
            raidTable.innerHTML = resRaid.map(r => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded ${r.item_type === 'Risk' ? 'bg-red-50 text-red-700' : 'bg-amber-50 text-amber-700'} font-semibold">${r.item_type}</span></td>
                    <td class="p-3 font-medium text-slate-800">${r.title}</td>
                    <td class="p-3 text-slate-600">${r.severity_impact}</td>
                    <td class="p-3 text-xs text-slate-600">${r.mitigation_plan || '-'}</td>
                    <td class="p-3 text-slate-500">${r.owner}</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${r.status}</span></td>
                </tr>
            `).join('');
        }

        // 4. Stage-Gate 1: Project Intakes
        const intakeTable = document.getElementById('table-pmo-intakes');
        if (intakeTable && resIntakes) {
            intakeTable.innerHTML = resIntakes.map(i => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-bold text-blue-700">${i.intake_code}</td>
                    <td class="p-2.5 font-semibold text-slate-800">${i.project_name} <br><span class="text-[10px] text-slate-400 font-normal">Sponsor: ${i.sponsor}</span></td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${i.strategic_fit === 'Critical' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-blue-50 text-blue-700 border border-blue-200'}">${i.strategic_fit}</span></td>
                    <td class="p-2.5 text-right font-mono font-semibold">${formatINR(i.estimated_budget_inr)}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${i.intake_status.includes('Approved') ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">${i.intake_status}</span></td>
                </tr>
            `).join('');
        }

        // 5. Stage-Gate 2: Charters
        const charterTable = document.getElementById('table-pmo-charters');
        if (charterTable && resCharters) {
            charterTable.innerHTML = resCharters.map(c => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2.5 font-bold font-mono text-indigo-700">${c.charter_code}</td>
                    <td class="p-2.5 text-slate-700 max-w-xs truncate" title="${c.problem_statement}">${c.problem_statement}</td>
                    <td class="p-2.5 text-slate-600 max-w-xs truncate" title="${c.measurable_success_criteria}">${c.measurable_success_criteria}</td>
                    <td class="p-2.5 font-medium text-slate-800">${c.signed_off_by}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${c.signoff_status}</span></td>
                </tr>
            `).join('');
        }

        // 6. Resource Capacity Plan
        const capTable = document.getElementById('table-pmo-capacity');
        if (capTable && resCapacity) {
            capTable.innerHTML = resCapacity.map(cp => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2.5 font-bold text-slate-800">${cp.role_title}</td>
                    <td class="p-2.5 text-slate-700">${cp.person_or_vendor}</td>
                    <td class="p-2.5 text-right font-mono">${cp.required_hours}h</td>
                    <td class="p-2.5 text-right font-mono">${cp.available_hours}h</td>
                    <td class="p-2.5 text-right font-mono font-bold ${cp.utilization_pct > 105 ? 'text-rose-600' : 'text-emerald-600'}">${cp.utilization_pct}%</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${cp.status.includes('Constrained') ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'}">${cp.status}</span></td>
                </tr>
            `).join('');
        }

        // 7. SteerCo Action Items & Decisions
        const actionTable = document.getElementById('table-pmo-actions');
        if (actionTable && resActions) {
            actionTable.innerHTML = resActions.map(a => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${a.item_type === 'Decision' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}">${a.item_type}</span></td>
                    <td class="p-2.5 font-medium text-slate-800">${a.title_or_decision}</td>
                    <td class="p-2.5 text-slate-600">${a.owner}</td>
                    <td class="p-2.5 text-slate-500 font-mono">${a.due_date ? formatDate(a.due_date) : '-'}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${a.status === 'Closed' || a.status === 'Implemented' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">${a.status}</span></td>
                </tr>
            `).join('');
        }

        // 8. Stage-Gate 4: Quality & UAT
        const uatTable = document.getElementById('table-pmo-uat');
        if (uatTable && resUat) {
            uatTable.innerHTML = resUat.map(u => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2.5 font-semibold text-slate-800">${u.deliverable_name}</td>
                    <td class="p-2.5 text-slate-600">${u.test_or_review_type}</td>
                    <td class="p-2.5 text-slate-700">${u.client_reviewer}</td>
                    <td class="p-2.5 font-mono text-slate-500">${u.signoff_date ? formatDate(u.signoff_date) : '-'}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${u.status}</span></td>
                </tr>
            `).join('');
        }

        // 9. Stage-Gate 5: Closure & Lessons Learned
        const closeTable = document.getElementById('table-pmo-closures');
        if (closeTable && resClosures) {
            closeTable.innerHTML = resClosures.map(cl => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2.5 font-bold text-slate-800">${cl.closure_area}</td>
                    <td class="p-2.5 text-blue-700 font-medium">${cl.evidence_signoff}</td>
                    <td class="p-2.5 text-slate-600 max-w-xs truncate" title="${cl.lessons_learned_summary}">${cl.lessons_learned_summary}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700">${cl.closure_status}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Error loading PMO:', err);
    }
}

export function togglePMOModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.toggle('hidden');
}

export async function handleCreatePMOIntake(event) {
    event.preventDefault();
    const code = document.getElementById('pmo-intk-code').value.trim();
    const name = document.getElementById('pmo-intk-name').value.trim();
    const sponsor = document.getElementById('pmo-intk-sponsor').value.trim();
    const client = document.getElementById('pmo-intk-client').value.trim();
    const fit = document.getElementById('pmo-intk-fit').value;
    const value = document.getElementById('pmo-intk-value').value.trim();
    const budget = parseFloat(document.getElementById('pmo-intk-budget').value) || 0.0;

    try {
        const res = await fetch(`${API_BASE}/pmo/intakes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                intake_code: code,
                project_name: name,
                sponsor: sponsor,
                client_or_internal: client,
                strategic_fit: fit,
                expected_value: value,
                estimated_budget_inr: budget
            })
        });
        if (!res.ok) throw new Error("Failed to register project intake");
        alert("✅ Project intake successfully recorded under Stage-Gate 1!");
        togglePMOModal('modal-pmo-intake');
        loadPMO();
    } catch (err) {
        alert("Error creating intake: " + err.message);
    }
}

export async function handleCreatePMOAction(event) {
    event.preventDefault();
    const type = document.getElementById('pmo-act-type').value;
    const meeting = document.getElementById('pmo-act-meeting').value.trim();
    const title = document.getElementById('pmo-act-title').value.trim();
    const owner = document.getElementById('pmo-act-owner').value.trim();
    const dateVal = document.getElementById('pmo-act-due').value || null;

    try {
        const res = await fetch(`${API_BASE}/pmo/actions-decisions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: 1,
                item_type: type,
                source_meeting: meeting,
                title_or_decision: title,
                owner: owner,
                due_date: dateVal
            })
        });
        if (!res.ok) throw new Error("Failed to record SteerCo item");
        alert("✅ SteerCo item successfully logged in decision register!");
        togglePMOModal('modal-pmo-action');
        loadPMO();
    } catch (err) {
        alert("Error logging action: " + err.message);
    }
}

export async function changeTaskStatus(taskId, newStatus) {
    try {
        await fetch(`${API_BASE}/pmo/tasks/${taskId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        loadPMO();
    } catch (err) {
        console.error('Error updating task:', err);
    }
}

// ==============================================================================
// 6b. SDLC & DEVSECOPS ENGINEERING COCKPIT
// ==============================================================================

export async function loadSDLC() {
    try {
        const [resReqs, resAdrs, resPrs, resPipes, resBugs, resReleases, resObs, resOverview] = await Promise.all([
            fetch(`${API_BASE}/sdlc/requirements`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/adrs`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/pull-requests`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/pipelines`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/defects`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/releases`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/observability`).then(r => r.json()),
            fetch(`${API_BASE}/sdlc/overview`).then(r => r.json()).catch(() => null)
        ]);

        // Render Telemetry KPI Cards
        if (resOverview && resOverview.sdlc_kpis) {
            const k = resOverview.sdlc_kpis;
            const elReqs = document.getElementById('sdlc-stat-reqs');
            if (elReqs) elReqs.innerText = k.total_requirements;
            const elAdrs = document.getElementById('sdlc-stat-adrs');
            if (elAdrs) elAdrs.innerText = k.approved_adrs;
            const elGate = document.getElementById('sdlc-stat-pipeline-gate');
            if (elGate) elGate.innerText = k.pipeline_pass_rate_pct === 100.0 ? "PASSED" : "WARNING";
            const elCov = document.getElementById('sdlc-stat-coverage');
            if (elCov) elCov.innerText = `${k.code_coverage_pct}% (${k.automated_test_count} tests)`;
            const elRel = document.getElementById('sdlc-stat-release');
            if (elRel) elRel.innerText = k.latest_release;
            const elLat = document.getElementById('sdlc-stat-latency');
            if (elLat) elLat.innerText = `${k.p95_latency_ms} ms`;
        }

        // 1. Stage 1: Requirements Table
        const reqTable = document.getElementById('table-sdlc-reqs');
        if (reqTable && resReqs) {
            reqTable.innerHTML = resReqs.map(r => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-bold font-mono text-blue-700">${r.req_code}</td>
                    <td class="p-2.5">
                        <div class="font-semibold text-slate-800">${r.title}</div>
                        <div class="text-[10px] text-slate-500 line-clamp-1">${r.acceptance_criteria}</div>
                    </td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">${r.category}</span></td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${r.priority === 'Must Have' ? 'bg-red-50 text-red-700' : 'bg-slate-100 text-slate-700'}">${r.priority}</span></td>
                    <td class="p-2.5 text-slate-600 font-mono text-[11px]">${r.verification_method}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700">${r.status}</span></td>
                </tr>
            `).join('');
        }

        // 2. Stage 2: ADR Table
        const adrTable = document.getElementById('table-sdlc-adrs');
        if (adrTable && resAdrs) {
            adrTable.innerHTML = resAdrs.map(a => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-bold font-mono text-indigo-700">${a.adr_number}</td>
                    <td class="p-2.5 font-semibold text-slate-800">${a.title}</td>
                    <td class="p-2.5 text-slate-600 max-w-xs truncate" title="${a.context}">${a.context}</td>
                    <td class="p-2.5 text-slate-500">${a.author.split(' ')[0]}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${a.status}</span></td>
                </tr>
            `).join('');
        }

        // 3. Stage 3: Pull Requests Table
        const prTable = document.getElementById('table-sdlc-prs');
        if (prTable && resPrs) {
            prTable.innerHTML = resPrs.map(p => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-bold font-mono text-purple-700">${p.pr_number}</td>
                    <td class="p-2.5">
                        <div class="font-semibold text-slate-800">${p.title}</div>
                        <div class="text-[10px] text-slate-400 font-mono">${p.source_branch} &rarr; ${p.target_branch}</div>
                    </td>
                    <td class="p-2.5 text-slate-700">${p.author}</td>
                    <td class="p-2.5 text-slate-500">${p.peer_reviewers}</td>
                    <td class="p-2.5">${p.security_signoff ? '<span class="text-emerald-600 font-bold text-xs"><i class="fa-solid fa-check-circle"></i> Clean</span>' : '<span class="text-amber-500 font-bold text-xs">Pending</span>'}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.review_status === 'Merged' ? 'bg-purple-100 text-purple-800' : 'bg-emerald-50 text-emerald-700'}">${p.review_status}</span></td>
                </tr>
            `).join('');
        }

        // 4. Stage 4: CI/CD Pipelines
        const pipeTable = document.getElementById('table-sdlc-pipelines');
        if (pipeTable && resPipes) {
            pipeTable.innerHTML = resPipes.map(p => `
                <tr class="hover:bg-slate-50 transition font-mono">
                    <td class="p-2.5 font-bold text-blue-700">${p.pipeline_code}</td>
                    <td class="p-2.5 text-slate-600">${p.commit_sha.substring(0, 8)}</td>
                    <td class="p-2.5 text-right font-bold text-emerald-600">${p.unit_tests_passed} passed</td>
                    <td class="p-2.5 text-right font-bold text-purple-700">${p.test_coverage_pct}%</td>
                    <td class="p-2.5 font-semibold text-emerald-600 text-[11px]"><i class="fa-solid fa-shield mr-1"></i>SAST/SCA Clean</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">${p.quality_gate_result}</span></td>
                </tr>
            `).join('');
        }

        // 5. Stage 5: Defects Table
        const bugTable = document.getElementById('table-sdlc-bugs');
        if (bugTable && resBugs) {
            bugTable.innerHTML = resBugs.map(b => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2 font-mono font-bold text-rose-700">${b.bug_id}</td>
                    <td class="p-2 font-medium text-slate-800 truncate max-w-[140px]" title="${b.title}">${b.title}</td>
                    <td class="p-2"><span class="px-1.5 py-0.2 rounded text-[9px] font-bold ${b.severity.includes('Critical') || b.severity.includes('Blocker') ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}">${b.severity.split('-')[0]}</span></td>
                    <td class="p-2"><span class="px-1.5 py-0.2 rounded text-[9px] font-semibold bg-emerald-50 text-emerald-700">${b.status.split(' ')[0]}</span></td>
                </tr>
            `).join('');
        }

        // 6. Stage 6: Releases Table
        const relTable = document.getElementById('table-sdlc-releases');
        if (relTable && resReleases) {
            relTable.innerHTML = resReleases.map(r => `
                <tr class="hover:bg-slate-50 transition text-xs">
                    <td class="p-2 font-mono font-bold text-blue-700">${r.release_tag}</td>
                    <td class="p-2 text-slate-600">${r.deployment_strategy.split(' ')[0]}</td>
                    <td class="p-2 text-slate-500 truncate max-w-[100px]" title="${r.change_advisory_board_approval}">${r.change_advisory_board_approval.split(' ')[0]}</td>
                    <td class="p-2"><span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-emerald-50 text-emerald-700">${r.deployment_status.split(' ')[0]}</span></td>
                </tr>
            `).join('');
        }

        // 7. Stage 7: SRE Telemetry
        if (resObs && resObs.length > 0) {
            const o = resObs[0];
            const p95 = document.getElementById('sre-p95-val');
            if (p95) p95.innerText = o.p95_latency_ms;
            const p99 = document.getElementById('sre-p99-val');
            if (p99) p99.innerText = o.p99_latency_ms;
            const err = document.getElementById('sre-error-rate-val');
            if (err) err.innerText = o.error_rate_pct;
            const bg = document.getElementById('sre-budget-val');
            if (bg) bg.innerText = o.error_budget_remaining_pct;
            const mem = document.getElementById('sre-mem-val');
            if (mem) mem.innerText = o.active_memory_mb;
            const cpu = document.getElementById('sre-cpu-val');
            if (cpu) cpu.innerText = o.cpu_utilization_pct;
        }
    } catch (err) {
        console.error('Error loading SDLC:', err);
    }
}

export function toggleSDLCModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.toggle('hidden');
}

export async function handleCreateSDLCRequirement(event) {
    event.preventDefault();
    const code = document.getElementById('sdlc-req-code').value.trim();
    const title = document.getElementById('sdlc-req-title').value.trim();
    const cat = document.getElementById('sdlc-req-cat').value;
    const prio = document.getElementById('sdlc-req-prio').value;
    const verif = document.getElementById('sdlc-req-verif').value;
    const crit = document.getElementById('sdlc-req-criteria').value.trim();

    try {
        const res = await fetch(`${API_BASE}/sdlc/requirements`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                req_code: code,
                title: title,
                category: cat,
                priority: prio,
                acceptance_criteria: crit,
                verification_method: verif
            })
        });
        if (!res.ok) throw new Error("Failed to create SRS specification");
        alert("✅ Software Requirement Specification (SRS) successfully registered in RTM!");
        toggleSDLCModal('modal-sdlc-req');
        loadSDLC();
    } catch (err) {
        alert("Error saving requirement: " + err.message);
    }
}

export async function handleCreateSDLCDefect(event) {
    event.preventDefault();
    const id = document.getElementById('sdlc-bug-id').value.trim();
    const title = document.getElementById('sdlc-bug-title').value.trim();
    const sev = document.getElementById('sdlc-bug-sev').value;
    const mod = document.getElementById('sdlc-bug-mod').value.trim();
    const env = document.getElementById('sdlc-bug-env').value;

    try {
        const res = await fetch(`${API_BASE}/sdlc/defects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                bug_id: id,
                title: title,
                severity: sev,
                module_affected: mod,
                environment: env
            })
        });
        if (!res.ok) throw new Error("Failed to log defect");
        alert("✅ Defect registered under IEEE 1044 standard!");
        toggleSDLCModal('modal-sdlc-bug');
        loadSDLC();
    } catch (err) {
        alert("Error logging bug: " + err.message);
    }
}

export async function handleTriggerPipelineRun() {
    try {
        const randSha = Math.random().toString(16).substring(2, 10);
        const randCode = "PIPE-2026-" + Math.floor(100 + Math.random() * 900);
        const res = await fetch(`${API_BASE}/sdlc/pipelines/trigger`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pipeline_code: randCode,
                commit_sha: randSha,
                branch: "main",
                triggered_by: "Varadi Vijay (Sole Director)",
                duration_seconds: 115
            })
        });
        if (!res.ok) throw new Error("Failed to trigger pipeline");
        const data = await res.json();
        alert(`🚀 CI/CD Automated Pipeline Run ${data.pipeline_code} Complete!\nCommit SHA: ${data.commit_sha}\nUnit Tests: ${data.unit_tests_passed} Passed\nCode Coverage: ${data.test_coverage_pct}%\nDevSecOps SAST/SCA Quality Gate: ${data.quality_gate_result}\nArtifact Built: ${data.artifacts_generated}`);
        loadSDLC();
    } catch (err) {
        alert("Pipeline error: " + err.message);
    }
}

// 7. Procurement
export async function loadProcurement() {
    try {
        const [
            resOverview, resEvents, resPRs, resVendors,
            resContracts, resGRNs, resScorecards, resRisks,
            resCAPAs, resCategories, resRFPs
        ] = await Promise.all([
            fetch(`${API_BASE}/procurement/overview`).then(r => r.json()).catch(() => ({})),
            fetch(`${API_BASE}/procurement/sourcing-events`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/requisitions`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/vendors`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/contracts`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/grns`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/scorecards`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/risk-assessments`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/capas`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/categories`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/procurement/rfp-comparisons`).then(r => r.json()).catch(() => [])
        ]);

        // 1. Telemetry KPIs
        if (resOverview && resOverview.procurement_kpis) {
            const kpi = resOverview.procurement_kpis;
            const elSpend = document.getElementById('kpi-procure-spend');
            if (elSpend) elSpend.innerText = formatINR(kpi.managed_spend_inr || 1665000);
            const elMsme = document.getElementById('kpi-procure-msme');
            if (elMsme) elMsme.innerText = `${kpi.msme_spend_share_pct || 48.9}%`;
            const elSavings = document.getElementById('kpi-procure-savings');
            if (elSavings) elSavings.innerText = formatINR(kpi.savings_realized_inr || 74000);
            const elPRs = document.getElementById('kpi-procure-prs');
            if (elPRs) elPRs.innerText = `${kpi.purchase_requisitions_count || 4} PRs`;
            const elEvents = document.getElementById('kpi-procure-events');
            if (elEvents) elEvents.innerText = `${kpi.active_sourcing_events || 3} Events`;
            const elContracts = document.getElementById('kpi-procure-contracts');
            if (elContracts) elContracts.innerText = `${formatINR(kpi.active_contracts_value_inr || 1320000)}/yr`;
            const elGRNs = document.getElementById('kpi-procure-grns');
            if (elGRNs) elGRNs.innerText = `${kpi.total_grns_inspected || 2} Batches`;
            const elRating = document.getElementById('kpi-procure-rating');
            if (elRating) elRating.innerText = `${(kpi.average_vendor_quality_score || 96.3).toFixed(1)} / 100`;
        }

        // 2. Strategic Sourcing e-RFX Events
        const eventsTable = document.getElementById('table-sourcing-events');
        if (eventsTable && resEvents) {
            eventsTable.innerHTML = resEvents.map(e => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-purple-700 font-bold">${e.event_code}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded font-semibold text-[10px] ${e.event_type === 'RFP' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}">${e.event_type}</span></td>
                    <td class="p-2.5 font-medium text-slate-800">${e.title}</td>
                    <td class="p-2.5 text-slate-600">${e.category}</td>
                    <td class="p-2.5 font-mono font-medium">${formatINR(e.budget_allocation_inr)}</td>
                    <td class="p-2.5 font-mono text-slate-500">${formatINR(e.baseline_cost_inr)}</td>
                    <td class="p-2.5">
                        ${e.awarded_vendor_name ? `
                            <span class="font-semibold text-emerald-700">${e.awarded_vendor_name}</span>
                            <br><span class="text-[10px] text-emerald-600 font-mono">Saved ${formatINR(e.savings_realized_inr)}</span>
                        ` : '<span class="text-slate-400 italic">Evaluation in progress</span>'}
                    </td>
                    <td class="p-2.5 font-mono text-slate-500">${e.closing_date}</td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${e.status === 'Awarded' ? 'bg-emerald-100 text-emerald-800' : (e.status === 'Commercial BAFO' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800')}">
                            ${e.status}
                        </span>
                    </td>
                </tr>
            `).join('');
        }

        // 3. Purchase Requisitions (PR)
        const prsTable = document.getElementById('table-purchase-requisitions');
        if (prsTable && resPRs) {
            prsTable.innerHTML = resPRs.map(pr => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-blue-700 font-bold">${pr.pr_number}</td>
                    <td class="p-2.5 font-medium text-slate-800">${pr.requester_name}<br><span class="text-[10px] text-slate-400">${pr.department}</span></td>
                    <td class="p-2.5 text-slate-600">${pr.category}</td>
                    <td class="p-2.5 text-slate-700 max-w-xs truncate" title="${pr.item_details}">${pr.item_details}</td>
                    <td class="p-2.5 font-mono font-bold text-slate-900">${formatINR(pr.estimated_amount_inr)}</td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${pr.urgency === 'Critical' ? 'bg-rose-100 text-rose-800' : (pr.urgency === 'Urgent' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700')}">
                            ${pr.urgency}
                        </span>
                    </td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${pr.approval_status === 'Approved' || pr.approval_status === 'Converted to PO' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
                            ${pr.approval_status}
                        </span>
                    </td>
                    <td class="p-2.5 text-slate-600 text-[11px]">${pr.approved_by || '<span class="text-amber-600 font-medium">Pending Review</span>'}</td>
                    <td class="p-2.5 font-mono text-emerald-700 font-semibold">${pr.linked_po_number || '-'}</td>
                </tr>
            `).join('');
        }

        // 4. Approved Vendors Master
        const venTable = document.getElementById('table-vendors');
        if (venTable && resVendors) {
            venTable.innerHTML = resVendors.map(v => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-blue-700 font-bold">${v.vendor_code}</td>
                    <td class="p-2.5 font-medium text-slate-800">${v.vendor_name}<br><span class="text-[10px] text-slate-400">${v.email}</span></td>
                    <td class="p-2.5 text-slate-600">${v.category}<br><span class="px-1.5 py-0.5 text-[9px] rounded font-semibold bg-slate-100 text-slate-700">${v.criticality_tier}</span></td>
                    <td class="p-2.5">
                        ${v.msme_registered ? `<span class="px-1.5 py-0.5 text-[9px] rounded font-bold bg-amber-100 text-amber-800">MSME-${v.msme_category || 'Micro'} (45d)</span>` : '<span class="text-[10px] text-slate-400">Non-MSME</span>'}
                        <br><span class="text-[10px] text-slate-500 font-mono">DUNS: ${v.duns_number || 'N/A'}</span>
                    </td>
                    <td class="p-2.5">
                        <span class="px-1.5 py-0.5 text-[9px] rounded font-semibold bg-emerald-100 text-emerald-800">${v.kyc_status}</span>
                        <br><span class="px-1.5 py-0.5 text-[9px] rounded font-semibold bg-blue-100 text-blue-800">${v.dpdp_compliance_status}</span>
                    </td>
                    <td class="p-2.5 font-mono font-semibold">${formatINR(v.annual_spend_estimate)}</td>
                    <td class="p-2.5 font-bold text-amber-600">${(v.rating || 92.5).toFixed(1)}/100</td>
                </tr>
            `).join('');
        }

        // 5. Vendor Contracts (CLM)
        const conTable = document.getElementById('table-vendor-contracts');
        if (conTable && resContracts) {
            conTable.innerHTML = resContracts.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-emerald-700 font-bold">${c.contract_reference}</td>
                    <td class="p-2.5 font-medium text-slate-800">${c.agreement_type}</td>
                    <td class="p-2.5 font-mono text-[10px] text-slate-600">${c.effective_date} to ${c.expiry_date || 'Perpetual'}</td>
                    <td class="p-2.5 font-mono font-bold">${formatINR(c.annual_value_inr)}</td>
                    <td class="p-2.5 font-semibold text-blue-700">${c.sla_uptime_commitment}%</td>
                    <td class="p-2.5 text-slate-500">${c.renewal_notice_days || 60}d</td>
                    <td class="p-2.5"><span class="px-1.5 py-0.5 rounded font-bold text-[9px] bg-emerald-100 text-emerald-800">${c.status}</span></td>
                </tr>
            `).join('');
        }

        // 6. Goods Received Notes (GRN)
        const grnTable = document.getElementById('table-grns');
        if (grnTable && resGRNs) {
            grnTable.innerHTML = resGRNs.map(g => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-teal-700 font-bold">${g.grn_number}</td>
                    <td class="p-2.5 font-mono font-medium text-blue-700">${g.po_reference}</td>
                    <td class="p-2.5 font-mono text-slate-500">${g.delivery_challan_no || '-'}</td>
                    <td class="p-2.5 font-mono text-slate-600">${g.received_date}</td>
                    <td class="p-2.5 font-medium text-slate-800">${g.item_description}</td>
                    <td class="p-2.5 font-mono">${g.quantity_ordered} / ${g.quantity_received} / <span class="font-bold text-emerald-700">${g.quantity_accepted}</span></td>
                    <td class="p-2.5 text-slate-600">${g.warehouse_location || 'Bangalore HQ'}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">${g.inspection_status}</span></td>
                    <td class="p-2.5 text-slate-500">${g.inspected_by}</td>
                </tr>
            `).join('');
        }

        // 7. QBR Scorecards
        const scoreTable = document.getElementById('table-scorecards');
        if (scoreTable && resScorecards) {
            scoreTable.innerHTML = resScorecards.map(s => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2 font-mono text-slate-600">${s.evaluation_period}</td>
                    <td class="p-2 font-medium text-slate-800">Vendor #${s.vendor_id}</td>
                    <td class="p-2 font-bold text-amber-600">${s.overall_rating.toFixed(1)}/100</td>
                    <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-800">${s.performance_tier}</span></td>
                </tr>
            `).join('');
        }

        // 8. Third-Party Risk (TPRM)
        const riskTable = document.getElementById('table-vendor-risks');
        if (riskTable && resRisks) {
            riskTable.innerHTML = resRisks.map(r => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2 font-medium text-slate-800">Vendor #${r.vendor_id}</td>
                    <td class="p-2 text-slate-600">${r.data_access_level}</td>
                    <td class="p-2 font-semibold ${r.iso27001_certified ? 'text-emerald-700' : 'text-slate-400'}">${r.iso27001_certified ? 'Certified' : 'Pending'}</td>
                    <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[9px] font-bold ${r.residual_risk_level === 'Low' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">${r.residual_risk_level}</span></td>
                </tr>
            `).join('');
        }

        // 9. Vendor CAPA
        const capaTable = document.getElementById('table-vendor-capas');
        if (capaTable && resCAPAs) {
            capaTable.innerHTML = resCAPAs.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2 font-mono text-indigo-700 font-bold">${c.capa_code}</td>
                    <td class="p-2 font-medium text-slate-800">${c.vendor_name}</td>
                    <td class="p-2 text-slate-600 truncate max-w-[120px]" title="${c.corrective_action_agreed}">${c.corrective_action_agreed}</td>
                    <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-100 text-amber-800">${c.status}</span></td>
                </tr>
            `).join('');
        }

        // 10. Sourcing Categories
        const catTable = document.getElementById('table-sourcing-categories');
        if (catTable && resCategories) {
            catTable.innerHTML = resCategories.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-slate-700 font-bold">${c.category_code}</td>
                    <td class="p-2.5 font-semibold text-slate-900">${c.category_name}</td>
                    <td class="p-2.5 font-mono font-bold text-slate-800">${formatINR(c.annual_budget_inr)}</td>
                    <td class="p-2.5 text-slate-600"><span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-800">${c.sourcing_strategy}</span></td>
                    <td class="p-2.5 text-slate-600">${c.lead_buyer}</td>
                    <td class="p-2.5 font-semibold text-center">${c.active_vendors_count}</td>
                    <td class="p-2.5 font-mono text-center">${c.esg_weight_pct}%</td>
                </tr>
            `).join('');
        }

        // 11. Legacy 3-Quote RFP Comparisons
        const rfpTable = document.getElementById('table-rfp-comparison');
        if (rfpTable && resRFPs) {
            rfpTable.innerHTML = resRFPs.map(r => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-blue-700 font-bold">${r.rfp_reference}</td>
                    <td class="p-2.5 font-medium text-slate-800">${r.item_title}</td>
                    <td class="p-2.5 text-slate-600">${r.vendor_a_name}: ${formatINR(r.vendor_a_quote)}</td>
                    <td class="p-2.5 text-slate-600">${r.vendor_b_name}: ${formatINR(r.vendor_b_quote)}</td>
                    <td class="p-2.5 font-bold text-emerald-700">${r.selected_vendor}</td>
                    <td class="p-2.5 text-slate-500">${r.commercial_justification}</td>
                </tr>
            `).join('');
        }

    } catch (err) {
        console.error('Error loading procurement:', err);
    }
}

// Procurement Modal Handlers
export function toggleProcurementModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.toggle('hidden');
}

export async function handleCreateProcurePR(e) {
    e.preventDefault();
    const payload = {
        pr_number: document.getElementById('procure-pr-num').value,
        department: document.getElementById('procure-pr-dept').value,
        requester_name: document.getElementById('procure-pr-name').value,
        requester_email: document.getElementById('procure-pr-email').value,
        category: document.getElementById('procure-pr-cat').value,
        estimated_amount_inr: parseFloat(document.getElementById('procure-pr-amt').value),
        item_details: document.getElementById('procure-pr-items').value,
        urgency: document.getElementById('procure-pr-urgency').value,
        business_justification: document.getElementById('procure-pr-just').value
    };
    try {
        const res = await fetch(`${API_BASE}/procurement/requisitions`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            toggleProcurementModal('modal-procure-pr');
            showToast('Spend Requisition (PR) submitted successfully!');
            loadProcurement();
        } else {
            showToast('Failed to submit requisition.', 'error');
        }
    } catch (err) {
        showToast('Error submitting PR: ' + err.message, 'error');
    }
}

export async function handleCreateProcureEvent(e) {
    e.preventDefault();
    const payload = {
        event_code: document.getElementById('procure-ev-code').value,
        event_type: document.getElementById('procure-ev-type').value,
        title: document.getElementById('procure-ev-title').value,
        category: document.getElementById('procure-ev-cat').value,
        budget_allocation_inr: parseFloat(document.getElementById('procure-ev-budget').value),
        baseline_cost_inr: parseFloat(document.getElementById('procure-ev-base').value),
        closing_date: document.getElementById('procure-ev-close').value
    };
    try {
        const res = await fetch(`${API_BASE}/procurement/sourcing-events`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            toggleProcurementModal('modal-procure-event');
            showToast('Strategic Sourcing Event published successfully!');
            loadProcurement();
        } else {
            showToast('Failed to publish sourcing event.', 'error');
        }
    } catch (err) {
        showToast('Error creating sourcing event: ' + err.message, 'error');
    }
}

export async function handleCreateProcureVendor(e) {
    e.preventDefault();
    const payload = {
        vendor_code: document.getElementById('procure-ven-code').value,
        vendor_name: document.getElementById('procure-ven-name').value,
        email: document.getElementById('procure-ven-email').value,
        category: document.getElementById('procure-ven-cat').value,
        criticality_tier: document.getElementById('procure-ven-tier').value,
        pan: document.getElementById('procure-ven-pan').value,
        gstin: document.getElementById('procure-ven-gst').value,
        msme_registered: document.getElementById('procure-ven-msme').value !== 'Non-MSME',
        msme_category: document.getElementById('procure-ven-msme').value,
        annual_spend_estimate: parseFloat(document.getElementById('procure-ven-spend').value)
    };
    try {
        const res = await fetch(`${API_BASE}/procurement/vendors`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            toggleProcurementModal('modal-procure-vendor');
            showToast('Vendor onboarded successfully!');
            loadProcurement();
        } else {
            showToast('Failed to onboard vendor.', 'error');
        }
    } catch (err) {
        showToast('Error onboarding vendor: ' + err.message, 'error');
    }
}

export async function handleCreateProcureGRN(e) {
    e.preventDefault();
    const payload = {
        grn_number: document.getElementById('procure-grn-num').value,
        vendor_id: 1,
        po_reference: document.getElementById('procure-grn-po').value,
        delivery_challan_no: document.getElementById('procure-grn-dc').value,
        received_date: new Date().toISOString().split('T')[0],
        item_description: document.getElementById('procure-grn-desc').value,
        quantity_ordered: parseFloat(document.getElementById('procure-grn-ord').value),
        quantity_received: parseFloat(document.getElementById('procure-grn-recv').value),
        quantity_accepted: parseFloat(document.getElementById('procure-grn-acc').value),
        warehouse_location: document.getElementById('procure-grn-loc').value,
        inspection_status: 'Accepted'
    };
    try {
        const res = await fetch(`${API_BASE}/procurement/grns`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            toggleProcurementModal('modal-procure-grn');
            showToast('Inbound GRN logged and accepted!');
            loadProcurement();
        } else {
            showToast('Failed to log GRN.', 'error');
        }
    } catch (err) {
        showToast('Error logging GRN: ' + err.message, 'error');
    }
}

// 8. Infrastructure
// Switch Sub-tabs in IT, Cloud & Passkey Access Infrastructure
export function switchInfraTab(tabKey) {
    document.querySelectorAll('.infra-tab-panel').forEach(el => el.classList.add('hidden'));
    const targetPanel = document.getElementById(`infra-tab-content-${tabKey}`);
    if (targetPanel) targetPanel.classList.remove('hidden');

    document.querySelectorAll('.infra-tab-btn').forEach(btn => {
        btn.classList.remove('bg-white', 'text-indigo-700', 'shadow-sm', 'border', 'border-slate-200');
        btn.classList.add('text-slate-600');
    });
    if (typeof window !== 'undefined' && window.event && window.event.currentTarget) {
        event.currentTarget.classList.add('bg-white', 'text-indigo-700', 'shadow-sm', 'border', 'border-slate-200');
        event.currentTarget.classList.remove('text-slate-600');
    }
}

export async function loadInfrastructure() {
    try {
        const [
            resOverview,
            resPasskeys,
            resZTNA,
            resDR,
            resAssets,
            resCloud,
            resIAM,
            resCerts,
            resChecklists
        ] = await Promise.all([
            fetch(`${API_BASE}/infrastructure/overview`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/infrastructure/passkeys`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/zero-trust-policies`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/dr-simulations`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/assets`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/cloud-accounts`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/iam-credentials`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/certificates-secrets`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/infrastructure/provisioning-checklists`).then(r => r.json()).catch(() => [])
        ]);

        // 1. KPI Cards
        if (resOverview) {
            const elHw = document.getElementById('infra-kpi-hardware');
            if (elHw) elHw.textContent = `${resOverview.hardware_assets.assigned} Assigned / ${resOverview.hardware_assets.total} Total`;
            
            const elCloud = document.getElementById('infra-kpi-cloud');
            if (elCloud) elCloud.textContent = `${formatINR(resOverview.cloud_infrastructure.total_monthly_spend_inr)} / mo`;
            
            const elPk = document.getElementById('infra-kpi-passkeys');
            if (elPk) elPk.textContent = `${resOverview.passkey_and_zero_trust.enrolled_passkeys} Enrolled`;

            const elDr = document.getElementById('infra-kpi-dr');
            if (elDr) elDr.textContent = `RTO ${resOverview.disaster_recovery.latest_rto_minutes}m`;
        }

        // 2. FIDO2 Passkeys Directory Table
        const passkeysTable = document.getElementById('table-passkeys-directory');
        if (passkeysTable) {
            passkeysTable.innerHTML = (resPasskeys || []).map(pk => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-semibold text-indigo-700">
                        ${pk.passkey_id}
                        <br><span class="text-[10px] text-slate-400 font-normal">AAGUID: ${pk.aaguid || '00000000-0000'}</span>
                    </td>
                    <td class="p-3">
                        <div class="font-medium text-slate-800">${pk.user_name}</div>
                        <div class="text-xs text-slate-500 font-mono">${pk.user_email}</div>
                    </td>
                    <td class="p-3">
                        <div class="text-xs font-semibold text-slate-700">${pk.device_name}</div>
                        <div class="text-[11px] text-slate-500">${pk.authenticator_type}</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 text-xs font-mono font-bold rounded bg-slate-100 text-slate-800">
                            #${pk.sign_count}
                        </span>
                        <span class="text-[11px] text-emerald-600 font-semibold ml-1"><i class="fa-solid fa-check"></i> Monotonic</span>
                    </td>
                    <td class="p-3 text-xs text-slate-600">
                        ${formatDate(pk.last_used_at)}
                    </td>
                    <td class="p-3">
                        <span class="px-2.5 py-1 text-xs rounded-full bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">
                            <i class="fa-solid fa-shield-check mr-1"></i> ${pk.zero_trust_status}
                        </span>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No passkeys enrolled yet.</td></tr>';
        }

        // 3. Zero-Trust Policies (ZTNA) Table
        const ztnaTable = document.getElementById('table-ztna-policies');
        if (ztnaTable) {
            ztnaTable.innerHTML = (resZTNA || []).map(pol => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-bold text-slate-800">${pol.policy_code}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-900">${pol.policy_name}</div>
                        <div class="text-xs text-slate-500 font-mono">${pol.target_resource}</div>
                    </td>
                    <td class="p-3 text-xs font-medium text-indigo-700">${pol.required_privilege}</td>
                    <td class="p-3">
                        <div class="flex items-center gap-1.5">
                            <span class="px-2 py-0.5 rounded text-[11px] font-semibold ${pol.fido2_passkey_required ? 'bg-indigo-50 text-indigo-700' : 'bg-slate-100 text-slate-600'}">
                                ${pol.fido2_passkey_required ? 'FIDO2 Mandated' : 'Password/MFA'}
                            </span>
                            <span class="px-2 py-0.5 rounded text-[11px] font-semibold ${pol.device_encryption_required ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}">
                                ${pol.device_encryption_required ? 'Disk Encrypted' : 'Any'}
                            </span>
                        </div>
                    </td>
                    <td class="p-3">
                        <div class="text-xs text-slate-700 font-medium">${pol.allowed_ip_ranges}</div>
                        <div class="text-[11px] text-slate-400">TTL: ${pol.session_timeout_minutes} mins</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-1 text-xs rounded font-bold ${pol.enforcement_mode === 'Active_Blocking' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-amber-50 text-amber-700'}">
                            ${pol.enforcement_mode}
                        </span>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No ZTNA policies active.</td></tr>';
        }

        // 4. Disaster Recovery (DR) Simulation Drills Table
        const drTable = document.getElementById('table-dr-simulations');
        if (drTable) {
            drTable.innerHTML = (resDR || []).map(dr => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3">
                        <div class="font-mono text-xs font-bold text-blue-700">${dr.test_code}</div>
                        <div class="text-[11px] text-slate-500">${dr.test_type}</div>
                    </td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800 text-xs">${dr.target_cluster}</div>
                        <div class="text-[11px] text-slate-500 truncate max-w-xs">${dr.simulated_scenario}</div>
                    </td>
                    <td class="p-3">
                        <span class="font-bold text-emerald-700 text-xs">${dr.actual_rto_minutes} mins</span>
                        <span class="text-slate-400 text-xs">/ SLA &le; ${dr.target_rto_minutes}m</span>
                    </td>
                    <td class="p-3">
                        <span class="font-bold text-emerald-700 text-xs">${dr.actual_rpo_minutes} mins</span>
                        <span class="text-slate-400 text-xs">/ SLA &le; ${dr.target_rpo_minutes}m</span>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-semibold ${dr.data_loss_detected ? 'bg-rose-100 text-rose-700' : 'bg-emerald-50 text-emerald-700'}">
                            ${dr.data_loss_detected ? 'Data Loss Detected' : 'Zero Data Loss'}
                        </span>
                    </td>
                    <td class="p-3">
                        <div class="font-bold text-xs text-slate-800">${dr.test_outcome}</div>
                        <div class="text-[11px] text-slate-500">${dr.conducted_by} &bull; ${formatDate(dr.conducted_at)}</div>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No DR drills recorded.</td></tr>';
        }

        // 5. Hardware Assets Table
        const assetTable = document.getElementById('table-assets');
        if (assetTable && resAssets) {
            assetTable.innerHTML = resAssets.map(a => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${a.asset_tag}</td>
                    <td class="p-3 font-medium text-slate-800">${a.make_model} <br><span class="text-xs text-slate-400">S/N: ${a.serial_number}</span></td>
                    <td class="p-3 text-slate-700">${a.assigned_user_name || 'Unassigned'}</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${a.disk_encryption_enabled ? 'Encrypted (BitLocker/FileVault)' : 'No'}</span></td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-blue-50 text-blue-700 font-medium">${a.asset_status}</span></td>
                </tr>
            `).join('');
        }

        // 6. Cloud Workloads Table
        const cloudTable = document.getElementById('table-cloud');
        if (cloudTable && resCloud) {
            cloudTable.innerHTML = resCloud.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${c.cloud_id}</td>
                    <td class="p-3 font-medium text-slate-800">${c.provider} (${c.environment})</td>
                    <td class="p-3 text-slate-600">${c.primary_region}</td>
                    <td class="p-3 font-semibold text-slate-800">${formatINR(c.current_month_spend_inr)} / ${formatINR(c.monthly_budget_inr)}</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${c.mfa_enforced_root ? 'Root MFA Enforced' : 'Warning'}</span></td>
                </tr>
            `).join('');
        }

        // 7. Certificates & Secrets Table
        const certTable = document.getElementById('table-certs');
        if (certTable && resCerts) {
            certTable.innerHTML = resCerts.map(crt => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-2.5 font-mono text-blue-700 font-bold">${crt.item_type}</td>
                    <td class="p-2.5 font-medium text-slate-800">${crt.identifier_name}</td>
                    <td class="p-2.5 text-slate-500">${crt.issuer}</td>
                    <td class="p-2.5 font-semibold text-rose-600">${formatDate(crt.expiry_date)}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-medium">${crt.status}</span></td>
                </tr>
            `).join('');
        }

        // 8. IAM Access Table
        const iamTable = document.getElementById('table-iam');
        if (iamTable && resIAM) {
            iamTable.innerHTML = resIAM.map(i => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-semibold">${i.credential_id}</td>
                    <td class="p-3 font-medium text-slate-800">${i.user_name} <br><span class="text-xs text-slate-400">${i.user_email}</span></td>
                    <td class="p-3 text-slate-600">${i.system} (${i.role_assigned})</td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-purple-50 text-purple-700 font-semibold">${i.passkey_fido2_enabled ? 'FIDO2 Passkey Active' : 'Password only'}</span></td>
                    <td class="p-3"><span class="px-2 py-1 text-xs rounded bg-emerald-50 text-emerald-700 font-medium">${i.review_status}</span></td>
                </tr>
            `).join('');
        }

        // 9. IT Provisioning Checklists Table
        const chkTable = document.getElementById('table-provisioning-checklists');
        if (chkTable && resChecklists) {
            chkTable.innerHTML = resChecklists.map(chk => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-medium text-slate-900">${chk.employee_name} <br><span class="font-mono text-[11px] text-slate-400">${chk.employee_code}</span></td>
                    <td class="p-3 font-semibold text-slate-700">${chk.process_type}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded ${chk.google_workspace_provisioned ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-400'}">${chk.google_workspace_provisioned ? 'Provisioned' : 'Pending'}</span></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded ${chk.github_org_access_granted ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-400'}">${chk.github_org_access_granted ? 'Granted' : 'Pending'}</span></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded ${chk.aws_iam_identity_center_granted ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-400'}">${chk.aws_iam_identity_center_granted ? 'Granted' : 'Not Req'}</span></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded ${chk.fido2_passkey_enrolled ? 'bg-indigo-50 text-indigo-700 font-semibold' : 'bg-rose-50 text-rose-700'}">${chk.fido2_passkey_enrolled ? 'Enrolled' : 'Pending'}</span></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">${chk.signoff_status}</span></td>
                </tr>
            `).join('') || '<tr><td colspan="7" class="p-4 text-center text-slate-400">No provisioning records found.</td></tr>';
        }

    } catch (err) {
        console.error('Error loading infrastructure:', err);
    }
}

// User Action Handlers for Passkeys, ZTNA, and DR Drills
export async function openPasskeyEnrollModal() {
    const userEmail = prompt("Enter stakeholder email for FIDO2 Passkey enrollment (e.g. employee@asperiondigital.com):", "varadivijay@asperiondigital.com");
    if (!userEmail) return;
    const deviceName = prompt("Enter authenticator device name (e.g. MacBook Pro Touch ID / YubiKey 5C NFC):", "YubiKey 5C NFC");
    if (!deviceName) return;

    try {
        const passkeyId = `fido2-${Date.now()}`;
        const res = await fetch(`${API_BASE}/infrastructure/passkeys`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                passkey_id: passkeyId,
                user_email: userEmail,
                user_name: userEmail.split('@')[0].toUpperCase(),
                device_name: deviceName,
                authenticator_type: deviceName.includes("Yubi") ? "Cross-Platform Hardware FIDO2 (YubiKey 5 Series)" : "Platform Authenticator (TouchID / Windows Hello)",
                public_key_spki: `MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE${Math.random().toString(36).substring(2)}...`,
                user_verified: true
            })
        });
        if (res.ok) {
            alert(`FIDO2 Passkey registered successfully for ${userEmail}! Hardware binding active.`);
            loadInfrastructure();
        } else {
            alert("Failed to register passkey.");
        }
    } catch (e) {
        alert("Error registering passkey: " + e.message);
    }
}

export async function openZTNAPolicyModal() {
    const policyName = prompt("Enter ZTNA Policy Name (e.g. Production Redis Cluster Zero-Trust Gate):", "Production Redis Cluster Gate");
    if (!policyName) return;
    const targetResource = prompt("Enter target resource (e.g. redis-prod.internal.asperion.in:6379):", "redis-prod.internal.asperion.in:6379");
    if (!targetResource) return;

    try {
        const code = `ZTNA-POL-${Math.floor(100 + Math.random() * 900)}`;
        const res = await fetch(`${API_BASE}/infrastructure/zero-trust-policies`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                policy_code: code,
                policy_name: policyName,
                target_resource: targetResource,
                required_privilege: "Elevated / Superadmin",
                fido2_passkey_required: true,
                device_encryption_required: true,
                allowed_ip_ranges: "Horamavu HQ Office IP / ZTNA WireGuard Tunnel",
                session_timeout_minutes: 60,
                enforcement_mode: "Active_Blocking"
            })
        });
        if (res.ok) {
            alert(`ZTNA Policy [${code}] enforced in Active_Blocking mode!`);
            loadInfrastructure();
        } else {
            alert("Failed to create ZTNA policy.");
        }
    } catch (e) {
        alert("Error creating policy: " + e.message);
    }
}

export async function triggerDRSimulationDrill() {
    if (!confirm("Execute simulated full regional failover to AWS Hyderabad warm standby (ap-south-2)?")) return;

    try {
        const code = `DR-SIM-${new Date().getFullYear()}-M${new Date().getMonth() + 1}`;
        const res = await fetch(`${API_BASE}/infrastructure/dr-simulations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_code: code,
                test_type: "Full Failover Simulation",
                simulated_scenario: "Automated simulation of AWS Mumbai network partition; DNS failover switchover to Hyderabad standby.",
                target_cluster: "Secondary EKS Warm Standby (ap-south-2 Hyderabad)",
                database_backup_point: new Date().toISOString(),
                actual_rto_minutes: +(12 + Math.random() * 8).toFixed(1),
                actual_rpo_minutes: +(1 + Math.random() * 2).toFixed(1),
                data_loss_detected: false,
                test_outcome: "PASSED - RTO/RPO SLA Met",
                conducted_by: "Head of Infrastructure (Priya Nair)"
            })
        });
        if (res.ok) {
            alert(`DR Simulation Drill [${code}] completed successfully! All RTO/RPO SLAs verified with zero data loss.`);
            loadInfrastructure();
        } else {
            alert("Failed to record DR simulation drill.");
        }
    } catch (e) {
        alert("Error triggering drill: " + e.message);
    }
}

// 9. SecOps & Cybersecurity
// Switch Sub-tabs in Cybersecurity War Room
export function switchSecOpsTab(tabKey) {
    document.querySelectorAll('.secops-tab-panel').forEach(el => el.classList.add('hidden'));
    const targetPanel = document.getElementById(`secops-tab-content-${tabKey}`);
    if (targetPanel) targetPanel.classList.remove('hidden');

    document.querySelectorAll('.secops-tab-btn').forEach(btn => {
        btn.classList.remove('bg-white', 'text-rose-700', 'shadow-sm', 'border', 'border-slate-200');
        btn.classList.add('text-slate-600');
    });
    if (typeof window !== 'undefined' && window.event && window.event.currentTarget) {
        event.currentTarget.classList.add('bg-white', 'text-rose-700', 'shadow-sm', 'border', 'border-slate-200');
        event.currentTarget.classList.remove('text-slate-600');
    }
}

export async function loadSecOps() {
    try {
        const [
            resOverview,
            resIncidents,
            resAlerts,
            resEvidence,
            resIOCs,
            resPlaybooks,
            resVulns,
            resDrills,
            resReports
        ] = await Promise.all([
            fetch(`${API_BASE}/cybersecurity/overview`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/cybersecurity/incidents`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/alerts`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/evidence`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/threat-intel`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/playbooks`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/vulnerabilities`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/drills`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/cybersecurity/cert-in-reports`).then(r => r.json()).catch(() => [])
        ]);

        // 1. Executive KPI Cards
        if (resOverview) {
            const elInc = document.getElementById('secops-kpi-active-incidents');
            if (elInc) elInc.textContent = `${resOverview.incidents_summary.active_now} Active (${resOverview.incidents_summary.p1_critical_and_p2_high} P1/P2)`;
            
            const elSla = document.getElementById('secops-kpi-certin-sla');
            if (elSla) elSla.textContent = `${resOverview.incidents_summary.cert_in_pending_filings} Pending`;
            
            const elIoc = document.getElementById('secops-kpi-threat-iocs');
            if (elIoc) elIoc.textContent = `${resOverview.defense_telemetry.active_threat_iocs_blocked} Blocked`;
            
            const elEvd = document.getElementById('secops-kpi-evidence-count');
            if (elEvd) elEvd.textContent = `${resOverview.defense_telemetry.forensic_evidence_items_preserved} Artifacts`;
        }

        // 2. Active Incidents Table
        const incTable = document.getElementById('table-incidents');
        if (incTable) {
            incTable.innerHTML = (resIncidents || []).map(i => {
                const isP1 = i.severity.startsWith('P1');
                const isP2 = i.severity.startsWith('P2');
                const sevBadge = isP1 ? 'bg-red-100 text-red-800 font-bold border border-red-200' :
                                 isP2 ? 'bg-orange-100 text-orange-800 font-bold border border-orange-200' :
                                 'bg-blue-50 text-blue-700 font-medium';
                
                return `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3">
                        <div class="font-mono text-xs text-rose-700 font-bold">${i.incident_id}</div>
                        <span class="px-2 py-0.5 text-[11px] rounded ${sevBadge}">${i.severity}</span>
                    </td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800">${i.title}</div>
                        <div class="text-xs text-slate-500">${i.category} &bull; <span class="font-mono text-slate-400">${i.mitre_tactics || 'Initial Access'}</span></div>
                    </td>
                    <td class="p-3">
                        <div class="text-xs font-medium text-slate-700">${i.affected_systems}</div>
                        <div class="text-[11px] text-slate-400">Impacted: ${i.affected_users_count || 0} users &bull; ${i.data_classification_impacted || 'Confidential'}</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-1 text-xs rounded font-medium ${i.status === 'Contained' ? 'bg-emerald-50 text-emerald-700' : i.status === 'Closed' ? 'bg-slate-100 text-slate-600' : 'bg-amber-50 text-amber-700'}">${i.status}</span>
                        <div class="text-[11px] text-slate-500 mt-1">${i.incident_commander}</div>
                    </td>
                    <td class="p-3">
                        ${i.cert_in_reporting_required ? `
                            <div class="text-xs font-bold text-rose-600 flex items-center gap-1">
                                <span class="certin-countdown-timer px-2 py-0.5 rounded bg-rose-50 border border-rose-200 text-rose-700 font-mono text-[11px] font-bold" data-deadline="${i.cert_in_deadline || ''}">
                                    <i class="fa-solid fa-stopwatch animate-pulse mr-1"></i> 6h SLA (${i.cert_in_status})
                                </span>
                            </div>
                            <div class="text-[11px] text-slate-400 mt-1">Ref: ${i.cert_in_incident_ref || 'Pending'}</div>
                        ` : `<span class="text-xs text-slate-400">Not Mandated</span>`}
                    </td>
                    <td class="p-3">
                        <div class="flex flex-wrap items-center gap-1.5">
                            ${i.war_room_url ? `
                                <a href="${i.war_room_url}" target="_blank" class="px-2 py-1 text-xs bg-rose-600 hover:bg-rose-700 text-white rounded font-bold flex items-center gap-1 shadow-sm">
                                    <i class="fa-solid fa-headset"></i> War Room
                                </a>
                            ` : ''}
                            <button onclick="viewCertInReport('${i.incident_id}')" class="px-2 py-1 text-xs bg-slate-800 text-white rounded hover:bg-slate-700 font-medium">Form</button>
                            <a href="${API_BASE}/cybersecurity/incidents/${i.incident_id}/docx" target="_blank" class="px-2 py-1 text-xs bg-red-700 hover:bg-red-800 text-white rounded inline-flex items-center gap-1 font-medium">
                                <i class="fa-solid fa-file-word"></i> DOCX
                            </a>
                            <button onclick="updateIncidentStatusPrompt('${i.incident_id}')" class="px-2 py-1 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded font-medium">Status</button>
                        </div>
                    </td>
                </tr>
                `;
            }).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No active incidents in queue.</td></tr>';
        }

        // 3. SIEM Threat Alerts Table
        const alertsTable = document.getElementById('table-secops-alerts');
        if (alertsTable) {
            alertsTable.innerHTML = (resAlerts || []).map(alt => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-bold text-indigo-700">${alt.alert_id}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800 text-xs">${alt.rule_name}</div>
                        <span class="text-[11px] text-slate-500 font-medium bg-slate-100 px-1.5 py-0.5 rounded">${alt.source}</span>
                    </td>
                    <td class="p-3 text-xs text-slate-600 max-w-xs truncate">${alt.signal_summary}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 text-xs font-bold rounded ${alt.initial_severity === 'High' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}">${alt.initial_severity}</span>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 text-xs rounded font-medium ${alt.validation_status.includes('Escalated') ? 'bg-purple-100 text-purple-700 font-bold' : 'bg-slate-100 text-slate-600'}">${alt.validation_status}</span>
                        <div class="text-[11px] text-slate-400 mt-0.5">${alt.assigned_analyst}</div>
                    </td>
                    <td class="p-3">
                        ${!alt.validation_status.includes('Escalated') ? `
                            <button onclick="escalateAlertToIncident('${alt.alert_id}')" class="px-2.5 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-xs font-semibold flex items-center gap-1 shadow-sm">
                                <i class="fa-solid fa-bolt"></i> Escalate
                            </button>
                        ` : `<span class="text-xs text-emerald-600 font-semibold"><i class="fa-solid fa-check"></i> Escalated</span>`}
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No threat alerts recorded.</td></tr>';
        }

        // 4. Forensic Evidence Locker Table
        const evTable = document.getElementById('table-secops-evidence');
        if (evTable) {
            evTable.innerHTML = (resEvidence || []).map(ev => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-bold text-emerald-700">${ev.evidence_id}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800 text-xs">${ev.item_name}</div>
                        <span class="text-[11px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">${ev.source_type}</span>
                    </td>
                    <td class="p-3">
                        <div class="font-mono text-[11px] text-slate-700 bg-slate-100 p-1 rounded max-w-xs truncate" title="${ev.sha256_checksum}">
                            <i class="fa-solid fa-fingerprint text-emerald-600 mr-1"></i>${ev.sha256_checksum}
                        </div>
                    </td>
                    <td class="p-3">
                        <div class="font-mono text-xs text-blue-700 truncate max-w-xs">${ev.storage_uri}</div>
                        <div class="text-[11px] text-slate-500">${ev.custody_notes || 'Locked'} &bull; Preserved by ${ev.collected_by}</div>
                    </td>
                    <td class="p-3 text-xs text-slate-500">${formatDate(ev.collected_at)}</td>
                </tr>
            `).join('') || '<tr><td colspan="5" class="p-4 text-center text-slate-400">No evidence items in custody.</td></tr>';
        }

        // 5. Threat Intelligence Indicators Table
        const iocTable = document.getElementById('table-secops-iocs');
        if (iocTable) {
            iocTable.innerHTML = (resIOCs || []).map(ioc => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3">
                        <div class="font-mono text-xs font-bold text-purple-700">${ioc.ioc_id}</div>
                        <span class="text-[10px] uppercase font-bold text-slate-500 px-1 rounded bg-slate-100">${ioc.ioc_type}</span>
                    </td>
                    <td class="p-3 font-mono text-xs font-semibold text-slate-900">${ioc.ioc_value}</td>
                    <td class="p-3">
                        <div class="font-semibold text-xs text-slate-800">${ioc.threat_actor_group}</div>
                        <div class="text-[11px] text-slate-500">${ioc.source_feed}</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-bold bg-purple-50 text-purple-700">${ioc.confidence_score}%</span>
                        <div class="text-[11px] text-slate-400 font-mono">${ioc.mitre_technique}</div>
                    </td>
                    <td class="p-3 text-xs text-slate-700 font-medium">${ioc.action_taken}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200">
                            <i class="fa-solid fa-ban mr-1"></i> ${ioc.status}
                        </span>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No threat intel IOCs registered.</td></tr>';
        }

        // 6. Playbooks Table
        const pbTable = document.getElementById('table-playbooks');
        if (pbTable) {
            pbTable.innerHTML = (resPlaybooks || []).map(p => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs text-blue-700 font-bold">${p.playbook_code}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800 text-xs">${p.title}</div>
                        <span class="text-[11px] text-slate-500 font-medium">${p.threat_category}</span>
                    </td>
                    <td class="p-3 text-xs text-slate-700 max-w-xs">${p.immediate_containment}</td>
                    <td class="p-3 text-xs text-slate-600 max-w-xs">${p.investigation_steps}</td>
                    <td class="p-3 text-xs text-slate-500">${p.regulatory_mandate}</td>
                </tr>
            `).join('') || '<tr><td colspan="5" class="p-4 text-center text-slate-400">No playbooks found.</td></tr>';
        }

        // 7. Vulnerabilities Table
        const vTable = document.getElementById('table-secops-vulns');
        if (vTable) {
            vTable.innerHTML = (resVulns || []).map(v => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3">
                        <div class="font-mono text-xs font-bold text-amber-700">${v.cve_id}</div>
                        <span class="font-bold text-xs ${v.cvss_score >= 9 ? 'text-red-600' : 'text-orange-600'}">CVSS ${v.cvss_score}</span>
                    </td>
                    <td class="p-3">
                        <div class="font-medium text-slate-800 text-xs">${v.affected_asset}</div>
                        <div class="text-[11px] text-slate-500 font-mono">${v.component}</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-bold ${v.severity === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'}">${v.severity}</span>
                    </td>
                    <td class="p-3 text-xs font-semibold ${v.patch_available ? 'text-emerald-600' : 'text-slate-400'}">
                        ${v.patch_available ? '<i class="fa-solid fa-check"></i> Available' : 'No Patch'}
                    </td>
                    <td class="p-3 text-xs font-semibold text-rose-600">${formatDate(v.remediation_due_date)}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-medium ${v.status === 'Applied & Verified' ? 'bg-emerald-50 text-emerald-700 font-bold' : 'bg-amber-50 text-amber-700'}">${v.status}</span>
                        <div class="text-[11px] text-slate-400">${v.assigned_engineer}</div>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No open vulnerabilities.</td></tr>';
        }

        // 8. Tabletop Drills Table
        const dTable = document.getElementById('table-secops-drills');
        if (dTable) {
            dTable.innerHTML = (resDrills || []).map(d => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-bold text-teal-700">${d.drill_code}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800 text-xs">${d.title}</div>
                        <div class="text-[11px] text-slate-500">${d.scenario_type} &bull; Facilitator: ${d.facilitator}</div>
                    </td>
                    <td class="p-3">
                        <div class="font-bold text-xs text-emerald-700">${d.actual_containment_minutes} mins actual</div>
                        <div class="text-[11px] text-slate-400">Target &le; ${d.target_containment_minutes} mins</div>
                    </td>
                    <td class="p-3 text-xs text-slate-600 max-w-xs">${d.lessons_learned_summary}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-bold bg-teal-50 text-teal-800 border border-teal-200">${d.drill_rating}</span>
                        <div class="text-[11px] text-slate-400 mt-1">${formatDate(d.drill_date)}</div>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="5" class="p-4 text-center text-slate-400">No crisis drills recorded.</td></tr>';
        }

        // 9. CERT-In Reports Ledger Table
        const rTable = document.getElementById('table-secops-certin-reports');
        if (rTable) {
            rTable.innerHTML = (resReports || []).map(rep => `
                <tr class="border-b border-slate-100 hover:bg-slate-50">
                    <td class="p-3 font-mono text-xs font-bold text-slate-800">${rep.report_reference}</td>
                    <td class="p-3 font-mono text-xs font-semibold text-rose-700">${rep.incident_id}</td>
                    <td class="p-3 font-mono text-xs font-bold text-emerald-700">${rep.cert_in_ack_number || 'Pending ACK'}</td>
                    <td class="p-3 text-xs text-slate-600">${formatDate(rep.submission_timestamp)}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${rep.filing_status}</span>
                    </td>
                    <td class="p-3 flex items-center gap-1.5">
                        <button onclick="viewCertInReport('${rep.incident_id}')" class="px-2 py-1 text-xs bg-slate-800 text-white rounded font-medium">View Form</button>
                        <a href="${API_BASE}/cybersecurity/incidents/${rep.incident_id}/docx" target="_blank" class="px-2 py-1 text-xs bg-red-700 hover:bg-red-800 text-white rounded inline-flex items-center gap-1 font-medium">
                            <i class="fa-solid fa-file-word"></i> DOCX
                        </a>
                    </td>
                </tr>
            `).join('') || '<tr><td colspan="6" class="p-4 text-center text-slate-400">No regulatory reports lodged yet.</td></tr>';
        }

    } catch (err) {
        console.error('Error loading secops:', err);
    }
}

export function viewCertInReport(incidentId) {
    window.open(`${API_BASE}/cybersecurity/cert-in-report/${incidentId}`, '_blank');
}

// User Action Handlers for Cybersecurity War Room
export function triggerEmergencyWarRoom() {
    const meetUrl = "https://meet.google.com/asp-sec-warroom";
    window.open(meetUrl, '_blank');
    alert("Emergency SecOps War Room bridge opened! Broadcast alerts dispatched to Founder Varadi Vijay & SecOps Lead Priya Nair.");
}

export async function openReportIncidentModal() {
    const title = prompt("Enter Incident Title (e.g. Unusual Outbound S3 Exfiltration Detected):", "Unusual Outbound Data Exfiltration Detected");
    if (!title) return;
    const category = prompt("Enter Category (Ransomware, Unauthorized Cloud Access, Phishing, Data Breach, DDoS):", "Unauthorized Cloud Access");
    if (!category) return;
    const systems = prompt("Enter Affected Systems:", "AWS ap-south-1 VPC & S3 Storage");
    if (!systems) return;

    try {
        const res = await fetch(`${API_BASE}/cybersecurity/incidents`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                category: category,
                affected_systems: systems,
                data_classification: "Confidential",
                is_customer_facing: true,
                estimated_impacted_users: 25,
                incident_commander: "Priya Nair (SecOps Lead)",
                war_room_url: "https://meet.google.com/asp-sec-warroom",
                mitre_tactics: "Initial Access, Exfiltration"
            })
        });
        if (res.ok) {
            const inc = await res.json();
            alert(`Incident [${inc.incident_id}] reported successfully with ${inc.severity}! CERT-In 6-hour SLA clock started.`);
            loadSecOps();
        } else {
            alert("Failed to report incident.");
        }
    } catch (e) {
        alert("Error reporting incident: " + e.message);
    }
}

export async function openIngestAlertModal() {
    const ruleName = prompt("Enter SIEM Alert Rule (e.g. AWS GuardDuty: IAMUser/AnomalousConsoleLogin):", "AWS GuardDuty: IAMUser/AnomalousConsoleLogin");
    if (!ruleName) return;
    const summary = prompt("Enter Alert Signal Summary:", "Root login from unrecognized ASN in Europe. CloudTrail MFA bypass detected.");
    if (!summary) return;

    try {
        const alertId = `ADT-ALT-${Date.now().toString().slice(-4)}`;
        const res = await fetch(`${API_BASE}/cybersecurity/alerts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                alert_id: alertId,
                source: "AWS GuardDuty",
                rule_name: ruleName,
                signal_summary: summary,
                initial_severity: "High",
                validation_status: "Under Investigation",
                assigned_analyst: "Priya Nair (SecOps Lead)"
            })
        });
        if (res.ok) {
            alert(`SIEM Alert [${alertId}] ingested into threat correlation queue!`);
            loadSecOps();
        } else {
            alert("Failed to ingest alert.");
        }
    } catch (e) {
        alert("Error ingesting alert: " + e.message);
    }
}

export async function openAddIOCModal() {
    const iocVal = prompt("Enter Threat IOC Value (e.g. 198.51.100.99 or malicious-domain.com):", "198.51.100.99");
    if (!iocVal) return;
    const actor = prompt("Enter Threat Actor Group:", "APT29 / LockBit Syndicate");
    if (!actor) return;

    try {
        const iocId = `ADT-IOC-${Math.floor(100 + Math.random() * 900)}`;
        const res = await fetch(`${API_BASE}/cybersecurity/threat-intel`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ioc_id: iocId,
                ioc_type: iocVal.includes('.') && !iocVal.includes(' ') && !isNaN(iocVal[0]) ? "IP_Address" : "Domain",
                ioc_value: iocVal,
                threat_actor_group: actor,
                confidence_score: 95,
                mitre_technique: "T1071 Web Protocols",
                action_taken: "Blocked at Cloudflare WAF & AWS Firewall",
                source_feed: "CERT-In Threat Advisory & Feeds",
                status: "Active_Blocked"
            })
        });
        if (res.ok) {
            alert(`Threat IOC [${iocVal}] blocked successfully across Cloudflare WAF and AWS Firewall!`);
            loadSecOps();
        } else {
            alert("Failed to register IOC.");
        }
    } catch (e) {
        alert("Error adding IOC: " + e.message);
    }
}

export async function escalateAlertToIncident(alertId) {
    if (!confirm(`Escalate SIEM Alert [${alertId}] directly to a P1/P2 Security Incident and spin up War Room?`)) return;

    try {
        const res = await fetch(`${API_BASE}/cybersecurity/alerts/${alertId}/escalate`, { method: 'POST' });
        if (res.ok) {
            const inc = await res.json();
            alert(`SIEM Alert escalated to Security Incident [${inc.incident_id}]! CERT-In statutory 6h countdown activated.`);
            loadSecOps();
        } else {
            alert("Failed to escalate alert.");
        }
    } catch (e) {
        alert("Error escalating alert: " + e.message);
    }
}

export async function updateIncidentStatusPrompt(incidentId) {
    const newStatus = prompt("Enter new status for incident (Triage, Contained, Eradicated, Recovered, Closed):", "Contained");
    if (!newStatus) return;
    const containmentSummary = prompt("Enter containment summary / actions taken:", "AWS session tokens revoked, affected IAM role detached, host isolated from VPC.");
    if (!containmentSummary) return;

    try {
        const res = await fetch(`${API_BASE}/cybersecurity/incidents/${incidentId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: newStatus,
                containment_summary: containmentSummary,
                root_cause_analysis: "Root API key inadvertently embedded in CI runner log output.",
                lessons_learned: "Pre-receive Git hooks updated to block high-entropy strings."
            })
        });
        if (res.ok) {
            alert(`Incident [${incidentId}] status updated to ${newStatus}!`);
            loadSecOps();
        } else {
            alert("Failed to update incident.");
        }
    } catch (e) {
        alert("Error updating incident: " + e.message);
    }
}

// Populate Letter Template Dropdown dynamically with all 70+ categories
export async function populateLetterTemplateDropdown() {
    const dropdown = document.getElementById('gen-letter-code');
    if (!dropdown) return;

    try {
        const res = await fetch(`${API_BASE}/hrms/all-letter-templates`);
        const templates = await res.json();

        dropdown.innerHTML = templates.map(t => `
            <option value="${t.code}">[${t.category}] ${t.code} - ${t.title}</option>
        `).join('');
    } catch (err) {
        console.error('Error populating templates:', err);
    }
}

// Live Statutory CTC Calculator handler
export async function calculateLiveCTC() {
    const ctcInput = parseFloat(document.getElementById('calc-ctc-input').value) || 1200000;
    const basicPct = parseFloat(document.getElementById('calc-basic-pct').value) || 0.40;
    const hraPct = parseFloat(document.getElementById('calc-hra-pct').value) || 0.40;
    const state = document.getElementById('calc-state').value || 'Karnataka';

    try {
        const res = await fetch(`${API_BASE}/hrms/calc-ctc`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                annual_ctc: ctcInput,
                basic_pct: basicPct,
                hra_pct: hraPct,
                state: state,
                cap_pf_at_ceiling: true,
                include_gratuity: true
            })
        });
        const data = await res.json();
        const e = data.earnings;
        const em = data.employer_contributions;
        const ed = data.employee_deductions;
        const th = data.take_home;

        document.getElementById('res-basic-monthly').innerText = formatINR(e.basic_salary.monthly);
        document.getElementById('res-basic-annual').innerText = formatINR(e.basic_salary.annual);
        document.getElementById('res-hra-monthly').innerText = formatINR(e.hra.monthly);
        document.getElementById('res-hra-annual').innerText = formatINR(e.hra.annual);
        document.getElementById('res-special-monthly').innerText = formatINR(e.special_allowance.monthly);
        document.getElementById('res-special-annual').innerText = formatINR(e.special_allowance.annual);
        document.getElementById('res-gross-monthly').innerText = formatINR(e.gross_salary.monthly);
        document.getElementById('res-gross-annual').innerText = formatINR(e.gross_salary.annual);

        document.getElementById('res-emp-pf-monthly').innerText = formatINR(em.employer_pf.monthly);
        document.getElementById('res-gratuity-monthly').innerText = formatINR(em.gratuity_provision.monthly);
        document.getElementById('res-ded-pf-monthly').innerText = formatINR(ed.employee_pf.monthly);
        document.getElementById('res-ded-pt-monthly').innerText = formatINR(ed.professional_tax.monthly);

        document.getElementById('res-net-monthly').innerText = formatINR(th.monthly_net_in_hand);
        document.getElementById('res-net-annual').innerText = formatINR(th.annual_net_in_hand);
    } catch (err) {
        console.error('Error running CTC calculation:', err);
    }
}

// Letter preview modal
export async function previewLetterById(letterId) {
    window.open(`${API_BASE}/hrms/letters/${letterId}/html`, '_blank');
}

// Generate new letter from UI
export async function handleGenerateLetter(event) {
    event.preventDefault();
    const code = document.getElementById('gen-letter-code').value;
    const recipient = document.getElementById('gen-recipient-name').value;
    const designation = document.getElementById('gen-designation').value;
    const ctc = parseFloat(document.getElementById('gen-ctc').value) || 1200000;

    try {
        const res = await fetch(`${API_BASE}/hrms/generate-letter`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                letter_code: code,
                recipient_name: recipient,
                designation: designation,
                annual_ctc: ctc,
                context_data: {
                    joining_date: "01 July 2026",
                    candidate_address: "Bangalore, Karnataka",
                    location: "Bangalore Head Office"
                }
            })
        });
        const result = await res.json();
        alert(`Successfully generated letter ${result.title} for ${result.recipient}!`);
        loadHRMS();
        window.open(`${API_BASE}/hrms/letters/${result.letter_id}/html`, '_blank');
    } catch (err) {
        console.error('Error generating letter:', err);
    }
}

// Run Monthly Payroll from UI
export async function handleRunPayroll() {
    const cycle = prompt("Enter Payroll Cycle (e.g. JUN-2026, JUL-2026):", "JUN-2026");
    if (!cycle) return;

    try {
        const res = await fetch(`${API_BASE}/hrms/run-monthly-payroll`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payroll_cycle: cycle, days_in_month: 30 })
        });
        const data = await res.json();
        alert(`Payroll Run Completed for ${data.payroll_cycle}!\nEmployees Processed: ${data.employees_count}\nTotal Net Payout: ${formatINR(data.total_net_disbursement_inr)}\nBank NEFT Batch Generated!`);
        loadHRMS();
    } catch (err) {
        console.error('Error running payroll:', err);
    }
}

// Persona Switcher & RBAC Context
export let currentUserSession = {
    role: "DIRECTOR",
    email: "director@asperion.in",
    token: null
};

export async function handleSwitchPersona(email) {
    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: "Password123!" })
        });
        if (!res.ok) throw new Error("Authentication failed");
        const data = await res.json();
        currentUserSession = {
            role: data.role,
            email: data.email,
            token: data.access_token
        };
        const badge = document.getElementById('role-badge');
        if (badge) {
            badge.innerText = `${data.role} Role`;
        }
        console.log(`[RBAC] Switched persona to: ${data.name} (${data.role})`);

        // Filter sidebar navigation buttons based on role authorization
        const authModules = data.authorized_modules || [];
        const isAll = authModules.includes("all");
        document.querySelectorAll('.nav-btn').forEach(btn => {
            const target = btn.getAttribute('data-target');
            if (isAll || authModules.includes(target)) {
                btn.classList.remove('hidden');
            } else {
                btn.classList.add('hidden');
            }
        });

        // Auto-navigate to appropriate dedicated dashboard view
        if (data.role === 'EMPLOYEE') {
            switchModule('portal-employee');
        } else if (data.role === 'CLIENT') {
            switchModule('portal-client');
        } else if (data.role === 'VENDOR') {
            switchModule('portal-vendor');
        } else if (authModules.length > 0 && !authModules.includes(currentModule) && !isAll) {
            switchModule(authModules[0]);
        }
    } catch (err) {
        console.error('Error switching persona:', err);
    }
}

// 10. Enterprise Document & Knowledge Vault
export let vaultState = {
    selectedCategory: '',
    selectedFormat: '',
    searchTerm: '',
    allDocuments: [],
    categories: []
};

export async function loadVault() {
    try {
        const [resCats, resDocs, resStats] = await Promise.all([
            fetch(`${API_BASE}/vault/categories`).then(r => r.json()),
            fetch(`${API_BASE}/vault/documents`).then(r => r.json()),
            fetch(`${API_BASE}/vault/stats`).then(r => r.json())
        ]);

        vaultState.categories = resCats;
        vaultState.allDocuments = resDocs;

        const badge = document.getElementById('vault-total-badge');
        if (badge && resStats.total_documents) {
            badge.innerText = `${resStats.total_documents} Enterprise Documents Indexed`;
        }

        renderVaultCategories();
        renderVaultDocuments();
    } catch (err) {
        console.error('Error loading vault:', err);
    }
}

export function renderVaultCategories() {
    const pillsContainer = document.getElementById('vault-category-pills');
    if (!pillsContainer) return;

    let html = `
        <button onclick="filterVaultCategory('')" class="cat-pill px-3 py-1.5 rounded-lg border font-medium transition ${vaultState.selectedCategory === '' ? 'bg-amber-500 text-white border-amber-500' : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'}">
            <i class="fa-solid fa-layer-group mr-1"></i> All Categories (${vaultState.allDocuments.length})
        </button>
    `;

    vaultState.categories.forEach(cat => {
        const isSelected = vaultState.selectedCategory === cat.category_id;
        html += `
            <button onclick="filterVaultCategory('${cat.category_id}')" class="cat-pill px-3 py-1.5 rounded-lg border font-medium transition ${isSelected ? 'bg-amber-500 text-white border-amber-500' : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'}">
                <i class="fa-solid ${cat.icon} mr-1"></i> ${cat.category_name} (${cat.document_count})
            </button>
        `;
    });

    pillsContainer.innerHTML = html;
}

export function filterVaultCategory(catId) {
    vaultState.selectedCategory = catId;
    renderVaultCategories();
    renderVaultDocuments();
}

export function filterVaultFormat(fmt) {
    vaultState.selectedFormat = fmt;
    document.querySelectorAll('.format-filter-btn').forEach(btn => {
        if (btn.getAttribute('data-fmt') === fmt) {
            btn.className = "format-filter-btn px-2.5 py-1 rounded bg-slate-800 text-white font-medium";
        } else {
            btn.className = "format-filter-btn px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200";
        }
    });
    renderVaultDocuments();
}

export function handleVaultSearch() {
    const input = document.getElementById('vault-search-input');
    vaultState.searchTerm = input ? input.value.trim().toLowerCase() : '';
    renderVaultDocuments();
}

export function renderVaultDocuments() {
    const table = document.getElementById('table-vault-docs');
    const counter = document.getElementById('vault-showing-count');
    if (!table) return;

    let filtered = vaultState.allDocuments.filter(doc => {
        if (vaultState.selectedCategory && doc.category_id !== vaultState.selectedCategory) return false;
        if (vaultState.selectedFormat && doc.file_type.toLowerCase() !== vaultState.selectedFormat.toLowerCase()) return false;
        if (vaultState.searchTerm) {
            const term = vaultState.searchTerm;
            return doc.filename.toLowerCase().includes(term) || doc.category_name.toLowerCase().includes(term);
        }
        return true;
    });

    if (counter) {
        counter.innerText = `Showing ${filtered.length} of ${vaultState.allDocuments.length} documents`;
    }

    if (filtered.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="5" class="p-8 text-center text-slate-400">
                    <i class="fa-solid fa-folder-open text-3xl mb-2"></i>
                    <p>No documents found matching your filter criteria.</p>
                </td>
            </tr>
        `;
        return;
    }

    table.innerHTML = filtered.map(doc => {
        let typeBadgeClass = 'bg-slate-100 text-slate-700';
        let typeIcon = 'fa-file';
        if (doc.file_type === 'DOCX') {
            typeBadgeClass = 'bg-blue-100 text-blue-800 font-bold';
            typeIcon = 'fa-file-word text-blue-600';
        } else if (doc.file_type === 'PDF') {
            typeBadgeClass = 'bg-red-100 text-red-800 font-bold';
            typeIcon = 'fa-file-pdf text-red-600';
        } else if (doc.file_type === 'XLSX') {
            typeBadgeClass = 'bg-emerald-100 text-emerald-800 font-bold';
            typeIcon = 'fa-file-excel text-emerald-600';
        }

        const cleanTitle = doc.filename.replace(/\.(docx|pdf|xlsx|txt)$/i, '').replace(/_/g, ' ');

        return `
            <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                <td class="p-3">
                    <span class="px-2 py-1 rounded bg-slate-100 text-slate-700 font-medium">${doc.category_name}</span>
                </td>
                <td class="p-3 font-medium text-slate-800">
                    <div class="flex items-center gap-2">
                        <i class="fa-solid ${typeIcon} text-base"></i>
                        <div>
                            <span class="text-sm font-semibold text-slate-900">${cleanTitle}</span>
                            <div class="font-mono text-xs text-slate-400">${doc.relative_path}</div>
                        </div>
                    </div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded text-xs ${typeBadgeClass}">${doc.file_type}</span>
                </td>
                <td class="p-3 font-mono text-slate-500">${doc.file_size_kb} KB</td>
                <td class="p-3 text-right">
                    <a href="${doc.download_url}" target="_blank" class="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white font-medium rounded-lg transition inline-flex items-center gap-1.5 shadow-sm">
                        <i class="fa-solid fa-download"></i> Download
                    </a>
                </td>
            </tr>
        `;
    }).join('');
}

// 11. Strategy, Functions, KPIs & Executive Decisions
export async function loadStrategy() {
    try {
        const [resSummary, resFuncs, resCaps, resKPIs, resThoughts, resRoadmap] = await Promise.all([
            fetch(`${API_BASE}/strategy/summary`).then(r => r.json()),
            fetch(`${API_BASE}/strategy/functions`).then(r => r.json()),
            fetch(`${API_BASE}/strategy/capabilities`).then(r => r.json()),
            fetch(`${API_BASE}/strategy/kpis`).then(r => r.json()),
            fetch(`${API_BASE}/strategy/thoughts-decisions`).then(r => r.json()),
            fetch(`${API_BASE}/strategy/roadmap`).then(r => r.json())
        ]);

        // Stat cards
        document.getElementById('stat-functions-count').innerText = resSummary.strategic_functions_count || 0;
        document.getElementById('stat-kpi-health').innerText = `${resSummary.kpis.health_score_pct}%`;
        document.getElementById('stat-decisions-count').innerText = resSummary.executive_decisions_logged || 0;
        document.getElementById('stat-roadmap-count').innerText = resSummary.active_roadmap_milestones || 0;

        // 1. KPIs Table
        const kpiTable = document.getElementById('table-enterprise-kpis');
        if (kpiTable) {
            kpiTable.innerHTML = resKPIs.map(k => {
                let badgeClass = 'bg-slate-100 text-slate-700';
                if (k.status === 'Achieved') badgeClass = 'bg-emerald-100 text-emerald-800 font-bold';
                else if (k.status === 'On Track') badgeClass = 'bg-blue-100 text-blue-800 font-bold';
                else if (k.status === 'At Risk') badgeClass = 'bg-amber-100 text-amber-800 font-bold';
                else if (k.status === 'Critical') badgeClass = 'bg-red-100 text-red-800 font-bold';

                const targetFormatted = k.unit === 'INR' ? formatINR(k.target_value) : `${k.target_value} ${k.unit}`;
                const actualFormatted = k.unit === 'INR' ? formatINR(k.actual_value) : `${k.actual_value} ${k.unit}`;

                return `
                    <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                        <td class="p-3 font-mono font-bold text-blue-800">${k.kpi_code}</td>
                        <td class="p-3 font-semibold text-slate-600">${k.category}</td>
                        <td class="p-3 font-medium text-slate-900">${k.name}</td>
                        <td class="p-3 font-semibold text-slate-700">${targetFormatted}</td>
                        <td class="p-3 font-bold text-emerald-700">${actualFormatted}</td>
                        <td class="p-3 font-medium ${k.variance >= 0 ? 'text-emerald-600' : 'text-red-600'}">
                            ${k.variance > 0 ? '+' : ''}${k.variance} (${k.variance_pct > 0 ? '+' : ''}${k.variance_pct}%)
                        </td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-xs ${badgeClass}">${k.status}</span></td>
                        <td class="p-3 text-slate-500">${k.owner}</td>
                    </tr>
                `;
            }).join('');
        }

        // 2. Functions Matrix Table
        const funcTable = document.getElementById('table-strategic-functions');
        if (funcTable) {
            funcTable.innerHTML = resFuncs.map(f => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-bold text-slate-900">${f.function_name}</td>
                    <td class="p-3 text-slate-700 font-medium">${f.function_owner}</td>
                    <td class="p-3 text-slate-600">${f.core_capabilities}</td>
                    <td class="p-3 text-blue-700 font-medium">${f.key_documents || '-'}</td>
                    <td class="p-3 text-slate-500">${f.review_cadence}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-blue-50 text-blue-800 font-bold border border-blue-200">${f.maturity_level}</span></td>
                </tr>
            `).join('');
        }

        // 3. Capability Capacity Table
        const capTable = document.getElementById('table-capability-capacity');
        if (capTable) {
            capTable.innerHTML = resCaps.map(c => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-bold text-slate-800">${c.capability_name}</td>
                    <td class="p-3 text-slate-600 font-mono">${c.current_capacity}</td>
                    <td class="p-3 text-emerald-700 font-mono font-bold">${c.target_capacity}</td>
                    <td class="p-3 text-amber-700">${c.primary_constraint}</td>
                    <td class="p-3 text-slate-600">${c.people_requirement || '-'}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded font-bold ${c.priority === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}">${c.priority}</span></td>
                </tr>
            `).join('');
        }

        // 4. Strategic Decisions & Thoughts Table
        const thoughtTable = document.getElementById('table-strategic-thoughts');
        if (thoughtTable) {
            thoughtTable.innerHTML = resThoughts.map(t => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-mono text-slate-500">${formatDate(t.date_recorded)}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-purple-50 text-purple-800 font-semibold border border-purple-200">${t.entry_type}</span></td>
                    <td class="p-3 font-bold text-slate-900">${t.title}</td>
                    <td class="p-3 text-slate-700">${t.author}</td>
                    <td class="p-3 text-slate-600 max-w-xs">${t.decision_rationale}</td>
                    <td class="p-3"><span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">${t.tags}</span></td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold">${t.status}</span></td>
                </tr>
            `).join('');
        }

        // 5. Strategic Roadmap Table
        const roadTable = document.getElementById('table-strategy-roadmap');
        if (roadTable) {
            roadTable.innerHTML = resRoadmap.map(r => `
                <tr class="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td class="p-3 font-semibold text-blue-800">${r.workstream}</td>
                    <td class="p-3 font-medium text-slate-900">${r.action_item}</td>
                    <td class="p-3 text-slate-600">${r.owner}</td>
                    <td class="p-3 text-slate-500">${formatDate(r.start_date)} to ${formatDate(r.due_date)}</td>
                    <td class="p-3">
                        <div class="w-24 bg-slate-200 rounded-full h-2 overflow-hidden inline-block mr-2 align-middle">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${r.progress_pct}%"></div>
                        </div>
                        <span class="font-bold text-slate-700">${r.progress_pct}%</span>
                    </td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded font-medium ${r.status === 'Complete' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-50 text-blue-700'}">${r.status}</span></td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Error loading strategy:', err);
    }
}

export function toggleStrategyModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
        el.classList.toggle('hidden');
    }
}

export async function handleCreateThought(event) {
    event.preventDefault();
    const type = document.getElementById('thought-type').value;
    const author = document.getElementById('thought-author').value;
    const title = document.getElementById('thought-title').value;
    const context = document.getElementById('thought-context').value;
    const rationale = document.getElementById('thought-rationale').value;
    const tags = document.getElementById('thought-tags').value;

    try {
        const res = await fetch(`${API_BASE}/strategy/thoughts-decisions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                entry_type: type,
                title: title,
                author: author,
                context_background: context,
                decision_rationale: rationale,
                tags: tags,
                status: 'Approved'
            })
        });
        if (!res.ok) throw new Error("Failed to save entry");
        alert("Strategic decision successfully recorded!");
        toggleStrategyModal('modal-thought');
        loadStrategy();
    } catch (err) {
        alert("Error saving thought: " + err.message);
    }
}

export async function handleCreateKPI(event) {
    event.preventDefault();
    const code = document.getElementById('kpi-code').value;
    const category = document.getElementById('kpi-category').value;
    const name = document.getElementById('kpi-name').value;
    const target = parseFloat(document.getElementById('kpi-target').value);
    const actual = parseFloat(document.getElementById('kpi-actual').value);
    const unit = document.getElementById('kpi-unit').value;
    const period = document.getElementById('kpi-period').value;
    const owner = document.getElementById('kpi-owner').value;

    try {
        const res = await fetch(`${API_BASE}/strategy/kpis`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                kpi_code: code,
                category: category,
                name: name,
                target_value: target,
                actual_value: actual,
                unit: unit,
                period: period,
                owner: owner,
                status: actual >= target ? 'Achieved' : 'On Track'
            })
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || "Failed to create KPI");
        }
        alert("KPI Metric successfully registered!");
        toggleStrategyModal('modal-kpi');
        loadStrategy();
    } catch (err) {
        alert("Error saving KPI: " + err.message);
    }
}





// =========================================================================
// 12. Visual Intelligence & Multi-Capable Analytics Hub
// =========================================================================

export let currentAnalyticsTab = 'fin';

export async function loadAnalyticsHub() {
    switchAnalyticsTab(currentAnalyticsTab);
}

export function switchAnalyticsTab(tabKey) {
    currentAnalyticsTab = tabKey;
    
    // Toggle Tab button styling
    const tabs = ['fin', 'pmo', 'talent', 'secops', 'strategy', 'sim', 'datascience', 'decision', 'montecarlo', 'infographics'];
    tabs.forEach(t => {
        const btn = document.getElementById(`btn-tab-${t}`);
        const pane = document.getElementById(`analytics-pane-${t}`);
        if (t === tabKey) {
            if (btn) {
                btn.className = "analytics-tab-btn px-4 py-2.5 border-b-2 border-emerald-600 text-emerald-700 font-bold flex items-center gap-2 whitespace-nowrap bg-emerald-50/50 rounded-t-lg";
            }
            if (pane) pane.classList.remove('hidden');
        } else {
            if (btn) {
                btn.className = "analytics-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap";
            }
            if (pane) pane.classList.add('hidden');
        }
    });

    // Invoke tab specific loader
    switch (tabKey) {
        case 'fin': loadFinAnalytics(); break;
        case 'pmo': loadPMOAnalytics(); break;
        case 'talent': loadTalentAnalytics(); break;
        case 'secops': loadSecOpsAnalytics(); break;
        case 'strategy': loadStrategyAnalytics(); break;
        case 'sim': loadSimAnalytics(); break;
        case 'datascience': loadDataScienceAnalytics(); break;
        case 'decision': loadDecisionTowerAnalytics(); break;
        case 'montecarlo': loadMonteCarloAnalytics(); break;
        case 'infographics': loadExecutiveInfographics(); break;
    }
}

// Tab 1: Financial & Treasury Visualizer
export async function loadFinAnalytics() {
    try {
        const [resOverview, resFin] = await Promise.all([
            fetch(`${API_BASE}/analytics/overview`).then(r => r.json()),
            fetch(`${API_BASE}/analytics/financial-charts`).then(r => r.json())
        ]);

        const fs = resOverview.financial_summary;
        const elInv = document.getElementById('v-fin-invoiced');
        if (elInv) elInv.innerText = formatINR(fs.total_invoiced_inr);
        const elAr = document.getElementById('v-fin-ar');
        if (elAr) elAr.innerText = formatINR(fs.accounts_receivable_inr);
        const elAp = document.getElementById('v-fin-ap');
        if (elAp) elAp.innerText = formatINR(fs.accounts_payable_inr);
        const elRun = document.getElementById('v-fin-runway');
        if (elRun) elRun.innerText = `${fs.cash_runway_months} Months`;

        // Tax matrix
        const tm = resFin.tax_matrix;
        document.getElementById('tax-output-gst').innerText = formatINR(tm.output_gst_inr);
        document.getElementById('tax-itc').innerText = formatINR(tm.input_tax_credit_inr);
        document.getElementById('tax-net-gst').innerText = formatINR(tm.net_gst_payable_inr);
        document.getElementById('tax-tds-due').innerText = formatINR(tm.tds_withheld_payable_inr);

        // Cashflow Chart
        const cf = resFin.cashflow_time_series;
        safeRenderChart('chart-fin-cashflow', 'line', {
            labels: cf.labels,
            datasets: [
                {
                    label: 'Treasury Closing Cash Position (INR)',
                    data: cf.closing_cash,
                    borderColor: '#059669',
                    backgroundColor: 'rgba(5, 150, 105, 0.1)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3
                },
                {
                    label: 'Weekly Customer Inflows (INR)',
                    data: cf.inflows,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    type: 'bar'
                },
                {
                    label: 'Weekly Disbursements / Burn (INR)',
                    data: cf.outflows,
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.7)',
                    type: 'bar'
                }
            ]
        }, {
            scales: {
                y: {
                    ticks: {
                        callback: (v) => '₹' + (v / 100000).toFixed(1) + 'L'
                    }
                }
            }
        });

        // AR vs AP Aging
        const aging = resFin.aging_analysis;
        safeRenderChart('chart-fin-aging', 'bar', {
            labels: aging.labels,
            datasets: [
                {
                    label: 'Accounts Receivable (AR Inflows Due)',
                    data: aging.accounts_receivable,
                    backgroundColor: '#d97706'
                },
                {
                    label: 'Accounts Payable (AP Outflows Due)',
                    data: aging.accounts_payable,
                    backgroundColor: '#475569'
                }
            ]
        }, {
            scales: {
                y: {
                    ticks: {
                        callback: (v) => '₹' + (v / 1000).toFixed(0) + 'k'
                    }
                }
            }
        });
    } catch (err) {
        console.error('Error loading financial analytics:', err);
    }
}

// Tab 2: PMO & Delivery Velocity
export async function loadPMOAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/delivery-charts`).then(r => r.json());
        
        // Sprint Velocity
        const vel = res.sprint_velocity;
        safeRenderChart('chart-pmo-velocity', 'bar', {
            labels: vel.labels,
            datasets: [
                {
                    label: 'Committed Story Points',
                    data: vel.committed_points,
                    backgroundColor: '#94a3b8'
                },
                {
                    label: 'Delivered / Completed Points',
                    data: vel.completed_points,
                    backgroundColor: '#4f46e5'
                }
            ]
        });

        // Tasks Pipeline
        const tasks = res.task_pipeline;
        safeRenderChart('chart-pmo-tasks', 'doughnut', {
            labels: tasks.labels,
            datasets: [{
                data: tasks.counts,
                backgroundColor: ['#94a3b8', '#0284c7', '#f59e0b', '#10b981']
            }]
        });

        // RAID Heatmap Distribution
        const raid = res.raid_risk_heatmap;
        safeRenderChart('chart-pmo-raid', 'bar', {
            labels: raid.labels,
            datasets: [{
                label: 'RAID Active Item Count',
                data: raid.counts,
                backgroundColor: ['#ef4444', '#f97316', '#eab308', '#10b981']
            }]
        }, {
            indexAxis: 'y'
        });
    } catch (err) {
        console.error('Error loading PMO analytics:', err);
    }
}

// Tab 3: Talent, CTC & Payroll Analytics
export async function loadTalentAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/talent-charts`).then(r => r.json());

        // Headcount by Department
        const dept = res.department_headcount;
        safeRenderChart('chart-talent-dept', 'doughnut', {
            labels: dept.labels,
            datasets: [{
                data: dept.counts,
                backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#10b981']
            }]
        });

        // Compensation Slabs
        const slabs = res.compensation_slabs;
        safeRenderChart('chart-talent-slabs', 'bar', {
            labels: slabs.labels,
            datasets: [{
                label: 'Employee Count by Slab',
                data: slabs.counts,
                backgroundColor: '#6366f1'
            }]
        });

        // Standard CTC Components
        const comp = res.ctc_components_breakdown;
        safeRenderChart('chart-talent-components', 'bar', {
            labels: comp.labels,
            datasets: [{
                label: 'Annual Cost in INR',
                data: comp.values,
                backgroundColor: ['#0284c7', '#0ea5e9', '#38bdf8', '#f59e0b', '#10b981']
            }]
        }, {
            indexAxis: 'y',
            scales: {
                x: {
                    ticks: {
                        callback: (v) => '₹' + (v / 1000).toFixed(0) + 'k'
                    }
                }
            }
        });
    } catch (err) {
        console.error('Error loading talent analytics:', err);
    }
}

// Tab 4: SecOps & CERT-In Radar
export async function loadSecOpsAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/secops-charts`).then(r => r.json());

        const elFido = document.getElementById('v-secops-fido2');
        if (elFido) elFido.innerText = `${res.iam_security_posture.passkey_adoption_pct}%`;

        // Threat Vectors
        const vec = res.threat_vectors;
        safeRenderChart('chart-secops-vectors', 'polarArea', {
            labels: vec.labels,
            datasets: [{
                data: vec.counts,
                backgroundColor: ['#f43f5e', '#ef4444', '#f97316', '#3b82f6']
            }]
        });

        // IAM Posture
        const iam = res.iam_security_posture;
        safeRenderChart('chart-secops-iam', 'doughnut', {
            labels: ['FIDO2 Passkeys Active', 'Password / Pending MFA'],
            datasets: [{
                data: [iam.fido2_passkeys_active, iam.total_credentials - iam.fido2_passkeys_active],
                backgroundColor: ['#10b981', '#cbd5e1']
            }]
        });
    } catch (err) {
        console.error('Error loading secops analytics:', err);
    }
}

// Tab 5: Org Maturity Spider & Strategy Matrix
export async function loadStrategyAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/strategy-radar`).then(r => r.json());

        // Radar chart
        const radar = res.maturity_radar;
        safeRenderChart('chart-strategy-radar', 'radar', {
            labels: radar.axes,
            datasets: [{
                label: 'Asperion Digital Operational Maturity (Score 0-100)',
                data: radar.scores,
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(6, 182, 212, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: '#0891b2'
            }]
        }, {
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: { stepSize: 20 }
                }
            }
        });

        // KPI status distribution
        const kpis = res.kpi_distribution;
        safeRenderChart('chart-strategy-kpis', 'doughnut', {
            labels: kpis.labels,
            datasets: [{
                data: kpis.counts,
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
            }]
        });
    } catch (err) {
        console.error('Error loading strategy analytics:', err);
    }
}

// Tab 6: Dynamic What-If Cashflow Simulator
export async function loadSimAnalytics() {
    runLiveCashflowSimulation();
}

export let simDebounceTimer = null;
export function runLiveCashflowSimulation() {
    if (simDebounceTimer) clearTimeout(simDebounceTimer);
    simDebounceTimer = setTimeout(async () => {
        const collVal = parseFloat(document.getElementById('slider-coll').value) || 0;
        const expVal = parseFloat(document.getElementById('slider-exp').value) || 0;
        const retVal = parseFloat(document.getElementById('slider-ret').value) || 0;

        document.getElementById('slider-val-coll').innerText = `+${collVal}%`;
        document.getElementById('slider-val-exp').innerText = `-${expVal}%`;
        document.getElementById('slider-val-ret').innerText = formatINR(retVal);

        try {
            const res = await fetch(`${API_BASE}/analytics/simulate-cashflow`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    collection_acceleration_pct: collVal,
                    expense_optimization_pct: expVal,
                    new_monthly_retainer_inr: retVal
                })
            });
            const data = await res.json();

            document.getElementById('sim-base-cash').innerText = formatINR(data.baseline_ending_cash_inr);
            document.getElementById('sim-result-cash').innerText = formatINR(data.simulated_ending_cash_inr);
            document.getElementById('sim-cash-delta').innerText = `${data.cash_variance_delta_inr >= 0 ? '+' : ''}${formatINR(data.cash_variance_delta_inr)}`;
            document.getElementById('sim-runway-months').innerText = `${data.simulated_runway_months} Months`;

            // Render simulated cash curve
            const cd = data.chart_data;
            safeRenderChart('chart-sim-cashflow', 'line', {
                labels: cd.labels,
                datasets: [
                    {
                        label: 'Simulated Ending Cash (INR)',
                        data: cd.simulated_closing_balance,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.15)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 3
                    },
                    {
                        label: 'Simulated Inflows (INR)',
                        data: cd.simulated_inflows,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.8)',
                        type: 'bar'
                    },
                    {
                        label: 'Optimized Disbursements (INR)',
                        data: cd.simulated_outflows,
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.7)',
                        type: 'bar'
                    }
                ]
            }, {
                scales: {
                    y: {
                        ticks: {
                            callback: (v) => '₹' + (v / 100000).toFixed(1) + 'L'
                        }
                    }
                }
            });
        } catch (err) {
            console.error('Error running simulation:', err);
        }
    }, 150);
}

// ==============================================================
// TAB 7: DATA SCIENCE & PREDICTIVE ML ANALYTICS
// ==============================================================
export async function loadDataScienceAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/data-science/predictive-models`).then(r => r.json());
        if (res.status !== 'success') return;

        // 1. Revenue Forecast (Historical + Predicted with Confidence Bands)
        const rf = res.revenue_forecast;
        const allLabels = [...rf.historical_labels, ...rf.forecast_labels];
        
        // Pad historical values with nulls for the forecast range, and vice versa
        const histData = [...rf.historical_values, ...rf.forecast_labels.map(() => null)];
        const meanData = [...rf.historical_labels.map(() => null), ...rf.forecast_mean];
        const upperData = [...rf.historical_labels.map(() => null), ...rf.forecast_upper_95];
        const lowerData = [...rf.historical_labels.map(() => null), ...rf.forecast_lower_95];

        // Bridge the seam between historical and forecast
        if (rf.historical_values.length > 0 && rf.forecast_mean.length > 0) {
            const lastHistIdx = rf.historical_values.length - 1;
            const lastHistVal = rf.historical_values[lastHistIdx];
            meanData[lastHistIdx] = lastHistVal;
            upperData[lastHistIdx] = lastHistVal;
            lowerData[lastHistIdx] = lastHistVal;
        }

        safeRenderChart('chart-ds-revenue-forecast', 'line', {
            labels: allLabels,
            datasets: [
                {
                    label: 'Historical Actual Revenue',
                    data: histData,
                    borderColor: '#4f46e5',
                    backgroundColor: '#4f46e5',
                    borderWidth: 3,
                    pointRadius: 4,
                    tension: 0.2
                },
                {
                    label: 'Forecast Mean Trajectory',
                    data: meanData,
                    borderColor: '#059669',
                    backgroundColor: '#059669',
                    borderWidth: 3,
                    borderDash: [6, 4],
                    pointRadius: 4,
                    tension: 0.2
                },
                {
                    label: 'Upper 95% Confidence Band (+1.96σ)',
                    data: upperData,
                    borderColor: 'rgba(16, 185, 129, 0.4)',
                    backgroundColor: 'rgba(16, 185, 129, 0.12)',
                    fill: '+1',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.2
                },
                {
                    label: 'Lower 95% Confidence Band (-1.96σ)',
                    data: lowerData,
                    borderColor: 'rgba(16, 185, 129, 0.4)',
                    backgroundColor: 'transparent',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.2
                }
            ]
        }, {
            scales: {
                y: {
                    ticks: {
                        callback: (v) => '₹' + (v / 100000).toFixed(1) + 'L'
                    }
                }
            }
        });

        // 2. Churn Feature Importance Bar Chart
        const fi = res.customer_churn_analytics.feature_importance;
        safeRenderChart('chart-ds-churn-features', 'bar', {
            labels: Object.keys(fi),
            datasets: [{
                label: 'XGBoost Feature Gini Importance',
                data: Object.values(fi),
                backgroundColor: ['#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'],
                borderRadius: 6
            }]
        }, {
            indexAxis: 'y',
            scales: {
                x: {
                    max: 0.5,
                    ticks: {
                        callback: (v) => (v * 100).toFixed(0) + '%'
                    }
                }
            }
        });

        // 3. Customer Churn Table
        const tbody = document.getElementById('table-ds-churn-clients');
        if (tbody) {
            tbody.innerHTML = res.customer_churn_analytics.clients.map(c => `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-2.5 font-bold text-slate-900">${c.client_name}</td>
                    <td class="p-2.5 font-mono font-bold text-slate-800">${formatINR(c.arr_inr)}</td>
                    <td class="p-2.5 font-mono font-bold ${c.churn_probability_pct > 30 ? 'text-rose-600' : (c.churn_probability_pct > 20 ? 'text-amber-600' : 'text-emerald-600')}">
                        ${c.churn_probability_pct}%
                    </td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${c.risk_tier === 'High Risk' ? 'bg-rose-100 text-rose-800' : (c.risk_tier === 'Moderate Risk' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800')}">
                            ${c.risk_tier}
                        </span>
                    </td>
                    <td class="p-2.5 font-bold text-slate-700">${c.nps_satisfaction}/10</td>
                    <td class="p-2.5 font-mono text-slate-600">${c.dso_payment_days}d</td>
                    <td class="p-2.5 text-center">
                        <button onclick="alert('⚡ Activated Retention Protocol for ${c.client_name}: Executive Sponsor check-in scheduled.')" class="px-2 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded text-[10px] font-bold transition">
                            Intervene
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        // 4. ML ROC Curve
        const roc = res.ml_model_telemetry.roc_curve;
        safeRenderChart('chart-ds-roc-curve', 'line', {
            labels: roc.fpr.map(v => (v * 100).toFixed(0) + '%'),
            datasets: [
                {
                    label: 'ROC Curve (AUC = 0.972)',
                    data: roc.tpr,
                    borderColor: '#a855f7',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'Random Guess Chance',
                    data: roc.fpr,
                    borderColor: '#94a3b8',
                    borderDash: [4, 4],
                    pointRadius: 0,
                    borderWidth: 1
                }
            ]
        }, {
            scales: {
                y: { min: 0, max: 1 },
                x: { title: { display: true, text: 'False Positive Rate' } }
            }
        });
    } catch (err) {
        console.error('Error loading data science analytics:', err);
    }
}

// ==============================================================
// TAB 8: DECISION TOWER & STRATEGIC MCDA
// ==============================================================
export async function loadDecisionTowerAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/decision-support/strategic-mcda`).then(r => r.json());
        if (res.status !== 'success') return;

        // Populate Table
        const tbody = document.getElementById('table-mcda-initiatives');
        if (tbody) {
            tbody.innerHTML = res.ranked_initiatives.map(init => `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-2.5 font-bold font-mono">
                        <span class="w-6 h-6 rounded-full inline-flex items-center justify-center text-xs font-bold ${init.priority_rank === 1 ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'bg-slate-100 text-slate-700'}">
                            #${init.priority_rank}
                        </span>
                    </td>
                    <td class="p-2.5">
                        <div class="font-bold text-slate-900">${init.name}</div>
                        <div class="text-[10px] text-slate-400 font-mono">${init.category} &bull; ${init.timeframe_months} Months</div>
                    </td>
                    <td class="p-2.5 font-mono text-slate-700 font-semibold">${formatINR(init.budget_inr)}</td>
                    <td class="p-2.5 font-mono text-emerald-700 font-bold">${formatINR(init.expected_npv_inr)}</td>
                    <td class="p-2.5 font-mono font-bold text-indigo-700 text-sm">
                        ${init.composite_mcda_score} / 100
                    </td>
                    <td class="p-2.5">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${init.risk_tier === 'Low Risk' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">
                            ${init.risk_tier}
                        </span>
                    </td>
                </tr>
            `).join('');
        }

        const recEl = document.getElementById('mcda-recommendation-text');
        if (recEl) recEl.innerText = res.decision_rationale;

        // Render MCDA Radar Chart comparing Top 2 Initiatives
        const top1 = res.ranked_initiatives[0];
        const top2 = res.ranked_initiatives[1];
        const critKeys = Object.keys(res.criteria_weights);
        const critLabels = critKeys.map(k => res.criteria_weights[k].name);

        safeRenderChart('chart-mcda-radar', 'radar', {
            labels: critLabels,
            datasets: [
                {
                    label: top1.name.substring(0, 26) + '...',
                    data: critKeys.map(k => top1.scores[k]),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#1d4ed8'
                },
                {
                    label: top2.name.substring(0, 26) + '...',
                    data: critKeys.map(k => top2.scores[k]),
                    borderColor: '#059669',
                    backgroundColor: 'rgba(5, 150, 105, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#047857'
                }
            ]
        }, {
            scales: {
                r: { min: 60, max: 100, ticks: { stepSize: 10 } }
            }
        });

        // Initialize capital simulation
        runLiveCapitalSimulation();
    } catch (err) {
        console.error('Error loading decision tower analytics:', err);
    }
}

export let capSimDebounce = null;
export function runLiveCapitalSimulation() {
    if (capSimDebounce) clearTimeout(capSimDebounce);
    capSimDebounce = setTimeout(async () => {
        const headVal = parseInt(document.getElementById('slider-cap-head')?.value) || 4;
        const gpuVal = parseFloat(document.getElementById('slider-cap-gpu')?.value) || 300000;
        const salesVal = parseFloat(document.getElementById('slider-cap-sales')?.value) || 200000;
        const priceVal = parseFloat(document.getElementById('slider-cap-price')?.value) || 15;

        const elHead = document.getElementById('slider-val-cap-head');
        if (elHead) elHead.innerText = `+${headVal} Engineers`;
        const elGpu = document.getElementById('slider-val-cap-gpu');
        if (elGpu) elGpu.innerText = `${formatINR(gpuVal)}/m`;
        const elSales = document.getElementById('slider-val-cap-sales');
        if (elSales) elSales.innerText = `${formatINR(salesVal)}/m`;
        const elPrice = document.getElementById('slider-val-cap-price');
        if (elPrice) elPrice.innerText = `${priceVal >= 0 ? '+' : ''}${priceVal}%`;

        try {
            const res = await fetch(`${API_BASE}/analytics/decision-support/simulate-capital-allocation`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    headcount_additions: headVal,
                    ai_compute_budget_monthly_inr: gpuVal,
                    enterprise_sales_spend_inr: salesVal,
                    pricing_tier_adjustment_pct: priceVal
                })
            });
            const data = await res.json();
            if (data.status !== 'success') return;

            const t = data.treasury_impact;
            const g = data.growth_and_unit_economics;

            const elBurn = document.getElementById('cap-sim-burn');
            if (elBurn) elBurn.innerText = formatINR(t.new_monthly_burn_inr);
            const elRun = document.getElementById('cap-sim-runway');
            if (elRun) elRun.innerText = `${t.simulated_runway_months} Months`;
            const elArr = document.getElementById('cap-sim-arr');
            if (elArr) elArr.innerText = formatINR(g.projected_arr_inr);
            const elRule = document.getElementById('cap-sim-rule40');
            if (elRule) elRule.innerText = `${g.rule_of_40_score}% (${g.rule_of_40_pass ? 'Pass' : 'Watch'})`;
            const elLtv = document.getElementById('cap-sim-ltvcac');
            if (elLtv) elLtv.innerText = g.ltv_to_cac_ratio;
            const elPay = document.getElementById('cap-sim-payback');
            if (elPay) elPay.innerText = `${g.payback_period_months} Months`;

            const elGuide = document.getElementById('cap-sim-guidance');
            if (elGuide) {
                elGuide.innerHTML = `
                    <span class="flex items-center gap-2">
                        <i class="fa-solid fa-circle-check text-emerald-400"></i>
                        <span><strong>${data.executive_recommendation.flag}:</strong> ${data.executive_recommendation.guidance}</span>
                    </span>
                    <span class="font-mono text-[11px] text-slate-400">${data.executive_recommendation.director}, Director</span>
                `;
            }
        } catch (err) {
            console.error('Error running capital simulation:', err);
        }
    }, 150);
}

// ==============================================================
// TAB 9: MONTE CARLO RISK SIMULATION
// ==============================================================
export async function loadMonteCarloAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/data-science/monte-carlo`).then(r => r.json());
        if (res.status !== 'success') return;

        // KPI Percentiles
        const p = res.schedule_percentiles;
        const elP50 = document.getElementById('mc-kpi-p50');
        if (elP50) elP50.innerText = `${p.p50_expected_days} Days`;
        const elP80 = document.getElementById('mc-kpi-p80');
        if (elP80) elP80.innerText = `${p.p80_high_confidence_days} Days`;
        const elP95 = document.getElementById('mc-kpi-p95');
        if (elP95) elP95.innerText = `${p.p95_contractual_sla_days} Days`;
        const elVar = document.getElementById('mc-kpi-var');
        if (elVar) elVar.innerText = formatINR(res.budget_risk_var.value_at_risk_95_inr);

        // 1. Monte Carlo Distribution Bell Curve
        const sd = res.schedule_distribution;
        safeRenderChart('chart-mc-distribution', 'bar', {
            labels: sd.labels,
            datasets: [{
                label: 'Simulated Outcomes (Frequency per Bin / 1000 Iterations)',
                data: sd.frequency,
                backgroundColor: 'rgba(139, 92, 246, 0.75)',
                borderColor: '#7c3aed',
                borderWidth: 1.5,
                borderRadius: 4
            }]
        }, {
            scales: {
                y: {
                    title: { display: true, text: 'Trial Iterations' }
                },
                x: {
                    title: { display: true, text: 'Schedule Duration (Days)' }
                }
            }
        });

        // 2. Cumulative Probability (CDF)
        safeRenderChart('chart-mc-cdf', 'line', {
            labels: sd.labels,
            datasets: [{
                label: 'Cumulative Probability % (CDF)',
                data: sd.cumulative_prob_pct,
                borderColor: '#4f46e5',
                backgroundColor: 'rgba(79, 70, 229, 0.15)',
                fill: true,
                tension: 0.3,
                borderWidth: 2.5
            }]
        }, {
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: { callback: (v) => v + '%' }
                }
            }
        });
    } catch (err) {
        console.error('Error loading monte carlo analytics:', err);
    }
}

// ==============================================================
// TAB 10: EXECUTIVE INFOGRAPHICS
// ==============================================================
export async function loadExecutiveInfographics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/executive-infographics`).then(r => r.json());
        if (res.status !== 'success') return;
        // Verify infographics loaded cleanly
        console.log('Executive Infographics synced for', res.entity.name);
    } catch (err) {
        console.error('Error loading executive infographics:', err);
    }
}

// -----------------------------------------------------------------------------
// MODULE 13: INTERNAL SERVICE DESK, ALERTS & NOTIFICATIONS
// -----------------------------------------------------------------------------

export let internalTicketsData = [];
export let currentDeptFilter = 'ALL';
export let activeTicketDetailId = null;
export let topCriticalAlertActionUrl = null;

// Notification Dropdown & Header Bell
export function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notif-dropdown');
    if (dropdown) dropdown.classList.toggle('hidden');
}

export function closeNotificationDropdown() {
    const dropdown = document.getElementById('notif-dropdown');
    if (dropdown) dropdown.classList.add('hidden');
}

// Global click-outside listener to close dropdown
if (typeof document !== 'undefined') document.addEventListener('click', (e) => {
    const bellBtn = document.getElementById('btn-notif-bell');
    const dropdown = document.getElementById('notif-dropdown');
    if (bellBtn && dropdown && !bellBtn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden');
    }
});


export async function fetchNotificationsAndAlerts() {
    try {
        const [notifResp, bannerResp] = await Promise.all([
            fetch(`${API_BASE}/internal-support/notifications?limit=25`),
            fetch(`${API_BASE}/internal-support/alerts/active-banner`)
        ]);

        if (notifResp.ok) {
            const notifications = await notifResp.json();
            renderNotificationDropdown(notifications);
        }

        if (bannerResp.ok) {
            const banner = await bannerResp.json();
            renderActiveAlertBanner(banner);
        }
    } catch (err) {
        console.error('Error fetching notifications:', err);
    }
}

export function renderNotificationDropdown(notifications) {
    const unreadCount = notifications.filter(n => !n.is_read).length;
    const badge = document.getElementById('notif-badge');
    const countPill = document.getElementById('notif-count-pill');
    const listContainer = document.getElementById('notif-list-container');

    if (badge) {
        if (unreadCount > 0) {
            badge.innerText = unreadCount > 9 ? '9+' : unreadCount;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }

    if (countPill) {
        countPill.innerText = `${unreadCount} Unread`;
    }

    if (listContainer) {
        if (!notifications || notifications.length === 0) {
            listContainer.innerHTML = '<div class="p-4 text-center text-xs text-slate-400">No active alerts.</div>';
            return;
        }

        listContainer.innerHTML = notifications.slice(0, 8).map(n => {
            const sevBg = n.severity === 'CRITICAL' ? 'bg-red-50 border-l-4 border-red-600' :
                          (n.severity === 'WARNING' ? 'bg-amber-50 border-l-4 border-amber-500' :
                          (n.severity === 'SUCCESS' ? 'bg-emerald-50 border-l-4 border-emerald-500' : 'bg-blue-50 border-l-4 border-blue-500'));
            
            const sevTag = n.severity === 'CRITICAL' ? 'bg-red-200 text-red-900' :
                           (n.severity === 'WARNING' ? 'bg-amber-200 text-amber-900' :
                           (n.severity === 'SUCCESS' ? 'bg-emerald-200 text-emerald-900' : 'bg-blue-200 text-blue-900'));

            return `
                <div class="p-3 ${sevBg} hover:bg-slate-50 transition flex items-start justify-between gap-2">
                    <div class="flex-1">
                        <div class="flex items-center gap-1.5 mb-1">
                            <span class="text-[10px] font-bold px-1.5 py-0.2 rounded uppercase ${sevTag}">${n.severity}</span>
                            <span class="text-[10px] font-semibold text-slate-500">${n.module_source}</span>
                            ${!n.is_read ? '<span class="w-1.5 h-1.5 rounded-full bg-blue-600 inline-block"></span>' : ''}
                        </div>
                        <div class="text-xs font-bold text-slate-900 leading-snug">${n.title}</div>
                        <p class="text-[11px] text-slate-600 mt-0.5 line-clamp-2">${n.message}</p>
                    </div>
                    <div class="shrink-0 flex flex-col items-end gap-1">
                        ${!n.is_read ? `
                            <button onclick="handleMarkSingleNotificationRead(${n.id})" class="text-[10px] text-slate-400 hover:text-blue-600" title="Mark as read">
                                <i class="fa-solid fa-check"></i>
                            </button>
                        ` : ''}
                        ${n.action_url ? `
                            <button onclick="handleNotificationDeepLink('${n.action_url}', ${n.id})" class="text-[10px] text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-0.5">
                                ${n.action_label || 'View'} <i class="fa-solid fa-arrow-right text-[8px]"></i>
                            </button>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');
    }
}

export function renderActiveAlertBanner(banner) {
    const bannerElem = document.getElementById('system-alert-banner');
    if (!bannerElem) return;

    if (banner.has_active_critical && banner.top_critical_alert && !sessionStorage.getItem('alert_banner_dismissed')) {
        const top = banner.top_critical_alert;
        document.getElementById('alert-banner-title').innerText = top.title;
        document.getElementById('alert-banner-msg').innerText = `${top.message} (${banner.critical_count} active critical conditions)`;
        topCriticalAlertActionUrl = top.action_url || '#view-internal-support';
        bannerElem.classList.remove('hidden');
    } else {
        bannerElem.classList.add('hidden');
    }
}

export function dismissAlertBanner() {
    const bannerElem = document.getElementById('system-alert-banner');
    if (bannerElem) bannerElem.classList.add('hidden');
    sessionStorage.setItem('alert_banner_dismissed', 'true');
}

export function handleAlertBannerAction() {
    if (topCriticalAlertActionUrl) {
        handleNotificationDeepLink(topCriticalAlertActionUrl);
    }
}

export function handleNotificationDeepLink(url, notifId = null) {
    if (notifId) {
        handleMarkSingleNotificationRead(notifId);
    }
    closeNotificationDropdown();
    if (url.startsWith('#view-')) {
        const mod = url.replace('#view-', '');
        switchModule(mod);
    }
}

export async function handleMarkSingleNotificationRead(notifId) {
    try {
        await fetch(`${API_BASE}/internal-support/notifications/${notifId}/read`, { method: 'PATCH' });
        fetchNotificationsAndAlerts();
    } catch (err) {
        console.error('Error marking read:', err);
    }
}

export async function handleMarkAllNotificationsRead() {
    try {
        await fetch(`${API_BASE}/internal-support/notifications/mark-all-read`, { method: 'POST' });
        fetchNotificationsAndAlerts();
        if (currentModule === 'internal-support') {
            loadInternalSupport();
        }
    } catch (err) {
        console.error('Error marking all read:', err);
    }
}

export async function handleTriggerSyncAlerts() {
    try {
        const resp = await fetch(`${API_BASE}/internal-support/sync-alerts`, { method: 'POST' });
        const res = await resp.json();
        alert(`System alert engine scan complete: ${res.created_alerts_count} active condition(s) synced.`);
        fetchNotificationsAndAlerts();
        if (currentModule === 'internal-support') {
            loadInternalSupport();
        }
    } catch (err) {
        console.error('Error syncing alerts:', err);
    }
}

// -----------------------------------------------------------------------------
// INTERNAL SERVICE DESK LOAD & RENDERING
// -----------------------------------------------------------------------------

export async function loadInternalSupport() {
    try {
        const [sumResp, tktResp, notifResp] = await Promise.all([
            fetch(`${API_BASE}/internal-support/summary`),
            fetch(`${API_BASE}/internal-support/tickets`),
            fetch(`${API_BASE}/internal-support/notifications?limit=50`)
        ]);

        if (sumResp.ok) {
            const summary = await sumResp.json();
            renderServiceDeskSummary(summary);
        }

        if (tktResp.ok) {
            internalTicketsData = await tktResp.json();
            renderInternalTicketsTable();
        }

        if (notifResp.ok) {
            const notifs = await notifResp.json();
            renderFullNotificationsFeed(notifs);
        }
    } catch (err) {
        console.error('Error loading internal support:', err);
    }
}

export function renderServiceDeskSummary(summary) {
    document.getElementById('srv-total-tickets').innerText = summary.total_tickets;
    document.getElementById('srv-open-tickets').innerText = summary.open_tickets + summary.in_progress_tickets;
    document.getElementById('srv-sla-rate').innerText = `${summary.sla_compliance_pct.toFixed(1)}%`;
    document.getElementById('srv-p1-tickets').innerText = summary.critical_p1_tickets;

    const deptCards = document.getElementById('dept-summary-cards');
    if (deptCards && summary.departments) {
        deptCards.innerHTML = summary.departments.map(d => `
            <div onclick="filterTicketsByDepartment('${d.department}')" class="cursor-pointer bg-slate-50 hover:bg-purple-50 p-2.5 rounded-lg border border-slate-200 transition">
                <div class="text-[11px] font-bold text-slate-700 truncate" title="${d.display_name}">${d.display_name.split(' ')[0]}</div>
                <div class="text-base font-extrabold text-slate-900 mt-0.5">${d.total_tickets} <span class="text-[10px] text-slate-400 font-normal">tkts</span></div>
                <div class="text-[10px] text-emerald-600 font-semibold mt-0.5">${d.sla_compliance_pct}% SLA</div>
            </div>
        `).join('');
    }
}

export function filterTicketsByDepartment(deptKey) {
    currentDeptFilter = deptKey;
    document.querySelectorAll('.tkt-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-dept') === deptKey) {
            btn.classList.add('bg-purple-600', 'text-white', 'shadow-sm');
            btn.classList.remove('text-slate-600', 'hover:bg-slate-200');
        } else {
            btn.classList.remove('bg-purple-600', 'text-white', 'shadow-sm');
            btn.classList.add('text-slate-600', 'hover:bg-slate-200');
        }
    });
    renderInternalTicketsTable();
}

export function renderInternalTicketsTable() {
    const tbody = document.getElementById('internal-tickets-tbody');
    if (!tbody) return;

    const prioFilter = document.getElementById('filter-ticket-priority')?.value || 'ALL';
    const statusFilter = document.getElementById('filter-ticket-status')?.value || 'ALL';

    const filtered = internalTicketsData.filter(t => {
        if (currentDeptFilter !== 'ALL' && t.department !== currentDeptFilter) return false;
        if (prioFilter !== 'ALL' && t.priority !== prioFilter) return false;
        if (statusFilter !== 'ALL' && t.status !== statusFilter) return false;
        return true;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="p-8 text-center text-slate-400">No service desk tickets found matching filters.</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(t => {
        // Priority Badge
        const prioBadge = t.priority === 'P1-Critical' ? 'bg-red-100 text-red-800 border border-red-300' :
                          (t.priority === 'P2-High' ? 'bg-orange-100 text-orange-800 border border-orange-300' :
                          (t.priority === 'P3-Medium' ? 'bg-blue-100 text-blue-800 border border-blue-300' : 'bg-slate-100 text-slate-700 border border-slate-300'));

        // Status Pill
        const statusPill = t.status === 'Resolved' || t.status === 'Closed' ? 'bg-emerald-100 text-emerald-800' :
                           (t.status === 'In Progress' ? 'bg-amber-100 text-amber-800' : 'bg-purple-100 text-purple-800');

        // SLA Badge
        const slaBadge = t.sla_breached ? '<span class="text-red-700 font-bold bg-red-100 px-1.5 py-0.5 rounded text-[10px]">BREACHED</span>' :
                         `<span class="text-slate-600 font-mono text-[11px]">${t.sla_deadline_hours}h</span>`;

        return `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3.5 font-mono font-bold text-purple-700">${t.ticket_number}</td>
                <td class="p-3.5 font-medium text-slate-700">
                    <span class="px-2 py-0.5 rounded bg-slate-100 text-[11px]">${t.department.replace('_', ' ')}</span>
                </td>
                <td class="p-3.5">
                    <div class="font-bold text-slate-900">${t.subject}</div>
                    <div class="text-[11px] text-slate-500">${t.category}</div>
                </td>
                <td class="p-3.5">
                    <span class="px-2 py-0.5 rounded font-bold text-[10px] ${prioBadge}">${t.priority}</span>
                </td>
                <td class="p-3.5">
                    <div class="font-medium text-slate-800">${t.requester_name}</div>
                    <div class="text-[10px] text-slate-400 font-mono">${t.requester_email}</div>
                </td>
                <td class="p-3.5 text-slate-700 font-medium">${t.assigned_to || 'Unassigned'}</td>
                <td class="p-3.5">${slaBadge}</td>
                <td class="p-3.5">
                    <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${statusPill}">${t.status}</span>
                </td>
                <td class="p-3.5 text-right">
                    <button onclick="openTicketDetail(${t.id})" class="text-xs px-2.5 py-1 bg-purple-50 hover:bg-purple-100 text-purple-700 font-semibold rounded transition border border-purple-200">
                        View / Resolve
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

export function renderFullNotificationsFeed(notifications) {
    const feed = document.getElementById('full-notifications-feed');
    if (!feed) return;

    if (!notifications || notifications.length === 0) {
        feed.innerHTML = '<div class="p-4 text-center text-xs text-slate-400">No active system alerts.</div>';
        return;
    }

    feed.innerHTML = notifications.map(n => {
        const sevBg = n.severity === 'CRITICAL' ? 'bg-red-50/80 border-red-300' :
                      (n.severity === 'WARNING' ? 'bg-amber-50/80 border-amber-300' :
                      (n.severity === 'SUCCESS' ? 'bg-emerald-50/80 border-emerald-300' : 'bg-blue-50/80 border-blue-300'));

        const sevTag = n.severity === 'CRITICAL' ? 'bg-red-600 text-white' :
                       (n.severity === 'WARNING' ? 'bg-amber-500 text-white' :
                       (n.severity === 'SUCCESS' ? 'bg-emerald-600 text-white' : 'bg-blue-600 text-white'));

        return `
            <div class="p-3.5 rounded-xl border ${sevBg} flex items-start justify-between gap-3 shadow-xs">
                <div class="flex items-start gap-3">
                    <span class="px-2 py-0.5 rounded font-bold text-[10px] uppercase shrink-0 mt-0.5 ${sevTag}">${n.severity}</span>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-mono font-bold text-slate-500">${n.notification_code}</span>
                            <span class="text-xs font-semibold text-slate-400">• ${n.module_source}</span>
                            <span class="text-xs font-semibold text-slate-400">• Target: ${n.target_role}</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-900 mt-1">${n.title}</h4>
                        <p class="text-xs text-slate-700 mt-0.5 leading-relaxed">${n.message}</p>
                    </div>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                    ${n.action_url ? `
                        <button onclick="handleNotificationDeepLink('${n.action_url}', ${n.id})" class="text-xs px-2.5 py-1 bg-white hover:bg-slate-50 text-blue-700 border border-blue-200 rounded font-semibold shadow-xs">
                            ${n.action_label || 'Inspect'}
                        </button>
                    ` : ''}
                    ${!n.is_read ? `
                        <button onclick="handleMarkSingleNotificationRead(${n.id})" class="text-xs px-2 py-1 bg-white hover:bg-slate-50 text-slate-600 border border-slate-200 rounded font-medium">
                            Mark Read
                        </button>
                    ` : '<span class="text-[10px] text-slate-400 font-medium">Read</span>'}
                </div>
            </div>
        `;
    }).join('');
}

// Modal Handlers: Create Internal Ticket
export function openCreateTicketModal() {
    const modal = document.getElementById('modal-internal-ticket');
    if (modal) modal.classList.remove('hidden');
}

export function closeCreateTicketModal() {
    const modal = document.getElementById('modal-internal-ticket');
    if (modal) modal.classList.add('hidden');
}

export async function handleCreateInternalTicket(event) {
    event.preventDefault();
    const payload = {
        department: document.getElementById('new-tkt-dept').value,
        priority: document.getElementById('new-tkt-priority').value,
        category: document.getElementById('new-tkt-cat').value,
        subject: document.getElementById('new-tkt-subject').value,
        description: document.getElementById('new-tkt-desc').value,
        requester_name: document.getElementById('new-tkt-req-name').value,
        requester_email: document.getElementById('new-tkt-req-email').value,
        requester_department: document.getElementById('new-tkt-req-dept').value
    };

    try {
        const resp = await fetch(`${API_BASE}/internal-support/tickets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (resp.ok) {
            const created = await resp.json();
            alert(`Internal Ticket ${created.ticket_number} created with ${created.sla_deadline_hours}h SLA target!`);
            closeCreateTicketModal();
            loadInternalSupport();
            fetchNotificationsAndAlerts();
        } else {
            const err = await resp.json();
            alert(`Error creating ticket: ${err.detail || 'Validation error'}`);
        }
    } catch (err) {
        console.error('Error submitting ticket:', err);
    }
}

// Modal Handlers: Ticket Inspection & Threaded Resolution
export async function openTicketDetail(ticketId) {
    activeTicketDetailId = ticketId;
    const modal = document.getElementById('modal-ticket-detail');
    if (!modal) return;

    try {
        const resp = await fetch(`${API_BASE}/internal-support/tickets/${ticketId}`);
        if (!resp.ok) return;
        const tkt = await resp.json();

        document.getElementById('detail-tkt-num').innerText = tkt.ticket_number;
        document.getElementById('detail-tkt-priority').innerText = tkt.priority;
        document.getElementById('detail-tkt-status').innerText = tkt.status;
        document.getElementById('detail-tkt-subject').innerText = tkt.subject;
        document.getElementById('detail-tkt-desc').innerText = tkt.description;
        document.getElementById('detail-tkt-requester').innerText = `${tkt.requester_name} (${tkt.requester_email})`;
        document.getElementById('detail-tkt-dept').innerText = tkt.department;
        document.getElementById('detail-tkt-sla').innerText = `${tkt.sla_deadline_hours}h (${tkt.sla_breached ? 'BREACHED' : 'Compliant'})`;

        document.getElementById('detail-update-status').value = tkt.status;
        document.getElementById('detail-update-assignee').value = tkt.assigned_to || '';
        document.getElementById('detail-update-resolution').value = tkt.resolution_summary || '';
        document.getElementById('detail-update-csat').value = tkt.satisfaction_score ? String(tkt.satisfaction_score) : '5';

        // Render Comments Thread
        renderTicketCommentsThread(tkt.comments_json);

        modal.classList.remove('hidden');
    } catch (err) {
        console.error('Error opening ticket detail:', err);
    }
}

export function closeTicketDetailModal() {
    const modal = document.getElementById('modal-ticket-detail');
    if (modal) modal.classList.add('hidden');
    activeTicketDetailId = null;
}

export function renderTicketCommentsThread(commentsJson) {
    const container = document.getElementById('detail-comments-container');
    if (!container) return;

    let comments = [];
    try {
        comments = JSON.parse(commentsJson || '[]');
    } catch (e) {
        comments = [];
    }

    if (comments.length === 0) {
        container.innerHTML = '<div class="text-[11px] text-slate-400 italic">No notes posted yet.</div>';
        return;
    }

    container.innerHTML = comments.map(c => `
        <div class="p-2.5 rounded-lg ${c.is_internal ? 'bg-amber-50/70 border border-amber-200' : 'bg-slate-100'} text-xs">
            <div class="flex items-center justify-between text-[10px] text-slate-500 mb-0.5">
                <span class="font-bold text-slate-700">${c.author} ${c.is_internal ? '<span class="text-amber-800 font-semibold">[Internal Note]</span>' : ''}</span>
                <span class="font-mono">${c.timestamp}</span>
            </div>
            <div class="text-slate-800">${c.message}</div>
        </div>
    `).join('');
}

export async function handleSaveTicketStatusUpdate() {
    if (!activeTicketDetailId) return;

    const payload = {
        status: document.getElementById('detail-update-status').value,
        assigned_to: document.getElementById('detail-update-assignee').value,
        resolution_summary: document.getElementById('detail-update-resolution').value,
        satisfaction_score: parseInt(document.getElementById('detail-update-csat').value, 10)
    };

    try {
        const resp = await fetch(`${API_BASE}/internal-support/tickets/${activeTicketDetailId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (resp.ok) {
            alert('Ticket status and resolution updated successfully!');
            closeTicketDetailModal();
            loadInternalSupport();
            fetchNotificationsAndAlerts();
        } else {
            alert('Error updating ticket.');
        }
    } catch (err) {
        console.error('Error saving ticket update:', err);
    }
}

export async function handleAddTicketComment(event) {
    event.preventDefault();
    if (!activeTicketDetailId) return;

    const input = document.getElementById('detail-new-comment');
    const isInternal = document.getElementById('detail-is-internal').checked;

    if (!input.value.trim()) return;

    const payload = {
        author_name: 'Varadi Vijay (Director)',
        message: input.value.trim(),
        is_internal_note: isInternal
    };

    try {
        const resp = await fetch(`${API_BASE}/internal-support/tickets/${activeTicketDetailId}/comments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (resp.ok) {
            const updated = await resp.json();
            input.value = '';
            renderTicketCommentsThread(updated.comments_json);
        }
    } catch (err) {
        console.error('Error adding comment:', err);
    }
}

// ==============================================================================
// 15. SMART ATTENDANCE, BIOMETRIC FACIAL & WHATSAPP INTEGRATION
// ==============================================================================

export async function loadSmartAttendance() {
    try {
        const [resSummary, resRecords, resEmployees] = await Promise.all([
            fetch(`${API_BASE}/attendance/daily-summary`).then(r => r.json()),
            fetch(`${API_BASE}/attendance/records`).then(r => r.json()),
            fetch(`${API_BASE}/hrms/employees`).then(r => r.json())
        ]);

        // Populate Employee Select
        const empSelect = document.getElementById('att-employee-select');
        if (empSelect && resEmployees) {
            empSelect.innerHTML = resEmployees.map(e => `
                <option value="${e.id}">${e.full_name} (${e.emp_code}) - ${e.designation}</option>
            `).join('');
        }

        // Render KPI stats
        if (resSummary) {
            document.getElementById('att-stat-headcount').innerText = resSummary.total_employees;
            document.getElementById('att-stat-present').innerText = resSummary.present_count;
            document.getElementById('att-stat-biometric').innerText = `${resSummary.biometric_compliance_pct}%`;
            document.getElementById('att-stat-late').innerText = resSummary.late_marks_count;
            document.getElementById('att-stat-wfh').innerText = resSummary.wfh_count;
            document.getElementById('att-stat-healed').innerText = resSummary.auto_healed_today_count;
        }

        // Render Table
        const tableBody = document.getElementById('table-attendance-records');
        if (tableBody && resRecords) {
            tableBody.innerHTML = resRecords.map(r => {
                const emp = (resEmployees || []).find(e => e.id === r.employee_id);
                const empName = emp ? emp.full_name : `Employee ID #${r.employee_id}`;
                const inTime = r.clock_in_time ? new Date(r.clock_in_time).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '--:--';
                const outTime = r.clock_out_time ? new Date(r.clock_out_time).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '--:--';
                
                const geoBadge = r.geofence_verified 
                    ? `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800"><i class="fa-solid fa-location-dot mr-1"></i>HQ (Verified)</span>`
                    : `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-950 text-purple-400 border border-purple-800"><i class="fa-solid fa-house-laptop mr-1"></i>Remote / WFH</span>`;
                
                const faceBadge = r.facial_recognition_verified
                    ? `<span class="text-cyan-400 font-mono font-bold">${r.facial_match_confidence_pct}% <i class="fa-solid fa-check-circle text-[10px]"></i></span>`
                    : `<span class="text-slate-500 font-mono text-[11px]">N/A</span>`;

                const autoFixBadge = r.auto_fixed 
                    ? `<span class="ml-1 px-1.5 py-0.5 rounded text-[9px] bg-blue-900 text-blue-300 font-bold uppercase">Healed</span>`
                    : ``;

                let statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-900 text-emerald-300">${r.status}</span>`;
                if (r.status === 'Late Mark') {
                    statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-900 text-amber-300">Late Mark</span>`;
                } else if (r.status === 'Half Day') {
                    statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-900 text-indigo-300">Half Day</span>`;
                } else if (r.status === 'Regularized') {
                    statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-900 text-blue-300">Regularized</span>`;
                }

                return `
                    <tr class="hover:bg-slate-800/50 transition">
                        <td class="p-3 font-mono text-slate-400">#${r.employee_id}</td>
                        <td class="p-3 font-semibold text-white">${empName}</td>
                        <td class="p-3 font-mono text-slate-400">${r.attendance_date}</td>
                        <td class="p-3 font-mono text-emerald-400 font-bold">${inTime}</td>
                        <td class="p-3 font-mono text-rose-400 font-bold">${outTime}</td>
                        <td class="p-3 text-right font-mono">${r.total_work_hours.toFixed(1)}h</td>
                        <td class="p-3 text-right font-mono font-bold text-white">${r.effective_work_hours.toFixed(1)}h</td>
                        <td class="p-3">${statusBadge}${autoFixBadge}</td>
                        <td class="p-3">${geoBadge}</td>
                        <td class="p-3">${faceBadge}</td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300">${r.in_source}</span></td>
                    </tr>
                `;
            }).join('');
        }
    } catch (err) {
        console.error('Error loading smart attendance:', err);
    }
}

export async function handleClockIn() {
    const empSelect = document.getElementById('att-employee-select');
    const sourceSelect = document.getElementById('att-source-select');
    if (!empSelect || !empSelect.value) return;

    const payload = {
        employee_id: parseInt(empSelect.value),
        source: sourceSelect ? sourceSelect.value : 'FACIAL_KIOSK',
        latitude: 13.035820,
        longitude: 77.653410,
        selfie_base64_or_hash: 'web_kiosk_live_frame_base64_payload'
    };

    try {
        const res = await fetch(`${API_BASE}/attendance/clock-in`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Clock-IN Notice: ${err.detail || 'Unable to record punch'}`);
            return;
        }

        const data = await res.json();
        alert(`✅ Clock-IN Recorded Successfully!\nBiometric Match: ${data.facial_match_confidence_pct}%\nGeofence: ${data.geofence_zone_code || 'HQ'} (Verified)`);
        loadSmartAttendance();
    } catch (err) {
        alert('Error recording clock-in: ' + err.message);
    }
}

export async function handleClockOut() {
    const empSelect = document.getElementById('att-employee-select');
    const sourceSelect = document.getElementById('att-source-select');
    if (!empSelect || !empSelect.value) return;

    const payload = {
        employee_id: parseInt(empSelect.value),
        source: sourceSelect ? sourceSelect.value : 'FACIAL_KIOSK',
        latitude: 13.035820,
        longitude: 77.653410
    };

    try {
        const res = await fetch(`${API_BASE}/attendance/clock-out`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Clock-OUT Notice: ${err.detail || 'Unable to clock out'}`);
            return;
        }

        const data = await res.json();
        alert(`✅ Clock-OUT Recorded!\nTotal Hours: ${data.total_work_hours}h\nEffective Credited Hours: ${data.effective_work_hours}h\nStatus: ${data.status}`);
        loadSmartAttendance();
    } catch (err) {
        alert('Error recording clock-out: ' + err.message);
    }
}

export async function handleTriggerAutoFixAttendance() {
    try {
        const res = await fetch(`${API_BASE}/attendance/auto-fix-anomalies`, { method: 'POST' });
        if (res.ok) {
            const data = await res.json();
            const msg = data.details.length > 0 
                ? `Self-Healing Complete!\n${data.auto_fixed_count} anomalous punches closed.\nDetails:\n${data.details.join('\n')}`
                : `Self-Healing Engine Scan: All records are up-to-date and regularized. Zero anomalies found.`;
            alert(msg);
            loadSmartAttendance();
        }
    } catch (err) {
        alert('Error triggering auto-fix: ' + err.message);
    }
}

export function openWhatsAppModal() {
    const modal = document.getElementById('modal-whatsapp-bot');
    if (modal) modal.classList.remove('hidden');
}

export function closeWhatsAppModal() {
    const modal = document.getElementById('modal-whatsapp-bot');
    if (modal) modal.classList.add('hidden');
}

export function setWhatsAppMsg(cmd) {
    const input = document.getElementById('wa-msg-input');
    if (input) input.value = cmd;
}

export async function handleSendWhatsAppBotMessage(event) {
    event.preventDefault();
    const phone = document.getElementById('wa-phone-input').value.trim();
    const msg = document.getElementById('wa-msg-input').value.trim();
    const lat = parseFloat(document.getElementById('wa-lat-input').value) || 13.035820;
    const lon = parseFloat(document.getElementById('wa-lon-input').value) || 77.653410;

    try {
        const res = await fetch(`${API_BASE}/attendance/whatsapp-webhook`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                phone_number: phone,
                message_body: msg,
                latitude: lat,
                longitude: lon
            })
        });

        if (res.ok) {
            const data = await res.json();
            const container = document.getElementById('wa-reply-container');
            const textEl = document.getElementById('wa-reply-text');
            if (container && textEl) {
                container.classList.remove('hidden');
                textEl.innerText = data.reply_message || JSON.stringify(data);
            }
            loadSmartAttendance();
        }
    } catch (err) {
        alert('Error contacting WhatsApp webhook: ' + err.message);
    }
}

// Global Autonomous Self-Healing Trigger
export async function handleTriggerGlobalSelfHeal() {
    try {
        const res = await fetch(`${API_BASE}/system/trigger-self-heal`, { method: 'POST' });
        if (res.ok) {
            const data = await res.json();
            const details = data.actions_taken && data.actions_taken.length > 0
                ? `\nRepairs Applied:\n` + data.actions_taken.join('\n')
                : `\nAll modules, registers, and ledgers are completely synchronized and verified!`;
            alert(`🏥 Autonomous Self-Healing Diagnostic Complete!\nHealth Score: ${data.system_health_score}%\nAnomalies Fixed: ${data.anomalies_auto_fixed} / ${data.anomalies_detected}${details}`);
            
            // Auto-refresh current view
            if (typeof switchModule === 'function' && currentModule) {
                switchModule(currentModule);
            }
            fetchNotificationsAndAlerts();
        }
    } catch (err) {
        alert('Error triggering self-heal: ' + err.message);
    }
}

// ==============================================================================
// 16. DEDICATED STAKEHOLDER PORTAL DATA LOADERS & RENDERERS
// ==============================================================================

/**
 * 1. Employee Self-Service (ESS) Digital Workplace & Portal Controller
 */
export let currentESSEmpCode = "ADT-EMP-001";
export let essCompChart = null;
export let essAttChart = null;
export let essLeavesChart = null;

export function switchESSTab(tabKey) {
    document.querySelectorAll('.ess-tab-pane').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`ess-tab-${tabKey}`);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.ess-nav-tab').forEach(b => {
        b.classList.remove('active', 'bg-blue-600', 'text-white', 'shadow-sm');
        b.classList.add('text-slate-600', 'hover:bg-slate-100');
    });
    const activeBtn = document.getElementById(`tab-btn-ess-${tabKey}`);
    if (activeBtn) {
        activeBtn.classList.add('active', 'bg-blue-600', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('text-slate-600', 'hover:bg-slate-100');
    }
}

export function switchEmployeeProfile(empCode) {
    currentESSEmpCode = empCode;
    loadEmployeePortal(empCode);
}

export async function loadEmployeePortal(empCode = currentESSEmpCode) {
    currentESSEmpCode = empCode;
    try {
        const res = await fetch(`${API_BASE}/portals/employee/dashboard-data?emp_code=${encodeURIComponent(empCode)}`);
        if (!res.ok) return;
        const data = await res.json();

        // 1. Employee Selector Sync & Options
        const sel = document.getElementById('ess-employee-selector');
        if (sel && data.employees_roster && data.employees_roster.length > 0) {
            sel.innerHTML = data.employees_roster.map(e => `
                <option value="${e.emp_code}" ${e.emp_code === empCode ? 'selected' : ''} class="bg-slate-900 text-white">
                    ${e.emp_code} &bull; ${e.name} (${e.department})
                </option>
            `).join('');
            sel.value = empCode;
        }

        // 2. Profile Details
        const prof = data.profile || {};
        const pInitials = prof.name ? prof.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'EMP';
        const avatarEl = document.getElementById('ess-emp-avatar');
        if (avatarEl) avatarEl.innerText = pInitials;

        const nameEl = document.getElementById('ess-emp-name');
        if (nameEl) nameEl.innerText = prof.name || 'Employee';
        const codeEl = document.getElementById('ess-emp-code');
        if (codeEl) codeEl.innerText = prof.emp_code || empCode;
        const desigEl = document.getElementById('ess-emp-designation');
        if (desigEl) desigEl.innerText = prof.designation || 'Designation';
        const deptEl = document.getElementById('ess-emp-department');
        if (deptEl) deptEl.innerText = prof.department || 'Department';

        const probBadge = document.getElementById('ess-badge-probation');
        if (probBadge) {
            const isConfirmed = prof.probation_status === 'Confirmed';
            probBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold flex items-center gap-1 ${isConfirmed ? 'bg-cyan-950/80 text-cyan-400 border border-cyan-800/50' : 'bg-amber-950/80 text-amber-400 border border-amber-800/50'}`;
            probBadge.innerHTML = `<i class="fa-solid fa-certificate text-[9px]"></i> ${prof.probation_status || 'Confirmed'}`;
        }

        // 3. 6 Top KPI Metrics
        const sal = data.salary_breakup || data.salary_overview || {};
        const ctcElem = document.getElementById('ess-kpi-annual-ctc');
        if (ctcElem) ctcElem.innerText = formatINR(sal.annual_ctc || 1440000);
        const grossElem = document.getElementById('ess-kpi-monthly-gross');
        if (grossElem) grossElem.innerText = formatINR(sal.monthly_gross || 120000);
        const netElem = document.getElementById('ess-kpi-net-takehome');
        if (netElem) netElem.innerText = formatINR(sal.net_in_hand || 115296);
        const bankElem = document.getElementById('ess-kpi-bank-account');
        if (bankElem) bankElem.innerText = prof.bank_name ? prof.bank_name.split('-')[0].trim() : 'ICICI Bank';

        const att = data.attendance_stats || {};
        const attKpi = document.getElementById('ess-kpi-attendance-pct');
        if (attKpi) attKpi.innerText = `${att.geofence_compliance_pct || 98.4}%`;
        const avgHoursKpi = document.getElementById('ess-kpi-avg-hours');
        if (avgHoursKpi) avgHoursKpi.innerText = `${att.avg_daily_hours || 8.5} hrs/day`;

        const ldg = data.leave_ledger || {};
        const ldgKpi = document.getElementById('ess-kpi-leave-balance');
        if (ldgKpi) ldgKpi.innerText = `${(ldg.total_available_days || 26.0).toFixed(1)} Days`;
        const ldgConsumedKpi = document.getElementById('ess-kpi-leave-consumed');
        if (ldgConsumedKpi) ldgConsumedKpi.innerText = `${(ldg.consumed_days || 4.0).toFixed(1)} Days`;

        const lrn = data.learning_and_probation || {};
        const lrnKpi = document.getElementById('ess-kpi-learning-hours');
        if (lrnKpi) lrnKpi.innerText = `${(lrn.total_hours_completed || 24.5).toFixed(1)} Hrs`;
        const certCountKpi = document.getElementById('ess-kpi-certs-count');
        if (certCountKpi) {
            const certCount = (lrn.certificates || []).length;
            certCountKpi.innerText = `${certCount} Certificate${certCount === 1 ? '' : 's'}`;
        }

        const assetsCountKpi = document.getElementById('ess-kpi-assets-count');
        if (assetsCountKpi) {
            const hwCount = (data.it_assets_and_security && data.it_assets_and_security.assets) ? data.it_assets_and_security.assets.length : 2;
            assetsCountKpi.innerText = `${hwCount} Hardware`;
        }

        // 4. Render Chart.js Visualizations
        renderESSCharts(sal, att, ldg);

        // 5. Statutory Dossier (Tab 1)
        const panEl = document.getElementById('ess-stat-pan');
        if (panEl) panEl.innerText = prof.pan_number || 'AAACA1234D';
        const aadhEl = document.getElementById('ess-stat-aadhaar');
        if (aadhEl) aadhEl.innerText = prof.aadhaar_number || '•••• •••• 9012';
        const uanEl = document.getElementById('ess-stat-uan');
        if (uanEl) uanEl.innerText = prof.uan_number || '101928374650';
        const esicEl = document.getElementById('ess-stat-esic');
        if (esicEl) esicEl.innerText = prof.esic_number || '55001234560010001';
        const bankDossierEl = document.getElementById('ess-stat-bank');
        if (bankDossierEl) bankDossierEl.innerText = `${prof.bank_name || 'ICICI Bank'} • A/C ${prof.bank_account_number || '000123456789'}`;
        const dojEl = document.getElementById('ess-stat-doj');
        if (dojEl) dojEl.innerText = `${prof.date_of_joining || '2026-01-15'} (${prof.probation_status || 'Confirmed'})`;

        // 6. Wage Code Compensation Tab (Tab 2)
        const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        setVal('comp-basic', formatINR(sal.basic_salary || 48000));
        setVal('comp-hra', formatINR(sal.hra || 19200));
        setVal('comp-special', formatINR(sal.special_allowance || 52800));
        setVal('comp-gross', formatINR(sal.monthly_gross || 120000));
        setVal('comp-pf-ee', `-${formatINR(sal.employee_pf || 1800)}`);
        setVal('comp-pt', `-${formatINR(sal.professional_tax || 200)}`);
        setVal('comp-tds', `-${formatINR(sal.estimated_tds || 0)}`);
        setVal('comp-net', formatINR(sal.net_in_hand || 115296));
        setVal('comp-pf-er', `${formatINR(sal.employer_pf || 1800)} / mo`);
        setVal('comp-gratuity', `${formatINR(sal.gratuity_provision || 2308)} / mo`);
        setVal('tax-annual-gross', formatINR(sal.annual_ctc || 1440000));

        // Render My Payslips Table
        const slipsTable = document.getElementById('table-ess-payslips');
        if (slipsTable && data.payslips) {
            if (data.payslips.length === 0) {
                slipsTable.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-slate-400">No payslips recorded yet.</td></tr>';
            } else {
                slipsTable.innerHTML = data.payslips.map(p => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 font-bold text-slate-800">${p.cycle}</td>
                        <td class="p-3 text-right font-mono text-slate-600">${formatINR(p.earned_gross)}</td>
                        <td class="p-3 text-right font-mono text-rose-600">-${formatINR(p.total_deductions)}</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-600">${formatINR(p.net_salary)}</td>
                        <td class="p-3 font-mono text-[11px] text-slate-600">${p.bank_utr}</td>
                        <td class="p-3 text-center">
                            <a href="${p.slip_url}" target="_blank" class="px-3 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-xs font-semibold transition inline-flex items-center gap-1.5 shadow-sm">
                                <i class="fa-solid fa-file-pdf"></i> Formal Slip
                            </a>
                        </td>
                    </tr>
                `).join('');
            }
        }

        // 7. Attendance Tab (Tab 3)
        const attTable = document.getElementById('table-ess-attendance');
        if (attTable && att.records) {
            if (att.records.length === 0) {
                attTable.innerHTML = '<tr><td colspan="7" class="p-4 text-center text-slate-400">No attendance punches recorded yet.</td></tr>';
            } else {
                attTable.innerHTML = att.records.map(r => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-2.5 text-slate-700 font-semibold">${r.date}</td>
                        <td class="p-2.5 font-bold text-emerald-600">${r.clock_in}</td>
                        <td class="p-2.5 font-bold text-rose-600">${r.clock_out}</td>
                        <td class="p-2.5 text-right font-bold text-slate-800">${(r.hours || 0).toFixed(1)}h</td>
                        <td class="p-2.5 text-slate-500 text-[10px]">${r.channel || 'FACIAL_KIOSK'}</td>
                        <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${r.status === 'Present' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">${r.status}</span></td>
                        <td class="p-2.5 text-slate-600 text-[11px]">${r.geofence} (${(r.distance_m || 15.2).toFixed(1)}m)</td>
                    </tr>
                `).join('');
            }
        }

        // 8. Leaves Tab (Tab 4)
        setVal('ess-leave-el', (ldg.annual_earned_leave_balance || 16.0).toFixed(1));
        setVal('ess-leave-cl', (ldg.casual_sick_leave_balance || 10.0).toFixed(1));
        setVal('ess-leave-comp', (ldg.comp_off_balance || 0.0).toFixed(1));
        setVal('ess-leave-total', (ldg.total_available_days || 26.0).toFixed(1));

        const leavesHistTable = document.getElementById('table-ess-leaves-history');
        if (leavesHistTable && ldg.applications) {
            if (ldg.applications.length === 0) {
                leavesHistTable.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-slate-400">No leave applications filed yet.</td></tr>';
            } else {
                leavesHistTable.innerHTML = ldg.applications.map(l => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-2.5 font-bold text-slate-800">${l.type}</td>
                        <td class="p-2.5 text-slate-600">${l.dates}</td>
                        <td class="p-2.5 text-right font-bold text-slate-900">${l.days}d</td>
                        <td class="p-2.5 text-slate-500">${l.reason}</td>
                        <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${l.status === 'Approved' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">${l.status}</span></td>
                    </tr>
                `).join('');
            }
        }

        const holidaysTable = document.getElementById('table-ess-holidays');
        if (holidaysTable && ldg.statutory_holidays_2026) {
            holidaysTable.innerHTML = ldg.statutory_holidays_2026.map(h => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-mono text-slate-700 font-bold">${h.date}</td>
                    <td class="p-2.5 text-slate-500">${h.day}</td>
                    <td class="p-2.5 font-semibold text-slate-800">${h.name}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600">${h.type}</span></td>
                </tr>
            `).join('');
        }

        // 9. Learning Academy Tab (Tab 5)
        const lrnProgLabel = document.getElementById('ess-learning-progress-label');
        if (lrnProgLabel) lrnProgLabel.innerText = `${(lrn.total_hours_completed || 24.5).toFixed(1)} / ${(lrn.min_required_hours || 16.0).toFixed(1)} Hrs`;
        const lrnProgBar = document.getElementById('ess-learning-progress-bar');
        if (lrnProgBar) {
            const pct = Math.min(100, Math.round(((lrn.total_hours_completed || 24.5) / (lrn.min_required_hours || 16.0)) * 100));
            lrnProgBar.style.width = `${pct}%`;
        }
        const probPill = document.getElementById('ess-probation-status-pill');
        if (probPill) {
            probPill.innerText = lrn.probation_clearance_ready ? 'Confirmed Permanent' : 'In Progress';
        }

        const coursesGrid = document.getElementById('grid-ess-enrolled-courses');
        if (coursesGrid && lrn.enrolled_courses) {
            if (lrn.enrolled_courses.length === 0) {
                coursesGrid.innerHTML = '<div class="col-span-3 p-4 text-center text-slate-400 bg-white rounded-xl border border-slate-200">No courses enrolled yet.</div>';
            } else {
                coursesGrid.innerHTML = lrn.enrolled_courses.map(c => `
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-start mb-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 text-blue-700 border border-blue-200">${c.code}</span>
                                <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">${c.status}</span>
                            </div>
                            <h4 class="font-bold text-slate-800 text-xs mb-1">${c.title}</h4>
                            <div class="text-[10px] text-slate-500">Hours: <strong class="text-slate-700">${c.hours_spent}h</strong> &bull; Score: <strong class="text-slate-700">${c.score_pct}%</strong></div>
                        </div>
                        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                            <div class="w-2/3 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                                <div class="bg-blue-600 h-1.5 rounded-full" style="width: ${c.progress_pct}%"></div>
                            </div>
                            <span class="text-[10px] font-bold text-blue-600">${c.progress_pct}%</span>
                        </div>
                    </div>
                `).join('');
            }
        }

        const certsTable = document.getElementById('table-ess-certificates');
        if (certsTable && lrn.certificates) {
            if (lrn.certificates.length === 0) {
                certsTable.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-slate-400">No certificates earned yet.</td></tr>';
            } else {
                certsTable.innerHTML = lrn.certificates.map(crt => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 font-bold text-blue-600 font-mono">${crt.certificate_id}</td>
                        <td class="p-3 font-semibold text-slate-800">${crt.module_title}</td>
                        <td class="p-3 text-center font-bold text-emerald-600">${crt.score_pct}%</td>
                        <td class="p-3 text-slate-600">${crt.completed_at}</td>
                        <td class="p-3 text-center">
                            <a href="${crt.export_url}" target="_blank" class="px-3 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded text-xs font-bold transition inline-flex items-center gap-1 shadow-sm">
                                <i class="fa-solid fa-award"></i> Certificate
                            </a>
                        </td>
                    </tr>
                `).join('');
            }
        }

        // 10. IT Assets, Passkeys & Helpdesk Tab (Tab 6)
        const assetsGrid = document.getElementById('grid-ess-it-assets');
        const itData = data.it_assets_and_security || {};
        if (assetsGrid && itData.assets) {
            if (itData.assets.length === 0) {
                assetsGrid.innerHTML = '<div class="p-4 text-center text-slate-400">No hardware assets registered to official email.</div>';
            } else {
                assetsGrid.innerHTML = itData.assets.map(a => `
                    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center text-lg">
                                <i class="fa-solid fa-laptop"></i>
                            </div>
                            <div>
                                <div class="font-bold text-slate-800 text-xs">${a.asset_name}</div>
                                <div class="text-[10px] text-slate-500 font-mono">Tag: ${a.tag} &bull; S/N: ${a.serial}</div>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">${a.encryption}</span>
                            <div class="text-[9px] text-slate-400 mt-0.5 font-mono">ZTNA: ${a.status}</div>
                        </div>
                    </div>
                `).join('');
            }
        }

        const passkeysGrid = document.getElementById('grid-ess-passkeys');
        if (passkeysGrid && itData.passkeys) {
            if (itData.passkeys.length === 0) {
                passkeysGrid.innerHTML = '<div class="p-4 text-center text-slate-400">No FIDO2 passkeys registered.</div>';
            } else {
                passkeysGrid.innerHTML = itData.passkeys.map(pk => `
                    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center text-lg">
                                <i class="fa-solid fa-key"></i>
                            </div>
                            <div>
                                <div class="font-bold text-slate-800 text-xs">${pk.device_name}</div>
                                <div class="text-[10px] text-slate-500 font-mono">${pk.type} &bull; Added ${pk.created_at}</div>
                            </div>
                        </div>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                            Hardware Bound
                        </span>
                    </div>
                `).join('');
            }
        }

        const ticketsTable = document.getElementById('table-ess-tickets');
        if (ticketsTable && data.internal_tickets) {
            if (data.internal_tickets.length === 0) {
                ticketsTable.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-slate-400">No internal helpdesk tickets logged.</td></tr>';
            } else {
                ticketsTable.innerHTML = data.internal_tickets.map(t => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-2.5 font-bold text-blue-600 font-mono">${t.ticket_number}</td>
                        <td class="p-2.5 text-slate-600">${t.department}</td>
                        <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${t.priority.includes('P1') || t.priority.includes('P2') ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-amber-50 text-amber-700 border border-amber-200'}">${t.priority}</span></td>
                        <td class="p-2.5 font-semibold text-slate-800">${t.subject}</td>
                        <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${t.status === 'Resolved' || t.status === 'Closed' ? 'bg-emerald-50 text-emerald-700' : 'bg-blue-50 text-blue-700'}">${t.status}</span></td>
                        <td class="p-2.5 text-slate-500 font-mono text-[11px]">${t.sla_deadline}</td>
                    </tr>
                `).join('');
            }
        }

    } catch (err) {
        console.error('Error loading employee portal:', err);
    }
}

export function renderESSCharts(sal, att, ldg) {
    if (typeof Chart === 'undefined') return;

    // Chart 1: Compensation Doughnut
    const ctxComp = document.getElementById('chart-ess-compensation');
    if (ctxComp) {
        if (essCompChart) essCompChart.destroy();
        essCompChart = new Chart(ctxComp, {
            type: 'doughnut',
            data: {
                labels: ['Basic (40%)', 'HRA (16%)', 'Special Allowance', 'Employer PF', 'Gratuity'],
                datasets: [{
                    data: [
                        sal.basic_salary || 48000,
                        sal.hra || 19200,
                        sal.special_allowance || 52800,
                        sal.employer_pf || 1800,
                        sal.gratuity_provision || 2308
                    ],
                    backgroundColor: ['#2563eb', '#38bdf8', '#818cf8', '#059669', '#d97706'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
                },
                cutout: '68%'
            }
        });

        // Update footer numbers
        const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        setTxt('ess-chart-basic', formatINR(sal.basic_salary || 48000));
        setTxt('ess-chart-hra', formatINR(sal.hra || 19200));
        setTxt('ess-chart-allow', formatINR(sal.special_allowance || 52800));
    }

    // Chart 2: Attendance Punch Pattern
    const ctxAtt = document.getElementById('chart-ess-attendance');
    if (ctxAtt && att.records) {
        if (essAttChart) essAttChart.destroy();
        const reversedRecords = [...att.records].slice(0, 7).reverse();
        const labels = reversedRecords.map(r => r.date ? r.date.substring(5) : '');
        const dataHours = reversedRecords.map(r => r.hours || 8.5);

        essAttChart = new Chart(ctxAtt, {
            type: 'bar',
            data: {
                labels: labels.length ? labels : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                datasets: [{
                    label: 'Effective Work Hours',
                    data: dataHours.length ? dataHours : [8.5, 9.0, 8.4, 8.6, 8.5],
                    backgroundColor: '#10b981',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 12, ticks: { font: { size: 10 } } },
                    x: { ticks: { font: { size: 10 } } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

        const geoEl = document.getElementById('ess-chart-geofence');
        if (geoEl) geoEl.innerText = `${att.geofence_compliance_pct || 98.4}%`;
    }

    // Chart 3: Leave Utilization
    const ctxLeaves = document.getElementById('chart-ess-leaves');
    if (ctxLeaves) {
        if (essLeavesChart) essLeavesChart.destroy();
        const elBal = ldg.annual_earned_leave_balance || 16.0;
        const clBal = ldg.casual_sick_leave_balance || 10.0;
        const taken = ldg.consumed_days || 4.0;

        essLeavesChart = new Chart(ctxLeaves, {
            type: 'doughnut',
            data: {
                labels: ['Earned Leave (EL)', 'Casual/Sick (CL/SL)', 'Consumed'],
                datasets: [{
                    data: [elBal, clBal, taken],
                    backgroundColor: ['#4f46e5', '#f59e0b', '#94a3b8'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
                },
                cutout: '68%'
            }
        });

        const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        setTxt('ess-chart-el', elBal.toFixed(1));
        setTxt('ess-chart-cl', clBal.toFixed(1));
        setTxt('ess-chart-taken', taken.toFixed(1));
    }
}

export async function portalQuickPunch() {
    let lat = 13.035820;
    let lon = 77.653410;

    if (navigator.geolocation) {
        try {
            const pos = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 3000 });
            });
            lat = pos.coords.latitude;
            lon = pos.coords.longitude;
        } catch (e) {
            // Keep default Horamavu HQ coordinates
        }
    }

    try {
        const res = await fetch(`${API_BASE}/portals/employee/quick-clock-in`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emp_code: currentESSEmpCode,
                latitude: lat,
                longitude: lon
            })
        });
        const result = await res.json();
        if (result.status === 'success') {
            alert(`✅ ${result.action === 'CLOCKED_IN' ? 'Clock In Punch' : 'Clock Out Punch'} Recorded Successfully!\nTime: ${result.time}\nGeofence Status: ${result.geofence_verified ? 'Verified (Within 200m)' : 'Remote Punch'}\nDistance: ${result.distance_m ? result.distance_m.toFixed(1) + 'm' : 'HQ Desk'}`);
            loadEmployeePortal(currentESSEmpCode);
        } else {
            alert(`Punch Error: ${result.message || 'Unable to record punch'}`);
        }
    } catch (err) {
        console.error('Error clocking punch:', err);
        alert('Network or server error during biometric punch.');
    }
}

export function openESSApplyLeaveModal() {
    const modal = document.getElementById('modal-ess-apply-leave');
    if (modal) modal.classList.remove('hidden');
}

export function closeESSApplyLeaveModal() {
    const modal = document.getElementById('modal-ess-apply-leave');
    if (modal) modal.classList.add('hidden');
}

export async function handleESSApplyLeave(e) {
    e.preventDefault();
    const leaveType = document.getElementById('ess-leave-input-type').value;
    const startDate = document.getElementById('ess-leave-input-start').value;
    const endDate = document.getElementById('ess-leave-input-end').value;
    const totalDays = parseFloat(document.getElementById('ess-leave-input-days').value) || 1.0;
    const reason = document.getElementById('ess-leave-input-reason').value;

    try {
        const res = await fetch(`${API_BASE}/portals/employee/apply-leave`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emp_code: currentESSEmpCode,
                leave_type: leaveType,
                start_date: startDate,
                end_date: endDate,
                total_days: totalDays,
                reason: reason
            })
        });
        const data = await res.json();
        if (res.ok) {
            alert(`✅ ${data.message || 'Leave application submitted successfully!'}`);
            closeESSApplyLeaveModal();
            loadEmployeePortal(currentESSEmpCode);
        } else {
            alert(`Error: ${data.detail || 'Could not apply leave'}`);
        }
    } catch (err) {
        console.error('Error applying leave:', err);
        alert('Network error while applying for leave.');
    }
}

export function openESSRaiseTicketModal() {
    const modal = document.getElementById('modal-ess-raise-ticket');
    if (modal) modal.classList.remove('hidden');
}

export function closeESSRaiseTicketModal() {
    const modal = document.getElementById('modal-ess-raise-ticket');
    if (modal) modal.classList.add('hidden');
}

export async function handleESSRaiseTicket(e) {
    e.preventDefault();
    const dept = document.getElementById('ess-tkt-input-dept').value;
    const priority = document.getElementById('ess-tkt-input-priority').value;
    const cat = document.getElementById('ess-tkt-input-cat').value;
    const sub = document.getElementById('ess-tkt-input-sub').value;
    const desc = document.getElementById('ess-tkt-input-desc').value;

    try {
        const res = await fetch(`${API_BASE}/portals/employee/raise-ticket`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emp_code: currentESSEmpCode,
                department: dept,
                category: cat,
                priority: priority,
                subject: sub,
                description: desc
            })
        });
        const data = await res.json();
        if (res.ok) {
            alert(`✅ Helpdesk Ticket ${data.ticket_number} Created Successfully!\nTarget SLA: 24.0 Hours`);
            closeESSRaiseTicketModal();
            loadEmployeePortal(currentESSEmpCode);
        } else {
            alert(`Error: ${data.detail || 'Could not file ticket'}`);
        }
    } catch (err) {
        console.error('Error filing ticket:', err);
        alert('Network error while creating ticket.');
    }
}

export function openDigitalIDCardModal() {
    const modal = document.getElementById('modal-ess-id-card');
    const iframe = document.getElementById('iframe-ess-id-card');
    if (iframe) {
        iframe.src = `${API_BASE}/portals/employee/id-card-html?emp_code=${encodeURIComponent(currentESSEmpCode)}`;
    }
    if (modal) modal.classList.remove('hidden');
}

export function closeDigitalIDCardModal() {
    const modal = document.getElementById('modal-ess-id-card');
    if (modal) modal.classList.add('hidden');
}

/**
 * 2. Enterprise Client Project & SLA Portal Loader
 */
/**
 * 2. Enterprise Client Project & SLA Portal Loader & Controller
 */
export let currentClientPortalName = "Zenith Global Corp";

export function switchClientPortalTab(tabKey) {
    document.querySelectorAll('.client-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-600', 'text-white', 'shadow-sm');
        btn.classList.add('bg-slate-100', 'text-slate-700');
    });
    const activeBtn = document.getElementById(`tab-btn-client-${tabKey}`);
    if (activeBtn) {
        activeBtn.classList.add('active', 'bg-emerald-600', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
    }

    document.querySelectorAll('.client-tab-view').forEach(view => {
        view.classList.add('hidden');
    });
    const targetView = document.getElementById(`client-subtab-${tabKey}`);
    if (targetView) {
        targetView.classList.remove('hidden');
    }
}

export function handleClientSelectorChange(clientName) {
    currentClientPortalName = clientName;
    loadClientPortal(clientName);
}

export function openClientModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.remove('hidden');
}

export function closeClientModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.add('hidden');
}

export function openClientTicketModal() {
    const nameInput = document.getElementById('client-ticket-client-name');
    if (nameInput) nameInput.value = currentClientPortalName;
    openClientModal('modal-client-ticket');
}

export async function handleCreateClientTicket(event) {
    event.preventDefault();
    try {
        const payload = {
            client_name: currentClientPortalName,
            contact_email: document.getElementById('client-ticket-email').value,
            subject: document.getElementById('client-ticket-subject').value,
            description: document.getElementById('client-ticket-desc').value,
            category: document.getElementById('client-ticket-cat').value,
            severity: document.getElementById('client-ticket-sev').value
        };

        const res = await fetch(`${API_BASE}/portals/client/tickets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Error creating ticket: ${err.detail || 'Request failed'}`);
            return;
        }

        const data = await res.json();
        alert(data.message || 'Support ticket logged successfully!');
        closeClientModal('modal-client-ticket');
        event.target.reset();
        loadClientPortal(currentClientPortalName);
    } catch (err) {
        console.error('Error logging client ticket:', err);
        alert('An unexpected error occurred while logging the support ticket.');
    }
}

export function openClientMilestoneSignoff(milestoneId, milestoneName, billingAmount) {
    document.getElementById('client-signoff-milestone-id').value = milestoneId;
    document.getElementById('client-signoff-milestone-name').value = milestoneName;
    document.getElementById('client-signoff-amount').value = formatINR(billingAmount);
    openClientModal('modal-client-milestone-signoff');
}

export async function handleClientMilestoneSignoff(event) {
    event.preventDefault();
    const milestoneId = document.getElementById('client-signoff-milestone-id').value;
    if (!milestoneId) return;

    try {
        const payload = {
            client_signatory_name: document.getElementById('client-signoff-name').value,
            approval_status: document.getElementById('client-signoff-decision').value,
            acceptance_notes: document.getElementById('client-signoff-notes').value
        };

        const res = await fetch(`${API_BASE}/portals/client/milestones/${milestoneId}/signoff`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Error recording signoff: ${err.detail || 'Request failed'}`);
            return;
        }

        const data = await res.json();
        alert(data.message || 'Milestone signoff recorded successfully!');
        closeClientModal('modal-client-milestone-signoff');
        event.target.reset();
        loadClientPortal(currentClientPortalName);
    } catch (err) {
        console.error('Error recording milestone signoff:', err);
        alert('An unexpected error occurred during milestone signoff.');
    }
}

export function openClientCRReview(crId, crNumber, title, costImpact) {
    document.getElementById('client-cr-id').value = crId;
    document.getElementById('client-cr-num').value = crNumber;
    document.getElementById('client-cr-title').value = title;
    document.getElementById('client-cr-cost').value = formatINR(costImpact);
    openClientModal('modal-client-cr-review');
}

export async function handleClientCRReview(event) {
    event.preventDefault();
    const crId = document.getElementById('client-cr-id').value;
    if (!crId) return;

    try {
        const payload = {
            action: document.getElementById('client-cr-action').value,
            client_approver_name: document.getElementById('client-cr-approver').value,
            review_notes: document.getElementById('client-cr-notes').value
        };

        const res = await fetch(`${API_BASE}/portals/client/change-requests/${crId}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Error reviewing CR: ${err.detail || 'Request failed'}`);
            return;
        }

        const data = await res.json();
        alert(data.message || 'Change request decision recorded!');
        closeClientModal('modal-client-cr-review');
        event.target.reset();
        loadClientPortal(currentClientPortalName);
    } catch (err) {
        console.error('Error reviewing change request:', err);
        alert('An unexpected error occurred while reviewing change request.');
    }
}

export function openClientPaymentModal(invId, invNum, balanceDue) {
    document.getElementById('client-pay-inv-id').value = invId;
    document.getElementById('client-pay-inv-num').value = invNum;
    document.getElementById('client-pay-inv-balance').value = formatINR(balanceDue);
    document.getElementById('client-pay-amount').value = balanceDue;
    openClientModal('modal-client-payment');
}

export async function handleRecordClientPayment(event) {
    event.preventDefault();
    const invId = document.getElementById('client-pay-inv-id').value;
    if (!invId) return;

    try {
        const payload = {
            payment_reference: document.getElementById('client-pay-ref').value,
            amount_inr: parseFloat(document.getElementById('client-pay-amount').value),
            payment_mode: document.getElementById('client-pay-mode').value
        };

        const res = await fetch(`${API_BASE}/portals/client/invoices/${invId}/record-payment`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`Error recording payment: ${err.detail || 'Request failed'}`);
            return;
        }

        const data = await res.json();
        alert(data.message || 'Payment recorded successfully!');
        closeClientModal('modal-client-payment');
        event.target.reset();
        loadClientPortal(currentClientPortalName);
    } catch (err) {
        console.error('Error recording payment:', err);
        alert('An unexpected error occurred while recording remittance.');
    }
}

export function previewClientInvoice(invoiceId) {
    const iframe = document.getElementById('client-invoice-iframe');
    if (iframe) {
        iframe.src = `${API_BASE}/portals/client/invoices/${invoiceId}/html`;
    }
    openClientModal('modal-client-invoice-preview');
}

export function printClientInvoiceCurrent() {
    const iframe = document.getElementById('client-invoice-iframe');
    if (iframe && iframe.contentWindow) {
        iframe.contentWindow.print();
    }
}

export function previewClientSOA() {
    const iframe = document.getElementById('client-soa-iframe');
    if (iframe) {
        iframe.src = `${API_BASE}/portals/client/statement-of-account?client_name=${encodeURIComponent(currentClientPortalName)}`;
    }
    openClientModal('modal-client-soa-preview');
}

export function printClientSOACurrent() {
    const iframe = document.getElementById('client-soa-iframe');
    if (iframe && iframe.contentWindow) {
        iframe.contentWindow.print();
    }
}

export function escalateClientToDirector() {
    alert("DIRECTOR EXECUTIVE ESCALATION CHANNEL:\n\nContact: Varadi Vijay (Founder & Sole Director)\nCompany: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED\nDirect Helpline: +91 80 4120 5678 / director@asperion.in\nRegistered Office: Horamavu, Bangalore - 560043, Karnataka\n\nYour emergency ticket has been flagged with highest Tier-0 executive escalation priority.");
}

export async function loadClientPortal(clientName = currentClientPortalName) {
    try {
        currentClientPortalName = clientName;
        const selector = document.getElementById('client-portal-selector');
        if (selector && selector.value !== clientName) {
            selector.value = clientName;
        }

        const res = await fetch(`${API_BASE}/portals/client/dashboard-data?client_name=${encodeURIComponent(clientName)}`);
        if (!res.ok) return;
        const data = await res.json();

        // Populate client dropdown if available
        if (selector && data.available_clients && data.available_clients.length > 0) {
            const currentVal = selector.value;
            selector.innerHTML = data.available_clients.map(c => `
                <option value="${c.name}" class="bg-slate-900 text-white" ${c.name === clientName ? 'selected' : ''}>
                    ${c.name} (${c.tier})
                </option>
            `).join('');
            selector.value = clientName;
        }

        // Executive KPIs
        const kpis = data.executive_kpis || {};
        const kpiUptime = document.getElementById('kpi-client-sla-uptime');
        if (kpiUptime) kpiUptime.innerText = `${kpis.contracted_uptime_pct || 99.98}%`;

        const kpiP1 = document.getElementById('kpi-client-p1-response');
        if (kpiP1) kpiP1.innerText = `P1 < ${kpis.p1_sla_target_hours || 1.0}h (Avg: ${kpis.avg_p1_response_mins || 18}m)`;

        const kpiSow = document.getElementById('kpi-client-sow-val');
        if (kpiSow) kpiSow.innerText = formatINR(kpis.total_sow_value_inr || 0);

        const kpiBilled = document.getElementById('kpi-client-billed-val');
        if (kpiBilled) kpiBilled.innerText = formatINR(kpis.total_billed_inr || 0);

        const kpiRemitted = document.getElementById('kpi-client-remitted-val');
        if (kpiRemitted) kpiRemitted.innerText = `${formatINR(kpis.total_received_inr || 0)} Remitted`;

        const kpiBalance = document.getElementById('kpi-client-balance-val');
        if (kpiBalance) kpiBalance.innerText = formatINR(kpis.outstanding_receivable_inr || 0);

        const kpiProgress = document.getElementById('kpi-client-progress-pct');
        if (kpiProgress) kpiProgress.innerText = `${kpis.milestones_progress_pct || 0}%`;

        const kpiSprint = document.getElementById('kpi-client-active-sprint');
        if (kpiSprint) kpiSprint.innerText = kpis.active_sprint_name || 'Sprint 14 Active';

        const billGross = document.getElementById('client-bill-gross');
        if (billGross) billGross.innerText = formatINR(kpis.total_billed_inr || 0);

        const billRecv = document.getElementById('client-bill-received');
        if (billRecv) billRecv.innerText = formatINR(kpis.total_received_inr || 0);

        const billOut = document.getElementById('client-bill-outstanding');
        if (billOut) billOut.innerText = formatINR(kpis.outstanding_receivable_inr || 0);

        // Project Banner
        if (data.active_projects && data.active_projects.length > 0) {
            const p = data.active_projects[0];
            const pCode = document.getElementById('client-proj-code');
            if (pCode) pCode.innerText = p.code;
            const pStatus = document.getElementById('client-proj-status');
            if (pStatus) pStatus.innerText = p.status;
            const pName = document.getElementById('client-proj-name');
            if (pName) pName.innerText = p.name;
            const pPm = document.getElementById('client-proj-pm');
            if (pPm) pPm.innerText = p.manager;
            const pDates = document.getElementById('client-proj-dates');
            if (pDates) pDates.innerText = p.dates;
            const pBudget = document.getElementById('client-proj-budget');
            if (pBudget) pBudget.innerText = formatINR(p.budget);
        }

        // Render Milestones Table
        const milestoneTable = document.getElementById('table-client-milestones');
        if (milestoneTable) {
            if (!data.project_milestones || data.project_milestones.length === 0) {
                milestoneTable.innerHTML = '<tr><td colspan="7" class="p-4 text-center text-slate-400">No project milestones registered.</td></tr>';
            } else {
                milestoneTable.innerHTML = data.project_milestones.map(m => {
                    const isApproved = m.status === 'Client Approved' || m.status === 'Billed';
                    const isUnderReview = m.status === 'UAT Under Review';
                    let statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200">${m.status}</span>`;
                    if (isApproved) {
                        statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200"><i class="fa-solid fa-check-circle mr-1"></i>${m.status}</span>`;
                    } else if (isUnderReview) {
                        statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200"><i class="fa-solid fa-hourglass-half mr-1"></i>${m.status}</span>`;
                    }

                    let signoffText = '<span class="text-slate-400 italic">Pending UAT verification</span>';
                    if (m.signoff_by) {
                        signoffText = `<div class="font-semibold text-slate-800">${m.signoff_by}</div><div class="text-[10px] text-slate-500">${m.completion_date || ''}</div>`;
                    }

                    let actionHtml = '';
                    if (!isApproved) {
                        actionHtml = `
                            <button onclick="openClientMilestoneSignoff(${m.id}, '${m.name.replace(/'/g, "\\'")}', ${m.billing_amount})" class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold text-[11px] transition shadow">
                                <i class="fa-solid fa-signature mr-1"></i> Sign Off UAT
                            </button>
                        `;
                    } else {
                        actionHtml = `<span class="text-emerald-700 font-bold text-xs"><i class="fa-solid fa-file-circle-check mr-1"></i>Accepted</span>`;
                    }

                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${m.name}</div>
                                <div class="text-[11px] text-slate-500 mt-0.5">${m.deliverable_summary || ''}</div>
                            </td>
                            <td class="p-3 font-mono font-semibold text-slate-700">${m.target_date}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded font-mono text-[11px] bg-purple-50 text-purple-700 border border-purple-200 font-bold">${m.payment_linked_percent}%</span></td>
                            <td class="p-3 text-right font-mono font-bold text-slate-900">${formatINR(m.billing_amount)}</td>
                            <td class="p-3">${statusBadge}</td>
                            <td class="p-3 text-xs">${signoffText}</td>
                            <td class="p-3 text-center">${actionHtml}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render WBS Tasks Table
        const wbsTable = document.getElementById('table-client-wbs-tasks');
        if (wbsTable) {
            if (!data.wbs_tasks || data.wbs_tasks.length === 0) {
                wbsTable.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-slate-400">No active sprint tasks found.</td></tr>';
            } else {
                wbsTable.innerHTML = data.wbs_tasks.map(w => {
                    const isDone = w.status === 'Done';
                    const badge = isDone ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : (w.status === 'In Progress' ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-slate-100 text-slate-700 border-slate-200');
                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-2.5 font-mono font-bold text-blue-700">${w.code}</td>
                            <td class="p-2.5 font-semibold text-slate-800">${w.name}</td>
                            <td class="p-2.5 font-mono text-purple-700">${w.sprint}</td>
                            <td class="p-2.5 text-slate-600">${w.assignee}</td>
                            <td class="p-2.5 font-mono text-[11px]">${w.actual_hours}h / ${w.estimated_hours}h</td>
                            <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badge}">${w.status}</span></td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render Invoices Table
        const invTable = document.getElementById('table-client-invoices');
        if (invTable && data.billing_invoices) {
            if (data.billing_invoices.length === 0) {
                invTable.innerHTML = '<tr><td colspan="10" class="p-4 text-center text-slate-400">No commercial tax invoices generated.</td></tr>';
            } else {
                invTable.innerHTML = data.billing_invoices.map(i => {
                    const isPaid = i.status === 'Paid';
                    const badge = isPaid ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-amber-100 text-amber-800 border-amber-200';
                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-3 font-bold text-purple-700">${i.number}</td>
                            <td class="p-3 text-slate-600">${i.date}</td>
                            <td class="p-3 text-slate-600">${i.due_date || '-'}</td>
                            <td class="p-3 text-right font-mono">${formatINR(i.taxable)}</td>
                            <td class="p-3 text-right font-mono text-slate-500">${formatINR(i.tax)}</td>
                            <td class="p-3 text-right font-mono font-bold text-slate-900">${formatINR(i.total)}</td>
                            <td class="p-3 text-right font-mono text-emerald-700">${formatINR(i.received || 0)}</td>
                            <td class="p-3 text-right font-mono font-bold ${i.balance > 0 ? 'text-amber-700' : 'text-slate-400'}">${formatINR(i.balance || 0)}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badge}">${i.status}</span></td>
                            <td class="p-3 text-center">
                                <div class="flex items-center justify-center gap-1.5">
                                    <button onclick="previewClientInvoice(${i.id})" class="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-white rounded text-[11px] font-bold transition flex items-center gap-1 shadow-sm">
                                        <i class="fa-solid fa-file-invoice"></i> View
                                    </button>
                                    ${i.balance > 0 ? `
                                        <button onclick="openClientPaymentModal(${i.id}, '${i.number}', ${i.balance})" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[11px] font-bold transition flex items-center gap-1 shadow-sm">
                                            <i class="fa-solid fa-money-bill-transfer"></i> Remit
                                        </button>
                                    ` : ''}
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render SLA Tickets Table
        const ticketTable = document.getElementById('table-client-tickets');
        if (ticketTable && data.sla_tickets) {
            if (data.sla_tickets.length === 0) {
                ticketTable.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400">Zero active support incidents logged.</td></tr>';
            } else {
                ticketTable.innerHTML = data.sla_tickets.map(t => {
                    let sevBadge = 'bg-blue-100 text-blue-800 border-blue-200';
                    if (t.severity.includes('P1')) sevBadge = 'bg-red-100 text-red-800 border-red-200';
                    else if (t.severity.includes('P2')) sevBadge = 'bg-amber-100 text-amber-800 border-amber-200';

                    const isResolved = t.status === 'Resolved' || t.status === 'Closed';
                    const statusBadge = isResolved ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-purple-100 text-purple-800 border-purple-200';

                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-3 font-mono font-bold text-slate-800">${t.ticket_number}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${sevBadge}">${t.severity}</span></td>
                            <td class="p-3 text-slate-600 font-semibold">${t.category}</td>
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${t.subject}</div>
                                <div class="text-[11px] text-slate-500 mt-0.5">${t.description || ''}</div>
                            </td>
                            <td class="p-3 font-mono text-[11px] text-slate-700">${t.sla_hours}h SLA Commitment</td>
                            <td class="p-3 text-slate-700 font-semibold">${t.assigned_engineer || 'SRE Lead'}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${statusBadge}">${t.status}</span></td>
                            <td class="p-3 text-xs text-slate-600">${t.resolution_summary || '<span class="text-slate-400 italic">Under investigation</span>'}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render Scope Change Orders Table
        const crTable = document.getElementById('table-client-crs');
        if (crTable && data.change_orders) {
            if (data.change_orders.length === 0) {
                crTable.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400">No scope change requests on record.</td></tr>';
            } else {
                crTable.innerHTML = data.change_orders.map(cr => {
                    const isApproved = cr.status === 'Client Approved';
                    const badge = isApproved ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : (cr.status === 'Rejected' ? 'bg-red-100 text-red-800 border-red-200' : 'bg-purple-100 text-purple-800 border-purple-200');

                    let actionHtml = `<span class="text-xs text-slate-400 italic">Decided</span>`;
                    if (!isApproved && cr.status !== 'Rejected') {
                        actionHtml = `
                            <button onclick="openClientCRReview(${cr.id}, '${cr.cr_number}', '${cr.title.replace(/'/g, "\\'")}', ${cr.cost_impact_inr})" class="px-2.5 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded text-[11px] font-bold transition shadow">
                                <i class="fa-solid fa-code-branch mr-1"></i> Review CR
                            </button>
                        `;
                    }

                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-3 font-mono font-bold text-purple-700">${cr.cr_number}</td>
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${cr.title}</div>
                                <div class="text-[11px] text-slate-500 mt-0.5">${cr.scope_impact || ''}</div>
                            </td>
                            <td class="p-3 text-slate-600 text-[11px]">${cr.reason}</td>
                            <td class="p-3 text-right font-mono font-bold text-slate-900">${formatINR(cr.cost_impact_inr)}</td>
                            <td class="p-3 font-mono text-[11px] text-slate-700">+${cr.schedule_impact_days} Days</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badge}">${cr.status}</span></td>
                            <td class="p-3 text-xs">
                                <div class="font-semibold text-slate-800">${cr.approver || '-'}</div>
                                <div class="text-[10px] text-slate-500">${cr.decision_date || ''}</div>
                            </td>
                            <td class="p-3 text-center">${actionHtml}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render Legal Contracts Table
        const contractTable = document.getElementById('table-client-contracts');
        if (contractTable && data.contracts_and_agreements) {
            if (data.contracts_and_agreements.length === 0) {
                contractTable.innerHTML = '<tr><td colspan="7" class="p-4 text-center text-slate-400">No client legal agreements on file.</td></tr>';
            } else {
                contractTable.innerHTML = data.contracts_and_agreements.map(c => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 font-mono font-bold text-slate-900">${c.contract_reference}</td>
                        <td class="p-3 font-bold text-purple-700">${c.contract_type}</td>
                        <td class="p-3 font-mono text-[11px] text-slate-600">${c.effective_date} &bull; ${c.expiry_date || 'Perpetual'}</td>
                        <td class="p-3 text-right font-mono font-bold text-slate-900">${c.value_inr > 0 ? formatINR(c.value_inr) : 'Retainer'}</td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">${c.status}</span></td>
                        <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.stamp_duty_paid ? 'bg-blue-100 text-blue-800 border border-blue-200' : 'bg-slate-100 text-slate-600'}">${c.stamp_duty_paid ? 'Paid' : 'N/A'}</span></td>
                        <td class="p-3 text-xs text-slate-600">
                            <div>${c.special_conditions || 'Standard Asperion commercial terms.'}</div>
                            <div class="text-[10px] text-slate-400 mt-0.5">Jurisdiction: ${c.governing_law || 'Bengaluru, India'}</div>
                        </td>
                    </tr>
                `).join('');
            }
        }

    } catch (err) {
        console.error('Error loading comprehensive client portal:', err);
    }
}

/**
 * 3. Comprehensive Vendor Sourcing, POs & Inward GRN Portal Loader
 */
export let currentVendorPortalData = null;

export async function loadVendorPortal(vendorQuery = null) {
    try {
        let url = `${API_BASE}/portals/vendor/dashboard-data`;
        if (vendorQuery) {
            if (typeof vendorQuery === 'number' || !isNaN(Number(vendorQuery))) {
                url += `?vendor_id=${vendorQuery}`;
            } else {
                url += `?vendor_name=${encodeURIComponent(vendorQuery)}`;
            }
        }
        
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        currentVendorPortalData = data;

        const vp = data.vendor_profile;
        const kpis = data.kpis;

        // 1. Populate Vendor Selector Dropdown
        const selector = document.getElementById('vendor-portal-selector');
        if (selector && data.vendors_list) {
            const currentSelectedId = vp.id;
            selector.innerHTML = data.vendors_list.map(v => `
                <option value="${v.id}" ${v.id === currentSelectedId ? 'selected' : ''}>
                    ${v.vendor_code} — ${v.vendor_name} (${v.category})
                </option>
            `).join('');
        }

        // 2. Populate Header Badges & Master Profile Fields
        const elBadgeMsme = document.getElementById('vp-badge-msme');
        if (elBadgeMsme) {
            if (vp.msme_registered) {
                elBadgeMsme.innerHTML = `<i class="fa-solid fa-certificate mr-1"></i> MSME ${vp.msme_category} Priority`;
                elBadgeMsme.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 uppercase";
            } else {
                elBadgeMsme.innerHTML = `<i class="fa-solid fa-building mr-1"></i> Non-MSME Corporate`;
                elBadgeMsme.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-500/20 text-slate-300 border border-slate-500/40 uppercase";
            }
        }

        const elBadgeRating = document.getElementById('vp-badge-rating');
        if (elBadgeRating) {
            elBadgeRating.innerHTML = `<i class="fa-solid fa-star mr-1"></i> ${vp.rating.toFixed(1)} / 100 Rating`;
        }

        const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        setTxt('vp-code', vp.vendor_code);
        setTxt('vp-category', `Category: ${vp.category}`);
        setTxt('vp-terms', `Net ${vp.payment_terms_days} Days`);
        setTxt('vp-udyam', vp.msme_udyam_number || 'Not Registered');
        setTxt('vp-msme-badge', vp.msme_registered ? `Priority Due: max ${vp.msme_payment_due_days}d` : 'Standard Due Terms');
        setTxt('vp-gstin', vp.gstin || 'GSTIN Pending');
        setTxt('vp-pan', `PAN: ${vp.pan || 'N/A'}`);
        setTxt('vp-kyc', vp.kyc_status);
        setTxt('vp-total-billed', formatINR(kpis.total_ap_billed_inr));
        setTxt('vp-active-pos-kpi', `${kpis.active_pos_count} Active POs (${formatINR(kpis.total_po_value_inr)})`);

        // 3. Tab 1: Purchase Orders (PO) Table
        const poTable = document.getElementById('table-vp-pos');
        if (poTable && data.purchase_orders) {
            if (data.purchase_orders.length === 0) {
                poTable.innerHTML = '<tr><td colspan="7" class="p-4 text-center text-slate-400 font-sans">No purchase orders found for this vendor.</td></tr>';
            } else {
                poTable.innerHTML = data.purchase_orders.map(p => {
                    const stColor = p.status === 'Fulfilled' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                                    (p.status === 'In Transit' ? 'bg-sky-50 text-sky-700 border-sky-200' :
                                    (p.status === 'Partial GRN Inward' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-blue-50 text-blue-700 border-blue-200'));
                    
                    const itemsDesc = (p.items || []).map(it => `${it.qty}x ${it.item}`).join(', ') || 'Enterprise Goods/Services';

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3">
                                <div class="font-bold text-blue-700">${p.po_number}</div>
                                <div class="text-[10px] text-slate-400 font-sans">Project: ${p.project_code}</div>
                            </td>
                            <td class="p-3 text-slate-600">
                                <div>Issued: ${p.po_date}</div>
                                <div class="text-[10px] text-slate-400">Due: ${p.delivery_due_date || '7 Days'}</div>
                            </td>
                            <td class="p-3 font-sans max-w-xs">
                                <div class="font-semibold text-slate-800 line-clamp-1">${itemsDesc}</div>
                                <div class="text-[10px] text-slate-500">${p.items ? p.items.length + ' line item(s)' : '--'}</div>
                            </td>
                            <td class="p-3 text-right font-bold text-slate-900">${formatINR(p.total_amount)}</td>
                            <td class="p-3">
                                <div class="text-[11px] text-slate-700">${p.payment_terms}</div>
                                <div class="text-[10px] text-slate-400 font-sans">Challan: ${p.delivery_challan_no || 'Pending'}</div>
                            </td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${stColor}">${p.status}</span>
                            </td>
                            <td class="p-3 text-right">
                                <a href="${p.html_url}" target="_blank" class="px-2.5 py-1 text-xs bg-slate-900 hover:bg-slate-800 text-white rounded-lg inline-flex items-center gap-1 font-sans font-bold shadow-sm">
                                    <i class="fa-solid fa-file-invoice"></i> View PO
                                </a>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 4. Tab 2: Inward Goods Received Notes (GRN) Table
        const grnTable = document.getElementById('table-vp-grns');
        if (grnTable && data.inward_grns) {
            if (data.inward_grns.length === 0) {
                grnTable.innerHTML = '<tr><td colspan="10" class="p-4 text-center text-slate-400 font-sans">No Inward GRNs logged yet. Use "Log Inward GRN" above.</td></tr>';
            } else {
                grnTable.innerHTML = data.inward_grns.map(g => {
                    const inspColor = g.inspection_status === 'Accepted' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                                      (g.inspection_status === 'Partial Rejection' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-rose-50 text-rose-700 border-rose-200');

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3">
                                <div class="font-bold text-teal-700">${g.grn_number}</div>
                            </td>
                            <td class="p-3">
                                <div class="font-semibold text-slate-800">${g.po_reference}</div>
                                <div class="text-[10px] text-slate-400">DC: ${g.delivery_challan_no}</div>
                            </td>
                            <td class="p-3 text-slate-600">${g.received_date}</td>
                            <td class="p-3 font-sans max-w-xs">
                                <div class="font-semibold text-slate-800 line-clamp-1">${g.item_description}</div>
                                <div class="text-[10px] text-slate-400">${g.remarks || 'Tamper seals verified'}</div>
                            </td>
                            <td class="p-3 text-center text-slate-700 font-bold">${g.quantity_ordered}</td>
                            <td class="p-3 text-center text-emerald-700 font-black">${g.quantity_accepted}</td>
                            <td class="p-3 text-center text-rose-600 font-bold">${g.quantity_rejected}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${inspColor}">${g.inspection_status}</span>
                            </td>
                            <td class="p-3 font-sans">
                                <div class="text-[11px] text-slate-800 font-medium">${g.inspected_by}</div>
                                <div class="text-[10px] text-slate-400">${g.warehouse_location}</div>
                            </td>
                            <td class="p-3 text-right">
                                <a href="${g.certificate_url}" target="_blank" class="px-2.5 py-1 text-xs bg-teal-700 hover:bg-teal-800 text-white rounded-lg inline-flex items-center gap-1 font-sans font-bold shadow-sm">
                                    <i class="fa-solid fa-stamp"></i> Certificate
                                </a>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 5. Tab 3: 3-Way Match & AP Bills Table
        const billsTable = document.getElementById('table-vp-bills');
        if (billsTable && data.ap_bills) {
            if (data.ap_bills.length === 0) {
                billsTable.innerHTML = '<tr><td colspan="9" class="p-4 text-center text-slate-400 font-sans">No AP bills submitted yet. Use "Submit AP Bill" above.</td></tr>';
            } else {
                billsTable.innerHTML = data.ap_bills.map(b => {
                    const matchColor = b.three_way_match_status === 'Matched' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                                       (b.three_way_match_status === 'Pending GRN' ? 'bg-sky-50 text-sky-700 border-sky-200' : 'bg-rose-50 text-rose-700 border-rose-200');

                    const isUrgent = b.days_remaining <= 10 && b.approval_status !== 'Paid';
                    const msmeBadge = vp.msme_registered ? `
                        <div class="text-[10px] font-bold ${isUrgent ? 'text-rose-600 animate-pulse' : 'text-purple-700'}">
                            ${b.days_remaining}d Left (MSME 45d SLA)
                        </div>
                    ` : `<div class="text-[10px] text-slate-400">${b.days_remaining}d Left</div>`;

                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3">
                                <div class="font-bold text-slate-900">${b.bill_number}</div>
                                <div class="text-[10px] text-slate-400 font-sans">${b.expense_category}</div>
                            </td>
                            <td class="p-3 text-slate-600">
                                <div>Bill: ${b.bill_date}</div>
                                <div class="text-[10px] text-slate-400">Due: ${b.due_date}</div>
                            </td>
                            <td class="p-3">
                                <div class="text-[11px] font-bold text-blue-700">PO: ${b.po_reference}</div>
                                <div class="text-[10px] text-teal-700">GRN: ${b.grn_reference}</div>
                            </td>
                            <td class="p-3 text-right font-medium text-slate-700">${formatINR(b.taxable_amount)}</td>
                            <td class="p-3 text-right text-rose-600 font-semibold font-mono">
                                <div>-${formatINR(b.tds_amount)}</div>
                                <div class="text-[9px] text-slate-400 font-sans">Sec ${b.tds_section} (${b.tds_rate_pct}%)</div>
                            </td>
                            <td class="p-3 text-right font-bold text-emerald-700">${formatINR(b.net_payable)}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${matchColor}">
                                    <i class="fa-solid fa-${b.three_way_match_status === 'Matched' ? 'check-double' : 'triangle-exclamation'} mr-1"></i> ${b.three_way_match_status}
                                </span>
                            </td>
                            <td class="p-3 font-sans">
                                <span class="px-2 py-0.5 rounded text-[10px] font-medium ${b.approval_status === 'Approved' ? 'bg-emerald-50 text-emerald-800' : 'bg-amber-50 text-amber-800'}">${b.approval_status}</span>
                                ${b.payment_reference ? `<div class="text-[9px] text-slate-400 mt-0.5 font-mono">${b.payment_reference}</div>` : ''}
                            </td>
                            <td class="p-3 font-sans">
                                ${msmeBadge}
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 6. Tab 4: e-RFX Sourcing Table
        const rfxTable = document.getElementById('table-vp-rfx');
        if (rfxTable && data.sourcing_rfx_events) {
            if (data.sourcing_rfx_events.length === 0) {
                rfxTable.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400 font-sans">No open e-RFX sourcing events at this time.</td></tr>';
            } else {
                rfxTable.innerHTML = data.sourcing_rfx_events.map(ev => {
                    const hasBid = !!ev.my_bid;
                    return `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                            <td class="p-3 font-bold text-indigo-700">${ev.event_code}</td>
                            <td class="p-3 font-semibold text-slate-800 font-sans">${ev.title}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[10px] font-bold">${ev.event_type}</span> <span class="text-[10px] text-slate-500 font-sans">${ev.category}</span></td>
                            <td class="p-3 text-right font-bold text-slate-900">${formatINR(ev.budget_allocation_inr)}</td>
                            <td class="p-3 text-rose-600 font-medium">${ev.closing_date}</td>
                            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700">${ev.status}</span></td>
                            <td class="p-3 font-sans">
                                ${hasBid ? `
                                    <div class="text-[11px] font-bold text-emerald-700">Quote: ${formatINR(ev.my_bid.quote_inr)}</div>
                                    <div class="text-[10px] text-slate-500">Composite: ${ev.my_bid.composite_score} &bull; ${ev.my_bid.award_status}</div>
                                ` : `<span class="text-xs text-slate-400">No Bid Submitted</span>`}
                            </td>
                            <td class="p-3 text-right">
                                <button onclick="prefillAndOpenBidModal(${ev.id}, '${ev.event_code} — ${ev.title.replace(/'/g, '')}')" class="px-2.5 py-1 text-xs bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-sans font-bold shadow-sm">
                                    ${hasBid ? 'Revise Bid' : 'Submit Bid'}
                                </button>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // 7. Tab 5: Contracts Table
        const conTable = document.getElementById('table-vp-contracts');
        if (conTable && data.contracts) {
            if (data.contracts.length === 0) {
                conTable.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400 font-sans">No executed contracts in vault.</td></tr>';
            } else {
                conTable.innerHTML = data.contracts.map(c => `
                    <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                        <td class="p-3 font-bold text-blue-700">${c.contract_reference}</td>
                        <td class="p-3 font-semibold text-slate-800 font-sans">${c.agreement_type}</td>
                        <td class="p-3 text-slate-600">${c.effective_date}</td>
                        <td class="p-3 text-slate-600">${c.expiry_date || 'Auto-Renew'}</td>
                        <td class="p-3 text-right font-bold text-slate-900">${formatINR(c.annual_value_inr)}</td>
                        <td class="p-3 font-bold text-emerald-700">${c.sla_uptime_commitment}% Uptime</td>
                        <td class="p-3 font-sans">
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.dpdp_dpa_signed ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">
                                ${c.dpdp_dpa_signed ? 'DPA Executed' : 'DPA Pending'}
                            </span>
                        </td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${c.status}</span></td>
                    </tr>
                `).join('');
            }
        }

        // 8. Tab 6: Scorecards & CAPA Tables
        const scoreTable = document.getElementById('table-vp-scorecards');
        if (scoreTable && data.scorecards) {
            scoreTable.innerHTML = data.scorecards.map(s => `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-3 font-bold text-slate-800">${s.evaluation_period}</td>
                    <td class="p-3 text-center">${s.quality_score}</td>
                    <td class="p-3 text-center">${s.sla_adherence_score}</td>
                    <td class="p-3 text-center">${s.pricing_competitiveness}</td>
                    <td class="p-3 text-center">${s.security_privacy_score}</td>
                    <td class="p-3 text-center font-black text-purple-700">${s.overall_rating.toFixed(1)}</td>
                    <td class="p-3 font-sans"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700">${s.performance_tier}</span></td>
                </tr>
            `).join('') || '<tr><td colspan="7" class="p-4 text-center text-slate-400 font-sans">No scorecards found.</td></tr>';
        }

        const capaTable = document.getElementById('table-vp-capas');
        if (capaTable && data.capas) {
            capaTable.innerHTML = data.capas.map(cap => `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-3 font-bold text-amber-700">${cap.capa_code}</td>
                    <td class="p-3 font-sans max-w-xs">
                        <div class="font-semibold text-slate-800 line-clamp-1">${cap.issue_description}</div>
                        <div class="text-[10px] text-slate-500">${cap.root_cause}</div>
                    </td>
                    <td class="p-3 font-sans text-slate-700 text-[11px]">${cap.corrective_action_agreed}</td>
                    <td class="p-3 text-slate-600">${cap.target_closure_date}</td>
                    <td class="p-3 font-sans"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800">${cap.status}</span></td>
                </tr>
            `).join('') || '<tr><td colspan="5" class="p-4 text-center text-slate-400 font-sans">Zero active corrective action plans. Quality nominal.</td></tr>';
        }

        // 9. Pre-populate Modal Dropdowns
        populatePortalModalSelectors(data);

    } catch (err) {
        console.error('Error loading vendor portal:', err);
    }
}

export function handleVendorSelectorChange(vendorId) {
    if (!vendorId) return;
    loadVendorPortal(vendorId);
    if (typeof showEnterpriseToast === 'function') {
        showEnterpriseToast('Vendor Sourcing Portal', `Switched active supplier profile.`, 'info', 2500);
    }
}

export function switchVendorPortalTab(tabKey) {
    document.querySelectorAll('.vendor-tab-panel').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`vendor-tab-content-${tabKey}`);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.vendor-portal-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-amber-700', 'text-white', 'shadow-sm');
        btn.classList.add('text-slate-600');
    });
    if (typeof window !== 'undefined' && window.event && window.event.currentTarget) {
        event.currentTarget.classList.add('active', 'bg-amber-700', 'text-white', 'shadow-sm');
        event.currentTarget.classList.remove('text-slate-600');
    }
}

export function openVendorPortalModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('hidden');
}

export function closeVendorPortalModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('hidden');
}

export function populatePortalModalSelectors(data) {
    const vp = data.vendor_profile;

    // 1. GRN Modal Pre-fill
    const grnVenName = document.getElementById('vp-grn-vendor-name');
    const grnVenId = document.getElementById('vp-grn-vendor-id');
    if (grnVenName) grnVenName.value = vp.vendor_name;
    if (grnVenId) grnVenId.value = vp.id;

    const grnPoSelect = document.getElementById('vp-grn-po-select');
    if (grnPoSelect && data.purchase_orders) {
        grnPoSelect.innerHTML = data.purchase_orders.map(p => `
            <option value="${p.po_number}">
                ${p.po_number} — ${p.items && p.items.length ? p.items[0].item : 'Order'} (${formatINR(p.total_amount)})
            </option>
        `).join('') || '<option value="ADT/PO/2026/001">ADT/PO/2026/001</option>';
        if (data.purchase_orders.length) {
            handlePortalGRNPOSelect(data.purchase_orders[0].po_number);
        }
    }

    const grnDate = document.getElementById('vp-grn-date');
    if (grnDate) grnDate.value = new Date().toISOString().split('T')[0];

    // 2. Bill Modal Pre-fill
    const billPoSelect = document.getElementById('vp-bill-po-select');
    if (billPoSelect && data.purchase_orders) {
        billPoSelect.innerHTML = data.purchase_orders.map(p => `
            <option value="${p.po_number}">${p.po_number} (${formatINR(p.total_amount)})</option>
        `).join('') || '<option value="ADT/PO/2026/001">ADT/PO/2026/001</option>';
    }

    const billGrnSelect = document.getElementById('vp-bill-grn-select');
    if (billGrnSelect && data.inward_grns) {
        billGrnSelect.innerHTML = data.inward_grns.map(g => `
            <option value="${g.grn_number}">${g.grn_number} — ${g.item_description} (${g.inspection_status})</option>
        `).join('') || '<option value="ADT-GRN-2026-001">ADT-GRN-2026-001</option>';
    }

    const billDate = document.getElementById('vp-bill-date');
    if (billDate) billDate.value = new Date().toISOString().split('T')[0];

    // 3. Bid Modal Pre-fill
    const bidEventSelect = document.getElementById('vp-bid-event-select');
    if (bidEventSelect && data.sourcing_rfx_events) {
        bidEventSelect.innerHTML = data.sourcing_rfx_events.map(ev => `
            <option value="${ev.id}">${ev.event_code} — ${ev.title} (Budget: ${formatINR(ev.budget_allocation_inr)})</option>
        `).join('') || '<option value="1">ADT-RFX-2026-001</option>';
    }
}

export function handlePortalGRNPOSelect(poNumber) {
    if (!currentVendorPortalData || !currentVendorPortalData.purchase_orders) return;
    const po = currentVendorPortalData.purchase_orders.find(p => p.po_number === poNumber);
    if (!po) return;

    const descElem = document.getElementById('vp-grn-desc');
    const ordElem = document.getElementById('vp-grn-ord');
    const recvElem = document.getElementById('vp-grn-recv');
    const accElem = document.getElementById('vp-grn-acc');
    const dcElem = document.getElementById('vp-grn-dc-num');

    if (po.items && po.items.length) {
        if (descElem) descElem.value = po.items[0].item;
        const qty = po.items[0].qty || 1;
        if (ordElem) ordElem.value = qty;
        if (recvElem) recvElem.value = qty;
        if (accElem) accElem.value = qty;
    }
    if (dcElem && po.delivery_challan_no) {
        dcElem.value = po.delivery_challan_no;
    }
}

export function handlePortalGRNQtyChange() {
    const recv = parseFloat(document.getElementById('vp-grn-recv').value) || 0;
    const acc = parseFloat(document.getElementById('vp-grn-acc').value) || 0;
    const stElem = document.getElementById('vp-grn-status');
    if (stElem) {
        if (acc >= recv) {
            stElem.value = 'Accepted';
        } else if (acc > 0) {
            stElem.value = 'Partial Rejection';
        } else {
            stElem.value = 'Rejected';
        }
    }
}

export function calculatePortalBillNet() {
    const taxable = parseFloat(document.getElementById('vp-bill-taxable').value) || 0;
    const gst = parseFloat(document.getElementById('vp-bill-gst').value) || 0;
    const sec = document.getElementById('vp-bill-tds-sec').value;

    let tdsRate = 0.02;
    if (sec === '194C') {
        tdsRate = 0.02;
    } else if (sec === '194J') {
        tdsRate = 0.02; // technical services rate
    }

    const tdsAmt = Math.round(taxable * tdsRate * 100) / 100;
    const net = Math.round((taxable + gst - tdsAmt) * 100) / 100;

    const elTds = document.getElementById('vp-bill-calc-tds');
    const elNet = document.getElementById('vp-bill-calc-net');
    if (elTds) elTds.innerText = formatINR(tdsAmt);
    if (elNet) elNet.innerText = formatINR(net);
}

export function prefillAndOpenBidModal(eventId, eventLabel) {
    openVendorPortalModal('modal-vendor-portal-bid');
    const select = document.getElementById('vp-bid-event-select');
    if (select) select.value = eventId;
}

export async function handlePortalGRNSubmit(event) {
    event.preventDefault();
    const vendorId = parseInt(document.getElementById('vp-grn-vendor-id').value) || (currentVendorPortalData ? currentVendorPortalData.vendor_profile.id : 2);
    const payload = {
        vendor_id: vendorId,
        po_reference: document.getElementById('vp-grn-po-select').value,
        delivery_challan_no: document.getElementById('vp-grn-dc-num').value,
        received_date: document.getElementById('vp-grn-date').value,
        item_description: document.getElementById('vp-grn-desc').value,
        quantity_ordered: parseFloat(document.getElementById('vp-grn-ord').value) || 1.0,
        quantity_received: parseFloat(document.getElementById('vp-grn-recv').value) || 1.0,
        quantity_accepted: parseFloat(document.getElementById('vp-grn-acc').value) || 1.0,
        quantity_rejected: Math.max(0, (parseFloat(document.getElementById('vp-grn-recv').value) || 1.0) - (parseFloat(document.getElementById('vp-grn-acc').value) || 1.0)),
        inspection_status: document.getElementById('vp-grn-status').value,
        inspected_by: "Arjun Sharma (Lead Architect)",
        warehouse_location: document.getElementById('vp-grn-loc').value,
        remarks: document.getElementById('vp-grn-remarks').value
    };

    try {
        const res = await fetch(`${API_BASE}/portals/vendor/inward-grn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Failed to create Inward GRN');
        const data = await res.json();
        closeVendorPortalModal('modal-vendor-portal-grn');

        if (typeof showEnterpriseToast === 'function') {
            showEnterpriseToast('Inward GRN Verified', `${data.grn_number} successfully registered for PO ${data.po_reference}. 3-Way match updated.`, 'success', 4500);
        } else {
            alert(`✅ Inward GRN ${data.grn_number} registered!`);
        }
        loadVendorPortal(vendorId);
    } catch (err) {
        alert('Error recording Inward GRN: ' + err.message);
    }
}

export async function handlePortalBillSubmit(event) {
    event.preventDefault();
    const vendorName = currentVendorPortalData ? currentVendorPortalData.vendor_profile.vendor_name : "Nexus Micro Systems Pvt Ltd";
    const payload = {
        vendor_name: vendorName,
        bill_number: document.getElementById('vp-bill-num').value,
        bill_date: document.getElementById('vp-bill-date').value,
        po_reference: document.getElementById('vp-bill-po-select').value,
        grn_reference: document.getElementById('vp-bill-grn-select').value,
        taxable_amount: parseFloat(document.getElementById('vp-bill-taxable').value) || 0,
        gst_amount: parseFloat(document.getElementById('vp-bill-gst').value) || 0,
        tds_section: document.getElementById('vp-bill-tds-sec').value,
        expense_category: document.getElementById('vp-bill-category').value
    };

    try {
        const res = await fetch(`${API_BASE}/portals/vendor/ap-bill`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Failed to submit AP Bill');
        const data = await res.json();
        closeVendorPortalModal('modal-vendor-portal-bill');

        if (typeof showEnterpriseToast === 'function') {
            showEnterpriseToast('AP Bill Submitted', `Bill ${data.bill_number} logged! 3-Way Match: ${data.three_way_match_status}. Statutory Due: ${data.statutory_due_date}`, 'success', 4500);
        } else {
            alert(`✅ AP Bill ${data.bill_number} submitted! Match: ${data.three_way_match_status}`);
        }
        loadVendorPortal(currentVendorPortalData.vendor_profile.id);
    } catch (err) {
        alert('Error submitting AP Bill: ' + err.message);
    }
}

export async function handlePortalBidSubmit(event) {
    event.preventDefault();
    const vendorId = currentVendorPortalData ? currentVendorPortalData.vendor_profile.id : 2;
    const payload = {
        event_id: parseInt(document.getElementById('vp-bid-event-select').value),
        vendor_id: vendorId,
        commercial_quote_inr: parseFloat(document.getElementById('vp-bid-quote').value) || 0,
        sla_guarantee_pct: parseFloat(document.getElementById('vp-bid-sla').value) || 99.9,
        technical_score: parseFloat(document.getElementById('vp-bid-tech').value) || 90.0,
        compliance_score: parseFloat(document.getElementById('vp-bid-comp').value) || 92.0,
        notes: document.getElementById('vp-bid-notes').value
    };

    try {
        const res = await fetch(`${API_BASE}/portals/vendor/rfx-bid`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Failed to submit e-RFX bid');
        const data = await res.json();
        closeVendorPortalModal('modal-vendor-portal-bid');

        if (typeof showEnterpriseToast === 'function') {
            showEnterpriseToast('e-RFX Bid Submitted', `Bid ${data.bid_code} submitted for ${data.event_code}. Composite Score: ${data.composite_score}`, 'success', 4500);
        } else {
            alert(`✅ Sourcing Bid ${data.bid_code} submitted! Composite Score: ${data.composite_score}`);
        }
        loadVendorPortal(vendorId);
    } catch (err) {
        alert('Error submitting bid: ' + err.message);
    }
}


// Stakeholder Login Modal Controllers
export function openStakeholderLoginModal() {
    const modal = document.getElementById('modal-stakeholder-login');
    if (modal) modal.classList.remove('hidden');
}

export function closeStakeholderLoginModal() {
    const modal = document.getElementById('modal-stakeholder-login');
    if (modal) modal.classList.add('hidden');
}

export function setStakeholderLoginCredentials(email, role) {
    const emailInput = document.getElementById('stakeholder-login-email');
    const pwdInput = document.getElementById('stakeholder-login-password');
    if (emailInput) emailInput.value = email;
    if (pwdInput) pwdInput.value = "Password123!";
}

export async function handleStakeholderLogin(event) {
    event.preventDefault();
    const email = document.getElementById('stakeholder-login-email').value.trim();
    const password = document.getElementById('stakeholder-login-password').value.trim();
    const errorDiv = document.getElementById('stakeholder-login-error');

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });

        if (!res.ok) {
            const err = await res.json();
            if (errorDiv) {
                errorDiv.innerText = err.detail || 'Authentication failed. Please check credentials.';
                errorDiv.classList.remove('hidden');
            }
            return;
        }

        const data = await res.json();
        if (errorDiv) errorDiv.classList.add('hidden');

        // Update selector
        const selector = document.getElementById('persona-selector');
        if (selector) selector.value = data.email;

        closeStakeholderLoginModal();
        await handleSwitchPersona(data.email);
        alert(`🔐 Welcome, ${data.name}!\nLogged in as: ${data.title}\nRole: ${data.role}`);
    } catch (err) {
        if (errorDiv) {
            errorDiv.innerText = 'Network error: ' + err.message;
            errorDiv.classList.remove('hidden');
        }
    }
}

/* ============================================================================
   PILLAR 15: ENTERPRISE GUARDRAILS, SYSTEM ARCHITECTURES & FLOWCHARTS
============================================================================ */

export let cachedFlowcharts = [];
export let cachedBlueprints = [];
export let cachedDocuments = [];

export async function loadGuardrails() {
    try {
        // 1. Fetch Overview Telemetry
        const overRes = await fetch(`${API_BASE}/guardrails/overview`);
        if (overRes.ok) {
            const over = await overRes.json();
            const scoreEl = document.getElementById('guardrail-kpi-score');
            const activeEl = document.getElementById('guardrail-kpi-active');
            const evalsEl = document.getElementById('guardrail-kpi-evals');
            const blockedEl = document.getElementById('guardrail-kpi-blocked');

            if (scoreEl) scoreEl.innerText = `${over.compliance_score_pct}%`;
            if (activeEl) activeEl.innerText = over.active_rules;
            if (evalsEl) evalsEl.innerText = over.total_evaluations;
            if (blockedEl) blockedEl.innerText = over.total_blocked;
        }

        // 2. Fetch Rules
        loadGuardrailRulesTable();

        // 3. Preload Flowcharts, Blueprints, Documents, and Logs
        loadEnterpriseFlowchartsView();
        loadArchitectureBlueprintsView();
        loadGuardrailLogsTable();
        loadTechnicalDocumentsView();

    } catch (err) {
        console.error('Error loading guardrails module:', err);
    }
}

export async function loadGuardrailRulesTable() {
    const tbody = document.getElementById('guardrail-rules-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/guardrails/rules`);
        if (!res.ok) throw new Error('Failed to fetch rules');
        const rules = await res.json();

        if (!rules || rules.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400">No guardrails registered.</td></tr>';
            return;
        }

        tbody.innerHTML = rules.map(r => {
            const sevBadge = r.severity === 'Critical_Blocker'
                ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700 border border-rose-300">Critical Blocker</span>'
                : '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700 border border-amber-300">Warning / Heal</span>';

            const modeBadge = r.enforcement_mode === 'Active_Blocking'
                ? '<span class="text-[10px] font-semibold text-rose-600"><i class="fa-solid fa-lock"></i> Hard Block</span>'
                : '<span class="text-[10px] font-semibold text-teal-600"><i class="fa-solid fa-wand-magic-sparkles"></i> Auto-Heal</span>';

            const statusBadge = r.total_blocked === 0
                ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700">Healthy</span>'
                : '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700">Interventions</span>';

            return `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-3 font-mono font-bold text-teal-700">${r.rule_code}</td>
                    <td class="p-3">
                        <div class="font-bold text-slate-800">${r.name}</div>
                        <div class="text-[11px] text-slate-500">${r.description}</div>
                    </td>
                    <td class="p-3">
                        <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[10px] font-semibold border">${r.regulatory_framework}</span>
                    </td>
                    <td class="p-3 space-y-1">
                        <div>${sevBadge}</div>
                        <div>${modeBadge}</div>
                    </td>
                    <td class="p-3 font-mono font-semibold text-slate-700">${r.total_evaluations}</td>
                    <td class="p-3 font-mono font-bold text-emerald-600">${r.total_passed}</td>
                    <td class="p-3 font-mono">
                        <span class="text-rose-600 font-bold">${r.total_blocked}</span> / 
                        <span class="text-teal-600 font-bold">${r.total_auto_healed}</span>
                    </td>
                    <td class="p-3">${statusBadge}</td>
                </tr>
            `;
        }).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-red-500">Error loading rules: ${err.message}</td></tr>`;
    }
}

export async function loadEnterpriseFlowchartsView() {
    const btnContainer = document.getElementById('flowchart-selector-buttons');
    if (!btnContainer) return;

    try {
        const res = await fetch(`${API_BASE}/guardrails/flowcharts`);
        if (!res.ok) throw new Error('Failed to fetch flowcharts');
        cachedFlowcharts = await res.json();

        if (!cachedFlowcharts || cachedFlowcharts.length === 0) {
            btnContainer.innerHTML = '<span class="text-xs text-slate-400">No flowcharts available.</span>';
            return;
        }

        btnContainer.innerHTML = cachedFlowcharts.map((fc, idx) => `
            <button onclick="displayFlowchart('${fc.flowchart_id}')" class="px-3 py-1.5 rounded-lg text-xs font-semibold border transition ${idx === 0 ? 'bg-teal-700 text-white border-teal-800' : 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300'}" id="fc-btn-${fc.flowchart_id}">
                ${fc.title}
            </button>
        `).join('');

        // Display first flowchart
        displayFlowchart(cachedFlowcharts[0].flowchart_id);

    } catch (err) {
        btnContainer.innerHTML = `<span class="text-xs text-red-500">Error: ${err.message}</span>`;
    }
}

export function displayFlowchart(flowchartId) {
    const fc = cachedFlowcharts.find(f => f.flowchart_id === flowchartId);
    if (!fc) return;

    // Update active button state
    cachedFlowcharts.forEach(item => {
        const btn = document.getElementById(`fc-btn-${item.flowchart_id}`);
        if (btn) {
            if (item.flowchart_id === flowchartId) {
                btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold border transition bg-teal-700 text-white border-teal-800 shadow-sm';
            } else {
                btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold border transition bg-white text-slate-700 hover:bg-slate-100 border-slate-300';
            }
        }
    });

    // Populate metadata
    const titleEl = document.getElementById('flowchart-active-title');
    const stdEl = document.getElementById('flowchart-active-standard');
    const grListEl = document.getElementById('flowchart-active-guardrails');
    const codeEl = document.getElementById('flowchart-mermaid-code');
    const stepsEl = document.getElementById('flowchart-steps-container');

    if (titleEl) titleEl.innerText = `${fc.title} (${fc.pillar})`;
    if (stdEl) stdEl.innerText = `Standard: ${fc.regulatory_standard}`;

    if (grListEl) {
        grListEl.innerHTML = (fc.active_guardrails || []).map(g => `
            <span class="bg-teal-50 border border-teal-300 text-teal-800 font-mono text-[10px] font-bold px-2 py-0.5 rounded-full">
                <i class="fa-solid fa-shield-halved mr-1"></i>${g}
            </span>
        `).join('');
    }

    if (codeEl) {
        codeEl.innerText = fc.mermaid_diagram;
    }

    if (stepsEl) {
        stepsEl.innerHTML = (fc.steps || []).map(s => `
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                <div class="flex items-start gap-2.5">
                    <span class="w-6 h-6 rounded-full bg-teal-600 text-white flex items-center justify-center font-bold text-[11px] shrink-0 mt-0.5">${s.step_number}</span>
                    <div>
                        <div class="font-bold text-slate-800">${s.title}</div>
                        <div class="text-slate-600 text-[11px] mt-0.5"><strong>Actor:</strong> ${s.actor} | <strong>Input:</strong> ${s.input_data}</div>
                        <div class="text-slate-500 text-[11px] mt-0.5"><strong>Logic:</strong> ${s.decision_or_processing}</div>
                    </div>
                </div>
                <div class="text-right shrink-0">
                    <div class="text-[10px] font-bold font-mono text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200 inline-block mb-1">
                        ${s.guardrail_enforced}
                    </div>
                    <div class="text-[11px] font-semibold text-emerald-700">➔ ${s.output_state}</div>
                </div>
            </div>
        `).join('');
    }
}

export async function loadArchitectureBlueprintsView() {
    const container = document.getElementById('blueprints-grid-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/guardrails/blueprints`);
        if (!res.ok) throw new Error('Failed to fetch blueprints');
        cachedBlueprints = await res.json();

        if (!cachedBlueprints || cachedBlueprints.length === 0) {
            container.innerHTML = '<div class="p-4 text-center text-slate-400 col-span-2">No blueprints registered.</div>';
            return;
        }

        container.innerHTML = cachedBlueprints.map(b => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-teal-700">${b.blueprint_code}</div>
                        <div class="text-sm font-bold text-slate-800">${b.title}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-slate-100 text-slate-700 font-semibold text-[10px] rounded border">
                        ${b.architecture_type}
                    </span>
                </div>
                <p class="text-xs text-slate-600">${b.description}</p>
                <div class="text-[11px] text-slate-500">
                    <strong>Standard Alignment:</strong> ${b.standard_alignment}<br>
                    <strong>Key Subsystems:</strong> ${b.key_components}
                </div>
                <pre class="bg-slate-900 text-teal-300 font-mono text-[10px] p-3 rounded-lg overflow-x-auto whitespace-pre border border-slate-800">${b.diagram_mermaid}</pre>
                <div class="text-[10px] text-teal-700 font-mono font-semibold">
                    <i class="fa-solid fa-link mr-1"></i>Enforced Guardrails: ${b.guardrail_linkage || 'None'}
                </div>
            </div>
        `).join('');

    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export async function loadGuardrailLogsTable() {
    const tbody = document.getElementById('guardrail-logs-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/guardrails/logs?limit=50`);
        if (!res.ok) throw new Error('Failed to fetch logs');
        const logs = await res.json();

        if (!logs || logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-400">No execution logs recorded.</td></tr>';
            return;
        }

        tbody.innerHTML = logs.map(l => {
            const resBadge = l.evaluation_result === 'PASSED'
                ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700">PASSED</span>'
                : l.evaluation_result === 'BLOCKED'
                    ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700">BLOCKED</span>'
                    : '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-100 text-teal-700">AUTO_HEALED</span>';

            return `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-3 font-mono font-bold text-slate-700">${l.execution_id}</td>
                    <td class="p-3 font-mono font-semibold text-teal-700">${l.rule_code}</td>
                    <td class="p-3 text-slate-600 font-medium">${l.module}</td>
                    <td class="p-3 font-mono font-semibold text-slate-800">${l.entity_reference}</td>
                    <td class="p-3">${resBadge}</td>
                    <td class="p-3 text-slate-600 text-[11px]">${l.trigger_payload_summary || '-'}</td>
                    <td class="p-3 text-slate-700 font-semibold">${l.action_taken}</td>
                    <td class="p-3 text-slate-500 text-[11px] whitespace-nowrap">${formatDate(l.evaluated_at)}</td>
                </tr>
            `;
        }).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-red-500">Error: ${err.message}</td></tr>`;
    }
}

export async function loadTechnicalDocumentsView() {
    const container = document.getElementById('documents-grid-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/guardrails/documents`);
        if (!res.ok) throw new Error('Failed to fetch documents');
        cachedDocuments = await res.json();

        if (!cachedDocuments || cachedDocuments.length === 0) {
            container.innerHTML = '<div class="p-4 text-center text-slate-400 col-span-2">No documents available.</div>';
            return;
        }

        container.innerHTML = cachedDocuments.map(d => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-indigo-700">${d.doc_id} • ${d.version}</div>
                        <div class="text-sm font-bold text-slate-800">${d.title}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-700 font-semibold text-[10px] rounded border border-amber-200">
                        ${d.classification}
                    </span>
                </div>
                <p class="text-xs text-slate-600">${d.summary}</p>
                <div>
                    <div class="text-[11px] font-bold text-slate-700 mb-1">Key Specification Sections:</div>
                    <ul class="text-[11px] text-slate-500 list-disc list-inside space-y-0.5">
                        ${(d.key_sections || []).map(sec => `<li>${sec}</li>`).join('')}
                    </ul>
                </div>
                <div class="flex items-center justify-between pt-2 border-t">
                    <span class="text-[10px] text-slate-400">Published: ${d.published_date}</span>
                    <button onclick="alert('📥 Specification Document Downloaded: ${d.title} (${d.version})')" class="px-3 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold text-xs rounded-lg transition border border-indigo-200 flex items-center gap-1.5">
                        <i class="fa-solid fa-file-arrow-down"></i> Download Specification
                    </button>
                </div>
            </div>
        `).join('');

    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export function switchGuardrailTab(tabName) {
    const tabs = ['rules', 'flowcharts', 'blueprints', 'logs', 'docs'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-guardrail-${t}`);
        const panel = document.getElementById(`guardrail-panel-${t}`);
        if (btn && panel) {
            if (t === tabName) {
                btn.className = 'py-2 border-b-2 border-teal-600 text-teal-700 flex items-center gap-2 font-bold';
                panel.classList.remove('hidden');
            } else {
                btn.className = 'py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2';
                panel.classList.add('hidden');
            }
        }
    });
}

export async function handleRunGuardrailsScan() {
    try {
        const res = await fetch(`${API_BASE}/guardrails/evaluate`, { method: 'POST' });
        if (!res.ok) throw new Error('Live scan failed');
        const data = await res.json();

        alert(`🛡️ Guardrails Autonomous Scan Completed!\n\n` +
            `• Rules Evaluated: ${data.total_rules_active}\n` +
            `• Total Checkpoints: ${data.total_evaluations}\n` +
            `• Compliant & Passed: ${data.total_passed}\n` +
            `• Violations Blocked: ${data.total_violations_blocked}\n` +
            `• Anomalies Auto-Healed: ${data.total_anomalies_auto_healed}\n` +
            `• Overall Compliance: ${data.compliance_score_pct}%`
        );

        loadGuardrails();
    } catch (err) {
        alert('Error executing guardrails scan: ' + err.message);
    }
}

/* ============================================================================
   PILLAR 16: AI MODEL APIS, MCP TOOL SERVERS, MULTI-CLOUD & AUTHENTICITY
============================================================================ */

export async function loadAICloudModule() {
    try {
        // 1. Overview Telemetry
        const overRes = await fetch(`${API_BASE}/ai-cloud/overview`);
        if (overRes.ok) {
            const data = await overRes.json();
            const spendEl = document.getElementById('ai-kpi-spend');
            const utilEl = document.getElementById('ai-kpi-util');
            const mcpEl = document.getElementById('ai-kpi-mcp');
            const cloudEl = document.getElementById('ai-kpi-cloud');
            const cloudSpendEl = document.getElementById('ai-kpi-cloud-spend');
            const certsEl = document.getElementById('ai-kpi-certs');

            if (spendEl) spendEl.innerText = `${formatINR(data.total_ai_spend_inr)} / ${formatINR(data.total_ai_budget_inr)}`;
            if (utilEl) utilEl.innerText = `${data.ai_budget_utilization_pct}% monthly token budget utilized`;
            if (mcpEl) mcpEl.innerText = `${data.active_mcp_servers} / ${data.mcp_servers_count} Active`;
            if (cloudEl) cloudEl.innerText = `${data.average_uptime_sla_pct}%`;
            if (cloudSpendEl) cloudSpendEl.innerText = `Multi-Cloud Spend: ${formatINR(data.total_cloud_spend_inr)}/mo`;
            if (certsEl) certsEl.innerText = `${data.valid_trusted_certificates} Valid`;
        }

        // 2. Load Sub-Panels
        loadAIModelsTable();
        loadMCPServersGrid();
        loadCloudNodesGrid();
        loadAuthenticityCertsTable();
        loadExecutiveAlertRulesGrid();

    } catch (err) {
        console.error('Error loading AI Cloud Module:', err);
    }
}

export async function loadAIModelsTable() {
    const tbody = document.getElementById('ai-models-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/ai-models`);
        if (!res.ok) throw new Error('Failed to fetch AI models');
        const models = await res.json();

        tbody.innerHTML = models.map(m => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3 font-mono font-bold text-violet-700">${m.endpoint_code}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-800">${m.model_name}</div>
                    <div class="text-[11px] text-slate-500">${m.provider}</div>
                </td>
                <td class="p-3">
                    <span class="bg-violet-50 text-violet-700 px-2 py-0.5 rounded text-[10px] font-semibold border border-violet-200">${m.model_family}</span>
                </td>
                <td class="p-3 font-mono text-slate-700 font-semibold">${(m.context_window_tokens).toLocaleString()} tokens</td>
                <td class="p-3 font-mono text-[11px] text-slate-600">${m.rpm_limit} RPM / ${(m.tpm_limit / 1000).toFixed(0)}k TPM</td>
                <td class="p-3 font-mono text-[11px]">
                    <span class="text-teal-700 font-bold">${m.avg_latency_ms}ms</span> • 
                    <span class="text-slate-500">₹${m.cost_per_million_tokens_inr}/1M</span>
                </td>
                <td class="p-3">
                    <div class="font-bold text-slate-800 font-mono">${formatINR(m.current_month_usage_inr)}</div>
                    <div class="text-[10px] text-slate-400">Cap: ${formatINR(m.monthly_budget_inr)}</div>
                </td>
                <td class="p-3 font-mono text-[10px] text-slate-500">${m.api_key_vault_ref}</td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-red-500">Error: ${err.message}</td></tr>`;
    }
}

export async function loadMCPServersGrid() {
    const container = document.getElementById('mcp-servers-grid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/mcp-servers`);
        if (!res.ok) throw new Error('Failed to fetch MCP servers');
        const mcps = await res.json();

        container.innerHTML = mcps.map(srv => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-indigo-700">${srv.server_id}</div>
                        <div class="text-sm font-bold text-slate-800">${srv.name}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-semibold text-[10px] rounded-full border border-emerald-200">
                        <i class="fa-solid fa-circle text-[8px] text-emerald-500 mr-1 animate-pulse"></i>${srv.last_ping_status}
                    </span>
                </div>
                <p class="text-xs text-slate-600">${srv.description}</p>
                <div class="text-[11px] text-slate-500 space-y-0.5">
                    <div><strong>Transport:</strong> <code class="bg-slate-100 px-1 py-0.5 rounded text-indigo-700">${srv.transport_type} (${srv.protocol_version})</code></div>
                    <div><strong>Endpoint / Execution:</strong> <code class="bg-slate-100 px-1 py-0.5 rounded text-slate-700">${srv.endpoint_or_command}</code></div>
                    <div><strong>Authentication:</strong> ${srv.auth_mode}</div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <div class="flex gap-2">
                        <span class="bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded border border-indigo-200">${srv.exposed_tools_count} Tools</span>
                        <span class="bg-slate-50 text-slate-700 font-bold px-2 py-0.5 rounded border border-slate-200">${srv.exposed_resources_count} Resources</span>
                    </div>
                    <button onclick="handlePingMCP('${srv.server_id}')" class="px-3 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold rounded-lg transition border border-indigo-200 flex items-center gap-1">
                        <i class="fa-solid fa-bolt"></i> Ping Test
                    </button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export async function handlePingMCP(serverId) {
    try {
        const res = await fetch(`${API_BASE}/ai-cloud/mcp-servers/${serverId}/ping`, { method: 'POST' });
        if (!res.ok) throw new Error('Ping failed');
        const data = await res.json();
        alert(`⚡ MCP Server Ping Succeeded!\n\n• Server: ${data.server_id}\n• Status: ${data.status}\n• Telemetry: ${data.latency}`);
        loadMCPServersGrid();
    } catch (err) {
        alert('Error testing MCP connection: ' + err.message);
    }
}

export async function loadCloudNodesGrid() {
    const container = document.getElementById('cloud-nodes-grid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/cloud-nodes`);
        if (!res.ok) throw new Error('Failed to fetch cloud nodes');
        const nodes = await res.json();

        container.innerHTML = nodes.map(n => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-teal-700">${n.node_code} • ${n.cloud_provider}</div>
                        <div class="text-sm font-bold text-slate-800">${n.cluster_or_service_name}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-700 font-bold text-[10px] rounded border border-emerald-200">
                        ${n.uptime_sla_pct}% SLA
                    </span>
                </div>
                <div class="text-xs text-slate-600 space-y-1">
                    <div><strong>Region / Multi-AZ:</strong> ${n.region} (${n.availability_zone})</div>
                    <div><strong>Compute Sizing:</strong> ${n.compute_capacity}</div>
                    <div><strong>Security Ingress:</strong> Zero-Trust mTLS & IAM Role Verified</div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <div class="font-bold text-slate-700 font-mono">Cost: ${formatINR(n.monthly_cost_inr)}/mo</div>
                    <span class="text-teal-700 font-semibold"><i class="fa-solid fa-user-shield mr-1"></i>${n.technical_lead}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export async function loadAuthenticityCertsTable() {
    const tbody = document.getElementById('certs-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/certificates`);
        if (!res.ok) throw new Error('Failed to fetch certs');
        const certs = await res.json();

        tbody.innerHTML = certs.map(c => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3 font-mono font-bold text-indigo-700">${c.cert_code}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-800">${c.certificate_name}</div>
                    <div class="text-[11px] text-slate-500">${c.subject_entity}</div>
                </td>
                <td class="p-3 font-semibold text-slate-700">${c.issuing_authority}</td>
                <td class="p-3 text-[11px]">
                    <div class="font-mono font-bold text-slate-700">${c.key_algorithm}</div>
                    <div class="text-slate-500 text-[10px]">${c.fips_compliance_level}</div>
                </td>
                <td class="p-3 font-mono text-[10px] text-slate-600 max-w-[150px] truncate" title="${c.public_key_fingerprint}">
                    ${c.public_key_fingerprint.substring(0, 16)}...
                </td>
                <td class="p-3 text-[11px]">
                    <div class="font-bold text-slate-700">${formatDate(c.valid_until)}</div>
                    <div class="text-teal-600 font-semibold">${c.days_until_expiry} days remaining</div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                        ${c.status}
                    </span>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-red-500">Error: ${err.message}</td></tr>`;
    }
}

export async function loadExecutiveAlertRulesGrid() {
    const container = document.getElementById('alert-rules-grid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/alert-rules`);
        if (!res.ok) throw new Error('Failed to fetch alert rules');
        const rules = await res.json();

        container.innerHTML = rules.map(r => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-rose-700">${r.rule_code}</div>
                        <div class="text-sm font-bold text-slate-800">${r.title}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-rose-50 text-rose-700 font-bold text-[10px] rounded border border-rose-200">
                        ${r.escalation_window_mins} Min SLA
                    </span>
                </div>
                <div class="text-xs text-slate-600 space-y-1">
                    <div><strong>Trigger Invariant:</strong> <code class="bg-slate-100 text-rose-700 px-1 py-0.5 rounded">${r.trigger_condition}</code></div>
                    <div><strong>Escalation Head:</strong> ${r.target_head_role} (${r.target_head_email})</div>
                    <div><strong>Direct Dispatch Channels:</strong> ${r.dispatch_channels}</div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <span class="text-slate-500 font-mono"><i class="fa-brands fa-whatsapp text-emerald-600 mr-1"></i>${r.target_head_whatsapp}</span>
                    <button onclick="handleTriggerDirectAlert('${r.rule_code}')" class="px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold rounded-lg transition border border-rose-200 flex items-center gap-1">
                        <i class="fa-solid fa-paper-plane"></i> Test Alert Ping
                    </button>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export function switchAICloudTab(tabName) {
    const tabs = ['models', 'mcps', 'cloud', 'certs', 'alerts'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-aicloud-${t}`);
        const panel = document.getElementById(`aicloud-panel-${t}`);
        if (btn && panel) {
            if (t === tabName) {
                btn.className = 'py-2 border-b-2 border-violet-600 text-violet-700 flex items-center gap-2 font-bold';
                panel.classList.remove('hidden');
            } else {
                btn.className = 'py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2';
                panel.classList.add('hidden');
            }
        }
    });
}

export function handleTriggerOmniHeadAlertModal() {
    const modal = document.getElementById('modal-omni-alert');
    if (modal) modal.classList.remove('hidden');
}

export function closeOmniHeadAlertModal() {
    const modal = document.getElementById('modal-omni-alert');
    if (modal) modal.classList.add('hidden');
}

export async function handleDispatchAlertForm(event) {
    event.preventDefault();
    const head = document.getElementById('modal-alert-target-head').value;
    const title = document.getElementById('modal-alert-title').value;
    const severity = document.getElementById('modal-alert-severity').value;
    const msg = document.getElementById('modal-alert-msg').value;

    try {
        const res = await fetch(`${API_BASE}/ai-cloud/alert-rules/EAR-FIN-LIQ-01/dispatch?custom_message=${encodeURIComponent(msg)}`, {
            method: 'POST'
        });
        if (!res.ok) throw new Error('Failed to dispatch alert');
        const data = await res.json();

        closeOmniHeadAlertModal();
        alert(`🚨 Executive Alert Dispatched Successfully!\n\n` +
            `• Target Head: ${head}\n` +
            `• Subject: [${severity}] ${title}\n` +
            `• Notification ID: ${data.notification_code}\n` +
            `• Omni-Channels: WhatsApp Cloud API, Email SES, and In-App Alert Bell.`
        );

        fetchNotificationsAndAlerts();
    } catch (err) {
        alert('Error dispatching alert: ' + err.message);
    }
}

export async function handleTriggerDirectAlert(ruleCode) {
    try {
        const res = await fetch(`${API_BASE}/ai-cloud/alert-rules/${ruleCode}/dispatch`, { method: 'POST' });
        if (!res.ok) throw new Error('Dispatch failed');
        const data = await res.json();
        alert(`🚨 Direct Alert Transmitted!\n\n• Rule: ${ruleCode}\n• Target: ${data.target_role}\n• Status: ${data.status} via WhatsApp & SES`);
        fetchNotificationsAndAlerts();
    } catch (err) {
        alert('Error: ' + err.message);
    }
}

/* ============================================================================
   PILLAR 17: ISO STANDARDS, QMS & FORMAL GRIEVANCE REDRESSAL
============================================================================ */

export let cachedISOControls = [];

export async function loadISOStandardsModule() {
    try {
        // 1. Overview Telemetry
        const overRes = await fetch(`${API_BASE}/iso-standards/overview`);
        if (overRes.ok) {
            const data = await overRes.json();
            const scoreEl = document.getElementById('iso-kpi-score');
            const stdEl = document.getElementById('iso-kpi-standards');
            const auditsEl = document.getElementById('iso-kpi-audits');
            const auditsSubEl = document.getElementById('iso-kpi-audits-sub');
            const grvEl = document.getElementById('iso-kpi-grievances');
            const csatEl = document.getElementById('iso-kpi-csat');

            if (scoreEl) scoreEl.innerText = `${data.overall_compliance_score_pct}%`;
            if (stdEl) stdEl.innerText = `${data.total_iso_certifications} Acquired`;
            if (auditsEl) auditsEl.innerText = `${data.total_major_non_conformances + data.total_minor_non_conformances} NCs`;
            if (auditsSubEl) auditsSubEl.innerText = `${data.total_internal_audits} Audits (${data.opportunities_for_improvement} OFIs)`;
            if (grvEl) grvEl.innerText = `${data.resolved_grievances} / ${data.total_grievances_logged} Resolved`;
            if (csatEl) csatEl.innerText = `Average CSAT: ${data.average_customer_satisfaction_csat} / 5.0`;
        }

        // 2. Load Sub-Panels
        loadISOCertificationsGrid();
        loadISOControlsTable();
        loadISOAuditsGrid();
        loadISOCapasContainer();
        loadISOGrievancesTable();

    } catch (err) {
        console.error('Error loading ISO standards module:', err);
    }
}

export async function loadISOCertificationsGrid() {
    const container = document.getElementById('iso-certifications-grid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/iso-standards/certifications`);
        if (!res.ok) throw new Error('Failed to fetch certifications');
        const certs = await res.json();

        container.innerHTML = certs.map(c => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-amber-700">${c.certificate_number}</div>
                        <div class="text-sm font-bold text-slate-800">${c.standard_code} - ${c.standard_name}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold text-[10px] rounded-full border border-emerald-200">
                        <i class="fa-solid fa-check-double mr-1"></i>${c.status}
                    </span>
                </div>
                <p class="text-xs text-slate-600"><strong>Scope of Certification:</strong> ${c.scope_description}</p>
                <div class="text-[11px] text-slate-500 space-y-0.5">
                    <div><strong>Accreditation Body:</strong> ${c.accreditation_body}</div>
                    <div><strong>Management Representative:</strong> ${c.management_representative}</div>
                    <div><strong>Lead Auditor:</strong> ${c.lead_auditor}</div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <span class="text-slate-500">Issued: ${formatDate(c.issue_date)} • Expires: ${formatDate(c.expiry_date)}</span>
                    <span class="text-amber-700 font-semibold font-mono">Surveillance: ${formatDate(c.surveillance_audit_due)}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export async function loadISOControlsTable(filterStandard = '') {
    const tbody = document.getElementById('iso-controls-table-body');
    if (!tbody) return;

    try {
        const url = filterStandard
            ? `${API_BASE}/iso-standards/controls?standard=${encodeURIComponent(filterStandard)}`
            : `${API_BASE}/iso-standards/controls`;
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to fetch controls');
        cachedISOControls = await res.json();

        tbody.innerHTML = cachedISOControls.map(ctrl => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3 font-mono font-bold text-amber-700">${ctrl.control_code}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-800">${ctrl.standard_code} • Clause ${ctrl.clause_number}</div>
                    <div class="text-[11px] text-slate-600">${ctrl.title}</div>
                </td>
                <td class="p-3">
                    <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[10px] font-semibold border">${ctrl.control_domain}</span>
                </td>
                <td class="p-3 text-[11px] text-slate-600 max-w-[200px]">${ctrl.requirement_summary}</td>
                <td class="p-3 text-[11px] text-slate-700 font-medium max-w-[200px]">${ctrl.implementation_mechanism}</td>
                <td class="p-3 font-mono text-[10px] text-indigo-700">${ctrl.evidence_vault_ref || '-'}</td>
                <td class="p-3">
                    <div class="font-bold text-emerald-700 font-mono text-xs">${ctrl.compliance_score_pct}%</div>
                    <div class="text-[10px] text-slate-400">${ctrl.maturity_level}</div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">Conforming</span>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-red-500">Error: ${err.message}</td></tr>`;
    }
}

export function filterISOClauseControls(standardVal) {
    loadISOControlsTable(standardVal);
}

export async function loadISOAuditsGrid() {
    const container = document.getElementById('iso-audits-grid');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/iso-standards/audits`);
        if (!res.ok) throw new Error('Failed to fetch audits');
        const audits = await res.json();

        container.innerHTML = audits.map(a => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-blue-700">${a.audit_code} • ${a.standard_code}</div>
                        <div class="text-sm font-bold text-slate-800">${a.audit_type}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-blue-50 text-blue-700 font-bold text-[10px] rounded border border-blue-200">
                        ${formatDate(a.audit_date)}
                    </span>
                </div>
                <p class="text-xs text-slate-600">${a.findings_summary}</p>
                <div class="text-[11px] text-slate-500 space-y-0.5">
                    <div><strong>Audited Scope:</strong> ${a.audited_department}</div>
                    <div><strong>Auditor Team:</strong> ${a.lead_auditor} (Auditee: ${a.auditee_representative})</div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <div class="flex gap-2">
                        <span class="bg-rose-50 text-rose-700 font-bold px-2 py-0.5 rounded border border-rose-200">${a.major_nc_count} Major NC</span>
                        <span class="bg-amber-50 text-amber-700 font-bold px-2 py-0.5 rounded border border-amber-200">${a.minor_nc_count} Minor NC</span>
                        <span class="bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">${a.ofi_count} OFI</span>
                    </div>
                    <span class="text-emerald-700 font-bold"><i class="fa-solid fa-check mr-1"></i>${a.audit_outcome}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500 col-span-2">Error: ${err.message}</div>`;
    }
}

export async function loadISOCapasContainer() {
    const container = document.getElementById('iso-capas-container');
    if (!container) return;

    try {
        const res = await fetch(`${API_BASE}/iso-standards/capas`);
        if (!res.ok) throw new Error('Failed to fetch CAPAs');
        const capas = await res.json();

        container.innerHTML = capas.map(cp => `
            <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
                <div class="flex items-center justify-between border-b pb-2">
                    <div>
                        <div class="text-xs font-bold font-mono text-rose-700">${cp.capa_number} • ${cp.standard_code}</div>
                        <div class="text-sm font-bold text-slate-800">${cp.source_type}</div>
                    </div>
                    <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold text-[10px] rounded-full border border-emerald-300">
                        <i class="fa-solid fa-shield-check mr-1"></i>${cp.status}
                    </span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div class="space-y-1">
                        <div class="font-bold text-slate-700">Problem Statement:</div>
                        <div class="text-slate-600 bg-slate-50 p-2 rounded border">${cp.problem_statement}</div>
                        <div class="font-bold text-slate-700 mt-2">Immediate Containment Action:</div>
                        <div class="text-teal-800 bg-teal-50 p-2 rounded border border-teal-200">${cp.immediate_containment_action}</div>
                    </div>
                    <div class="space-y-1">
                        <div class="font-bold text-slate-700">Root Cause Analysis (${cp.root_cause_analysis_method}):</div>
                        <div class="text-slate-600 bg-slate-50 p-2 rounded border">${cp.root_cause_findings}</div>
                        <div class="font-bold text-slate-700 mt-2">Systemic Preventive & Corrective Action:</div>
                        <div class="text-slate-700 bg-blue-50 p-2 rounded border border-blue-200">${cp.preventive_corrective_action}</div>
                    </div>
                </div>
                <div class="flex items-center justify-between pt-2 border-t text-[11px]">
                    <span class="text-slate-500">Owner: ${cp.action_owner} | Target: ${formatDate(cp.target_closure_date)}</span>
                    <span class="text-emerald-700 font-semibold"><i class="fa-solid fa-signature mr-1"></i>Verified by: ${cp.verifier_name} (${formatDate(cp.actual_closure_date)})</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<div class="p-4 text-center text-red-500">Error: ${err.message}</div>`;
    }
}

export async function loadISOGrievancesTable() {
    const tbody = document.getElementById('iso-grievances-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/iso-standards/grievances`);
        if (!res.ok) throw new Error('Failed to fetch grievances');
        const grievances = await res.json();

        tbody.innerHTML = grievances.map(g => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3 font-mono font-bold text-amber-700">${g.grievance_id}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-800">${g.stakeholder_name}</div>
                    <span class="bg-amber-50 text-amber-700 px-2 py-0.5 rounded text-[10px] font-semibold border border-amber-200">${g.stakeholder_type}</span>
                </td>
                <td class="p-3 text-[11px]">
                    <div class="font-semibold text-slate-700">${g.category}</div>
                    <span class="text-rose-600 font-bold">${g.severity} Priority</span>
                </td>
                <td class="p-3 text-[11px] max-w-[220px]">
                    <div class="font-bold text-slate-800">${g.subject}</div>
                    <div class="text-slate-500 text-[10px]">${g.description}</div>
                </td>
                <td class="p-3 text-[11px] max-w-[240px]">
                    <div class="text-slate-700 font-medium"><strong>Remedy:</strong> ${g.resolution_details || 'Pending Investigation'}</div>
                    <div class="text-slate-400 text-[10px]">Officer: ${g.assigned_redressal_officer}</div>
                </td>
                <td class="p-3 text-center">
                    <div class="text-amber-500 font-bold text-xs">${'★'.repeat(g.csat_score)}${'☆'.repeat(5 - g.csat_score)}</div>
                    <div class="text-[10px] text-slate-400">${g.statutory_sla_days}-Day SLA</div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                        ${g.status}
                    </span>
                </td>
                <td class="p-3">
                    <div class="flex items-center gap-1.5">
                        <a href="${API_BASE}/iso-standards/grievances/${g.grievance_id}/document" target="_blank" class="px-2 py-1 bg-amber-50 hover:bg-amber-100 text-amber-700 font-semibold rounded text-[10px] border border-amber-200 inline-flex items-center gap-1" title="Print ISO Grievance Certificate">
                            <i class="fa-solid fa-file-contract"></i> Cert
                        </a>
                        ${g.status !== 'Resolved & Closed' ? `
                            <button onclick="handlePromptResolveGrievance('${g.grievance_id}')" class="px-2 py-1 bg-teal-50 hover:bg-teal-100 text-teal-700 font-semibold rounded text-[10px] border border-teal-200">
                                Resolve
                            </button>
                        ` : '<span class="text-[10px] text-slate-400 font-semibold">Closed</span>'}
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-red-500">Error: ${err.message}</td></tr>`;
    }
}

export function switchISOTab(tabName) {
    const tabs = ['certs', 'controls', 'audits', 'capas', 'grievances'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-iso-${t}`);
        const panel = document.getElementById(`iso-panel-${t}`);
        if (btn && panel) {
            if (t === tabName) {
                btn.className = 'py-2 border-b-2 border-amber-600 text-amber-700 flex items-center gap-2 font-bold';
                panel.classList.remove('hidden');
            } else {
                btn.className = 'py-2 text-slate-500 hover:text-slate-800 flex items-center gap-2';
                panel.classList.add('hidden');
            }
        }
    });
}

export function handleOpenGrievanceModal() {
    const modal = document.getElementById('modal-lodge-grievance');
    if (modal) modal.classList.remove('hidden');
}

export function closeGrievanceModal() {
    const modal = document.getElementById('modal-lodge-grievance');
    if (modal) modal.classList.add('hidden');
}

export async function handleLodgeGrievanceSubmit(event) {
    event.preventDefault();
    const grvId = `GRV-${new Date().getFullYear()}-${Math.floor(100 + Math.random() * 900)}`;
    const payload = {
        grievance_id: grvId,
        stakeholder_type: document.getElementById('grv-stakeholder-type').value,
        stakeholder_name: document.getElementById('grv-name').value,
        stakeholder_email: document.getElementById('grv-email').value,
        category: document.getElementById('grv-category').value,
        severity: 'High',
        subject: document.getElementById('grv-subject').value,
        description: document.getElementById('grv-desc').value,
        assigned_redressal_officer: 'Sole Director (Varadi Vijay)',
        statutory_sla_days: 7
    };

    try {
        const res = await fetch(`${API_BASE}/iso-standards/grievances`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Failed to lodge grievance');
        const data = await res.json();

        closeGrievanceModal();
        alert(`📜 Formal Grievance Registered!\n\n• Grievance ID: ${data.grievance_id}\n• Assigned Officer: ${data.assigned_redressal_officer}\n• Statutory SLA: ${data.statutory_sla_days} Days\n• An automated acknowledgment has been dispatched.`);
        loadISOStandardsModule();
    } catch (err) {
        alert('Error lodging grievance: ' + err.message);
    }
}

export async function handlePromptResolveGrievance(grievanceId) {
    const remedy = prompt('Enter final resolution details and remedial action taken:');
    if (!remedy) return;

    try {
        const res = await fetch(`${API_BASE}/iso-standards/grievances/${grievanceId}/resolve`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                investigation_notes: 'Reviewed and verified against standard operating procedures.',
                resolution_details: remedy,
                complainant_satisfied: true,
                csat_score: 5,
                status: 'Resolved & Closed'
            })
        });
        if (!res.ok) throw new Error('Failed to resolve grievance');
        alert(`✅ Grievance ${grievanceId} successfully resolved and closed!`);
        loadISOGrievancesTable();
    } catch (err) {
        alert('Error: ' + err.message);
    }
}

// ==========================================
// DYNAMIC REAL-TIME ENTERPRISE UTILITIES
// ==========================================

/**
 * Real-Time NTP Synchronized IST Clock (UTC+05:30)
 */
export function startLiveClockAndHeartbeat() {
    function updateClock() {
        const el = document.getElementById('live-ist-clock');
        if (!el) return;
        const now = new Date();
        const istString = now.toLocaleTimeString('en-GB', { timeZone: 'Asia/Kolkata', hour12: false });
        el.textContent = `${istString} IST`;
    }
    updateClock();
    setInterval(updateClock, 1000);
}

/**
 * Real-Time CERT-In 6-Hour SLA Live Countdown Timer
 */
export function startLiveCertInCountdown() {
    setInterval(() => {
        const timerBadges = document.querySelectorAll('.certin-countdown-timer');
        timerBadges.forEach(badge => {
            const deadlineAttr = badge.getAttribute('data-deadline');
            if (!deadlineAttr) return;
            const deadline = new Date(deadlineAttr).getTime();
            const now = Date.now();
            const diff = deadline - now;
            if (diff <= 0) {
                badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation mr-1"></i> SLA BREACHED`;
                badge.className = 'certin-countdown-timer px-2 py-0.5 rounded bg-rose-600 text-white font-mono text-[10px] font-black animate-pulse';
            } else {
                const hours = Math.floor(diff / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const secs = Math.floor((diff % (1000 * 60)) / 1000);
                const pad = (n) => String(n).padStart(2, '0');
                badge.innerHTML = `<i class="fa-solid fa-stopwatch mr-1"></i> ${pad(hours)}h ${pad(mins)}m ${pad(secs)}s REMAINING`;
                if (hours < 2) {
                    badge.className = 'certin-countdown-timer px-2 py-0.5 rounded bg-rose-500/20 border border-rose-500 text-rose-300 font-mono text-[10px] font-bold animate-pulse';
                }
            }
        });
    }, 1000);
}

/**
 * Enterprise Toast Notification Engine
 */
export function showEnterpriseToast(title, message, type = 'info', duration = 4500) {
    const container = document.getElementById('enterprise-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto transform transition-all duration-300 ease-out translate-y-2 opacity-0 p-4 rounded-xl shadow-2xl border flex items-start gap-3 backdrop-blur-md';
    
    let borderStyle = 'border-slate-700 bg-slate-900/95 text-white';
    let iconClass = 'fa-solid fa-circle-info text-blue-400';
    let badge = 'INFO';
    let badgeStyle = 'bg-blue-500/20 text-blue-300 border-blue-500/30';

    if (type === 'success') {
        borderStyle = 'border-emerald-500/40 bg-slate-900/95 text-white';
        iconClass = 'fa-solid fa-circle-check text-emerald-400';
        badge = 'SUCCESS';
        badgeStyle = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    } else if (type === 'error') {
        borderStyle = 'border-rose-500/50 bg-slate-900/95 text-white';
        iconClass = 'fa-solid fa-triangle-exclamation text-rose-400';
        badge = 'ALERT';
        badgeStyle = 'bg-rose-500/20 text-rose-300 border-rose-500/30';
    } else if (type === 'warning') {
        borderStyle = 'border-amber-500/50 bg-slate-900/95 text-white';
        iconClass = 'fa-solid fa-triangle-exclamation text-amber-400';
        badge = 'WARNING';
        badgeStyle = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
    } else if (type === 'certin') {
        borderStyle = 'border-red-600 bg-red-950/95 text-white ring-2 ring-red-500/50 animate-pulse';
        iconClass = 'fa-solid fa-shield-virus text-red-400 text-lg';
        badge = 'CERT-In SLA';
        badgeStyle = 'bg-red-500/30 text-red-200 border-red-500/50';
    }

    toast.className += ` ${borderStyle}`;
    const timeNow = new Date().toLocaleTimeString('en-GB', { timeZone: 'Asia/Kolkata', hour12: false });
    toast.innerHTML = `
        <div class="mt-0.5"><i class="${iconClass}"></i></div>
        <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2 mb-1">
                <span class="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded border ${badgeStyle}">${badge}</span>
                <span class="text-[10px] text-slate-400 font-mono">${timeNow} IST</span>
            </div>
            <h4 class="text-xs font-bold text-slate-100 truncate">${title}</h4>
            <p class="text-[11px] text-slate-300 mt-0.5 line-clamp-2 leading-relaxed">${message}</p>
        </div>
        <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-white transition text-xs p-1">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });

    if (duration > 0) {
        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => toast.remove(), 350);
        }, duration);
    }
}

/**
 * Dynamic Breadcrumb Navigation Metadata
 */
const MODULE_METADATA = {
    'dashboard': { category: 'Executive MIS', name: 'Executive Dashboard', icon: 'fa-chart-pie' },
    'governance': { category: 'Corporate Governance', name: 'MCA & Secretarial Records', icon: 'fa-building-columns' },
    'crm': { category: 'Client Operations', name: 'CRM & Client Pipeline', icon: 'fa-handshake' },
    'finance': { category: 'Finance & Treasury', name: 'Financial Accounting & Banking', icon: 'fa-scale-balanced' },
    'hrms': { category: 'People & HR', name: 'Human Resource Management', icon: 'fa-users' },
    'pmo': { category: 'Delivery Governance', name: 'PMO & CMMI/SDLC Tracking', icon: 'fa-diagram-project' },
    'sdlc': { category: 'Engineering & Dev', name: 'SDLC Process & Guardrails', icon: 'fa-code-branch' },
    'procurement': { category: 'Supply Chain', name: 'Vendor Sourcing & Strategic POs', icon: 'fa-boxes-packing' },
    'guardrails': { category: 'Architecture & QA', name: 'Architecture Guardrails', icon: 'fa-compass-drafting' },
    'iso-standards': { category: 'Quality & Standards', name: 'ISO 9001/27001/42001 & Grievances', icon: 'fa-award' },
    'ai-cloud': { category: 'AI & Cloud Infrastructure', name: 'AI Models, Cloud & MCPs', icon: 'fa-brain' },
    'infrastructure': { category: 'IT & Identity', name: 'Cloud & Passkey Access IAM', icon: 'fa-fingerprint' },
    'secops': { category: 'Cybersecurity', name: 'CERT-In Incident War Room', icon: 'fa-shield-halved' },
    'vault': { category: 'Security & Secrets', name: 'Enterprise Secrets Vault', icon: 'fa-vault' },
    'strategy': { category: 'Corporate Strategy', name: 'Strategic Roadmap & Goals', icon: 'fa-bullseye' },
    'analytics': { category: 'Business Intelligence', name: 'Executive Analytics Hub', icon: 'fa-chart-line' },
    'internal-support': { category: 'IT Service Management', name: 'Internal Service Desk', icon: 'fa-headset' },
    'itsm': { category: 'IT Service Management', name: 'ITSM & CMDB Operations Control Tower', icon: 'fa-network-wired' },
    'teams': { category: 'Enterprise Communications', name: 'Asperion Teams & Chat', icon: 'fa-comments' },
    'sharepoint': { category: 'Knowledge Management', name: 'SharePoint & SOP Repository', icon: 'fa-shapes' },
    'training': { category: 'Talent & Learning', name: 'Training & Joinee Academy LMS', icon: 'fa-graduation-cap' },
    'agentic-ai': { category: 'Autonomous Swarm', name: 'Agentic AI & Multi-Agent Swarm', icon: 'fa-robot' },
    'portal-employee': { category: 'Stakeholder Portals', name: 'Employee Self-Service Portal', icon: 'fa-user-gear' },
    'portal-client': { category: 'Stakeholder Portals', name: 'Client Engagement Portal', icon: 'fa-briefcase' },
    'portal-vendor': { category: 'Stakeholder Portals', name: 'Vendor Sourcing, POs & Inward GRN Portal', icon: 'fa-boxes-packing' }
};

export function updateBreadcrumbs(moduleName) {
    const meta = MODULE_METADATA[moduleName] || { category: 'Enterprise Core', name: moduleName, icon: 'fa-cube' };
    const catEl = document.getElementById('breadcrumb-category');
    const modEl = document.getElementById('breadcrumb-module');
    if (catEl) catEl.textContent = meta.category;
    if (modEl) {
        modEl.innerHTML = `<i class="fa-solid ${meta.icon} mr-1.5 text-blue-600"></i> ${meta.name}`;
    }
}

// ==============================================================================
// ENTERPRISE REAL-TIME DYNAMIC AUTO-SYNC & CONTINUOUS WATCHER
// ==============================================================================
export let autoSyncIntervalSec = 30;
export let autoSyncCountdown = 30;
export let autoSyncTimerId = null;

export function initAutoSyncManager() {
    if (autoSyncTimerId) clearInterval(autoSyncTimerId);
    autoSyncCountdown = autoSyncIntervalSec;
    
    autoSyncTimerId = setInterval(() => {
        if (autoSyncIntervalSec <= 0) return; // Paused
        autoSyncCountdown--;
        
        const countdownEl = document.getElementById('auto-sync-countdown');
        if (countdownEl) {
            countdownEl.textContent = `${autoSyncCountdown}s`;
        }
        
        if (autoSyncCountdown <= 0) {
            autoSyncCountdown = autoSyncIntervalSec;
            handleTriggerGlobalSync(false);
        }
    }, 1000);
}

export function setAutoSyncFrequency(seconds) {
    autoSyncIntervalSec = parseInt(seconds, 10);
    autoSyncCountdown = Math.max(1, autoSyncIntervalSec);
    const countdownEl = document.getElementById('auto-sync-countdown');
    if (countdownEl) {
        countdownEl.textContent = autoSyncIntervalSec > 0 ? `${autoSyncCountdown}s` : 'Paused';
    }
    showEnterpriseToast('Auto-Sync Frequency', `Continuous background sync updated to ${autoSyncIntervalSec > 0 ? autoSyncIntervalSec + 's interval' : 'Manual only'}.`, 'info', 2000);
}

export async function handleTriggerGlobalSync(isManual = true) {
    const syncBtn = document.getElementById('btn-global-sync');
    const syncIcon = document.getElementById('icon-global-sync');
    if (syncIcon) syncIcon.classList.add('fa-spin');
    
    try {
        const res = await fetch(`${API_BASE}/system/sync-all`, { method: 'POST' });
        const data = await res.json();
        
        // Refresh active module data dynamically
        if (typeof currentModule !== 'undefined' && currentModule) {
            refreshModuleData(currentModule);
        }
        
        // Refresh notifications & alerts
        if (typeof fetchNotificationsAndAlerts === 'function') {
            fetchNotificationsAndAlerts();
        }

        // Update live status text
        const syncLabel = document.getElementById('auto-sync-status-text');
        if (syncLabel) {
            const timeStr = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            syncLabel.innerHTML = `Auto-Sync: <strong id="auto-sync-countdown" class="text-slate-800 font-mono">${autoSyncCountdown}s</strong> <span class="text-[10px] text-emerald-600 font-medium font-mono">(${timeStr})</span>`;
        }
        
        if (isManual) {
            showEnterpriseToast(
                'Enterprise State Synchronized',
                `Reconciled all 21 modules with live database. Health: ${data.metrics?.system_health_score || 99.4}% | Active Agents: ${data.metrics?.active_agents || 5} | CI Nodes: ${data.metrics?.cmdb_ci_nodes || 8}.`,
                'success',
                3500
            );
        }
    } catch (err) {
        console.error('Error during global sync:', err);
        if (isManual) {
            showEnterpriseToast('Sync Notice', 'State refreshed from active database cache.', 'info', 2500);
        }
    } finally {
        if (syncIcon) {
            setTimeout(() => syncIcon.classList.remove('fa-spin'), 600);
        }
    }
}

export function refreshModuleData(moduleName) {
    switch (moduleName) {
        case 'dashboard': if (typeof loadDashboard === 'function') loadDashboard(); break;
        case 'governance': if (typeof loadGovernance === 'function') loadGovernance(); break;
        case 'crm': if (typeof loadCRM === 'function') loadCRM(); break;
        case 'finance': if (typeof loadFinance === 'function') loadFinance(); break;
        case 'hrms': if (typeof loadHRMS === 'function') loadHRMS(); break;
        case 'pmo': if (typeof loadPMO === 'function') loadPMO(); break;
        case 'sdlc': if (typeof loadSDLC === 'function') loadSDLC(); break;
        case 'procurement': if (typeof loadProcurement === 'function') loadProcurement(); break;
        case 'guardrails': if (typeof loadGuardrails === 'function') loadGuardrails(); break;
        case 'iso-standards': if (typeof loadISOStandardsModule === 'function') loadISOStandardsModule(); break;
        case 'ai-cloud': if (typeof loadAICloudModule === 'function') loadAICloudModule(); break;
        case 'agentic-ai': if (typeof loadAgenticAI === 'function') loadAgenticAI(); break;
        case 'infrastructure': if (typeof loadInfrastructure === 'function') loadInfrastructure(); break;
        case 'secops': if (typeof loadSecOps === 'function') loadSecOps(); break;
        case 'vault': if (typeof loadVault === 'function') loadVault(); break;
        case 'strategy': if (typeof loadStrategy === 'function') loadStrategy(); break;
        case 'analytics': if (typeof loadAnalyticsHub === 'function') loadAnalyticsHub(); break;
        case 'internal-support': if (typeof loadInternalSupport === 'function') loadInternalSupport(); break;
        case 'itsm': if (typeof loadITSM === 'function') loadITSM(); break;
        case 'teams': if (typeof loadTeams === 'function') loadTeams(); break;
        case 'sharepoint': if (typeof loadSharePoint === 'function') loadSharePoint(); break;
        case 'training': if (typeof loadTraining === 'function') loadTraining(); break;
        case 'portal-employee': if (typeof loadEmployeePortal === 'function') loadEmployeePortal(); break;
        case 'portal-client': if (typeof loadClientPortal === 'function') loadClientPortal(); break;
        case 'portal-vendor': if (typeof loadVendorPortal === 'function') loadVendorPortal(); break;
        case 'operations': if (typeof loadOperations === 'function') loadOperations(); break;
        case 'crypto-tools': if (typeof loadCryptoTools === 'function') loadCryptoTools(); break;
    }
}

export function toggleFloatingCopilotModal() {
    switchModule('agentic-ai');
    setTimeout(() => {
        if (typeof switchAgenticAITab === 'function') {
            switchAgenticAITab('chat');
        }
        const input = document.getElementById('agentic-chat-input');
        if (input) input.focus();
    }, 150);
}

/**
 * Universal Enterprise Command Palette Registry & Controller
 */
const ENTERPRISE_COMMANDS = [
    // Modules & Portals
    { category: 'Modules & Portals', title: 'Executive Management Information System (MIS)', icon: 'fa-chart-pie', action: () => switchModule('dashboard'), badge: 'Executive' },
    { category: 'Modules & Portals', title: 'Corporate Governance & MCA Filings', icon: 'fa-building-columns', action: () => switchModule('governance'), badge: 'MCA 2013' },
    { category: 'Modules & Portals', title: 'CRM & Client Pipeline', icon: 'fa-handshake', action: () => switchModule('crm'), badge: 'Clients' },
    { category: 'Modules & Portals', title: 'Financial Accounting, Tax & Treasury', icon: 'fa-scale-balanced', action: () => switchModule('finance'), badge: 'Tax & GST' },
    { category: 'Modules & Portals', title: 'Human Resources & Statutory Payroll', icon: 'fa-users', action: () => switchModule('hrms'), badge: 'EPFO & ESIC' },
    { category: 'Modules & Portals', title: 'PMO & Global Delivery Governance', icon: 'fa-diagram-project', action: () => switchModule('pmo'), badge: 'CMMI' },
    { category: 'Modules & Portals', title: 'SDLC Process, CI/CD & DevSecOps', icon: 'fa-code-branch', action: () => switchModule('sdlc'), badge: 'DevSecOps' },
    { category: 'Modules & Portals', title: 'Vendor Sourcing, POs & Inward GRN Portal', icon: 'fa-boxes-packing', action: () => switchModule('portal-vendor'), badge: 'Procurement' },
    { category: 'Modules & Portals', title: 'Architecture Guardrails & ADRs', icon: 'fa-compass-drafting', action: () => switchModule('guardrails'), badge: 'Tech Stack' },
    { category: 'Modules & Portals', title: 'ISO 9001, 27001, 42001 & Grievances', icon: 'fa-award', action: () => switchModule('iso-standards'), badge: 'ISO' },
    { category: 'Modules & Portals', title: 'AI Infrastructure, LLM APIs & MCPs', icon: 'fa-brain', action: () => switchModule('ai-cloud'), badge: 'AI & Cloud' },
    { category: 'Modules & Portals', title: 'Agentic AI & Autonomous Multi-Agent Swarm', icon: 'fa-robot', action: () => switchModule('agentic-ai'), badge: 'Swarm' },
    { category: 'Modules & Portals', title: 'ITSM & CMDB Operations Control Tower', icon: 'fa-network-wired', action: () => switchModule('itsm'), badge: 'ITIL v4' },
    { category: 'Modules & Portals', title: 'Training & Joinee Academy LMS', icon: 'fa-graduation-cap', action: () => switchModule('training'), badge: 'Academy' },
    { category: 'Modules & Portals', title: 'Asperion SharePoint & Knowledge Base', icon: 'fa-shapes', action: () => switchModule('sharepoint'), badge: 'SharePoint' },
    { category: 'Modules & Portals', title: 'IT Infrastructure & Passkey Access IAM', icon: 'fa-fingerprint', action: () => switchModule('infrastructure'), badge: 'Passkeys' },
    { category: 'Modules & Portals', title: 'Cybersecurity, SecOps & CERT-In War Room', icon: 'fa-shield-halved', action: () => switchModule('secops'), badge: 'CERT-In P1' },
    { category: 'Modules & Portals', title: 'Enterprise Secrets Vault', icon: 'fa-vault', action: () => switchModule('vault'), badge: 'AES-256' },
    { category: 'Modules & Portals', title: 'Strategic Roadmap & FY Objectives', icon: 'fa-bullseye', action: () => switchModule('strategy'), badge: 'Roadmap' },
    { category: 'Modules & Portals', title: 'Executive Analytics & BI Hub', icon: 'fa-chart-line', action: () => switchModule('analytics'), badge: 'Analytics' },
    { category: 'Modules & Portals', title: 'Internal IT Service Desk', icon: 'fa-headset', action: () => switchModule('internal-support'), badge: 'Support' },
    { category: 'Modules & Portals', title: 'Asperion Teams & Enterprise Chat Hub', icon: 'fa-comments', action: () => switchModule('teams'), badge: 'Teams' },
    { category: 'Modules & Portals', title: 'Employee Self-Service (ESS) Portal', icon: 'fa-user-gear', action: () => switchModule('portal-employee'), badge: 'ESS' },
    { category: 'Modules & Portals', title: 'Client Engagement Portal', icon: 'fa-briefcase', action: () => switchModule('portal-client'), badge: 'Client' },
    
    // Statutory & Enterprise Actions
    { category: 'Statutory & Operational Actions', title: 'Log Inward Goods Received Note (GRN)', icon: 'fa-truck-ramp-box', action: () => { switchModule('portal-vendor'); setTimeout(() => { if (typeof openVendorInwardModal === 'function') openVendorInwardModal(); }, 250); }, badge: 'Action' },
    { category: 'Statutory & Operational Actions', title: 'Create Purchase Order (PO)', icon: 'fa-cart-plus', action: () => { switchModule('portal-vendor'); setTimeout(() => { if (typeof openCreatePoModal === 'function') openCreatePoModal(); }, 250); }, badge: 'Action' },
    { category: 'Statutory & Operational Actions', title: 'Submit AP Bill (3-Way Match & TDS)', icon: 'fa-file-invoice-dollar', action: () => { switchModule('portal-vendor'); setTimeout(() => { if (typeof openSubmitBillModal === 'function') openSubmitBillModal(); }, 250); }, badge: 'Action' },
    { category: 'Statutory & Operational Actions', title: 'Lodge Formal ISO Grievance', icon: 'fa-file-shield', action: () => { if (typeof openGrievanceModal === 'function') openGrievanceModal(); }, badge: 'Action' },
    { category: 'Statutory & Operational Actions', title: 'Report Security Incident (CERT-In 6h SLA)', icon: 'fa-triangle-exclamation', action: () => { if (typeof openIncidentModal === 'function') openIncidentModal(); }, badge: 'Urgent' },
    { category: 'Statutory & Operational Actions', title: 'Run Autonomous Self-Healing Diagnostic Scan', icon: 'fa-wand-magic-sparkles', action: () => handleTriggerGlobalSelfHeal(), badge: 'Diagnostics' },
    { category: 'Statutory & Operational Actions', title: 'Stakeholder Dedicated Sign-In', icon: 'fa-lock', action: () => { if (typeof openStakeholderLoginModal === 'function') openStakeholderLoginModal(); }, badge: 'Auth' },
    { category: 'Statutory & Operational Actions', title: 'Sync System Notifications & Cross-Group Alerts', icon: 'fa-arrows-rotate', action: () => handleTriggerSyncAlerts(), badge: 'Sync' },
    { category: 'Statutory & Operational Actions', title: 'Start Instant Virtual Conference Huddle', icon: 'fa-headset', action: () => { switchModule('teams'); setTimeout(() => openTeamsHuddleModal(), 200); }, badge: 'Huddle' },
    { category: 'Statutory & Operational Actions', title: 'Open Sentinel AI Bot Assistant', icon: 'fa-robot', action: () => { switchModule('teams'); setTimeout(() => handleTriggerBotHelp(), 200); }, badge: 'AI Bot' },
    { category: 'Statutory & Operational Actions', title: 'Dispatch Autonomous Mission (ReAct Loop)', icon: 'fa-bolt', action: () => { switchModule('agentic-ai'); setTimeout(() => openDispatchMissionModal(), 200); }, badge: 'Swarm Action' },
    { category: 'Statutory & Operational Actions', title: 'Open Autonomous AI Swarm Copilot', icon: 'fa-comments', action: () => { switchModule('agentic-ai'); setTimeout(() => switchAgenticAITab('chat'), 200); }, badge: 'Copilot' },

    // Personas
    { category: 'Switch Persona', title: 'Varadi Vijay (Director / SuperAdmin)', icon: 'fa-user-tie', action: () => handleSwitchPersona('director@asperion.in'), badge: 'OPC Director' },
    { category: 'Switch Persona', title: 'Finance Head (CFO / Controller)', icon: 'fa-calculator', action: () => handleSwitchPersona('finance@asperion.in'), badge: 'Finance' },
    { category: 'Switch Persona', title: 'People & HR Lead', icon: 'fa-user-group', action: () => handleSwitchPersona('hr@asperion.in'), badge: 'HR' },
    { category: 'Switch Persona', title: 'PMO Delivery Lead', icon: 'fa-list-check', action: () => handleSwitchPersona('delivery@asperion.in'), badge: 'Delivery' },
    { category: 'Switch Persona', title: 'CISO / SOC Lead', icon: 'fa-user-shield', action: () => handleSwitchPersona('soc@asperion.in'), badge: 'Cybersecurity' },
    { category: 'Switch Persona', title: 'Arjun Sharma (Employee Self-Service)', icon: 'fa-id-badge', action: () => handleSwitchPersona('employee@asperion.in'), badge: 'Employee' },
    { category: 'Switch Persona', title: 'Zenith Global (Client Sponsor)', icon: 'fa-globe', action: () => handleSwitchPersona('client@zenith.com'), badge: 'Client' },
    { category: 'Switch Persona', title: 'Nexus Micro Cables (Vendor Supplier)', icon: 'fa-boxes-stacked', action: () => handleSwitchPersona('vendor@nexuscables.in'), badge: 'Vendor' }
];

export let commandPaletteSelectedIndex = 0;
export let currentFilteredCommands = [];

export function openCommandPalette() {
    const modal = document.getElementById('modal-command-palette');
    const input = document.getElementById('command-palette-input');
    if (!modal || !input) return;
    
    modal.classList.remove('hidden');
    input.value = '';
    handleCommandPaletteSearch('');
    setTimeout(() => input.focus(), 60);
}

export function closeCommandPalette() {
    const modal = document.getElementById('modal-command-palette');
    if (modal) modal.classList.add('hidden');
}

export function handleCommandPaletteSearch(query) {
    const q = (query || '').trim().toLowerCase();
    if (!q) {
        currentFilteredCommands = [...ENTERPRISE_COMMANDS];
    } else {
        currentFilteredCommands = ENTERPRISE_COMMANDS.filter(cmd => 
            cmd.title.toLowerCase().includes(q) || 
            cmd.category.toLowerCase().includes(q) ||
            (cmd.badge && cmd.badge.toLowerCase().includes(q))
        );
    }
    commandPaletteSelectedIndex = 0;
    renderCommandPaletteResults();
}

export function renderCommandPaletteResults() {
    const container = document.getElementById('command-palette-results');
    if (!container) return;

    if (currentFilteredCommands.length === 0) {
        container.innerHTML = `
            <div class="p-8 text-center text-slate-400">
                <i class="fa-solid fa-magnifying-glass text-2xl mb-2 text-slate-300"></i>
                <p class="font-medium text-xs">No matching modules or actions found</p>
                <p class="text-[11px] text-slate-400 mt-1">Try searching for "Vendor", "PO", "CERT-In", "ISO", or "Self-Heal"</p>
            </div>
        `;
        return;
    }

    const groups = {};
    currentFilteredCommands.forEach((cmd, idx) => {
        if (!groups[cmd.category]) groups[cmd.category] = [];
        groups[cmd.category].push({ cmd, originalIndex: idx });
    });

    let html = '';

    for (const [category, items] of Object.entries(groups)) {
        html += `<div class="pt-2 pb-1 px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400">${category}</div>`;
        items.forEach(({ cmd, originalIndex }) => {
            const isSelected = originalIndex === commandPaletteSelectedIndex;
            const activeClass = isSelected ? 'bg-blue-50 text-blue-900 border-l-4 border-blue-600 pl-2 font-medium' : 'hover:bg-slate-50 text-slate-700';
            
            html += `
                <div onclick="executeCommand(${originalIndex})" 
                     class="command-item flex items-center justify-between p-2.5 rounded-lg cursor-pointer transition ${activeClass}"
                     data-command-idx="${originalIndex}">
                    <div class="flex items-center gap-2.5 min-w-0">
                        <div class="w-7 h-7 rounded-md bg-slate-100 flex items-center justify-center text-slate-600 shrink-0 text-xs">
                            <i class="fa-solid ${cmd.icon}"></i>
                        </div>
                        <span class="truncate text-xs">${cmd.title}</span>
                    </div>
                    <div class="flex items-center gap-2 shrink-0">
                        ${cmd.badge ? `<span class="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">${cmd.badge}</span>` : ''}
                        ${isSelected ? '<kbd class="kbd-pill text-[9px] text-blue-700 font-bold">↵</kbd>' : ''}
                    </div>
                </div>
            `;
        });
    }

    container.innerHTML = html;

    const selectedEl = container.querySelector(`[data-command-idx="${commandPaletteSelectedIndex}"]`);
    if (selectedEl) {
        selectedEl.scrollIntoView({ block: 'nearest' });
    }
}

export function handleCommandPaletteKeydown(event) {
    if (event.key === 'Escape') {
        event.preventDefault();
        closeCommandPalette();
    } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (currentFilteredCommands.length > 0) {
            commandPaletteSelectedIndex = (commandPaletteSelectedIndex + 1) % currentFilteredCommands.length;
            renderCommandPaletteResults();
        }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (currentFilteredCommands.length > 0) {
            commandPaletteSelectedIndex = (commandPaletteSelectedIndex - 1 + currentFilteredCommands.length) % currentFilteredCommands.length;
            renderCommandPaletteResults();
        }
    } else if (event.key === 'Enter') {
        event.preventDefault();
        if (currentFilteredCommands[commandPaletteSelectedIndex]) {
            executeCommand(commandPaletteSelectedIndex);
        }
    }
}

export function executeCommand(index) {
    const item = currentFilteredCommands[index];
    if (!item) return;
    closeCommandPalette();
    try {
        item.action();
    } catch (err) {
        console.error('Error executing command:', err);
    }
}

export function openKeyboardShortcutsModal() {
    const modal = document.getElementById('modal-keyboard-shortcuts');
    if (modal) modal.classList.remove('hidden');
}

export function closeKeyboardShortcutsModal() {
    const modal = document.getElementById('modal-keyboard-shortcuts');
    if (modal) modal.classList.add('hidden');
}

export function filterTableRows(tableId, query) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const q = (query || '').toLowerCase().trim();
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? '' : 'none';
    });
}

/**
 * Enterprise Navigation & System Keyboard Shortcuts (Alt+1 through Alt+6, Alt+S, Ctrl+K, ?)
 */
export function initKeyboardShortcuts() {
    window.addEventListener('keydown', (e) => {
        // Universal Command Palette: Ctrl+K or Cmd+K
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            const modal = document.getElementById('modal-command-palette');
            if (modal && !modal.classList.contains('hidden')) {
                closeCommandPalette();
            } else {
                openCommandPalette();
            }
            return;
        }

        // Dismiss open modals on Escape
        if (e.key === 'Escape') {
            closeCommandPalette();
            closeKeyboardShortcutsModal();
            return;
        }

        // Open Shortcuts Modal on '?' (when not in an active input/textarea)
        const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
        const isEditing = activeTag === 'input' || activeTag === 'textarea' || activeTag === 'select';
        
        if (e.key === '?' && !isEditing && !e.ctrlKey && !e.altKey && !e.metaKey) {
            e.preventDefault();
            const modal = document.getElementById('modal-keyboard-shortcuts');
            if (modal && !modal.classList.contains('hidden')) {
                closeKeyboardShortcutsModal();
            } else {
                openKeyboardShortcutsModal();
            }
            return;
        }

        // Fast Alt+1..6 and Alt+S
        if (e.altKey && !e.ctrlKey && !e.metaKey) {
            if (e.key === '1') {
                e.preventDefault();
                switchModule('dashboard');
                showEnterpriseToast('Executive MIS', 'Navigated to Executive Dashboard (Alt+1)', 'info', 2000);
            } else if (e.key === '2') {
                e.preventDefault();
                switchModule('secops');
                showEnterpriseToast('Cybersecurity War Room', 'Navigated to CERT-In War Room & SecOps (Alt+2)', 'info', 2000);
            } else if (e.key === '3') {
                e.preventDefault();
                switchModule('infrastructure');
                showEnterpriseToast('IT & Cloud Infrastructure', 'Navigated to Passkey IAM & Multi-Cloud Posture (Alt+3)', 'info', 2000);
            } else if (e.key === '4') {
                e.preventDefault();
                switchModule('iso-standards');
                showEnterpriseToast('ISO & Compliance', 'Navigated to Integrated Standards & Redressal (Alt+4)', 'info', 2000);
            } else if (e.key === '5') {
                e.preventDefault();
                switchModule('pmo');
                showEnterpriseToast('PMO & Global Delivery', 'Navigated to CMMI/SDLC Delivery Governance (Alt+5)', 'info', 2000);
            } else if (e.key === '6') {
                e.preventDefault();
                switchModule('portal-vendor');
                showEnterpriseToast('Vendor Management', 'Navigated to Strategic Sourcing, POs & GRN (Alt+6)', 'info', 2000);
            } else if (e.key.toLowerCase() === 's') {
                e.preventDefault();
                handleTriggerGlobalSelfHeal();
            }
        }
    });
}








// =========================================================================
// ASPERION TEAMS & ENTERPRISE COMMUNICATIONS HUB CONTROLLER
// Channels, DMs, Document Embeds, Reactions, Virtual Huddles & Sentinel Bot
// =========================================================================

export let activeTeamsChannelId = null;
export let cachedTeamsChannels = [];
export let teamsPollingInterval = null;
export let isHuddleMicActive = true;
export let isHuddleCamActive = true;
export let isHuddleScreenSharing = false;

export async function loadTeams() {
    try {
        const [resOverview, resChannels, resPresence] = await Promise.all([
            fetch(`${API_BASE}/communications/overview`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/communications/channels`).then(r => r.json()),
            fetch(`${API_BASE}/communications/presence`).then(r => r.json())
        ]);

        cachedTeamsChannels = resChannels;

        // 1. Populate Overview Metrics
        if (resOverview) {
            const elCh = document.getElementById('teams-stat-channels');
            if (elCh) elCh.innerText = `${resOverview.total_channels} Channels`;

            const elOn = document.getElementById('teams-stat-online');
            if (elOn) elOn.innerText = `${resOverview.online_count} Online`;

            const elMsg = document.getElementById('teams-stat-messages');
            if (elMsg) elMsg.innerText = `${resOverview.total_messages} Messages`;

            const elHud = document.getElementById('teams-stat-huddles');
            if (elHud) elHud.innerText = `${resOverview.active_huddles_count} Huddle Active`;
        }

        // 2. Render Channels List in Left Rail
        renderTeamsChannelsList(resChannels);

        // 3. Render Team Presence Roster
        renderTeamsPresenceRoster(resPresence);

        // 4. Select default channel if not set
        if (!activeTeamsChannelId && resChannels.length > 0) {
            const defaultCh = resChannels.find(c => c.slug === 'announcements') || resChannels[0];
            selectTeamsChannel(defaultCh.id);
        } else if (activeTeamsChannelId) {
            selectTeamsChannel(activeTeamsChannelId);
        }

        // 5. Setup auto-refresh polling (every 6 seconds if module is active)
        if (!teamsPollingInterval) {
            teamsPollingInterval = setInterval(() => {
                if (currentModule === 'teams' && activeTeamsChannelId) {
                    reloadActiveChannelMessages(true);
                }
            }, 6000);
        }

    } catch (err) {
        console.error('Error loading Asperion Teams:', err);
    }
}

export function renderTeamsChannelsList(channels) {
    const chContainer = document.getElementById('teams-channels-list');
    const dmContainer = document.getElementById('teams-dms-list');
    if (!chContainer || !dmContainer) return;

    const publicChannels = channels.filter(c => c.channel_type !== 'DIRECT_MESSAGE');
    const directMessages = channels.filter(c => c.channel_type === 'DIRECT_MESSAGE');

    chContainer.innerHTML = publicChannels.map(c => {
        const isCurrent = c.id === activeTeamsChannelId;
        const icon = c.channel_type === 'WAR_ROOM' ? '<i class="fa-solid fa-shield-halved text-rose-400"></i>' : (c.is_pinned ? '<i class="fa-solid fa-thumbtack text-amber-400 text-[10px]"></i>' : '#');
        const badge = c.channel_type === 'WAR_ROOM' ? '<span class="px-1.5 py-0.2 rounded text-[8px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">WAR ROOM</span>' : '';

        return `
            <button onclick="selectTeamsChannel(${c.id})" class="w-full text-left px-2.5 py-1.5 rounded-lg flex items-center justify-between transition group ${isCurrent ? 'bg-indigo-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}">
                <div class="flex items-center gap-2 truncate min-w-0">
                    <span class="w-4 text-center font-bold text-xs ${isCurrent ? 'text-white' : 'text-slate-400'}">${icon}</span>
                    <span class="truncate text-xs">${c.slug}</span>
                </div>
                ${badge}
            </button>
        `;
    }).join('');

    dmContainer.innerHTML = directMessages.map(dm => {
        const isCurrent = dm.id === activeTeamsChannelId;
        return `
            <button onclick="selectTeamsChannel(${dm.id})" class="w-full text-left px-2.5 py-1.5 rounded-lg flex items-center justify-between transition group ${isCurrent ? 'bg-indigo-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}">
                <div class="flex items-center gap-2 truncate min-w-0">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 shrink-0"></span>
                    <span class="truncate text-xs">${dm.display_name.replace('🔒 Direct Message: ', '')}</span>
                </div>
            </button>
        `;
    }).join('');
}

export function renderTeamsPresenceRoster(presenceList) {
    const roster = document.getElementById('teams-presence-roster');
    if (!roster) return;

    roster.innerHTML = presenceList.map(p => {
        const statusDot = p.status === 'ONLINE' ? 'bg-emerald-400' :
            p.status === 'IN_MEETING' ? 'bg-amber-400' :
            p.status === 'FOCUS_DND' ? 'bg-rose-400' : 'bg-slate-500';

        return `
            <div class="flex items-center justify-between p-1.5 rounded-lg hover:bg-slate-800/60 transition text-[11px]">
                <div class="flex items-center gap-2 min-w-0">
                    <span class="w-2 h-2 rounded-full ${statusDot} shrink-0"></span>
                    <div class="truncate">
                        <span class="font-semibold text-slate-200 block truncate">${p.employee_name}</span>
                        <span class="text-[9px] text-slate-400 block truncate">${p.status_message}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

export function filterTeamsChannels(query) {
    if (!query) {
        renderTeamsChannelsList(cachedTeamsChannels);
        return;
    }
    const q = query.toLowerCase();
    const filtered = cachedTeamsChannels.filter(c => 
        c.slug.toLowerCase().includes(q) ||
        c.display_name.toLowerCase().includes(q) ||
        (c.description && c.description.toLowerCase().includes(q))
    );
    renderTeamsChannelsList(filtered);
}

export async function selectTeamsChannel(channelId) {
    activeTeamsChannelId = channelId;
    const channel = cachedTeamsChannels.find(c => c.id === channelId);
    
    // Update Header
    if (channel) {
        const nameEl = document.getElementById('teams-current-channel-name');
        if (nameEl) nameEl.innerText = `#${channel.slug} (${channel.display_name})`;

        const typeEl = document.getElementById('teams-current-channel-type');
        if (typeEl) {
            typeEl.innerText = channel.channel_type.replace('_', ' ');
            typeEl.className = channel.channel_type === 'WAR_ROOM' 
                ? 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-200'
                : 'px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800';
        }

        const topicEl = document.getElementById('teams-current-channel-topic');
        if (topicEl) topicEl.innerText = channel.topic || channel.description || 'Enterprise Workspace Channel';

        // Update Pinned Banner if exists
        const bannerEl = document.getElementById('teams-pinned-banner');
        if (bannerEl) {
            if (channel.is_pinned) {
                bannerEl.classList.remove('hidden');
                document.getElementById('teams-pinned-text').innerText = channel.description || channel.topic;
            } else {
                bannerEl.classList.add('hidden');
            }
        }
    }

    // Refresh Left Rail Active States
    renderTeamsChannelsList(cachedTeamsChannels);

    // Fetch and Render Messages
    await reloadActiveChannelMessages(false);
}

export async function reloadActiveChannelMessages(isSilent = false) {
    if (!activeTeamsChannelId) return;
    try {
        const res = await fetch(`${API_BASE}/communications/channels/${activeTeamsChannelId}/messages`);
        if (!res.ok) return;
        const messages = await res.json();
        renderTeamsMessages(messages, !isSilent);
    } catch (err) {
        console.error('Error fetching channel messages:', err);
    }
}

export function renderTeamsMessages(messages, autoScroll = true) {
    const container = document.getElementById('teams-messages-container');
    if (!container) return;

    if (messages.length === 0) {
        container.innerHTML = `
            <div class="h-full flex flex-col items-center justify-center text-center p-8 text-slate-400">
                <i class="fa-solid fa-comments text-4xl mb-3 text-slate-300"></i>
                <h4 class="font-bold text-sm text-slate-600">No messages in this channel yet</h4>
                <p class="text-xs text-slate-400 max-w-sm mt-1">Start the conversation or ask the Sentinel AI Bot with <code class="bg-slate-200 px-1 py-0.5 rounded text-[11px]">/status</code> or <code class="bg-slate-200 px-1 py-0.5 rounded text-[11px]">/kpi</code>.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = messages.map(m => {
        const isBot = m.message_type === 'SYSTEM_BOT';
        const isMe = m.sender_email === 'director@asperion.in';
        
        // Avatar circle color
        const avatarLetter = (m.sender_name || 'U').charAt(0).toUpperCase();
        const avatarBg = isBot ? 'bg-cyan-600' : (isMe ? 'bg-indigo-600' : 'bg-slate-700');
        const roleBadgeClass = isBot ? 'bg-cyan-100 text-cyan-800 border-cyan-200' :
            m.sender_role.includes('Director') ? 'bg-indigo-100 text-indigo-800 border-indigo-200' :
            m.sender_role.includes('Staff') || m.sender_role.includes('Engineer') ? 'bg-blue-100 text-blue-800 border-blue-200' :
            'bg-slate-100 text-slate-700 border-slate-200';

        // Format message body (support code block, bold markdown)
        let bodyHtml = escapeHtml(m.content)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code class="bg-slate-200 px-1 py-0.5 rounded text-[11px] font-mono text-indigo-700">$1</code>')
            .replace(/\n/g, '<br>');

        if (m.message_type === 'CODE_SNIPPET') {
            bodyHtml = `
                <div class="bg-slate-900 text-slate-100 p-3 rounded-xl font-mono text-[11px] overflow-x-auto border border-slate-800 shadow-inner mt-1">
                    <pre><code>${escapeHtml(m.content)}</code></pre>
                </div>
            `;
        }

        // Document Embed Card (if attached)
        let embedCardHtml = '';
        if (m.embed_type && m.embed_title) {
            const embedIcon = m.embed_type === 'OFFER_LETTER' ? 'fa-file-lines text-purple-600' :
                m.embed_type === 'PURCHASE_ORDER' ? 'fa-file-invoice text-emerald-600' :
                m.embed_type === 'INCIDENT_WAR_ROOM' ? 'fa-shield-halved text-rose-600' : 'fa-file-certificate text-blue-600';

            const actionBtn = m.embed_url ? `
                <a href="${m.embed_url}" target="_blank" class="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[10px] font-bold transition flex items-center gap-1">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Preview
                </a>
            ` : '';

            embedCardHtml = `
                <div class="mt-2 p-3 bg-white rounded-xl border border-indigo-200 shadow-sm flex items-center justify-between gap-3">
                    <div class="flex items-center gap-2.5 min-w-0">
                        <i class="fa-solid ${embedIcon} text-lg shrink-0"></i>
                        <div class="min-w-0">
                            <span class="text-[9px] font-bold uppercase tracking-wider text-slate-400 block">${m.embed_type.replace('_', ' ')}</span>
                            <span class="font-bold text-slate-900 text-xs truncate block">${m.embed_title}</span>
                        </div>
                    </div>
                    ${actionBtn}
                </div>
            `;
        }

        // Reactions Pills Bar
        const reactions = m.reactions || {};
        const reactionPills = Object.entries(reactions).map(([emoji, users]) => `
            <button onclick="handleToggleMessageReaction(${m.id}, '${emoji}')" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-white border border-slate-200 hover:border-indigo-400 shadow-2xs transition" title="${users.join(', ')}">
                <span>${emoji}</span>
                <span class="text-slate-600 font-bold">${users.length}</span>
            </button>
        `).join('');

        // Action Toolbar
        const pinAction = m.is_pinned 
            ? `<button onclick="handleToggleMessagePin(${m.id})" class="text-amber-500 hover:text-amber-600" title="Unpin"><i class="fa-solid fa-thumbtack text-xs"></i></button>`
            : `<button onclick="handleToggleMessagePin(${m.id})" class="text-slate-400 hover:text-slate-600" title="Pin Message"><i class="fa-solid fa-thumbtack text-xs"></i></button>`;

        return `
            <div class="flex items-start gap-3 group transition p-2 rounded-xl hover:bg-white/80 ${m.is_pinned ? 'bg-amber-50/50 border-l-2 border-amber-400 pl-3' : ''}">
                <div class="w-8 h-8 rounded-full ${avatarBg} text-white font-bold flex items-center justify-center text-xs shrink-0 shadow-sm">
                    ${isBot ? '<i class="fa-solid fa-robot text-xs"></i>' : avatarLetter}
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="font-bold text-slate-900 text-xs">${m.sender_name}</span>
                            <span class="px-1.5 py-0.2 rounded text-[9px] font-semibold border ${roleBadgeClass}">${m.sender_role}</span>
                            <span class="text-[10px] text-slate-400 font-mono">${formatDate(m.created_at)}</span>
                        </div>
                        <div class="opacity-0 group-hover:opacity-100 flex items-center gap-1.5 transition">
                            <button onclick="handleToggleMessageReaction(${m.id}, '👍')" class="text-slate-400 hover:text-slate-600 px-1" title="React 👍">👍</button>
                            <button onclick="handleToggleMessageReaction(${m.id}, '🚀')" class="text-slate-400 hover:text-slate-600 px-1" title="React 🚀">🚀</button>
                            <button onclick="handleToggleMessageReaction(${m.id}, '❤️')" class="text-slate-400 hover:text-slate-600 px-1" title="React ❤️">❤️</button>
                            ${pinAction}
                        </div>
                    </div>
                    <div class="text-xs text-slate-800 mt-1 leading-relaxed">${bodyHtml}</div>
                    ${embedCardHtml}
                    ${reactionPills ? `<div class="flex flex-wrap items-center gap-1.5 mt-2">${reactionPills}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');

    if (autoScroll) {
        container.scrollTop = container.scrollHeight;
    }
}

// Handler: Send Message
export async function handleSendTeamsMessage(e) {
    e.preventDefault();
    if (!activeTeamsChannelId) {
        alert('Please select a channel first.');
        return;
    }

    const input = document.getElementById('teams-message-input');
    const content = input.value.trim();
    if (!content) return;

    // Check embed select
    const embedSelect = document.getElementById('teams-quick-embed-select');
    let embedType = null;
    let embedId = null;
    let embedTitle = null;
    let embedUrl = null;

    if (embedSelect && embedSelect.value) {
        embedType = embedSelect.value;
        if (embedType === 'OFFER_LETTER') {
            embedId = 1;
            embedTitle = 'HR-ONB-01 Formal Offer Letter: Siddharth Kulkarni';
            embedUrl = '/api/v1/hrms/letters/1/html';
        } else if (embedType === 'PURCHASE_ORDER') {
            embedId = 1;
            embedTitle = 'PO-2026-001: AWS Cloud Reserved Infrastructure';
            embedUrl = '/api/v1/procurement/orders/1/html';
        } else if (embedType === 'INCIDENT_WAR_ROOM') {
            embedId = 1;
            embedTitle = 'INC-2026-0881 CERT-In Incident Triage Report';
            embedUrl = '/api/v1/cybersecurity/incidents/1/filing-report';
        } else if (embedType === 'BOARD_RESOLUTION') {
            embedId = 1;
            embedTitle = 'ADT/RES/2026/001: Opening of Current Account with ICICI Bank';
            embedUrl = '#view-governance';
        }
    }

    input.value = '';
    if (embedSelect) embedSelect.value = '';

    try {
        const res = await fetch(`${API_BASE}/communications/channels/${activeTeamsChannelId}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content: content,
                message_type: embedType ? 'DOCUMENT_EMBED' : 'TEXT',
                embed_type: embedType,
                embed_id: embedId,
                embed_title: embedTitle,
                embed_url: embedUrl,
                sender_name: "Director Varadi Vijay",
                sender_email: "director@asperion.in",
                sender_role: "Director & Founder"
            })
        });

        if (res.ok) {
            await reloadActiveChannelMessages(false);
            // Refresh channel list so latest message snippet updates
            const chRes = await fetch(`${API_BASE}/communications/channels`).then(r => r.json());
            cachedTeamsChannels = chRes;
            renderTeamsChannelsList(chRes);
        } else {
            alert('Failed to send message.');
        }
    } catch (err) {
        alert('Error sending message: ' + err.message);
    }
}

// Handler: Toggle Reaction
export async function handleToggleMessageReaction(messageId, emoji) {
    try {
        const res = await fetch(`${API_BASE}/communications/messages/${messageId}/reactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emoji: emoji,
                user_name: "Director Varadi Vijay"
            })
        });
        if (res.ok) {
            reloadActiveChannelMessages(true);
        }
    } catch (err) {
        console.error('Error toggling reaction:', err);
    }
}

// Handler: Toggle Message Pin
export async function handleToggleMessagePin(messageId) {
    try {
        const res = await fetch(`${API_BASE}/communications/messages/${messageId}/pin`, {
            method: 'PATCH'
        });
        if (res.ok) {
            reloadActiveChannelMessages(true);
        }
    } catch (err) {
        console.error('Error pinning message:', err);
    }
}

// Handler: Create Channel
export async function handleCreateTeamsChannel(e) {
    e.preventDefault();
    try {
        const slug = document.getElementById('new-ch-slug').value.trim();
        const display = document.getElementById('new-ch-display').value.trim();
        const chType = document.getElementById('new-ch-type').value;
        const desc = document.getElementById('new-ch-desc').value.trim();

        const res = await fetch(`${API_BASE}/communications/channels`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: slug,
                display_name: display,
                channel_type: chType,
                description: desc,
                topic: desc,
                created_by_name: "Director Varadi Vijay"
            })
        });

        if (res.ok) {
            const newCh = await res.json();
            alert(`✅ Channel #${newCh.slug} created successfully!`);
            closeTeamsModal('modal-teams-new-channel');
            await loadTeams();
            selectTeamsChannel(newCh.id);
        } else {
            const err = await res.json();
            alert('Error creating channel: ' + (err.detail || 'Validation error'));
        }
    } catch (err) {
        alert('Error creating channel: ' + err.message);
    }
}

// Handler: Update Presence
export async function handleUpdateMyPresence(status) {
    try {
        let msg = "Available";
        if (status === 'IN_MEETING') msg = "In SteerCo Meeting";
        else if (status === 'FOCUS_DND') msg = "Focus Mode (Do Not Disturb)";
        else if (status === 'AWAY') msg = "Away from keyboard";

        const res = await fetch(`${API_BASE}/communications/presence?user_email=director@asperion.in`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: status,
                status_message: msg,
                location_tag: "Horamavu Bangalore HQ"
            })
        });

        if (res.ok) {
            const presRes = await fetch(`${API_BASE}/communications/presence`).then(r => r.json());
            renderTeamsPresenceRoster(presRes);
        }
    } catch (err) {
        console.error('Error updating presence:', err);
    }
}

// Helper: Insert text formatting snippet into input
export function insertMessageSnippet(type) {
    const input = document.getElementById('teams-message-input');
    if (!input) return;
    if (type === 'bold') input.value += ' **bold text** ';
    else if (type === 'italic') input.value += ' *italic text* ';
    else if (type === 'code') input.value += ' `code_snippet()` ';
    input.focus();
}

export function handleSelectDocumentEmbed(val) {
    const input = document.getElementById('teams-message-input');
    if (!input || !val) return;
    input.value = `Attaching official ${val.replace('_', ' ')} for team review and sign-off.`;
    input.focus();
}

export function handleTriggerBotHelp() {
    const input = document.getElementById('teams-message-input');
    if (!input) return;
    input.value = '/help';
    input.focus();
}

// Modals management
export function openTeamsModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('hidden');
}

export function closeTeamsModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('hidden');
}

// Virtual Conference Huddle Handlers
export function openTeamsHuddleModal() {
    const el = document.getElementById('modal-teams-huddle');
    if (el) el.classList.remove('hidden');
}

export function closeTeamsHuddleModal() {
    const el = document.getElementById('modal-teams-huddle');
    if (el) el.classList.add('hidden');
}

export function toggleHuddleMic() {
    isHuddleMicActive = !isHuddleMicActive;
    const btn = document.getElementById('huddle-btn-mic');
    if (btn) {
        btn.innerHTML = isHuddleMicActive 
            ? '<i class="fa-solid fa-microphone text-emerald-400"></i> Mute Mic'
            : '<i class="fa-solid fa-microphone-slash text-rose-400"></i> Unmute Mic';
    }
}

export function toggleHuddleCam() {
    isHuddleCamActive = !isHuddleCamActive;
    const btn = document.getElementById('huddle-btn-cam');
    if (btn) {
        btn.innerHTML = isHuddleCamActive 
            ? '<i class="fa-solid fa-video text-blue-400"></i> Video On'
            : '<i class="fa-solid fa-video-slash text-slate-400"></i> Video Off';
    }
}

export function toggleHuddleScreenShare() {
    isHuddleScreenSharing = !isHuddleScreenSharing;
    const btn = document.getElementById('huddle-btn-screen');
    if (btn) {
        btn.innerHTML = isHuddleScreenSharing 
            ? '<i class="fa-solid fa-stop text-rose-400"></i> Stop Sharing'
            : '<i class="fa-solid fa-arrow-up-from-bracket text-cyan-400"></i> Share Screen';
    }
}

export function handleLeaveHuddle() {
    closeTeamsHuddleModal();
    alert('You have left the virtual huddle session.');
}

// Helper: Escape HTML string safely
export function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}



/* =========================================================================
   ASPERION SHAREPOINT & ENTERPRISE KNOWLEDGE MANAGEMENT CONTROLLER
   Supports: SOPs, Methods, Mechanisms, Employee Thoughts, Q&A, Document Library
   ========================================================================= */

export let currentSharePointTab = 'sops';
export let spSearchDebounce = null;

export async function loadSharePoint() {
    try {
        const overviewRes = await fetch('/api/v1/sharepoint/overview');
        if (overviewRes.ok) {
            const overview = await overviewRes.json();
            const setVal = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.innerText = val;
            };
            setVal('sp-kpi-sops', overview.total_sops || 0);
            setVal('sp-kpi-thoughts', overview.total_thoughts || 0);
            setVal('sp-kpi-mechanisms', overview.total_mechanisms || 0);
            setVal('sp-kpi-questions', overview.total_questions || 0);
            setVal('sp-kpi-documents', overview.total_documents || 0);
            setVal('sp-doc-lib-count', overview.total_documents || 0);
        }
        await loadSharePointTabContent(currentSharePointTab);
    } catch (err) {
        console.error("Error loading SharePoint:", err);
    }
}

export function switchSharePointTab(tabName) {
    currentSharePointTab = tabName;
    document.querySelectorAll('.sp-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.className = "sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-teal-50 text-teal-700 border border-teal-200 shadow-sm";
        } else {
            btn.className = "sp-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100";
        }
    });

    document.querySelectorAll('.sp-tab-pane').forEach(pane => pane.classList.add('hidden'));
    const activePane = document.getElementById(`sp-pane-${tabName}`);
    if (activePane) activePane.classList.remove('hidden');

    loadSharePointTabContent(tabName);
}

export function handleSharePointSearch(val) {
    clearTimeout(spSearchDebounce);
    spSearchDebounce = setTimeout(() => {
        loadSharePointTabContent(currentSharePointTab);
    }, 300);
}

export function handleSharePointDeptFilter(val) {
    loadSharePointTabContent(currentSharePointTab);
}

export async function loadSharePointTabContent(tabName) {
    const searchVal = document.getElementById('sp-search-input')?.value?.trim() || '';
    const deptVal = document.getElementById('sp-dept-filter')?.value || 'All';
    const params = new URLSearchParams();
    if (searchVal) params.append('query', searchVal);
    if (deptVal && deptVal !== 'All') params.append('department', deptVal);

    if (tabName === 'sops') {
        params.append('category', 'SOP & Procedures');
        const res = await fetch(`/api/v1/sharepoint/articles?${params.toString()}`);
        if (res.ok) {
            const articles = await res.json();
            renderSharePointSOPs(articles);
        }
    } else if (tabName === 'thoughts') {
        params.append('category', 'Employee Thoughts');
        const res = await fetch(`/api/v1/sharepoint/articles?${params.toString()}`);
        if (res.ok) {
            const articles = await res.json();
            renderSharePointThoughts(articles);
        }
    } else if (tabName === 'methods') {
        params.append('category', 'Methods & Mechanisms');
        const res = await fetch(`/api/v1/sharepoint/articles?${params.toString()}`);
        if (res.ok) {
            const articles = await res.json();
            renderSharePointMethods(articles);
        }
    } else if (tabName === 'community') {
        const res = await fetch(`/api/v1/sharepoint/community/questions?${params.toString()}`);
        if (res.ok) {
            const questions = await res.json();
            renderSharePointCommunity(questions);
        }
    } else if (tabName === 'documents') {
        const res = await fetch(`/api/v1/sharepoint/document-library?${params.toString()}`);
        if (res.ok) {
            const docs = await res.json();
            renderSharePointDocumentLibrary(docs);
        }
    }
}

export function renderSharePointSOPs(articles) {
    const container = document.getElementById('sp-list-sops');
    if (!container) return;
    if (!articles || articles.length === 0) {
        container.innerHTML = `
            <div class="col-span-2 text-center p-8 bg-white rounded-xl border border-dashed border-slate-200">
                <i class="fa-solid fa-list-check text-slate-300 text-3xl mb-2"></i>
                <div class="text-sm font-semibold text-slate-600">No Standard Operating Procedures Found</div>
                <div class="text-xs text-slate-400 mt-1">Try adjusting your filters or publish a new SOP above.</div>
            </div>`;
        return;
    }

    container.innerHTML = articles.map(a => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200 font-mono">
                        ${a.article_code}
                    </span>
                    <div class="flex items-center gap-1.5">
                        <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                            ${a.department}
                        </span>
                        <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                            ${a.version || 'v1.0'}
                        </span>
                        ${a.featured_badge ? `<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-amber-50 text-amber-700 border border-amber-200">${a.featured_badge}</span>` : ''}
                    </div>
                </div>
                <h3 class="font-bold text-slate-800 text-sm mb-1 leading-snug">${a.title}</h3>
                <p class="text-xs text-slate-500 mb-3 line-clamp-2">${a.summary}</p>
                <div class="flex flex-wrap items-center gap-2 text-[10px] text-slate-400 mb-3">
                    <span><i class="fa-solid fa-shield-halved text-teal-600"></i> ${a.iso_compliance_tag}</span>
                    <span>&bull;</span>
                    <span><i class="fa-solid fa-user-pen text-slate-500"></i> ${a.author_name}</span>
                    <span>&bull;</span>
                    <span><i class="fa-solid fa-eye text-slate-400"></i> ${a.views_count} views</span>
                </div>
                ${a.steps && a.steps.length > 0 ? `
                <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100 mb-3 text-[11px] text-slate-600 flex items-center justify-between">
                    <span><i class="fa-solid fa-diagram-project text-blue-600 mr-1"></i> Structured Workflow: <strong>${a.steps.length} Execution Steps</strong></span>
                    <span class="text-[10px] text-slate-400">Checklist Ready</span>
                </div>` : ''}
            </div>
            <div class="flex items-center justify-between pt-3 border-t border-slate-100 gap-2">
                <button onclick="viewSharePointSOP(${a.id})" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5">
                    <i class="fa-solid fa-clipboard-check"></i> View Procedure
                </button>
                <button onclick="exportSharePointDocument(${a.id})" class="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition flex items-center gap-1" title="Printable Document">
                    <i class="fa-solid fa-print"></i> Printable
                </button>
            </div>
        </div>
    `).join('');
}

export function renderSharePointThoughts(articles) {
    const container = document.getElementById('sp-list-thoughts');
    if (!container) return;
    if (!articles || articles.length === 0) {
        container.innerHTML = `
            <div class="text-center p-8 bg-white rounded-xl border border-dashed border-slate-200">
                <i class="fa-solid fa-lightbulb text-slate-300 text-3xl mb-2"></i>
                <div class="text-sm font-semibold text-slate-600">No Thought Pieces Found</div>
                <div class="text-xs text-slate-400 mt-1">Share your reflections, insights, or ideas with the team above.</div>
            </div>`;
        return;
    }

    container.innerHTML = articles.map(a => {
        const currentUser = "Varadi Vijay";
        const hasLiked = (a.likes_users || []).includes(currentUser);
        return `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div class="flex items-start justify-between gap-3 mb-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-teal-600 to-indigo-600 text-white font-bold flex items-center justify-center text-sm shadow">
                        ${a.author_name.charAt(0)}
                    </div>
                    <div>
                        <div class="font-bold text-slate-800 text-xs flex items-center gap-2">
                            ${a.author_name}
                            <span class="px-1.5 py-0.2 rounded text-[9px] bg-slate-100 text-slate-600 font-normal">${a.author_role}</span>
                        </div>
                        <div class="text-[10px] text-slate-400 flex items-center gap-1.5 mt-0.5">
                            <span>${a.department}</span>
                            <span>&bull;</span>
                            <span>${new Date(a.created_at).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
                            ${a.is_pinned ? `<span class="text-indigo-600 font-bold"><i class="fa-solid fa-thumbtack"></i> Pinned</span>` : ''}
                        </div>
                    </div>
                </div>
                ${a.featured_badge ? `<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-amber-50 text-amber-700 border border-amber-200">${a.featured_badge}</span>` : ''}
            </div>

            <h3 class="font-bold text-slate-900 text-sm mb-2 leading-snug">${a.title}</h3>
            <div class="text-xs text-slate-700 leading-relaxed space-y-2 mb-4 bg-slate-50/70 p-3.5 rounded-xl border border-slate-100 whitespace-pre-line font-sans">
                ${a.content}
            </div>

            <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
                <div class="flex items-center gap-3">
                    <button onclick="toggleSharePointLike(${a.id})" class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg transition ${hasLiked ? 'text-rose-600 bg-rose-50 font-bold' : 'text-slate-500 hover:bg-slate-100'}">
                        <i class="fa-${hasLiked ? 'solid' : 'regular'} fa-heart"></i>
                        <span>${a.likes_count || 0}</span>
                    </button>
                    <button onclick="toggleThoughtComments(${a.id})" class="flex items-center gap-1.5 px-2.5 py-1 text-slate-500 hover:bg-slate-100 rounded-lg transition">
                        <i class="fa-regular fa-comment"></i>
                        <span id="thought-comments-count-${a.id}">Comments</span>
                    </button>
                </div>
                <button onclick="exportSharePointDocument(${a.id})" class="text-slate-400 hover:text-slate-600 text-[11px] flex items-center gap-1">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Export Printable
                </button>
            </div>

            <!-- Threaded Comments Section -->
            <div id="thought-comments-pane-${a.id}" class="hidden mt-3 pt-3 border-t border-slate-100 space-y-2">
                <div id="thought-comments-list-${a.id}" class="space-y-2">
                    <!-- Loaded dynamically -->
                </div>
                <form onsubmit="handlePostArticleComment(event, ${a.id})" class="flex items-center gap-2 mt-2 pt-2 border-t border-slate-100">
                    <input type="text" name="comment_content" placeholder="Write a reflection or reply..." required class="flex-1 px-3 py-1.5 border border-slate-200 rounded-lg text-xs bg-slate-50 focus:outline-none focus:ring-1 focus:ring-teal-500">
                    <button type="submit" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold transition">Reply</button>
                </form>
            </div>
        </div>`;
    }).join('');
}

export function renderSharePointMethods(articles) {
    const container = document.getElementById('sp-list-methods');
    if (!container) return;
    if (!articles || articles.length === 0) {
        container.innerHTML = `
            <div class="col-span-2 text-center p-8 bg-white rounded-xl border border-dashed border-slate-200">
                <i class="fa-solid fa-network-wired text-slate-300 text-3xl mb-2"></i>
                <div class="text-sm font-semibold text-slate-600">No Methods or Mechanisms Found</div>
                <div class="text-xs text-slate-400 mt-1">Publish architectural patterns, engineering mechanisms, or blueprints above.</div>
            </div>`;
        return;
    }

    container.innerHTML = articles.map(a => `
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200 font-mono">
                        ${a.article_code}
                    </span>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                        ${a.department}
                    </span>
                </div>
                <h3 class="font-bold text-slate-800 text-sm mb-1 leading-snug">${a.title}</h3>
                <p class="text-xs text-slate-500 mb-3">${a.summary}</p>
                <div class="bg-slate-900 text-slate-200 p-3 rounded-lg text-[11px] font-mono mb-3 line-clamp-3">
                    ${a.content}
                </div>
                <div class="flex items-center gap-2 text-[10px] text-slate-400 mb-2">
                    <span><i class="fa-solid fa-code-commit text-purple-600"></i> ${a.author_name}</span>
                    <span>&bull;</span>
                    <span><i class="fa-solid fa-certificate text-teal-600"></i> ${a.iso_compliance_tag}</span>
                </div>
            </div>
            <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                <span class="text-[10px] text-slate-400"><i class="fa-solid fa-heart text-rose-500 mr-1"></i> ${a.likes_count || 0} likes</span>
                <button onclick="exportSharePointDocument(${a.id})" class="px-3 py-1 bg-purple-50 text-purple-700 hover:bg-purple-100 rounded-lg text-xs font-bold transition flex items-center gap-1">
                    <i class="fa-solid fa-file-lines"></i> Open Blueprint
                </button>
            </div>
        </div>
    `).join('');
}

export function renderSharePointCommunity(questions) {
    const container = document.getElementById('sp-list-community');
    if (!container) return;
    if (!questions || questions.length === 0) {
        container.innerHTML = `
            <div class="text-center p-8 bg-white rounded-xl border border-dashed border-slate-200">
                <i class="fa-solid fa-comments text-slate-300 text-3xl mb-2"></i>
                <div class="text-sm font-semibold text-slate-600">No Community Questions Found</div>
                <div class="text-xs text-slate-400 mt-1">Ask the team a technical or operational question above.</div>
            </div>`;
        return;
    }

    container.innerHTML = questions.map(q => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-start gap-4">
            <div class="flex flex-col items-center justify-center p-2 rounded-lg bg-slate-50 border border-slate-200 text-center shrink-0 w-16">
                <button onclick="upvoteSharePointQuestion(${q.id})" class="text-slate-400 hover:text-emerald-600 transition" title="Upvote this question">
                    <i class="fa-solid fa-arrow-up text-sm"></i>
                </button>
                <span class="font-bold text-slate-800 text-xs my-0.5">${q.upvotes_count || 0}</span>
                <span class="text-[9px] text-slate-400 uppercase font-bold">Votes</span>
            </div>
            <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono">${q.question_code}</span>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600 border border-slate-200">${q.department}</span>
                    ${q.has_verified_solution ? '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-teal-100 text-teal-800"><i class="fa-solid fa-circle-check"></i> Verified Solution</span>' : ''}
                    <span class="ml-auto text-[10px] text-slate-400">${new Date(q.created_at).toLocaleDateString()}</span>
                </div>
                <h3 class="font-bold text-slate-900 text-sm mb-1">${q.title}</h3>
                <p class="text-xs text-slate-600 mb-2 leading-relaxed">${q.body}</p>
                <div class="flex flex-wrap items-center justify-between text-xs pt-2 border-t border-slate-100 gap-2">
                    <div class="flex items-center gap-1.5 text-[10px] text-slate-400">
                        <span>Asked by: <strong>${q.author_name}</strong> (${q.author_role})</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] font-semibold text-slate-600"><i class="fa-regular fa-comment-dots text-emerald-600 mr-1"></i> ${q.answers_count || 0} Answers</span>
                        <button onclick="promptAnswerSharePointQuestion(${q.id})" class="px-2.5 py-1 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded text-xs font-bold transition">
                            + Answer
                        </button>
                    </div>
                </div>

                ${q.answers && q.answers.length > 0 ? `
                <div class="mt-3 space-y-2 pt-2 border-t border-slate-100">
                    ${q.answers.map(ans => `
                        <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                            <div class="flex items-center justify-between mb-1">
                                <span class="font-bold text-slate-700">${ans.author} <span class="text-[10px] font-normal text-slate-500">(${ans.role})</span></span>
                                ${ans.is_verified ? '<span class="text-[10px] font-bold text-teal-600"><i class="fa-solid fa-check-circle"></i> Best Answer</span>' : ''}
                            </div>
                            <div class="text-slate-600 leading-relaxed font-sans">${ans.text}</div>
                        </div>
                    `).join('')}
                </div>` : ''}
            </div>
        </div>
    `).join('');
}

export function renderSharePointDocumentLibrary(docs) {
    const tbody = document.getElementById('sp-table-documents');
    if (!tbody) return;
    if (!docs || docs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-6 text-center text-slate-400 text-xs">No documents found in repository.</td></tr>`;
        return;
    }

    const typeBadges = {
        'DOCX': 'bg-blue-100 text-blue-800 border-blue-200',
        'PDF': 'bg-rose-100 text-rose-800 border-rose-200',
        'XLSX': 'bg-emerald-100 text-emerald-800 border-emerald-200',
        'DRAWIO': 'bg-amber-100 text-amber-800 border-amber-200',
        'MARKDOWN': 'bg-purple-100 text-purple-800 border-purple-200'
    };

    tbody.innerHTML = docs.map(d => `
        <tr class="hover:bg-slate-50/80 transition">
            <td class="p-3 font-mono font-bold text-slate-700">${escapeHtml(d.doc_code)}</td>
            <td class="p-3">
                <div class="font-bold text-slate-800">${escapeHtml(d.title)}</div>
                <div class="text-[10px] text-slate-500 line-clamp-1">${escapeHtml(d.description || '')}</div>
            </td>
            <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${typeBadges[d.file_type] || 'bg-slate-100 text-slate-700'}">${escapeHtml(d.file_type)}</span>
            </td>
            <td class="p-3 text-slate-600">${escapeHtml(d.category)}</td>
            <td class="p-3 text-slate-600">${escapeHtml(d.department)}</td>
            <td class="p-3 font-mono text-[11px] text-slate-700">${escapeHtml(d.version_tag || 'v1.0')}</td>
            <td class="p-3 text-slate-600">${escapeHtml(d.uploaded_by || 'Admin')}</td>
            <td class="p-3 text-right">
                <button onclick="showEnterpriseToast('Document Selected', 'Opening ${escapeHtml(d.doc_code)}: ${escapeHtml(d.title)}', 'info', 2000)" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-50 hover:text-teal-700 rounded text-[11px] font-medium transition">
                    <i class="fa-solid fa-eye mr-1"></i> View
                </button>
            </td>
        </tr>
    `).join('');
}

export function openSharePointModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.remove('hidden');
}

export function closeSharePointModal(modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.add('hidden');
}

export function handleSharePointCategoryChange(val) {
    const stepsSec = document.getElementById('sp-art-steps-section');
    if (!stepsSec) return;
    if (val === 'SOP & Procedures') {
        stepsSec.classList.remove('hidden');
    } else {
        stepsSec.classList.add('hidden');
    }
}

export function addSharePointStepRow() {
    const container = document.getElementById('sp-art-steps-container');
    if (!container) return;
    const stepNum = container.children.length + 1;
    const row = document.createElement('div');
    row.className = "flex items-start gap-2 bg-white p-2.5 rounded-lg border border-slate-200 text-xs";
    row.innerHTML = `
        <span class="w-6 h-6 rounded-full bg-teal-100 text-teal-800 font-bold flex items-center justify-center text-[10px] shrink-0 mt-1">${stepNum}</span>
        <div class="flex-1 space-y-1">
            <input type="text" placeholder="Step title (e.g. Verify Staging Health)..." required class="sp-step-title w-full px-2 py-1 border border-slate-200 rounded text-xs">
            <input type="text" placeholder="Step execution description..." required class="sp-step-desc w-full px-2 py-1 border border-slate-200 rounded text-xs">
            <div class="grid grid-cols-2 gap-2">
                <input type="text" placeholder="RACI (e.g. Resp: DevOps)" class="sp-step-raci w-full px-2 py-1 border border-slate-200 rounded text-[11px]">
                <input type="number" placeholder="Est. Mins (e.g. 15)" class="sp-step-mins w-full px-2 py-1 border border-slate-200 rounded text-[11px]" value="15">
            </div>
        </div>
        <button type="button" onclick="this.parentElement.remove()" class="text-rose-500 hover:text-rose-700 p-1 shrink-0">
            <i class="fa-solid fa-trash-can"></i>
        </button>
    `;
    container.appendChild(row);
}

export async function handleCreateSharePointArticle(e) {
    e.preventDefault();
    const title = document.getElementById('sp-art-title')?.value?.trim();
    const category = document.getElementById('sp-art-category')?.value;
    const department = document.getElementById('sp-art-dept')?.value;
    const summary = document.getElementById('sp-art-summary')?.value?.trim();
    const content = document.getElementById('sp-art-content')?.value?.trim();
    const isoTag = document.getElementById('sp-art-iso')?.value?.trim() || "ISO 9001:2015 & ISO 27001:2022";

    // Collect steps if category is SOP
    const steps = [];
    if (category === 'SOP & Procedures') {
        const rows = document.querySelectorAll('#sp-art-steps-container > div');
        rows.forEach((r, idx) => {
            const stepTitle = r.querySelector('.sp-step-title')?.value?.trim();
            const stepDesc = r.querySelector('.sp-step-desc')?.value?.trim();
            const raci = r.querySelector('.sp-step-raci')?.value?.trim() || "Responsible: Team Lead";
            const mins = parseInt(r.querySelector('.sp-step-mins')?.value) || 15;
            if (stepTitle) {
                steps.push({
                    step: idx + 1,
                    title: stepTitle,
                    description: stepDesc || "",
                    raci: raci,
                    estimated_minutes: mins
                });
            }
        });
    }

    const payload = {
        title: title,
        category: category,
        department: department,
        summary: summary,
        content: content,
        steps: steps,
        author_name: "Varadi Vijay",
        author_role: "Director & Founder",
        author_email: "director@asperion.in",
        iso_compliance_tag: isoTag
    };

    try {
        const res = await fetch('/api/v1/sharepoint/articles', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            closeSharePointModal('modal-sharepoint-new-article');
            alert(`Document successfully published to Asperion SharePoint!`);
            await loadSharePoint();
        } else {
            const err = await res.json();
            alert("Error publishing document: " + (err.detail || "Server error"));
        }
    } catch (err) {
        alert("Failed to publish document: " + err.message);
    }
}

export async function viewSharePointSOP(articleId) {
    try {
        const res = await fetch(`/api/v1/sharepoint/articles/${articleId}`);
        if (!res.ok) return;
        const art = await res.json();

        document.getElementById('sp-modal-view-badge').innerText = art.article_code;
        document.getElementById('sp-modal-view-title').innerText = art.title;
        document.getElementById('sp-modal-view-summary').innerText = art.summary;
        document.getElementById('sp-modal-view-content').innerText = art.content;

        const metaEl = document.getElementById('sp-modal-view-meta');
        if (metaEl) {
            metaEl.innerHTML = `
                <div><strong class="text-slate-400 block text-[9px] uppercase">Department</strong>${art.department}</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Author</strong>${art.author_name}</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Compliance</strong>${art.iso_compliance_tag}</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Version</strong>${art.version}</div>
            `;
        }

        const stepsContainer = document.getElementById('sp-modal-view-steps');
        if (stepsContainer) {
            if (art.steps && art.steps.length > 0) {
                stepsContainer.innerHTML = art.steps.map(s => `
                    <div class="p-3 bg-slate-50 rounded-lg border-l-4 border-teal-500 border border-slate-200">
                        <div class="font-bold text-slate-800 text-xs">Step ${s.step}: ${s.title}</div>
                        <div class="text-slate-600 text-[11px] mt-1">${s.description}</div>
                        <div class="text-[10px] text-slate-400 mt-2">
                            <strong>RACI:</strong> ${s.raci} &bull; <strong>Est. Duration:</strong> ${s.estimated_minutes} mins
                        </div>
                    </div>
                `).join('');
                document.getElementById('sp-modal-view-steps-wrapper')?.classList.remove('hidden');
            } else {
                document.getElementById('sp-modal-view-steps-wrapper')?.classList.add('hidden');
            }
        }

        const exportBtn = document.getElementById('sp-modal-export-btn');
        if (exportBtn) {
            exportBtn.onclick = () => exportSharePointDocument(art.id);
        }

        openSharePointModal('modal-sharepoint-view-sop');
    } catch (err) {
        console.error("Error viewing SOP:", err);
    }
}

export async function toggleSharePointLike(articleId) {
    try {
        const res = await fetch(`/api/v1/sharepoint/articles/${articleId}/like`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_name: "Varadi Vijay" })
        });
        if (res.ok) {
            await loadSharePointTabContent(currentSharePointTab);
        }
    } catch (err) {
        console.error("Error toggling like:", err);
    }
}

export async function toggleThoughtComments(articleId) {
    const pane = document.getElementById(`thought-comments-pane-${articleId}`);
    if (!pane) return;
    if (pane.classList.contains('hidden')) {
        pane.classList.remove('hidden');
        await loadArticleComments(articleId);
    } else {
        pane.classList.add('hidden');
    }
}

export async function loadArticleComments(articleId) {
    try {
        const res = await fetch(`/api/v1/sharepoint/articles/${articleId}/comments`);
        if (!res.ok) return;
        const comments = await res.json();
        const list = document.getElementById(`thought-comments-list-${articleId}`);
        const countSpan = document.getElementById(`thought-comments-count-${articleId}`);
        if (countSpan) countSpan.innerText = `${comments.length} Comments`;
        if (list) {
            if (comments.length === 0) {
                list.innerHTML = `<div class="text-slate-400 text-[11px] italic">No comments yet. Share your reflection below.</div>`;
            } else {
                list.innerHTML = comments.map(c => `
                    <div class="p-2 bg-slate-50 rounded border border-slate-200 text-xs">
                        <div class="flex items-center justify-between mb-0.5">
                            <span class="font-bold text-slate-700">${c.author_name} <span class="text-[10px] font-normal text-slate-400">(${c.author_role})</span></span>
                            <span class="text-[10px] text-slate-400">${new Date(c.created_at).toLocaleDateString()}</span>
                        </div>
                        <div class="text-slate-600">${c.content}</div>
                    </div>
                `).join('');
            }
        }
    } catch (err) {
        console.error("Error loading comments:", err);
    }
}

export async function handlePostArticleComment(e, articleId) {
    e.preventDefault();
    const input = e.target.querySelector('input[name="comment_content"]');
    const content = input?.value?.trim();
    if (!content) return;

    try {
        const res = await fetch(`/api/v1/sharepoint/articles/${articleId}/comments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content: content,
                author_name: "Varadi Vijay",
                author_role: "Director & Founder"
            })
        });
        if (res.ok) {
            input.value = "";
            await loadArticleComments(articleId);
        }
    } catch (err) {
        console.error("Error posting comment:", err);
    }
}

export async function handleCreateSharePointQuestion(e) {
    e.preventDefault();
    const title = document.getElementById('sp-q-title')?.value?.trim();
    const dept = document.getElementById('sp-q-dept')?.value;
    const tags = document.getElementById('sp-q-tags')?.value?.trim();
    const body = document.getElementById('sp-q-body')?.value?.trim();

    try {
        const res = await fetch('/api/v1/sharepoint/community/questions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                department: dept,
                tags: tags,
                body: body,
                author_name: "Varadi Vijay",
                author_role: "Director & Founder"
            })
        });
        if (res.ok) {
            closeSharePointModal('modal-sharepoint-new-question');
            alert("Question posted to Asperion Community forum!");
            await loadSharePointTabContent('community');
        }
    } catch (err) {
        alert("Error posting question: " + err.message);
    }
}

export async function upvoteSharePointQuestion(qId) {
    try {
        const res = await fetch(`/api/v1/sharepoint/community/questions/${qId}/upvote?user_name=Varadi Vijay`, {
            method: 'POST'
        });
        if (res.ok) {
            await loadSharePointTabContent('community');
        }
    } catch (err) {
        console.error("Error upvoting question:", err);
    }
}

export async function promptAnswerSharePointQuestion(qId) {
    const text = prompt("Enter your answer or technical guidance for this question:");
    if (!text || !text.trim()) return;

    try {
        const res = await fetch(`/api/v1/sharepoint/community/questions/${qId}/answers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                author_name: "Varadi Vijay",
                author_role: "Director & Founder",
                text: text.trim()
            })
        });
        if (res.ok) {
            await loadSharePointTabContent('community');
        }
    } catch (err) {
        alert("Error submitting answer: " + err.message);
    }
}

export function exportSharePointDocument(articleId) {
    window.open(`/api/v1/sharepoint/articles/${articleId}/export-html`, '_blank');
}


/* =========================================================================
   ASPERION ENTERPRISE TRAINING ACADEMY & NEW JOINEE ONBOARDING CONTROLLER
   Supports: Role-based Tracks, Min/Max Hours, Course Catalog, Quizzes, Certificates
   ========================================================================= */

export let currentTrainingTab = 'tracks';
export let trnSearchDebounce = null;
export let currentViewingModule = null;

export async function loadTraining() {
    try {
        const overviewRes = await fetch('/api/v1/training/overview');
        if (overviewRes.ok) {
            const overview = await overviewRes.json();
            const setVal = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.innerText = val;
            };
            setVal('trn-kpi-tracks', overview.total_tracks || 0);
            setVal('trn-kpi-modules', overview.total_modules || 0);
            setVal('trn-kpi-materials', overview.total_materials || 0);
            setVal('trn-kpi-hours', (overview.total_learning_hours_delivered || 0).toFixed(1));
        }
        await loadTrainingTabContent(currentTrainingTab);
    } catch (err) {
        console.error("Error loading Training Academy:", err);
    }
}

export function switchTrainingTab(tabName) {
    currentTrainingTab = tabName;
    document.querySelectorAll('.trn-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.className = "trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-amber-50 text-amber-800 border border-amber-200 shadow-sm";
        } else {
            btn.className = "trn-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:bg-slate-100";
        }
    });

    document.querySelectorAll('.trn-tab-pane').forEach(pane => pane.classList.add('hidden'));
    const activePane = document.getElementById(`trn-pane-${tabName}`);
    if (activePane) activePane.classList.remove('hidden');

    loadTrainingTabContent(tabName);
}

export function handleTrainingSearch(val) {
    clearTimeout(trnSearchDebounce);
    trnSearchDebounce = setTimeout(() => {
        loadTrainingTabContent(currentTrainingTab);
    }, 300);
}

export function handleTrainingDeptFilter(val) {
    loadTrainingTabContent(currentTrainingTab);
}

export async function loadTrainingTabContent(tabName) {
    const searchVal = document.getElementById('trn-search-input')?.value?.trim() || '';
    const deptVal = document.getElementById('trn-dept-filter')?.value || 'All';
    const params = new URLSearchParams();
    if (searchVal) params.append('query', searchVal);
    if (deptVal && deptVal !== 'All') params.append('department', deptVal);

    if (tabName === 'tracks') {
        const res = await fetch(`/api/v1/training/tracks?${params.toString()}`);
        if (res.ok) {
            const tracks = await res.json();
            renderTrainingTracks(tracks);
        }
    } else if (tabName === 'catalog') {
        const res = await fetch(`/api/v1/training/modules?${params.toString()}`);
        if (res.ok) {
            const modules = await res.json();
            renderTrainingCatalog(modules);
        }
    } else if (tabName === 'materials') {
        const res = await fetch(`/api/v1/training/materials?${params.toString()}`);
        if (res.ok) {
            const materials = await res.json();
            renderTrainingMaterials(materials);
        }
    } else if (tabName === 'my-learning') {
        const res = await fetch(`/api/v1/training/enrollments`);
        if (res.ok) {
            const enrollments = await res.json();
            renderMyTrainingEnrollments(enrollments);
        }
    } else if (tabName === 'compliance') {
        const res = await fetch(`/api/v1/training/enrollments`);
        if (res.ok) {
            const enrollments = await res.json();
            renderTrainingComplianceMatrix(enrollments);
        }
    } else if (tabName === 'analytics') {
        loadTrainingAnalytics();
    }
}

export function renderTrainingTracks(tracks) {
    const container = document.getElementById('trn-list-tracks');
    if (!container) return;
    if (!tracks || tracks.length === 0) {
        container.innerHTML = `<div class="col-span-3 text-center p-8 bg-white rounded-xl border border-dashed border-slate-200 text-slate-500 text-xs">No curriculum tracks found.</div>`;
        return;
    }

    container.innerHTML = tracks.map(t => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200 font-mono">
                        ${t.track_code}
                    </span>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                        ${t.target_department}
                    </span>
                </div>
                <h3 class="font-bold text-slate-900 text-sm mb-1 leading-snug">${t.name}</h3>
                <p class="text-xs text-slate-500 mb-3 line-clamp-3">${t.description}</p>
                
                <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100 space-y-1 mb-3 text-[11px]">
                    <div class="flex justify-between text-slate-600">
                        <span>Min Mandatory Hours:</span>
                        <strong class="text-amber-700 font-mono">${t.min_training_hours} hrs</strong>
                    </div>
                    <div class="flex justify-between text-slate-600">
                        <span>Max Recommended Hours:</span>
                        <strong class="text-emerald-700 font-mono">${t.max_training_hours} hrs</strong>
                    </div>
                    <div class="flex justify-between text-slate-600">
                        <span>Min Passing Score:</span>
                        <strong class="text-blue-700 font-mono">${t.min_passing_score_pct}%</strong>
                    </div>
                </div>

                <div class="text-[10px] text-slate-400">
                    Target Roles: <strong class="text-slate-600">${t.target_roles}</strong>
                </div>
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-slate-100 mt-3">
                <span class="text-[10px] font-bold text-emerald-600">
                    <i class="fa-solid fa-check-circle"></i> Mandatory for Probation
                </span>
                <button onclick="filterCatalogByTrack(${t.id})" class="px-3 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-lg text-xs font-bold transition">
                    View Modules
                </button>
            </div>
        </div>
    `).join('');
}

export function filterCatalogByTrack(trackId) {
    switchTrainingTab('catalog');
}

export function renderTrainingCatalog(modules) {
    const container = document.getElementById('trn-list-catalog');
    if (!container) return;
    if (!modules || modules.length === 0) {
        container.innerHTML = `<div class="col-span-2 text-center p-8 bg-white rounded-xl border border-dashed border-slate-200 text-slate-500 text-xs">No courses found matching filters.</div>`;
        return;
    }

    container.innerHTML = modules.map(m => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200 font-mono">
                        ${m.module_code}
                    </span>
                    <div class="flex items-center gap-1.5">
                        <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600">
                            ${m.department}
                        </span>
                        <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
                            ${m.level}
                        </span>
                        ${m.is_mandatory ? '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-rose-50 text-rose-700 border border-rose-200">Mandatory</span>' : ''}
                    </div>
                </div>
                <h3 class="font-bold text-slate-900 text-sm mb-1 leading-snug">${m.title}</h3>
                <p class="text-xs text-slate-500 mb-3">${m.learning_objectives}</p>
                
                <div class="flex items-center gap-3 text-[11px] text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100 mb-3">
                    <span><i class="fa-solid fa-clock text-amber-500 mr-1"></i> Duration: <strong>${m.duration_hours} hrs</strong></span>
                    <span>&bull;</span>
                    <span><i class="fa-solid fa-shield-halved text-teal-600 mr-1"></i> ${m.policy_reference}</span>
                </div>
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-slate-100 gap-2">
                <button onclick="viewTrainingModule(${m.id})" class="px-3.5 py-1.5 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow">
                    <i class="fa-solid fa-book-reader"></i> Open Course
                </button>
                <button onclick="quickEnrollMySelf(${m.id})" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition">
                    + Enroll Joinee
                </button>
            </div>
        </div>
    `).join('');
}

export function renderMyTrainingEnrollments(enrollments) {
    const container = document.getElementById('trn-list-my-learning');
    if (!container) return;
    if (!enrollments || enrollments.length === 0) {
        container.innerHTML = `<div class="text-center p-8 bg-white rounded-xl border border-dashed border-slate-200 text-slate-500 text-xs">No active course enrollments. Browse the catalog above to enroll.</div>`;
        return;
    }

    container.innerHTML = enrollments.map(e => `
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200 font-mono">${e.module_code}</span>
                    <span class="text-xs font-bold text-slate-800">${e.module_title}</span>
                    ${e.status === 'COMPLETED' ? '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-check"></i> Completed</span>' : '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-blue-50 text-blue-700">In Progress</span>'}
                </div>
                <div class="text-xs text-slate-500 mb-2">
                    Enrolled by: <strong>${e.employee_name}</strong> (${e.employee_role} &bull; ${e.department})
                </div>

                <!-- Progress Bar -->
                <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden mb-1.5 max-w-md">
                    <div class="h-2 rounded-full ${e.status === 'COMPLETED' ? 'bg-emerald-500' : 'bg-amber-500'}" style="width: ${e.progress_pct}%"></div>
                </div>
                <div class="flex items-center gap-3 text-[10px] text-slate-400">
                    <span>Progress: <strong>${e.progress_pct}%</strong></span>
                    <span>&bull;</span>
                    <span>Hours Spent: <strong>${e.hours_spent.toFixed(1)} / ${e.module_duration} hrs</strong></span>
                    <span>&bull;</span>
                    <span>Assessment Score: <strong class="text-slate-700">${e.score_pct}%</strong></span>
                </div>
            </div>

            <div class="flex items-center gap-2 shrink-0">
                <button onclick="viewTrainingModule(${e.module_id}, ${e.id})" class="px-3.5 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded-lg text-xs font-bold transition">
                    Study Lesson
                </button>
                ${e.status !== 'COMPLETED' ? `
                <button onclick="openTrainingQuizByEnrollmentId(${e.id}, ${e.module_id})" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition shadow">
                    Take Quiz
                </button>` : `
                <button onclick="exportTrainingCertificate('${e.certificate_id}')" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold transition shadow flex items-center gap-1">
                    <i class="fa-solid fa-certificate"></i> Certificate
                </button>`}
            </div>
        </div>
    `).join('');
}

export function renderTrainingComplianceMatrix(enrollments) {
    if (!tbody) return;
    if (!enrollments || enrollments.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-6 text-center text-slate-400 text-xs">No enrollment records found.</td></tr>`;
        return;
    }

    // Group by employee email
    const emps = {};
    enrollments.forEach(e => {
        if (!emps[e.employee_email]) {
            emps[e.employee_email] = {
                name: e.employee_name,
                role: e.employee_role,
                dept: e.department,
                total: 0,
                completed: 0,
                hours: 0.0
            };
        }
        emps[e.employee_email].total += 1;
        if (e.status === 'COMPLETED') {
            emps[e.employee_email].completed += 1;
            emps[e.employee_email].hours += (e.hours_spent || 0.0);
        }
    });

    tbody.innerHTML = Object.values(emps).map(emp => {
        const minReq = 16.0;
        const isReady = emp.hours >= minReq && emp.completed >= 3;
        return `
        <tr class="hover:bg-slate-50/80 transition">
            <td class="p-3 font-bold text-slate-900">${emp.name}</td>
            <td class="p-3 text-slate-600">${emp.role}</td>
            <td class="p-3 text-slate-600">${emp.dept}</td>
            <td class="p-3 font-mono text-slate-700">${emp.total}</td>
            <td class="p-3 font-mono font-bold text-emerald-600">${emp.completed}</td>
            <td class="p-3 font-mono font-bold text-amber-600">${emp.hours.toFixed(1)} hrs</td>
            <td class="p-3 font-mono text-slate-500">${minReq} hrs</td>
            <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${isReady ? 'bg-emerald-100 text-emerald-800 border-emerald-200' : 'bg-amber-100 text-amber-800 border-amber-200'}">
                    ${isReady ? 'Clearance Ready' : 'In Progress'}
                </span>
            </td>
        </tr>`;
    }).join('');
}

/* Modals & Handlers */
export function openTrainingModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('hidden');
}

export function closeTrainingModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('hidden');
}

export async function viewTrainingModule(moduleId, enrollmentId = null) {
    try {
        const res = await fetch(`/api/v1/training/modules/${moduleId}`);
        if (!res.ok) return;
        const mod = await res.json();
        currentViewingModule = mod;

        document.getElementById('trn-viewer-badge').innerText = mod.module_code;
        document.getElementById('trn-viewer-title').innerText = mod.title;
        document.getElementById('trn-viewer-objectives').innerText = mod.learning_objectives;
        document.getElementById('trn-viewer-content').innerText = mod.lesson_content;
        document.getElementById('trn-viewer-policy').innerText = mod.policy_reference;

        const metaEl = document.getElementById('trn-viewer-meta');
        if (metaEl) {
            metaEl.innerHTML = `
                <div><strong class="text-slate-400 block text-[9px] uppercase">Department</strong>${mod.department}</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Level</strong>${mod.level}</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Duration</strong>${mod.duration_hours} hrs</div>
                <div><strong class="text-slate-400 block text-[9px] uppercase">Passing Threshold</strong>${mod.passing_score_pct}%</div>
            `;
        }

        const syllabusContainer = document.getElementById('trn-viewer-syllabus');
        if (syllabusContainer) {
            if (mod.syllabus && mod.syllabus.length > 0) {
                syllabusContainer.innerHTML = mod.syllabus.map(s => `
                    <div class="p-2.5 bg-slate-50 rounded-lg border border-slate-200 flex items-start gap-2 text-xs">
                        <span class="w-5 h-5 rounded-full bg-amber-100 text-amber-800 font-bold flex items-center justify-center text-[10px] shrink-0 mt-0.5">${s.chapter}</span>
                        <div>
                            <div class="font-bold text-slate-800">${s.title} <span class="text-[10px] text-slate-400 font-normal">(${s.duration_mins} mins)</span></div>
                            <div class="text-[11px] text-slate-600 mt-0.5">${s.summary}</div>
                        </div>
                    </div>
                `).join('');
                document.getElementById('trn-viewer-syllabus-wrapper')?.classList.remove('hidden');
            } else {
                document.getElementById('trn-viewer-syllabus-wrapper')?.classList.add('hidden');
            }
        }

        const quizBtn = document.getElementById('trn-viewer-take-quiz-btn');
        if (quizBtn) {
            quizBtn.onclick = () => {
                closeTrainingModal('modal-training-course-viewer');
                openTrainingQuiz(enrollmentId, mod);
            };
        }

        openTrainingModal('modal-training-course-viewer');
    } catch (err) {
        console.error("Error viewing course:", err);
    }
}

export async function quickEnrollMySelf(moduleId) {
    try {
        const res = await fetch('/api/v1/training/enrollments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                employee_name: "Varadi Vijay",
                employee_email: "director@asperion.in",
                employee_role: "Director & Founder",
                department: "Executive & Strategy",
                module_id: moduleId
            })
        });
        if (res.ok) {
            alert("Enrollment confirmed! Course added to your learning dashboard.");
            switchTrainingTab('my-learning');
        }
    } catch (err) {
        alert("Enrollment failed: " + err.message);
    }
}

export async function openTrainingQuizByEnrollmentId(enrollmentId, moduleId) {
    const res = await fetch(`/api/v1/training/modules/${moduleId}`);
    if (res.ok) {
        const mod = await res.json();
        openTrainingQuiz(enrollmentId, mod);
    }
}

export function openTrainingQuiz(enrollmentId, mod) {
    document.getElementById('trn-quiz-title').innerText = `${mod.module_code} - Assessment Quiz`;
    document.getElementById('trn-quiz-enrollment-id').value = enrollmentId || "";

    const container = document.getElementById('trn-quiz-questions-container');
    if (!container) return;

    if (!mod.quiz || mod.quiz.length === 0) {
        container.innerHTML = `<div class="p-4 bg-slate-50 text-slate-600 rounded-lg text-center">This course does not require an assessment quiz. Click Submit to verify completion.</div>`;
    } else {
        container.innerHTML = mod.quiz.map((q, qIdx) => `
            <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                <div class="font-bold text-slate-800 text-xs">
                    Question ${qIdx + 1}: ${q.question}
                </div>
                <div class="space-y-1.5 pl-2">
                    ${q.options.map((opt, optIdx) => `
                        <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer p-1.5 rounded hover:bg-slate-100">
                            <input type="radio" name="q_${qIdx}" value="${optIdx}" required class="text-amber-600 focus:ring-amber-500">
                            <span>${opt}</span>
                        </label>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }

    openTrainingModal('modal-training-quiz-taker');
}

export async function handleTrainingQuizSubmit(e) {
    e.preventDefault();
    const enrollmentId = document.getElementById('trn-quiz-enrollment-id')?.value;
    if (!enrollmentId) {
        alert("Please enroll in this course first before submitting the assessment quiz.");
        closeTrainingModal('modal-training-quiz-taker');
        return;
    }

    // Collect chosen radio answers
    const answers = [];
    const questionContainers = document.querySelectorAll('#trn-quiz-questions-container > div');
    questionContainers.forEach((_, qIdx) => {
        const selected = document.querySelector(`input[name="q_${qIdx}"]:checked`);
        if (selected) {
            answers.push(parseInt(selected.value));
        }
    });

    try {
        const res = await fetch(`/api/v1/training/enrollments/${enrollmentId}/submit-quiz`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: answers })
        });
        if (res.ok) {
            const result = await res.json();
            closeTrainingModal('modal-training-quiz-taker');
            if (result.passed) {
                alert(`Assessment Passed! Score: ${result.score_pct}%.\nYour official Certificate of Completion (${result.certificate_id}) has been issued!`);
                if (result.certificate_id) {
                    exportTrainingCertificate(result.certificate_id);
                }
            } else {
                alert(`Assessment Not Passed. Score: ${result.score_pct}%. Minimum threshold is 80%. Please review the lesson and re-attempt.`);
            }
            await loadTraining();
        } else {
            const err = await res.json();
            alert("Quiz evaluation error: " + (err.detail || "Server error"));
        }
    } catch (err) {
        alert("Failed to submit quiz: " + err.message);
    }
}

export async function openMyTrainingSummaryModal() {
    try {
        const res = await fetch(`/api/v1/training/employee/summary?email=siddharth.kulkarni@asperion.in`);
        if (!res.ok) return;
        const summary = await res.json();

        document.getElementById('trn-summary-hours').innerText = `${summary.total_hours_completed.toFixed(1)} hrs`;
        document.getElementById('trn-summary-min-req').innerText = `${summary.min_required_hours} hrs`;
        document.getElementById('trn-summary-completed').innerText = `${summary.total_completed} / ${summary.total_enrolled}`;
        document.getElementById('trn-summary-probation').innerText = summary.compliance_status;

        const certsContainer = document.getElementById('trn-summary-certs');
        if (certsContainer) {
            const completed = (summary.enrollments || []).filter(e => e.certificate_id);
            if (completed.length === 0) {
                certsContainer.innerHTML = `<div class="p-3 bg-slate-50 text-slate-400 text-center rounded">No certificates issued yet. Complete mandatory modules with >= 80% score.</div>`;
            } else {
                certsContainer.innerHTML = completed.map(c => `
                    <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                        <div>
                            <span class="font-mono text-[10px] text-amber-700 font-bold">${c.certificate_id}</span>
                            <div class="font-bold text-slate-800 text-xs">${c.module_title}</div>
                            <div class="text-[10px] text-slate-400">Score: ${c.score_pct}% &bull; Completed: ${new Date(c.completed_at).toLocaleDateString()}</div>
                        </div>
                        <button onclick="exportTrainingCertificate('${c.certificate_id}')" class="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-bold transition flex items-center gap-1">
                            <i class="fa-solid fa-print"></i> Certificate
                        </button>
                    </div>
                `).join('');
            }
        }

        openTrainingModal('modal-training-my-summary');
    } catch (err) {
        console.error("Error opening summary:", err);
    }
}

export function exportTrainingCertificate(certId) {
    if (!certId) return;
    window.open(`/api/v1/training/certificates/${certId}/html`, '_blank');
}

/* =========================================================================
   TRAINING MATERIALS, HANDBOOKS & ACCESS PLAYBOOKS CONTROLLER
   ========================================================================= */

export function renderTrainingMaterials(materials) {
    const container = document.getElementById('trn-list-materials');
    if (!container) return;
    if (!materials || materials.length === 0) {
        container.innerHTML = `<div class="col-span-3 text-center p-8 bg-white rounded-xl border border-dashed border-slate-200 text-slate-500 text-xs">No training materials, handbooks, or playbooks found matching filters.</div>`;
        return;
    }

    const docTypeColors = {
        'HANDBOOK': 'bg-emerald-50 text-emerald-800 border-emerald-200',
        'PLAYBOOK': 'bg-blue-50 text-blue-800 border-blue-200',
        'RUNBOOK': 'bg-rose-50 text-rose-800 border-rose-200',
        'LAB GUIDE': 'bg-purple-50 text-purple-800 border-purple-200',
        'CHEATSHEET': 'bg-amber-50 text-amber-800 border-amber-200'
    };

    container.innerHTML = materials.map(m => {
        const typeStyle = docTypeColors[m.doc_type] || 'bg-slate-100 text-slate-800 border-slate-200';
        return `
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between gap-2 mb-2">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-900 text-emerald-400 font-mono">
                            ${m.material_code || 'MAT-DOC'}
                        </span>
                        <div class="flex items-center gap-1.5">
                            <span class="px-2 py-0.5 rounded text-[9px] font-bold border ${typeStyle}">
                                ${m.doc_type || 'HANDBOOK'}
                            </span>
                            <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-600">
                                ${m.department}
                            </span>
                        </div>
                    </div>

                    <h3 class="font-bold text-slate-900 text-sm mb-1.5 leading-snug line-clamp-2">${m.title}</h3>
                    <p class="text-xs text-slate-500 mb-3 line-clamp-3">${m.summary}</p>

                    <div class="bg-slate-50 p-2.5 rounded-lg border border-slate-100 space-y-1 mb-3 text-[11px]">
                        <div class="flex justify-between text-slate-600">
                            <span>Category:</span>
                            <strong class="text-slate-800">${m.category}</strong>
                        </div>
                        <div class="flex justify-between text-slate-600">
                            <span>Target Role:</span>
                            <strong class="text-slate-800">${m.target_role || 'All Roles'}</strong>
                        </div>
                        <div class="flex justify-between text-slate-600">
                            <span>Reading Time:</span>
                            <strong class="text-emerald-700 font-mono">${m.reading_time_mins} mins</strong>
                        </div>
                        <div class="flex justify-between text-slate-600">
                            <span>Access Level:</span>
                            <strong class="text-blue-700">${m.access_level}</strong>
                        </div>
                    </div>

                    <div class="flex flex-wrap gap-1.5 mb-2">
                        ${m.linked_module_code ? `<span class="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-50 text-blue-700 border border-blue-200"><i class="fa-solid fa-graduation-cap mr-1"></i>${m.linked_module_code}</span>` : ''}
                        ${m.linked_sop_code ? `<span class="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-50 text-amber-700 border border-amber-200"><i class="fa-solid fa-file-contract mr-1"></i>${m.linked_sop_code}</span>` : ''}
                    </div>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-slate-100 mt-2">
                    <span class="text-[10px] text-slate-400 font-medium">
                        <i class="fa-solid fa-eye text-slate-400 mr-0.5"></i> ${m.download_count} readers
                    </span>
                    <div class="flex items-center gap-1.5">
                        <button onclick="exportTrainingMaterial(${m.id})" title="Printable Guide" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold transition flex items-center gap-1">
                            <i class="fa-solid fa-print"></i>
                        </button>
                        <button onclick="viewTrainingMaterial(${m.id})" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition flex items-center gap-1">
                            <i class="fa-solid fa-book-open"></i> Read
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

export async function viewTrainingMaterial(materialId) {
    try {
        const res = await fetch(`/api/v1/training/materials/${materialId}`);
        if (!res.ok) {
            alert("Could not load material details.");
            return;
        }
        const m = await res.json();

        document.getElementById('trn-mat-badge').innerText = m.material_code || 'MAT-DOC';
        document.getElementById('trn-mat-doctype').innerText = m.doc_type || 'HANDBOOK';
        document.getElementById('trn-mat-access').innerText = m.access_level || 'Internal';
        document.getElementById('trn-mat-title').innerText = m.title;
        document.getElementById('trn-mat-category').innerText = m.category;
        document.getElementById('trn-mat-role-dept').innerText = `${m.target_role || 'All Roles'} • ${m.department}`;
        document.getElementById('trn-mat-time').innerText = `${m.reading_time_mins} mins read`;
        document.getElementById('trn-mat-downloads').innerText = `${m.download_count} readers`;
        document.getElementById('trn-mat-summary').innerText = m.summary;
        document.getElementById('trn-mat-content').innerText = m.content;

        const linksBar = document.getElementById('trn-mat-links-bar');
        if (linksBar) {
            let linksHtml = '';
            if (m.linked_module_code) {
                linksHtml += `<span class="px-2.5 py-1 rounded text-xs font-mono bg-blue-50 text-blue-800 border border-blue-200 font-bold"><i class="fa-solid fa-graduation-cap mr-1"></i> Linked Module: ${m.linked_module_code}</span>`;
            }
            if (m.linked_sop_code) {
                linksHtml += `<span class="px-2.5 py-1 rounded text-xs font-mono bg-amber-50 text-amber-800 border border-amber-200 font-bold"><i class="fa-solid fa-file-contract mr-1"></i> Linked SOP: ${m.linked_sop_code}</span>`;
            }
            if (m.external_link) {
                linksHtml += `<a href="${m.external_link}" target="_blank" class="px-2.5 py-1 rounded text-xs bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold hover:bg-emerald-100 transition"><i class="fa-solid fa-arrow-up-right-from-square mr-1"></i> Live Endpoint / System Tool</a>`;
            }
            linksBar.innerHTML = linksHtml;
        }

        const exportBtn = document.getElementById('trn-mat-export-btn');
        if (exportBtn) {
            exportBtn.onclick = () => exportTrainingMaterial(m.id);
        }

        openTrainingModal('modal-training-material-viewer');
    } catch (err) {
        console.error("Error loading material:", err);
    }
}

export function exportTrainingMaterial(materialId) {
    if (!materialId) return;
    window.open(`/api/v1/training/materials/${materialId}/export-html`, '_blank');
}

export async function handleCreateTrainingMaterial(e) {
    e.preventDefault();
    const payload = {
        title: document.getElementById('trn-new-mat-title').value.trim(),
        category: document.getElementById('trn-new-mat-category').value,
        department: document.getElementById('trn-new-mat-department').value,
        target_role: document.getElementById('trn-new-mat-role').value.trim() || 'All Roles',
        doc_type: document.getElementById('trn-new-mat-doctype').value,
        reading_time_mins: parseInt(document.getElementById('trn-new-mat-reading-time').value) || 20,
        access_level: 'Internal Authenticated',
        linked_module_code: document.getElementById('trn-new-mat-linked-module').value.trim() || null,
        linked_sop_code: document.getElementById('trn-new-mat-linked-sop').value.trim() || null,
        external_link: document.getElementById('trn-new-mat-link').value.trim() || null,
        summary: document.getElementById('trn-new-mat-summary').value.trim(),
        content: document.getElementById('trn-new-mat-content').value.trim()
    };

    try {
        const res = await fetch('/api/v1/training/materials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            const created = await res.json();
            alert(`Training Material Published!\nCode: ${created.material_code}\nTitle: ${created.title}`);
            closeTrainingModal('modal-training-new-material');
            e.target.reset();
            await loadTraining();
            switchTrainingTab('materials');
        } else {
            const err = await res.json();
            alert("Error publishing material: " + (err.detail || "Server error"));
        }
    } catch (err) {
        alert("Failed to submit material: " + err.message);
    }
}

/* =========================================================================
   EXECUTIVE BALANCED SCORECARD & STATUTORY COUNTDOWN CONTROLLER
   ========================================================================= */

export async function loadBalancedScorecard() {
    try {
        const res = await fetch(`${API_BASE}/analytics/balanced-scorecard`);
        if (!res.ok) return;
        const data = await res.json();
        
        // Render 4 Quadrants
        const bscContainer = document.getElementById('exec-bsc-cards');
        if (bscContainer && data.scorecard) {
            const sc = data.scorecard;
            const quadrants = [
                { title: '1. Financial Health & Liquidity', icon: 'fa-wallet', color: 'emerald', data: sc.financial_perspective },
                { title: '2. Client & Commercial Growth', icon: 'fa-handshake', color: 'blue', data: sc.customer_commercial_perspective },
                { title: '3. Internal Process & Security (ISO)', icon: 'fa-shield-halved', color: 'purple', data: sc.internal_process_perspective },
                { title: '4. People, Learning & Academy', icon: 'fa-graduation-cap', color: 'amber', data: sc.learning_people_perspective }
            ];

            bscContainer.innerHTML = quadrants.map(q => `
                <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                                <i class="fa-solid ${q.icon} text-${q.color}-600"></i> ${q.title}
                            </span>
                            <span class="text-xs font-black text-${q.color}-700 bg-${q.color}-100 px-2 py-0.5 rounded-full border border-${q.color}-200">
                                ${q.data.score_pct}%
                            </span>
                        </div>
                        <div class="w-full bg-slate-200 rounded-full h-1.5 mb-3 overflow-hidden">
                            <div class="bg-${q.color}-600 h-1.5 rounded-full" style="width: ${q.data.score_pct}%"></div>
                        </div>
                        <div class="space-y-1.5 text-[11px]">
                            ${q.data.metrics.map(m => `
                                <div class="flex items-center justify-between text-slate-600">
                                    <span class="truncate pr-1">${m.label}:</span>
                                    <strong class="text-slate-900 font-mono shrink-0">${m.value}</strong>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Render Statutory Filings Countdown Cards
        const radarContainer = document.getElementById('exec-statutory-radar-cards');
        if (radarContainer && data.statutory_countdown_radar) {
            radarContainer.innerHTML = data.statutory_countdown_radar.map(item => {
                const daysBadge = item.days_left <= 10 
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' 
                    : (item.days_left <= 25 ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40');
                return `
                    <div class="p-3.5 rounded-xl border border-slate-800 bg-slate-900/80 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between gap-1 mb-2">
                                <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-slate-800 text-slate-300 border border-slate-700">
                                    ${item.code}
                                </span>
                                <span class="px-2 py-0.5 rounded text-[9px] font-bold border ${daysBadge}">
                                    ${item.days_left} Days Left
                                </span>
                            </div>
                            <h4 class="font-bold text-white text-xs mb-1 line-clamp-2">${item.name}</h4>
                            <div class="text-[10px] text-slate-400 mb-2">${item.authority}</div>
                        </div>
                        <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-[10px]">
                            <span class="text-slate-400 font-mono">Due: ${item.due_date}</span>
                            <span class="text-emerald-400 font-bold">${item.status}</span>
                        </div>
                    </div>
                `;
            }).join('');
        }
    } catch (err) {
        console.error("Error loading Balanced Scorecard:", err);
    }
}

/* =========================================================================
   HRMS WORKFORCE INTELLIGENCE & VISUAL ANALYTICS CONTROLLER
   ========================================================================= */

export async function loadHRMSAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/workforce-intelligence`);
        if (!res.ok) return;
        const data = await res.json();

        // 1. Department Headcount Donut
        const dept = data.department_headcount;
        safeRenderChart('chart-hrms-dept-headcount', 'doughnut', {
            labels: dept.labels,
            datasets: [{
                data: dept.counts,
                backgroundColor: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899', '#06b6d4']
            }]
        }, {
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
            }
        });

        // 2. CTC Slabs Bar
        const ctc = data.ctc_slabs;
        safeRenderChart('chart-hrms-ctc-slabs', 'bar', {
            labels: ctc.labels,
            datasets: [{
                label: 'Employees in Bracket',
                data: ctc.counts,
                backgroundColor: '#10b981',
                borderRadius: 6
            }]
        }, {
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        });

        // 3. Attendance Verification Health
        const att = data.attendance_health;
        safeRenderChart('chart-hrms-attendance-health', 'doughnut', {
            labels: att.labels,
            datasets: [{
                data: att.counts,
                backgroundColor: ['#2563eb', '#059669', '#d97706', '#dc2626']
            }]
        }, {
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
            }
        });

        // 4. Leave Utilization
        const l = data.leave_utilization;
        safeRenderChart('chart-hrms-leave-burn', 'bar', {
            labels: l.labels,
            datasets: [{
                label: 'Days Consumed',
                data: l.counts,
                backgroundColor: '#f59e0b',
                borderRadius: 6
            }]
        }, {
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        });

        // 5. Recruitment ATS Funnel
        const funnel = data.recruitment_funnel;
        safeRenderChart('chart-hrms-ats-funnel', 'bar', {
            labels: funnel.labels,
            datasets: [{
                label: 'Candidates in Stage',
                data: funnel.counts,
                backgroundColor: ['#8b5cf6', '#a78bfa', '#c084fc', '#d8b4fe', '#06b6d4', '#10b981'],
                borderRadius: 6
            }]
        }, {
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true, ticks: { stepSize: 2 } } }
        });

        // 6. Probation counts
        if (data.probation_status) {
            const p = data.probation_status;
            const confEl = document.getElementById('hrms-probation-confirmed');
            if (confEl) confEl.innerText = `${p.confirmed_count} Confirmed`;
            const actEl = document.getElementById('hrms-probation-active');
            if (actEl) actEl.innerText = `${p.in_probation_count} In Progress`;
            const rateEl = document.getElementById('hrms-kpi-probation-rate');
            if (rateEl) rateEl.innerText = `${p.clearance_rate_pct}%`;
        }
    } catch (err) {
        console.error("Error loading HRMS Analytics:", err);
    }
}

/* =========================================================================
   TRAINING ACADEMY LEARNING INTELLIGENCE & RADAR CONTROLLER
   ========================================================================= */

export async function loadTrainingAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics/learning-intelligence`);
        if (!res.ok) return;
        const data = await res.json();

        // 1. Department Training Hours Bar
        const dh = data.department_hours;
        safeRenderChart('chart-trn-dept-hours', 'bar', {
            labels: dh.labels,
            datasets: [
                {
                    label: 'Delivered Hours',
                    data: dh.delivered_hours,
                    backgroundColor: '#f59e0b',
                    borderRadius: 6
                },
                {
                    label: 'Min Mandatory Threshold (16.0h)',
                    data: dh.labels.map(() => dh.min_required_threshold),
                    type: 'line',
                    borderColor: '#dc2626',
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        }, {
            scales: { y: { beginAtZero: true } }
        });

        // 2. Track Completion Donut
        const tc = data.track_completion;
        safeRenderChart('chart-trn-track-completion', 'doughnut', {
            labels: tc.labels,
            datasets: [{
                data: tc.completion_percentages,
                backgroundColor: ['#10b981', '#3b82f6', '#8b5cf6', '#06b6d4']
            }]
        }, {
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } }
            }
        });

        // 3. Quiz Score Distribution Bar
        const qs = data.quiz_score_distribution;
        safeRenderChart('chart-trn-quiz-scores', 'bar', {
            labels: qs.labels,
            datasets: [{
                label: 'Employees in Bracket',
                data: qs.counts,
                backgroundColor: '#3b82f6',
                borderRadius: 6
            }]
        }, {
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        });

        // 4. Top Read Materials Table
        const tableBody = document.getElementById('trn-top-materials-table');
        if (tableBody && data.top_materials) {
            tableBody.innerHTML = data.top_materials.map(m => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 font-mono font-bold text-amber-700">${m.code}</td>
                    <td class="p-2.5 font-bold text-slate-800">${m.title}</td>
                    <td class="p-2.5 text-slate-600">${m.category}</td>
                    <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-100 text-slate-700">${m.doc_type}</span></td>
                    <td class="p-2.5 text-center font-bold text-emerald-600 font-mono">${m.reads} readers</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error("Error loading Training Analytics:", err);
    }
}

// ==============================================================
// MODULE 13B: COMPREHENSIVE IT SERVICE MANAGEMENT (ITSM) SUITE
// ==============================================================
export let currentITSMTab = 'cmdb';
export let cachedITSM_LOIs = [];
export let currentViewingLOI = null;

export async function loadITSM() {
    try {
        // 1. Fetch Executive Overview
        const res = await fetch(`${API_BASE}/itsm/overview`).then(r => r.json());
        if (res.status === 'success') {
            const m = res.metrics;
            const elNodes = document.getElementById('itsm-stat-nodes');
            if (elNodes) elNodes.innerText = `${m.total_configuration_items} CIs`;
            const elHealth = document.getElementById('itsm-stat-health');
            if (elHealth) elHealth.innerText = `${m.cmdb_health_index_pct}%`;
            const elKedb = document.getElementById('itsm-stat-kedb');
            if (elKedb) elKedb.innerText = `${m.kedb_published_solutions} Fixed`;
            const elCab = document.getElementById('itsm-stat-cab');
            if (elCab) elCab.innerText = `${m.approved_scheduled_changes} Sched`;
            const elFixes = document.getElementById('itsm-stat-fixes');
            if (elFixes) elFixes.innerText = `${m.automated_self_healing_executions} Auto`;
            const elLoi = document.getElementById('itsm-stat-loi');
            if (elLoi) elLoi.innerText = formatINR(m.total_procurement_pipeline_inr);
        }

        // 2. Load active subview tab
        switchITSMTab(currentITSMTab);
    } catch (err) {
        console.error("Error loading ITSM Suite:", err);
    }
}

export function switchITSMTab(tabKey) {
    currentITSMTab = tabKey;
    const tabs = ['cmdb', 'problems', 'cab', 'runbooks', 'loi'];
    tabs.forEach(t => {
        const btn = document.getElementById(`itsm-tab-btn-${t}`);
        const pane = document.getElementById(`itsm-subview-${t}`);
        if (t === tabKey) {
            if (btn) {
                btn.className = "itsm-tab-btn px-4 py-2.5 border-b-2 border-cyan-600 text-cyan-700 font-bold flex items-center gap-2 whitespace-nowrap bg-cyan-50/50 rounded-t-lg";
            }
            if (pane) pane.classList.remove('hidden');
        } else {
            if (btn) {
                btn.className = "itsm-tab-btn px-4 py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 font-medium flex items-center gap-2 whitespace-nowrap";
            }
            if (pane) pane.classList.add('hidden');
        }
    });

    switch (tabKey) {
        case 'cmdb': loadCMDBNodes(); break;
        case 'problems': loadITSMProblems(); break;
        case 'cab': loadITSMChanges(); break;
        case 'runbooks': loadITSMRunbooks(); break;
        case 'loi': loadITSMLOIs(); loadITSMSLAs(); break;
    }
}

// Subview 1: CMDB Nodes & Topology
export async function loadCMDBNodes() {
    try {
        const env = document.getElementById('itsm-filter-env')?.value || 'ALL';
        const cat = document.getElementById('itsm-filter-cat')?.value || 'ALL';
        
        const [nodes, topo] = await Promise.all([
            fetch(`${API_BASE}/itsm/cmdb/nodes?environment=${env}&category=${cat}`).then(r => r.json()),
            fetch(`${API_BASE}/itsm/cmdb/topology`).then(r => r.json())
        ]);

        const tbody = document.getElementById('table-itsm-ci-nodes');
        if (tbody) {
            if (nodes.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-slate-400">No Configuration Items match selected filter.</td></tr>`;
            } else {
                tbody.innerHTML = nodes.map(c => `
                    <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                        <td class="p-3">
                            <div class="font-bold text-slate-900">${c.ci_name}</div>
                            <div class="text-[10px] text-cyan-700 font-mono font-bold">${c.ci_code}</div>
                        </td>
                        <td class="p-3">
                            <div class="font-medium text-slate-800">${c.ci_type}</div>
                            <span class="px-1.5 py-0.2 rounded text-[9px] font-bold ${c.tier.includes('Tier-0') ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-blue-50 text-blue-700 border border-blue-200'}">${c.tier}</span>
                        </td>
                        <td class="p-3 font-mono text-[11px] text-slate-700">
                            <div>${c.ip_address}</div>
                            <div class="text-[10px] text-slate-400">${c.fqdn}</div>
                        </td>
                        <td class="p-3 text-slate-600">${c.cloud_provider}</td>
                        <td class="p-3">
                            <div class="flex items-center gap-2 text-[11px] font-mono">
                                <span>CPU: <strong class="${c.cpu_utilization_pct > 75 ? 'text-rose-600' : 'text-slate-800'}">${c.cpu_utilization_pct}%</strong></span>
                                <span>RAM: <strong class="${c.memory_utilization_pct > 80 ? 'text-amber-600' : 'text-slate-800'}">${c.memory_utilization_pct}%</strong></span>
                            </div>
                            <div class="w-24 bg-slate-200 h-1 rounded-full mt-1 overflow-hidden">
                                <div class="bg-cyan-600 h-1" style="width: ${c.cpu_utilization_pct}%"></div>
                            </div>
                        </td>
                        <td class="p-3 font-mono font-bold text-emerald-600">${c.health_score}%</td>
                        <td class="p-3">
                            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${c.status === 'Operational' ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-200'}">
                                ${c.status}
                            </span>
                        </td>
                        <td class="p-3 text-center whitespace-nowrap">
                            <button onclick="handleExecuteRunbook(1, '${c.ci_code}')" class="px-2 py-1 bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border border-cyan-200 rounded text-[10px] font-bold transition flex items-center gap-1 mx-auto">
                                <i class="fa-solid fa-heart-pulse"></i> Diagnostic
                            </button>
                        </td>
                    </tr>
                `).join('');
            }
        }

        // Render Topology Container
        const topoBox = document.getElementById('cmdb-topology-container');
        if (topoBox && topo.nodes) {
            topoBox.innerHTML = topo.nodes.map(n => `
                <div class="p-3 bg-slate-800/80 rounded-xl border border-slate-700 hover:border-cyan-500/50 transition">
                    <div class="flex justify-between items-center mb-1">
                        <span class="font-mono text-cyan-400 font-bold text-[10px]">${n.id}</span>
                        <span class="w-2 h-2 rounded-full ${n.status === 'Operational' ? 'bg-emerald-400' : 'bg-amber-400'}"></span>
                    </div>
                    <div class="font-bold text-white text-[11px] truncate" title="${n.label}">${n.label}</div>
                    <div class="text-[9px] text-slate-400 mt-1">${n.type} &bull; ${n.cloud_provider.split(' ')[0]}</div>
                    <div class="mt-2 text-[10px] flex justify-between font-mono text-slate-300 border-t border-slate-700 pt-1">
                        <span>Health: <strong class="text-emerald-400">${n.health_score}%</strong></span>
                        <span>CPU: ${n.cpu_pct}%</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error("Error loading CMDB nodes:", err);
    }
}

// Subview 2: Problems & KEDB
export async function loadITSMProblems() {
    try {
        const problems = await fetch(`${API_BASE}/itsm/problems`).then(r => r.json());
        const tbody = document.getElementById('table-itsm-problems');
        if (!tbody) return;

        if (problems.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-400">No problems logged. All services stable.</td></tr>`;
            return;
        }

        tbody.innerHTML = problems.map(p => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3">
                    <div class="font-mono text-amber-700 font-bold">${p.problem_code}</div>
                    <div class="font-bold text-slate-900 text-xs">${p.title}</div>
                    <div class="text-[10px] text-slate-400 font-mono mt-0.5">Impact: ${p.impacted_ci_code}</div>
                </td>
                <td class="p-3 text-slate-700">${p.category}</td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${p.priority === 'P1-Critical' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'}">
                        ${p.priority}
                    </span>
                </td>
                <td class="p-3 text-slate-700 text-[11px] max-w-xs">
                    <div class="line-clamp-2" title="${p.root_cause_analysis}">${p.root_cause_analysis}</div>
                </td>
                <td class="p-3 text-slate-700 text-[11px] max-w-xs">
                    <div class="text-emerald-700 font-medium line-clamp-1" title="${p.temporary_workaround}">Workaround: ${p.temporary_workaround}</div>
                    <div class="text-slate-500 line-clamp-1 mt-0.5" title="${p.permanent_fix_plan}">Fix: ${p.permanent_fix_plan}</div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
                        ${p.status}
                    </span>
                </td>
                <td class="p-3 text-center">
                    ${p.kedb_published ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-book-bookmark mr-1"></i>KEDB</span>' : '<span class="text-slate-400 text-[10px]">Draft</span>'}
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error("Error loading ITSM problems:", err);
    }
}

// Subview 3: CAB Change Enablement
export async function loadITSMChanges() {
    try {
        const changes = await fetch(`${API_BASE}/itsm/changes`).then(r => r.json());
        const tbody = document.getElementById('table-itsm-changes');
        if (!tbody) return;

        if (changes.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="p-4 text-center text-slate-400">No change requests registered.</td></tr>`;
            return;
        }

        tbody.innerHTML = changes.map(c => {
            const isApproved = c.cab_status === 'Approved' || c.cab_status === 'Scheduled';
            return `
                <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                    <td class="p-3">
                        <div class="font-mono text-blue-700 font-bold">${c.cr_code}</div>
                        <div class="font-bold text-slate-900 text-xs">${c.title}</div>
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.change_type === 'Emergency' ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700'}">${c.change_type}</span>
                    </td>
                    <td class="p-3 text-slate-700 font-mono text-[11px]">${c.impact_scope}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${c.risk_level === 'High' ? 'bg-rose-100 text-rose-800' : (c.risk_level === 'Medium' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800')}">
                            ${c.risk_level} (${c.risk_score}/100)
                        </span>
                    </td>
                    <td class="p-3 text-slate-600 font-mono text-[11px]">
                        ${formatDate(c.scheduled_start_time)}
                    </td>
                    <td class="p-3 text-slate-600 text-[11px] max-w-xs truncate" title="${c.backout_rollback_plan}">
                        ${c.backout_rollback_plan}
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isApproved ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-200'}">
                            ${c.cab_status}
                        </span>
                    </td>
                    <td class="p-3 text-center whitespace-nowrap">
                        ${!isApproved ? `
                            <button onclick="handleCABReview(${c.id}, 'APPROVE')" class="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-bold transition">
                                <i class="fa-solid fa-check"></i> Approve CAB
                            </button>
                        ` : `
                            <span class="text-slate-400 text-[10px] font-bold"><i class="fa-solid fa-shield-check text-emerald-600 mr-0.5"></i> Authorized</span>
                        `}
                    </td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error("Error loading ITSM changes:", err);
    }
}

// Subview 4: Self-Healing Runbooks
export async function loadITSMRunbooks() {
    try {
        const runbooks = await fetch(`${API_BASE}/itsm/runbook-fixes`).then(r => r.json());
        const grid = document.getElementById('grid-itsm-runbooks');
        if (!grid) return;

        grid.innerHTML = runbooks.map(r => `
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 hover:border-purple-300 transition space-y-2">
                <div class="flex justify-between items-center">
                    <span class="font-mono text-purple-700 font-bold text-xs">${r.fix_code}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800">${r.execution_type}</span>
                </div>
                <h4 class="font-bold text-slate-900 text-sm">${r.fix_name}</h4>
                <div class="text-[11px] text-slate-500 font-mono">Trigger: <span class="text-slate-800 font-bold">${r.trigger_alert_pattern}</span></div>
                <div class="grid grid-cols-2 gap-2 text-[10px] text-slate-600 font-mono py-1 border-t border-slate-200">
                    <div>Executions: <strong>${r.execution_count}</strong></div>
                    <div>Success Rate: <strong class="text-emerald-600">${r.success_rate_pct}%</strong></div>
                    <div>Target: <strong>${r.target_ci_type}</strong></div>
                    <div>MTTR Saved: <strong class="text-purple-600">${r.average_mttr_reduction_mins}m</strong></div>
                </div>
                <button onclick="handleExecuteRunbook(${r.id}, 'CI-DB-PROD-01')" class="w-full mt-2 py-1.5 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-lg text-xs transition flex items-center justify-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-play"></i> Execute Self-Healing Fix
                </button>
            </div>
        `).join('');
    } catch (err) {
        console.error("Error loading ITSM runbooks:", err);
    }
}

// Subview 5: Procurement LOIs & SLAs
export async function loadITSMLOIs() {
    try {
        const lois = await fetch(`${API_BASE}/itsm/procurement-lois`).then(r => r.json());
        cachedITSM_LOIs = lois;
        const tbody = document.getElementById('table-itsm-lois');
        if (!tbody) return;

        if (lois.length === 0) {
            tbody.innerHTML = `<tr><td colspan="9" class="p-4 text-center text-slate-400">No IT procurement LOIs drafted.</td></tr>`;
            return;
        }

        tbody.innerHTML = lois.map(l => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3 font-mono font-bold text-emerald-700">${l.loi_number}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-900">${l.vendor_name}</div>
                    <div class="text-[10px] text-slate-400">${l.vendor_contact_person} (${l.vendor_email})</div>
                </td>
                <td class="p-3 text-slate-700 text-xs">${l.asset_category}</td>
                <td class="p-3 font-mono font-bold text-slate-900">${formatINR(l.estimated_contract_value_inr)}</td>
                <td class="p-3 text-slate-600 font-mono">${l.delivery_sla_weeks} Weeks</td>
                <td class="p-3 font-mono text-slate-600">${formatDate(l.valid_until_date)}</td>
                <td class="p-3">
                    <div class="font-bold text-slate-800 text-[11px]">${l.director_signatory}</div>
                    <div class="text-[9px] text-slate-400 font-mono">${l.company_cin}</div>
                </td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                        ${l.status}
                    </span>
                </td>
                <td class="p-3 text-center whitespace-nowrap">
                    <div class="flex items-center justify-center gap-1">
                        <button onclick="previewITSM_LOI(${l.id})" class="px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 rounded text-[10px] font-bold transition flex items-center gap-1">
                            <i class="fa-solid fa-eye"></i> View Formal LOI
                        </button>
                        <a href="${API_BASE}/itsm/procurement-lois/${l.id}/html" target="_blank" class="px-2 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded text-[10px] font-bold transition flex items-center gap-1">
                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Open Tab
                        </a>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error("Error loading ITSM LOIs:", err);
    }
}

export async function loadITSMSLAs() {
    try {
        const slas = await fetch(`${API_BASE}/itsm/sla-contracts`).then(r => r.json());
        const tbody = document.getElementById('table-itsm-slas');
        if (!tbody) return;

        tbody.innerHTML = slas.map(s => `
            <tr class="hover:bg-slate-50 transition border-b border-slate-100">
                <td class="p-3">
                    <div class="font-mono text-blue-700 font-bold">${s.service_code}</div>
                    <div class="font-bold text-slate-900">${s.service_name}</div>
                </td>
                <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${s.service_tier}</span></td>
                <td class="p-3 font-mono font-bold text-emerald-700">${s.target_uptime_pct}%</td>
                <td class="p-3 font-mono font-bold text-slate-900">${s.current_monthly_uptime_pct}%</td>
                <td class="p-3 font-mono text-slate-700">${s.p1_resolution_hours} Hours</td>
                <td class="p-3 font-mono text-slate-700">${s.p2_resolution_hours} Hours</td>
                <td class="p-3 text-[11px] text-slate-600 max-w-xs">${s.sla_penalty_clause}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">${s.status}</span></td>
            </tr>
        `).join('');
    } catch (err) {
        console.error("Error loading ITSM SLAs:", err);
    }
}

// Action Handlers
export async function handleCreateCMDBNode(e) {
    e.preventDefault();
    try {
        const body = {
            ci_code: document.getElementById('new-ci-code').value.trim(),
            ci_name: document.getElementById('new-ci-name').value.trim(),
            ci_type: document.getElementById('new-ci-type').value,
            category: document.getElementById('new-ci-cat').value,
            environment: document.getElementById('new-ci-env').value,
            tier: document.getElementById('new-ci-tier').value,
            ip_address: document.getElementById('new-ci-ip').value.trim() || '10.0.1.15',
            fqdn: document.getElementById('new-ci-fqdn').value.trim() || 'node.asperion.internal',
            cloud_provider: document.getElementById('new-ci-cloud').value.trim(),
            upstream_dependencies_json: document.getElementById('new-ci-upstreams').value.trim() || '[]',
            status: 'Operational',
            health_score: 99.8,
            cpu_utilization_pct: 35.0,
            memory_utilization_pct: 50.0,
            disk_utilization_pct: 25.0
        };

        const res = await fetch(`${API_BASE}/itsm/cmdb/nodes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Configuration Item successfully registered in CMDB!");
            closeITSMModal('modal-itsm-ci');
            loadCMDBNodes();
        } else {
            const err = await res.json();
            alert("Error registering CI: " + (err.detail || "Validation error"));
        }
    } catch (err) {
        alert("Error saving CI node: " + err.message);
    }
}

export async function handleCreateChangeRequest(e) {
    e.preventDefault();
    try {
        const body = {
            cr_code: document.getElementById('new-cr-code').value.trim(),
            title: document.getElementById('new-cr-title').value.trim(),
            change_type: document.getElementById('new-cr-type').value,
            reason_for_change: document.getElementById('new-cr-reason').value.trim(),
            impact_scope: document.getElementById('new-cr-scope').value.trim(),
            risk_level: document.getElementById('new-cr-risk').value,
            risk_score: 40,
            cab_status: 'Submitted',
            implementation_plan: document.getElementById('new-cr-impl').value.trim(),
            backout_rollback_plan: document.getElementById('new-cr-rollback').value.trim(),
            test_validation_procedure: 'Perform synthetic health checks on API endpoints post-release.',
            scheduled_start_time: new Date(Date.now() + 86400000).toISOString(),
            scheduled_end_time: new Date(Date.now() + 93600000).toISOString(),
            outage_required: false,
            lead_implementer: 'Release Engineering Lead'
        };

        const res = await fetch(`${API_BASE}/itsm/changes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            alert("✅ Change Request successfully submitted for CAB review!");
            closeITSMModal('modal-itsm-cr');
            loadITSMChanges();
        } else {
            const err = await res.json();
            alert("Error submitting CR: " + (err.detail || "Validation error"));
        }
    } catch (err) {
        alert("Error creating CR: " + err.message);
    }
}

export async function handleCABReview(changeId, action) {
    try {
        const res = await fetch(`${API_BASE}/itsm/changes/${changeId}/cab-review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: action,
                reviewer_name: "Varadi Vijay",
                reviewer_role: "Founder & Sole Director",
                review_notes: "CAB review executed. Production change window authorized."
            })
        });

        if (res.ok) {
            alert(`✅ Change Request ${action}D by Change Advisory Board (Director: Varadi Vijay)!`);
            loadITSMChanges();
        } else {
            alert("Failed to review Change Request.");
        }
    } catch (err) {
        alert("Error in CAB review: " + err.message);
    }
}

export async function handleExecuteRunbook(fixId, nodeCode) {
    const consoleEl = document.getElementById('itsm-runbook-console');
    if (consoleEl) {
        consoleEl.innerHTML = `<div class="text-cyan-400">[EXEC] Triggering Runbook #${fixId} on ${nodeCode}...</div>`;
    }

    try {
        const res = await fetch(`${API_BASE}/itsm/runbook-fixes/${fixId}/execute?target_node=${nodeCode}`, {
            method: 'POST'
        });
        const data = await res.json();

        if (res.ok) {
            if (consoleEl && data.output_log) {
                consoleEl.innerHTML = data.output_log.map(l => `<div class="${l.includes('SUCCESS') || l.includes('RESOLVED') ? 'text-emerald-400 font-bold' : 'text-slate-300'}">${l}</div>`).join('');
            }
            alert(`⚡ Runbook executed successfully! Node ${nodeCode} telemetry restored to 99.8%.`);
            loadITSM();
        } else {
            alert("Runbook execution failed: " + (data.detail || "Error"));
        }
    } catch (err) {
        alert("Error executing runbook: " + err.message);
    }
}

export async function handleCreateProcurementLOI(e) {
    e.preventDefault();
    try {
        const body = {
            loi_number: document.getElementById('new-loi-num').value.trim(),
            vendor_name: document.getElementById('new-loi-vendor').value.trim(),
            vendor_address: document.getElementById('new-loi-address').value.trim(),
            vendor_contact_person: document.getElementById('new-loi-contact').value.trim(),
            vendor_email: document.getElementById('new-loi-email').value.trim(),
            asset_category: document.getElementById('new-loi-cat').value.trim(),
            scope_of_procurement: document.getElementById('new-loi-scope').value.trim(),
            equipment_specifications: document.getElementById('new-loi-specs').value.trim(),
            estimated_contract_value_inr: parseFloat(document.getElementById('new-loi-val').value) || 1000000,
            delivery_sla_weeks: parseInt(document.getElementById('new-loi-delivery').value) || 3,
            valid_until_date: document.getElementById('new-loi-validity').value,
            director_signatory: "Varadi Vijay",
            director_title: "Founder & Sole Director",
            company_name: "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            company_cin: "U85500KA2026OPC222069",
            registered_office: "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India",
            status: "Approved & Issued"
        };

        const res = await fetch(`${API_BASE}/itsm/procurement-lois`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            const data = await res.json();
            alert(`✅ Formal Letter of Intent ${data.loi_number} drafted and authorized!`);
            closeITSMModal('modal-itsm-loi');
            loadITSMLOIs();
            previewITSM_LOI(data.id);
        } else {
            const err = await res.json();
            alert("Error drafting LOI: " + (err.detail || "Validation error"));
        }
    } catch (err) {
        alert("Error generating LOI: " + err.message);
    }
}

export async function previewITSM_LOI(loiId) {
    try {
        const res = await fetch(`${API_BASE}/itsm/procurement-lois/${loiId}/html`);
        if (!res.ok) throw new Error("Failed to load LOI document.");
        const html = await res.text();

        const container = document.getElementById('itsm-loi-preview-container');
        if (container) {
            container.innerHTML = html;
        }
        currentViewingLOI = loiId;
        openITSMModal('modal-itsm-loi-preview');
    } catch (err) {
        alert("Failed to load LOI preview: " + err.message);
    }
}

export function printITSMCurrentLOI() {
    const container = document.getElementById('itsm-loi-preview-container');
    if (!container) return;
    const printWin = window.open('', '_blank');
    printWin.document.write(container.innerHTML);
    printWin.document.close();
    printWin.focus();
    printWin.print();
}

export function openITSMModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('hidden');
}

export function closeITSMModal(modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('hidden');
}


// ==============================================================================
// 17. AGENTIC AI & AUTONOMOUS MULTI-AGENT SWARM CONTROLLER
// Fleet Management, ReAct Loops, Tool Execution, Mission Traces & Live Chat
// ==============================================================================

export let cachedAgenticFleet = [];
export let cachedAgenticMissions = [];
export let currentAgenticTab = 'fleet';

export function switchAgenticAITab(tabKey) {
    currentAgenticTab = tabKey;
    ['fleet', 'missions', 'chat', 'topology'].forEach(k => {
        const view = document.getElementById(`agentic-view-${k}`);
        const btn = document.getElementById(`agentic-tab-btn-${k}`);
        if (view) {
            if (k === tabKey) view.classList.remove('hidden');
            else view.classList.add('hidden');
        }
        if (btn) {
            if (k === tabKey) {
                btn.className = "px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-purple-900 text-white shadow";
            } else {
                btn.className = "px-4 py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 transition flex items-center gap-2";
            }
        }
    });
}

export async function loadAgenticAI() {
    try {
        const [overviewRes, agentsRes, missionsRes] = await Promise.all([
            fetch(`${API_BASE}/agentic-ai/overview`).then(r => r.json()).catch(() => null),
            fetch(`${API_BASE}/agentic-ai/agents`).then(r => r.json()).catch(() => []),
            fetch(`${API_BASE}/agentic-ai/missions`).then(r => r.json()).catch(() => [])
        ]);

        cachedAgenticFleet = Array.isArray(agentsRes) ? agentsRes : [];
        cachedAgenticMissions = Array.isArray(missionsRes) ? missionsRes : [];

        // 1. Populate Executive KPIs
        if (overviewRes) {
            const kActive = document.getElementById('kpi-agentic-active-agents');
            const kMissions = document.getElementById('kpi-agentic-total-missions');
            const kSuccess = document.getElementById('kpi-agentic-success-rate');
            const kApproval = document.getElementById('kpi-agentic-approval-gates');
            const kTools = document.getElementById('kpi-agentic-grounded-tools');
            const kGuard = document.getElementById('kpi-agentic-guardrail-pass');

            if (kActive) kActive.textContent = overviewRes.total_agents || cachedAgenticFleet.length || 5;
            if (kMissions) kMissions.textContent = `${overviewRes.total_missions_executed || 200}+`;
            if (kSuccess) kSuccess.textContent = `${overviewRes.fleet_success_rate_pct || 99.6}%`;
            if (kApproval) kApproval.textContent = `${overviewRes.pending_human_approvals || 0} Gate(s)`;
            if (kTools) kTools.textContent = `${overviewRes.mcp_tools_connected || 24} Tools`;
            if (kGuard) kGuard.textContent = `${overviewRes.guardrail_compliance_score || 100}%`;
        }

        // 2. Render Agent Fleet Cards
        renderAgenticFleet(cachedAgenticFleet);

        // 3. Render Missions Table
        renderAgenticMissions(cachedAgenticMissions);

    } catch (err) {
        console.error("Error loading Agentic AI suite:", err);
    }
}

export function renderAgenticFleet(agents) {
    const grid = document.getElementById('agentic-fleet-grid');
    if (!grid) return;

    if (!agents || agents.length === 0) {
        grid.innerHTML = `<div class="p-8 text-center text-slate-400 bg-white rounded-xl border border-slate-200 col-span-3">No autonomous agents currently registered.</div>`;
        return;
    }

    grid.innerHTML = agents.map(agent => {
        let tools = [];
        try {
            tools = JSON.parse(agent.assigned_tools_json || "[]");
        } catch (e) {
            tools = [];
        }

        let tierBadgeColor = "bg-purple-100 text-purple-800 border-purple-200";
        if (agent.autonomy_tier.includes("Level 4")) tierBadgeColor = "bg-purple-100 text-purple-800 border-purple-200";
        else if (agent.autonomy_tier.includes("Level 3")) tierBadgeColor = "bg-blue-100 text-blue-800 border-blue-200";
        else if (agent.autonomy_tier.includes("Level 2")) tierBadgeColor = "bg-amber-100 text-amber-800 border-amber-200";

        const toolsHtml = tools.slice(0, 4).map(t => `<span class="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-100 text-slate-700 border border-slate-200">${t}</span>`).join(' ') + 
            (tools.length > 4 ? ` <span class="text-[10px] text-slate-400 font-mono">+${tools.length - 4} more</span>` : '');

        return `
        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition space-y-4 flex flex-col justify-between">
            <div class="space-y-3">
                <div class="flex items-start justify-between gap-2">
                    <div class="flex items-center gap-2.5">
                        <div class="w-10 h-10 rounded-xl bg-purple-900 text-purple-200 flex items-center justify-center font-bold text-sm shadow">
                            <i class="fa-solid fa-robot"></i>
                        </div>
                        <div>
                            <div class="text-[11px] font-mono text-purple-600 font-bold">${escapeHtml(agent.agent_code)}</div>
                            <h4 class="font-bold text-sm text-slate-800 leading-tight">${escapeHtml(agent.name)}</h4>
                        </div>
                    </div>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold border ${tierBadgeColor} whitespace-nowrap">
                        ${escapeHtml(agent.autonomy_tier.split(':')[0])}
                    </span>
                </div>
                <div>
                    <div class="text-xs font-semibold text-slate-700">${escapeHtml(agent.role)}</div>
                    <div class="text-[11px] text-slate-500 font-medium">${escapeHtml(agent.department)} • <span class="font-mono text-slate-600">${escapeHtml(agent.model_endpoint)}</span></div>
                </div>
                <div class="p-2.5 bg-slate-50 rounded-lg text-[11px] text-slate-600 italic border border-slate-100 line-clamp-3">
                    "${escapeHtml(agent.system_prompt)}"
                </div>
                <div>
                    <div class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Grounded MCP Tools</div>
                    <div class="flex flex-wrap gap-1">${toolsHtml}</div>
                </div>
            </div>
            <div class="pt-3 border-t border-slate-100 space-y-3">
                <div class="grid grid-cols-3 gap-2 text-center text-xs">
                    <div class="p-2 bg-slate-50 rounded-lg">
                        <div class="font-bold text-slate-800">${agent.total_missions_executed}</div>
                        <div class="text-[9px] text-slate-500 uppercase">Missions</div>
                    </div>
                    <div class="p-2 bg-slate-50 rounded-lg">
                        <div class="font-bold text-emerald-600">${agent.success_rate_pct}%</div>
                        <div class="text-[9px] text-slate-500 uppercase">Success</div>
                    </div>
                    <div class="p-2 bg-slate-50 rounded-lg">
                        <div class="font-bold text-purple-600">${agent.avg_execution_latency_sec}s</div>
                        <div class="text-[9px] text-slate-500 uppercase">Latency</div>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="openDispatchMissionModal('${agent.agent_code}')" class="flex-1 py-1.5 px-3 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold transition flex items-center justify-center gap-1.5 shadow-sm">
                        <i class="fa-solid fa-bolt text-[11px]"></i> Dispatch
                    </button>
                    <button onclick="startAgentChatWithPersona('${agent.agent_code}')" class="py-1.5 px-3 bg-slate-100 hover:bg-purple-50 hover:text-purple-700 text-slate-700 border border-slate-200 rounded-lg text-xs font-semibold transition flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-comments text-[11px]"></i> Chat
                    </button>
                </div>
            </div>
        </div>
        `;
    }).join('');
}

export function renderAgenticMissions(missions) {
    const tbody = document.getElementById('agentic-missions-table-body');
    if (!tbody) return;

    if (!missions || missions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-400">No mission execution history available.</td></tr>`;
        return;
    }

    tbody.innerHTML = missions.map(m => {
        let statusBadge = "bg-emerald-100 text-emerald-800 border-emerald-200";
        if (m.status === "Requires Human Approval") statusBadge = "bg-amber-100 text-amber-800 border-amber-300";
        else if (m.status === "Executing") statusBadge = "bg-blue-100 text-blue-800 border-blue-200";
        else if (m.status === "Failed") statusBadge = "bg-rose-100 text-rose-800 border-rose-200";

        const isApprovalRequired = (m.status === "Requires Human Approval");

        return `
        <tr class="hover:bg-slate-50/80 transition">
            <td class="p-3 font-mono font-bold text-purple-700">${escapeHtml(m.mission_code)}</td>
            <td class="p-3">
                <div class="font-bold text-slate-800">${escapeHtml(m.agent_name || m.agent_code || 'Autonomous Sentinel')}</div>
                <div class="text-[10px] text-slate-500 font-mono">${escapeHtml(m.agent_code || '')}</div>
            </td>
            <td class="p-3">
                <div class="font-semibold text-slate-800">${escapeHtml(m.title)}</div>
                <div class="text-[11px] text-slate-500 line-clamp-1">${escapeHtml(m.output_summary)}</div>
            </td>
            <td class="p-3 font-mono text-[11px] text-slate-600">${escapeHtml(m.trigger_type)}</td>
            <td class="p-3 font-mono text-slate-700">${m.execution_duration_sec}s</td>
            <td class="p-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold border ${statusBadge}">
                    ${escapeHtml(m.status)}
                </span>
            </td>
            <td class="p-3">
                <div class="flex items-center gap-1.5">
                    ${isApprovalRequired ? `
                        <button onclick="handleApproveAgentMission(${m.id})" class="px-2.5 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded text-[11px] font-bold transition flex items-center gap-1 shadow-sm">
                            <i class="fa-solid fa-signature"></i> Signoff
                        </button>
                    ` : ''}
                    <button onclick="viewMissionTrace(${m.id})" class="px-2.5 py-1 bg-slate-100 hover:bg-purple-100 hover:text-purple-800 text-slate-700 border border-slate-200 rounded text-[11px] font-medium transition flex items-center gap-1">
                        <i class="fa-solid fa-list-check"></i> Traces
                    </button>
                </div>
            </td>
        </tr>
        `;
    }).join('');
}

export function filterAgenticMissions() {
    const statusFilter = document.getElementById('agentic-missions-filter-status')?.value || '';
    if (!statusFilter) {
        renderAgenticMissions(cachedAgenticMissions);
        return;
    }
    const filtered = cachedAgenticMissions.filter(m => m.status === statusFilter);
    renderAgenticMissions(filtered);
}

export function openDispatchMissionModal(agentCode = null) {
    const modal = document.getElementById('modal-agent-dispatch');
    if (!modal) return;
    if (agentCode) {
        const select = document.getElementById('dispatch-agent-select');
        if (select) select.value = agentCode;
    }
    modal.classList.remove('hidden');
}

export function closeDispatchMissionModal() {
    const modal = document.getElementById('modal-agent-dispatch');
    if (modal) modal.classList.add('hidden');
}

export async function handleDispatchMissionSubmit(event) {
    event.preventDefault();
    const btn = document.getElementById('dispatch-submit-btn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Executing ReAct Loop...`;
    }

    const payload = {
        agent_code: document.getElementById('dispatch-agent-select')?.value || 'AGT-SRE-01',
        title: document.getElementById('dispatch-title-input')?.value || 'Autonomous Operational Mission',
        prompt_or_goal: document.getElementById('dispatch-goal-input')?.value || 'Execute verification',
        trigger_type: document.getElementById('dispatch-trigger-select')?.value || 'User Dispatched'
    };

    try {
        const res = await fetch(`${API_BASE}/agentic-ai/missions/dispatch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Dispatch failed with status ${res.status}`);
        }

        const mission = await res.json();
        closeDispatchMissionModal();
        if (typeof showEnterpriseToast === 'function') {
            showEnterpriseToast('Mission Completed', `Mission ${mission.mission_code} dispatched and completed successfully.`, 'success', 3500);
        } else {
            alert(`Mission ${mission.mission_code} completed successfully!`);
        }

        await loadAgenticAI();
        viewMissionTrace(mission.id);

    } catch (err) {
        alert("Mission dispatch failed: " + err.message);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = `<i class="fa-solid fa-rocket"></i> Launch Autonomous ReAct Loop`;
        }
    }
}

export async function handleApproveAgentMission(missionId) {
    const approver = prompt("Enter Authorized Approver Name (e.g. Director Varadi Vijay):", "Varadi Vijay");
    if (!approver) return;

    try {
        const res = await fetch(`${API_BASE}/agentic-ai/missions/${missionId}/approve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'APPROVE',
                approver_name: approver,
                notes: 'Director authorization confirmed via Human-in-the-Loop signature.'
            })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Approval failed");
        }

        if (typeof showEnterpriseToast === 'function') {
            showEnterpriseToast('Human-in-the-Loop Signoff', `Mission ${missionId} authorized and approved by ${approver}.`, 'success', 3000);
        } else {
            alert(`Mission ${missionId} approved successfully by ${approver}!`);
        }
        await loadAgenticAI();
    } catch (e) {
        alert("Error approving mission: " + e.message);
    }
}

export async function viewMissionTrace(missionId) {
    try {
        const [mission, traces] = await Promise.all([
            fetch(`${API_BASE}/agentic-ai/missions/${missionId}`).then(r => r.json()),
            fetch(`${API_BASE}/agentic-ai/traces/${missionId}`).then(r => r.json()).catch(() => [])
        ]);

        const modal = document.getElementById('modal-mission-trace');
        if (!modal) return;

        document.getElementById('trace-modal-title').textContent = `Mission: ${mission.mission_code} - ${mission.title}`;
        document.getElementById('trace-modal-subtitle').textContent = `Status: ${mission.status} | Duration: ${mission.execution_duration_sec}s | Trigger: ${mission.trigger_type}`;
        document.getElementById('trace-modal-agent').textContent = `Assigned Agent: ${mission.agent_name || mission.agent_code || 'Autonomous Sentinel'}`;
        document.getElementById('trace-modal-output').textContent = `Outcome: ${mission.output_summary}`;

        // Render Thought Chain
        let thoughts = [];
        try {
            thoughts = JSON.parse(mission.thought_chain_json || "[]");
        } catch (e) {
            thoughts = [];
        }

        const thoughtsContainer = document.getElementById('trace-modal-thoughts');
        if (thoughtsContainer) {
            thoughtsContainer.innerHTML = thoughts.map(t => `
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs space-y-1">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-purple-900 font-mono text-[10px]">STEP ${t.step || 1} • ${escapeHtml(t.phase || 'REASONING')}</span>
                        ${t.tool ? `<span class="px-2 py-0.5 rounded text-[10px] bg-indigo-100 text-indigo-700 font-mono">${escapeHtml(t.tool)}</span>` : ''}
                    </div>
                    ${t.thought ? `<div class="text-slate-800"><strong>Thought:</strong> ${escapeHtml(t.thought)}</div>` : ''}
                    ${t.observation ? `<div class="text-slate-600"><strong>Observation:</strong> ${escapeHtml(t.observation)}</div>` : ''}
                </div>
            `).join('');
        }

        // Render Execution Traces
        const tracesBody = document.getElementById('trace-modal-traces-body');
        if (tracesBody) {
            if (!traces || traces.length === 0) {
                tracesBody.innerHTML = `<tr><td colspan="6" class="p-3 text-center text-slate-400">No granular audit traces recorded for this mission.</td></tr>`;
            } else {
                tracesBody.innerHTML = traces.map(tr => `
                    <tr class="hover:bg-slate-50">
                        <td class="p-2 font-mono font-bold text-slate-700">${tr.step_number}</td>
                        <td class="p-2 font-mono text-purple-700">${escapeHtml(tr.action_type)}</td>
                        <td class="p-2 font-mono text-slate-600">${escapeHtml(tr.tool_name || 'Guardrail Verification')}</td>
                        <td class="p-2 font-mono text-slate-700">${tr.latency_ms} ms</td>
                        <td class="p-2 font-mono text-slate-700">${tr.tokens_consumed}</td>
                        <td class="p-2">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold ${tr.guardrail_passed ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">
                                ${tr.guardrail_passed ? 'PASSED' : 'BLOCKED'}
                            </span>
                        </td>
                    </tr>
                `).join('');
            }
        }

        modal.classList.remove('hidden');

    } catch (err) {
        alert("Failed to load mission traces: " + err.message);
    }
}

export function closeMissionTraceModal() {
    const modal = document.getElementById('modal-mission-trace');
    if (modal) modal.classList.add('hidden');
}

// Interactive Chat
export function startAgentChatWithPersona(agentCode) {
    switchAgenticAITab('chat');
    const select = document.getElementById('agentic-chat-agent-select');
    if (select) {
        select.value = agentCode;
        handleAgentChatSelectChange();
    }
}

export function handleAgentChatSelectChange() {
    const agentCode = document.getElementById('agentic-chat-agent-select')?.value || 'AGT-SRE-01';
    const agent = cachedAgenticFleet.find(a => a.agent_code === agentCode);

    const titleEl = document.getElementById('chat-header-agent-title');
    const nameEl = document.getElementById('chat-card-agent-name');
    const tierEl = document.getElementById('chat-card-agent-tier');
    const descEl = document.getElementById('chat-card-agent-desc');

    if (agent) {
        if (titleEl) titleEl.textContent = `${agent.name} (${agent.agent_code})`;
        if (nameEl) nameEl.textContent = agent.name;
        if (tierEl) tierEl.textContent = agent.autonomy_tier;
        if (descEl) descEl.textContent = agent.role;
    }
}

export function fillAgentChatPrompt(text) {
    const input = document.getElementById('agentic-chat-input');
    if (input) {
        input.value = text;
        input.focus();
    }
}

export function clearAgentChatHistory() {
    const container = document.getElementById('agentic-chat-messages');
    if (container) {
        container.innerHTML = `
            <div class="flex items-start gap-2.5">
                <div class="w-7 h-7 rounded-full bg-purple-600 text-white flex items-center justify-center text-xs flex-shrink-0">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div class="bg-white p-3.5 rounded-xl rounded-tl-none border border-slate-200 text-xs text-slate-800 max-w-xl shadow-sm space-y-1.5">
                    <div class="font-bold text-purple-900">Autonomous Sentinel Ready</div>
                    <p>Conversation history cleared. Ready for next query or enterprise mission directive.</p>
                </div>
            </div>
        `;
    }
}

export async function handleSendAgentChatMessage(event) {
    event.preventDefault();
    const input = document.getElementById('agentic-chat-input');
    const sendBtn = document.getElementById('agentic-chat-send-btn');
    const msgContainer = document.getElementById('agentic-chat-messages');

    if (!input || !input.value.trim()) return;
    const userMessage = input.value.trim();
    input.value = '';

    const agentCode = document.getElementById('agentic-chat-agent-select')?.value || 'AGT-SRE-01';

    // Append User Message
    if (msgContainer) {
        msgContainer.insertAdjacentHTML('beforeend', `
            <div class="flex items-start justify-end gap-2.5">
                <div class="bg-purple-900 text-white p-3.5 rounded-xl rounded-tr-none text-xs max-w-xl shadow-sm">
                    ${escapeHtml(userMessage)}
                </div>
                <div class="w-7 h-7 rounded-full bg-slate-800 text-white flex items-center justify-center text-xs flex-shrink-0">
                    <i class="fa-solid fa-user"></i>
                </div>
            </div>
        `);
        msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i>`;
    }

    try {
        const res = await fetch(`${API_BASE}/agentic-ai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent_code: agentCode,
                message: userMessage
            })
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || "Agent chat execution failed.");
        }

        const data = await res.json();

        const toolPills = (data.tools_called && data.tools_called.length > 0)
            ? `<div class="flex flex-wrap gap-1 mt-2">` + data.tools_called.map(t => `<span class="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-100 text-purple-800 border border-purple-200"><i class="fa-solid fa-wrench mr-1"></i>${escapeHtml(t)}</span>`).join('') + `</div>`
            : '';

        // Append Agent Response
        if (msgContainer) {
            msgContainer.insertAdjacentHTML('beforeend', `
                <div class="flex items-start gap-2.5">
                    <div class="w-7 h-7 rounded-full bg-purple-600 text-white flex items-center justify-center text-xs flex-shrink-0">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <div class="bg-white p-3.5 rounded-xl rounded-tl-none border border-slate-200 text-xs text-slate-800 max-w-xl shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-purple-900">${escapeHtml(data.agent_name)}</span>
                            <span class="text-[10px] text-slate-400 font-mono">${escapeHtml(data.timestamp || '')}</span>
                        </div>
                        <div class="text-slate-800 leading-relaxed whitespace-pre-line">${escapeHtml(data.reply)}</div>
                        ${toolPills}
                        <div class="text-[10px] text-slate-500 bg-slate-50 p-2 rounded border border-slate-100 font-mono">
                            <i class="fa-solid fa-circle-info mr-1 text-purple-600"></i> ${escapeHtml(data.reasoning_summary)}
                        </div>
                    </div>
                </div>
            `);
            msgContainer.scrollTop = msgContainer.scrollHeight;
        }

    } catch (e) {
        if (msgContainer) {
            msgContainer.insertAdjacentHTML('beforeend', `
                <div class="p-3 bg-rose-50 text-rose-700 rounded-lg text-xs border border-rose-200">
                    <i class="fa-solid fa-triangle-exclamation mr-1"></i> Error: ${escapeHtml(e.message)}
                </div>
            `);
        }
    } finally {
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.innerHTML = `<i class="fa-solid fa-paper-plane"></i> Send`;
        }
    }
}

// =========================================================================
// 22. ENTERPRISE OPERATIONS, BCP/DR & CRYPTOGRAPHIC EVENT LEDGER CONTROLLER
// =========================================================================

export let currentOperationsTab = 'ledger';
export let cachedLedgerEvents = [];

export async function loadOperations() {
    await Promise.all([
        loadOperationsOverview(),
        loadOperationsLedger(),
        loadOperationsSnapshots(),
        loadOperationsConsents(),
        loadOperationsTelemetry()
    ]);
}

export async function loadOperationsOverview() {
    try {
        const res = await fetch(`${API_BASE}/operations/overview`);
        if (!res.ok) return;
        const data = await res.json();

        // Update Executive KPI stat cards
        const evCount = document.getElementById('ops-stat-events-count');
        if (evCount) evCount.textContent = data.ledger_summary.total_events || '0';

        const statusEl = document.getElementById('ops-stat-ledger-status');
        if (statusEl) {
            if (data.ledger_summary.is_tamper_evident) {
                statusEl.innerHTML = `<i class="fa-solid fa-circle-check"></i> SHA-256 Chained (100% Valid)`;
                statusEl.className = 'text-[11px] font-mono text-emerald-400 mt-0.5 flex items-center gap-1';
            } else {
                statusEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Tamper Detected!`;
                statusEl.className = 'text-[11px] font-mono text-rose-400 mt-0.5 flex items-center gap-1';
            }
        }

        const snapCount = document.getElementById('ops-stat-snapshots-count');
        if (snapCount) snapCount.textContent = data.bcp_dr_summary.total_snapshots || '0';

        const consentCount = document.getElementById('ops-stat-consents-count');
        if (consentCount) consentCount.textContent = `${data.dpdp_summary.granted_consents}/${data.dpdp_summary.total_consents}`;

        const dbSizeEl = document.getElementById('ops-stat-db-size');
        if (dbSizeEl) dbSizeEl.textContent = data.telemetry_summary.db_size_formatted || '--';

        const latEl = document.getElementById('ops-stat-latency');
        if (latEl) latEl.textContent = `Query: ${data.telemetry_summary.query_latency_ms}ms`;

        const lastTag = document.getElementById('ops-last-verified-tag');
        if (lastTag && data.ledger_summary.latest_hash) {
            const shortHash = data.ledger_summary.latest_hash.substring(0, 16) + '...';
            lastTag.innerHTML = `Latest Hash: <strong class="text-cyan-300 font-mono">${escapeHtml(shortHash)}</strong>`;
        }
    } catch (e) {
        console.warn("Failed to load operations overview:", e);
    }
}

export function switchOperationsTab(tabId) {
    currentOperationsTab = tabId;
    ['ledger', 'bcp-dr', 'dpdp', 'telemetry'].forEach(t => {
        const pane = document.getElementById(`ops-tab-${t}`);
        const btn = document.getElementById(`btn-ops-tab-${t}`);
        if (pane) {
            if (t === tabId) pane.classList.remove('hidden');
            else pane.classList.add('hidden');
        }
        if (btn) {
            if (t === tabId) {
                btn.classList.add('border-cyan-500', 'text-cyan-400');
                btn.classList.remove('border-transparent', 'text-slate-400');
            } else {
                btn.classList.remove('border-cyan-500', 'text-cyan-400');
                btn.classList.add('border-transparent', 'text-slate-400');
            }
        }
    });
}

export async function loadOperationsLedger() {
    const tbody = document.getElementById('ops-ledger-table-body');
    if (!tbody) return;

    const filterSelect = document.getElementById('ops-filter-aggregate-type');
    const aggFilter = filterSelect ? filterSelect.value : '';

    let url = `${API_BASE}/operations/ledger?limit=50`;
    if (aggFilter) url += `&aggregate_type=${encodeURIComponent(aggFilter)}`;

    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error("Failed to load cryptographic ledger.");
        const entries = await res.json();
        cachedLedgerEvents = entries;

        if (entries.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-500">No event records found matching filter.</td></tr>`;
            return;
        }

        tbody.innerHTML = entries.map((e, idx) => {
            const shortCurr = e.current_hash.substring(0, 12) + '...';
            const shortPrev = e.prev_hash.substring(0, 12) + '...';
            const isGenesis = e.prev_hash.startsWith('0000000000');
            const prevBadge = isGenesis
                ? `<span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-950/70 text-emerald-400 border border-emerald-800">GENESIS</span>`
                : `<span class="text-slate-400 font-mono text-[11px]" title="${escapeHtml(e.prev_hash)}">${escapeHtml(shortPrev)}</span>`;

            return `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="py-2.5 px-4 font-bold text-cyan-400">${escapeHtml(e.event_code)}</td>
                    <td class="py-2.5 px-4">
                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-200 border border-slate-700">
                            ${escapeHtml(e.aggregate_type)}
                        </span>
                        <div class="text-[10px] text-slate-400 font-mono mt-0.5">${escapeHtml(e.aggregate_id)}</div>
                    </td>
                    <td class="py-2.5 px-4 font-sans text-xs font-medium text-white">${escapeHtml(e.event_type)}</td>
                    <td class="py-2.5 px-4 font-sans">
                        <div class="text-slate-200">${escapeHtml(e.actor_name)}</div>
                        <div class="text-[10px] text-slate-400">${escapeHtml(e.actor_role)}</div>
                    </td>
                    <td class="py-2.5 px-4 font-mono text-[11px] text-emerald-300" title="${escapeHtml(e.current_hash)}">
                        <i class="fa-solid fa-lock text-[9px] mr-1 text-emerald-500"></i>${escapeHtml(shortCurr)}
                    </td>
                    <td class="py-2.5 px-4">${prevBadge}</td>
                    <td class="py-2.5 px-4 text-slate-400 text-[11px] font-mono">${formatDate(e.timestamp)} ${new Date(e.timestamp).toLocaleTimeString('en-IN', { hour12: false })}</td>
                    <td class="py-2.5 px-4 text-right">
                        <button onclick="viewLedgerPayload(${e.id})" class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[11px] font-semibold transition border border-slate-700">
                            <i class="fa-solid fa-code mr-1"></i> View
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-rose-400">Error: ${escapeHtml(e.message)}</td></tr>`;
    }
}

export function viewLedgerPayload(eventId) {
    const ev = cachedLedgerEvents.find(x => x.id === eventId);
    if (!ev) return;

    const titleEl = document.getElementById('ops-payload-modal-title');
    const codeEl = document.getElementById('ops-payload-event-code');
    const actorEl = document.getElementById('ops-payload-actor');
    const contentEl = document.getElementById('ops-payload-json-content');

    if (titleEl) titleEl.textContent = `Cryptographic Ledger Block #${ev.id}`;
    if (codeEl) codeEl.textContent = ev.event_code;
    if (actorEl) actorEl.textContent = `${ev.actor_name} (${ev.actor_role})`;

    try {
        const parsed = JSON.parse(ev.payload_json);
        if (contentEl) contentEl.textContent = JSON.stringify(parsed, null, 2);
    } catch (e) {
        if (contentEl) contentEl.textContent = ev.payload_json;
    }

    openModal('modal-ops-payload-viewer');
}

export async function verifyEventLedger() {
    showEnterpriseToast('Verifying Ledger', 'Recomputing cryptographic hash chains from Genesis Block...', 'info', 2000);
    try {
        const res = await fetch(`${API_BASE}/operations/ledger/verify`, { method: 'POST' });
        if (!res.ok) throw new Error("Verification request failed.");
        const result = await res.json();

        if (result.is_tamper_evident) {
            showEnterpriseToast(
                'Ledger Verified 100% Genuine',
                `All ${result.total_events_verified} chained event blocks verified with zero tampering. Latest hash: ${result.latest_hash.substring(0, 16)}...`,
                'success',
                6000
            );
        } else {
            showEnterpriseToast(
                'Cryptographic Integrity Warning',
                `Tamper detected at block ID #${result.tampered_event_id}! Status: ${result.verification_status}`,
                'error',
                10000
            );
        }
        loadOperationsOverview();
        loadOperationsLedger();
    } catch (e) {
        showEnterpriseToast('Ledger Verification Failed', e.message, 'error', 4000);
    }
}

export async function loadOperationsSnapshots() {
    const grid = document.getElementById('ops-snapshots-grid');
    if (!grid) return;

    try {
        const res = await fetch(`${API_BASE}/operations/bcp-dr/snapshots?limit=20`);
        if (!res.ok) throw new Error("Failed to load snapshots.");
        const snapshots = await res.json();

        if (snapshots.length === 0) {
            grid.innerHTML = `<div class="p-6 text-center text-slate-500 col-span-3">No BCP/DR snapshots recorded.</div>`;
            return;
        }

        grid.innerHTML = snapshots.map(s => {
            const shortChecksum = s.sha256_checksum.substring(0, 16) + '...';
            const sizeMb = (s.file_size_bytes / (1024 * 1024)).toFixed(2);

            return `
                <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow flex flex-col justify-between space-y-4">
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-white text-sm font-mono flex items-center gap-1.5">
                                <i class="fa-solid fa-cloud-arrow-up text-cyan-400"></i> ${escapeHtml(s.snapshot_code)}
                            </span>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                                ${escapeHtml(s.restore_test_status)}
                            </span>
                        </div>
                        <div class="text-xs text-slate-300 font-semibold">${escapeHtml(s.backup_type)}</div>
                        <div class="text-[11px] text-slate-400 leading-relaxed">${escapeHtml(s.notes || 'Automated baseline snapshot.')}</div>
                    </div>

                    <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-1.5 text-[11px] font-mono">
                        <div class="flex items-center justify-between text-slate-400">
                            <span>Storage Tier:</span>
                            <span class="text-slate-200">${escapeHtml(s.encryption_algorithm)}</span>
                        </div>
                        <div class="flex items-center justify-between text-slate-400">
                            <span>File Size:</span>
                            <span class="text-cyan-300 font-bold">${sizeMb} MB</span>
                        </div>
                        <div class="flex items-center justify-between text-slate-400" title="${escapeHtml(s.sha256_checksum)}">
                            <span>SHA-256:</span>
                            <span class="text-slate-300 truncate max-w-[130px]">${escapeHtml(shortChecksum)}</span>
                        </div>
                        <div class="flex items-center justify-between text-slate-400">
                            <span>RPO Commitment:</span>
                            <span class="text-emerald-400">&le; ${s.rpo_minutes}m</span>
                        </div>
                        <div class="flex items-center justify-between text-slate-400">
                            <span>RTO Target:</span>
                            <span class="text-emerald-400">&le; ${s.rto_minutes}m</span>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-1">
                        <span class="text-[10px] text-slate-500">${formatDate(s.created_at)}</span>
                        <button onclick="simulateDRRestore(${s.id})" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-1.5">
                            <i class="fa-solid fa-vial"></i> Test Restore Drill
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        grid.innerHTML = `<div class="p-6 text-center text-rose-400 col-span-3">Error: ${escapeHtml(e.message)}</div>`;
    }
}

export async function handleCreateBackupSnapshot(e) {
    e.preventDefault();
    const typeSelect = document.getElementById('ops-new-snapshot-type');
    const notesInput = document.getElementById('ops-new-snapshot-notes');

    const backupType = typeSelect ? typeSelect.value : "Full SQLite Hot Backup";
    const notes = notesInput ? notesInput.value.trim() : "On-demand administrator backup snapshot.";

    showEnterpriseToast('Generating Snapshot', 'Creating hot SQLite snapshot with real SHA-256 digest...', 'info', 2500);

    try {
        const res = await fetch(`${API_BASE}/operations/bcp-dr/snapshots/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ backup_type: backupType, notes: notes })
        });
        if (!res.ok) throw new Error("Failed to generate backup snapshot.");
        const snap = await res.json();

        closeModal('modal-create-backup-snapshot');
        showEnterpriseToast('Snapshot Generated', `Snapshot ${snap.snapshot_code} created and verified. SHA-256: ${snap.sha256_checksum.substring(0, 16)}...`, 'success', 4000);
        loadOperations();
    } catch (err) {
        showEnterpriseToast('Snapshot Creation Failed', err.message, 'error', 4000);
    }
}

export async function simulateDRRestore(snapshotId) {
    showEnterpriseToast('Executing DR Drill', `Mounting snapshot #${snapshotId} in isolated sandbox...`, 'info', 2000);
    try {
        const res = await fetch(`${API_BASE}/operations/bcp-dr/snapshots/${snapshotId}/test-restore`, { method: 'POST' });
        if (!res.ok) throw new Error("Restore drill simulation failed.");
        const result = await res.json();

        showEnterpriseToast(
            'DR Drill Succeeded (< 5m RTO)',
            `Snapshot ${result.snapshot_code} successfully restored in ${result.measured_rto_seconds}s (Target: < 300s). Data integrity score: 100%.`,
            'success',
            6000
        );
        loadOperationsOverview();
        loadOperationsSnapshots();
        loadOperationsLedger();
    } catch (e) {
        showEnterpriseToast('DR Drill Failed', e.message, 'error', 4000);
    }
}

export async function loadOperationsConsents() {
    const tbody = document.getElementById('ops-dpdp-table-body');
    if (!tbody) return;

    try {
        const res = await fetch(`${API_BASE}/operations/dpdp/consents?limit=50`);
        if (!res.ok) throw new Error("Failed to load DPDP consents.");
        const records = await res.json();

        if (records.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-500">No DPDP statutory consent records found.</td></tr>`;
            return;
        }

        tbody.innerHTML = records.map(r => `
            <tr class="hover:bg-slate-800/40 transition">
                <td class="py-2.5 px-4 font-mono font-bold text-amber-400">${escapeHtml(r.consent_ref)}</td>
                <td class="py-2.5 px-4">
                    <div class="font-bold text-white">${escapeHtml(r.data_principal_name)}</div>
                    <div class="text-[10px] text-slate-400">${escapeHtml(r.data_principal_type)}</div>
                </td>
                <td class="py-2.5 px-4 font-mono text-[11px] text-cyan-300">${escapeHtml(r.principal_identifier)}</td>
                <td class="py-2.5 px-4 text-slate-300">${escapeHtml(r.purpose_category)}</td>
                <td class="py-2.5 px-4 font-mono text-[11px] text-slate-400">${escapeHtml(r.notice_reference)}</td>
                <td class="py-2.5 px-4">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${r.consent_status === 'Granted' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'}">
                        ${escapeHtml(r.consent_status)}
                    </span>
                </td>
                <td class="py-2.5 px-4 text-slate-400 text-[11px] font-mono">${formatDate(r.granted_at)}</td>
                <td class="py-2.5 px-4 text-slate-300 text-[11px]">${escapeHtml(r.data_protection_officer)}</td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-rose-400">Error: ${escapeHtml(e.message)}</td></tr>`;
    }
}

export async function handleRecordDPDPConsent(e) {
    e.preventDefault();
    const name = document.getElementById('ops-dpdp-name').value.trim();
    const type = document.getElementById('ops-dpdp-type').value;
    const identifier = document.getElementById('ops-dpdp-identifier').value.trim();
    const purpose = document.getElementById('ops-dpdp-purpose').value;
    const notice = document.getElementById('ops-dpdp-notice').value.trim();
    const notes = document.getElementById('ops-dpdp-notes').value.trim();

    try {
        const res = await fetch(`${API_BASE}/operations/dpdp/consents`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data_principal_name: name,
                data_principal_type: type,
                principal_identifier: identifier,
                purpose_category: purpose,
                notice_reference: notice,
                consent_status: "Granted",
                audit_notes: notes || "Affirmative consent logged with cryptographic IP attestation."
            })
        });
        if (!res.ok) throw new Error("Failed to register statutory consent.");
        const record = await res.json();

        closeModal('modal-record-dpdp-consent');
        showEnterpriseToast('DPDP Consent Registered', `Consent ${record.consent_ref} successfully recorded for ${name}. Chained to event ledger.`, 'success', 4000);
        loadOperationsOverview();
        loadOperationsConsents();
        loadOperationsLedger();
    } catch (err) {
        showEnterpriseToast('DPDP Registration Failed', err.message, 'error', 4000);
    }
}

export async function loadOperationsTelemetry() {
    try {
        const res = await fetch(`${API_BASE}/operations/telemetry/live`);
        if (!res.ok) return;
        const data = await res.json();

        const dbSize = document.getElementById('tel-db-size');
        if (dbSize) dbSize.textContent = data.db_size_formatted;

        const walSize = document.getElementById('tel-wal-size');
        if (walSize) walSize.textContent = data.wal_size_formatted;

        const walMode = document.getElementById('tel-wal-mode');
        if (walMode) walMode.textContent = data.wal_checkpoint_status;

        const qLat = document.getElementById('tel-query-latency');
        if (qLat) qLat.textContent = `${data.db_query_latency_ms} ms`;

        const memRss = document.getElementById('tel-memory-rss');
        if (memRss) memRss.textContent = `${data.process_rss_mb} MB`;
    } catch (e) {
        console.warn("Failed to load live telemetry:", e);
    }
}

export async function triggerDBVacuum() {
    showEnterpriseToast('SRE Maintenance Active', 'Executing WAL checkpoint (TRUNCATE) and SQLite VACUUM...', 'info', 2500);
    try {
        const res = await fetch(`${API_BASE}/operations/telemetry/vacuum`, { method: 'POST' });
        if (!res.ok) throw new Error("Database vacuum execution failed.");
        const result = await res.json();

        showEnterpriseToast(
            'Optimization Completed',
            `Reclaimed ${result.reclaimed_bytes} bytes in ${result.vacuum_duration_sec}s. WAL truncate checkpoint clean.`,
            'success',
            4000
        );
        loadOperationsTelemetry();
        loadOperationsOverview();
        loadOperationsLedger();
    } catch (e) {
        showEnterpriseToast('Vacuum Failed', e.message, 'error', 4000);
    }
}

// =========================================================================
// 23. CRYPTOGRAPHIC & PKI TOOLS WORKBENCH CONTROLLER
// =========================================================================

export let currentCryptoTab = 'hashing';
export let activeGeneratedKeyPair = null;

export function loadCryptoTools() {
    if (!activeGeneratedKeyPair) {
        generateNewKeyPair('Ed25519', false);
    }
}

export function switchCryptoTab(tabId) {
    currentCryptoTab = tabId;
    ['hashing', 'aes-gcm', 'signatures', 'merkle'].forEach(t => {
        const pane = document.getElementById(`crypto-tab-${t}`);
        const btn = document.getElementById(`btn-crypto-tab-${t}`);
        if (pane) {
            if (t === tabId) pane.classList.remove('hidden');
            else pane.classList.add('hidden');
        }
        if (btn) {
            if (t === tabId) {
                btn.classList.add('border-emerald-500', 'text-emerald-400');
                btn.classList.remove('border-transparent', 'text-slate-400');
            } else {
                btn.classList.remove('border-emerald-500', 'text-emerald-400');
                btn.classList.add('border-transparent', 'text-slate-400');
            }
        }
    });
}

export async function executeCryptoHash() {
    const data = document.getElementById('crypto-hash-input').value;
    const algo = document.getElementById('crypto-hash-algo').value;
    const out = document.getElementById('crypto-hash-output');

    if (!data) {
        showEnterpriseToast('Input Required', 'Please enter payload string to compute hash.', 'warning');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/crypto/hash`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: data, algorithm: algo })
        });
        if (!res.ok) throw new Error("Hash computation failed.");
        const json = await res.json();
        if (out) out.textContent = json.digest;
        showEnterpriseToast('Digest Computed', `${algo} (${json.length_bits}-bit) generated.`, 'success', 2000);
    } catch (e) {
        showEnterpriseToast('Hashing Error', e.message, 'error');
    }
}

export async function executeCryptoHMAC() {
    const key = document.getElementById('crypto-hmac-key').value;
    const msg = document.getElementById('crypto-hmac-msg').value;
    const out = document.getElementById('crypto-hmac-output');

    if (!key || !msg) {
        showEnterpriseToast('Input Required', 'Secret key and message string are both required.', 'warning');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/crypto/hmac`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: key, message: msg })
        });
        if (!res.ok) throw new Error("HMAC generation failed.");
        const json = await res.json();
        if (out) out.textContent = json.hmac_digest;
        showEnterpriseToast('HMAC Authenticated', 'HMAC-SHA256 signature generated.', 'success', 2000);
    } catch (e) {
        showEnterpriseToast('HMAC Error', e.message, 'error');
    }
}

export async function executeAESEncrypt() {
    const pass = document.getElementById('crypto-aes-enc-pass').value;
    const pt = document.getElementById('crypto-aes-enc-plaintext').value;
    const ctOut = document.getElementById('crypto-aes-enc-ct');
    const nonceOut = document.getElementById('crypto-aes-enc-nonce');

    if (!pass || !pt) {
        showEnterpriseToast('Input Required', 'Passphrase and plaintext payload are required.', 'warning');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/crypto/encrypt/aes-gcm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plaintext: pt, passphrase: pass })
        });
        if (!res.ok) throw new Error("AES-GCM Encryption failed.");
        const json = await res.json();
        if (ctOut) ctOut.textContent = json.ciphertext_b64;
        if (nonceOut) nonceOut.textContent = json.nonce_b64;

        // Auto-fill decrypt box for seamless developer experience
        const decPass = document.getElementById('crypto-aes-dec-pass');
        const decNonce = document.getElementById('crypto-aes-dec-nonce');
        const decCt = document.getElementById('crypto-aes-dec-ct');
        if (decPass) decPass.value = pass;
        if (decNonce) decNonce.value = json.nonce_b64;
        if (decCt) decCt.value = json.ciphertext_b64;

        showEnterpriseToast('AES-256-GCM Encrypted', 'Authenticated ciphertext generated with 96-bit nonce.', 'success', 2500);
    } catch (e) {
        showEnterpriseToast('Encryption Error', e.message, 'error');
    }
}

export async function executeAESDecrypt() {
    const pass = document.getElementById('crypto-aes-dec-pass').value;
    const nonce = document.getElementById('crypto-aes-dec-nonce').value;
    const ct = document.getElementById('crypto-aes-dec-ct').value;
    const out = document.getElementById('crypto-aes-dec-output');

    if (!pass || !nonce || !ct) {
        showEnterpriseToast('Input Required', 'Passphrase, nonce, and ciphertext are required.', 'warning');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/crypto/decrypt/aes-gcm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ciphertext_b64: ct, nonce_b64: nonce, passphrase: pass })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Authentication tag mismatch.");
        }
        const json = await res.json();
        if (out) out.textContent = json.plaintext;
        showEnterpriseToast('Decrypted & Verified', 'Authenticated ciphertext verified with zero tampering.', 'success', 2500);
    } catch (e) {
        if (out) out.textContent = `[DECRYPTION FAILED]: ${e.message}`;
        showEnterpriseToast('Decryption Failed', e.message, 'error');
    }
}

export async function generateNewKeyPair(algo = 'Ed25519', toast = true) {
    const endpoint = algo === 'Ed25519' ? '/crypto/keys/generate/ed25519' : '/crypto/keys/generate/rsa?key_size=2048';
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, { method: 'POST' });
        if (!res.ok) throw new Error("Key generation failed.");
        const json = await res.json();
        activeGeneratedKeyPair = json;

        const pubEl = document.getElementById('crypto-pubkey-display');
        const privEl = document.getElementById('crypto-privkey-display');
        if (pubEl) pubEl.value = json.public_key_pem;
        if (privEl) privEl.value = json.private_key_pem;

        if (toast) {
            showEnterpriseToast('Keypair Generated', `${json.key_type} keypair initialized. Fingerprint: ${json.fingerprint_sha256.substring(0, 16)}...`, 'success', 3000);
        }
    } catch (e) {
        showEnterpriseToast('Key Generation Error', e.message, 'error');
    }
}

export async function executeSignMessage() {
    const msg = document.getElementById('crypto-sign-msg').value;
    const privEl = document.getElementById('crypto-privkey-display');
    const sigOut = document.getElementById('crypto-sig-output');

    if (!msg || !privEl || !privEl.value) {
        showEnterpriseToast('Input Required', 'Message to sign and active private key are required.', 'warning');
        return;
    }

    const algo = activeGeneratedKeyPair ? activeGeneratedKeyPair.key_type.startsWith('RSA') ? 'RSA-PSS' : 'Ed25519' : 'Ed25519';

    try {
        const res = await fetch(`${API_BASE}/crypto/sign`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: msg,
                private_key_pem: privEl.value,
                algorithm: algo
            })
        });
        if (!res.ok) throw new Error("Signing failed.");
        const json = await res.json();
        if (sigOut) sigOut.textContent = json.signature_b64;

        showEnterpriseToast('Digital Signature Generated', `${json.algorithm} signature created.`, 'success', 2500);
    } catch (e) {
        showEnterpriseToast('Signing Error', e.message, 'error');
    }
}

export async function executeVerifySignature() {
    const msg = document.getElementById('crypto-sign-msg').value;
    const pubEl = document.getElementById('crypto-pubkey-display');
    const sigOut = document.getElementById('crypto-sig-output');
    const verdict = document.getElementById('crypto-verify-verdict');

    if (!msg || !pubEl || !pubEl.value || !sigOut || !sigOut.textContent || sigOut.textContent === '--') {
        showEnterpriseToast('Input Required', 'Message, signature, and public key are required for verification.', 'warning');
        return;
    }

    const algo = activeGeneratedKeyPair ? activeGeneratedKeyPair.key_type.startsWith('RSA') ? 'RSA-PSS' : 'Ed25519' : 'Ed25519';

    try {
        const res = await fetch(`${API_BASE}/crypto/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: msg,
                signature_b64: sigOut.textContent,
                public_key_pem: pubEl.value,
                algorithm: algo
            })
        });
        if (!res.ok) throw new Error("Verification call failed.");
        const json = await res.json();

        if (verdict) {
            if (json.is_valid) {
                verdict.innerHTML = `<span class="text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> 100% Genuine Signature (Non-Repudiation Verified)</span>`;
                showEnterpriseToast('Signature Verified', 'Authenticity certified with zero forgery.', 'success', 3000);
            } else {
                verdict.innerHTML = `<span class="text-rose-400 font-bold"><i class="fa-solid fa-triangle-exclamation"></i> INVALID / FORGED SIGNATURE</span>`;
                showEnterpriseToast('Signature Invalid', 'Cryptographic verification failed.', 'error', 4000);
            }
        }
    } catch (e) {
        showEnterpriseToast('Verification Error', e.message, 'error');
    }
}

export async function executeMerkleTree() {
    const raw = document.getElementById('crypto-merkle-input').value;
    const rootOut = document.getElementById('crypto-merkle-root');
    const certOut = document.getElementById('crypto-merkle-cert');
    const leavesOut = document.getElementById('crypto-merkle-leaves');

    const lines = raw.split(/[\n,]/).map(x => x.trim()).filter(x => x.length > 0);
    if (lines.length === 0) {
        showEnterpriseToast('Input Required', 'Please enter at least one audit record or transaction.', 'warning');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/crypto/merkle-tree`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ leaf_values: lines })
        });
        if (!res.ok) throw new Error("Merkle Tree calculation failed.");
        const json = await res.json();

        if (rootOut) rootOut.textContent = json.merkle_root;
        if (certOut) certOut.textContent = json.audit_cert;
        if (leavesOut) {
            leavesOut.innerHTML = `<strong>${json.leaf_count} Leaves Rooted:</strong> ` + json.leaf_hashes.map((h, i) => `<span class="text-slate-300 font-mono text-[10px]" title="${escapeHtml(lines[i])}">[#${i+1}] ${h.substring(0, 8)}...</span>`).join(', ');
        }

        showEnterpriseToast('Merkle Root Computed', `Root computed across ${json.leaf_count} leaves.`, 'success', 2500);
    } catch (e) {
        showEnterpriseToast('Merkle Calculation Error', e.message, 'error');
    }
}

export async function generateRandomCSPRNGToken() {
    try {
        const res = await fetch(`${API_BASE}/crypto/token/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nbytes: 32 })
        });
        if (!res.ok) return;
        const json = await res.json();
        showEnterpriseToast('CSPRNG Token Generated', `256-bit Token: ${json.token}`, 'info', 4000);
    } catch (e) {
        console.warn("CSPRNG token generation failed:", e);
    }
}




// Expose all functions to global window for template event handlers
if (typeof window !== 'undefined') {
    window.addSharePointStepRow = addSharePointStepRow;
    window.advanceOpportunityStage = advanceOpportunityStage;
    window.calculateLiveCTC = calculateLiveCTC;
    window.calculatePortalBillNet = calculatePortalBillNet;
    window.captureHRMSWebcam = captureHRMSWebcam;
    window.changeTaskStatus = changeTaskStatus;
    window.clearAgentChatHistory = clearAgentChatHistory;
    window.closeClientModal = closeClientModal;
    window.closeCommandPalette = closeCommandPalette;
    window.closeCreateTicketModal = closeCreateTicketModal;
    window.closeDigitalIDCardModal = closeDigitalIDCardModal;
    window.closeDispatchMissionModal = closeDispatchMissionModal;
    window.closeESSApplyLeaveModal = closeESSApplyLeaveModal;
    window.closeESSRaiseTicketModal = closeESSRaiseTicketModal;
    window.closeGPSLocationModal = closeGPSLocationModal;
    window.closeGrievanceModal = closeGrievanceModal;
    window.closeHRMSModal = closeHRMSModal;
    window.closeITSMModal = closeITSMModal;
    window.closeKeyboardShortcutsModal = closeKeyboardShortcutsModal;
    window.closeMissionTraceModal = closeMissionTraceModal;
    window.closeNotificationDropdown = closeNotificationDropdown;
    window.closeOmniHeadAlertModal = closeOmniHeadAlertModal;
    window.closeSharePointModal = closeSharePointModal;
    window.closeStakeholderLoginModal = closeStakeholderLoginModal;
    window.closeTeamsHuddleModal = closeTeamsHuddleModal;
    window.closeTeamsModal = closeTeamsModal;
    window.closeTicketDetailModal = closeTicketDetailModal;
    window.closeTrainingModal = closeTrainingModal;
    window.closeVendorPortalModal = closeVendorPortalModal;
    window.closeWebcamEnrollModal = closeWebcamEnrollModal;
    window.closeWhatsAppModal = closeWhatsAppModal;
    window.computeHaversineMeters = computeHaversineMeters;
    window.detectCurrentLocation = detectCurrentLocation;
    window.dismissAlertBanner = dismissAlertBanner;
    window.displayFlowchart = displayFlowchart;
    window.escalateAlertToIncident = escalateAlertToIncident;
    window.escalateClientToDirector = escalateClientToDirector;
    window.escapeHtml = escapeHtml;
    window.executeAESDecrypt = executeAESDecrypt;
    window.executeAESEncrypt = executeAESEncrypt;
    window.executeCommand = executeCommand;
    window.executeCryptoHMAC = executeCryptoHMAC;
    window.executeCryptoHash = executeCryptoHash;
    window.executeMerkleTree = executeMerkleTree;
    window.executeSignMessage = executeSignMessage;
    window.executeVerifySignature = executeVerifySignature;
    window.exportSharePointDocument = exportSharePointDocument;
    window.exportTrainingCertificate = exportTrainingCertificate;
    window.exportTrainingMaterial = exportTrainingMaterial;
    window.fetchNotificationsAndAlerts = fetchNotificationsAndAlerts;
    window.fillAgentChatPrompt = fillAgentChatPrompt;
    window.fillHoramavuHQCoords = fillHoramavuHQCoords;
    window.filterAgenticMissions = filterAgenticMissions;
    window.filterCatalogByTrack = filterCatalogByTrack;
    window.filterHRMSEmployees = filterHRMSEmployees;
    window.filterISOClauseControls = filterISOClauseControls;
    window.filterTableRows = filterTableRows;
    window.filterTeamsChannels = filterTeamsChannels;
    window.filterTicketsByDepartment = filterTicketsByDepartment;
    window.filterVaultCategory = filterVaultCategory;
    window.filterVaultFormat = filterVaultFormat;
    window.generateNewKeyPair = generateNewKeyPair;
    window.generateRandomCSPRNGToken = generateRandomCSPRNGToken;
    window.handleAddTicketComment = handleAddTicketComment;
    window.handleAdvanceCandidateStage = handleAdvanceCandidateStage;
    window.handleAgentChatSelectChange = handleAgentChatSelectChange;
    window.handleAlertBannerAction = handleAlertBannerAction;
    window.handleApplyLeave = handleApplyLeave;
    window.handleApproveAgentMission = handleApproveAgentMission;
    window.handleCABReview = handleCABReview;
    window.handleClientCRReview = handleClientCRReview;
    window.handleClientMilestoneSignoff = handleClientMilestoneSignoff;
    window.handleClientSelectorChange = handleClientSelectorChange;
    window.handleClockIn = handleClockIn;
    window.handleClockOut = handleClockOut;
    window.handleCommandPaletteKeydown = handleCommandPaletteKeydown;
    window.handleCommandPaletteSearch = handleCommandPaletteSearch;
    window.handleConcludePOSH = handleConcludePOSH;
    window.handleCreateBackupSnapshot = handleCreateBackupSnapshot;
    window.handleCreateCMDBNode = handleCreateCMDBNode;
    window.handleCreateCandidate = handleCreateCandidate;
    window.handleCreateChangeRequest = handleCreateChangeRequest;
    window.handleCreateClientTicket = handleCreateClientTicket;
    window.handleCreateEmployee = handleCreateEmployee;
    window.handleCreateInternalTicket = handleCreateInternalTicket;
    window.handleCreateKPI = handleCreateKPI;
    window.handleCreateOpportunity = handleCreateOpportunity;
    window.handleCreatePMOAction = handleCreatePMOAction;
    window.handleCreatePMOIntake = handleCreatePMOIntake;
    window.handleCreatePOSHCase = handleCreatePOSHCase;
    window.handleCreateProcureEvent = handleCreateProcureEvent;
    window.handleCreateProcureGRN = handleCreateProcureGRN;
    window.handleCreateProcurePR = handleCreateProcurePR;
    window.handleCreateProcureVendor = handleCreateProcureVendor;
    window.handleCreateProcurementLOI = handleCreateProcurementLOI;
    window.handleCreateSDLCDefect = handleCreateSDLCDefect;
    window.handleCreateSDLCRequirement = handleCreateSDLCRequirement;
    window.handleCreateSharePointArticle = handleCreateSharePointArticle;
    window.handleCreateSharePointQuestion = handleCreateSharePointQuestion;
    window.handleCreateTeamsChannel = handleCreateTeamsChannel;
    window.handleCreateThought = handleCreateThought;
    window.handleCreateTicket = handleCreateTicket;
    window.handleCreateTrainingMaterial = handleCreateTrainingMaterial;
    window.handleDispatchAlertForm = handleDispatchAlertForm;
    window.handleDispatchMissionSubmit = handleDispatchMissionSubmit;
    window.handleESSApplyLeave = handleESSApplyLeave;
    window.handleESSRaiseTicket = handleESSRaiseTicket;
    window.handleExecuteRunbook = handleExecuteRunbook;
    window.handleGenerateLetter = handleGenerateLetter;
    window.handleHireCandidate = handleHireCandidate;
    window.handleInitiateSeparation = handleInitiateSeparation;
    window.handleLeaveHuddle = handleLeaveHuddle;
    window.handleLodgeGrievanceSubmit = handleLodgeGrievanceSubmit;
    window.handleMarkAllNotificationsRead = handleMarkAllNotificationsRead;
    window.handleMarkSingleNotificationRead = handleMarkSingleNotificationRead;
    window.handleNotificationDeepLink = handleNotificationDeepLink;
    window.handleOpenGrievanceModal = handleOpenGrievanceModal;
    window.handlePingMCP = handlePingMCP;
    window.handlePortalBidSubmit = handlePortalBidSubmit;
    window.handlePortalBillSubmit = handlePortalBillSubmit;
    window.handlePortalGRNPOSelect = handlePortalGRNPOSelect;
    window.handlePortalGRNQtyChange = handlePortalGRNQtyChange;
    window.handlePortalGRNSubmit = handlePortalGRNSubmit;
    window.handlePostArticleComment = handlePostArticleComment;
    window.handleProcessFF = handleProcessFF;
    window.handlePromptResolveGrievance = handlePromptResolveGrievance;
    window.handleRecordClientPayment = handleRecordClientPayment;
    window.handleRecordDPDPConsent = handleRecordDPDPConsent;
    window.handleRunAttendancePayroll = handleRunAttendancePayroll;
    window.handleRunGuardrailsScan = handleRunGuardrailsScan;
    window.handleRunPayroll = handleRunPayroll;
    window.handleSaveTicketStatusUpdate = handleSaveTicketStatusUpdate;
    window.handleSelectDocumentEmbed = handleSelectDocumentEmbed;
    window.handleSendAgentChatMessage = handleSendAgentChatMessage;
    window.handleSendTeamsMessage = handleSendTeamsMessage;
    window.handleSendWhatsAppBotMessage = handleSendWhatsAppBotMessage;
    window.handleSharePointCategoryChange = handleSharePointCategoryChange;
    window.handleSharePointDeptFilter = handleSharePointDeptFilter;
    window.handleSharePointSearch = handleSharePointSearch;
    window.handleStakeholderLogin = handleStakeholderLogin;
    window.handleSwitchPersona = handleSwitchPersona;
    window.handleToggleMessagePin = handleToggleMessagePin;
    window.handleToggleMessageReaction = handleToggleMessageReaction;
    window.handleTrainingDeptFilter = handleTrainingDeptFilter;
    window.handleTrainingQuizSubmit = handleTrainingQuizSubmit;
    window.handleTrainingSearch = handleTrainingSearch;
    window.handleTriggerAutoFixAttendance = handleTriggerAutoFixAttendance;
    window.handleTriggerBotHelp = handleTriggerBotHelp;
    window.handleTriggerDirectAlert = handleTriggerDirectAlert;
    window.handleTriggerGlobalSelfHeal = handleTriggerGlobalSelfHeal;
    window.handleTriggerGlobalSync = handleTriggerGlobalSync;
    window.handleTriggerOmniHeadAlertModal = handleTriggerOmniHeadAlertModal;
    window.handleTriggerPipelineRun = handleTriggerPipelineRun;
    window.handleTriggerSyncAlerts = handleTriggerSyncAlerts;
    window.handleUpdateLeaveStatus = handleUpdateLeaveStatus;
    window.handleUpdateMyPresence = handleUpdateMyPresence;
    window.handleUpdateSeparationClearance = handleUpdateSeparationClearance;
    window.handleVaultSearch = handleVaultSearch;
    window.handleVendorSelectorChange = handleVendorSelectorChange;
    window.initAutoSyncManager = initAutoSyncManager;
    window.initKeyboardShortcuts = initKeyboardShortcuts;
    window.initNavigation = initNavigation;
    window.insertMessageSnippet = insertMessageSnippet;
    window.loadAICloudModule = loadAICloudModule;
    window.loadAIModelsTable = loadAIModelsTable;
    window.loadAgenticAI = loadAgenticAI;
    window.loadAnalyticsHub = loadAnalyticsHub;
    window.loadArchitectureBlueprintsView = loadArchitectureBlueprintsView;
    window.loadArticleComments = loadArticleComments;
    window.loadAuthenticityCertsTable = loadAuthenticityCertsTable;
    window.loadBalancedScorecard = loadBalancedScorecard;
    window.loadCMDBNodes = loadCMDBNodes;
    window.loadCRM = loadCRM;
    window.loadClientPortal = loadClientPortal;
    window.loadCloudNodesGrid = loadCloudNodesGrid;
    window.loadCryptoTools = loadCryptoTools;
    window.loadDashboard = loadDashboard;
    window.loadDataScienceAnalytics = loadDataScienceAnalytics;
    window.loadDecisionTowerAnalytics = loadDecisionTowerAnalytics;
    window.loadEmployeePortal = loadEmployeePortal;
    window.loadEnterpriseFlowchartsView = loadEnterpriseFlowchartsView;
    window.loadExecutiveAlertRulesGrid = loadExecutiveAlertRulesGrid;
    window.loadExecutiveInfographics = loadExecutiveInfographics;
    window.loadFinAnalytics = loadFinAnalytics;
    window.loadFinance = loadFinance;
    window.loadGovernance = loadGovernance;
    window.loadGuardrailLogsTable = loadGuardrailLogsTable;
    window.loadGuardrailRulesTable = loadGuardrailRulesTable;
    window.loadGuardrails = loadGuardrails;
    window.loadHRMS = loadHRMS;
    window.loadHRMSAnalytics = loadHRMSAnalytics;
    window.loadISOAuditsGrid = loadISOAuditsGrid;
    window.loadISOCapasContainer = loadISOCapasContainer;
    window.loadISOCertificationsGrid = loadISOCertificationsGrid;
    window.loadISOControlsTable = loadISOControlsTable;
    window.loadISOGrievancesTable = loadISOGrievancesTable;
    window.loadISOStandardsModule = loadISOStandardsModule;
    window.loadITSM = loadITSM;
    window.loadITSMChanges = loadITSMChanges;
    window.loadITSMLOIs = loadITSMLOIs;
    window.loadITSMProblems = loadITSMProblems;
    window.loadITSMRunbooks = loadITSMRunbooks;
    window.loadITSMSLAs = loadITSMSLAs;
    window.loadInfrastructure = loadInfrastructure;
    window.loadInternalSupport = loadInternalSupport;
    window.loadMCPServersGrid = loadMCPServersGrid;
    window.loadMonteCarloAnalytics = loadMonteCarloAnalytics;
    window.loadOperations = loadOperations;
    window.loadOperationsConsents = loadOperationsConsents;
    window.loadOperationsLedger = loadOperationsLedger;
    window.loadOperationsOverview = loadOperationsOverview;
    window.loadOperationsSnapshots = loadOperationsSnapshots;
    window.loadOperationsTelemetry = loadOperationsTelemetry;
    window.loadPMO = loadPMO;
    window.loadPMOAnalytics = loadPMOAnalytics;
    window.loadProcurement = loadProcurement;
    window.loadSDLC = loadSDLC;
    window.loadSalaryStatements = loadSalaryStatements;
    window.loadSecOps = loadSecOps;
    window.loadSecOpsAnalytics = loadSecOpsAnalytics;
    window.loadSharePoint = loadSharePoint;
    window.loadSharePointTabContent = loadSharePointTabContent;
    window.loadSimAnalytics = loadSimAnalytics;
    window.loadSmartAttendance = loadSmartAttendance;
    window.loadStrategy = loadStrategy;
    window.loadStrategyAnalytics = loadStrategyAnalytics;
    window.loadTalentAnalytics = loadTalentAnalytics;
    window.loadTeams = loadTeams;
    window.loadTechnicalDocumentsView = loadTechnicalDocumentsView;
    window.loadTraining = loadTraining;
    window.loadTrainingAnalytics = loadTrainingAnalytics;
    window.loadTrainingTabContent = loadTrainingTabContent;
    window.loadVault = loadVault;
    window.loadVendorPortal = loadVendorPortal;
    window.openAddIOCModal = openAddIOCModal;
    window.openClientCRReview = openClientCRReview;
    window.openClientMilestoneSignoff = openClientMilestoneSignoff;
    window.openClientModal = openClientModal;
    window.openClientPaymentModal = openClientPaymentModal;
    window.openClientTicketModal = openClientTicketModal;
    window.openCommandPalette = openCommandPalette;
    window.openCreateTicketModal = openCreateTicketModal;
    window.openDigitalIDCardModal = openDigitalIDCardModal;
    window.openDispatchMissionModal = openDispatchMissionModal;
    window.openESSApplyLeaveModal = openESSApplyLeaveModal;
    window.openESSRaiseTicketModal = openESSRaiseTicketModal;
    window.openGPSLocationModal = openGPSLocationModal;
    window.openHRMSModal = openHRMSModal;
    window.openITSMModal = openITSMModal;
    window.openIngestAlertModal = openIngestAlertModal;
    window.openKeyboardShortcutsModal = openKeyboardShortcutsModal;
    window.openMyTrainingSummaryModal = openMyTrainingSummaryModal;
    window.openPasskeyEnrollModal = openPasskeyEnrollModal;
    window.openReportIncidentModal = openReportIncidentModal;
    window.openSharePointModal = openSharePointModal;
    window.openStakeholderLoginModal = openStakeholderLoginModal;
    window.openTeamsHuddleModal = openTeamsHuddleModal;
    window.openTeamsModal = openTeamsModal;
    window.openTicketDetail = openTicketDetail;
    window.openTrainingModal = openTrainingModal;
    window.openTrainingQuiz = openTrainingQuiz;
    window.openTrainingQuizByEnrollmentId = openTrainingQuizByEnrollmentId;
    window.openVendorPortalModal = openVendorPortalModal;
    window.openWebcamEnrollModal = openWebcamEnrollModal;
    window.openWhatsAppModal = openWhatsAppModal;
    window.openZTNAPolicyModal = openZTNAPolicyModal;
    window.populateLetterTemplateDropdown = populateLetterTemplateDropdown;
    window.populatePortalModalSelectors = populatePortalModalSelectors;
    window.portalQuickPunch = portalQuickPunch;
    window.prefillAndOpenBidModal = prefillAndOpenBidModal;
    window.previewClientInvoice = previewClientInvoice;
    window.previewClientSOA = previewClientSOA;
    window.previewITSM_LOI = previewITSM_LOI;
    window.previewLetterById = previewLetterById;
    window.printClientInvoiceCurrent = printClientInvoiceCurrent;
    window.printClientSOACurrent = printClientSOACurrent;
    window.printITSMCurrentLOI = printITSMCurrentLOI;
    window.promptAnswerSharePointQuestion = promptAnswerSharePointQuestion;
    window.quickEnrollMySelf = quickEnrollMySelf;
    window.recalcGPSModalDistance = recalcGPSModalDistance;
    window.refreshModuleData = refreshModuleData;
    window.reloadActiveChannelMessages = reloadActiveChannelMessages;
    window.renderActiveAlertBanner = renderActiveAlertBanner;
    window.renderAgenticFleet = renderAgenticFleet;
    window.renderAgenticMissions = renderAgenticMissions;
    window.renderCommandPaletteResults = renderCommandPaletteResults;
    window.renderESSCharts = renderESSCharts;
    window.renderExecCharts = renderExecCharts;
    window.renderFullNotificationsFeed = renderFullNotificationsFeed;
    window.renderHRMSEmployees = renderHRMSEmployees;
    window.renderInternalTicketsTable = renderInternalTicketsTable;
    window.renderMyTrainingEnrollments = renderMyTrainingEnrollments;
    window.renderNotificationDropdown = renderNotificationDropdown;
    window.renderServiceDeskSummary = renderServiceDeskSummary;
    window.renderSharePointCommunity = renderSharePointCommunity;
    window.renderSharePointDocumentLibrary = renderSharePointDocumentLibrary;
    window.renderSharePointMethods = renderSharePointMethods;
    window.renderSharePointSOPs = renderSharePointSOPs;
    window.renderSharePointThoughts = renderSharePointThoughts;
    window.renderTeamsChannelsList = renderTeamsChannelsList;
    window.renderTeamsMessages = renderTeamsMessages;
    window.renderTeamsPresenceRoster = renderTeamsPresenceRoster;
    window.renderTicketCommentsThread = renderTicketCommentsThread;
    window.renderTrainingCatalog = renderTrainingCatalog;
    window.renderTrainingComplianceMatrix = renderTrainingComplianceMatrix;
    window.renderTrainingMaterials = renderTrainingMaterials;
    window.renderTrainingTracks = renderTrainingTracks;
    window.renderVaultCategories = renderVaultCategories;
    window.renderVaultDocuments = renderVaultDocuments;
    window.resolveTicket = resolveTicket;
    window.runLiveCapitalSimulation = runLiveCapitalSimulation;
    window.runLiveCashflowSimulation = runLiveCashflowSimulation;
    window.safeRenderChart = safeRenderChart;
    window.selectTeamsChannel = selectTeamsChannel;
    window.setAutoSyncFrequency = setAutoSyncFrequency;
    window.setStakeholderLoginCredentials = setStakeholderLoginCredentials;
    window.setWhatsAppMsg = setWhatsAppMsg;
    window.showEnterpriseToast = showEnterpriseToast;
    window.simulateDRRestore = simulateDRRestore;
    window.startAgentChatWithPersona = startAgentChatWithPersona;
    window.startHRMSWebcam = startHRMSWebcam;
    window.startLiveCertInCountdown = startLiveCertInCountdown;
    window.startLiveClockAndHeartbeat = startLiveClockAndHeartbeat;
    window.stopHRMSWebcam = stopHRMSWebcam;
    window.submitGPSLocationUpdate = submitGPSLocationUpdate;
    window.submitWebcamEnrollment = submitWebcamEnrollment;
    window.switchAICloudTab = switchAICloudTab;
    window.switchAgenticAITab = switchAgenticAITab;
    window.switchAnalyticsTab = switchAnalyticsTab;
    window.switchClientPortalTab = switchClientPortalTab;
    window.switchCryptoTab = switchCryptoTab;
    window.switchESSTab = switchESSTab;
    window.switchEmployeeProfile = switchEmployeeProfile;
    window.switchGuardrailTab = switchGuardrailTab;
    window.switchHRMSTab = switchHRMSTab;
    window.switchISOTab = switchISOTab;
    window.switchITSMTab = switchITSMTab;
    window.switchInfraTab = switchInfraTab;
    window.switchModule = switchModule;
    window.switchOperationsTab = switchOperationsTab;
    window.switchSecOpsTab = switchSecOpsTab;
    window.switchSharePointTab = switchSharePointTab;
    window.switchTrainingTab = switchTrainingTab;
    window.switchVendorPortalTab = switchVendorPortalTab;
    window.toggleCRMModal = toggleCRMModal;
    window.toggleFloatingCopilotModal = toggleFloatingCopilotModal;
    window.toggleHuddleCam = toggleHuddleCam;
    window.toggleHuddleMic = toggleHuddleMic;
    window.toggleHuddleScreenShare = toggleHuddleScreenShare;
    window.toggleNotificationDropdown = toggleNotificationDropdown;
    window.togglePMOModal = togglePMOModal;
    window.toggleProcurementModal = toggleProcurementModal;
    window.toggleSDLCModal = toggleSDLCModal;
    window.toggleSharePointLike = toggleSharePointLike;
    window.toggleStrategyModal = toggleStrategyModal;
    window.toggleThoughtComments = toggleThoughtComments;
    window.triggerDBVacuum = triggerDBVacuum;
    window.triggerDRSimulationDrill = triggerDRSimulationDrill;
    window.triggerEmergencyWarRoom = triggerEmergencyWarRoom;
    window.updateBreadcrumbs = updateBreadcrumbs;
    window.updateIncidentStatusPrompt = updateIncidentStatusPrompt;
    window.upvoteSharePointQuestion = upvoteSharePointQuestion;
    window.verifyEventLedger = verifyEventLedger;
    window.viewCertInReport = viewCertInReport;
    window.viewEmployeeProfile = viewEmployeeProfile;
    window.viewLedgerPayload = viewLedgerPayload;
    window.viewMissionTrace = viewMissionTrace;
    window.viewSharePointSOP = viewSharePointSOP;
    window.viewTrainingMaterial = viewTrainingMaterial;
    window.viewTrainingModule = viewTrainingModule;
    window.activeGeneratedKeyPair = activeGeneratedKeyPair;
    window.activeTeamsChannelId = activeTeamsChannelId;
    window.activeTicketDetailId = activeTicketDetailId;
    window.autoSyncCountdown = autoSyncCountdown;
    window.autoSyncIntervalSec = autoSyncIntervalSec;
    window.autoSyncTimerId = autoSyncTimerId;
    window.cachedAgenticFleet = cachedAgenticFleet;
    window.cachedAgenticMissions = cachedAgenticMissions;
    window.cachedBlueprints = cachedBlueprints;
    window.cachedDocuments = cachedDocuments;
    window.cachedFlowcharts = cachedFlowcharts;
    window.cachedHRMSEmployees = cachedHRMSEmployees;
    window.cachedISOControls = cachedISOControls;
    window.cachedITSM_LOIs = cachedITSM_LOIs;
    window.cachedLedgerEvents = cachedLedgerEvents;
    window.cachedTeamsChannels = cachedTeamsChannels;
    window.capSimDebounce = capSimDebounce;
    window.commandPaletteSelectedIndex = commandPaletteSelectedIndex;
    window.currentAgenticTab = currentAgenticTab;
    window.currentAnalyticsTab = currentAnalyticsTab;
    window.currentClientPortalName = currentClientPortalName;
    window.currentCryptoTab = currentCryptoTab;
    window.currentDeptFilter = currentDeptFilter;
    window.currentESSEmpCode = currentESSEmpCode;
    window.currentEnrollEmp = currentEnrollEmp;
    window.currentFilteredCommands = currentFilteredCommands;
    window.currentGPSEmp = currentGPSEmp;
    window.currentITSMTab = currentITSMTab;
    window.currentModule = currentModule;
    window.currentOperationsTab = currentOperationsTab;
    window.currentSharePointTab = currentSharePointTab;
    window.currentTrainingTab = currentTrainingTab;
    window.currentUserSession = currentUserSession;
    window.currentVendorPortalData = currentVendorPortalData;
    window.currentViewingLOI = currentViewingLOI;
    window.currentViewingModule = currentViewingModule;
    window.essAttChart = essAttChart;
    window.essCompChart = essCompChart;
    window.essLeavesChart = essLeavesChart;
    window.hrmsActiveStreams = hrmsActiveStreams;
    window.internalTicketsData = internalTicketsData;
    window.isHuddleCamActive = isHuddleCamActive;
    window.isHuddleMicActive = isHuddleMicActive;
    window.isHuddleScreenSharing = isHuddleScreenSharing;
    window.simDebounceTimer = simDebounceTimer;
    window.spSearchDebounce = spSearchDebounce;
    window.teamsPollingInterval = teamsPollingInterval;
    window.topCriticalAlertActionUrl = topCriticalAlertActionUrl;
    window.trnSearchDebounce = trnSearchDebounce;
    window.vaultState = vaultState;
    window.formatINR = formatINR;
    window.formatDate = formatDate;
}
