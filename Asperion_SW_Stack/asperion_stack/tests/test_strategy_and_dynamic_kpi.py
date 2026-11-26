"""
Unit & Integration Tests for Dynamic Strategy, Function Matrix, Enterprise KPIs, and Decision Journal
"""
import pytest
from datetime import date
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.strategy_kpi import (
    StrategicFunction, CapabilityCapacity, EnterpriseKPI,
    StrategicDecisionThought, ImplementationRoadmapItem
)
from app.api.strategy import (
    list_functions, create_function, list_capabilities, create_capability,
    list_kpis, create_kpi, update_kpi_actual, list_thoughts_decisions,
    record_thought_or_decision, list_roadmap_items, create_roadmap_item, get_strategy_summary
)
from app.api.pmo import create_wbs_task, WBSTaskCreate
from app.schemas.strategy_kpi import (
    StrategicFunctionCreate, CapabilityCapacityCreate,
    EnterpriseKPICreate, EnterpriseKPIUpdate,
    StrategicDecisionThoughtCreate, ImplementationRoadmapItemCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_strategy_functions_crud(db_session):
    db_session.query(StrategicFunction).filter(StrategicFunction.function_name == "Client Solutions & Pre-Sales").delete()
    db_session.commit()
    funcs = list_functions(db=db_session)
    assert len(funcs) >= 4
    names = [f.function_name for f in funcs]
    assert "Leadership & Corporate Governance" in names

    # Add a new function
    new_fn = StrategicFunctionCreate(
        function_name="Client Solutions & Pre-Sales",
        function_owner="Pre-Sales Lead",
        core_capabilities="Deal structuring, RFP solutions, client demos",
        review_cadence="Fortnightly",
        maturity_level="L1"
    )
    saved = create_function(new_fn, db=db_session)
    assert saved.id is not None
    assert saved.function_name == "Client Solutions & Pre-Sales"

def test_strategy_capabilities_crud(db_session):
    db_session.query(CapabilityCapacity).filter(CapabilityCapacity.capability_name == "Kubernetes Cloud Migration").delete()
    db_session.commit()
    caps = list_capabilities(db=db_session)
    assert len(caps) >= 1

    new_cap = CapabilityCapacityCreate(
        capability_name="Kubernetes Cloud Migration",
        current_capacity="Docker Swarm Single Host",
        target_capacity="EKS Multi-Cluster",
        primary_constraint="Cloud infrastructure expertise",
        priority="High"
    )
    saved = create_capability(new_cap, db=db_session)
    assert saved.id is not None
    assert saved.priority == "High"

def test_strategy_kpis_crud_and_variance(db_session):
    db_session.query(EnterpriseKPI).filter(EnterpriseKPI.kpi_code == "KPI-TST-01").delete()
    db_session.commit()
    # Create new KPI
    kpi_in = EnterpriseKPICreate(
        kpi_code="KPI-TST-01",
        category="Delivery",
        name="API Response Latency p95",
        target_value=100.0,
        actual_value=65.0,
        unit="ms",
        period="JUN-2026",
        owner="Tech Lead"
    )
    saved = create_kpi(kpi_in, db=db_session)
    assert saved.id is not None
    assert saved.variance == -35.0  # (65 - 100)
    assert saved.variance_pct == -35.0

    # Update actual value
    updated = update_kpi_actual(
        kpi_id=saved.id,
        update_data=EnterpriseKPIUpdate(actual_value=50.0, status="Achieved"),
        db=db_session
    )
    assert updated.actual_value == 50.0
    assert updated.variance == -50.0
    assert updated.status == "Achieved"

def test_strategic_decisions_and_thoughts(db_session):
    entries = list_thoughts_decisions(db=db_session)
    assert len(entries) >= 2

    # Add new thought
    th = StrategicDecisionThoughtCreate(
        entry_type="Architecture Note",
        title="Event-Driven Microservices Evaluation",
        author="Tech Lead",
        context_background="Assessing pub/sub queues for financial ledger async processing.",
        decision_rationale="FastAPI background tasks sufficient for current OPC transactional scale.",
        tags="Architecture, Performance"
    )
    saved = record_thought_or_decision(th, db=db_session)
    assert saved.id is not None
    assert saved.entry_type == "Architecture Note"

def test_implementation_roadmap_items(db_session):
    items = list_roadmap_items(db=db_session)
    assert len(items) >= 1

    item_in = ImplementationRoadmapItemCreate(
        workstream="Cybersecurity",
        action_item="Execute ISO 27001 Internal Surveillance Audit",
        priority="High",
        owner="CISO Lead",
        start_date=date(2026, 8, 1),
        due_date=date(2026, 8, 30),
        progress_pct=10,
        status="In Progress"
    )
    saved = create_roadmap_item(item_in, db=db_session)
    assert saved.id is not None
    assert saved.workstream == "Cybersecurity"

def test_strategy_summary_metrics(db_session):
    summary = get_strategy_summary(db=db_session)
    assert summary["status"] == "success"
    assert summary["strategic_functions_count"] >= 4
    assert summary["kpis"]["total"] >= 3
    assert summary["kpis"]["health_score_pct"] > 0
    assert summary["executive_decisions_logged"] >= 2

def test_pmo_task_creation_endpoint(db_session):
    task_in = WBSTaskCreate(
        project_id=1,
        wbs_code="WBS-1.5",
        task_name="Interactive Dynamic Strategy UI Verification",
        owner="QA Team",
        planned_hours=8.0
    )
    saved = create_wbs_task(task_in, db=db_session)
    assert saved.id is not None
    assert saved.task_name == "Interactive Dynamic Strategy UI Verification"
