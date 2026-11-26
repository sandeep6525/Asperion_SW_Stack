"""
Asperion Enterprise OS - Strategy, Functions, KPIs & Executive Thought Engine API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.strategy_kpi import (
    StrategicFunction, CapabilityCapacity, EnterpriseKPI, StrategicDecisionThought, ImplementationRoadmapItem
)
from app.schemas.strategy_kpi import (
    StrategicFunctionCreate, StrategicFunctionOut,
    CapabilityCapacityCreate, CapabilityCapacityOut,
    EnterpriseKPICreate, EnterpriseKPIUpdate, EnterpriseKPIOut,
    StrategicDecisionThoughtCreate, StrategicDecisionThoughtOut,
    ImplementationRoadmapItemCreate, ImplementationRoadmapItemOut
)

router = APIRouter(prefix="/strategy", tags=["Strategy, Functions, KPIs & Executive Thoughts"])

# 1. Functions
@router.get("/functions", response_model=List[StrategicFunctionOut])
def list_functions(db: Session = Depends(get_db)):
    return db.query(StrategicFunction).order_by(StrategicFunction.id.asc()).all()

@router.post("/functions", response_model=StrategicFunctionOut)
def create_function(item_in: StrategicFunctionCreate, db: Session = Depends(get_db)):
    existing = db.query(StrategicFunction).filter(StrategicFunction.function_name == item_in.function_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Function with this name already exists")
    func = StrategicFunction(**item_in.model_dump())
    db.add(func)
    db.commit()
    db.refresh(func)
    return func

# 2. Capabilities
@router.get("/capabilities", response_model=List[CapabilityCapacityOut])
def list_capabilities(db: Session = Depends(get_db)):
    return db.query(CapabilityCapacity).order_by(CapabilityCapacity.id.asc()).all()

@router.post("/capabilities", response_model=CapabilityCapacityOut)
def create_capability(item_in: CapabilityCapacityCreate, db: Session = Depends(get_db)):
    cap = CapabilityCapacity(**item_in.model_dump())
    db.add(cap)
    db.commit()
    db.refresh(cap)
    return cap

# 3. Dynamic KPIs
@router.get("/kpis", response_model=List[EnterpriseKPIOut])
def list_kpis(category: Optional[str] = None, period: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(EnterpriseKPI)
    if category:
        q = q.filter(EnterpriseKPI.category == category)
    if period:
        q = q.filter(EnterpriseKPI.period == period)
    return q.order_by(EnterpriseKPI.id.asc()).all()

@router.post("/kpis", response_model=EnterpriseKPIOut)
def create_kpi(kpi_in: EnterpriseKPICreate, db: Session = Depends(get_db)):
    existing = db.query(EnterpriseKPI).filter(EnterpriseKPI.kpi_code == kpi_in.kpi_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="KPI Code already exists")
    
    variance = kpi_in.actual_value - kpi_in.target_value
    variance_pct = (variance / kpi_in.target_value * 100) if kpi_in.target_value != 0 else 0.0

    kpi = EnterpriseKPI(
        **kpi_in.model_dump(),
        variance=round(variance, 2),
        variance_pct=round(variance_pct, 2)
    )
    db.add(kpi)
    db.commit()
    db.refresh(kpi)
    return kpi

@router.patch("/kpis/{kpi_id}", response_model=EnterpriseKPIOut)
def update_kpi_actual(kpi_id: int, update_data: EnterpriseKPIUpdate, db: Session = Depends(get_db)):
    kpi = db.query(EnterpriseKPI).filter(EnterpriseKPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
        
    if update_data.actual_value is not None:
        kpi.actual_value = update_data.actual_value
        kpi.variance = round(kpi.actual_value - kpi.target_value, 2)
        kpi.variance_pct = round((kpi.variance / kpi.target_value * 100) if kpi.target_value != 0 else 0.0, 2)
    if update_data.status:
        kpi.status = update_data.status
    if update_data.notes:
        kpi.notes = update_data.notes
        
    db.commit()
    db.refresh(kpi)
    return kpi

# 4. Strategic Decisions & Executive Thoughts
@router.get("/thoughts-decisions", response_model=List[StrategicDecisionThoughtOut])
@router.get("/thoughts", response_model=List[StrategicDecisionThoughtOut])
def list_thoughts_decisions(entry_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(StrategicDecisionThought)
    if entry_type:
        q = q.filter(StrategicDecisionThought.entry_type == entry_type)
    return q.order_by(StrategicDecisionThought.date_recorded.desc()).all()

@router.post("/thoughts-decisions", response_model=StrategicDecisionThoughtOut)
@router.post("/thoughts", response_model=StrategicDecisionThoughtOut)
def record_thought_or_decision(item_in: StrategicDecisionThoughtCreate, db: Session = Depends(get_db)):
    entry = StrategicDecisionThought(**item_in.model_dump())
    if not entry.date_recorded:
        entry.date_recorded = date.today()
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# 5. Implementation Roadmap
@router.get("/roadmap", response_model=List[ImplementationRoadmapItemOut])
def list_roadmap_items(workstream: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(ImplementationRoadmapItem)
    if workstream:
        q = q.filter(ImplementationRoadmapItem.workstream == workstream)
    return q.order_by(ImplementationRoadmapItem.due_date.asc()).all()

@router.post("/roadmap", response_model=ImplementationRoadmapItemOut)
def create_roadmap_item(item_in: ImplementationRoadmapItemCreate, db: Session = Depends(get_db)):
    item = ImplementationRoadmapItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# 6. Executive Strategy Summary
@router.get("/summary")
def get_strategy_summary(db: Session = Depends(get_db)):
    total_funcs = db.query(StrategicFunction).count()
    total_kpis = db.query(EnterpriseKPI).count()
    on_track_kpis = db.query(EnterpriseKPI).filter(EnterpriseKPI.status.in_(["On Track", "Achieved"])).count()
    total_decisions = db.query(StrategicDecisionThought).count()
    total_roadmap = db.query(ImplementationRoadmapItem).count()
    
    return {
        "status": "success",
        "strategic_functions_count": total_funcs,
        "kpis": {
            "total": total_kpis,
            "on_track_or_achieved": on_track_kpis,
            "health_score_pct": round((on_track_kpis / total_kpis * 100) if total_kpis > 0 else 100, 1)
        },
        "executive_decisions_logged": total_decisions,
        "active_roadmap_milestones": total_roadmap
    }
