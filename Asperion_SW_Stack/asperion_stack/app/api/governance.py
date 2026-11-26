"""
Asperion Enterprise OS - Governance API
Handles Corporate Records, Board Resolutions, Compliance Calendar, and Policies
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.governance import EntityMaster, BoardResolution, ComplianceCalendarItem, PolicyRecord, AuthorityMatrixItem, AuditLog
from app.schemas.governance import (
    EntityMasterOut, BoardResolutionCreate, BoardResolutionOut,
    ComplianceCalendarItemCreate, ComplianceCalendarItemOut,
    AuditLogCreate, AuditLogOut
)

router = APIRouter(prefix="/governance", tags=["Corporate Governance & Legal Entity"])

@router.get("/entity", response_model=EntityMasterOut)
def get_entity_profile(db: Session = Depends(get_db)):
    entity = db.query(EntityMaster).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity profile not initialized")
    return entity

@router.get("/resolutions", response_model=List[BoardResolutionOut])
def list_board_resolutions(db: Session = Depends(get_db)):
    return db.query(BoardResolution).order_by(BoardResolution.date_passed.desc()).all()

@router.post("/resolutions", response_model=BoardResolutionOut)
def create_board_resolution(res_in: BoardResolutionCreate, db: Session = Depends(get_db)):
    res = BoardResolution(**res_in.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

@router.get("/compliance-calendar", response_model=List[ComplianceCalendarItemOut])
def list_compliance_items(db: Session = Depends(get_db)):
    return db.query(ComplianceCalendarItem).order_by(ComplianceCalendarItem.due_date.asc()).all()

@router.post("/compliance-calendar", response_model=ComplianceCalendarItemOut)
def add_compliance_item(item_in: ComplianceCalendarItemCreate, db: Session = Depends(get_db)):
    item = ComplianceCalendarItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/policies")
def list_policies(db: Session = Depends(get_db)):
    return db.query(PolicyRecord).all()

@router.get("/authority-matrix")
def list_authority_matrix(db: Session = Depends(get_db)):
    return db.query(AuthorityMatrixItem).all()

@router.get("/audit-logs", response_model=List[AuditLogOut])
def list_audit_logs(module: str = None, severity: str = None, db: Session = Depends(get_db)):
    q = db.query(AuditLog)
    if module:
        q = q.filter(AuditLog.module == module)
    if severity:
        q = q.filter(AuditLog.severity == severity)
    return q.order_by(AuditLog.created_at.desc()).limit(100).all()

@router.post("/audit-logs", response_model=AuditLogOut)
def record_audit_log(entry: AuditLogCreate, db: Session = Depends(get_db)):
    log_rec = AuditLog(**entry.model_dump())
    db.add(log_rec)
    db.commit()
    db.refresh(log_rec)
    return log_rec

