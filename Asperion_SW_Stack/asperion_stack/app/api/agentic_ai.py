"""
Asperion Enterprise OS - Agentic AI & Autonomous Multi-Agent Swarm API Router
Exposes enterprise agent roster, autonomous mission dispatch (ReAct loop),
human-in-the-loop approval, verifiable tool-grounded chat, and swarm telemetry.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.agentic_ai import EnterpriseAgent, AgenticMission, AgentExecutionTrace
from app.schemas.agentic_ai import (
    EnterpriseAgentCreate, EnterpriseAgentOut,
    AgenticMissionCreate, AgenticMissionOut,
    AgentExecutionTraceOut,
    MissionDispatchPayload, MissionApprovalPayload,
    AgentChatRequest, AgentChatResponse
)
from app.engines.agentic_ai_engine import (
    dispatch_autonomous_mission,
    approve_mission,
    chat_with_agent,
    get_agentic_mesh_overview
)

router = APIRouter(prefix="/agentic-ai", tags=["Agentic AI & Autonomous Swarm Suite"])

# -------------------------------------------------------------
# 1. Swarm Mesh Overview & Telemetry
# -------------------------------------------------------------
@router.get("/overview")
def get_swarm_overview(db: Session = Depends(get_db)):
    """
    Returns enterprise agent swarm health, mission velocity,
    autonomy tier breakdown, tool utilization, and active missions.
    """
    return get_agentic_mesh_overview(db)


# -------------------------------------------------------------
# 2. Agent Roster Management
# -------------------------------------------------------------
@router.get("/agents", response_model=List[EnterpriseAgentOut])
def list_agents(
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieves all registered enterprise autonomous agents.
    """
    query = db.query(EnterpriseAgent)
    if department:
        query = query.filter(EnterpriseAgent.department == department)
    if is_active is not None:
        query = query.filter(EnterpriseAgent.is_active == is_active)
    return query.order_by(EnterpriseAgent.id.asc()).all()


@router.post("/agents", response_model=EnterpriseAgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(payload: EnterpriseAgentCreate, db: Session = Depends(get_db)):
    """
    Registers a new specialized autonomous agent in the swarm registry.
    """
    existing = db.query(EnterpriseAgent).filter(EnterpriseAgent.agent_code == payload.agent_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Agent with code '{payload.agent_code}' already exists.")
    
    agent = EnterpriseAgent(**payload.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("/agents/{agent_code}", response_model=EnterpriseAgentOut)
def get_agent(agent_code: str, db: Session = Depends(get_db)):
    """
    Retrieves detailed persona and telemetry for a specific agent.
    """
    agent = db.query(EnterpriseAgent).filter(EnterpriseAgent.agent_code == agent_code).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_code}' not found.")
    return agent


# -------------------------------------------------------------
# 3. Autonomous Mission Dispatch & Console
# -------------------------------------------------------------
@router.get("/missions", response_model=List[AgenticMissionOut])
def list_missions(
    status: Optional[str] = None,
    agent_code: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lists autonomous missions with execution traces and reasoning steps.
    """
    actual_limit = 50
    if isinstance(limit, int):
        actual_limit = limit
    elif hasattr(limit, "default") and isinstance(getattr(limit, "default"), int):
        actual_limit = getattr(limit, "default")

    query = db.query(AgenticMission)
    if status:
        query = query.filter(AgenticMission.status == status)
    if agent_code:
        query = query.join(EnterpriseAgent).filter(EnterpriseAgent.agent_code == agent_code)
    
    return query.order_by(AgenticMission.id.desc()).limit(actual_limit).all()


@router.get("/missions/{mission_id}", response_model=AgenticMissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    """
    Retrieves full execution details, step-by-step thoughts, and traces for a mission.
    """
    mission = db.query(AgenticMission).filter(AgenticMission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission ID {mission_id} not found.")
    return mission


@router.post("/missions/dispatch", response_model=AgenticMissionOut)
def dispatch_mission(payload: MissionDispatchPayload, db: Session = Depends(get_db)):
    """
    Dispatches a real-time goal to an autonomous agent.
    Executes multi-step ReAct reasoning, tool invocations, and guardrails.
    """
    try:
        mission = dispatch_autonomous_mission(db, payload)
        return mission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Autonomous mission dispatch failed: {str(e)}")


@router.post("/missions/{mission_id}/approve", response_model=AgenticMissionOut)
def approve_mission_endpoint(mission_id: int, payload: MissionApprovalPayload, db: Session = Depends(get_db)):
    """
    Human-in-the-loop signoff for Level 2 supervised missions requiring manual authorization.
    """
    try:
        mission = approve_mission(db, mission_id, payload)
        return mission
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Mission approval failed: {str(e)}")


# -------------------------------------------------------------
# 4. Interactive Tool-Grounded Agent Chat
# -------------------------------------------------------------
@router.post("/chat", response_model=AgentChatResponse)
def chat_agent(request: AgentChatRequest, db: Session = Depends(get_db)):
    """
    Direct interactive conversation with an enterprise agent persona.
    Grounds answers in real database records with tool execution synthesis.
    """
    try:
        response = chat_with_agent(db, request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent chat execution failed: {str(e)}")


# -------------------------------------------------------------
# 5. Granular Execution Traces (Auditing)
# -------------------------------------------------------------
@router.get("/traces/{mission_id}", response_model=List[AgentExecutionTraceOut])
def get_mission_traces(mission_id: int, db: Session = Depends(get_db)):
    """
    Retrieves granular SOC2 / ISO 27001 execution audit traces for a specific mission.
    """
    traces = db.query(AgentExecutionTrace).filter(
        AgentExecutionTrace.mission_id == mission_id
    ).order_by(AgentExecutionTrace.step_number.asc()).all()
    return traces
