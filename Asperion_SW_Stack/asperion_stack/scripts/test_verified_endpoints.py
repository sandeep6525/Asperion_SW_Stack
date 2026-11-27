import urllib.request
import json

verified_endpoints = [
    # Operations
    "/api/v1/operations/overview",
    "/api/v1/operations/ledger",
    "/api/v1/operations/bcp-dr/snapshots",
    "/api/v1/operations/dpdp/consents",
    "/api/v1/operations/telemetry/live",
    # Infrastructure
    "/api/v1/infrastructure/overview",
    "/api/v1/infrastructure/passkeys",
    "/api/v1/infrastructure/zero-trust-policies",
    "/api/v1/infrastructure/dr-simulations",
    "/api/v1/infrastructure/assets",
    "/api/v1/infrastructure/cloud-accounts",
    "/api/v1/infrastructure/certificates-secrets",
    "/api/v1/infrastructure/provisioning-checklists",
    # SecOps / Cybersecurity
    "/api/v1/cybersecurity/overview",
    "/api/v1/cybersecurity/incidents",
    "/api/v1/cybersecurity/alerts",
    "/api/v1/cybersecurity/evidence",
    "/api/v1/cybersecurity/threat-intel",
    "/api/v1/cybersecurity/playbooks",
    # Vault
    "/api/v1/vault/stats",
    "/api/v1/vault/categories",
    "/api/v1/vault/documents",
    # Strategy
    "/api/v1/strategy/summary",
    "/api/v1/strategy/kpis",
    "/api/v1/strategy/roadmap",
    "/api/v1/strategy/capabilities",
    "/api/v1/strategy/thoughts-decisions",
    # Analytics
    "/api/v1/analytics/overview",
    "/api/v1/analytics/financial-charts",
    "/api/v1/analytics/balanced-scorecard",
    # Internal Support
    "/api/v1/internal-support/summary",
    "/api/v1/internal-support/tickets",
    "/api/v1/internal-support/notifications",
    # ITSM
    "/api/v1/itsm/overview",
    "/api/v1/itsm/cmdb/nodes",
    "/api/v1/itsm/problems",
    "/api/v1/itsm/changes",
    "/api/v1/itsm/procurement-lois",
    "/api/v1/itsm/runbook-fixes",
    # Communications / Teams
    "/api/v1/communications/overview",
    "/api/v1/communications/channels",
    # SharePoint
    "/api/v1/sharepoint/overview",
    "/api/v1/sharepoint/articles",
    "/api/v1/sharepoint/document-library",
    # Training
    "/api/v1/training/overview",
    "/api/v1/training/tracks",
    "/api/v1/training/modules",
    "/api/v1/training/enrollments",
    # AI Cloud
    "/api/v1/ai-cloud/overview",
    "/api/v1/ai-cloud/ai-models",
    "/api/v1/ai-cloud/mcp-servers",
    # Agentic AI
    "/api/v1/agentic-ai/overview",
    "/api/v1/agentic-ai/agents",
    "/api/v1/agentic-ai/missions",
    # Governance
    "/api/v1/governance/entity",
    "/api/v1/governance/authority-matrix",
    "/api/v1/governance/compliance-calendar",
    "/api/v1/governance/resolutions",
    # SDLC
    "/api/v1/sdlc/overview",
    "/api/v1/sdlc/repositories",
    "/api/v1/sdlc/pipelines",
    "/api/v1/sdlc/defects"
]

print(f"{'Endpoint':<45} | {'Status':<8} | {'Items'}")
print("-" * 65)

for ep in verified_endpoints:
    url = f"http://127.0.0.1:8080{ep}"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode())
        count = len(data) if isinstance(data, list) else len(data.keys()) if isinstance(data, dict) else 1
        print(f"{ep:<45} | 200 OK   | {count}")
    except Exception as e:
        print(f"{ep:<45} | ERR      | {e}")
