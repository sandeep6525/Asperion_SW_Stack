"""
Asperion Enterprise OS - Attendance, Biometric & WhatsApp REST API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.models.attendance import GeofenceZone, AttendanceRecord, AttendanceAnomalyLog
from app.models.hrms import Employee
from app.schemas.attendance import (
    GeofenceZoneCreate, GeofenceZoneOut, ClockInRequest, ClockOutRequest,
    WhatsAppWebhookPayload, AttendanceRecordOut, AttendanceAnomalyLogOut,
    AttendanceDailySummaryOut, AutoFixResponse
)
from app.engines.attendance_engine import (
    evaluate_geofence, verify_facial_recognition, calculate_work_hours_and_status,
    auto_fix_and_self_heal_anomalies, process_whatsapp_attendance
)

router = APIRouter(prefix="/attendance", tags=["Smart Attendance & Workforce Tracking Hub"])

@router.post("/clock-in", response_model=AttendanceRecordOut, status_code=201)
def api_clock_in(req: ClockInRequest, db: Session = Depends(get_db)):
    """
    Records employee clock-in with GPS geofencing and facial recognition verification.
    """
    emp = db.query(Employee).filter(Employee.id == req.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = date.today()
    now = datetime.utcnow()

    # Check if already clocked in today
    att = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id,
        AttendanceRecord.attendance_date == today
    ).first()

    if att and att.clock_in_time:
        raise HTTPException(status_code=400, detail="Employee has already clocked in today")

    # Geofence & Facial Verification
    geo_ok, zone_code, dist = evaluate_geofence(db, req.latitude, req.longitude)
    face_ok, match_pct, live_ok = verify_facial_recognition(req.selfie_base64_or_hash, emp.emp_code)

    if not att:
        att = AttendanceRecord(
            employee_id=emp.id,
            attendance_date=today,
            clock_in_time=now,
            in_source=req.source,
            in_latitude=req.latitude,
            in_longitude=req.longitude,
            geofence_verified=geo_ok,
            geofence_zone_code=zone_code,
            geofence_distance_meters=dist,
            facial_recognition_verified=face_ok,
            facial_match_confidence_pct=match_pct,
            facial_liveness_verified=live_ok,
            status="Present"
        )
        db.add(att)
    else:
        att.clock_in_time = now
        att.in_source = req.source
        att.in_latitude = req.latitude
        att.in_longitude = req.longitude
        att.geofence_verified = geo_ok
        att.geofence_zone_code = zone_code
        att.geofence_distance_meters = dist
        att.facial_recognition_verified = face_ok
        att.facial_match_confidence_pct = match_pct
        att.facial_liveness_verified = live_ok

    db.commit()
    db.refresh(att)
    return att

@router.post("/clock-out", response_model=AttendanceRecordOut)
def api_clock_out(req: ClockOutRequest, db: Session = Depends(get_db)):
    """
    Records employee clock-out, auto-calculates shift hours, and updates attendance status.
    """
    emp = db.query(Employee).filter(Employee.id == req.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = date.today()
    now = datetime.utcnow()

    att = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id,
        AttendanceRecord.attendance_date == today
    ).first()

    if not att or not att.clock_in_time:
        raise HTTPException(status_code=400, detail="No active clock-in found for today. Please clock in first.")

    calc = calculate_work_hours_and_status(att.clock_in_time, now)

    att.clock_out_time = now
    att.out_source = req.source
    att.out_latitude = req.latitude
    att.out_longitude = req.longitude
    att.total_work_hours = calc["total_work_hours"]
    att.effective_work_hours = calc["effective_work_hours"]
    att.status = calc["status"]
    att.updated_at = now

    db.commit()
    db.refresh(att)
    return att

@router.post("/whatsapp-webhook")
def api_whatsapp_webhook(payload: WhatsAppWebhookPayload, db: Session = Depends(get_db)):
    """
    Simulates incoming Meta WhatsApp Cloud API workforce attendance webhook.
    """
    res = process_whatsapp_attendance(
        db=db,
        phone_number=payload.phone_number,
        message_body=payload.message_body,
        lat=payload.latitude,
        lon=payload.longitude,
        media_url=payload.media_url
    )
    return res

@router.post("/auto-fix-anomalies", response_model=AutoFixResponse)
def api_auto_fix_anomalies(db: Session = Depends(get_db)):
    """
    Triggers self-healing attendance algorithm to auto-regularize missing punches.
    """
    return auto_fix_and_self_heal_anomalies(db=db)

@router.get("/records", response_model=List[AttendanceRecordOut])
def list_attendance_records(
    employee_id: Optional[int] = None,
    target_date: Optional[date] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AttendanceRecord)
    if employee_id:
        query = query.filter(AttendanceRecord.employee_id == employee_id)
    if target_date:
        query = query.filter(AttendanceRecord.attendance_date == target_date)
    if status and status != "ALL":
        query = query.filter(AttendanceRecord.status == status)

    return query.order_by(AttendanceRecord.attendance_date.desc(), AttendanceRecord.id.desc()).all()

@router.get("/daily-summary", response_model=AttendanceDailySummaryOut)
def get_daily_attendance_summary(target_date: Optional[date] = None, db: Session = Depends(get_db)):
    """
    Computes real-time daily presence, late marks, biometric compliance %, and auto-healed counts.
    """
    t_date = target_date or date.today()
    employees = db.query(Employee).filter(Employee.employment_status == "Active").all()
    total_emp = len(employees)

    records = db.query(AttendanceRecord).filter(AttendanceRecord.attendance_date == t_date).all()
    
    present = sum(1 for r in records if r.status in ["Present", "Late Mark", "Half Day", "Regularized"])
    leave = sum(1 for r in records if r.status == "On Leave")
    late = sum(1 for r in records if r.status == "Late Mark")
    wfh = sum(1 for r in records if r.geofence_verified == False and r.clock_in_time is not None)
    
    face_verified = sum(1 for r in records if r.facial_recognition_verified)
    bio_comp = round((face_verified / len(records)) * 100, 1) if records else 100.0
    auto_healed = sum(1 for r in records if r.auto_fixed)

    return AttendanceDailySummaryOut(
        status="success",
        date=t_date,
        total_employees=total_emp,
        present_count=present,
        on_leave_count=leave,
        late_marks_count=late,
        wfh_count=wfh,
        biometric_compliance_pct=bio_comp,
        auto_healed_today_count=auto_healed,
        records=records
    )

@router.get("/geofences", response_model=List[GeofenceZoneOut])
def list_geofences(db: Session = Depends(get_db)):
    return db.query(GeofenceZone).all()

@router.post("/geofences", response_model=GeofenceZoneOut, status_code=201)
def create_geofence(zone_in: GeofenceZoneCreate, db: Session = Depends(get_db)):
    exists = db.query(GeofenceZone).filter(GeofenceZone.zone_code == zone_in.zone_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Geofence zone code already exists")
    
    zone = GeofenceZone(**zone_in.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone

@router.get("/anomalies", response_model=List[AttendanceAnomalyLogOut])
def list_attendance_anomalies(db: Session = Depends(get_db)):
    return db.query(AttendanceAnomalyLog).order_by(AttendanceAnomalyLog.id.desc()).all()
