"""
Asperion Enterprise OS - Agentic AI, Autonomous Multi-Agent Swarm & MCP Models
Defines enterprise agent personas, autonomous mission executions, thought chains,
human-in-the-loop approval gates, and granular execution trace auditing.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EnterpriseAgent(Base):
    """
    Autonomous Enterprise Agent Persona.
    Equipped with specific enterprise role, model endpoint, autonomy level, and MCP tools.
    """
    __tablename__ = "enterprise_agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_code = Column(String(50), unique=True, index=True) # e.g. AGT-SRE-01, AGT-COMPLY-01, AGT-FINOPS-01
    name = Column(String(100), nullable=False) # e.g. SRE & DevSecOps Sentinel
    role = Column(String(100), nullable=False) # Autonomous Systems Reliability Engineer
    department = Column(String(50), default="Engineering & Infrastructure") # Engineering, Finance, Legal, HR, PMO
    model_endpoint = Column(String(100), default="Gemini 2.5 Pro (1M Context)") # Gemini 2.5 Pro, Claude 3.7 Sonnet, DeepSeek-R1
    system_prompt = Column(Text, nullable=False)
    autonomy_tier = Column(String(50), default="Level 3: Supervised Autonomy") # Level 4: Fully Autonomous, Level 3: Supervised, Level 2: Human-in-Loop
    assigned_tools_json = Column(Text, default="[]") # JSON list of tool names / MCP capabilities
    is_active = Column(Boolean, default=True)
    health_status = Column(String(30), default="Optimal") # Optimal, Standby, Executing Mission, Throttled
    total_missions_executed = Column(Integer, default=0)
    success_rate_pct = Column(Float, default=99.2)
    avg_execution_latency_sec = Column(Float, default=2.4)
    created_at = Column(DateTime, default=datetime.utcnow)

    missions = relationship("AgenticMission", back_populates="agent", cascade="all, delete-orphan")


class AgenticMission(Base):
    """
    Autonomous Mission / Goal Execution Record.
    Tracks goal dispatch, step-by-step reasoning (Chain of Thought), tool calls,
    human approval gates, and generated operational artifacts.
    """
    __tablename__ = "agentic_missions"

    id = Column(Integer, primary_key=True, index=True)
    mission_code = Column(String(50), unique=True, index=True) # e.g. MSN-2026-0042
    agent_id = Column(Integer, ForeignKey("enterprise_agents.id"), nullable=False)
    title = Column(String(255), nullable=False)
    trigger_type = Column(String(50), default="User Dispatched") # User Dispatched, Scheduled Autonomous Cron, Event-Driven Webhook, Incident Auto-Escalation
    input_parameters_json = Column(Text, default="{}") # JSON input context / payload
    status = Column(String(50), default="Completed") # Queued, Executing, Completed, Requires Human Approval, Failed
    thought_chain_json = Column(Text, default="[]") # Step-by-step reasoning steps (Thought -> Tool -> Observation)
    executed_tools_json = Column(Text, default="[]") # Tools called during mission
    output_summary = Column(Text, nullable=False) # Plain text / markdown outcome summary
    artifacts_generated_json = Column(Text, default="[]") # Links, patch references, generated reports
    human_approval_by = Column(String(100), nullable=True) # Approver name if required
    human_approval_notes = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    execution_duration_sec = Column(Float, default=1.8)

    agent = relationship("EnterpriseAgent", back_populates="missions")
    traces = relationship("AgentExecutionTrace", back_populates="mission", cascade="all, delete-orphan")

    @property
    def agent_name(self):
        return self.agent.name if self.agent else None

    @property
    def agent_code(self):
        return self.agent.agent_code if self.agent else None


class AgentExecutionTrace(Base):
    """
    Granular Execution Trace for SOC2 & ISO 27001 AI Governance Auditing.
    Logs every tool invocation, latency, prompt tokens, completion tokens, and guardrail checks.
    """
    __tablename__ = "agent_execution_traces"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("agentic_missions.id"), nullable=False)
    step_number = Column(Integer, default=1)
    action_type = Column(String(50), default="TOOL_CALL") # REASONING, TOOL_CALL, POLICY_GUARDRAIL_CHECK, REFLECTION
    tool_name = Column(String(100), nullable=True)
    tool_input_json = Column(Text, nullable=True)
    tool_output_json = Column(Text, nullable=True)
    latency_ms = Column(Float, default=120.0)
    tokens_consumed = Column(Integer, default=450)
    guardrail_passed = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    mission = relationship("AgenticMission", back_populates="traces")
