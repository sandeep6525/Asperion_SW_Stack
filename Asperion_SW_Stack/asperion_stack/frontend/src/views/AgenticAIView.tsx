import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface AgentPersona {
  agent_id: string;
  name: string;
  role: string;
  model: string;
  autonomy_tier: string;
  status: string;
  success_rate: string;
  assigned_tools_json?: string;
  assigned_tools?: string[];
  missions_count?: number;
}

interface Mission {
  mission_id: string;
  title: string;
  agent_name: string;
  status: string;
  timestamp: string;
  execution_time: string;
  cost: string;
  tool_calls: number;
  approval_status: string;
  reasoning_trace?: string;
}

export const AgenticAIView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'fleet' | 'missions' | 'chat' | 'topology'>('fleet');
  const [isDispatchModalOpen, setIsDispatchModalOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{ sender: 'user' | 'agent'; text: string; time: string }>>([
    {
      sender: 'agent',
      text: 'Greetings Director. Autonomous Swarm Coordinator initialized with Level 4 Autonomy under ISO/IEC 42001 and DPDP Act 2023 guardrails. What mission shall we execute today?',
      time: '10:00 AM',
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const [overview, setOverview] = useState({
    active_agents: 5,
    total_missions: '248',
    success_rate: '99.6%',
    approval_gates: '1 Gate',
    grounded_tools: '24 Tools',
    guardrail_pass: '100%',
  });

  const [agents, setAgents] = useState<AgentPersona[]>([
    {
      agent_id: 'AGT-SRE-01',
      name: 'Atlas SRE Sentinel',
      role: 'Autonomous Cloud Health & Self-Healing SRE',
      model: 'Gemini 2.5 Flash',
      autonomy_tier: 'Level 4: Autonomous with Rollback',
      status: 'ACTIVE',
      success_rate: '99.8%',
      assigned_tools: ['kubectl', 'aws_cli', 'cloudwatch_metrics', 'prometheus', 'vault_secrets'],
      missions_count: 82,
    },
    {
      agent_id: 'AGT-COMP-02',
      name: 'Lex OPC Compliance Auditor',
      role: 'MCA21, ISO 27001 & DPDP Act 2023 Guardrail Enforcement',
      model: 'Gemini 2.5 Pro',
      autonomy_tier: 'Level 3: Human-in-Loop Approval',
      status: 'ACTIVE',
      success_rate: '100%',
      assigned_tools: ['mca_portal_sync', 'gstin_api', 'dpdp_consent_db', 'audit_log_verifier'],
      missions_count: 64,
    },
    {
      agent_id: 'AGT-FIN-03',
      name: 'Aurelia FinOps Controller',
      role: '13-Week Cash Flow Optimization & 3-Way Match Verification',
      model: 'Claude 3.7 Sonnet',
      autonomy_tier: 'Level 3: Human-in-Loop Approval',
      status: 'ACTIVE',
      success_rate: '99.4%',
      assigned_tools: ['bank_statement_ocr', 'tally_ledger_sync', 'tds_calculator', 'gst_e_invoicing'],
      missions_count: 51,
    },
    {
      agent_id: 'AGT-TAL-04',
      name: 'Kora Talent & Wage Code Engine',
      role: 'Smart Attendance, Code on Wages 2019 CTC Restructuring & POSH',
      model: 'Gemini 2.5 Flash',
      autonomy_tier: 'Level 4: Autonomous with Rollback',
      status: 'ACTIVE',
      success_rate: '99.7%',
      assigned_tools: ['epfo_portal_api', 'esic_sync', 'wage_code_engine', 'face_recognition_kiosk'],
      missions_count: 37,
    },
    {
      agent_id: 'AGT-SEC-05',
      name: 'Vanguard CERT-In Defense Agent',
      role: '6-Hour CERT-In Incident Reporting & Continuous Forensic Triage',
      model: 'DeepSeek-R1 Distill',
      autonomy_tier: 'Level 4: Autonomous with Rollback',
      status: 'ACTIVE',
      success_rate: '99.9%',
      assigned_tools: ['siem_suricata_stream', 'cert_in_api', 'ioc_hash_lookup', 'pcap_forensic_analyzer'],
      missions_count: 14,
    },
  ]);

  const [missions, setMissions] = useState<Mission[]>([
    {
      mission_id: 'MSN-2026-098',
      title: 'Auto-remediate Redis cluster memory pressure on us-east-1 pod-7',
      agent_name: 'Atlas SRE Sentinel',
      status: 'COMPLETED',
      timestamp: 'Today, 14:22 IST',
      execution_time: '1.4s',
      cost: '₹0.18',
      tool_calls: 3,
      approval_status: 'Auto-Approved (Level 4)',
      reasoning_trace: 'Observation: Redis memory reached 88%. Action: kubectl scale replicas + flush expired keys cache. Verification: Memory normalized to 42%.',
    },
    {
      mission_id: 'MSN-2026-097',
      title: 'Verify TDS Section 194J 10% deduction on Q3 Vendor Invoices',
      agent_name: 'Aurelia FinOps Controller',
      status: 'COMPLETED',
      timestamp: 'Today, 11:45 IST',
      execution_time: '2.8s',
      cost: '₹0.42',
      tool_calls: 5,
      approval_status: 'Director Signed (Varadi Vijay)',
      reasoning_trace: 'Verified PAN linking, Form 26AS matching, and generated provisional TDS voucher in compliance with Section 194J.',
    },
    {
      mission_id: 'MSN-2026-096',
      title: 'DPDP Consent Audit & Automated DPDPA 2023 Data Erasure request #41',
      agent_name: 'Lex OPC Compliance Auditor',
      status: 'COMPLETED',
      timestamp: 'Today, 09:15 IST',
      execution_time: '3.1s',
      cost: '₹0.64',
      tool_calls: 4,
      approval_status: 'Director Signed (Varadi Vijay)',
      reasoning_trace: 'Verified user consent withdrawal token, executed soft deletion with pseudonymization hash across 3 operational schemas.',
    },
    {
      mission_id: 'MSN-2026-095',
      title: 'Wage Code 2019 Basic 50% Rule Audit across All 42 Employees',
      agent_name: 'Kora Talent Engine',
      status: 'COMPLETED',
      timestamp: 'Yesterday, 18:30 IST',
      execution_time: '4.2s',
      cost: '₹0.32',
      tool_calls: 6,
      approval_status: 'Auto-Approved (Level 4)',
      reasoning_trace: 'Recalculated Basic, HRA, Special Allowances to ensure compliance with 50% statutory ceiling. Generated revised CTC annexures.',
    },
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ovRes, agRes, msRes] = await Promise.all([
          axios.get('/api/v1/agentic-ai/overview').catch(() => null),
          axios.get('/api/v1/agentic-ai/agents').catch(() => null),
          axios.get('/api/v1/agentic-ai/missions').catch(() => null),
        ]);
        if (ovRes?.data) setOverview(ovRes.data);
        if (agRes?.data && Array.isArray(agRes.data) && agRes.data.length > 0) {
          setAgents(agRes.data);
        }
        if (msRes?.data && Array.isArray(msRes.data) && msRes.data.length > 0) {
          setMissions(msRes.data);
        }
      } catch {
        // Keep resilient demo data
      }
    };
    fetchData();
  }, []);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;
    const userMsg = inputMessage;
    setInputMessage('');
    setChatMessages((prev) => [
      ...prev,
      { sender: 'user', text: userMsg, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) },
    ]);

    setTimeout(() => {
      setChatMessages((prev) => [
        ...prev,
        {
          sender: 'agent',
          text: `[ReAct Agent Loop Triggered]\n- Thought: Analyzing user directive "${userMsg}" against enterprise guardrails and assigned tools.\n- Tool Execution: Checked current system topology, ERP ledgers, and ISO compliance.\n- Result: Action simulated successfully. No regulatory deviations detected.`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }, 700);
  };

  return (
    <div className="space-y-6">
      {/* Executive Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-purple-950 to-slate-900 rounded-2xl p-6 text-white border border-purple-800/40 shadow-xl relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 opacity-10 pointer-events-none">
          <i className="fa-solid fa-network-wired text-[200px] text-purple-400"></i>
        </div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">
                <i className="fa-solid fa-brain mr-1"></i> Enterprise Autonomous Swarm
              </span>
              <span className="text-xs text-slate-400 font-mono">CIN: U85500KA2026OPC222069 | ISO/IEC 42001 &amp; 27001</span>
            </div>
            <h2 className="text-2xl font-black tracking-tight text-white flex items-center gap-2">
              <i className="fa-solid fa-robot text-purple-400"></i>
              Agentic AI &amp; Autonomous Multi-Agent Swarm
            </h2>
            <p className="text-xs text-slate-300 max-w-3xl">
              Orchestrating deterministic enterprise autonomy across SRE, Statutory Compliance, FinOps, Talent, and Client Delivery. Powered by ReAct (Reasoning + Action) execution loops, Model Context Protocol (MCP) tool integration, and human-in-the-loop safety gates.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setIsDispatchModalOpen(true)}
              className="px-3.5 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow-lg shadow-purple-900/40"
            >
              <i className="fa-solid fa-bolt"></i> Dispatch Mission
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow"
            >
              <i className="fa-solid fa-comments"></i> Copilot Chat
            </button>
          </div>
        </div>
      </div>

      {/* 6 Executive KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Active Agents
            <i className="fa-solid fa-users-gear text-purple-500"></i>
          </div>
          <div className="text-xl font-bold text-slate-800 mt-1">{overview.active_agents}</div>
          <div className="text-[10px] text-emerald-600 font-medium mt-0.5">
            <i className="fa-solid fa-circle-check"></i> 100% Swarm Health
          </div>
        </div>
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Total Missions
            <i className="fa-solid fa-satellite-dish text-blue-500"></i>
          </div>
          <div className="text-xl font-bold text-slate-800 mt-1">{overview.total_missions}</div>
          <div className="text-[10px] text-slate-500 font-medium mt-0.5">Dispatched &amp; Audited</div>
        </div>
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Success Velocity
            <i className="fa-solid fa-gauge-high text-emerald-500"></i>
          </div>
          <div className="text-xl font-bold text-emerald-600 mt-1">{overview.success_rate}</div>
          <div className="text-[10px] text-slate-500 font-medium mt-0.5">Avg 1.8s Latency</div>
        </div>
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Human Approval
            <i className="fa-solid fa-user-shield text-amber-500"></i>
          </div>
          <div className="text-xl font-bold text-amber-600 mt-1">{overview.approval_gates}</div>
          <div className="text-[10px] text-slate-500 font-medium mt-0.5">Director Signoff Pending</div>
        </div>
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Grounded Tools
            <i className="fa-solid fa-toolbox text-indigo-500"></i>
          </div>
          <div className="text-xl font-bold text-slate-800 mt-1">{overview.grounded_tools}</div>
          <div className="text-[10px] text-slate-500 font-medium mt-0.5">MCP Protocol Grounded</div>
        </div>
        <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
          <div className="text-[11px] font-semibold text-slate-500 uppercase flex items-center justify-between">
            Guardrail Audit
            <i className="fa-solid fa-shield-halved text-cyan-500"></i>
          </div>
          <div className="text-xl font-bold text-cyan-600 mt-1">{overview.guardrail_pass}</div>
          <div className="text-[10px] text-emerald-600 font-medium mt-0.5">
            <i className="fa-solid fa-check"></i> ISO 27001 / DPDP
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('fleet')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${
            activeTab === 'fleet'
              ? 'bg-purple-900 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <i className="fa-solid fa-id-card-clip"></i> Swarm Agent Fleet ({agents.length})
        </button>
        <button
          onClick={() => setActiveTab('missions')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${
            activeTab === 'missions'
              ? 'bg-purple-900 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <i className="fa-solid fa-terminal"></i> Mission Console &amp; Traces
        </button>
        <button
          onClick={() => setActiveTab('chat')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${
            activeTab === 'chat'
              ? 'bg-purple-900 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <i className="fa-solid fa-comments"></i> Interactive Copilot
        </button>
        <button
          onClick={() => setActiveTab('topology')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 ${
            activeTab === 'topology'
              ? 'bg-purple-900 text-white shadow'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <i className="fa-solid fa-circle-nodes"></i> Swarm Mesh &amp; Governance
        </button>
      </div>

      {/* TAB 1: SWARM AGENT FLEET */}
      {activeTab === 'fleet' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Enterprise Agent Personas</h3>
              <p className="text-xs text-slate-500">
                Specialized autonomous entities with deterministic system prompts, autonomy tiers, and assigned MCP tools.
              </p>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 bg-purple-50 text-purple-700 border border-purple-200 rounded-lg">
              <i className="fa-solid fa-microchip mr-1"></i> Multi-Model: Gemini 2.5 Pro &amp; Flash
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => {
              const tools =
                agent.assigned_tools ||
                (agent.assigned_tools_json ? JSON.parse(agent.assigned_tools_json) : []);
              return (
                <div
                  key={agent.agent_id}
                  className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition space-y-4 flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                            {agent.agent_id}
                          </span>
                          <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            {agent.status}
                          </span>
                        </div>
                        <h4 className="font-black text-slate-800 text-base mt-1.5">{agent.name}</h4>
                        <p className="text-xs text-slate-500">{agent.role}</p>
                      </div>
                    </div>

                    <div className="bg-slate-50 rounded-lg p-2.5 text-xs space-y-1.5 border border-slate-100">
                      <div className="flex justify-between">
                        <span className="text-slate-500">Inference Engine:</span>
                        <span className="font-semibold text-slate-700">{agent.model}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Autonomy Tier:</span>
                        <span className="font-semibold text-purple-700">{agent.autonomy_tier}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Historical Accuracy:</span>
                        <span className="font-semibold text-emerald-600">{agent.success_rate}</span>
                      </div>
                    </div>

                    <div>
                      <div className="text-[11px] font-bold text-slate-600 mb-1.5">Assigned MCP Tools:</div>
                      <div className="flex flex-wrap gap-1">
                        {tools.slice(0, 5).map((tool: string, idx: number) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-100 text-slate-700 border border-slate-200"
                          >
                            {tool}
                          </span>
                        ))}
                        {tools.length > 5 && (
                          <span className="text-[10px] text-slate-400 font-mono self-center">
                            +{tools.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-xs text-slate-500">
                      Missions: <strong className="text-slate-700">{agent.missions_count || 42}</strong>
                    </span>
                    <button
                      onClick={() => setIsDispatchModalOpen(true)}
                      className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1 shadow-sm"
                    >
                      <i className="fa-solid fa-play text-[10px]"></i> Dispatch
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 2: MISSION CONSOLE & TRACES */}
      {activeTab === 'missions' && (
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm space-y-3">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <h3 className="font-bold text-slate-800 text-sm">Mission Execution History &amp; Reasoning Traces</h3>
                <p className="text-xs text-slate-500">
                  Complete audit trail of autonomous actions, tool calls, and human-in-the-loop decisions.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold">
                  Filter: All (4)
                </button>
                <button
                  onClick={() => setIsDispatchModalOpen(true)}
                  className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold"
                >
                  <i className="fa-solid fa-plus mr-1"></i> New Mission
                </button>
              </div>
            </div>

            <div className="divide-y divide-slate-100 border rounded-xl overflow-hidden">
              {missions.map((m) => (
                <div key={m.mission_id} className="p-4 hover:bg-slate-50/70 transition space-y-2">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono text-xs font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                        {m.mission_id}
                      </span>
                      <span className="font-bold text-slate-800 text-sm">{m.title}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                        {m.status}
                      </span>
                      <span className="text-xs text-slate-400 font-mono">{m.timestamp}</span>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500">
                    <span>
                      Agent: <strong className="text-slate-700">{m.agent_name}</strong>
                    </span>
                    <span>
                      Latency: <strong className="text-slate-700">{m.execution_time}</strong>
                    </span>
                    <span>
                      Cost: <strong className="text-slate-700">{m.cost}</strong>
                    </span>
                    <span>
                      Tool Calls: <strong className="text-purple-600 font-bold">{m.tool_calls}</strong>
                    </span>
                    <span>
                      Signoff: <strong className="text-slate-700">{m.approval_status}</strong>
                    </span>
                  </div>

                  {m.reasoning_trace && (
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-3 font-mono text-[11px] leading-relaxed border border-slate-800">
                      <span className="text-purple-400 font-bold">Trace &gt;</span> {m.reasoning_trace}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: INTERACTIVE COPILOT */}
      {activeTab === 'chat' && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[600px]">
          <div className="p-4 bg-slate-900 text-white flex items-center justify-between border-b border-purple-900">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-white">
                <i className="fa-solid fa-robot"></i>
              </div>
              <div>
                <h4 className="font-bold text-sm">Enterprise Copilot (ReAct Agent)</h4>
                <p className="text-[10px] text-purple-300">Grounding: Live SQLite DB + FastMCP Tools + ISO 42001 Guardrails</p>
              </div>
            </div>
            <span className="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono">
              Online
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50">
            {chatMessages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.sender === 'agent' && (
                  <div className="w-7 h-7 rounded-full bg-purple-600 text-white flex items-center justify-center text-xs shrink-0 mt-1">
                    <i className="fa-solid fa-robot"></i>
                  </div>
                )}
                <div
                  className={`max-w-xl rounded-xl p-3.5 text-xs shadow-sm ${
                    msg.sender === 'user'
                      ? 'bg-purple-600 text-white rounded-br-none'
                      : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none whitespace-pre-line'
                  }`}
                >
                  <p>{msg.text}</p>
                  <span
                    className={`text-[9px] block text-right mt-1.5 ${
                      msg.sender === 'user' ? 'text-purple-200' : 'text-slate-400'
                    }`}
                  >
                    {msg.time}
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask Copilot: e.g. Audit Q3 TDS compliance or recalculate wage code Basic 50%..."
              className="flex-1 px-4 py-2 border border-slate-200 rounded-lg text-xs focus:outline-none focus:border-purple-600"
            />
            <button
              onClick={handleSendMessage}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow"
            >
              <span>Send</span>
              <i className="fa-solid fa-paper-plane text-[10px]"></i>
            </button>
          </div>
        </div>
      )}

      {/* TAB 4: SWARM MESH & GOVERNANCE */}
      {activeTab === 'topology' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center font-bold">
                <i className="fa-solid fa-shield-halved"></i>
              </div>
              <div>
                <h4 className="font-bold text-slate-800 text-sm">ISO/IEC 42001 AI Management System (AIMS)</h4>
                <p className="text-xs text-slate-500">Autonomous Execution Guardrails &amp; Ethics Audit</p>
              </div>
            </div>
            <div className="space-y-2 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                <span>Autonomous Rollback Mechanism:</span>
                <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Active (Zero-Data-Loss)</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                <span>Human-In-The-Loop Ceiling:</span>
                <span className="font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded">&gt; ₹10,000 Financials</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                <span>DPDP Act 2023 Erasure Hooks:</span>
                <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Deterministic Pseudonymization</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 flex justify-between items-center">
                <span>CERT-In 6-Hour Triage Integration:</span>
                <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Direct Dispatch Endpoint</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center font-bold">
                <i className="fa-solid fa-network-wired"></i>
              </div>
              <div>
                <h4 className="font-bold text-slate-800 text-sm">Multi-Agent Swarm Orchestration Topology</h4>
                <p className="text-xs text-slate-500">Inter-Agent PubSub Mesh over FastMCP Protocol</p>
              </div>
            </div>
            <div className="bg-slate-900 rounded-xl p-4 text-xs font-mono text-slate-300 space-y-2 border border-slate-800">
              <div className="text-purple-400 font-bold">// Enterprise Swarm Router</div>
              <div>Coordinator: Varadi Vijay (Director) -&gt; Swarm Master</div>
              <div className="text-slate-400">├── SRE Sentinel (Atlas) &lt;--&gt; Infra Tools</div>
              <div className="text-slate-400">├── Compliance Auditor (Lex) &lt;--&gt; MCA21 + DPDP DB</div>
              <div className="text-slate-400">├── FinOps Controller (Aurelia) &lt;--&gt; Direct 13-W Cash</div>
              <div className="text-slate-400">├── Talent Engine (Kora) &lt;--&gt; Wage Code 2019 Engine</div>
              <div className="text-slate-400">└── CERT-In War Room (Vanguard) &lt;--&gt; Suricata SIEM</div>
            </div>
          </div>
        </div>
      )}

      {/* DISPATCH MISSION MODAL */}
      {isDispatchModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-purple-600 text-white flex items-center justify-center">
                  <i className="fa-solid fa-bolt"></i>
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-sm">Dispatch Autonomous Mission</h4>
                  <p className="text-xs text-slate-500">Assign ReAct loop to enterprise agent fleet</p>
                </div>
              </div>
              <button
                onClick={() => setIsDispatchModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <i className="fa-solid fa-xmark"></i>
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Target Agent Persona</label>
                <select className="w-full border border-slate-200 rounded-lg p-2 text-xs focus:border-purple-600">
                  {agents.map((a) => (
                    <option key={a.agent_id} value={a.agent_id}>
                      {a.name} ({a.role})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Mission Objective / Directive</label>
                <textarea
                  rows={3}
                  placeholder="e.g. Run 13-week cash flow stress test with 15% delayed client collections..."
                  className="w-full border border-slate-200 rounded-lg p-2.5 text-xs focus:border-purple-600"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Max Cost Ceiling</label>
                  <input
                    type="text"
                    defaultValue="₹5.00"
                    className="w-full border border-slate-200 rounded-lg p-2 text-xs"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Safety Gate Level</label>
                  <select className="w-full border border-slate-200 rounded-lg p-2 text-xs">
                    <option>Level 3: Human Approval</option>
                    <option>Level 4: Full Autonomous Rollback</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
              <button
                onClick={() => setIsDispatchModalOpen(false)}
                className="px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  alert('Mission successfully dispatched to Enterprise Swarm!');
                  setIsDispatchModalOpen(false);
                }}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold shadow"
              >
                Confirm &amp; Dispatch
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default AgenticAIView;
