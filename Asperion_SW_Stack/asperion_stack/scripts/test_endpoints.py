import urllib.request
import json

endpoints = [
    # Operations
    "/api/v1/operations/ledger",
    "/api/v1/operations/bcp-snapshots",
    "/api/v1/operations/dpdp-consents",
    "/api/v1/operations/telemetry",
    # Infrastructure
    "/api/v1/infrastructure/overview",
    "/api/v1/infrastructure/passkeys",
    "/api/v1/infrastructure/zero-trust-policies",
    "/api/v1/infrastructure/dr-simulations",
    "/api/v1/infrastructure/assets",
    "/api/v1/infrastructure/cloud-accounts",
    "/api/v1/infrastructure/iam-credentials",
    "/api/v1/infrastructure/certificates-secrets",
    "/api/v1/infrastructure/provisioning-checklists",
    # SecOps
    "/api/v1/secops/incidents",
    "/api/v1/secops/siem-alerts",
    "/api/v1/secops/evidence-locker",
    "/api/v1/secops/threat-intel",
    "/api/v1/secops/playbooks",
    # Vault
    "/api/v1/vault/documents",
    "/api/v1/vault/categories",
    # Strategy
    "/api/v1/strategy/kpis",
    "/api/v1/strategy/initiatives",
    "/api/v1/strategy/decisions",
    "/api/v1/strategy/executive-decisions",
    # Analytics / Visual Intelligence
    "/api/v1/analytics/overview",
    "/api/v1/analytics/financial-charts",
    "/api/v1/analytics/headcount-trends",
    # Internal Service Desk
    "/api/v1/internal-support/tickets",
    "/api/v1/internal-support/alerts",
    # ITSM
    "/api/v1/itsm/problems",
    "/api/v1/itsm/changes",
    "/api/v1/itsm/nodes",
    "/api/v1/itsm/runbooks",
    "/api/v1/itsm/lois",
    # Teams
    "/api/v1/teams/channels",
    "/api/v1/teams/channels/c-general/messages",
    # SharePoint
    "/api/v1/sharepoint/documents",
    "/api/v1/sharepoint/folders",
    # Training
    "/api/v1/training/courses",
    "/api/v1/training/enrollments",
    # Governance
    "/api/v1/governance/directors",
    "/api/v1/governance/resolutions",
    # Procurement
    "/api/v1/procurement/purchase-orders",
    "/api/v1/procurement/vendors",
    # SDLC
    "/api/v1/sdlc/repositories",
    "/api/v1/sdlc/pipelines"
]

print(f"{'Endpoint':<45} | {'Status':<8} | {'Items'}")
print("-" * 65)

for ep in endpoints:
    url = f"http://127.0.0.1:8080{ep}"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode())
        count = len(data) if isinstance(data, list) else len(data.keys()) if isinstance(data, dict) else 1
        print(f"{ep:<45} | 200 OK   | {count}")
    except Exception as e:
        print(f"{ep:<45} | ERR      | {e}")
