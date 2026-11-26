"""
Asperion Enterprise OS - Agentic AI & Autonomous Swarm Schemas (Pydantic V2)
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class EnterpriseAgentBase(BaseModel):
    agent_code: str
    name: str
    role: str
    department: str = "Engineering & Infrastructure"
    model_endpoint: str = "Gemini 2.5 Pro (1M Context)"
    system_prompt: str
    autonomy_tier: str = "Level 3: Supervised Autonomy"
    assigned_tools_json: str = "[]"
    is_active: bool = True
    health_status: str = "Optimal"
    total_missions_executed: int = 0
    success_rate_pct: float = 99.2
    avg_execution_latency_sec: float = 2.4

class EnterpriseAgentCreate(EnterpriseAgentBase):
    pass

class EnterpriseAgentOut(EnterpriseAgentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AgentExecutionTraceOut(BaseModel):
    id: int
    mission_id: int
    step_number: int
    action_type: str
    tool_name: Optional[str] = None
    tool_input_json: Optional[str] = None
    tool_output_json: Optional[str] = None
    latency_ms: float
    tokens_consumed: int
    guardrail_passed: bool
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class AgenticMissionBase(BaseModel):
    mission_code: str
    agent_id: int
    title: str
    trigger_type: str = "User Dispatched"
    input_parameters_json: str = "{}"
    status: str = "Completed"
    thought_chain_json: str = "[]"
    executed_tools_json: str = "[]"
    output_summary: str
    artifacts_generated_json: str = "[]"
    human_approval_by: Optional[str] = None
    human_approval_notes: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_duration_sec: float = 1.8

class AgenticMissionCreate(AgenticMissionBase):
    pass

class AgenticMissionOut(AgenticMissionBase):
    id: int
    agent_name: Optional[str] = None
    agent_code: Optional[str] = None
    traces: List[AgentExecutionTraceOut] = []
    model_config = ConfigDict(from_attributes=True)


class MissionDispatchPayload(BaseModel):
    agent_code: str
    title: str
    prompt_or_goal: str
    trigger_type: str = "User Dispatched"
    parameters: Optional[Dict[str, Any]] = None

class MissionApprovalPayload(BaseModel):
    action: str = Field(..., description="APPROVE or REJECT")
    approver_name: str
    notes: Optional[str] = ""

class AgentChatRequest(BaseModel):
    agent_code: str
    message: str
    context: Optional[Dict[str, Any]] = None

class AgentChatResponse(BaseModel):
    agent_code: str
    agent_name: str
    role: str
    reply: str
    tools_called: List[str] = []
    reasoning_summary: str
    timestamp: str
