"""
Asperion Enterprise OS - ISO Standards, QMS, Grievance Redressal & Worksheets API Router
Pillars: ISO 9001 (QMS), ISO 27001 (ISMS), ISO 42001 (AIMS), ISO 20000-1 (ITSM), ISO 22301 (BCMS), Grievance Redressal
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import get_db
from app.models.iso_standards import (
    ISOCertificationMaster, ISOClauseControl, ISOAuditInspection,
    ISOCorrectiveActionWorksheet, FormalGrievanceRecord
)
from app.schemas.iso_standards import (
    ISOCertificationCreate, ISOCertificationOut,
    ISOClauseControlCreate, ISOClauseControlOut,
    ISOAuditInspectionCreate, ISOAuditInspectionOut,
    ISOCorrectiveActionWorksheetCreate, ISOCorrectiveActionWorksheetOut,
    FormalGrievanceCreate, FormalGrievanceOut, GrievanceResolutionUpdate
)
from app.engines.iso_engine import evaluate_enterprise_iso_compliance

router = APIRouter(prefix="/iso-standards", tags=["ISO Standards & Grievance Redressal"])

@router.get("/overview", response_model=Dict[str, Any])
def get_iso_overview(db: Session = Depends(get_db)):
    """Holistic conformity telemetry across all 5 acquired ISO standards."""
    return evaluate_enterprise_iso_compliance(db)

# --- 1. ISO CERTIFICATION LEDGER ---
@router.get("/certifications", response_model=List[ISOCertificationOut])
def list_iso_certifications(db: Session = Depends(get_db)):
    """List all official ISO certifications acquired by Asperion."""
    return db.query(ISOCertificationMaster).order_by(ISOCertificationMaster.standard_code.asc()).all()

@router.post("/certifications", response_model=ISOCertificationOut, status_code=status.HTTP_201_CREATED)
def register_iso_certification(payload: ISOCertificationCreate, db: Session = Depends(get_db)):
    """Register or renew an ISO certificate record."""
    existing = db.query(ISOCertificationMaster).filter(ISOCertificationMaster.standard_code == payload.standard_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Certification for {payload.standard_code} already registered.")
    cert = ISOCertificationMaster(**payload.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

# --- 2. ISO CLAUSES, CONTROLS & IMPLEMENTATION WORKSHEETS ---
@router.get("/controls", response_model=List[ISOClauseControlOut])
def list_iso_clause_controls(
    standard: Optional[str] = Query(None, description="Filter by ISO standard code (e.g. ISO-9001:2015, ISO-42001:2023)"),
    db: Session = Depends(get_db)
):
    """Retrieve clause implementation worksheets, requirements, mechanisms and compliance scores."""
    q = db.query(ISOClauseControl)
    if standard:
        q = q.filter(ISOClauseControl.standard_code == standard)
    return q.order_by(ISOClauseControl.standard_code.asc(), ISOClauseControl.clause_number.asc()).all()

@router.post("/controls", response_model=ISOClauseControlOut, status_code=status.HTTP_201_CREATED)
def create_iso_clause_control(payload: ISOClauseControlCreate, db: Session = Depends(get_db)):
    """Add a detailed ISO clause worksheet control."""
    existing = db.query(ISOClauseControl).filter(ISOClauseControl.control_code == payload.control_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Control {payload.control_code} already exists.")
    ctrl = ISOClauseControl(**payload.dict())
    db.add(ctrl)
    db.commit()
    db.refresh(ctrl)
    return ctrl

# --- 3. AUDIT INSPECTIONS ---
@router.get("/audits", response_model=List[ISOAuditInspectionOut])
def list_iso_audits(db: Session = Depends(get_db)):
    """List internal and external ISO audit inspection records."""
    return db.query(ISOAuditInspection).order_by(ISOAuditInspection.audit_date.desc()).all()

@router.post("/audits", response_model=ISOAuditInspectionOut, status_code=status.HTTP_201_CREATED)
def record_iso_audit(payload: ISOAuditInspectionCreate, db: Session = Depends(get_db)):
    """Record an audit inspection report."""
    audit = ISOAuditInspection(**payload.dict())
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit

# --- 4. CAPA WORKSHEETS ---
@router.get("/capas", response_model=List[ISOCorrectiveActionWorksheetOut])
def list_iso_capas(db: Session = Depends(get_db)):
    """List ISO Corrective and Preventive Action (CAPA) worksheets with 5-Whys root cause analysis."""
    return db.query(ISOCorrectiveActionWorksheet).order_by(ISOCorrectiveActionWorksheet.target_closure_date.desc()).all()

@router.post("/capas", response_model=ISOCorrectiveActionWorksheetOut, status_code=status.HTTP_201_CREATED)
def create_iso_capa(payload: ISOCorrectiveActionWorksheetCreate, db: Session = Depends(get_db)):
    """Create a new CAPA worksheet."""
    capa = ISOCorrectiveActionWorksheet(**payload.dict())
    db.add(capa)
    db.commit()
    db.refresh(capa)
    return capa

# --- 5. FORMAL GRIEVANCE REDRESSAL REGISTER ---
@router.get("/grievances", response_model=List[FormalGrievanceOut])
def list_formal_grievances(
    status_filter: Optional[str] = Query(None, description="Filter by status (Open, Resolved & Closed)"),
    db: Session = Depends(get_db)
):
    """Retrieve formal stakeholder grievances, investigation notes, and resolution records."""
    q = db.query(FormalGrievanceRecord)
    if status_filter:
        q = q.filter(FormalGrievanceRecord.status == status_filter)
    return q.order_by(FormalGrievanceRecord.created_at.desc()).all()

@router.post("/grievances", response_model=FormalGrievanceOut, status_code=status.HTTP_201_CREATED)
def lodge_formal_grievance(payload: FormalGrievanceCreate, db: Session = Depends(get_db)):
    """Lodge a new formal grievance with statutory escalation timeline."""
    existing = db.query(FormalGrievanceRecord).filter(FormalGrievanceRecord.grievance_id == payload.grievance_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Grievance ID {payload.grievance_id} already exists.")
    grv = FormalGrievanceRecord(**payload.dict())
    db.add(grv)
    db.commit()
    db.refresh(grv)
    return grv

@router.patch("/grievances/{grievance_id}/resolve", response_model=FormalGrievanceOut)
def resolve_formal_grievance(grievance_id: str, payload: GrievanceResolutionUpdate, db: Session = Depends(get_db)):
    """Formally resolve and close a grievance with investigation notes and CSAT rating."""
    grv = db.query(FormalGrievanceRecord).filter(FormalGrievanceRecord.grievance_id == grievance_id).first()
    if not grv:
        raise HTTPException(status_code=404, detail="Grievance not found.")
    grv.investigation_notes = payload.investigation_notes
    grv.resolution_details = payload.resolution_details
    grv.complainant_satisfied = payload.complainant_satisfied
    grv.csat_score = payload.csat_score
    grv.status = payload.status
    grv.closure_date = date.today()
    db.commit()
    db.refresh(grv)
    return grv


@router.get("/grievances/{grievance_id}/document", response_class=HTMLResponse)
def get_grievance_document_html(grievance_id: str, db: Session = Depends(get_db)):
    """Renders a formal printable ISO Grievance Acknowledgment & Redressal Certificate with company logo."""
    grv = db.query(FormalGrievanceRecord).filter(FormalGrievanceRecord.grievance_id == grievance_id).first()
    if not grv:
        raise HTTPException(status_code=404, detail="Grievance record not found.")

    created_str = grv.created_at.strftime('%Y-%m-%d %H:%M:%S') if grv.created_at else 'Recorded'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ISO Grievance Redressal Certificate - {grv.grievance_id}</title>
        <style>
            body {{ font-family: 'Segoe UI', -apple-system, Arial, sans-serif; background: #f8fafc; color: #0f172a; padding: 30px; }}
            .doc-container {{ max-width: 820px; margin: 0 auto; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 36px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); }}
            .header-table {{ width: 100%; border-bottom: 2px solid #d97706; padding-bottom: 16px; margin-bottom: 24px; }}
            .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 12px; }}
            .data-table th, .data-table td {{ border: 1px solid #e2e8f0; padding: 10px 12px; text-align: left; }}
            .data-table th {{ background: #f1f5f9; font-weight: 700; width: 28%; }}
            .seal-box {{ display: inline-block; padding: 6px 14px; background: #ecfdf5; border: 1.5px solid #10b981; border-radius: 6px; color: #047857; font-weight: bold; font-size: 12px; }}
            .footer {{ margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 10px; color: #64748b; text-align: center; }}
            @media print {{ body {{ background: #fff; padding: 0; }} .doc-container {{ border: none; box-shadow: none; padding: 0; }} .print-btn {{ display: none; }} }}
            .print-btn {{ background: #2563eb; color: #fff; border: none; padding: 8px 18px; border-radius: 6px; font-weight: 600; cursor: pointer; margin-bottom: 16px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div style="max-width: 820px; margin: 0 auto;">
            <button class="print-btn" onclick="window.print()">🖨️ Print Grievance Certificate</button>
        </div>
        <div class="doc-container">
            <table class="header-table">
                <tr>
                    <td style="vertical-align: middle; width: 64px; padding-right: 14px;">
                        <img src="/static/img/logo.png" alt="Asperion Logo" style="width: 58px; height: 58px; border-radius: 50%; object-fit: contain; background: #0f172a; padding: 2px; border: 1.5px solid #d97706; display: block;">
                    </td>
                    <td style="vertical-align: middle;">
                        <div style="font-size: 18px; font-weight: 800; color: #0f172a;">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                        <div style="font-size: 11px; font-family: monospace; color: #475569; margin-top: 2px;">CIN: U85500KA2026OPC222069 | ISO 9001:2015 & ISO/IEC 27001:2022 Certified</div>
                        <div style="font-size: 10px; color: #64748b; margin-top: 2px;">
                            Registered Office: Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore - 560043
                        </div>
                    </td>
                    <td style="text-align: right; vertical-align: middle;">
                        <div style="font-size: 15px; font-weight: 800; color: #d97706; text-transform: uppercase;">ISO Grievance Record</div>
                        <div style="font-family: monospace; font-size: 13px; font-weight: 700; color: #0f172a; margin-top: 2px;">{grv.grievance_id}</div>
                        <div style="margin-top: 4px;"><span class="seal-box">{grv.status}</span></div>
                    </td>
                </tr>
            </table>

            <table class="data-table">
                <tr><th>Complainant Name</th><td><strong>{grv.complainant_name}</strong> ({grv.complainant_email})</td></tr>
                <tr><th>Stakeholder Category</th><td>{grv.stakeholder_category}</td></tr>
                <tr><th>Grievance Nature</th><td>{grv.grievance_category}</td></tr>
                <tr><th>Lodged Date & Time</th><td>{created_str}</td></tr>
                <tr><th>Subject</th><td><strong>{grv.subject}</strong></td></tr>
                <tr><th>Full Description</th><td>{grv.description}</td></tr>
                <tr><th>Assigned Redressal Officer</th><td>{grv.assigned_redressal_officer}</td></tr>
                <tr><th>Statutory Resolution SLA</th><td>{grv.statutory_sla_days} Calendar Days</td></tr>
                <tr><th>Investigation Findings</th><td>{grv.investigation_notes or 'Under formal review against standard operating procedures.'}</td></tr>
                <tr><th>Remedial Action Taken</th><td>{grv.resolution_details or 'Pending final stakeholder confirmation.'}</td></tr>
            </table>

            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 40px; padding-top: 15px; border-top: 1px solid #cbd5e1;">
                <div>
                    <div style="font-size: 11px; color: #64748b;">Statutory Quality Management Certification:</div>
                    <div style="font-size: 10px; font-weight: 600; color: #0f172a; margin-top: 2px;">ISO 9001:2015 &bull; ISO/IEC 27001:2022 &bull; ISO/IEC 42001:2023</div>
                </div>
                <div style="text-align: center; border-top: 1px solid #94a3b8; width: 220px; padding-top: 6px;">
                    <div style="font-size: 12px; font-weight: 700; color: #0f172a;">Varadi Vijay</div>
                    <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Founder & Sole Director</div>
                    <div style="font-size: 9px; color: #2563eb; font-weight: 600;">Authorized Redressal Authority</div>
                </div>
            </div>

            <div class="footer">
                Asperion Enterprise Operating System &bull; Official Statutory Grievance Document &bull; Generated from Immutable Audit Ledger
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

