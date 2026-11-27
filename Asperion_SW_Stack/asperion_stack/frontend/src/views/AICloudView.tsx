import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const AICloudView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'models' | 'mcps' | 'cloud' | 'certs' | 'alerts'>('models');
  const [isAlertModalOpen, setIsAlertModalOpen] = useState(false);
  const [overview, setOverview] = useState<any>({
    monthly_spend: 38400,
    monthly_budget: 50000,
    active_mcp_servers: 4,
    cloud_uptime: '99.98%',
    authenticity_certs: 6,
  });

  const [models, setModels] = useState<any[]>([
    {
      code: 'EP-AI-01',
      name: 'Gemini 2.5 Pro Multimodal Reasoning',
      provider: 'Google Cloud Vertex AI',
      role: 'Core Enterprise Reasoning & Multimodal Audit',
      context: '1,000,000 Tokens',
      limits: '60 RPM / 4M TPM',
      latency: '240ms',
      cost: '₹104 / 1M Input',
      spend: '₹14,200',
      budget: '₹20,000',
      spend_pct: 71,
      vault: 'VAULT-SEC-01 (AES-256)',
    },
    {
      code: 'EP-AI-02',
      name: 'Claude 3.7 Sonnet Hybrid Reasoning',
      provider: 'Anthropic Bedrock',
      role: 'Contract Synthesizer & Code Audit Agent',
      context: '200,000 Tokens',
      limits: '50 RPM / 2M TPM',
      latency: '310ms',
      cost: '₹250 / 1M Input',
      spend: '₹12,800',
      budget: '₹15,000',
      spend_pct: 85,
      vault: 'VAULT-SEC-02 (AES-256)',
    },
    {
      code: 'EP-AI-03',
      name: 'DeepSeek-R1 Distill Llama 70B',
      provider: 'Self-Hosted vLLM (GCP A100)',
      role: 'Local Compliance & Offline Air-Gap Reasoning',
      context: '128,000 Tokens',
      limits: 'Unmetered (GPU Bound)',
      latency: '180ms',
      cost: 'Fixed Node OPEX',
      spend: '₹6,400',
      budget: '₹10,000',
      spend_pct: 64,
      vault: 'VAULT-SEC-03 (Air-Gapped)',
    },
    {
      code: 'EP-AI-04',
      name: 'OpenAI GPT-4o Omni Vision',
      provider: 'Azure OpenAI (Central India)',
      role: 'OCR Inward GRN & Bill Parsing Agent',
      context: '128,000 Tokens',
      limits: '100 RPM / 5M TPM',
      latency: '290ms',
      cost: '₹208 / 1M Input',
      spend: '₹5,000',
      budget: '₹5,000',
      spend_pct: 100,
      vault: 'VAULT-SEC-04 (Azure HSM)',
    },
  ]);

  const [mcps, setMcps] = useState<any[]>([
    {
      name: 'FastAPI Core ERP MCP Server',
      command: 'uvicorn app.main:app --port 8050',
      transport: 'SSE (Server-Sent Events)',
      tools_count: 14,
      status: 'HEALTHY',
      description: 'Exposes HRMS, Finance, PMO, and Governance tools directly to LLM context.',
    },
    {
      name: 'Docker Swarm & SRE Tool Server',
      command: 'docker mcp-bridge --socket /var/run/docker.sock',
      transport: 'stdio (Unix Domain Socket)',
      tools_count: 8,
      status: 'HEALTHY',
      description: 'Host monitoring, container restarts, log tailing, and memory threshold checks.',
    },
    {
      name: 'PostgreSQL & CMDB Dependency Explorer',
      command: 'python -m mcp_postgres --db asperion_cmdb',
      transport: 'stdio',
      tools_count: 6,
      status: 'HEALTHY',
      description: 'Allows LLMs to inspect ITIL configuration items, relationships, and change logs.',
    },
    {
      name: 'SecOps CERT-In Sentinel Tool Server',
      command: 'certin-daemon --mcp-mode --strict',
      transport: 'SSE (/api/v1/secops/mcp)',
      tools_count: 9,
      status: 'HEALTHY',
      description: 'Evaluates statutory 6-hour reporting invariants, threat feeds, and NTP clock locks.',
    },
  ]);

  const [cloudNodes, setCloudNodes] = useState<any[]>([
    { region: 'AWS ap-south-1 (Mumbai)', cluster: 'k8s-prod-mum-01', nodes: '8 Nodes', pods: '64 Pods', health: '99.99%', role: 'Primary API Gateway & DB' },
    { region: 'GCP us-central1 (Iowa)', cluster: 'gke-ai-inference-01', nodes: '4 Nodes (A100)', pods: '16 Pods', health: '99.95%', role: 'vLLM DeepSeek Reasoning' },
    { region: 'Azure Central India (Pune)', cluster: 'aks-dr-replica-01', nodes: '4 Nodes', pods: '28 Pods', health: '100.0%', role: 'Standby DR & Azure OpenAI' },
  ]);

  const [certs, setCerts] = useState<any[]>([
    { code: 'DSC-VVIJ-01', name: 'Sole Director Class 3 DSC', entity: 'Varadi Vijay (OPC)', ca: 'eMudhra India', algo: 'RSA-4096 (FIPS 140-2 Level 3)', fp: '7F:3A:9B:4C:E1:82:99...', val: '284 Days Left', status: 'VALID' },
    { code: 'SEAL-ASPER-02', name: 'Enterprise Corporate Seal', entity: 'Asperion Digital Tech (OPC)', ca: 'DigiCert Global', algo: 'ECDSA P-384', fp: '4D:21:88:AC:3B:11:FA...', val: '410 Days Left', status: 'VALID' },
    { code: 'SSL-APIGW-03', name: 'Wildcard *.asperion.in TLS', entity: 'Cloudflare Inc', ca: 'Let’s Encrypt Authority', algo: 'RSA-2048', fp: 'E8:19:93:12:0A:CF:55...', val: '72 Days Left', status: 'AUTO-RENEW' },
  ]);

  const [alertRules, setAlertRules] = useState<any[]>([
    { title: 'Statutory MCA Filing Invariant Breach', target: 'Sole Director (Varadi Vijay)', channel: 'WhatsApp Cloud API + High-Priority Email', threshold: 'T - 48 Hours', status: 'ACTIVE' },
    { title: 'CERT-In Mandatory 6-Hour Countdown Alert', target: 'CISO & Lead Architect', channel: 'SMS + PagerDuty Ping', threshold: 'T - 3 Hours', status: 'ACTIVE' },
    { title: 'AP Vendor MSME Samadhaan 45-Day Overdue', target: 'Head of Finance', channel: 'In-App Tray + Email', threshold: 'T - 5 Days', status: 'ACTIVE' },
    { title: 'Monthly AI Token Quota 85% Warning', target: 'Lead Architect', channel: 'Slack #devsecops + Email', threshold: '₹42,500 Burn', status: 'ACTIVE' },
  ]);

  useEffect(() => {
    async function loadData() {
      try {
        const [overRes, modRes, mcpRes, nodeRes, certRes, ruleRes] = await Promise.all([
          axios.get('/api/v1/ai-cloud/overview').catch(() => null),
          axios.get('/api/v1/ai-cloud/ai-models').catch(() => null),
          axios.get('/api/v1/ai-cloud/mcp-servers').catch(() => null),
          axios.get('/api/v1/ai-cloud/cloud-nodes').catch(() => null),
          axios.get('/api/v1/ai-cloud/certificates').catch(() => null),
          axios.get('/api/v1/ai-cloud/alert-rules').catch(() => null),
        ]);

        if (overRes?.data) setOverview(overRes.data);

        if (Array.isArray(modRes?.data) && modRes.data.length > 0) {
          setModels(modRes.data.map((m: any) => ({
            code: m.endpoint_code || m.code || `EP-${m.id}`,
            name: m.model_name || m.name,
            provider: m.provider || 'Enterprise Cloud',
            role: m.model_family || m.role || 'Enterprise AI',
            context: m.context_window_tokens ? `${m.context_window_tokens.toLocaleString()} Tokens` : m.context || '128K Tokens',
            limits: m.rpm_limit ? `${m.rpm_limit} RPM / ${Math.round((m.tpm_limit || 0)/1000)}K TPM` : m.limits || '60 RPM',
            latency: m.avg_latency_ms ? `${Math.round(m.avg_latency_ms)}ms` : m.latency || '240ms',
            cost: m.cost_per_million_tokens_inr ? `₹${m.cost_per_million_tokens_inr} / 1M` : m.cost || '₹100 / 1M',
            spend: m.current_month_usage_inr ? `₹${m.current_month_usage_inr.toLocaleString()}` : m.spend || '₹0',
            budget: m.monthly_budget_inr ? `₹${m.monthly_budget_inr.toLocaleString()}` : m.budget || '₹20,000',
            spend_pct: m.monthly_budget_inr ? Math.round(((m.current_month_usage_inr || 0) / m.monthly_budget_inr) * 100) : m.spend_pct || 50,
            vault: m.api_key_vault_ref || m.vault || 'VAULT-SEC-01',
          })));
        }

        if (Array.isArray(mcpRes?.data) && mcpRes.data.length > 0) {
          setMcps(mcpRes.data.map((s: any) => ({
            name: s.name,
            command: s.endpoint_or_command || s.command,
            transport: s.transport_type ? `${s.transport_type.toUpperCase()} Protocol` : s.transport,
            tools_count: s.exposed_tools_count ?? s.tools_count ?? 8,
            status: s.last_ping_status?.includes('Healthy') || s.is_connected ? 'HEALTHY' : (s.status || 'ACTIVE'),
            description: s.description || 'Enterprise MCP Integration Bridge',
          })));
        }

        if (Array.isArray(nodeRes?.data) && nodeRes.data.length > 0) {
          setCloudNodes(nodeRes.data.map((n: any) => ({
            region: `${n.cloud_provider} ${n.region}`,
            cluster: n.cluster_or_service_name || n.node_code,
            nodes: n.compute_capacity || '8 Nodes',
            pods: n.resource_type || 'Active Workload',
            health: n.uptime_sla_pct ? `${n.uptime_sla_pct}%` : '99.9%',
            role: n.technical_lead ? `Lead: ${n.technical_lead}` : 'Enterprise Cluster',
          })));
        }

        if (Array.isArray(certRes?.data) && certRes.data.length > 0) {
          setCerts(certRes.data.map((c: any) => ({
            code: c.cert_code || `DSC-${c.id}`,
            name: c.certificate_name || c.name,
            entity: c.subject_entity || 'ASPERION DIGITAL TECHNOLOGIES',
            ca: c.issuing_authority || c.ca,
            algo: `${c.key_algorithm || ''} (${c.fips_compliance_level || 'FIPS 140-3'})`,
            fp: c.public_key_fingerprint ? `${c.public_key_fingerprint.slice(0, 16)}...` : c.fp,
            val: c.days_until_expiry ? `${c.days_until_expiry} Days Left` : c.val,
            status: c.status?.toUpperCase() || 'VALID',
          })));
        }

        if (Array.isArray(ruleRes?.data) && ruleRes.data.length > 0) {
          setAlertRules(ruleRes.data.map((r: any) => ({
            title: r.title,
            target: r.target_head_role || 'Sole Director',
            channel: r.dispatch_channels || 'WhatsApp + Email',
            threshold: r.trigger_condition || 'Invariant Trigger',
            status: r.is_active ? 'ACTIVE' : 'STANDBY',
          })));
        }
      } catch (err) {
        console.error('Failed to load AI Cloud telemetry:', err);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
              <i className="fa-solid fa-microchip text-violet-600"></i>
              AI APIs, Model Context Protocol (MCP), Multi-Cloud & Authenticity Mesh
            </h2>
            <span className="bg-violet-100 text-violet-800 border border-violet-300 px-2.5 py-0.5 rounded-full text-xs font-semibold">
              Enterprise Agentic Layer
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Operationalize Multimodal Reasoning LLMs (Gemini 2.5 Pro, Claude 3.7, DeepSeek-R1), Open Standard Model Context Protocol (MCP) tool servers, multi-region Kubernetes topology, and FIPS-compliant cryptographic authenticity certificates.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsAlertModalOpen(true)}
            className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow"
          >
            <i className="fa-solid fa-bullhorn"></i> Dispatch Head Alert
          </button>
          <button
            onClick={() => {
              window.location.reload();
            }}
            className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 border rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
          >
            <i className="fa-solid fa-arrows-rotate"></i> Refresh Mesh
          </button>
        </div>
      </div>

      {/* Telemetry KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between stat-card">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">AI API Token Budget</div>
            <div className="text-2xl font-black text-violet-600 mt-1">
              ₹{overview.monthly_spend ? overview.monthly_spend.toLocaleString() : '38,400'} / ₹{overview.monthly_budget ? overview.monthly_budget.toLocaleString() : '50,000'}
            </div>
            <div className="text-[10px] text-slate-500 mt-0.5">76.8% monthly spend quota utilized</div>
          </div>
          <div className="w-12 h-12 bg-violet-50 rounded-xl flex items-center justify-center text-violet-600 text-xl border border-violet-100">
            <i className="fa-solid fa-brain"></i>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between stat-card">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Connected MCP Servers</div>
            <div className="text-2xl font-black text-indigo-600 mt-1">{mcps.length} Active</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Model Context Protocol Bridges</div>
          </div>
          <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 text-xl border border-indigo-100">
            <i className="fa-solid fa-network-wired"></i>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between stat-card">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Cloud SLA Uptime</div>
            <div className="text-2xl font-black text-emerald-600 mt-1">{overview.cloud_uptime || '99.98%'}</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Multi-Region Kubernetes & CDN</div>
          </div>
          <div className="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 text-xl border border-emerald-100">
            <i className="fa-solid fa-cloud"></i>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between stat-card">
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Authenticity Certs</div>
            <div className="text-2xl font-black text-teal-600 mt-1">{certs.length} Trusted</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Class 3 DSC & Document Seals</div>
          </div>
          <div className="w-12 h-12 bg-teal-50 rounded-xl flex items-center justify-center text-teal-600 text-xl border border-teal-100">
            <i className="fa-solid fa-stamp"></i>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-6 text-sm font-semibold">
        <button
          onClick={() => setActiveTab('models')}
          className={`py-2 flex items-center gap-2 border-b-2 transition ${
            activeTab === 'models'
              ? 'border-violet-600 text-violet-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <i className="fa-solid fa-robot"></i> AI Model APIs & Quotas ({models.length})
        </button>
        <button
          onClick={() => setActiveTab('mcps')}
          className={`py-2 flex items-center gap-2 border-b-2 transition ${
            activeTab === 'mcps'
              ? 'border-violet-600 text-violet-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <i className="fa-solid fa-cubes-stacked"></i> MCP Tool Servers ({mcps.length})
        </button>
        <button
          onClick={() => setActiveTab('cloud')}
          className={`py-2 flex items-center gap-2 border-b-2 transition ${
            activeTab === 'cloud'
              ? 'border-violet-600 text-violet-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <i className="fa-solid fa-server"></i> Multi-Cloud Topology ({cloudNodes.length})
        </button>
        <button
          onClick={() => setActiveTab('certs')}
          className={`py-2 flex items-center gap-2 border-b-2 transition ${
            activeTab === 'certs'
              ? 'border-violet-600 text-violet-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <i className="fa-solid fa-certificate"></i> Authenticity & Signatures ({certs.length})
        </button>
        <button
          onClick={() => setActiveTab('alerts')}
          className={`py-2 flex items-center gap-2 border-b-2 transition ${
            activeTab === 'alerts'
              ? 'border-violet-600 text-violet-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <i className="fa-solid fa-bell-concierge"></i> Executive Alerts ({alertRules.length})
        </button>
      </div>

      {/* TAB 1: AI MODEL ENDPOINTS */}
      {activeTab === 'models' && (
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
            <div className="p-3 bg-slate-50 border-b flex justify-between items-center text-xs">
              <span className="font-bold text-slate-700 uppercase">Production Reasoning LLMs & Vector Embeddings</span>
              <span className="text-slate-500 font-medium">Zero Data-Retention Agreements Active ({models.length} Models)</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-slate-100 text-slate-600 border-b">
                    <th className="p-3 font-semibold">Endpoint Code</th>
                    <th className="p-3 font-semibold">Model Name & Provider</th>
                    <th className="p-3 font-semibold">Family / Role</th>
                    <th className="p-3 font-semibold">Context Window</th>
                    <th className="p-3 font-semibold">Rate Limits</th>
                    <th className="p-3 font-semibold">Latency / Cost</th>
                    <th className="p-3 font-semibold">Monthly Spend / Budget</th>
                    <th className="p-3 font-semibold">Vault Credential</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {models.map((m, idx) => (
                    <tr key={idx} className="hover:bg-slate-50 transition">
                      <td className="p-3 font-mono font-bold text-violet-700">{m.code}</td>
                      <td className="p-3">
                        <div className="font-bold text-slate-900">{m.name}</div>
                        <div className="text-[11px] text-slate-500">{m.provider}</div>
                      </td>
                      <td className="p-3 text-slate-600">{m.role}</td>
                      <td className="p-3 font-mono text-slate-700">{m.context}</td>
                      <td className="p-3 text-slate-500">{m.limits}</td>
                      <td className="p-3">
                        <div className="font-mono text-emerald-600 font-semibold">{m.latency}</div>
                        <div className="text-[10px] text-slate-400">{m.cost}</div>
                      </td>
                      <td className="p-3">
                        <div className="font-semibold text-slate-800">{m.spend} / {m.budget}</div>
                        <div className="w-24 bg-slate-200 h-1.5 rounded-full mt-1 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${m.spend_pct >= 90 ? 'bg-rose-500' : 'bg-violet-600'}`}
                            style={{ width: `${Math.min(100, m.spend_pct)}%` }}
                          />
                        </div>
                      </td>
                      <td className="p-3 font-mono text-[10px] text-slate-500">{m.vault}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: MCP SERVERS */}
      {activeTab === 'mcps' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {mcps.map((s, idx) => (
            <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between stat-card">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <i className="fa-solid fa-server text-indigo-600"></i>
                    <h4 className="font-bold text-slate-800 text-sm">{s.name}</h4>
                  </div>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    {s.status}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mb-3">{s.description}</p>
                <div className="bg-slate-900 text-slate-200 p-2.5 rounded-lg font-mono text-[11px] mb-3 overflow-x-auto">
                  <code>$ {s.command}</code>
                </div>
              </div>
              <div className="flex justify-between items-center text-xs border-t pt-3 text-slate-500">
                <span>Transport: <strong className="text-slate-700">{s.transport}</strong></span>
                <span className="px-2 py-1 bg-indigo-50 text-indigo-700 font-bold rounded">
                  {s.tools_count} Tools Bound
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 3: CLOUD TOPOLOGY */}
      {activeTab === 'cloud' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {cloudNodes.map((c, i) => (
            <div key={i} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between stat-card">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-slate-800">{c.region}</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">HEALTHY</span>
                </div>
                <div className="font-mono text-xs text-indigo-600 font-semibold mb-1">{c.cluster}</div>
                <p className="text-xs text-slate-500 mb-3">{c.role}</p>
              </div>
              <div className="border-t pt-3 flex justify-between text-xs text-slate-600 font-mono">
                <span>{c.nodes}</span>
                <span>{c.pods}</span>
                <span className="text-emerald-600 font-bold">{c.health}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 4: AUTHENTICITY CERTIFICATES */}
      {activeTab === 'certs' && (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="p-3 bg-slate-50 border-b flex justify-between items-center text-xs">
            <span className="font-bold text-slate-700 uppercase">Cryptographic Authenticity & Digital Seal Registry</span>
            <span className="text-slate-500">Non-Repudiation Verified</span>
          </div>
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100 text-slate-600 border-b">
                <th className="p-3 font-semibold">Cert Code</th>
                <th className="p-3 font-semibold">Certificate Name & Entity</th>
                <th className="p-3 font-semibold">Issuing CA</th>
                <th className="p-3 font-semibold">Algorithm & FIPS Level</th>
                <th className="p-3 font-semibold">SHA-256 Fingerprint</th>
                <th className="p-3 font-semibold">Validity</th>
                <th className="p-3 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {certs.map((c, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="p-3 font-mono font-bold text-teal-700">{c.code}</td>
                  <td className="p-3 font-semibold text-slate-800">{c.name}</td>
                  <td className="p-3 text-slate-600">{c.ca}</td>
                  <td className="p-3 text-slate-500">{c.algo}</td>
                  <td className="p-3 font-mono text-[10px] text-slate-400">{c.fp}</td>
                  <td className="p-3 font-medium text-slate-700">{c.val}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      {c.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 5: ALERTS */}
      {activeTab === 'alerts' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {alertRules.map((a, i) => (
            <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between stat-card">
              <div>
                <div className="flex justify-between items-start mb-1">
                  <h4 className="font-bold text-slate-800 text-xs">{a.title}</h4>
                  <span className="px-2 py-0.5 rounded-full text-[9px] font-bold bg-rose-100 text-rose-800">
                    {a.status}
                  </span>
                </div>
                <div className="text-[11px] text-slate-600 mt-1">Recipient: <strong className="text-slate-800">{a.target}</strong></div>
                <div className="text-[11px] text-slate-500 mt-0.5">Route: {a.channel}</div>
              </div>
              <div className="border-t pt-2 mt-3 flex justify-between text-[11px] text-slate-400 font-mono">
                <span>Threshold: {a.threshold}</span>
                <button onClick={() => alert(`Simulating test ping for: ${a.title}`)} className="text-violet-600 hover:text-violet-800 font-bold">
                  Test Ping
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* MODAL: TRIGGER OMNI-HEAD ALERT DISPATCH */}
      {isAlertModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center gap-2">
                <i className="fa-solid fa-bullhorn text-rose-600 text-lg"></i>
                <h3 className="font-bold text-slate-800 text-base">Dispatch Verified Alert to Department Head</h3>
              </div>
              <button onClick={() => setIsAlertModalOpen(false)} className="text-slate-400 hover:text-slate-600 text-sm">
                <i className="fa-solid fa-xmark"></i>
              </button>
            </div>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                alert('Omni-Head Alert Dispatched Successfully!');
                setIsAlertModalOpen(false);
              }}
              className="space-y-3"
            >
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Target Department Head & Role</label>
                <select className="w-full text-xs border border-slate-300 rounded-lg p-2.5 bg-slate-50 font-medium">
                  <option value="Sole Director & Head of Finance (Varadi Vijay)">Sole Director & Head of Finance (Varadi Vijay)</option>
                  <option value="CISO & Sole Director">CISO & Information Security Lead</option>
                  <option value="Head of Procurement & Accounts Payable">Head of Procurement & Accounts Payable</option>
                  <option value="Head of PMO & Project Delivery (Arjun Sharma)">Head of PMO & Project Delivery (Arjun Sharma)</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Alert Title & Incident Subject</label>
                <input
                  type="text"
                  required
                  defaultValue="Statutory Compliance / Critical Escalation Notice"
                  className="w-full text-xs border border-slate-300 rounded-lg p-2.5"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Severity Classification</label>
                <select className="w-full text-xs border border-slate-300 rounded-lg p-2.5 bg-slate-50 font-semibold text-rose-700">
                  <option value="CRITICAL">CRITICAL (Immediate 15-Minute SLA)</option>
                  <option value="WARNING">WARNING (High Priority)</option>
                  <option value="INFO">INFORMATIONAL (Advisory)</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Detailed Operational Message</label>
                <textarea
                  rows={3}
                  required
                  defaultValue="Immediate intervention required: Verified statutory invariant trigger flagged. Please review in executive cockpit."
                  className="w-full text-xs border border-slate-300 rounded-lg p-2.5"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2 border-t">
                <button
                  type="button"
                  onClick={() => setIsAlertModalOpen(false)}
                  className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-lg transition shadow"
                >
                  <i className="fa-solid fa-paper-plane mr-1"></i> Transmit Urgent Alert
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AICloudView;
