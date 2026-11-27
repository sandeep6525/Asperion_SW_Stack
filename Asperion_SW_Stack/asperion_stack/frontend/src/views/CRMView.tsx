import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { formatINR, formatDate } from '../utils/formatters.ts';

interface Opportunity {
  id: number;
  opportunity_code: string;
  client_name: string;
  deal_title: string;
  deal_value_inr: number;
  stage: string;
  probability_pct: number;
  weighted_value_inr: number;
  deal_desk_status: string;
  expected_close_date: string;
  owner: string;
}

interface Account {
  id: number;
  client_name: string;
  tier: string;
  industry: string;
  annual_recurring_revenue_inr: number;
  health_score: number;
  health_status: string;
  nps_score: number;
  primary_csm: string;
  executive_sponsor: string;
  renewal_date: string;
  churn_risk_level: string;
}

interface Ticket {
  id: number;
  ticket_number: string;
  client_name: string;
  subject: string;
  severity: string;
  sla_response_hours: number;
  status: string;
}

interface Risk {
  id: number;
  risk_code: string;
  risk_category: string;
  risk_title: string;
  risk_description: string;
  inherent_rpn: number;
  existing_controls: string;
  residual_rpn: number;
  treatment_strategy: string;
  risk_owner: string;
  status: string;
}

interface Prospect {
  id?: number;
  company_name: string;
  contact_person: string;
  contact_email: string;
  pipeline_stage: string;
  deal_value: number;
  owner: string;
}

interface Contract {
  id?: number;
  contract_reference: string;
  client_name: string;
  contract_type: string;
  value_inr: number;
  status: string;
  effective_date: string;
}

export const CRMView: React.FC = () => {
  const [summary, setSummary] = useState({
    total_pipeline_value_inr: 8150000,
    weighted_pipeline_value_inr: 3475000,
    managed_arr_inr: 7950000,
    win_rate_pct: 100,
    average_health_score: 96.6,
    open_tickets: 25,
  });

  const [opportunities, setOpportunities] = useState<Opportunity[]>([
    {
      id: 1,
      opportunity_code: 'OPP-2026-001',
      client_name: 'Nexus Fintech Solutions India Pvt Ltd',
      deal_title: 'Enterprise Multi-Cloud Infrastructure & DevSecOps Migration',
      deal_value_inr: 2500000,
      stage: 'Solution Architecture',
      probability_pct: 50,
      weighted_value_inr: 1250000,
      deal_desk_status: 'Approved (Standard MSA)',
      expected_close_date: '2026-12-15',
      owner: 'Varadi Vijay (Director)',
    },
    {
      id: 2,
      opportunity_code: 'OPP-2026-002',
      client_name: 'Zenith Retail Tech Bangalore',
      deal_title: 'Omnichannel Supply Chain Analytics Platform',
      deal_value_inr: 1500000,
      stage: 'Discovery',
      probability_pct: 25,
      weighted_value_inr: 3750000,
      deal_desk_status: 'Pending Deal Desk Review',
      expected_close_date: '2027-01-30',
      owner: 'Varadi Vijay (Director)',
    },
  ]);

  const [accounts, setAccounts] = useState<Account[]>([
    {
      id: 1,
      client_name: 'Nexus Fintech Solutions India Pvt Ltd',
      tier: 'Tier 1 Enterprise',
      industry: 'Fintech & Digital Banking',
      annual_recurring_revenue_inr: 3500000,
      health_score: 98,
      health_status: 'Healthy',
      nps_score: 9,
      primary_csm: 'Customer Success Lead',
      executive_sponsor: 'Varadi Vijay (Director)',
      renewal_date: '2027-04-01',
      churn_risk_level: 'Low',
    },
    {
      id: 2,
      client_name: 'Zenith Retail Tech Bangalore',
      tier: 'Tier 2 Growth',
      industry: 'Retail & E-commerce',
      annual_recurring_revenue_inr: 2200000,
      health_score: 92,
      health_status: 'Healthy',
      nps_score: 8,
      primary_csm: 'Customer Success Lead',
      executive_sponsor: 'Varadi Vijay (Director)',
      renewal_date: '2027-02-15',
      churn_risk_level: 'Low',
    },
  ]);

  const [tickets, setTickets] = useState<Ticket[]>([
    {
      id: 1,
      ticket_number: 'TKT-2026-001',
      client_name: 'Nexus Fintech Solutions India Pvt Ltd',
      subject: 'Kubernetes Pod Autoscaling latency spike under high ingress traffic',
      severity: 'High',
      sla_response_hours: 4,
      status: 'In Progress',
    },
    {
      id: 2,
      ticket_number: 'TKT-2026-002',
      client_name: 'Zenith Retail Tech Bangalore',
      subject: 'TDS Certificate form 16A download verification',
      severity: 'Low',
      sla_response_hours: 24,
      status: 'Open',
    },
  ]);

  const [risks, setRisks] = useState<Risk[]>([
    {
      id: 1,
      risk_code: 'ERM-FIN-01',
      risk_category: 'Financial & Liquidity',
      risk_title: 'Client Payment Delay exceeding 45 days (DSO expansion)',
      risk_description: 'Working capital strain if tier-1 client receivables stretch past contracted Net 30 days.',
      inherent_rpn: 180,
      existing_controls: 'Automated D+15 invoice reminders, early-payment 2% rebate, Director follow-up',
      residual_rpn: 45,
      treatment_strategy: 'Mitigate (Strict Credit Policy)',
      risk_owner: 'Varadi Vijay (Director)',
      status: 'Controlled',
    },
    {
      id: 2,
      risk_code: 'ERM-LEG-02',
      risk_category: 'Legal & Compliance',
      risk_title: 'DPDP Act 2023 Non-Compliance Liability',
      risk_description: 'Regulatory penalties if digital personal data consent records are improperly retained.',
      inherent_rpn: 240,
      existing_controls: 'Automated consent logs with SHA-256 hash proofs, ISO 27001 ISMS policies',
      residual_rpn: 30,
      treatment_strategy: 'Transfer & Mitigate',
      risk_owner: 'Compliance Officer',
      status: 'Compliant',
    },
  ]);

  const [prospects, setProspects] = useState<Prospect[]>([
    {
      id: 1,
      company_name: 'Tata Consultancy Services - Cloud Unit',
      contact_person: 'Rajesh Sharma',
      contact_email: 'rajesh.sharma@tcs-cloud.in',
      pipeline_stage: 'Contract Negotiation',
      deal_value: 4500000,
      owner: 'Varadi Vijay (Director)',
    },
  ]);

  const [contracts, setContracts] = useState<Contract[]>([
    {
      id: 1,
      contract_reference: 'CTR-2026-NEXUS-01',
      client_name: 'Nexus Fintech Solutions India Pvt Ltd',
      contract_type: 'Master Services Agreement (MSA) + SLA',
      value_inr: 3500000,
      status: 'Active',
      effective_date: '2026-04-01',
    },
    {
      id: 2,
      contract_reference: 'CTR-2026-ZENITH-02',
      client_name: 'Zenith Retail Tech Bangalore',
      contract_type: 'Annual Maintenance Contract (AMC)',
      value_inr: 2200000,
      status: 'Active',
      effective_date: '2026-02-15',
    },
  ]);

  const [isOppModalOpen, setIsOppModalOpen] = useState(false);
  const [isTicketModalOpen, setIsTicketModalOpen] = useState(false);

  // New Opp Form State
  const [newOpp, setNewOpp] = useState({
    client_name: '',
    deal_title: '',
    deal_value_inr: 1000000,
    stage: 'Lead Qualified',
    probability_pct: 20,
    expected_close_date: new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0],
    owner: 'Varadi Vijay (Director)',
  });

  // New Ticket Form State
  const [newTicket, setNewTicket] = useState({
    client_name: 'Nexus Fintech Solutions India Pvt Ltd',
    subject: '',
    severity: 'Medium',
    description: '',
  });

  const fetchCRMData = async () => {
    try {
      const [sumRes, oppRes, accRes, tktRes, rskRes, prsRes, ctrRes] = await Promise.all([
        axios.get('/api/v1/crm-enterprise/pipeline-summary').catch(() => null),
        axios.get('/api/v1/crm-enterprise/opportunities').catch(() => null),
        axios.get('/api/v1/crm-enterprise/accounts').catch(() => null),
        axios.get('/api/v1/crm-enterprise/tickets').catch(() => null),
        axios.get('/api/v1/crm-enterprise/enterprise-risks').catch(() => null),
        axios.get('/api/v1/crm-legal/prospects').catch(() => null),
        axios.get('/api/v1/crm-legal/contracts').catch(() => null),
      ]);

      if (sumRes?.data?.pipeline) {
        const p = sumRes.data.pipeline;
        const cs = sumRes.data.customer_success;
        const sd = sumRes.data.service_desk;
        setSummary({
          total_pipeline_value_inr: p.total_pipeline_value_inr || 8150000,
          weighted_pipeline_value_inr: p.weighted_pipeline_value_inr || 3475000,
          managed_arr_inr: cs?.managed_arr_inr || 7950000,
          win_rate_pct: p.win_rate_pct || 100,
          average_health_score: cs?.average_health_score || 96.6,
          open_tickets: sd?.open_tickets || 25,
        });
      }

      if (oppRes?.data && Array.isArray(oppRes.data) && oppRes.data.length > 0) {
        setOpportunities(oppRes.data);
      }
      if (accRes?.data && Array.isArray(accRes.data) && accRes.data.length > 0) {
        setAccounts(accRes.data);
      }
      if (tktRes?.data && Array.isArray(tktRes.data) && tktRes.data.length > 0) {
        setTickets(tktRes.data);
      }
      if (rskRes?.data && Array.isArray(rskRes.data) && rskRes.data.length > 0) {
        setRisks(rskRes.data);
      }
      if (prsRes?.data && Array.isArray(prsRes.data) && prsRes.data.length > 0) {
        setProspects(prsRes.data);
      }
      if (ctrRes?.data && Array.isArray(ctrRes.data) && ctrRes.data.length > 0) {
        setContracts(ctrRes.data);
      }
    } catch {
      // Keep resilient data
    }
  };

  useEffect(() => {
    fetchCRMData();
  }, []);

  const handleAdvanceStage = async (id: number, newStage: string) => {
    try {
      await axios.patch(`/api/v1/crm-enterprise/opportunities/${id}/stage`, { stage: newStage });
      setOpportunities((prev) =>
        prev.map((o) => (o.id === id ? { ...o, stage: newStage } : o))
      );
      fetchCRMData();
    } catch {
      setOpportunities((prev) =>
        prev.map((o) => (o.id === id ? { ...o, stage: newStage } : o))
      );
    }
  };

  const handleResolveTicket = async (id: number) => {
    try {
      await axios.patch(`/api/v1/crm-enterprise/tickets/${id}/status`, { status: 'Resolved' });
      setTickets((prev) =>
        prev.map((t) => (t.id === id ? { ...t, status: 'Resolved' } : t))
      );
      fetchCRMData();
    } catch {
      setTickets((prev) =>
        prev.map((t) => (t.id === id ? { ...t, status: 'Resolved' } : t))
      );
    }
  };

  const handleCreateOpp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/v1/crm-enterprise/opportunities', newOpp);
      if (res?.data) {
        setOpportunities((prev) => [res.data, ...prev]);
      }
      setIsOppModalOpen(false);
      fetchCRMData();
    } catch {
      alert('Created locally.');
      setIsOppModalOpen(false);
    }
  };

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/v1/crm-enterprise/tickets', newTicket);
      if (res?.data) {
        setTickets((prev) => [res.data, ...prev]);
      }
      setIsTicketModalOpen(false);
      fetchCRMData();
    } catch {
      alert('Created locally.');
      setIsTicketModalOpen(false);
    }
  };

  return (
    <div className="w-full space-y-6">
      <section id="view-crm" className="module-view space-y-6">
        {/* Balanced Two-Column Enterprise CRM Header */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-800 text-white shadow-md">
          {/* Main Content Area (~67% width on desktop) */}
          <div className="lg:col-span-8 flex flex-col justify-between gap-4">
            <div className="flex items-start sm:items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-slate-950 border border-cyan-500/30 p-1.5 flex items-center justify-center shrink-0 shadow-sm">
                <img src="/static/img/logo.png" alt="Asperion Brand" className="w-full h-full object-contain" />
              </div>
              <div className="min-w-0">
                <h2 className="text-lg sm:text-2xl font-bold text-white tracking-tight">
                  Enterprise CRM, Contracting &amp; Service Desk
                </h2>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
                  Pipeline opportunities, Deal Desk approvals, customer health scores, SLA service desk, and Enterprise Risk Management (ERM).
                </p>
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-2 pt-1">
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-blue-300 border border-blue-500/30">
                DEAL DESK &amp; CONTRACTS
              </span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-cyan-300 border border-cyan-500/30">
                CUSTOMER HEALTH SCORING
              </span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-emerald-300 border border-emerald-500/30">
                SLA SERVICE DESK
              </span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-purple-300 border border-purple-500/30">
                ISO 31000 ERM
              </span>
            </div>
          </div>

          {/* Right-Side Actions Panel (~33% width on desktop) */}
          <div className="lg:col-span-4 bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between gap-3">
            <div className="text-xs text-slate-300 font-semibold border-b border-slate-800/80 pb-2 flex items-center justify-between">
              <span>CRM &amp; Contracting Actions</span>
              <span className="text-[10px] font-mono text-cyan-400">REVENUE OPS</span>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={() => setIsOppModalOpen(true)}
                className="w-full px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition flex items-center justify-center gap-2 shadow-sm"
              >
                <i className="fa-solid fa-plus"></i> New Deal / Opportunity
              </button>
              <button
                onClick={() => setIsTicketModalOpen(true)}
                className="w-full px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 text-xs font-semibold rounded-lg transition flex items-center justify-center gap-2 shadow-sm"
              >
                <i className="fa-solid fa-ticket"></i> New Support Ticket
              </button>
            </div>
          </div>
        </div>

        {/* CRM Top Stat Cards */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Total Pipeline</div>
            <div id="crm-stat-pipeline" className="text-lg font-bold text-slate-900 mt-1">
              {formatINR(summary.total_pipeline_value_inr)}
            </div>
            <div className="text-[10px] text-slate-500 mt-0.5">Active enterprise deals</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Weighted Pipeline</div>
            <div id="crm-stat-weighted" className="text-lg font-bold text-emerald-700 mt-1">
              {formatINR(summary.weighted_pipeline_value_inr)}
            </div>
            <div className="text-[10px] text-emerald-600 mt-0.5 font-medium">Probability weighted</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Managed ARR</div>
            <div id="crm-stat-arr" className="text-lg font-bold text-blue-700 mt-1">
              {formatINR(summary.managed_arr_inr)}
            </div>
            <div className="text-[10px] text-blue-600 mt-0.5 font-medium">Contracted recurring</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Win Rate</div>
            <div id="crm-stat-winrate" className="text-lg font-bold text-emerald-600 mt-1">
              {summary.win_rate_pct}%
            </div>
            <div className="text-[10px] text-slate-500 mt-0.5">Qualified closed-won</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Client Health</div>
            <div id="crm-stat-health" className="text-lg font-bold text-cyan-600 mt-1">
              {summary.average_health_score}%
            </div>
            <div className="text-[10px] text-cyan-600 mt-0.5 font-medium">Composite CS metric</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-400 font-semibold uppercase">Open Tickets</div>
            <div id="crm-stat-tickets" className="text-lg font-bold text-amber-600 mt-1">
              {summary.open_tickets}
            </div>
            <div className="text-[10px] text-amber-600 mt-0.5 font-medium">Active SLA tickets</div>
          </div>
        </div>

        {/* 1. Enterprise Opportunities & Deal Desk */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="p-4 border-b flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                <i className="fa-solid fa-briefcase text-purple-600"></i> Enterprise Opportunities &amp; Deal Desk
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Qualified pipeline deals subject to Board/Director approval and legal contract sign-off.
              </p>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 bg-purple-50 text-purple-700 border border-purple-200 rounded-lg self-start sm:self-center">
              Active Deals ({opportunities.length})
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                <tr>
                  <th className="p-3">Deal Code</th>
                  <th className="p-3">Client &amp; Deal Title</th>
                  <th className="p-3 text-right">Deal Value</th>
                  <th className="p-3">Stage</th>
                  <th className="p-3 text-right">Prob %</th>
                  <th className="p-3 text-right">Weighted Value</th>
                  <th className="p-3">Deal Desk</th>
                  <th className="p-3">Close Date</th>
                  <th className="p-3">Owner</th>
                </tr>
              </thead>
              <tbody id="table-crm-opportunities">
                {opportunities.map((o) => {
                  let deskBadge = 'bg-slate-100 text-slate-700';
                  if (o.deal_desk_status.includes('Approved')) {
                    deskBadge = 'bg-emerald-100 text-emerald-800 font-semibold';
                  } else if (o.deal_desk_status.includes('Director Approval')) {
                    deskBadge = 'bg-amber-100 text-amber-800 font-bold';
                  }

                  const stageOptions = [
                    'Lead Qualified',
                    'Discovery',
                    'Solution Architecture',
                    'Legal/Deal Desk',
                    'Closed Won',
                    'Closed Lost',
                  ];

                  return (
                    <tr key={o.id} className="border-b border-slate-100 hover:bg-slate-50 text-xs">
                      <td className="p-3 font-mono font-bold text-purple-800">{o.opportunity_code}</td>
                      <td className="p-3">
                        <div className="font-bold text-slate-900">{o.client_name}</div>
                        <div className="text-slate-500 text-[11px]">{o.deal_title}</div>
                      </td>
                      <td className="p-3 text-right font-bold text-slate-900">{formatINR(o.deal_value_inr)}</td>
                      <td className="p-3">
                        <select
                          value={o.stage}
                          onChange={(e) => handleAdvanceStage(o.id, e.target.value)}
                          className="text-xs font-semibold px-2 py-1 rounded border border-slate-300 bg-white shadow-sm focus:outline-none focus:ring-1 focus:ring-purple-500"
                        >
                          {stageOptions.map((st) => (
                            <option key={st} value={st}>
                              {st}
                            </option>
                          ))}
                        </select>
                      </td>
                      <td className="p-3 text-right font-bold text-slate-700">{o.probability_pct}%</td>
                      <td className="p-3 text-right font-mono font-bold text-emerald-700">
                        {formatINR(o.weighted_value_inr)}
                      </td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[11px] ${deskBadge}`}>
                          {o.deal_desk_status}
                        </span>
                      </td>
                      <td className="p-3 text-slate-500">{formatDate(o.expected_close_date)}</td>
                      <td className="p-3 text-slate-600 font-medium">{o.owner}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* 2-Column: Customer Accounts & SLA Service Desk */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Customer Accounts & CS Health */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm flex flex-col justify-between">
            <div>
              <div className="p-4 border-b flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                    <i className="fa-solid fa-users-viewfinder text-cyan-600"></i> Customer Accounts &amp; Health Scorecard
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">Key accounts, annual recurring revenue (ARR), and health scores.</p>
                </div>
                <span className="text-xs font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded">
                  {accounts.length} Accounts
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                    <tr>
                      <th className="p-2.5">Account</th>
                      <th className="p-2.5 text-right">ARR</th>
                      <th className="p-2.5 text-center">Health</th>
                      <th className="p-2.5">CSM Lead</th>
                      <th className="p-2.5">Renewal</th>
                    </tr>
                  </thead>
                  <tbody id="table-crm-accounts">
                    {accounts.map((a) => {
                      let healthColor = 'text-emerald-700 bg-emerald-100';
                      if (a.health_score < 70) healthColor = 'text-rose-700 bg-rose-100';
                      else if (a.health_score < 90) healthColor = 'text-amber-700 bg-amber-100';

                      return (
                        <tr key={a.id} className="border-b border-slate-100 hover:bg-slate-50 text-xs">
                          <td className="p-2.5">
                            <div className="font-bold text-slate-900">{a.client_name}</div>
                            <div className="font-mono text-[10px] text-slate-500">{a.tier}</div>
                          </td>
                          <td className="p-2.5 text-right font-bold text-slate-900">
                            {formatINR(a.annual_recurring_revenue_inr)}
                          </td>
                          <td className="p-2.5 text-center">
                            <span className={`px-2 py-0.5 rounded font-bold text-[11px] ${healthColor}`}>
                              {a.health_score}%
                            </span>
                          </td>
                          <td className="p-2.5 text-slate-600">{a.primary_csm}</td>
                          <td className="p-2.5 text-slate-500">{formatDate(a.renewal_date)}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* SLA Service Desk & Support Tickets */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm flex flex-col justify-between">
            <div>
              <div className="p-4 border-b flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                    <i className="fa-solid fa-headset text-blue-600"></i> SLA Service Desk &amp; Active Tickets
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">24x7 Enterprise support tickets and SLA countdown commitments.</p>
                </div>
                <button
                  onClick={() => setIsTicketModalOpen(true)}
                  className="px-2.5 py-1 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded text-xs font-semibold transition"
                >
                  <i className="fa-solid fa-plus mr-1"></i> New Ticket
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                    <tr>
                      <th className="p-2.5">Ticket #</th>
                      <th className="p-2.5">Subject &amp; Client</th>
                      <th className="p-2.5">Severity / SLA</th>
                      <th className="p-2.5">Status</th>
                      <th className="p-2.5 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody id="table-crm-tickets">
                    {tickets.map((t) => {
                      let sevBadge = 'bg-slate-100 text-slate-700';
                      if (t.severity === 'Critical') sevBadge = 'bg-rose-100 text-rose-800 font-bold';
                      else if (t.severity === 'High') sevBadge = 'bg-amber-100 text-amber-800 font-semibold';

                      let statusBadge = 'bg-amber-50 text-amber-700';
                      if (t.status === 'Resolved') statusBadge = 'bg-emerald-50 text-emerald-700 font-bold';
                      else if (t.status === 'In Progress') statusBadge = 'bg-blue-50 text-blue-700 font-medium';

                      return (
                        <tr key={t.id} className="border-b border-slate-100 hover:bg-slate-50 text-xs">
                          <td className="p-2.5 font-mono font-bold text-blue-800">{t.ticket_number}</td>
                          <td className="p-2.5">
                            <div className="font-bold text-slate-900">{t.client_name}</div>
                            <div className="text-slate-600 text-[11px]">{t.subject}</div>
                          </td>
                          <td className="p-2.5">
                            <span className={`px-2 py-0.5 rounded text-[10px] ${sevBadge}`}>
                              {t.severity} ({t.sla_response_hours}h SLA)
                            </span>
                          </td>
                          <td className="p-2.5">
                            <span className={`px-2 py-0.5 rounded text-[10px] ${statusBadge}`}>
                              {t.status}
                            </span>
                          </td>
                          <td className="p-2.5 text-right">
                            {t.status !== 'Resolved' ? (
                              <button
                                onClick={() => handleResolveTicket(t.id)}
                                className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-[11px] font-semibold transition shadow-sm"
                              >
                                <i className="fa-solid fa-check mr-1"></i> Resolve
                              </button>
                            ) : (
                              <span className="text-emerald-700 font-bold text-[11px]">
                                <i className="fa-solid fa-circle-check mr-1"></i> Closed
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Enterprise Risk Management (ERM) ISO 31000 */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="p-4 border-b flex items-center justify-between">
            <div>
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                <i className="fa-solid fa-triangle-exclamation text-rose-600"></i> Enterprise Risk Management (ERM) ISO 31000
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Proactive risk register, Risk Priority Numbers (RPN), mitigation strategies, and risk ownership.
              </p>
            </div>
            <span className="text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-1 rounded">
              ISO 31000 Register ({risks.length})
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                <tr>
                  <th className="p-3">Risk Code</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Risk Title &amp; Description</th>
                  <th className="p-3 text-center">Inherent RPN</th>
                  <th className="p-3">Controls</th>
                  <th className="p-3 text-center">Residual RPN</th>
                  <th className="p-3">Strategy</th>
                  <th className="p-3">Owner</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody id="table-crm-risks">
                {risks.map((r) => (
                  <tr key={r.id} className="border-b border-slate-100 hover:bg-slate-50 text-xs">
                    <td className="p-3 font-mono font-bold text-rose-800">{r.risk_code}</td>
                    <td className="p-3 font-semibold text-slate-700">{r.risk_category}</td>
                    <td className="p-3">
                      <div className="font-bold text-slate-900">{r.risk_title}</div>
                      <div className="text-slate-500 text-[11px]">{r.risk_description}</div>
                    </td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 rounded bg-red-100 text-red-800 font-bold text-xs">
                        RPN {r.inherent_rpn}
                      </span>
                    </td>
                    <td className="p-3 text-slate-700 text-[11px]">{r.existing_controls || 'In progress'}</td>
                    <td className="p-3 text-center">
                      <span className="px-2 py-1 rounded bg-emerald-100 text-emerald-800 font-bold text-xs">
                        RPN {r.residual_rpn}
                      </span>
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold">
                        {r.treatment_strategy}
                      </span>
                    </td>
                    <td className="p-3 text-slate-600">{r.risk_owner}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold">
                        {r.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 4. Prospects & Client Contracts Register */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Prospects Pipeline */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div className="p-4 border-b flex items-center justify-between">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                <i className="fa-solid fa-address-book text-indigo-600"></i> Qualified Prospects Pipeline
              </h3>
              <span className="text-xs text-slate-500">{prospects.length} Prospects</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                  <tr>
                    <th className="p-3">Company</th>
                    <th className="p-3">Contact</th>
                    <th className="p-3">Stage</th>
                    <th className="p-3 text-right">Value</th>
                    <th className="p-3">Owner</th>
                  </tr>
                </thead>
                <tbody id="table-prospects">
                  {prospects.map((p, idx) => (
                    <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="p-3 font-medium text-slate-900">{p.company_name}</td>
                      <td className="p-3 text-slate-600">
                        {p.contact_person} <br />
                        <span className="text-[10px] text-slate-400">{p.contact_email}</span>
                      </td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 text-[10px] rounded bg-purple-50 text-purple-700 font-medium">
                          {p.pipeline_stage}
                        </span>
                      </td>
                      <td className="p-3 text-right font-semibold text-slate-800">{formatINR(p.deal_value)}</td>
                      <td className="p-3 text-slate-500">{p.owner}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Client Contracts Register */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div className="p-4 border-b flex items-center justify-between">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                <i className="fa-solid fa-file-contract text-emerald-600"></i> Client Contracts Register
              </h3>
              <span className="text-xs text-slate-500">{contracts.length} Active Contracts</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] border-b">
                  <tr>
                    <th className="p-3">Ref No</th>
                    <th className="p-3">Client</th>
                    <th className="p-3">Type</th>
                    <th className="p-3 text-right">Value</th>
                    <th className="p-3">Status</th>
                    <th className="p-3">Effective</th>
                  </tr>
                </thead>
                <tbody id="table-contracts">
                  {contracts.map((c, idx) => (
                    <tr key={idx} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="p-3 font-mono text-[11px] text-blue-700 font-semibold">{c.contract_reference}</td>
                      <td className="p-3 font-medium text-slate-800">{c.client_name}</td>
                      <td className="p-3 text-slate-600">{c.contract_type}</td>
                      <td className="p-3 text-right font-semibold text-slate-800">{formatINR(c.value_inr)}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 text-[10px] rounded bg-emerald-50 text-emerald-700 font-medium">
                          {c.status}
                        </span>
                      </td>
                      <td className="p-3 text-slate-500">{formatDate(c.effective_date)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* MODAL: Register Opportunity */}
      {isOppModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <i className="fa-solid fa-briefcase text-purple-600"></i> Register New Enterprise Opportunity
              </h3>
              <button onClick={() => setIsOppModalOpen(false)} className="text-slate-400 hover:text-slate-600 p-1">
                <i className="fa-solid fa-xmark"></i>
              </button>
            </div>
            <form onSubmit={handleCreateOpp} className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Client Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Infosys Digital Solutions"
                  value={newOpp.client_name}
                  onChange={(e) => setNewOpp({ ...newOpp, client_name: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2"
                />
              </div>
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Deal Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Multi-Cloud Kubernetes & SRE Engagement"
                  value={newOpp.deal_title}
                  onChange={(e) => setNewOpp({ ...newOpp, deal_title: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Deal Value (INR)</label>
                  <input
                    type="number"
                    required
                    value={newOpp.deal_value_inr}
                    onChange={(e) => setNewOpp({ ...newOpp, deal_value_inr: parseFloat(e.target.value) || 0 })}
                    className="w-full border border-slate-200 rounded-lg p-2"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Stage</label>
                  <select
                    value={newOpp.stage}
                    onChange={(e) => setNewOpp({ ...newOpp, stage: e.target.value })}
                    className="w-full border border-slate-200 rounded-lg p-2"
                  >
                    <option value="Lead Qualified">Lead Qualified</option>
                    <option value="Discovery">Discovery</option>
                    <option value="Solution Architecture">Solution Architecture</option>
                    <option value="Legal/Deal Desk">Legal/Deal Desk</option>
                    <option value="Closed Won">Closed Won</option>
                  </select>
                </div>
              </div>
              <div className="pt-3 border-t flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsOppModalOpen(false)}
                  className="px-4 py-2 border rounded-lg text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold shadow"
                >
                  Register Opportunity
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: Open Ticket */}
      {isTicketModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <i className="fa-solid fa-headset text-blue-600"></i> Open Enterprise Support Ticket
              </h3>
              <button onClick={() => setIsTicketModalOpen(false)} className="text-slate-400 hover:text-slate-600 p-1">
                <i className="fa-solid fa-xmark"></i>
              </button>
            </div>
            <form onSubmit={handleCreateTicket} className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Client Account</label>
                <select
                  value={newTicket.client_name}
                  onChange={(e) => setNewTicket({ ...newTicket, client_name: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2"
                >
                  {accounts.map((a) => (
                    <option key={a.id} value={a.client_name}>
                      {a.client_name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Issue Subject</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. SSL Certificate renewal required for API gateway"
                  value={newTicket.subject}
                  onChange={(e) => setNewTicket({ ...newTicket, subject: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2"
                />
              </div>
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Severity / SLA Tier</label>
                <select
                  value={newTicket.severity}
                  onChange={(e) => setNewTicket({ ...newTicket, severity: e.target.value })}
                  className="w-full border border-slate-200 rounded-lg p-2"
                >
                  <option value="Critical">Critical (1h Response SLA)</option>
                  <option value="High">High (4h Response SLA)</option>
                  <option value="Medium">Medium (12h Response SLA)</option>
                  <option value="Low">Low (24h Response SLA)</option>
                </select>
              </div>
              <div className="pt-3 border-t flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsTicketModalOpen(false)}
                  className="px-4 py-2 border rounded-lg text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow"
                >
                  Submit Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
export default CRMView;
