"""
Asperion Enterprise OS - Strategy, Functions, KPIs & Decision Pydantic Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

# Strategic Function
class StrategicFunctionBase(BaseModel):
    function_name: str
    function_owner: str
    core_capabilities: str
    key_documents: Optional[str] = None
    core_registers: Optional[str] = None
    review_cadence: str = "Monthly"
    maturity_level: str = "L1"
    status: str = "Active"

class StrategicFunctionCreate(StrategicFunctionBase):
    pass

class StrategicFunctionOut(StrategicFunctionBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Capability Capacity
class CapabilityCapacityBase(BaseModel):
    capability_name: str
    current_capacity: str
    target_capacity: str
    primary_constraint: str
    people_requirement: Optional[str] = None
    tool_system_requirement: Optional[str] = None
    process_requirement: Optional[str] = None
    priority: str = "High"
    status: str = "Planned"

class CapabilityCapacityCreate(CapabilityCapacityBase):
    pass

class CapabilityCapacityOut(CapabilityCapacityBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Enterprise KPI
class EnterpriseKPIBase(BaseModel):
    kpi_code: str
    category: str
    name: str
    target_value: float
    actual_value: float = 0.0
    unit: str = "INR"
    period: str = "JUN-2026"
    status: str = "On Track"
    owner: str = "Director / Founder"
    notes: Optional[str] = None

class EnterpriseKPICreate(EnterpriseKPIBase):
    pass

class EnterpriseKPIUpdate(BaseModel):
    actual_value: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class EnterpriseKPIOut(EnterpriseKPIBase):
    id: int
    variance: float
    variance_pct: float
    created_at: datetime
    class Config:
        from_attributes = True

# Strategic Decision / Thought
class StrategicDecisionThoughtBase(BaseModel):
    entry_type: str = "Strategic Decision"
    title: str
    author: str = "Varadi Vijay (Sole Director)"
    date_recorded: Optional[date] = None
    context_background: str
    options_considered: Optional[str] = None
    decision_rationale: str
    approver: str = "Varadi Vijay (Sole Member)"
    evidence_or_artifact_link: Optional[str] = None
    status: str = "Approved"
    tags: str = "Governance, Strategy, AI"

class StrategicDecisionThoughtCreate(StrategicDecisionThoughtBase):
    pass

class StrategicDecisionThoughtOut(StrategicDecisionThoughtBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Roadmap
class ImplementationRoadmapItemBase(BaseModel):
    workstream: str
    action_item: str
    priority: str = "High"
    owner: str = "Function Lead"
    start_date: date
    due_date: date
    progress_pct: int = 0
    status: str = "In Progress"
    notes: Optional[str] = None

class ImplementationRoadmapItemCreate(ImplementationRoadmapItemBase):
    pass

class ImplementationRoadmapItemOut(ImplementationRoadmapItemBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
