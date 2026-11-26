"""
Asperion Enterprise OS - PMO Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    project_code: str
    name: str
    client_name: str = "Internal R&D"
    project_type: str = "Client Delivery"
    sponsor: str = "Varadi Vijay"
    project_manager: str = "PMO Lead"
    technical_lead: Optional[str] = None
    start_date: date
    target_end_date: date
    priority: str = "High"
    budget_inr: float = 0.0
    estimated_effort_days: float = 0.0

class ProjectOut(ProjectCreate):
    id: int
    status: str
    actual_spent_inr: float
    actual_effort_days: float
    created_at: datetime
    class Config:
        from_attributes = True

class RAIDItemCreate(BaseModel):
    project_id: int
    item_type: str # Risk, Assumption, Issue, Dependency
    title: str
    description: Optional[str] = None
    severity_impact: str = "Medium"
    probability: str = "Medium"
    mitigation_plan: Optional[str] = None
    owner: str = "Project Manager"

class RAIDItemOut(RAIDItemCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# Stage-Gate 1: Project Intake
class ProjectIntakeCreate(BaseModel):
    intake_code: str
    project_name: str
    sponsor: str = "Varadi Vijay (Director)"
    client_or_internal: str = "Enterprise Client"
    strategic_fit: str = "High"
    expected_value: str = "Revenue expansion & client retention"
    estimated_budget_inr: float = 0.0

class ProjectIntakeOut(ProjectIntakeCreate):
    id: int
    intake_status: str
    target_start_date: Optional[date]
    approval_date: Optional[date]
    approved_by: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# Stage-Gate 2: Charter Baseline
class ProjectCharterCreate(BaseModel):
    project_id: int
    charter_code: str
    problem_statement: str
    business_case: Optional[str] = None
    measurable_success_criteria: str
    scope_included: str
    scope_excluded: str
    assumptions_summary: Optional[str] = None
    constraints_summary: Optional[str] = None
    governance_cadence: str = "Weekly SteerCo, Daily Standups"

class ProjectCharterOut(ProjectCharterCreate):
    id: int
    signoff_status: str
    signed_off_by: str
    signoff_date: Optional[date]
    created_at: datetime
    class Config:
        from_attributes = True

# Action & Decision
class ActionDecisionCreate(BaseModel):
    project_id: int
    item_type: str = "Action" # Action, Decision
    source_meeting: str = "Weekly SteerCo"
    title_or_decision: str
    rationale_or_context: Optional[str] = None
    owner: str = "PMO Lead"
    due_date: Optional[date] = None

class ActionDecisionOut(ActionDecisionCreate):
    id: int
    status: str
    recorded_date: Optional[date]
    created_at: datetime
    class Config:
        from_attributes = True

# Capacity Plan
class CapacityPlanCreate(BaseModel):
    project_id: int
    role_title: str
    person_or_vendor: str
    skill_area: str = "Architecture & Full-Stack"
    required_hours: float = 80.0
    available_hours: float = 80.0

class CapacityPlanOut(CapacityPlanCreate):
    id: int
    utilization_pct: float
    variance_hours: float
    status: str
    class Config:
        from_attributes = True

# Quality UAT
class QualityUATCreate(BaseModel):
    project_id: int
    deliverable_name: str
    test_or_review_type: str = "Client UAT"
    acceptance_criteria: str
    test_lead: str = "Lead QA"
    client_reviewer: str = "Client SPOC"

class QualityUATOut(QualityUATCreate):
    id: int
    status: str
    signoff_date: Optional[date]
    evidence_notes: Optional[str]
    class Config:
        from_attributes = True

# Project Closure & Lessons Learned
class ProjectClosureCreate(BaseModel):
    project_id: int
    closure_area: str
    description: str
    evidence_signoff: str = "Client Acceptance Certificate"
    owner: str = "PMO Lead"
    lessons_learned_summary: Optional[str] = None

class ProjectClosureOut(ProjectClosureCreate):
    id: int
    closure_status: str
    completed_date: Optional[date]
    class Config:
        from_attributes = True

