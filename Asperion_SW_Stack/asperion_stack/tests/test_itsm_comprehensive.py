"""
Unit & Integration Tests for Comprehensive IT Service Management (ITSM) Suite
Covers CMDB Configuration Items, Problem KEDB, CAB Changes,
Automated Runbook Fixes, Procurement Letters of Intent (LOIs), and SLAs.
"""
import uuid
import pytest
from datetime import datetime, date, timedelta
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.itsm import (
    ConfigurationItem, ITSMProblem, ITSMChangeRequest, ITSMRunbookFix,
    ITSMProcurementLOI, ITSMSLAContract
)
from app.api.itsm import (
    get_itsm_overview, list_cmdb_nodes, create_cmdb_node, get_cmdb_topology,
    list_problems, create_problem, list_change_requests, create_change_request,
    review_change_request, list_runbook_fixes, execute_runbook_fix,
    list_procurement_lois, create_procurement_loi, get_loi_html,
    list_sla_contracts, create_sla_contract
)
from app.schemas.itsm import (
    ConfigurationItemCreate, ITSMProblemCreate, ITSMChangeRequestCreate,
    ITSMChangeReviewRequest, ITSMProcurementLOICreate, ITSMSLAContractCreate
)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

def test_itsm_overview(db_session):
    data = get_itsm_overview(db=db_session)
    assert data["status"] == "success"
    assert data["corporate_entity"] == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert data["cin"] == "U85500KA2026OPC222069"
    assert data["director"] == "Varadi Vijay"
    
    m = data["metrics"]
    assert m["total_configuration_items"] >= 8
    assert m["cmdb_health_index_pct"] >= 95.0
    assert m["kedb_published_solutions"] >= 3
    assert m["active_procurement_lois"] >= 2
    assert m["total_procurement_pipeline_inr"] > 5000000.0
    assert m["average_service_uptime_pct"] >= 99.9

def test_cmdb_nodes_and_topology(db_session):
    nodes = list_cmdb_nodes(environment="Production", category="ALL", status="ALL", db=db_session)
    assert len(nodes) >= 6
    assert any(n.ci_code == "CI-SRV-GW-01" for n in nodes)
    assert any(n.ci_code == "CI-DB-PROD-01" for n in nodes)

    # Register new CI node with unique code
    test_code = f"CI-TEST-REDIS-{uuid.uuid4().hex[:6].upper()}"
    new_ci = ConfigurationItemCreate(
        ci_code=test_code,
        ci_name="Secondary Read Replica Redis Cache",
        ci_type="In-Memory Cache",
        category="Database",
        environment="Production",
        tier="Tier-1 Business Critical",
        ip_address="10.0.3.61",
        fqdn="cache-replica.asperion.internal",
        cloud_provider="AWS ap-south-1",
        status="Operational",
        health_score=99.9,
        cpu_utilization_pct=12.0,
        memory_utilization_pct=30.0,
        disk_utilization_pct=8.0,
        upstream_dependencies_json='["CI-CACHE-REDIS-01"]',
        downstream_dependencies_json='[]'
    )
    created_ci = create_cmdb_node(node_in=new_ci, db=db_session)
    assert created_ci.id is not None
    assert created_ci.ci_code == test_code

    # Fetch topology
    topo = get_cmdb_topology(db=db_session)
    assert topo["status"] == "success"
    assert topo["total_nodes"] >= 8
    assert topo["total_edges"] >= 4
    assert any(e["relationship"] == "PROVIDES_SERVICE_TO" for e in topo["edges"])

def test_problem_management_kedb(db_session):
    # List KEDB published
    problems = list_problems(kedb_only=True, status="ALL", db=db_session)
    assert len(problems) >= 3
    assert any("PostgreSQL Connection Pool" in p.title for p in problems)

    # Create new problem with unique code
    test_prb = f"PRB-TEST-{uuid.uuid4().hex[:6].upper()}"
    new_prob = ITSMProblemCreate(
        problem_code=test_prb,
        title="Spike in JWT Token Deserialization Latency during Deployments",
        category="Microservice Performance",
        priority="P2-High",
        status="Known Error (KEDB)",
        impacted_ci_code="CI-SVC-AUTH-01",
        root_cause_analysis="5-Whys: Ed25519 public key re-fetching blocked HTTP event loop on auth service cold starts.",
        temporary_workaround="Warm up public key cache in static memory on service initialization.",
        permanent_fix_plan="Pre-bake public JWKS into local application configuration.",
        kedb_published=True,
        assigned_engineer="DevOps Lead",
        related_incidents_count=2
    )
    created_prob = create_problem(prob_in=new_prob, db=db_session)
    assert created_prob.id is not None
    assert created_prob.problem_code == test_prb
    assert created_prob.kedb_published is True

def test_change_enablement_and_cab_review(db_session):
    changes = list_change_requests(cab_status="ALL", change_type="ALL", db=db_session)
    assert len(changes) >= 2
    assert any(c.cr_code == "CR-2026-0042" for c in changes)

    # Create Change Request with unique code
    test_cr = f"CR-TEST-{uuid.uuid4().hex[:6].upper()}"
    new_cr = ITSMChangeRequestCreate(
        cr_code=test_cr,
        title="Migrate Horamavu HQ Biometric Kiosk to Dedicated VLAN 10",
        change_type="Normal",
        reason_for_change="Isolate biometric facial recognition and attendance kiosk traffic onto secure dedicated VLAN.",
        impact_scope="Horamavu HQ Perimeter Gateway (CI-HQ-ROUTER-01)",
        risk_level="Low",
        risk_score=20,
        cab_status="Submitted",
        implementation_plan="1. Provision VLAN 10. 2. Tag switchports. 3. Re-assign static DHCP leases. 4. Verify connectivity.",
        backout_rollback_plan="Revert port configuration to untagged VLAN 1 (Execution time: 2 mins).",
        test_validation_procedure="Verify ping and biometric attendance punch from Horamavu HQ Kiosk.",
        scheduled_start_time=datetime.utcnow() + timedelta(days=1),
        scheduled_end_time=datetime.utcnow() + timedelta(days=1, hours=2),
        outage_required=False,
        lead_implementer="Network Engineer"
    )
    created_cr = create_change_request(cr_in=new_cr, db=db_session)
    assert created_cr.id is not None
    assert created_cr.cab_status == "Submitted"

    # CAB Review & Approval
    review_req = ITSMChangeReviewRequest(
        action="APPROVE",
        reviewer_name="Varadi Vijay",
        reviewer_role="Founder & Sole Director",
        review_notes="Approved by CAB. Clear rollback plan provided."
    )
    reviewed = review_change_request(change_id=created_cr.id, review_in=review_req, db=db_session)
    assert reviewed.cab_status == "Approved"
    assert "Varadi Vijay" in reviewed.cab_approvers_json

def test_automated_runbook_execution(db_session):
    fixes = list_runbook_fixes(db=db_session)
    assert len(fixes) >= 3
    fix = fixes[0]

    initial_count = fix.execution_count
    resp = execute_runbook_fix(fix_id=fix.id, target_node="CI-DB-PROD-01", db=db_session)
    assert resp["status"] == "success"
    assert resp["health_restored"] is True
    assert len(resp["output_log"]) >= 4
    assert fix.fix_code in resp["message"]

    # Verify count increment
    db_session.refresh(fix)
    assert fix.execution_count == initial_count + 1

def test_procurement_loi_lifecycle_and_html_generation(db_session):
    lois = list_procurement_lois(db=db_session)
    assert len(lois) >= 2
    assert any(l.loi_number == "LOI-IT-2026-001" for l in lois)

    # Create new LOI with unique number
    test_loi = f"LOI-TEST-{uuid.uuid4().hex[:6].upper()}"
    new_loi = ITSMProcurementLOICreate(
        loi_number=test_loi,
        vendor_name="Lenovo Enterprise Solutions India",
        vendor_address="Prestige Tech Park, Marathahalli, Bengaluru - 560103",
        vendor_contact_person="Sunil Verma",
        vendor_email="sunil.verma@lenovo.com",
        asset_category="High-Performance Developer ThinkPad Workstations",
        scope_of_procurement="Procurement of 10x ThinkPad P1 Gen 7 Mobile Workstations for core engineering team.",
        equipment_specifications="ThinkPad P1 Gen 7, Intel Core Ultra 9, 64GB DDR5, NVIDIA RTX 4080 Ada, 2TB PCIe 4.0 SSD.",
        estimated_contract_value_inr=2400000.0,
        valid_until_date=date(2026, 12, 31)
    )
    created_loi = create_procurement_loi(loi_in=new_loi, db=db_session)
    assert created_loi.id is not None
    assert created_loi.director_signatory == "Varadi Vijay"
    assert created_loi.company_cin == "U85500KA2026OPC222069"

    # Fetch standalone HTML
    html_resp = get_loi_html(loi_id=created_loi.id, db=db_session)
    content = html_resp.body.decode()
    assert "LETTER OF INTENT (LOI)" in content
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in content
    assert "U85500KA2026OPC222069" in content
    assert "Varadi Vijay" in content
    assert "₹2,400,000.00" in content

def test_sla_contracts_catalog(db_session):
    slas = list_sla_contracts(db=db_session)
    assert len(slas) >= 3
    assert any(s.service_code == "SLA-CORE-API" for s in slas)
    
    api_sla = next(s for s in slas if s.service_code == "SLA-CORE-API")
    assert api_sla.target_uptime_pct >= 99.95
    assert api_sla.p1_resolution_hours <= 2.0
    assert "service credit" in api_sla.sla_penalty_clause

    # Fetch standalone HTML
    html_resp = get_loi_html(loi_id=created_loi.id, db=db_session)
    content = html_resp.body.decode()
    assert "LETTER OF INTENT (LOI)" in content
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in content
    assert "U85500KA2026OPC222069" in content
    assert "Varadi Vijay" in content
    assert "₹2,400,000.00" in content

def test_sla_contracts_catalog(db_session):
    slas = list_sla_contracts(db=db_session)
    assert len(slas) >= 3
    assert any(s.service_code == "SLA-CORE-API" for s in slas)
    
    api_sla = next(s for s in slas if s.service_code == "SLA-CORE-API")
    assert api_sla.target_uptime_pct >= 99.95
    assert api_sla.p1_resolution_hours <= 2.0
    assert "service credit" in api_sla.sla_penalty_clause
