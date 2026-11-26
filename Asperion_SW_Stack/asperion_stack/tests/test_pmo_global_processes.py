"""
Asperion Enterprise OS - Unit Tests for Globally Acknowledged PMO Processes
Tests stage-gate lifecycle:
1. Stage-Gate 1: Project Intake & Strategic Business Case
2. Stage-Gate 2: Project Charter Baseline & Scope Lock
3. SteerCo Action & Decision Registers
4. Resource Capacity & Skills Allocation Planning
5. Stage-Gate 4: Quality & Client UAT Acceptance Sign-Offs
6. Stage-Gate 5: Project Closure, Lessons Learned & Commercial Handover
7. PMO Governance Health Overview
"""
import uuid
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.pmo import (
    list_project_intakes, create_project_intake,
    list_project_charters,
    list_actions_and_decisions,
    list_capacity_plan_items,
    list_quality_uat_items,
    list_project_closures,
    get_pmo_governance_overview
)
from app.schemas.pmo import ProjectIntakeCreate

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_pmo_stage_gate_1_intakes(db_session):
    # 1. List Intakes
    intakes = list_project_intakes(db=db_session)
    assert len(intakes) >= 2
    assert any(i.intake_code == "ADT-INTK-2026-001" for i in intakes)

    # 2. Create New Intake
    uniq_code = f"ADT-INTK-TEST-{uuid.uuid4().hex[:6].upper()}"
    new_intake = ProjectIntakeCreate(
        intake_code=uniq_code,
        project_name="Cloud Multi-Region Failover Architecture",
        sponsor="Varadi Vijay (Director)",
        client_or_internal="Zenith Global Corp",
        strategic_fit="Critical",
        expected_value="Zero-downtime compliance under SOC2 & ISO 27001",
        estimated_budget_inr=1200000.0
    )
    created = create_project_intake(intake_in=new_intake, db=db_session)
    assert created.intake_code == uniq_code
    assert created.intake_status == "Under Evaluation"


def test_pmo_stage_gate_2_charter_baseline(db_session):
    charters = list_project_charters(db=db_session)
    assert len(charters) >= 1
    c = charters[0]
    assert c.signoff_status == "Approved & Baselined"
    assert c.problem_statement is not None
    assert c.measurable_success_criteria is not None


def test_pmo_action_decision_register(db_session):
    items = list_actions_and_decisions(db=db_session)
    assert len(items) >= 3
    has_action = any(item.item_type == "Action" for item in items)
    has_decision = any(item.item_type == "Decision" for item in items)
    assert has_action and has_decision


def test_pmo_resource_capacity_planning(db_session):
    caps = list_capacity_plan_items(db=db_session)
    assert len(caps) >= 3
    for cp in caps:
        assert cp.utilization_pct is not None
        assert cp.status is not None


def test_pmo_stage_gate_4_quality_uat(db_session):
    uats = list_quality_uat_items(db=db_session)
    assert len(uats) >= 3
    assert all("Passed" in u.status for u in uats)


def test_pmo_stage_gate_5_project_closures(db_session):
    closures = list_project_closures(db=db_session)
    assert len(closures) >= 2
    for cl in closures:
        assert cl.lessons_learned_summary is not None
        assert cl.closure_status == "Completed"


def test_pmo_governance_health_overview(db_session):
    data = get_pmo_governance_overview(db=db_session)
    assert data["status"] == "success"
    assert "stage_gates" in data
    assert data["stage_gates"]["gate_1_intakes"] >= 2
    assert data["stage_gates"]["gate_4_uat_deliverables"] >= 3
    assert data["governance_metrics"]["uat_pass_rate_pct"] >= 90.0
