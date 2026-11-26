"""
Asperion Enterprise OS - Strategy, Functions, Dynamic KPIs & Decision Models
Digitizes Function Map, Capacity Constraints, Executive Decision Logs, and KPI Matrix
from Asperion Digital Operating System Workbook and Strategic Founder Packs.
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StrategicFunction(Base):
    __tablename__ = "strategic_functions"
    
    id = Column(Integer, primary_key=True, index=True)
    function_name = Column(String(100), nullable=False, unique=True)
    function_owner = Column(String(100), nullable=False)
    core_capabilities = Column(Text, nullable=False)
    key_documents = Column(String(255), nullable=True)
    core_registers = Column(String(255), nullable=True)
    review_cadence = Column(String(50), default="Monthly") # Weekly, Fortnightly, Monthly, Quarterly
    maturity_level = Column(String(10), default="L1") # L0-Ad-hoc, L1-Initial, L2-Managed, L3-Defined, L4-Optimized
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

class CapabilityCapacity(Base):
    __tablename__ = "capability_capacity"
    
    id = Column(Integer, primary_key=True, index=True)
    capability_name = Column(String(150), nullable=False)
    current_capacity = Column(String(255), nullable=False)
    target_capacity = Column(String(255), nullable=False)
    primary_constraint = Column(String(255), nullable=False)
    people_requirement = Column(String(255), nullable=True)
    tool_system_requirement = Column(String(255), nullable=True)
    process_requirement = Column(String(255), nullable=True)
    priority = Column(String(20), default="High") # Critical, High, Medium
    status = Column(String(50), default="Planned") # Planned, In Progress, Realized
    created_at = Column(DateTime, default=datetime.utcnow)

class EnterpriseKPI(Base):
    __tablename__ = "enterprise_kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    kpi_code = Column(String(50), unique=True, index=True) # KPI-FIN-01, KPI-ENG-02
    category = Column(String(50), nullable=False) # Financial, Customer, Operational, People, Security, Governance
    name = Column(String(150), nullable=False)
    target_value = Column(Float, nullable=False)
    actual_value = Column(Float, default=0.0)
    unit = Column(String(30), default="INR") # INR, %, Hours, Count, Days, Score/100
    period = Column(String(30), default="JUN-2026") # Month or Quarter
    variance = Column(Float, default=0.0)
    variance_pct = Column(Float, default=0.0)
    status = Column(String(30), default="On Track") # On Track, At Risk, Critical, Achieved
    owner = Column(String(100), default="Director / Founder")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StrategicDecisionThought(Base):
    __tablename__ = "strategic_decisions_thoughts"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_type = Column(String(50), default="Strategic Decision") # Strategic Decision, Founder Thought / Thesis, Architecture Note, Market Vision
    title = Column(String(255), nullable=False)
    author = Column(String(100), default="Varadi Vijay (Sole Director)")
    date_recorded = Column(Date, default=date.today)
    context_background = Column(Text, nullable=False)
    options_considered = Column(Text, nullable=True)
    decision_rationale = Column(Text, nullable=False)
    approver = Column(String(100), default="Varadi Vijay (Sole Member)")
    evidence_or_artifact_link = Column(String(255), nullable=True)
    status = Column(String(50), default="Approved") # Draft, Approved, Executing, Closed
    tags = Column(String(255), default="Governance, Strategy, AI")
    created_at = Column(DateTime, default=datetime.utcnow)

class ImplementationRoadmapItem(Base):
    __tablename__ = "implementation_roadmap"
    
    id = Column(Integer, primary_key=True, index=True)
    workstream = Column(String(100), nullable=False) # Governance, Technology, Commercial, Finance, People
    action_item = Column(String(255), nullable=False)
    priority = Column(String(20), default="High") # Critical, High, Medium
    owner = Column(String(100), default="Function Lead")
    start_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    progress_pct = Column(Integer, default=0)
    status = Column(String(50), default="In Progress") # Not Started, In Progress, Blocked, Complete
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
