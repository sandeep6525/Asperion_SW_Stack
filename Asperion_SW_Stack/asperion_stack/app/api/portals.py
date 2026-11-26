"""
Asperion Enterprise OS - Stakeholder Portals API Router
Dedicated secure backends for:
1. Employee Self-Service (ESS): Personal biometric punches, salary statements, leaves, tax declarations.
2. Client Project & SLA Portal: Active deliverables, sprint progress, milestone invoices, support tickets.
3. Vendor Sourcing & Procurement Portal: POs, Goods Receipt Notes (GRN), invoice submissions, MSME status.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta
import json
import math
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.hrms import Employee, SalaryStructure, PayrollRecord, LeaveRecord
from app.models.attendance import AttendanceRecord
from app.models.finance import Invoice, PurchaseOrder, APBill
from app.models.pmo import Project, WBSTask, Sprint, ProjectMilestone, ChangeRequest
from app.models.crm_enterprise import SupportTicket, Opportunity, CustomerAccount
from app.models.crm_legal import ClientContract
from app.models.infrastructure import ITAsset, IAMCredential
from app.models.passkey_infrastructure import PasskeyCredential
from app.models.training import EmployeeTrainingEnrollment, TrainingModule, TrainingMaterial
from app.models.ticketing_notifications import InternalTicket
from app.models.governance import EntityMaster, PolicyRecord, ComplianceCalendarItem
from app.models.procurement import (
    Vendor, VendorContract, GoodsReceivedNote, StrategicSourcingEvent,
    VendorBidSubmission, VendorScorecard, VendorRiskAssessment, VendorCorrectiveActionPlan
)
from app.schemas.procurement import PortalInwardGRNCreate, PortalVendorBillSubmit, PortalRFXBidSubmit
from app.engines.salary_statement_engine import get_employee_salary_slip_html
import uuid

class ClientTicketCreateRequest(BaseModel):
    client_name: str = "Zenith Global Corp"
    contact_email: str
    subject: str
    description: str
    category: str = "Platform Feature"
    severity: str = "P3-Medium"

class ClientMilestoneSignoffRequest(BaseModel):
    client_signatory_name: str
    approval_status: str = "Client Approved"
    acceptance_notes: Optional[str] = ""

class ClientChangeRequestReview(BaseModel):
    action: str = "APPROVE"
    client_approver_name: str
    review_notes: Optional[str] = ""

class ClientPaymentRecordRequest(BaseModel):
    payment_reference: str
    amount_inr: float
    payment_mode: str = "NEFT / RTGS"
    notes: Optional[str] = ""

class PortalLeaveApplyRequest(BaseModel):
    emp_code: str
    leave_type: str = Field(..., description="Earned Leave, Casual Leave, Sick Leave")
    start_date: date
    end_date: date
    total_days: float = 1.0
    reason: str

class PortalQuickClockInRequest(BaseModel):
    emp_code: str
    latitude: Optional[float] = 13.035820
    longitude: Optional[float] = 77.653410
    in_source: Optional[str] = "ESS_PORTAL"

class PortalRaiseTicketRequest(BaseModel):
    emp_code: str
    department: str
    category: str
    subject: str
    description: str
    priority: Optional[str] = "P3-Medium"

router = APIRouter(prefix="/portals", tags=["Stakeholder Dedicated Portals"])

# ==============================================================================
# ==============================================================================
# 1. EMPLOYEE SELF-SERVICE (ESS) & DIGITAL WORKPLACE PORTAL
# ==============================================================================

HQ_LATITUDE = 13.035820
HQ_LONGITUDE = 77.653410

def _haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0 # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)

@router.get("/employee/dashboard-data")
def get_employee_portal_data(emp_code: str = "ADT-EMP-001", db: Session = Depends(get_db)) -> Dict[str, Any]:
    all_emps = db.query(Employee).filter(Employee.employment_status == "Active").all()
    emp = db.query(Employee).filter(Employee.emp_code == emp_code).first()
    if not emp:
        emp = all_emps[0] if all_emps else db.query(Employee).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    sal = emp.salary_structure

    # Attendance
    attendance_records = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id
    ).order_by(AttendanceRecord.attendance_date.desc()).limit(20).all()

    present_this_month = sum(1 for a in attendance_records if a.status in ["Present", "Late Mark", "Regularized"])
    avg_hours = round(sum(a.effective_work_hours for a in attendance_records) / len(attendance_records), 1) if attendance_records else 8.5
    geofence_verified_count = sum(1 for a in attendance_records if getattr(a, "geofence_verified", False))

    # Payroll records
    payroll_records = db.query(PayrollRecord).filter(
        PayrollRecord.employee_id == emp.id
    ).order_by(PayrollRecord.created_at.desc()).limit(12).all()

    # Leaves
    leaves = db.query(LeaveRecord).filter(
        LeaveRecord.employee_id == emp.id
    ).order_by(LeaveRecord.created_at.desc()).all()

    el_consumed = sum(l.total_days for l in leaves if "earn" in (l.leave_type or "").lower() and l.status == "Approved")
    cl_consumed = sum(l.total_days for l in leaves if "casual" in (l.leave_type or "").lower() and l.status == "Approved")
    sl_consumed = sum(l.total_days for l in leaves if "sick" in (l.leave_type or "").lower() and l.status == "Approved")

    # Learning & Training Academy
    enrollments = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.employee_email == emp.official_email
    ).all()
    total_hours_learned = sum(e.hours_spent for e in enrollments)
    certificates = [
        {
            "certificate_id": e.certificate_id,
            "module_code": e.module.module_code if e.module else "TRN-MOD",
            "module_title": e.module.title if e.module else "Module",
            "score_pct": e.score_pct,
            "completed_at": str(e.completed_at.date()) if e.completed_at else str(date.today()),
            "export_url": f"/api/v1/training/certificates/{e.certificate_id}/html"
        }
        for e in enrollments if e.certificate_id
    ]

    # IT Assets
    assets = db.query(ITAsset).filter(
        ITAsset.assigned_to_email == emp.official_email
    ).all()

    # Passkeys
    passkeys = db.query(PasskeyCredential).filter(
        PasskeyCredential.user_email == emp.official_email
    ).all()

    # Internal Tickets
    tickets = db.query(InternalTicket).filter(
        InternalTicket.requester_email == emp.official_email
    ).order_by(InternalTicket.created_at.desc()).limit(10).all()

    # Handbooks & Training Materials
    materials = db.query(TrainingMaterial).limit(7).all()

    # 2026 Karnataka Statutory Holidays
    karnataka_holidays_2026 = [
        {"date": "2026-01-26", "name": "Republic Day", "day": "Monday", "type": "National Holiday"},
        {"date": "2026-03-19", "name": "Ugadi (Kannada New Year)", "day": "Thursday", "type": "State Festival"},
        {"date": "2026-05-01", "name": "May Day / Labour Day", "day": "Friday", "type": "Statutory Holiday"},
        {"date": "2026-08-15", "name": "Independence Day", "day": "Saturday", "type": "National Holiday"},
        {"date": "2026-10-02", "name": "Mahatma Gandhi Jayanti", "day": "Friday", "type": "National Holiday"},
        {"date": "2026-10-20", "name": "Ayudha Pooja & Vijayadashami", "day": "Tuesday", "type": "State Festival"},
        {"date": "2026-11-01", "name": "Kannada Rajyotsava", "day": "Sunday", "type": "State Holiday"},
        {"date": "2026-11-08", "name": "Deepavali (Naraka Chaturdashi)", "day": "Sunday", "type": "Public Festival"},
        {"date": "2026-11-10", "name": "Balipadyami / Diwali", "day": "Tuesday", "type": "Public Festival"},
        {"date": "2026-12-25", "name": "Christmas Day", "day": "Friday", "type": "Public Holiday"}
    ]

    return {
        "corporate_entity": {
            "company_name": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            "cin": "U85500KA2026OPC222069",
            "founder_director": "Varadi Vijay",
            "director": "Varadi Vijay",
            "hq_address": "Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka",
            "hq_coordinates": {"latitude": HQ_LATITUDE, "longitude": HQ_LONGITUDE, "geofence_radius_meters": 200.0}
        },
        "employees_roster": [
            {
                "emp_code": e.emp_code,
                "name": e.full_name,
                "designation": e.designation,
                "department": e.department
            } for e in all_emps
        ],
        "profile": {
            "id": emp.id,
            "emp_code": emp.emp_code,
            "name": emp.full_name,
            "official_email": emp.official_email,
            "phone": emp.phone or "+91-9876543210",
            "designation": emp.designation,
            "department": emp.department,
            "employment_type": emp.employment_type or "Full-Time Permanent",
            "date_of_joining": str(emp.date_of_joining),
            "probation_status": emp.probation_status or "Confirmed",
            "reporting_manager": emp.reporting_manager or "Varadi Vijay (Sole Director)",
            "work_location": emp.work_location or "Bangalore (Horamavu HQ)",
            "pan_number": emp.pan_number or "AAACA1234D",
            "aadhaar_number": emp.aadhaar_number or "•••• •••• 9012",
            "uan_number": emp.uan_number or "101928374650",
            "esic_number": emp.esic_number or "55001234560010001",
            "bank_name": emp.bank_name or "ICICI Bank - Main Branch",
            "bank_account_number": emp.bank_account_number or "000123456789",
            "bank_ifsc": emp.bank_ifsc or "ICIC0001234"
        },
        "salary_overview": {
            "annual_ctc": sal.annual_ctc if sal else 1200000.0,
            "monthly_gross": sal.gross_salary if sal else 100000.0,
            "basic_salary": sal.basic_salary if sal else 40000.0,
            "hra": sal.hra if sal else 16000.0,
            "special_allowance": sal.special_allowance if sal else 44000.0,
            "employer_pf": sal.employer_pf if sal else 1800.0,
            "gratuity_provision": sal.gratuity_provision if sal else 1923.0,
            "employee_pf": sal.employee_pf if sal else 1800.0,
            "professional_tax": sal.professional_tax if sal else 200.0,
            "estimated_tds": sal.estimated_tds if sal else 0.0,
            "total_deductions": sal.total_deductions if sal else 2000.0,
            "net_in_hand": sal.net_in_hand if sal else 98000.0,
            "tax_regime": "Section 115BAC Default (New Tax Regime - Nil Tax up to ₹7.75 Lakhs with ₹75k Standard Deduction)"
        },
        "salary_breakup": {
            "annual_ctc": sal.annual_ctc if sal else 1200000.0,
            "monthly_gross": sal.gross_salary if sal else 100000.0,
            "basic_salary": sal.basic_salary if sal else 40000.0,
            "hra": sal.hra if sal else 16000.0,
            "special_allowance": sal.special_allowance if sal else 44000.0,
            "employer_pf": sal.employer_pf if sal else 1800.0,
            "gratuity_provision": sal.gratuity_provision if sal else 1923.0,
            "employee_pf": sal.employee_pf if sal else 1800.0,
            "professional_tax": sal.professional_tax if sal else 200.0,
            "estimated_tds": sal.estimated_tds if sal else 0.0,
            "total_deductions": sal.total_deductions if sal else 2000.0,
            "net_in_hand": sal.net_in_hand if sal else 98000.0,
            "tax_regime": "Section 115BAC Default (New Tax Regime - Nil Tax up to ₹7.75 Lakhs with ₹75k Standard Deduction)"
        },
        "attendance_stats": {
            "recent_punches": present_this_month,
            "avg_daily_hours": avg_hours,
            "geofence_compliance_pct": round((geofence_verified_count / len(attendance_records) * 100), 1) if attendance_records else 98.4,
            "records": [
                {
                    "date": str(a.attendance_date),
                    "clock_in": a.clock_in_time.strftime("%H:%M") if a.clock_in_time else "--:--",
                    "clock_out": a.clock_out_time.strftime("%H:%M") if a.clock_out_time else "--:--",
                    "hours": a.effective_work_hours,
                    "status": a.status,
                    "channel": a.in_source or "FACIAL_KIOSK",
                    "geofence": "Verified HQ (200m)" if getattr(a, "geofence_verified", False) else "Remote Approved",
                    "distance_m": getattr(a, "geofence_distance_meters", 15.2)
                } for a in attendance_records
            ]
        },
        "leave_ledger": {
            "annual_earned_leave_balance": max(0.0, 18.0 - el_consumed),
            "casual_sick_leave_balance": max(0.0, 12.0 - (cl_consumed + sl_consumed)),
            "comp_off_balance": 0.0,
            "total_available_days": max(0.0, 30.0 - (el_consumed + cl_consumed + sl_consumed)),
            "consumed_days": el_consumed + cl_consumed + sl_consumed,
            "applications": [
                {
                    "type": l.leave_type,
                    "dates": f"{l.start_date} to {l.end_date}",
                    "days": l.total_days,
                    "reason": l.reason,
                    "status": l.status,
                    "approved_by": getattr(l, "approver", None) or "HR / Director"
                } for l in leaves
            ],
            "statutory_holidays_2026": karnataka_holidays_2026
        },
        "learning_and_probation": {
            "total_hours_completed": total_hours_learned,
            "min_required_hours": 16.0,
            "max_recommended_hours": 40.0,
            "probation_clearance_ready": total_hours_learned >= 16.0 or emp.probation_status == "Confirmed",
            "probation_status": emp.probation_status or "Confirmed",
            "enrolled_courses": [
                {
                    "code": e.module.module_code if e.module else "TRN-001",
                    "title": e.module.title if e.module else "Course",
                    "progress_pct": e.progress_pct,
                    "hours_spent": e.hours_spent,
                    "status": e.status,
                    "score_pct": e.score_pct,
                    "certificate_id": e.certificate_id
                } for e in enrollments
            ],
            "certificates": certificates
        },
        "it_assets_and_security": {
            "hardware_assets": [
                {
                    "tag": a.asset_tag,
                    "model": a.make_model,
                    "serial": a.serial_number,
                    "os": a.os_version,
                    "encrypted": a.disk_encryption_enabled,
                    "antivirus": a.edr_antivirus_installed,
                    "warranty_until": str(a.warranty_expiry_date),
                    "status": a.asset_status
                } for a in assets
            ],
            "passkeys": [
                {
                    "passkey_id": p.passkey_id,
                    "device": p.device_name,
                    "type": p.authenticator_type,
                    "aaguid": p.aaguid,
                    "sign_count": getattr(p, "sign_count", 42)
                } for p in passkeys
            ] or [
                {
                    "passkey_id": f"FIDO-2026-{emp.emp_code[-3:]}",
                    "device": "YubiKey 5C NFC / Apple Secure Enclave",
                    "type": "Hardware WebAuthn Passkey (Level 3)",
                    "aaguid": "cb69481e-8ff7-4039-93ec-0a2729a100bf",
                    "sign_count": 86
                }
            ],
            "zero_trust_status": "ZTNA Active (Policy ZTNA-DEV-001)"
        },
        "payslips": [
            {
                "cycle": p.payroll_cycle,
                "earned_gross": p.earned_gross,
                "net_salary": p.net_salary,
                "payment_status": p.payment_status,
                "bank_utr": p.bank_utr or f"CMS{emp.id}9827364",
                "slip_url": f"/api/v1/hrms/salary-statement/payslip/{emp.id}?cycle={p.payroll_cycle}"
            } for p in payroll_records
        ],
        "internal_tickets": [
            {
                "number": t.ticket_number,
                "dept": t.department,
                "category": t.category,
                "subject": t.subject,
                "priority": t.priority,
                "status": t.status,
                "sla_hours": t.sla_deadline_hours,
                "created_at": str(t.created_at.date()) if t.created_at else str(date.today()),
                "resolution": t.resolution_summary or "Active in queue"
            } for t in tickets
        ],
        "handbooks_and_playbooks": [
            {
                "code": m.material_code,
                "title": m.title,
                "category": m.category,
                "doc_type": m.doc_type,
                "reading_time": m.reading_time_mins,
                "export_url": f"/api/v1/training/materials/{m.id}/export-html"
            } for m in materials
        ]
    }


@router.post("/employee/apply-leave")
def portal_apply_leave(req: PortalLeaveApplyRequest, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_code == req.emp_code).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_leave = LeaveRecord(
        employee_id=emp.id,
        employee_name=emp.full_name,
        leave_type=req.leave_type,
        start_date=req.start_date,
        end_date=req.end_date,
        total_days=req.total_days,
        reason=req.reason,
        status="Pending",
        approver=None
    )
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return {
        "status": "success",
        "message": f"Leave application for {req.total_days} day(s) submitted successfully.",
        "leave_id": new_leave.id,
        "leave_record": {
            "id": new_leave.id,
            "leave_type": new_leave.leave_type,
            "total_days": new_leave.total_days,
            "status": new_leave.status
        }
    }


@router.post("/employee/quick-clock-in")
def portal_quick_clock_in(req: PortalQuickClockInRequest, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_code == req.emp_code).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    dist = _haversine_distance_m(req.latitude or HQ_LATITUDE, req.longitude or HQ_LONGITUDE, HQ_LATITUDE, HQ_LONGITUDE)
    is_geofenced = dist <= 200.0

    today = date.today()
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id,
        AttendanceRecord.attendance_date == today
    ).first()

    now_dt = datetime.now()
    if existing:
        existing.clock_out_time = now_dt
        if existing.clock_in_time:
            delta = (now_dt - existing.clock_in_time).total_seconds() / 3600.0
            existing.effective_work_hours = round(delta, 1)
            existing.total_work_hours = round(delta, 1)
        db.commit()
        return {"status": "success", "action": "CLOCKED_OUT", "time": now_dt.strftime("%H:%M:%S"), "distance_m": dist, "geofence_verified": is_geofenced}
    else:
        att = AttendanceRecord(
            employee_id=emp.id,
            attendance_date=today,
            clock_in_time=now_dt,
            clock_out_time=None,
            total_work_hours=0.0,
            effective_work_hours=8.5,
            status="Present",
            in_source=req.in_source or "ESS_PORTAL",
            in_latitude=req.latitude,
            in_longitude=req.longitude,
            geofence_verified=is_geofenced,
            geofence_zone_code="GEO-BLR-HQ",
            geofence_distance_meters=dist,
            facial_recognition_verified=True,
            facial_match_confidence_pct=98.5,
            facial_liveness_verified=True,
            is_anomalous=False
        )
        db.add(att)
        db.commit()
        return {"status": "success", "action": "CLOCKED_IN", "time": now_dt.strftime("%H:%M:%S"), "distance_m": dist, "geofence_verified": is_geofenced}


@router.post("/employee/raise-ticket")
def portal_raise_ticket(req: PortalRaiseTicketRequest, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_code == req.emp_code).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    count = db.query(InternalTicket).count() + 1
    dept_prefix = req.department.split('_')[0].upper()
    tkt_num = f"{dept_prefix}-TKT-2026-{count:04d}"

    ticket = InternalTicket(
        ticket_number=tkt_num,
        department=req.department,
        category=req.category,
        subject=req.subject,
        description=req.description,
        priority=req.priority or "P3-Medium",
        status="Open",
        requester_name=emp.full_name,
        requester_email=emp.official_email,
        requester_department=emp.department,
        assigned_to="People Ops / IT Support",
        assigned_department=req.department,
        sla_deadline_hours=24.0,
        target_resolution_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return {
        "status": "success",
        "ticket_number": ticket.ticket_number,
        "message": "Helpdesk ticket queued with 24-hour SLA.",
        "ticket": {
            "ticket_number": ticket.ticket_number,
            "department": ticket.department,
            "priority": ticket.priority,
            "sla_deadline_hours": 24.0,
            "status": ticket.status
        }
    }


@router.get("/employee/id-card-html", response_class=HTMLResponse)
def get_employee_id_card_html(emp_code: str = "ADT-EMP-001", db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.emp_code == emp_code).first()
    if not emp:
        emp = db.query(Employee).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Digital Identity Card - {emp.full_name} ({emp.emp_code})</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
            .card {{ width: 380px; background: #ffffff; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); overflow: hidden; border: 1px solid #334155; position: relative; }}
            .card-header {{ background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #047857 100%); padding: 24px 20px; text-align: center; color: white; position: relative; }}
            .brand-name {{ font-size: 13px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #38bdf8; }}
            .cin-text {{ font-size: 9px; color: #94a3b8; margin-top: 2px; font-family: monospace; }}
            .avatar-container {{ width: 90px; height: 90px; margin: 16px auto 0; border-radius: 50%; border: 3px solid #38bdf8; background: #0f172a; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: #38bdf8; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }}
            .card-body {{ padding: 20px; text-align: center; }}
            .emp-name {{ font-size: 19px; font-weight: 800; color: #0f172a; margin: 0; }}
            .emp-role {{ font-size: 12px; font-weight: 600; color: #2563eb; margin-top: 3px; }}
            .emp-dept {{ font-size: 11px; color: #64748b; margin-top: 1px; }}
            .badge-code {{ display: inline-block; margin-top: 10px; background: #f1f5f9; color: #0f172a; padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; font-family: monospace; border: 1px solid #cbd5e1; }}
            .details-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 20px; text-align: left; background: #f8fafc; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0; font-size: 11px; }}
            .detail-label {{ color: #64748b; font-size: 9px; text-transform: uppercase; font-weight: bold; }}
            .detail-val {{ color: #0f172a; font-weight: bold; margin-top: 1px; font-family: monospace; }}
            .security-badges {{ display: flex; justify-content: center; gap: 6px; margin-top: 14px; }}
            .sec-pill {{ font-size: 9px; font-weight: bold; padding: 2px 8px; border-radius: 4px; background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }}
            .signature-area {{ margin-top: 20px; padding-top: 12px; border-top: 1px dashed #cbd5e1; display: flex; justify-content: space-between; align-items: flex-end; font-size: 10px; color: #475569; }}
            .sig-title {{ font-size: 8px; color: #94a3b8; text-transform: uppercase; }}
            .sig-name {{ font-weight: bold; color: #0f172a; font-family: 'Brush Script MT', cursive, sans-serif; font-size: 16px; }}
            .card-footer {{ background: #0f172a; color: #94a3b8; font-size: 9px; text-align: center; padding: 10px; border-top: 1px solid #1e293b; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-header">
                <div class="brand-name">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div class="cin-text">CIN: U85500KA2026OPC222069</div>
                <div class="avatar-container">
                    {emp.full_name[0]}
                </div>
            </div>
            <div class="card-body">
                <div class="emp-name">{emp.full_name}</div>
                <div class="emp-role">{emp.designation}</div>
                <div class="emp-dept">{emp.department} &bull; Horamavu HQ Bangalore</div>
                <div class="badge-code">{emp.emp_code}</div>

                <div class="details-grid">
                    <div>
                        <div class="detail-label">Joining Date</div>
                        <div class="detail-val">{emp.date_of_joining}</div>
                    </div>
                    <div>
                        <div class="detail-label">Probation Status</div>
                        <div class="detail-val" style="color: #059669;">{emp.probation_status or 'Confirmed'}</div>
                    </div>
                    <div>
                        <div class="detail-label">Official Email</div>
                        <div class="detail-val" style="font-size: 9px;">{emp.official_email}</div>
                    </div>
                    <div>
                        <div class="detail-label">EPFO UAN</div>
                        <div class="detail-val">{emp.uan_number or '101928374650'}</div>
                    </div>
                </div>

                <div class="security-badges">
                    <span class="sec-pill">FIDO2 Hardware Bound</span>
                    <span class="sec-pill" style="background: #eff6ff; color: #1e40af; border-color: #bfdbfe;">Zero Trust ZTNA</span>
                    <span class="sec-pill" style="background: #faf5ff; color: #6b21a8; border-color: #e9d5ff;">Geofenced HQ</span>
                </div>

                <div class="signature-area">
                    <div>
                        <div class="sig-title">Authorized Signatory</div>
                        <div class="sig-name">Varadi Vijay</div>
                        <div style="font-size: 9px;">Founder & Sole Director</div>
                    </div>
                    <div style="text-align: right; font-family: monospace; font-size: 9px;">
                        <span>SECURITY ID:</span><br>
                        <strong>ADT-2026-{emp.id:04d}</strong>
                    </div>
                </div>
            </div>
            <div class="card-footer">
                Registered Office: Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore - 560043
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


# ==============================================================================
# 2. CLIENT PROJECT & SERVICE DESK PORTAL
# ==============================================================================

@router.get("/client/dashboard-data")
def get_client_portal_data(client_name: str = "Zenith Global Corp", db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns comprehensive Client Portal telemetry across:
    1. Contracted Service Level Agreement (SLA) Health
    2. Active Project SOW Deliverables & Sprints
    3. Milestone Deliverables with UAT Sign-offs
    4. Commercial B2B Tax Invoices & Payments
    5. 24x7 Support SLA Incidents & Breaches
    6. Scope Change Requests (CRs)
    7. Executed Legal Agreements (MSA, SOWs, NDAs)
    """
    clean_name = client_name.strip()
    search_prefix = clean_name[:6]

    # Projects
    projects = db.query(Project).filter(Project.client_name.ilike(f"%{search_prefix}%")).all()
    if not projects:
        projects = db.query(Project).all()
    proj_ids = [p.id for p in projects]

    # Milestones
    milestones = db.query(ProjectMilestone).filter(ProjectMilestone.project_id.in_(proj_ids)).all() if proj_ids else []
    if not milestones:
        milestones = db.query(ProjectMilestone).all()

    # Invoices
    invoices = db.query(Invoice).filter(Invoice.customer_name.ilike(f"%{search_prefix}%")).order_by(Invoice.id.desc()).all()
    if not invoices:
        invoices = db.query(Invoice).order_by(Invoice.id.desc()).limit(10).all()

    # Support Tickets
    tickets = db.query(SupportTicket).filter(SupportTicket.client_name.ilike(f"%{search_prefix}%")).order_by(SupportTicket.id.desc()).all()
    if not tickets:
        tickets = db.query(SupportTicket).order_by(SupportTicket.id.desc()).limit(10).all()

    # Change Requests
    change_orders = db.query(ChangeRequest).filter(ChangeRequest.project_id.in_(proj_ids)).all() if proj_ids else []
    if not change_orders:
        change_orders = db.query(ChangeRequest).all()

    # Contracts
    contracts = db.query(ClientContract).filter(ClientContract.client_name.ilike(f"%{search_prefix}%")).all()
    if not contracts:
        contracts = db.query(ClientContract).all()

    # WBS Tasks
    wbs_tasks = db.query(WBSTask).filter(WBSTask.project_id.in_(proj_ids)).order_by(WBSTask.wbs_code).limit(20).all() if proj_ids else []
    if not wbs_tasks:
        wbs_tasks = db.query(WBSTask).order_by(WBSTask.wbs_code).limit(20).all()

    # Customer Account Profile
    account = db.query(CustomerAccount).filter(CustomerAccount.client_name == clean_name).first()
    if not account:
        account = db.query(CustomerAccount).filter(CustomerAccount.client_name.ilike(f"%{search_prefix}%")).first()
    all_accounts = db.query(CustomerAccount).all()
    available_clients = [{"name": a.client_name, "code": a.account_code, "tier": a.tier} for a in all_accounts]
    if not any(c["name"] == "Zenith Global Corp" for c in available_clients):
        available_clients.insert(0, {"name": "Zenith Global Corp", "code": "CUST-ZENITH-01", "tier": "Tier-1 Enterprise Retainer"})

    # Aggregate Metrics
    total_sow_value = sum(p.budget_inr for p in projects if p.budget_inr)
    total_billed = sum(i.total_invoice_value for i in invoices if i.total_invoice_value)
    total_received = sum(i.amount_received for i in invoices if i.amount_received)
    outstanding_receivable = sum(i.outstanding_balance for i in invoices if i.outstanding_balance)
    
    milestones_total = len(milestones)
    milestones_completed = len([m for m in milestones if m.status in ["Client Approved", "Billed", "Approved"]])
    milestones_progress_pct = round((milestones_completed / max(1, milestones_total)) * 100.0, 1)

    open_sla_tickets = len([t for t in tickets if t.status in ["Open", "In Progress", "Work in Progress"]])

    return {
        "status": "success",
        "client_name": client_name,
        "relationship_tier": "Enterprise Retainer Partner",
        "dedicated_spoc": "Varadi Vijay (Founder & Sole Director)",
        "sla_coverage": "24x7 Mission Critical (P1 < 1.0h, 99.98% Availability)",
        "corporate_entity": {
            "entity_name": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            "cin": "U85500KA2026OPC222069",
            "pan": "AABCU9603R",
            "gstin": "29AABCU9603R1ZM",
            "director": "Varadi Vijay",
            "registered_office": "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India",
            "bank_name": "ICICI Bank Limited",
            "bank_account_no": "000205001234",
            "ifsc_code": "ICIC0000002",
            "branch": "Bangalore Corporate Banking Branch"
        },
        "client_profile": {
            "account_code": account.account_code if account else "CUST-ZENITH-01",
            "client_name": account.client_name if account else client_name,
            "industry": account.industry if account else "Omni-Channel Retail & Supply Chain",
            "primary_csm": account.primary_csm if account else "Sneha Rao",
            "executive_sponsor": "Varadi Vijay (Founder & Sole Director)",
            "annual_recurring_revenue_inr": account.annual_recurring_revenue_inr if account else 3600000.0,
            "health_score": account.health_score if account else 98.5,
            "health_status": account.health_status if account else "Excellent / High Engagement",
            "nps_score": account.nps_score if account else 78,
            "contract_start_date": str(account.contract_start_date) if account and account.contract_start_date else "2026-06-01",
            "renewal_date": str(account.renewal_date) if account and account.renewal_date else "2027-05-31",
            "notes": account.notes if account else "Anchor enterprise client under active multi-year MSA."
        },
        "available_clients": available_clients,
        "executive_kpis": {
            "contracted_uptime_pct": 99.98,
            "p1_sla_target_hours": 1.0,
            "avg_p1_response_mins": 18.0,
            "p2_sla_target_hours": 4.0,
            "total_sow_value_inr": total_sow_value,
            "total_billed_inr": total_billed,
            "total_received_inr": total_received,
            "outstanding_receivable_inr": outstanding_receivable,
            "milestones_total": milestones_total,
            "milestones_completed": milestones_completed,
            "milestones_progress_pct": milestones_progress_pct,
            "open_sla_tickets_count": open_sla_tickets,
            "sla_breaches_count": 0,
            "client_csat_score": 4.9,
            "active_sprint_name": "Sprint 14: Automated Reconciliation & ITSM Self-Healing"
        },
        "active_projects": [
            {
                "id": p.id,
                "code": p.project_code,
                "name": p.name,
                "manager": p.project_manager,
                "budget": p.budget_inr,
                "status": p.status,
                "dates": f"{p.start_date} to {p.target_end_date}",
                "start_date": str(p.start_date),
                "target_end_date": str(p.target_end_date)
            } for p in projects
        ],
        "project_milestones": [
            {
                "id": m.id,
                "project_id": m.project_id,
                "name": m.milestone_name,
                "target_date": str(m.target_date),
                "deliverable_summary": m.deliverable_summary,
                "payment_linked_percent": m.payment_linked_percent,
                "billing_amount": m.billing_amount,
                "status": m.status,
                "completion_date": str(m.completion_date) if m.completion_date else None,
                "signoff_by": m.signoff_by,
                "signoff_at": m.signoff_at.isoformat() if m.signoff_at else None,
                "signoff_notes": m.signoff_notes,
                "acceptance_criteria": m.acceptance_criteria
            } for m in milestones
        ],
        "billing_invoices": [
            {
                "id": i.id,
                "number": i.invoice_number,
                "date": str(i.invoice_date),
                "due_date": str(i.due_date) if i.due_date else None,
                "project_ref": i.project_ref,
                "customer_gstin": i.customer_gstin,
                "taxable": i.taxable_value,
                "cgst": i.cgst_amount,
                "sgst": i.sgst_amount,
                "igst": i.igst_amount,
                "tax": i.total_tax,
                "total": i.total_invoice_value,
                "received": i.amount_received,
                "balance": i.outstanding_balance,
                "status": i.status,
                "payment_terms": i.payment_terms
            } for i in invoices
        ],
        "sla_tickets": [
            {
                "id": t.id,
                "ticket_number": t.ticket_number,
                "severity": t.severity,
                "category": t.category,
                "subject": t.subject,
                "description": t.description,
                "status": t.status,
                "sla_hours": t.sla_response_hours,
                "sla_deadline": t.sla_deadline.isoformat() if t.sla_deadline else None,
                "assigned_engineer": t.assigned_engineer,
                "resolution_summary": t.resolution_summary,
                "csat_rating": t.csat_rating,
                "created_at": str(t.created_at)
            } for t in tickets
        ],
        "change_orders": [
            {
                "id": cr.id,
                "cr_number": cr.cr_number,
                "title": cr.title,
                "reason": cr.reason,
                "scope_impact": cr.scope_impact,
                "cost_impact_inr": cr.cost_impact_inr,
                "schedule_impact_days": cr.schedule_impact_days,
                "status": cr.status,
                "approver": cr.approver,
                "decision_date": str(cr.decision_date) if cr.decision_date else None,
                "created_at": str(cr.created_at)
            } for cr in change_orders
        ],
        "contracts_and_agreements": [
            {
                "id": c.id,
                "contract_reference": c.contract_reference,
                "contract_type": c.contract_type,
                "effective_date": str(c.effective_date),
                "expiry_date": str(c.expiry_date) if c.expiry_date else None,
                "value_inr": c.value_inr,
                "status": c.status,
                "stamp_duty_paid": c.stamp_duty_paid,
                "governing_law": c.governing_law,
                "ip_ownership_clause": c.ip_ownership_clause,
                "special_conditions": c.special_conditions
            } for c in contracts
        ],
        "wbs_tasks": [
            {
                "id": w.id,
                "code": w.wbs_code,
                "name": w.task_name,
                "assignee": w.assigned_to,
                "sprint": w.sprint_phase,
                "estimated_hours": w.estimated_hours,
                "actual_hours": w.actual_hours,
                "status": w.status,
                "priority": w.priority
            } for w in wbs_tasks
        ]
    }


@router.post("/client/tickets", status_code=201)
def create_client_ticket(req: ClientTicketCreateRequest, db: Session = Depends(get_db)):
    """
    Submits an official client SLA support ticket with automatic SLA deadline calculation.
    """
    sla_map = {
        "P1-Critical": 1.0,
        "P2-High": 4.0,
        "P3-Medium": 12.0,
        "P4-Low": 24.0
    }
    sla_hours = sla_map.get(req.severity, 12.0)
    deadline = datetime.utcnow() + timedelta(hours=sla_hours)
    ticket_num = f"ADT-SRV-2026-{uuid.uuid4().hex[:4].upper()}"

    ticket = SupportTicket(
        ticket_number=ticket_num,
        client_name=req.client_name,
        contact_email=req.contact_email,
        subject=req.subject,
        description=req.description,
        category=req.category,
        severity=req.severity,
        sla_response_hours=sla_hours,
        sla_deadline=deadline,
        assigned_engineer="DevOps & SRE Lead",
        status="Open"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "status": "success",
        "message": f"SLA support ticket {ticket_num} logged successfully with {sla_hours}h SLA commitment.",
        "ticket": {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "severity": ticket.severity,
            "sla_response_hours": ticket.sla_response_hours,
            "sla_deadline": ticket.sla_deadline.isoformat(),
            "status": ticket.status
        }
    }


@router.post("/client/milestones/{milestone_id}/signoff")
def signoff_client_milestone(milestone_id: int, req: ClientMilestoneSignoffRequest, db: Session = Depends(get_db)):
    """
    Submits formal client UAT acceptance sign-off for a project milestone deliverable.
    """
    milestone = db.query(ProjectMilestone).filter(ProjectMilestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Project milestone not found.")

    milestone.status = req.approval_status
    if req.approval_status == "Client Approved":
        milestone.completion_date = date.today()
    milestone.signoff_by = req.client_signatory_name
    milestone.signoff_at = datetime.utcnow()
    milestone.signoff_notes = req.acceptance_notes

    db.commit()
    db.refresh(milestone)

    return {
        "status": "success",
        "message": f"Milestone '{milestone.milestone_name}' sign-off successfully recorded by {req.client_signatory_name}.",
        "milestone_id": milestone.id,
        "status_now": milestone.status,
        "signoff_by": milestone.signoff_by,
        "signoff_at": milestone.signoff_at.isoformat() if milestone.signoff_at else None
    }


@router.post("/client/change-requests/{cr_id}/review")
def review_client_change_request(cr_id: int, req: ClientChangeRequestReview, db: Session = Depends(get_db)):
    """
    Records formal client review, approval, or rejection of a project change request (CR).
    """
    cr = db.query(ChangeRequest).filter(ChangeRequest.id == cr_id).first()
    if not cr:
        raise HTTPException(status_code=404, detail="Change request not found.")

    if req.action.upper() == "APPROVE":
        cr.status = "Client Approved"
        cr.approver = f"{req.client_approver_name} (Client Authority)"
        cr.decision_date = date.today()
        # Optionally update project budget if linked
        if cr.project and cr.cost_impact_inr:
            cr.project.budget_inr = (cr.project.budget_inr or 0.0) + cr.cost_impact_inr
    else:
        cr.status = "Rejected"
        cr.approver = f"{req.client_approver_name} (Client Authority)"
        cr.decision_date = date.today()

    db.commit()
    db.refresh(cr)

    return {
        "status": "success",
        "message": f"Change request {cr.cr_number} has been set to '{cr.status}' by {req.client_approver_name}.",
        "cr_number": cr.cr_number,
        "status_now": cr.status,
        "approver": cr.approver
    }


@router.post("/client/invoices/{invoice_id}/record-payment")
def record_client_invoice_payment(invoice_id: int, req: ClientPaymentRecordRequest, db: Session = Depends(get_db)):
    """
    Records a wire transfer / NEFT / RTGS payment against an outstanding commercial B2B invoice.
    """
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Commercial invoice not found.")

    inv.amount_received = (inv.amount_received or 0.0) + req.amount_inr
    inv.outstanding_balance = max(0.0, (inv.total_invoice_value or 0.0) - inv.amount_received)
    if inv.outstanding_balance <= 0.0:
        inv.status = "Paid"
    else:
        inv.status = "Partially Paid"

    db.commit()
    db.refresh(inv)

    return {
        "status": "success",
        "message": f"Payment of INR {req.amount_inr:,.2f} recorded for Invoice {inv.invoice_number} (Ref: {req.payment_reference}).",
        "invoice_number": inv.invoice_number,
        "amount_received": inv.amount_received,
        "outstanding_balance": inv.outstanding_balance,
        "status_now": inv.status
    }


@router.get("/client/invoices/{invoice_id}/html", response_class=HTMLResponse)
def get_client_invoice_html(invoice_id: int, db: Session = Depends(get_db)):
    """
    Generates a formal, printable B2B Tax Invoice document with Asperion corporate seal,
    GSTIN compliance, itemized SAC 998314 billing, and Director Varadi Vijay signature.
    """
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    cgst_rate = "9.0%" if inv.cgst_amount and inv.cgst_amount > 0 else "0.0%"
    sgst_rate = "9.0%" if inv.sgst_amount and inv.sgst_amount > 0 else "0.0%"
    igst_rate = "18.0%" if inv.igst_amount and inv.igst_amount > 0 else "0.0%"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tax Invoice - {inv.invoice_number}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            background: #f8fafc;
            margin: 0;
            padding: 30px;
        }}
        .invoice-card {{
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .company-title {{
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
        }}
        .meta-text {{
            font-size: 11px;
            color: #64748b;
            line-height: 1.5;
            margin-top: 4px;
        }}
        .invoice-badge {{
            text-align: right;
        }}
        .invoice-title {{
            font-size: 24px;
            font-weight: 900;
            color: #2563eb;
            letter-spacing: 0.5px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 25px;
            font-size: 12px;
        }}
        .panel {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
        }}
        .panel-title {{
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 25px;
        }}
        th {{
            background: #0f172a;
            color: #ffffff;
            text-align: left;
            padding: 10px 12px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .text-right {{
            text-align: right;
        }}
        .totals-table {{
            width: 340px;
            margin-left: auto;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 25px;
        }}
        .totals-table td {{
            padding: 6px 12px;
            border: none;
        }}
        .totals-table tr.grand-total {{
            border-top: 2px solid #0f172a;
            border-bottom: 2px solid #0f172a;
            font-weight: 800;
            font-size: 14px;
            color: #0f172a;
            background: #f1f5f9;
        }}
        .signatory-section {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px dashed #cbd5e1;
        }}
        .bank-details {{
            font-size: 11px;
            color: #475569;
            line-height: 1.6;
        }}
        .signatory-box {{
            text-align: right;
        }}
        .stamp-box {{
            display: inline-block;
            border: 2px solid #0284c7;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            line-height: 70px;
            text-align: center;
            font-size: 9px;
            font-weight: 800;
            color: #0284c7;
            transform: rotate(-12deg);
            margin-bottom: 10px;
        }}
        .print-btn {{
            display: block;
            margin: 0 auto 20px auto;
            background: #0f172a;
            color: #fff;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        @media print {{
            body {{ background: #fff; padding: 0; }}
            .invoice-card {{ border: none; box-shadow: none; padding: 0; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>

    <div class="invoice-card">
        <div class="header">
            <div>
                <div class="company-title">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div class="meta-text">
                    <strong>CIN:</strong> U85500KA2026OPC222069 &bull; <strong>GSTIN:</strong> 29AABCU9603R1ZM &bull; <strong>PAN:</strong> AABCU9603R<br>
                    <strong>Registered Office:</strong> Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu,<br>
                    Bangalore North, Bangalore - 560043, Karnataka, India<br>
                    <strong>Corporate Email:</strong> finance@asperion.in &bull; <strong>Director:</strong> Varadi Vijay
                </div>
            </div>
            <div class="invoice-badge">
                <div class="invoice-title">TAX INVOICE</div>
                <div style="font-family: monospace; font-weight: 700; font-size: 13px; color: #334155; margin-top: 4px;">{inv.invoice_number}</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Original for Recipient</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="panel">
                <div class="panel-title">Billed To (Client Customer)</div>
                <div style="font-weight: 700; font-size: 13px; color: #0f172a;">{inv.customer_name}</div>
                <div style="margin-top: 4px; color: #475569;">
                    <strong>GSTIN / UIN:</strong> {inv.customer_gstin or '29AABCZ9988P1Z5'}<br>
                    <strong>State / Code:</strong> {inv.place_of_supply or 'Karnataka (29)'}<br>
                    <strong>Client SOW Reference:</strong> {inv.project_ref or 'ADT-PRJ-2026-002'}
                </div>
            </div>
            <div class="panel">
                <div class="panel-title">Invoice & Payment Terms</div>
                <div style="color: #475569; line-height: 1.6;">
                    <strong>Invoice Date:</strong> {inv.invoice_date.strftime('%d-%b-%Y') if inv.invoice_date else 'N/A'}<br>
                    <strong>Due Date:</strong> {inv.due_date.strftime('%d-%b-%Y') if inv.due_date else 'Net 30 Days'}<br>
                    <strong>Payment Terms:</strong> {inv.payment_terms or 'Net 30 Days'}<br>
                    <strong>Payment Status:</strong> <span style="font-weight: 700; color: {'#059669' if inv.status == 'Paid' else '#d97706'};">{inv.status}</span>
                </div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 50%;">Description of Services</th>
                    <th style="width: 15%; text-align: center;">HSN / SAC</th>
                    <th style="width: 15%; text-align: right;">Rate (INR)</th>
                    <th style="width: 15%; text-align: right;">Amount (INR)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>
                        <strong>Enterprise Software Architecture & Agile Sprint Delivery</strong><br>
                        <span style="font-size: 11px; color: #64748b;">Milestone deliverable execution, cloud microservices, and 24x7 SLA support under active Master Services Agreement.</span>
                    </td>
                    <td style="text-align: center; font-family: monospace;">998314</td>
                    <td class="text-right font-mono">₹{inv.taxable_value:,.2f}</td>
                    <td class="text-right font-mono"><strong>₹{inv.taxable_value:,.2f}</strong></td>
                </tr>
            </tbody>
        </table>

        <table class="totals-table">
            <tr>
                <td>Taxable Subtotal:</td>
                <td class="text-right">₹{inv.taxable_value:,.2f}</td>
            </tr>
            <tr>
                <td>Central GST (CGST @ {cgst_rate}):</td>
                <td class="text-right">₹{inv.cgst_amount or 0.0:,.2f}</td>
            </tr>
            <tr>
                <td>State GST (SGST @ {sgst_rate}):</td>
                <td class="text-right">₹{inv.sgst_amount or 0.0:,.2f}</td>
            </tr>
            {f'<tr><td>Integrated GST (IGST @ {igst_rate}):</td><td class="text-right">₹{inv.igst_amount:,.2f}</td></tr>' if inv.igst_amount and inv.igst_amount > 0 else ''}
            <tr class="grand-total">
                <td>Grand Total (INR):</td>
                <td class="text-right">₹{inv.total_invoice_value:,.2f}</td>
            </tr>
            <tr>
                <td>Amount Received:</td>
                <td class="text-right" style="color: #059669; font-weight: 700;">₹{inv.amount_received or 0.0:,.2f}</td>
            </tr>
            <tr>
                <td>Balance Due:</td>
                <td class="text-right" style="color: {'#dc2626' if (inv.outstanding_balance or 0.0) > 0 else '#059669'}; font-weight: 800;">₹{inv.outstanding_balance or 0.0:,.2f}</td>
            </tr>
        </table>

        <div class="signatory-section">
            <div class="bank-details">
                <strong>Electronic Remittance Instructions (NEFT / RTGS):</strong><br>
                Bank Name: ICICI Bank Limited<br>
                Account Name: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED<br>
                Account Number: 000205001234<br>
                IFSC Code: ICIC0000002<br>
                Branch: Bangalore Corporate Banking Branch
            </div>
            <div class="signatory-box">
                <div class="stamp-box">ASPERION<br>SEAL</div>
                <div style="font-weight: 800; font-size: 13px; color: #0f172a;">Varadi Vijay</div>
                <div style="font-size: 11px; color: #64748b;">Founder & Sole Director</div>
                <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html)


@router.get("/client/statement-of-account", response_class=HTMLResponse)
def get_client_statement_of_account_html(client_name: str = "Zenith Global Corp", db: Session = Depends(get_db)):
    """
    Generates a formal, printable Statement of Account (SOA) showing the ledger
    of all billed invoices, payments received, and running outstanding balances.
    """
    clean_name = client_name.strip()
    search_prefix = clean_name[:6]

    invoices = db.query(Invoice).filter(Invoice.customer_name.ilike(f"%{search_prefix}%")).order_by(Invoice.invoice_date.asc()).all()
    if not invoices:
        invoices = db.query(Invoice).order_by(Invoice.invoice_date.asc()).limit(10).all()

    total_billed = sum(i.total_invoice_value for i in invoices if i.total_invoice_value)
    total_received = sum(i.amount_received for i in invoices if i.amount_received)
    outstanding_bal = sum(i.outstanding_balance for i in invoices if i.outstanding_balance)

    rows_html = ""
    running_balance = 0.0

    for idx, inv in enumerate(invoices, 1):
        running_balance += (inv.total_invoice_value or 0.0)
        rows_html += f"""
        <tr>
            <td>{inv.invoice_date.strftime('%d-%b-%Y') if inv.invoice_date else 'N/A'}</td>
            <td style="font-family: monospace; font-weight: 700;">{inv.invoice_number}</td>
            <td>Tax Invoice - Software Architecture & Milestone Delivery</td>
            <td style="text-align: right; font-weight: 700;">₹{inv.total_invoice_value:,.2f}</td>
            <td style="text-align: right; color: #64748b;">-</td>
            <td style="text-align: right; font-weight: 700;">₹{running_balance:,.2f}</td>
        </tr>
        """
        if inv.amount_received and inv.amount_received > 0:
            running_balance -= inv.amount_received
            rows_html += f"""
            <tr style="background: #f0fdf4;">
                <td>{(inv.invoice_date + timedelta(days=15)).strftime('%d-%b-%Y') if inv.invoice_date else 'N/A'}</td>
                <td style="font-family: monospace; color: #059669;">PAY-REC-{inv.id:04d}</td>
                <td style="color: #059669;">Client Wire Remittance (NEFT / RTGS)</td>
                <td style="text-align: right; color: #64748b;">-</td>
                <td style="text-align: right; color: #059669; font-weight: 700;">₹{inv.amount_received:,.2f}</td>
                <td style="text-align: right; font-weight: 700;">₹{running_balance:,.2f}</td>
            </tr>
            """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Statement of Account - {client_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            background: #f8fafc;
            margin: 0;
            padding: 30px;
        }}
        .soa-card {{
            max-width: 880px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .company-title {{
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
        }}
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}
        .kpi-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .kpi-label {{
            font-size: 11px;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
        }}
        .kpi-value {{
            font-size: 20px;
            font-weight: 800;
            margin-top: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-bottom: 30px;
        }}
        th {{
            background: #0f172a;
            color: #ffffff;
            text-align: left;
            padding: 10px;
            font-size: 11px;
            text-transform: uppercase;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .signatory {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
            font-size: 12px;
        }}
        .print-btn {{
            display: block;
            margin: 0 auto 20px auto;
            background: #0f172a;
            color: #fff;
            padding: 10px 24px;
            border-radius: 8px;
            border: none;
            font-weight: 700;
            cursor: pointer;
        }}
        @media print {{
            body {{ background: #fff; padding: 0; }}
            .soa-card {{ border: none; box-shadow: none; padding: 0; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Print Statement</button>
    <div class="soa-card">
        <div class="header">
            <div>
                <div class="company-title">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">
                    CIN: U85500KA2026OPC222069 &bull; GSTIN: 29AABCU9603R1ZM &bull; Horamavu, Bangalore - 560043, Karnataka
                </div>
                <div style="margin-top: 10px; font-size: 13px;">
                    <strong>Statement For:</strong> <span style="font-weight: 800; color: #0f172a;">{client_name}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 20px; font-weight: 900; color: #0284c7;">STATEMENT OF ACCOUNT</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 2px;">As on {datetime.utcnow().strftime('%d-%b-%Y')}</div>
            </div>
        </div>

        <div class="kpi-row">
            <div class="kpi-box">
                <div class="kpi-label">Total Billed</div>
                <div class="kpi-value" style="color: #0f172a;">₹{total_billed:,.2f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Total Remitted</div>
                <div class="kpi-value" style="color: #059669;">₹{total_received:,.2f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Current Outstanding Due</div>
                <div class="kpi-value" style="color: {'#dc2626' if outstanding_bal > 0 else '#059669'};">₹{outstanding_bal:,.2f}</div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th style="width: 14%;">Date</th>
                    <th style="width: 20%;">Ref / Transaction #</th>
                    <th style="width: 32%;">Description</th>
                    <th style="width: 11%; text-align: right;">Debit (INR)</th>
                    <th style="width: 11%; text-align: right;">Credit (INR)</th>
                    <th style="width: 12%; text-align: right;">Balance (INR)</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="signatory">
            <div>
                <strong>Payment Remittance:</strong> ICICI Bank &bull; A/C: 000205001234 &bull; IFSC: ICIC0000002<br>
                <span style="font-size: 11px; color: #64748b;">Subject to Bengaluru Jurisdiction. Computer-generated official corporate ledger statement.</span>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 800; color: #0f172a;">Varadi Vijay</div>
                <div style="font-size: 11px; color: #64748b;">Founder & Sole Director</div>
                <div style="font-size: 10px; color: #94a3b8;">Asperion Digital Technologies</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html)

# ==============================================================================
# 3. VENDOR SOURCING, POS & INWARD GRN PORTAL
# ==============================================================================

@router.get("/vendor/dashboard-data")
def get_vendor_portal_data(
    vendor_id: Optional[int] = None,
    vendor_name: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # 1. Resolve selected vendor or default to first/Nexus
    query = db.query(Vendor)
    if vendor_id:
        v = query.filter(Vendor.id == vendor_id).first()
    elif vendor_name:
        v = query.filter(Vendor.vendor_name.ilike(f"%{vendor_name[:5]}%")).first()
    else:
        v = query.filter(Vendor.vendor_code == "ADT-VEN-002").first() or query.first()

    all_vendors = db.query(Vendor).filter(Vendor.is_active == True).order_by(Vendor.vendor_code.asc()).all()
    vendors_list = [
        {
            "id": item.id,
            "vendor_code": item.vendor_code,
            "vendor_name": item.vendor_name,
            "category": item.category,
            "criticality_tier": item.criticality_tier,
            "msme_registered": item.msme_registered,
            "msme_category": getattr(item, "msme_category", "Micro"),
            "rating": getattr(item, "rating", 92.5)
        } for item in all_vendors
    ]

    target_vid = v.id if v else 0
    target_vname = v.vendor_name if v else "Nexus Micro Systems Pvt Ltd"

    # 2. Query POs, GRNs, AP Bills, Contracts, Bids, Scorecards
    pos = db.query(PurchaseOrder).filter(
        (PurchaseOrder.vendor_id == target_vid) | (PurchaseOrder.vendor_name == target_vname)
    ).order_by(PurchaseOrder.po_date.desc()).all()
    if not pos and not vendor_id:
        pos = db.query(PurchaseOrder).order_by(PurchaseOrder.po_date.desc()).limit(10).all()

    grns = db.query(GoodsReceivedNote).filter(
        GoodsReceivedNote.vendor_id == target_vid
    ).order_by(GoodsReceivedNote.received_date.desc()).all()
    if not grns and not vendor_id:
        grns = db.query(GoodsReceivedNote).order_by(GoodsReceivedNote.received_date.desc()).limit(10).all()

    bills = db.query(APBill).filter(
        APBill.vendor_name == target_vname
    ).order_by(APBill.bill_date.desc()).all()
    if not bills and not vendor_id:
        bills = db.query(APBill).order_by(APBill.bill_date.desc()).limit(10).all()

    contracts = db.query(VendorContract).filter(
        VendorContract.vendor_id == target_vid
    ).order_by(VendorContract.effective_date.desc()).all()

    scorecards = db.query(VendorScorecard).filter(
        VendorScorecard.vendor_id == target_vid
    ).order_by(VendorScorecard.created_at.desc()).all()

    risks = db.query(VendorRiskAssessment).filter(
        VendorRiskAssessment.vendor_id == target_vid
    ).order_by(VendorRiskAssessment.review_date.desc()).all()

    capas = db.query(VendorCorrectiveActionPlan).filter(
        (VendorCorrectiveActionPlan.vendor_id == target_vid) | (VendorCorrectiveActionPlan.vendor_name == target_vname)
    ).order_by(VendorCorrectiveActionPlan.created_at.desc()).all()

    # Active Sourcing Events relevant to vendor's category
    v_category = v.category if v else "Cloud & Infrastructure"
    rfx_events = db.query(StrategicSourcingEvent).filter(
        StrategicSourcingEvent.status.in_(["Published / Open", "Technical Evaluation", "Commercial BAFO"])
    ).order_by(StrategicSourcingEvent.closing_date.asc()).all()

    bids = db.query(VendorBidSubmission).filter(
        (VendorBidSubmission.vendor_id == target_vid) | (VendorBidSubmission.vendor_name == target_vname)
    ).all()
    bids_by_event = {b.event_id: b for b in bids}

    # 3. Compute Executive KPIs
    total_po_val = sum(p.total_amount for p in pos)
    active_pos_count = sum(1 for p in pos if p.status in ["Approved", "In Transit", "Partial GRN Inward"])
    total_ap_billed = sum(b.net_payable for b in bills)
    pending_3way = sum(1 for b in bills if b.three_way_match_status != "Matched")
    msme_priority = v.msme_registered if v else False

    # 4. Format detailed payloads
    today = date.today()

    def parse_po_items(raw_json: Optional[str]) -> List[Dict[str, Any]]:
        if not raw_json:
            return []
        try:
            return json.loads(raw_json)
        except Exception:
            return [{"item": str(raw_json), "qty": 1, "rate": 0.0, "amount": 0.0}]

    formatted_pos = [
        {
            "id": p.id,
            "po_number": p.po_number,
            "date": str(p.po_date),
            "po_date": str(p.po_date),
            "delivery_due_date": str(p.delivery_due_date) if p.delivery_due_date else None,
            "vendor_name": p.vendor_name,
            "project_code": p.project_code or "ADT-GEN-2026",
            "amount": p.total_amount,
            "total_amount": p.total_amount,
            "status": p.status,
            "payment_terms": getattr(p, "payment_terms", "Net 30 Days"),
            "delivery_challan_no": getattr(p, "delivery_challan_no", None),
            "items": parse_po_items(getattr(p, "items_json", None)),
            "html_url": f"/api/v1/portals/vendor/po/document?po_number={p.po_number}"
        } for p in pos
    ]

    formatted_grns = [
        {
            "id": g.id,
            "grn_number": g.grn_number,
            "po_reference": g.po_reference,
            "delivery_challan_no": g.delivery_challan_no or "DC-PENDING",
            "received_date": str(getattr(g, "received_date", getattr(g, "grn_date", today))),
            "item_description": g.item_description,
            "quantity_ordered": getattr(g, "quantity_ordered", 1.0),
            "quantity_received": getattr(g, "quantity_received", 1.0),
            "quantity_accepted": getattr(g, "quantity_accepted", 1.0),
            "quantity_rejected": getattr(g, "quantity_rejected", 0.0),
            "inspection_status": g.inspection_status,
            "inspected_by": g.inspected_by or "IT Admin",
            "warehouse_location": getattr(g, "warehouse_location", "Horamavu Bangalore HQ"),
            "rejection_reason": getattr(g, "rejection_reason", None),
            "rtv_credit_note_ref": getattr(g, "rtv_credit_note_ref", None),
            "remarks": g.remarks,
            "certificate_url": f"/api/v1/portals/vendor/grn/{g.grn_number}/html"
        } for g in grns
    ]

    formatted_bills = [
        {
            "id": b.id,
            "bill_number": b.bill_number,
            "bill_date": str(b.bill_date),
            "due_date": str(b.due_date),
            "days_remaining": (b.due_date - today).days if b.due_date else 0,
            "po_reference": b.po_reference or "--",
            "grn_reference": b.grn_reference or "--",
            "expense_category": b.expense_category or "Procurement",
            "taxable_amount": b.taxable_amount,
            "gst_amount": getattr(b, "gst_amount", 0.0),
            "tds_section": getattr(b, "tds_section", "194C"),
            "tds_rate_pct": round(getattr(b, "tds_rate", 0.02) * 100, 1),
            "tds_amount": b.tds_amount,
            "net_payable": b.net_payable,
            "three_way_match_status": b.three_way_match_status,
            "approval_status": b.approval_status,
            "payment_reference": getattr(b, "payment_reference", None)
        } for b in bills
    ]

    formatted_rfx = [
        {
            "id": ev.id,
            "event_code": ev.event_code,
            "title": ev.title,
            "event_type": ev.event_type,
            "category": ev.category,
            "budget_allocation_inr": ev.budget_allocation_inr,
            "closing_date": str(ev.closing_date),
            "status": ev.status,
            "my_bid": {
                "bid_code": bids_by_event[ev.id].bid_code,
                "quote_inr": bids_by_event[ev.id].commercial_quote_inr,
                "composite_score": bids_by_event[ev.id].composite_score,
                "award_status": bids_by_event[ev.id].award_status
            } if ev.id in bids_by_event else None
        } for ev in rfx_events
    ]

    formatted_contracts = [
        {
            "id": c.id,
            "contract_reference": c.contract_reference,
            "agreement_type": c.agreement_type,
            "effective_date": str(c.effective_date),
            "expiry_date": str(c.expiry_date) if c.expiry_date else None,
            "annual_value_inr": c.annual_value_inr,
            "sla_uptime_commitment": c.sla_uptime_commitment,
            "dpdp_dpa_signed": c.data_protection_annexure,
            "auto_renew": c.auto_renew_enabled,
            "status": c.status
        } for c in contracts
    ]

    formatted_scorecards = [
        {
            "id": s.id,
            "evaluation_period": s.evaluation_period,
            "quality_score": s.quality_score,
            "sla_adherence_score": s.sla_adherence_score,
            "pricing_competitiveness": s.pricing_competitiveness,
            "security_privacy_score": s.security_privacy_score,
            "overall_rating": s.overall_rating,
            "performance_tier": s.performance_tier,
            "qbr_action_items": s.qbr_action_items
        } for s in scorecards
    ]

    return {
        "entity": {
            "name": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            "cin": "U85500KA2026OPC222069",
            "registered_office": "Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore - 560043, Karnataka",
            "gstin": "29AABCA1234D1Z1",
            "pan": "AABCA1234D"
        },
        "vendors_list": vendors_list,
        "vendor_profile": {
            "id": v.id if v else 0,
            "vendor_code": v.vendor_code if v else "VND-NEXUS-01",
            "vendor_name": v.vendor_name if v else "Nexus Micro Systems Pvt Ltd",
            "contact_person": v.contact_person if v else "Rohan Deshmukh",
            "email": v.email if v else "enterprise@nexusmicrosystems.in",
            "phone": v.phone if v else "+91 80 4123 9800",
            "category": v.category if v else "Hardware & Workstations",
            "criticality_tier": v.criticality_tier if v else "Tier 2 - High",
            "pan": v.pan if v else "AABCN5678E",
            "gstin": v.gstin if v else "29AABCN5678E1Z4",
            "duns_number": getattr(v, "duns_number", "91-456-7890"),
            "bank_account_number": getattr(v, "bank_account_number", "50200088991122"),
            "bank_ifsc": getattr(v, "bank_ifsc", "HDFC0001234"),
            "bank_name": getattr(v, "bank_name", "HDFC Bank Koramangala"),
            "msme_registered": msme_priority,
            "msme_udyam_number": v.msme_udyam_number if v else "UDYAM-KR-03-0091823",
            "msme_category": getattr(v, "msme_category", "Micro"),
            "msme_payment_due_days": getattr(v, "msme_payment_due_days", 45),
            "kyc_status": v.kyc_status if v else "Approved & Verified",
            "dpdp_compliance_status": v.dpdp_compliance_status if v else "Compliant",
            "payment_terms_days": v.payment_terms_days if v else 30,
            "rating": getattr(v, "rating", 94.2)
        },
        "kpis": {
            "active_pos_count": active_pos_count,
            "total_po_value_inr": total_po_val,
            "grns_logged_count": len(grns),
            "pending_3way_matching_count": pending_3way,
            "total_ap_billed_inr": total_ap_billed,
            "msme_priority_eligible": msme_priority,
            "overall_performance_rating": getattr(v, "rating", 94.2)
        },
        "purchase_orders": formatted_pos,
        "inward_grns": formatted_grns,
        "ap_bills": formatted_bills,
        "sourcing_rfx_events": formatted_rfx,
        "contracts": formatted_contracts,
        "scorecards": formatted_scorecards,
        "capas": [
            {
                "id": cap.id,
                "capa_code": cap.capa_code,
                "issue_description": cap.issue_description,
                "root_cause": cap.root_cause,
                "corrective_action_agreed": cap.corrective_action_agreed,
                "target_closure_date": str(cap.target_closure_date),
                "status": cap.status
            } for cap in capas
        ],
        "vendor_name": v.vendor_name if v else "Nexus Micro Systems Pvt Ltd",
        "vendor_code": v.vendor_code if v else "VND-NEXUS-01",
        "msme_registration": v.msme_udyam_number if v else "UDYAM-KR-03-0091823",
        "payment_terms": f"Net {v.payment_terms_days if v else 30} Days",
        "kyc_status": v.kyc_status if v else "Approved & Verified",
        "submitted_bills": [
            {
                "bill_number": b.bill_number,
                "date": str(b.bill_date),
                "taxable": b.taxable_amount,
                "tds": b.tds_amount,
                "net_payable": b.net_payable,
                "match_status": b.three_way_match_status,
                "status": b.approval_status
            } for b in bills
        ],
        "goods_received_notes": [
            {
                "grn_number": g.grn_number,
                "date": str(getattr(g, "received_date", getattr(g, "grn_date", today))),
                "inspection": g.inspection_status,
                "accepted": getattr(g, "quantity_accepted", 1.0)
            } for g in grns
        ]
    }


# ==============================================================================
# 4. INWARD GOODS RECEIVED NOTE (GRN) CREATION & 3-WAY MATCH ENGINE
# ==============================================================================

@router.post("/vendor/inward-grn")
def create_portal_inward_grn(
    grn_in: PortalInwardGRNCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.id == grn_in.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor record not found")

    # Generate unique GRN number
    year = datetime.utcnow().year
    count = db.query(GoodsReceivedNote).count() + 1
    grn_number = f"ADT-GRN-{year}-{count:03d}"

    # Calculate rejected quantity if not explicitly given
    qty_rej = grn_in.quantity_rejected
    if qty_rej == 0.0 and grn_in.quantity_received > grn_in.quantity_accepted:
        qty_rej = grn_in.quantity_received - grn_in.quantity_accepted

    grn = GoodsReceivedNote(
        grn_number=grn_number,
        vendor_id=vendor.id,
        po_reference=grn_in.po_reference,
        delivery_challan_no=grn_in.delivery_challan_no or f"DC-{vendor.vendor_code}-{count:03d}",
        received_date=grn_in.received_date,
        item_description=grn_in.item_description,
        quantity_ordered=grn_in.quantity_ordered,
        quantity_received=grn_in.quantity_received,
        quantity_accepted=grn_in.quantity_accepted,
        quantity_rejected=qty_rej,
        inspection_status=grn_in.inspection_status,
        inspected_by=grn_in.inspected_by,
        warehouse_location=grn_in.warehouse_location,
        rejection_reason=grn_in.rejection_reason,
        rtv_credit_note_ref=grn_in.rtv_credit_note_ref,
        remarks=grn_in.remarks
    )
    db.add(grn)
    db.flush()

    # Update Linked Purchase Order Status
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == grn_in.po_reference).first()
    if po:
        po.delivery_challan_no = grn.delivery_challan_no
        if grn_in.quantity_accepted >= grn_in.quantity_ordered and grn_in.inspection_status == "Accepted":
            po.status = "Fulfilled"
        elif grn_in.inspection_status == "Partial Rejection":
            po.status = "Partial GRN Inward"
        elif grn_in.inspection_status == "Rejected":
            po.status = "GRN Inspection Failed"

    # Automated 3-Way Match Check on Pending AP Bills
    matching_bills = db.query(APBill).filter(APBill.po_reference == grn_in.po_reference).all()
    for bill in matching_bills:
        bill.grn_reference = grn.grn_number
        if grn.inspection_status == "Accepted":
            bill.three_way_match_status = "Matched"
        else:
            bill.three_way_match_status = "Discrepancy"

    db.commit()
    db.refresh(grn)

    return {
        "status": "SUCCESS",
        "message": f"Inward Goods Received Note {grn.grn_number} registered & verified against PO {grn.po_reference}.",
        "grn_number": grn.grn_number,
        "po_reference": grn.po_reference,
        "inspection_status": grn.inspection_status,
        "accepted_quantity": grn.quantity_accepted,
        "certificate_url": f"/api/v1/portals/vendor/grn/{grn.grn_number}/html"
    }


# ==============================================================================
# 5. VENDOR BILL SUBMISSION WITH 3-WAY MATCHING & CHAPTER XVII-B TDS
# ==============================================================================

@router.post("/vendor/ap-bill")
def submit_portal_vendor_bill(
    bill_in: PortalVendorBillSubmit,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.vendor_name == bill_in.vendor_name).first()
    
    # Statutory Chapter XVII-B TDS calculation
    tds_rate = 0.02 # default 2%
    if bill_in.tds_section == "194C":
        # Under 194C: 1% for Individual/HUF, 2% for Corporate/LLP
        is_corporate = vendor and ("pvt" in vendor.vendor_name.lower() or "ltd" in vendor.vendor_name.lower() or "llp" in vendor.vendor_name.lower())
        tds_rate = 0.02 if is_corporate else 0.01
    elif bill_in.tds_section == "194J":
        # Under 194J: 2% for technical services, 10% for professional fees
        tds_rate = 0.02 if "hosting" in bill_in.expense_category.lower() or "cloud" in bill_in.expense_category.lower() else 0.10

    tds_amt = round(bill_in.taxable_amount * tds_rate, 2)
    net_payable = round(bill_in.taxable_amount + bill_in.gst_amount - tds_amt, 2)

    # Statutory Payment Due Date under MSMED Act 2006 (Section 15: max 45 days)
    terms_days = vendor.payment_terms_days if vendor else 30
    if vendor and vendor.msme_registered:
        terms_days = min(terms_days, getattr(vendor, "msme_payment_due_days", 45))
    
    due_date = bill_in.due_date or (bill_in.bill_date + timedelta(days=terms_days))

    # Automated 3-Way Match Verification
    match_status = "Pending 3-Way Match"
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == bill_in.po_reference).first() if bill_in.po_reference else None
    grn = db.query(GoodsReceivedNote).filter(
        (GoodsReceivedNote.po_reference == bill_in.po_reference) | (GoodsReceivedNote.grn_number == bill_in.grn_reference)
    ).first() if bill_in.po_reference or bill_in.grn_reference else None

    if po and grn and grn.inspection_status == "Accepted":
        match_status = "Matched"
    elif po and not grn:
        match_status = "Pending GRN"
    elif not po:
        match_status = "Discrepancy - Missing PO"

    bill = APBill(
        bill_number=bill_in.bill_number,
        bill_date=bill_in.bill_date,
        due_date=due_date,
        vendor_name=bill_in.vendor_name,
        po_reference=bill_in.po_reference,
        grn_reference=bill_in.grn_reference or (grn.grn_number if grn else None),
        three_way_match_status=match_status,
        expense_category=bill_in.expense_category,
        taxable_amount=bill_in.taxable_amount,
        gst_amount=bill_in.gst_amount,
        tds_section=bill_in.tds_section,
        tds_rate=tds_rate,
        tds_amount=tds_amt,
        net_payable=net_payable,
        approval_status="Pending Finance Approval" if match_status == "Matched" else "Under Discrepancy Review"
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)

    return {
        "status": "SUCCESS",
        "bill_number": bill.bill_number,
        "net_payable": bill.net_payable,
        "tds_deducted": bill.tds_amount,
        "tds_section": f"Section {bill.tds_section} ({int(tds_rate * 100)}%)",
        "three_way_match_status": bill.three_way_match_status,
        "statutory_due_date": str(bill.due_date),
        "msme_priority": vendor.msme_registered if vendor else False
    }


# ==============================================================================
# 6. E-RFX SOURCING BID SUBMISSION
# ==============================================================================

@router.post("/vendor/rfx-bid")
def submit_portal_rfx_bid(
    bid_in: PortalRFXBidSubmit,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    ev = db.query(StrategicSourcingEvent).filter(StrategicSourcingEvent.id == bid_in.event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Sourcing event not found")

    vendor = db.query(Vendor).filter(Vendor.id == bid_in.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    # Commercial weight calculation (relative to budget)
    comm_score = 90.0
    if ev.budget_allocation_inr > 0:
        ratio = bid_in.commercial_quote_inr / ev.budget_allocation_inr
        comm_score = max(50.0, min(100.0, 100.0 - (ratio - 0.8) * 50.0))

    composite = round(
        (bid_in.technical_score * (ev.technical_weight_pct / 100.0)) +
        (comm_score * (ev.commercial_weight_pct / 100.0)) +
        (bid_in.compliance_score * (ev.compliance_security_weight_pct / 100.0)) +
        ((bid_in.sla_guarantee_pct / 100.0 * 100.0) * (ev.sla_weight_pct / 100.0)),
        2
    )

    year = datetime.utcnow().year
    count = db.query(VendorBidSubmission).count() + 1
    bid_code = f"ADT-BID-{year}-{count:03d}"

    bid = VendorBidSubmission(
        bid_code=bid_code,
        event_id=ev.id,
        vendor_id=vendor.id,
        vendor_name=vendor.vendor_name,
        technical_score=bid_in.technical_score,
        commercial_quote_inr=bid_in.commercial_quote_inr,
        compliance_score=bid_in.compliance_score,
        sla_guarantee_pct=bid_in.sla_guarantee_pct,
        composite_score=composite,
        is_shortlisted=True if composite >= 85.0 else False,
        award_status="Submitted",
        notes=bid_in.notes
    )
    db.add(bid)
    db.commit()
    db.refresh(bid)

    return {
        "status": "SUCCESS",
        "bid_code": bid.bid_code,
        "event_code": ev.event_code,
        "composite_score": bid.composite_score,
        "is_shortlisted": bid.is_shortlisted,
        "message": f"Bid {bid.bid_code} submitted successfully for event {ev.event_code}."
    }


# ==============================================================================
# 7. OFFICIAL PURCHASE ORDER (PO) PRINTABLE HTML DOCUMENT
# ==============================================================================

def render_purchase_order_html(po_number: str, db: Session) -> HTMLResponse:
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == po_number).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    vendor = db.query(Vendor).filter(
        (Vendor.id == po.vendor_id) | (Vendor.vendor_name == po.vendor_name)
    ).first()

    raw_items = []
    if getattr(po, "items_json", None):
        try:
            raw_items = json.loads(po.items_json)
        except Exception:
            raw_items = [{"item": str(po.items_json), "qty": 1, "rate": po.total_amount, "amount": po.total_amount}]
    else:
        raw_items = [{"item": "Enterprise Goods / Managed IT Services as per SOW", "qty": 1, "rate": po.total_amount, "amount": po.total_amount}]

    items_html = ""
    subtotal = 0.0
    for idx, itm in enumerate(raw_items, start=1):
        q = float(itm.get("qty", 1))
        r = float(itm.get("rate", po.total_amount))
        amt = float(itm.get("amount", q * r))
        subtotal += amt
        hsn = itm.get("hsn") or itm.get("sac") or "84713010"
        items_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px 12px; font-family: monospace; color: #475569;">{idx:02d}</td>
            <td style="padding: 10px 12px;">
                <div style="font-weight: 600; color: #0f172a;">{itm.get('item', 'Item')}</div>
                <div style="font-size: 11px; color: #64748b;">HSN/SAC: {hsn}</div>
            </td>
            <td style="padding: 10px 12px; text-align: center; font-weight: 600;">{q}</td>
            <td style="padding: 10px 12px; text-align: right; font-family: monospace;">₹{r:,.2f}</td>
            <td style="padding: 10px 12px; text-align: right; font-family: monospace; font-weight: 700; color: #0f172a;">₹{amt:,.2f}</td>
        </tr>
        """

    gst_amt = round(subtotal * 0.18, 2)
    grand_total = round(subtotal + gst_amt, 2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Purchase Order — {po.po_number}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 30px; }}
        .doc-container {{ max-width: 850px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
        .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; border-bottom: 2px solid #0f172a; padding-bottom: 16px; }}
        .po-title {{ font-size: 26px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; text-align: right; text-transform: uppercase; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e0f2fe; color: #0369a1; }}
        .meta-grid {{ display: flex; justify-content: space-between; margin-bottom: 28px; gap: 20px; }}
        .meta-card {{ flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; font-size: 12px; line-height: 1.6; }}
        .items-table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 24px; }}
        .items-table th {{ background: #0f172a; color: #ffffff; text-align: left; padding: 10px 12px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .totals-table {{ width: 320px; margin-left: auto; border-collapse: collapse; font-size: 13px; margin-bottom: 30px; }}
        .totals-table td {{ padding: 6px 10px; }}
        .footer {{ font-size: 11px; color: #64748b; line-height: 1.6; border-top: 1px solid #e2e8f0; padding-top: 16px; margin-top: 30px; }}
        .print-btn {{ background: #0f172a; color: #ffffff; padding: 8px 16px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; float: right; margin-bottom: 15px; }}
        @media print {{ .print-btn {{ display: none; }} body {{ padding: 0; background: #ffffff; }} .doc-container {{ border: none; box-shadow: none; padding: 0; }} }}
    </style>
</head>
<body>
    <div style="max-width: 850px; margin: 0 auto;">
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
    <div class="doc-container">
        <table class="header-table">
            <tr>
                <td style="vertical-align: top;">
                    <table style="border: none; border-collapse: collapse; margin: 0; padding: 0;">
                        <tr>
                            <td style="vertical-align: middle; padding-right: 14px; border: none;">
                                <img src="/static/img/logo.png" alt="Asperion Logo" style="width: 58px; height: 58px; border-radius: 50%; object-fit: contain; background: #0f172a; padding: 2px; border: 1.5px solid #38bdf8;">
                            </td>
                            <td style="vertical-align: middle; border: none; padding: 0;">
                                <div style="font-size: 17px; font-weight: 800; color: #0f172a;">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                                <div style="font-size: 11px; font-family: monospace; color: #475569; margin-top: 2px;">CIN: U85500KA2026OPC222069 | GSTIN: 29AABCA1234D1Z1</div>
                                <div style="font-size: 10px; color: #64748b; margin-top: 2px;">
                                    Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu,<br>
                                    Bangalore North, Bangalore - 560043, Karnataka, India
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
                <td style="text-align: right; vertical-align: top;">
                    <div class="po-title">Purchase Order</div>
                    <div style="font-family: monospace; font-size: 14px; font-weight: 700; color: #2563eb; margin-top: 4px;">{po.po_number}</div>
                    <div style="margin-top: 6px;"><span class="badge">{po.status}</span></div>
                </td>
            </tr>
        </table>

        <div class="meta-grid">
            <div class="meta-card">
                <div style="font-weight: 700; color: #0f172a; text-transform: uppercase; font-size: 10px; margin-bottom: 6px; letter-spacing: 0.5px;">Vendor / Supplier (Party)</div>
                <div style="font-size: 14px; font-weight: 700; color: #0f172a;">{vendor.vendor_name if vendor else po.vendor_name}</div>
                <div>Code: <strong>{vendor.vendor_code if vendor else 'VND-SUPPLIER'}</strong> &bull; Tier: {vendor.criticality_tier if vendor else 'Standard'}</div>
                <div>GSTIN: <strong>{vendor.gstin if vendor else '29AABCN5678E1Z4'}</strong> &bull; PAN: {vendor.pan if vendor else 'AABCN5678E'}</div>
                <div>MSME Udyam: <strong>{vendor.msme_udyam_number if vendor and vendor.msme_registered else 'N/A'}</strong></div>
                <div>Contact: {vendor.contact_person if vendor else 'Sales & Dispatch'} ({vendor.email if vendor else 'sales@vendor.com'})</div>
            </div>
            <div class="meta-card">
                <div style="font-weight: 700; color: #0f172a; text-transform: uppercase; font-size: 10px; margin-bottom: 6px; letter-spacing: 0.5px;">Order & Shipping Metadata</div>
                <div>PO Date: <strong>{po.po_date}</strong></div>
                <div>Delivery Due Date: <strong>{po.delivery_due_date or 'Immediate / 7 Days'}</strong></div>
                <div>Payment Terms: <strong>{getattr(po, 'payment_terms', 'Net 30 Days')}</strong></div>
                <div>Project Code: <strong>{po.project_code or 'ADT-PRJ-2026-01'}</strong></div>
                <div>Ship-To Address: <strong>Horamavu Bangalore HQ (Type 4, Lakshith Props)</strong></div>
            </div>
        </div>

        <table class="items-table">
            <thead>
                <tr>
                    <th style="width: 40px;">#</th>
                    <th>Item Description & Specifications</th>
                    <th style="width: 60px; text-align: center;">Qty</th>
                    <th style="width: 120px; text-align: right;">Unit Rate</th>
                    <th style="width: 130px; text-align: right;">Amount (INR)</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>

        <table class="totals-table">
            <tr>
                <td style="color: #64748b;">Taxable Subtotal:</td>
                <td style="text-align: right; font-family: monospace; font-weight: 600;">₹{subtotal:,.2f}</td>
            </tr>
            <tr>
                <td style="color: #64748b;">Applicable GST (18%):</td>
                <td style="text-align: right; font-family: monospace; font-weight: 600;">₹{gst_amt:,.2f}</td>
            </tr>
            <tr style="border-top: 2px solid #0f172a; border-bottom: 2px solid #0f172a;">
                <td style="font-weight: 800; font-size: 14px; color: #0f172a;">Total Order Value:</td>
                <td style="text-align: right; font-family: monospace; font-weight: 800; font-size: 15px; color: #0f172a;">₹{grand_total:,.2f}</td>
            </tr>
        </table>

        <div style="margin-top: 30px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div style="font-size: 11px; color: #475569; max-width: 480px; line-height: 1.5;">
                <strong>Statutory Terms & Conditions:</strong><br>
                1. Delivery Challan and Tax Invoice must quote this PO number.<br>
                2. Goods subject to 100% inward QA inspection and serial number logging.<br>
                3. MSME suppliers eligible for statutory Section 15 priority clearance within 45 days.<br>
                4. Governed by Indian Law and subject to exclusive jurisdiction of Bengaluru courts.
            </div>
            <div style="text-align: center; border-top: 1px solid #94a3b8; width: 220px; padding-top: 6px;">
                <div style="font-size: 12px; font-weight: 700; color: #0f172a;">Varadi Vijay</div>
                <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Founder & Sole Director</div>
                <div style="font-size: 9px; color: #2563eb; font-weight: 600;">Authorized Signatory &bull; Digitally Signed</div>
            </div>
        </div>

        <div class="footer">
            Asperion Enterprise Operating System &bull; Official Procurement Document &bull; Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html)


@router.get("/vendor/po/document", response_class=HTMLResponse)
def get_purchase_order_document_by_query(po_number: str = Query(...), db: Session = Depends(get_db)):
    return render_purchase_order_html(po_number, db)


@router.get("/vendor/po/{po_number:path}", response_class=HTMLResponse)
def get_purchase_order_document_by_path(po_number: str, db: Session = Depends(get_db)):
    return render_purchase_order_html(po_number, db)

# Alias for testing and callers
get_purchase_order_html = render_purchase_order_html



# ==============================================================================
# 8. GOODS RECEIVED NOTE (GRN) & QA INSPECTION CERTIFICATE PRINTABLE HTML
# ==============================================================================

@router.get("/vendor/grn/{grn_number}/html", response_class=HTMLResponse)
def get_goods_received_note_html(grn_number: str, db: Session = Depends(get_db)):
    grn = db.query(GoodsReceivedNote).filter(GoodsReceivedNote.grn_number == grn_number).first()
    if not grn:
        raise HTTPException(status_code=404, detail="Goods Received Note not found")

    vendor = db.query(Vendor).filter(Vendor.id == grn.vendor_id).first()
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == grn.po_reference).first()

    status_color = "#059669" if grn.inspection_status == "Accepted" else ("#d97706" if grn.inspection_status == "Partial Rejection" else "#dc2626")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Inward GRN & Inspection Certificate — {grn.grn_number}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 30px; }}
        .doc-container {{ max-width: 850px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
        .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; border-bottom: 2px solid #0f172a; padding-bottom: 16px; }}
        .meta-grid {{ display: flex; justify-content: space-between; margin-bottom: 24px; gap: 20px; }}
        .meta-card {{ flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; font-size: 12px; line-height: 1.6; }}
        .quantities-table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 24px; }}
        .quantities-table th {{ background: #0f172a; color: #ffffff; padding: 10px 12px; font-size: 11px; text-transform: uppercase; }}
        .quantities-table td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; }}
        .seal-box {{ display: inline-block; border: 2px dashed {status_color}; padding: 8px 16px; border-radius: 8px; color: {status_color}; font-weight: 800; font-size: 13px; text-transform: uppercase; }}
        .print-btn {{ background: #0f172a; color: #ffffff; padding: 8px 16px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; float: right; margin-bottom: 15px; }}
        @media print {{ .print-btn {{ display: none; }} body {{ padding: 0; background: #ffffff; }} .doc-container {{ border: none; box-shadow: none; padding: 0; }} }}
    </style>
</head>
<body>
    <div style="max-width: 850px; margin: 0 auto;">
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
    <div class="doc-container">
        <table class="header-table">
            <tr>
                <td style="vertical-align: top;">
                    <table style="border: none; border-collapse: collapse; margin: 0; padding: 0;">
                        <tr>
                            <td style="vertical-align: middle; padding-right: 14px; border: none;">
                                <img src="/static/img/logo.png" alt="Asperion Logo" style="width: 58px; height: 58px; border-radius: 50%; object-fit: contain; background: #0f172a; padding: 2px; border: 1.5px solid #0284c7;">
                            </td>
                            <td style="vertical-align: middle; border: none; padding: 0;">
                                <div style="font-size: 17px; font-weight: 800; color: #0f172a;">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                                <div style="font-size: 11px; font-family: monospace; color: #475569; margin-top: 2px;">CIN: U85500KA2026OPC222069 | QA & Inbound Logistics</div>
                                <div style="font-size: 10px; color: #64748b; margin-top: 2px;">
                                    Warehouse & Quality Inspection Hub: Flat No.304, Type 4, Lakshith Properties, Horamavu, Bangalore - 560043
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
                <td style="text-align: right; vertical-align: top;">
                    <div style="font-size: 22px; font-weight: 800; color: #0f172a; text-transform: uppercase;">Goods Received Note</div>
                    <div style="font-family: monospace; font-size: 14px; font-weight: 700; color: #0284c7; margin-top: 4px;">{grn.grn_number}</div>
                    <div style="margin-top: 6px;"><div class="seal-box">{grn.inspection_status}</div></div>
                </td>
            </tr>
        </table>

        <div class="meta-grid">
            <div class="meta-card">
                <div style="font-weight: 700; color: #0f172a; text-transform: uppercase; font-size: 10px; margin-bottom: 6px;">Consignor / Supplier Details</div>
                <div style="font-size: 14px; font-weight: 700; color: #0f172a;">{vendor.vendor_name if vendor else 'Vendor Partner'}</div>
                <div>Vendor Code: <strong>{vendor.vendor_code if vendor else 'VND-001'}</strong></div>
                <div>GSTIN: <strong>{vendor.gstin if vendor else '29AABCN5678E1Z4'}</strong></div>
                <div>Delivery Challan Ref: <strong>{grn.delivery_challan_no or 'DC-UNKNOWN'}</strong></div>
            </div>
            <div class="meta-card">
                <div style="font-weight: 700; color: #0f172a; text-transform: uppercase; font-size: 10px; margin-bottom: 6px;">Inward Gate & Verification Audit</div>
                <div>Received Date: <strong>{grn.received_date}</strong></div>
                <div>Linked Purchase Order: <strong>{grn.po_reference}</strong></div>
                <div>Inspection Location: <strong>{getattr(grn, 'warehouse_location', 'Horamavu Bangalore HQ')}</strong></div>
                <div>Lead Inspector: <strong>{grn.inspected_by}</strong></div>
            </div>
        </div>

        <table class="quantities-table">
            <thead>
                <tr>
                    <th style="text-align: left;">Item Description & Specifications</th>
                    <th style="text-align: center; width: 100px;">Ordered</th>
                    <th style="text-align: center; width: 100px;">Received</th>
                    <th style="text-align: center; width: 100px;">Accepted</th>
                    <th style="text-align: center; width: 100px;">Rejected</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <div style="font-weight: 700; color: #0f172a;">{grn.item_description}</div>
                        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Remarks: {grn.remarks or 'Serial numbers recorded and matched with delivery challan.'}</div>
                    </td>
                    <td style="text-align: center; font-weight: 700; font-family: monospace;">{grn.quantity_ordered}</td>
                    <td style="text-align: center; font-weight: 700; font-family: monospace;">{grn.quantity_received}</td>
                    <td style="text-align: center; font-weight: 700; font-family: monospace; color: #059669;">{grn.quantity_accepted}</td>
                    <td style="text-align: center; font-weight: 700; font-family: monospace; color: #dc2626;">{getattr(grn, 'quantity_rejected', 0.0)}</td>
                </tr>
            </tbody>
        </table>

        {f'<div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 12px; margin-bottom: 24px; font-size: 12px; color: #991b1b;"><strong>Rejection Note:</strong> {grn.rejection_reason} &bull; RTV Credit Note Ref: {grn.rtv_credit_note_ref}</div>' if getattr(grn, 'rejection_reason', None) else ''}

        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 14px; margin-bottom: 24px; font-size: 12px; color: #166534; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <strong>3-Way Match Verification Posture:</strong><br>
                PO Reference ({grn.po_reference}) matched with Delivery Challan ({grn.delivery_challan_no}). Ready for AP Bill reconciliation.
            </div>
            <div style="font-size: 20px;">🛡️ ✅</div>
        </div>

        <div style="margin-top: 30px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div style="font-size: 11px; color: #64748b; max-width: 450px;">
                <strong>Quality Assurance Statement:</strong><br>
                Inspected under ISO 9001:2015 Clause 8.4 and ISO/IEC 27001 A.15 Supply Chain standards. Physical integrity, tamper seals, and technical specifications verified.
            </div>
            <div style="text-align: center; border-top: 1px solid #94a3b8; width: 220px; padding-top: 6px;">
                <div style="font-size: 12px; font-weight: 700; color: #0f172a;">{grn.inspected_by}</div>
                <div style="font-size: 10px; color: #64748b; text-transform: uppercase;">Quality Assurance / Store Lead</div>
                <div style="font-size: 9px; color: #059669; font-weight: 600;">Inspection Certified</div>
            </div>
        </div>

        <div style="font-size: 11px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 14px; margin-top: 24px;">
            Asperion Enterprise Operating System &bull; Goods Received Note &bull; Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html)

