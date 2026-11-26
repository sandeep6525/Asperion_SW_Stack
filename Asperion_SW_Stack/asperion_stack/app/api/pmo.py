"""
Asperion Enterprise OS - Comprehensive PMO & Delivery Operations API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from app.database import get_db
from app.models.pmo import (
    Project, ProjectMilestone, WBSTask, RACIAssignment, RAIDItem, ChangeRequest, Sprint, Stakeholder,
    ProjectIntake, ProjectCharter, ActionDecisionItem, CapacityPlanItem, QualityUATItem, ProjectClosureItem
)
from app.schemas.pmo import (
    ProjectCreate, ProjectOut, RAIDItemCreate, RAIDItemOut,
    ProjectIntakeCreate, ProjectIntakeOut,
    ProjectCharterCreate, ProjectCharterOut,
    ActionDecisionCreate, ActionDecisionOut,
    CapacityPlanCreate, CapacityPlanOut,
    QualityUATCreate, QualityUATOut,
    ProjectClosureCreate, ProjectClosureOut
)

router = APIRouter(prefix="/pmo", tags=["PMO & Delivery Operations"])

class TaskStatusUpdate(BaseModel):
    status: str # To Do, In Progress, Review, Done

class WBSTaskCreate(BaseModel):
    project_id: int
    wbs_code: str
    task_name: str
    owner: Optional[str] = "Developer"
    assigned_to: Optional[str] = None
    status: str = "To Do"
    planned_hours: Optional[float] = 16.0
    estimated_hours: Optional[float] = None
    actual_hours: float = 0.0
    sprint_phase: Optional[str] = "Sprint 1"
    sprint_id: Optional[int] = None

class SprintCreate(BaseModel):
    project_id: int
    sprint_name: str
    start_date: date
    end_date: date
    goal: Optional[str] = None
    committed_story_points: int = 40

class StakeholderCreate(BaseModel):
    project_id: int
    name: str
    organization: str = "Client"
    role_in_project: str
    influence_level: str = "High"
    interest_level: str = "High"
    communication_frequency: str = "Weekly Meeting"

@router.get("/projects", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.post("/projects", response_model=ProjectOut)
def create_project(proj_in: ProjectCreate, db: Session = Depends(get_db)):
    proj = Project(**proj_in.model_dump())
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.get("/tasks")
def list_wbs_tasks(db: Session = Depends(get_db)):
    return db.query(WBSTask).all()

@router.post("/tasks")
def create_wbs_task(task_in: WBSTaskCreate, db: Session = Depends(get_db)):
    data = task_in.model_dump()
    assigned = data.get("assigned_to") or data.get("owner") or "Developer"
    est_hours = data.get("estimated_hours") or data.get("planned_hours") or 8.0
    task = WBSTask(
        project_id=data["project_id"],
        wbs_code=data["wbs_code"],
        task_name=data["task_name"],
        assigned_to=assigned,
        sprint_phase=data.get("sprint_phase", "Sprint 1"),
        estimated_hours=float(est_hours),
        actual_hours=float(data.get("actual_hours", 0.0)),
        status=data.get("status", "To Do"),
        priority=data.get("priority", "Medium")
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = db.query(WBSTask).filter(WBSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status_update.status
    db.commit()
    db.refresh(task)
    return task

@router.get("/sprints")
def list_sprints(db: Session = Depends(get_db)):
    return db.query(Sprint).all()

@router.post("/sprints")
def create_sprint(sprint_in: SprintCreate, db: Session = Depends(get_db)):
    sprint = Sprint(**sprint_in.model_dump())
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint

@router.get("/milestones")
def list_milestones(db: Session = Depends(get_db)):
    return db.query(ProjectMilestone).all()

@router.get("/raid-items", response_model=List[RAIDItemOut])
def list_raid_items(db: Session = Depends(get_db)):
    return db.query(RAIDItem).order_by(RAIDItem.created_at.desc()).all()

@router.post("/raid-items", response_model=RAIDItemOut)
def create_raid_item(raid_in: RAIDItemCreate, db: Session = Depends(get_db)):
    raid = RAIDItem(**raid_in.model_dump())
    db.add(raid)
    db.commit()
    db.refresh(raid)
    return raid

@router.get("/change-requests")
def list_change_requests(db: Session = Depends(get_db)):
    return db.query(ChangeRequest).all()

@router.get("/raci")
def list_raci_assignments(db: Session = Depends(get_db)):
    return db.query(RACIAssignment).all()

@router.get("/stakeholders")
def list_stakeholders(db: Session = Depends(get_db)):
    return db.query(Stakeholder).all()

# ==============================================================================
# GLOBALLY ACKNOWLEDGED PMO PROCESSES (PMBOK / PRINCE2 / CMMI / ISO 21500)
# ==============================================================================

# 1. Stage-Gate 1: Project Intake & Strategic Business Case
@router.get("/intakes", response_model=List[ProjectIntakeOut])
def list_project_intakes(db: Session = Depends(get_db)):
    return db.query(ProjectIntake).order_by(ProjectIntake.created_at.desc()).all()

@router.post("/intakes", response_model=ProjectIntakeOut)
def create_project_intake(intake_in: ProjectIntakeCreate, db: Session = Depends(get_db)):
    intake = ProjectIntake(**intake_in.model_dump())
    db.add(intake)
    db.commit()
    db.refresh(intake)
    return intake

# 2. Stage-Gate 2: Charter Baseline & Scope Lock
@router.get("/charters", response_model=List[ProjectCharterOut])
def list_project_charters(db: Session = Depends(get_db)):
    return db.query(ProjectCharter).all()

@router.post("/charters", response_model=ProjectCharterOut)
def create_project_charter(charter_in: ProjectCharterCreate, db: Session = Depends(get_db)):
    charter = ProjectCharter(**charter_in.model_dump())
    db.add(charter)
    db.commit()
    db.refresh(charter)
    return charter

# 3. Action Items & Decision Log (SteerCo Cadence)
@router.get("/actions-decisions", response_model=List[ActionDecisionOut])
def list_actions_and_decisions(db: Session = Depends(get_db)):
    return db.query(ActionDecisionItem).order_by(ActionDecisionItem.created_at.desc()).all()

@router.post("/actions-decisions", response_model=ActionDecisionOut)
def create_action_decision_item(ad_in: ActionDecisionCreate, db: Session = Depends(get_db)):
    item = ActionDecisionItem(**ad_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 4. Resource Capacity & Skills Allocation Plan
@router.get("/capacity-plan", response_model=List[CapacityPlanOut])
def list_capacity_plan_items(db: Session = Depends(get_db)):
    return db.query(CapacityPlanItem).all()

@router.post("/capacity-plan", response_model=CapacityPlanOut)
def create_capacity_plan_item(cap_in: CapacityPlanCreate, db: Session = Depends(get_db)):
    data = cap_in.model_dump()
    req = float(data.get("required_hours", 80.0))
    avail = float(data.get("available_hours", 80.0))
    util = round((req / avail * 100.0), 1) if avail > 0 else 100.0
    var = round(avail - req, 1)
    status = "Balanced"
    if util > 105.0:
        status = "Constrained / Overallocated"
    elif util < 90.0:
        status = "Surplus Capacity"

    item = CapacityPlanItem(
        project_id=data["project_id"],
        role_title=data["role_title"],
        person_or_vendor=data["person_or_vendor"],
        skill_area=data["skill_area"],
        required_hours=req,
        available_hours=avail,
        utilization_pct=util,
        variance_hours=var,
        status=status
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 5. Quality Assurance & User Acceptance Testing (UAT)
@router.get("/quality-uat", response_model=List[QualityUATOut])
def list_quality_uat_items(db: Session = Depends(get_db)):
    return db.query(QualityUATItem).all()

@router.post("/quality-uat", response_model=QualityUATOut)
def create_quality_uat_item(uat_in: QualityUATCreate, db: Session = Depends(get_db)):
    item = QualityUATItem(**uat_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 6. Stage-Gate 5: Project Closure, Lessons Learned & Handover
@router.get("/closures", response_model=List[ProjectClosureOut])
def list_project_closures(db: Session = Depends(get_db)):
    return db.query(ProjectClosureItem).all()

@router.post("/closures", response_model=ProjectClosureOut)
def create_project_closure(close_in: ProjectClosureCreate, db: Session = Depends(get_db)):
    item = ProjectClosureItem(**close_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 7. Comprehensive PMO Stage-Gate Health & Executive Overview
@router.get("/governance-overview")
def get_pmo_governance_overview(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    intakes = db.query(ProjectIntake).all()
    charters = db.query(ProjectCharter).all()
    actions = db.query(ActionDecisionItem).all()
    capacity = db.query(CapacityPlanItem).all()
    uats = db.query(QualityUATItem).all()
    closures = db.query(ProjectClosureItem).all()
    raids = db.query(RAIDItem).all()
    crs = db.query(ChangeRequest).all()

    active_risks = sum(1 for r in raids if r.item_type == "Risk" and r.status == "Open")
    active_issues = sum(1 for r in raids if r.item_type == "Issue" and r.status == "Open")
    overallocated_resources = sum(1 for c in capacity if "Constrained" in c.status)
    passed_uats = sum(1 for u in uats if "Passed" in u.status)

    return {
        "status": "success",
        "stage_gates": {
            "gate_1_intakes": len(intakes),
            "gate_2_charters_baselined": len(charters),
            "gate_3_active_projects": len(projects),
            "gate_4_uat_deliverables": len(uats),
            "gate_5_closures_completed": len(closures)
        },
        "governance_metrics": {
            "total_open_actions": sum(1 for a in actions if a.item_type == "Action" and a.status == "Open"),
            "steerco_decisions_logged": sum(1 for a in actions if a.item_type == "Decision"),
            "open_risks": active_risks,
            "open_issues": active_issues,
            "resource_bottlenecks": overallocated_resources,
            "uat_pass_rate_pct": round((passed_uats / len(uats) * 100.0), 1) if uats else 100.0,
            "change_requests_logged": len(crs)
        }
    }

