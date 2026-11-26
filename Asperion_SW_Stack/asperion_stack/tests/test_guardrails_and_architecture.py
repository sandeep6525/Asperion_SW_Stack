"""
Asperion Enterprise OS - Comprehensive Test Suite for Enterprise Guardrails & System Architecture
Tests:
1. Enterprise Guardrails Overview Telemetry & Statutory Compliance Score
2. Guardrail Policy Rules Registry & Invariant Configuration (FinOps, MSMED, DPDP, HRMS, SDLC, DOA, CERT-In, SecOps)
3. New Guardrail Policy Creation & Validation
4. Live Autonomous Guardrails Evaluator Trigger & Verification
5. Guardrail Execution & Intervention Audit Logs
6. Interactive Multi-Stage Process Flowcharts (Mermaid Graphs & Step Data)
7. System Architecture Blueprints & Security Boundaries
8. Technical Architecture & DOA Governance Documents Catalog
"""
import uuid
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.guardrails import (
    get_guardrails_overview,
    list_guardrail_rules,
    create_guardrail_rule,
    run_live_guardrails_evaluation,
    list_guardrail_logs,
    list_architecture_blueprints,
    list_enterprise_flowcharts,
    list_technical_documents
)
from app.schemas.guardrails import GuardrailRuleCreate

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_guardrails_overview_telemetry(db_session):
    overview = get_guardrails_overview(db=db_session)
    assert overview is not None
    assert "status" in overview
    assert overview["total_rules"] >= 8
    assert overview["active_rules"] >= 8
    assert overview["total_evaluations"] >= 0
    assert overview["compliance_score_pct"] >= 0.0
    assert len(overview["supported_frameworks"]) >= 5
    assert "Internal Financial Controls (IFC)" in overview["supported_frameworks"]
    assert "Digital Personal Data Protection (DPDP) Act 2023" in overview["supported_frameworks"]

def test_list_guardrail_rules(db_session):
    rules = list_guardrail_rules(db=db_session)
    assert len(rules) >= 8
    codes = [r.rule_code for r in rules]
    assert "GRD-FIN-001" in codes
    assert "GRD-MSME-002" in codes
    assert "GRD-DPDP-003" in codes
    assert "GRD-HRMS-004" in codes
    assert "GRD-SDLC-005" in codes
    assert "GRD-DOA-006" in codes
    assert "GRD-CERT-007" in codes
    assert "GRD-SECR-008" in codes

def test_create_custom_guardrail_rule(db_session):
    unique_code = f"GRD-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_rule = GuardrailRuleCreate(
        rule_code=unique_code,
        name="Automated Cloud Cost Ceiling Invariant",
        category="FinOps",
        regulatory_framework="Internal Financial Controls (IFC)",
        severity="High_Warning",
        enforcement_mode="Alert_Escalate",
        description="Flags AWS & Cloud infrastructure burn rate exceeding monthly allocated threshold.",
        enforcement_logic="monthly_burn_rate_inr <= 150000.0"
    )
    created = create_guardrail_rule(payload=new_rule, db=db_session)
    assert created.id is not None
    assert created.rule_code == unique_code
    assert created.is_active is True

def test_live_autonomous_guardrails_evaluation(db_session):
    result = run_live_guardrails_evaluation(db=db_session)
    assert result is not None
    assert result["status"] == "success"
    assert result["total_rules_active"] >= 8
    assert result["total_evaluations"] > 0
    assert result["compliance_score_pct"] > 80.0
    assert len(result["rule_evaluations"]) >= 8

def test_guardrail_execution_audit_logs(db_session):
    logs = list_guardrail_logs(limit=50, result_filter=None, db=db_session)
    assert len(logs) >= 1
    first_log = logs[0]
    assert first_log.execution_id is not None
    assert first_log.evaluation_result in ["PASSED", "BLOCKED", "AUTO_HEALED"]
    assert first_log.action_taken is not None

def test_enterprise_process_flowcharts():
    flowcharts = list_enterprise_flowcharts()
    assert len(flowcharts) >= 6
    fc_ids = [fc["flowchart_id"] for fc in flowcharts]
    assert "FC-FIN-001" in fc_ids
    assert "FC-HRMS-002" in fc_ids
    assert "FC-SDLC-003" in fc_ids
    assert "FC-SEC-004" in fc_ids
    assert "FC-PMO-005" in fc_ids
    assert "FC-PROC-006" in fc_ids

    # Validate Mermaid code and steps structure
    fin_fc = next(f for f in flowcharts if f["flowchart_id"] == "FC-FIN-001")
    assert "graph TD" in fin_fc["mermaid_diagram"]
    assert len(fin_fc["steps"]) == 4
    assert fin_fc["steps"][0]["step_number"] == 1
    assert "GRD-FIN-001" in fin_fc["active_guardrails"]

def test_architecture_blueprints(db_session):
    blueprints = list_architecture_blueprints(db=db_session)
    assert len(blueprints) >= 3
    codes = [b.blueprint_code for b in blueprints]
    assert "ARCH-E2E-001" in codes
    assert "ARCH-SEC-002" in codes
    assert "ARCH-DATA-003" in codes

    e2e = next(b for b in blueprints if b.blueprint_code == "ARCH-E2E-001")
    assert "FastAPI" in e2e.key_components or "SQLite" in e2e.key_components
    assert "graph TB" in e2e.diagram_mermaid

def test_technical_architecture_documents():
    docs = list_technical_documents()
    assert len(docs) >= 4
    doc_ids = [d["doc_id"] for d in docs]
    assert "DOC-ARCH-001" in doc_ids
    assert "DOC-SEC-002" in doc_ids
    assert "DOC-DOA-003" in doc_ids
    assert "DOC-SDLC-004" in doc_ids

    arch_doc = next(d for d in docs if d["doc_id"] == "DOC-ARCH-001")
    assert "ISO/IEC 27001:2022" in arch_doc["compliance_standards"]
    assert len(arch_doc["key_sections"]) >= 5
