"""
Unit & Integration Tests for Agentic AI & Autonomous Multi-Agent Swarm Suite
Covers Swarm Mesh Telemetry, Agent Personas, ReAct Execution Loops,
Human-in-the-Loop Signoff Gates, Granular Trace Auditing, and Tool Grounding.
"""
import pytest
import json
import uuid
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.agentic_ai import EnterpriseAgent, AgenticMission, AgentExecutionTrace
from app.api.agentic_ai import (
    get_swarm_overview, list_agents, create_agent, get_agent,
    list_missions, get_mission, dispatch_mission, approve_mission_endpoint,
    chat_agent, get_mission_traces
)
from app.schemas.agentic_ai import (
    EnterpriseAgentCreate, MissionDispatchPayload, MissionApprovalPayload,
    AgentChatRequest
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


def test_swarm_overview(db_session):
    """Verifies aggregate swarm telemetry, agent counts, and mission success velocity."""
    overview = get_swarm_overview(db=db_session)
    assert overview["status"] == "success"
    assert overview["total_agents"] >= 5
    assert overview["fleet_success_rate_pct"] > 0
    assert "autonomy_tiers" in overview
    assert "Level 4: Fully Autonomous" in overview["autonomy_tiers"]
    assert overview["mcp_tools_connected"] >= 15


def test_list_and_get_agents(db_session):
    """Verifies listing and querying specialized enterprise agent personas."""
    agents = list_agents(db=db_session)
    assert len(agents) >= 5
    codes = [a.agent_code for a in agents]
    assert "AGT-SRE-01" in codes
    assert "AGT-COMPLY-01" in codes
    assert "AGT-FINOPS-01" in codes
    assert "AGT-TALENT-01" in codes
    assert "AGT-DELIVERY-01" in codes

    sre = get_agent("AGT-SRE-01", db=db_session)
    assert sre.name == "SRE & DevSecOps Sentinel"
    assert "Level 4" in sre.autonomy_tier
    tools = json.loads(sre.assigned_tools_json)
    assert "mcp_cmdb_telemetry_scan" in tools


def test_create_agent(db_session):
    """Verifies registration of a new specialized autonomous agent in the swarm."""
    rand_code = f"AGT-TEST-{uuid.uuid4().hex[:6].upper()}"
    payload = EnterpriseAgentCreate(
        agent_code=rand_code,
        name="Test Autonomous Sentinel",
        role="Automated QA & Verifier",
        department="Quality Assurance",
        model_endpoint="Gemini 2.5 Flash",
        system_prompt="Execute regression tests and report anomalies.",
        autonomy_tier="Level 4: Fully Autonomous",
        assigned_tools_json=json.dumps(["test_runner", "defect_filer"]),
        is_active=True,
        health_status="Optimal",
        total_missions_executed=5,
        success_rate_pct=100.0,
        avg_execution_latency_sec=0.8
    )
    new_agent = create_agent(payload, db=db_session)
    assert new_agent.id is not None
    assert new_agent.agent_code == rand_code

    retrieved = get_agent(rand_code, db=db_session)
    assert retrieved.name == "Test Autonomous Sentinel"


def test_list_and_filter_missions(db_session):
    """Verifies querying autonomous mission history and filtering by status."""
    all_missions = list_missions(db=db_session)
    assert len(all_missions) >= 4

    completed = list_missions(status="Completed", db=db_session)
    assert len(completed) >= 3
    for m in completed:
        assert m.status == "Completed"

    requires_approval = list_missions(status="Requires Human Approval", db=db_session)
    assert len(requires_approval) >= 1
    assert any("FINOPS" in (m.agent_code or "") for m in requires_approval)


def test_get_mission_and_traces(db_session):
    """Verifies retrieving detailed mission execution, ReAct thoughts, and audit traces."""
    missions = list_missions(db=db_session)
    mission_id = missions[0].id

    detail = get_mission(mission_id, db=db_session)
    assert detail.id == mission_id
    assert detail.mission_code.startswith("MSN-")
    assert len(detail.output_summary) > 10

    traces = get_mission_traces(mission_id, db=db_session)
    assert len(traces) >= 2
    for tr in traces:
        assert tr.latency_ms > 0
        assert tr.guardrail_passed is True


def test_dispatch_autonomous_mission_sre(db_session):
    """Tests real-time mission dispatch to AGT-SRE-01 with ReAct execution and tool logging."""
    payload = MissionDispatchPayload(
        agent_code="AGT-SRE-01",
        title="Emergency CMDB Tier-0 Health & Runbook Scan",
        prompt_or_goal="Scan all primary infrastructure nodes and verify Tier-0 99.98% SLA",
        trigger_type="User Dispatched"
    )
    mission = dispatch_mission(payload, db=db_session)
    assert mission.status == "Completed"
    assert "SRE" in mission.output_summary or "CMDB" in mission.output_summary
    assert mission.agent_code == "AGT-SRE-01"
    assert mission.execution_duration_sec > 0

    # Verify traces were created
    traces = get_mission_traces(mission.id, db=db_session)
    assert len(traces) >= 3
    tool_trace = [t for t in traces if t.action_type in ["TOOL_CALL", "TOOL_EXECUTION"]]
    assert len(tool_trace) >= 1


def test_dispatch_finops_requires_human_approval(db_session):
    """Tests that high-risk FinOps missions pause at a Human-in-the-Loop approval gate."""
    payload = MissionDispatchPayload(
        agent_code="AGT-FINOPS-01",
        title="Commercial Tax Invoicing & TDS Lock for Retainer Client",
        prompt_or_goal="Calculate GST 18% and TDS Section 194J for Zenith Global",
        trigger_type="Incident Auto-Escalation"
    )
    mission = dispatch_mission(payload, db=db_session)
    assert mission.status == "Requires Human Approval"
    assert mission.human_approval_by is None
    assert "Awaiting Director Varadi Vijay" in mission.output_summary or "approval" in mission.output_summary.lower()


def test_approve_mission_human_in_the_loop(db_session):
    """Tests authorized signoff by Director Varadi Vijay for a suspended mission."""
    # Find or dispatch a mission requiring approval
    missions = list_missions(status="Requires Human Approval", db=db_session)
    target_mission = missions[0]

    approval_payload = MissionApprovalPayload(
        action="APPROVE",
        approver_name="Varadi Vijay (Director)",
        notes="Authorized and confirmed against corporate bank ledger."
    )
    approved = approve_mission_endpoint(target_mission.id, approval_payload, db=db_session)
    assert approved.status == "Completed"
    assert approved.human_approval_by == "Varadi Vijay (Director)"
    assert "Authorized and confirmed" in (approved.human_approval_notes or "")


def test_agent_interactive_chat_tool_grounded(db_session):
    """Verifies that interactive chat executes tools and grounds answers in production database state."""
    # SRE query
    sre_req = AgentChatRequest(
        agent_code="AGT-SRE-01",
        message="What is the health of our infrastructure nodes?"
    )
    sre_res = chat_agent(sre_req, db=db_session)
    assert sre_res.agent_code == "AGT-SRE-01"
    assert "cmdb" in " ".join(sre_res.tools_called).lower() or "telemetry" in sre_res.reply.lower() or "node" in sre_res.reply.lower()

    # Identity / Governance query
    comply_req = AgentChatRequest(
        agent_code="AGT-COMPLY-01",
        message="Who is the registered director and what is our CIN?"
    )
    comply_res = chat_agent(comply_req, db=db_session)
    assert "U85500KA2026OPC222069" in comply_res.reply
    assert "Varadi Vijay" in comply_res.reply
    assert "ASPERION DIGITAL TECHNOLOGIES" in comply_res.reply
