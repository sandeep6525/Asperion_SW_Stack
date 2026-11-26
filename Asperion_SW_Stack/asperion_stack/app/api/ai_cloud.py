"""
Asperion Enterprise OS - AI APIs, MCP Servers, Cloud Infrastructure & Authenticity API Router
Pillars: AI Reasoning Engines, Model Context Protocol, Hybrid Multi-Cloud Topology & Authenticity Verification
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import get_db
from app.models.ai_infrastructure import (
    AIModelEndpoint, MCPServerCatalog, CloudInfrastructureTopology,
    SecurityAuthenticityCertificate, ExecutiveAlertRule
)
from app.schemas.ai_infrastructure import (
    AIModelEndpointCreate, AIModelEndpointOut,
    MCPServerCatalogCreate, MCPServerCatalogOut,
    CloudInfrastructureTopologyCreate, CloudInfrastructureTopologyOut,
    SecurityAuthenticityCertificateCreate, SecurityAuthenticityCertificateOut,
    ExecutiveAlertRuleCreate, ExecutiveAlertRuleOut
)
from app.engines.ai_cloud_engine import (
    evaluate_ai_and_cloud_infrastructure_health,
    dispatch_executive_alert_to_head
)

router = APIRouter(prefix="/ai-cloud", tags=["AI APIs, MCPs & Cloud Infrastructure"])

@router.get("/overview", response_model=Dict[str, Any])
def get_ai_cloud_overview(db: Session = Depends(get_db)):
    """Executive summary of AI models, MCP servers, cloud nodes, and authenticity certs."""
    return evaluate_ai_and_cloud_infrastructure_health(db)

# --- 1. AI MODEL ENDPOINTS ---
@router.get("/ai-models", response_model=List[AIModelEndpointOut])
def list_ai_models(db: Session = Depends(get_db)):
    """List all configured AI LLM/SLM endpoints with context window and spend metrics."""
    return db.query(AIModelEndpoint).order_by(AIModelEndpoint.endpoint_code.asc()).all()

@router.post("/ai-models", response_model=AIModelEndpointOut, status_code=status.HTTP_201_CREATED)
def create_ai_model(payload: AIModelEndpointCreate, db: Session = Depends(get_db)):
    """Register a new enterprise AI endpoint."""
    existing = db.query(AIModelEndpoint).filter(AIModelEndpoint.endpoint_code == payload.endpoint_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"AI Endpoint {payload.endpoint_code} already registered.")
    model = AIModelEndpoint(**payload.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

# --- 2. MODEL CONTEXT PROTOCOL (MCP) SERVERS ---
@router.get("/mcp-servers", response_model=List[MCPServerCatalogOut])
def list_mcp_servers(db: Session = Depends(get_db)):
    """List registered Model Context Protocol (MCP) servers."""
    return db.query(MCPServerCatalog).order_by(MCPServerCatalog.server_id.asc()).all()

@router.post("/mcp-servers", response_model=MCPServerCatalogOut, status_code=status.HTTP_201_CREATED)
def create_mcp_server(payload: MCPServerCatalogCreate, db: Session = Depends(get_db)):
    """Register a new Model Context Protocol (MCP) tool integration server."""
    existing = db.query(MCPServerCatalog).filter(MCPServerCatalog.server_id == payload.server_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"MCP Server {payload.server_id} already exists.")
    srv = MCPServerCatalog(**payload.dict())
    db.add(srv)
    db.commit()
    db.refresh(srv)
    return srv

@router.post("/mcp-servers/{server_id}/ping", response_model=Dict[str, Any])
def ping_mcp_server(server_id: str, db: Session = Depends(get_db)):
    """Simulate live health check and latency ping to an MCP server."""
    srv = db.query(MCPServerCatalog).filter(MCPServerCatalog.server_id == server_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="MCP Server not found.")
    srv.last_ping_status = f"Healthy ({round(10.5 + (len(server_id) % 5), 1)}ms)"
    srv.is_connected = True
    db.commit()
    return {"server_id": srv.server_id, "status": "CONNECTED", "latency": srv.last_ping_status}

# --- 3. CLOUD INFRASTRUCTURE TOPOLOGY ---
@router.get("/cloud-nodes", response_model=List[CloudInfrastructureTopologyOut])
def list_cloud_nodes(db: Session = Depends(get_db)):
    """List multi-cloud topology, Kubernetes clusters, and regional nodes."""
    return db.query(CloudInfrastructureTopology).order_by(CloudInfrastructureTopology.node_code.asc()).all()

@router.post("/cloud-nodes", response_model=CloudInfrastructureTopologyOut, status_code=status.HTTP_201_CREATED)
def create_cloud_node(payload: CloudInfrastructureTopologyCreate, db: Session = Depends(get_db)):
    """Register a new cloud cluster or infrastructure node."""
    existing = db.query(CloudInfrastructureTopology).filter(CloudInfrastructureTopology.node_code == payload.node_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Node {payload.node_code} already registered.")
    node = CloudInfrastructureTopology(**payload.dict())
    db.add(node)
    db.commit()
    db.refresh(node)
    return node

# --- 4. SECURITY & AUTHENTICITY CERTIFICATES ---
@router.get("/certificates", response_model=List[SecurityAuthenticityCertificateOut])
def list_authenticity_certificates(db: Session = Depends(get_db)):
    """List corporate digital signature certificates, TLS keys, and document signing credentials."""
    return db.query(SecurityAuthenticityCertificate).order_by(SecurityAuthenticityCertificate.cert_code.asc()).all()

@router.post("/certificates", response_model=SecurityAuthenticityCertificateOut, status_code=status.HTTP_201_CREATED)
def create_authenticity_certificate(payload: SecurityAuthenticityCertificateCreate, db: Session = Depends(get_db)):
    """Register an authenticity certificate or corporate digital signature."""
    existing = db.query(SecurityAuthenticityCertificate).filter(SecurityAuthenticityCertificate.cert_code == payload.cert_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Certificate {payload.cert_code} already registered.")
    cert = SecurityAuthenticityCertificate(**payload.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

# --- 5. EXECUTIVE ALERT RULES & DISPATCH TO HEADS ---
@router.get("/alert-rules", response_model=List[ExecutiveAlertRuleOut])
def list_executive_alert_rules(db: Session = Depends(get_db)):
    """List configured automated escalation rules to department heads."""
    return db.query(ExecutiveAlertRule).order_by(ExecutiveAlertRule.rule_code.asc()).all()

@router.post("/alert-rules", response_model=ExecutiveAlertRuleOut, status_code=status.HTTP_201_CREATED)
def create_executive_alert_rule(payload: ExecutiveAlertRuleCreate, db: Session = Depends(get_db)):
    """Create a new automated executive alert escalation rule."""
    existing = db.query(ExecutiveAlertRule).filter(ExecutiveAlertRule.rule_code == payload.rule_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Alert Rule {payload.rule_code} already exists.")
    rule = ExecutiveAlertRule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.post("/alert-rules/{rule_code}/dispatch", response_model=Dict[str, Any])
def trigger_alert_dispatch(
    rule_code: str,
    custom_message: Optional[str] = Query(None, description="Optional custom incident or escalation summary"),
    db: Session = Depends(get_db)
):
    """
    Manually or programmatically triggers an automated alert dispatch to the concerned Head.
    Dispatches across WhatsApp Cloud API, Email SES, and In-App notification tray.
    """
    rule = db.query(ExecutiveAlertRule).filter(ExecutiveAlertRule.rule_code == rule_code).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Executive alert rule not found.")
    
    msg = custom_message or f"Trigger condition met: {rule.trigger_condition}"
    return dispatch_executive_alert_to_head(
        db=db,
        alert_code=rule.rule_code,
        title=rule.title,
        message=msg,
        severity="CRITICAL",
        target_role=rule.target_head_role,
        module_source="EXECUTIVE_ESCALATION"
    )
