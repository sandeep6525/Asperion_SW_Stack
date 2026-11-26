"""
Asperion Enterprise OS - PMO & Delivery Operations Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, index=True) # ADT-PRJ-2026-001
    name = Column(String(255), nullable=False)
    client_name = Column(String(255), default="Internal R&D")
    project_type = Column(String(50), default="Client Delivery") # Client Delivery, Internal R&D, Platform Product, Maintenance
    sponsor = Column(String(100), default="Varadi Vijay")
    project_manager = Column(String(100), default="PMO Lead")
    technical_lead = Column(String(100))
    start_date = Column(Date, nullable=False)
    target_end_date = Column(Date, nullable=False)
    status = Column(String(50), default="In Progress") # Pipeline, Planning, In Progress, UAT, Closed, On Hold
    priority = Column(String(20), default="High") # Low, Medium, High, Critical
    budget_inr = Column(Float, default=0.0)
    actual_spent_inr = Column(Float, default=0.0)
    estimated_effort_days = Column(Float, default=0.0)
    actual_effort_days = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    milestones = relationship("ProjectMilestone", back_populates="project")
    tasks = relationship("WBSTask", back_populates="project")
    raid_items = relationship("RAIDItem", back_populates="project")
    change_requests = relationship("ChangeRequest", back_populates="project")

class ProjectMilestone(Base):
    __tablename__ = "project_milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    milestone_name = Column(String(255), nullable=False)
    target_date = Column(Date, nullable=False)
    deliverable_summary = Column(Text, nullable=True)
    payment_linked_percent = Column(Float, default=0.0)
    billing_amount = Column(Float, default=0.0)
    status = Column(String(50), default="Pending") # Pending, In Review, Client Approved, Billed
    completion_date = Column(Date, nullable=True)
    signoff_by = Column(String(100), nullable=True)
    signoff_at = Column(DateTime, nullable=True)
    signoff_notes = Column(Text, nullable=True)
    acceptance_criteria = Column(Text, nullable=True)
    
    project = relationship("Project", back_populates="milestones")

class WBSTask(Base):
    __tablename__ = "wbs_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    wbs_code = Column(String(50)) # e.g. 1.1, 1.2, 2.1.3
    task_name = Column(String(255), nullable=False)
    assigned_to = Column(String(100))
    sprint_phase = Column(String(50), default="Sprint 1")
    estimated_hours = Column(Float, default=8.0)
    actual_hours = Column(Float, default=0.0)
    status = Column(String(50), default="To Do") # To Do, In Progress, Review, Done, Blocked
    priority = Column(String(20), default="Medium")
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    
    project = relationship("Project", back_populates="tasks")

class RACIAssignment(Base):
    __tablename__ = "raci_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String(255), nullable=False)
    project_code = Column(String(50), nullable=True)
    responsible_role = Column(String(100), nullable=False) # R
    accountable_role = Column(String(100), nullable=False) # A
    consulted_roles = Column(String(255))                  # C
    informed_roles = Column(String(255))                   # I

class RAIDItem(Base):
    __tablename__ = "raid_items"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    item_type = Column(String(20), nullable=False) # Risk, Assumption, Issue, Dependency
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity_impact = Column(String(50), default="Medium") # Low, Medium, High, Critical
    probability = Column(String(50), default="Medium")     # Low, Medium, High
    mitigation_plan = Column(Text, nullable=True)
    owner = Column(String(100), default="Project Manager")
    status = Column(String(50), default="Open") # Open, Mitigated, Closed, Escalated
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="raid_items")

class ChangeRequest(Base):
    __tablename__ = "change_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    cr_number = Column(String(50), unique=True, index=True) # ADT-CR-001
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    scope_impact = Column(Text, nullable=True)
    cost_impact_inr = Column(Float, default=0.0)
    schedule_impact_days = Column(Integer, default=0)
    status = Column(String(50), default="Submitted") # Submitted, Under Evaluation, Approved, Rejected, Implemented
    approver = Column(String(100), default="Sponsor / Client Authority")
    decision_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="change_requests")

class Sprint(Base):
    __tablename__ = "sprints"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    sprint_name = Column(String(100), nullable=False) # Sprint 1, Sprint 2
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    goal = Column(Text, nullable=True)
    committed_story_points = Column(Integer, default=40)
    completed_story_points = Column(Integer, default=0)
    velocity = Column(Float, default=0.0)
    status = Column(String(50), default="Active") # Planning, Active, Completed, Closed

class Stakeholder(Base):
    __tablename__ = "stakeholders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(100), nullable=False)
    organization = Column(String(100), default="Client")
    role_in_project = Column(String(100), nullable=False)
    influence_level = Column(String(20), default="High") # High, Medium, Low
    interest_level = Column(String(20), default="High")  # High, Medium, Low
    communication_frequency = Column(String(50), default="Weekly Status Meeting")
    engagement_strategy = Column(Text, nullable=True)

class ProjectIntake(Base):
    """Stage-Gate 1: Project Intake, Business Case & Strategic Fit"""
    __tablename__ = "project_intakes"

    id = Column(Integer, primary_key=True, index=True)
    intake_code = Column(String(50), unique=True, index=True) # ADT-INTK-2026-001
    project_name = Column(String(255), nullable=False)
    sponsor = Column(String(100), default="Varadi Vijay (Director)")
    client_or_internal = Column(String(100), default="Enterprise Client")
    strategic_fit = Column(String(50), default="High") # Critical, High, Medium, Low
    expected_value = Column(String(255), default="Revenue expansion & client retention")
    target_start_date = Column(Date, nullable=True)
    estimated_budget_inr = Column(Float, default=0.0)
    intake_status = Column(String(50), default="Under Evaluation") # Submitted, Under Evaluation, Approved to Charter, Deferred, Rejected
    approval_date = Column(Date, nullable=True)
    approved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProjectCharter(Base):
    """Stage-Gate 2: Project Charter Baseline & Authorization"""
    __tablename__ = "project_charters"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True)
    charter_code = Column(String(50), unique=True, index=True) # ADT-CHTR-2026-001
    problem_statement = Column(Text, nullable=False)
    business_case = Column(Text, nullable=True)
    measurable_success_criteria = Column(Text, nullable=False)
    scope_included = Column(Text, nullable=False)
    scope_excluded = Column(Text, nullable=False)
    assumptions_summary = Column(Text, nullable=True)
    constraints_summary = Column(Text, nullable=True)
    governance_cadence = Column(String(100), default="Weekly SteerCo, Daily Standups")
    signoff_status = Column(String(50), default="Approved & Baselined") # Draft, In Review, Approved & Baselined
    signed_off_by = Column(String(100), default="Varadi Vijay (Sole Director)")
    signoff_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ActionDecisionItem(Base):
    """Action Item & Decision Log (SteerCo & Project Cadence)"""
    __tablename__ = "action_decision_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    item_type = Column(String(20), default="Action") # Action, Decision
    source_meeting = Column(String(100), default="Weekly SteerCo")
    title_or_decision = Column(String(255), nullable=False)
    rationale_or_context = Column(Text, nullable=True)
    owner = Column(String(100), default="PMO Lead")
    due_date = Column(Date, nullable=True)
    status = Column(String(50), default="Open") # Open, In Progress, Closed, Implemented
    recorded_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CapacityPlanItem(Base):
    """Resource Capacity & Skills Allocation Planning"""
    __tablename__ = "capacity_plan_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    role_title = Column(String(100), nullable=False) # Project Manager, Tech Lead, Full-Stack Dev, QA
    person_or_vendor = Column(String(100), nullable=False) # Arjun Sharma, Nexus Team
    skill_area = Column(String(100), default="Architecture & Full-Stack")
    required_hours = Column(Float, default=80.0)
    available_hours = Column(Float, default=80.0)
    utilization_pct = Column(Float, default=100.0)
    variance_hours = Column(Float, default=0.0) # available - required
    status = Column(String(50), default="Balanced") # Balanced, Constrained / Overallocated, Surplus

class QualityUATItem(Base):
    """Quality Assurance & User Acceptance Testing (UAT) Sign-Offs"""
    __tablename__ = "quality_uat_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    deliverable_name = Column(String(255), nullable=False)
    test_or_review_type = Column(String(100), default="Client UAT") # Internal QA, Automated Integration, Security Scan, Client UAT
    acceptance_criteria = Column(Text, nullable=False)
    test_lead = Column(String(100), default="Lead QA")
    client_reviewer = Column(String(100), default="Client SPOC")
    status = Column(String(50), default="Passed & Signed-Off") # Pending, In Testing, Defects Blocked, Passed & Signed-Off
    signoff_date = Column(Date, nullable=True)
    evidence_notes = Column(Text, nullable=True)

class ProjectClosureItem(Base):
    """Stage-Gate 5: Formal Project Closure, Lessons Learned & Handover"""
    __tablename__ = "project_closure_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    closure_area = Column(String(100), nullable=False) # Deliverables Accepted, Financial Billing Settled, Support Handover, Lessons Learned
    description = Column(String(255), nullable=False)
    evidence_signoff = Column(String(255), default="Client Acceptance Certificate")
    owner = Column(String(100), default="PMO Lead")
    closure_status = Column(String(50), default="Completed") # Pending, In Progress, Completed
    lessons_learned_summary = Column(Text, nullable=True)
    completed_date = Column(Date, nullable=True)


