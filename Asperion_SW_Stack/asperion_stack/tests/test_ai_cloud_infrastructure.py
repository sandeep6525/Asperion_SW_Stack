"""
Asperion Enterprise OS - Comprehensive Test Suite for AI Model APIs, MCP Servers, Multi-Cloud & Authenticity Mesh
Validates:
1. Executive Health & AI Budget Utilization Overview
2. Production AI Reasoning Models (Gemini 2.5 Pro, Claude 3.7 Sonnet, DeepSeek-R1, Embeddings)
3. Model Context Protocol (MCP) Server Registry & Live Latency Pings
4. Multi-Cloud & Kubernetes Infrastructure Topology
5. Cryptographic Authenticity, Verifiable Digital Signatures & FIPS Seals
6. Automated Executive Escalation Rules & Direct Dispatch to Department Heads
"""
import uuid
from datetime import date
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.ai_cloud import (
    get_ai_cloud_overview,
    list_ai_models, create_ai_model,
    list_mcp_servers, create_mcp_server, ping_mcp_server,
    list_cloud_nodes, create_cloud_node,
    list_authenticity_certificates, create_authenticity_certificate,
    list_executive_alert_rules, create_executive_alert_rule, trigger_alert_dispatch
)
from app.schemas.ai_infrastructure import (
    AIModelEndpointCreate, MCPServerCatalogCreate,
    CloudInfrastructureTopologyCreate, SecurityAuthenticityCertificateCreate,
    ExecutiveAlertRuleCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_ai_cloud_overview_telemetry(db_session):
    overview = get_ai_cloud_overview(db=db_session)
    assert overview is not None
    assert overview["status"] == "HEALTHY"
    assert overview["ai_models_count"] >= 4
    assert overview["total_ai_budget_inr"] > 0
    assert overview["mcp_servers_count"] >= 4
    assert overview["active_mcp_servers"] >= 4
    assert overview["cloud_nodes_count"] >= 4
    assert overview["average_uptime_sla_pct"] >= 99.0
    assert overview["certificates_count"] >= 3
    assert overview["executive_alert_rules_count"] >= 4

def test_ai_models_catalog_and_creation(db_session):
    models = list_ai_models(db=db_session)
    assert len(models) >= 4
    codes = [m.endpoint_code for m in models]
    assert "AI-GEMINI-25-PRO" in codes
    assert "AI-CLAUDE-37-SONNET" in codes
    assert "AI-DEEPSEEK-R1" in codes

    # Test create new custom model
    unique_code = f"AI-CUSTOM-{uuid.uuid4().hex[:4].upper()}"
    new_model = AIModelEndpointCreate(
        endpoint_code=unique_code,
        model_name="Custom Specialized Code SLM",
        provider="Local VLLM",
        model_family="Code Intelligence",
        context_window_tokens=65536,
        rpm_limit=120,
        tpm_limit=400000,
        avg_latency_ms=180.0,
        cost_per_million_tokens_inr=25.0,
        monthly_budget_inr=10000.0
    )
    created = create_ai_model(payload=new_model, db=db_session)
    assert created.id is not None
    assert created.endpoint_code == unique_code

def test_mcp_servers_and_ping(db_session):
    mcps = list_mcp_servers(db=db_session)
    assert len(mcps) >= 4
    server_ids = [s.server_id for s in mcps]
    assert "MCP-SQLITE-ERP" in server_ids
    assert "MCP-AWS-BEDROCK" in server_ids
    assert "MCP-GITHUB-SDLC" in server_ids

    # Ping MCP server
    ping_res = ping_mcp_server(server_id="MCP-SQLITE-ERP", db=db_session)
    assert ping_res["status"] == "CONNECTED"
    assert "Healthy" in ping_res["latency"]

def test_cloud_infrastructure_topology(db_session):
    nodes = list_cloud_nodes(db=db_session)
    assert len(nodes) >= 4
    node_codes = [n.node_code for n in nodes]
    assert "CLD-K8S-MUM-01" in node_codes
    assert "CLD-CF-EDGE-01" in node_codes

    k8s = next(n for n in nodes if n.node_code == "CLD-K8S-MUM-01")
    assert k8s.uptime_sla_pct >= 99.99
    assert k8s.zero_trust_ingress_verified is True

def test_security_authenticity_certificates(db_session):
    certs = list_authenticity_certificates(db=db_session)
    assert len(certs) >= 3
    codes = [c.cert_code for c in certs]
    assert "AUTH-CORP-DSC-01" in codes
    assert "AUTH-TLS-WILDCARD-02" in codes

    dsc = next(c for c in certs if c.cert_code == "AUTH-CORP-DSC-01")
    assert "Class 3" in dsc.certificate_name
    assert dsc.days_until_expiry > 0
    assert dsc.status == "Valid & Trusted"

def test_executive_alert_rules_and_dispatch(db_session):
    rules = list_executive_alert_rules(db=db_session)
    assert len(rules) >= 4
    codes = [r.rule_code for r in rules]
    assert "EAR-FIN-LIQ-01" in codes
    assert "EAR-SEC-P1-02" in codes
    assert "EAR-MSME-45D-03" in codes

    # Trigger manual dispatch to head
    dispatch_res = trigger_alert_dispatch(
        rule_code="EAR-FIN-LIQ-01",
        custom_message="Automated Test: Working capital reserves audited.",
        db=db_session
    )
    assert dispatch_res["status"] == "DISPATCHED"
    assert dispatch_res["notification_code"] is not None
    assert "Sole Director" in dispatch_res["target_role"]
    assert "WhatsApp_Cloud_API" in dispatch_res["channels"]
