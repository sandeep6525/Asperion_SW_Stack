"""
Unit & Integration Tests for Smart Attendance, WhatsApp Webhook, Geofencing,
Biometric Facial Recognition, and Self-Healing Error Auto-Fixing Engine.
"""
import pytest
from datetime import datetime, date, time
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.hrms import Employee
from app.models.attendance import GeofenceZone, AttendanceRecord, AttendanceAnomalyLog, WhatsAppAttendanceSession
from app.engines.attendance_engine import (
    haversine_distance, evaluate_geofence, verify_facial_recognition,
    calculate_work_hours_and_status, auto_fix_and_self_heal_anomalies,
    process_whatsapp_attendance
)
from app.api.attendance import (
    api_clock_in, api_clock_out, api_whatsapp_webhook, api_auto_fix_anomalies,
    get_daily_attendance_summary, list_attendance_records, list_geofences
)
from app.schemas.attendance import ClockInRequest, ClockOutRequest, WhatsAppWebhookPayload

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    yield session
    session.close()

def test_haversine_distance_calculation():
    # Distance between Horamavu HQ and nearby point (approx 111 meters north: 0.001 deg latitude)
    lat1, lon1 = 13.035820, 77.653410
    lat2, lon2 = 13.036820, 77.653410
    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert 100.0 < dist < 120.0
    
    # Distance to self must be 0
    assert haversine_distance(lat1, lon1, lat1, lon1) == 0.0

def test_evaluate_geofence(db):
    # Within HQ perimeter
    is_inside, zone_code, distance = evaluate_geofence(db, 13.035825, 77.653412)
    assert is_inside is True
    assert zone_code == "GEO-BLR-HQ"
    assert distance < 50.0

    # Outside perimeter (e.g. 50 km away in Bangalore outskirts)
    is_inside_far, _, dist_far = evaluate_geofence(db, 12.500000, 77.100000)
    assert is_inside_far is False
    assert dist_far > 1000.0

def test_facial_recognition_biometric_engine():
    # Returns (verified, confidence_pct, liveness_passed) tuple
    verified, conf_pct, live_ok = verify_facial_recognition("valid_biometric_selfie_base64_payload", "ADT-EMP-001")
    assert verified is True
    assert conf_pct >= 90.0
    assert live_ok is True

    # Empty payload defaults to standard web check
    ver_web, conf_web, live_web = verify_facial_recognition("", "ADT-EMP-001")
    assert ver_web is True
    assert conf_web >= 90.0

def test_work_hours_calculation():
    # Full day (9 hours from 09:00 to 18:00)
    t_in = datetime(2026, 6, 15, 9, 0, 0)
    t_out = datetime(2026, 6, 15, 18, 0, 0)
    calc = calculate_work_hours_and_status(t_in, t_out)
    assert calc["total_work_hours"] == 9.0
    assert calc["effective_work_hours"] == 8.25  # 0.75h deduction for > 5h
    assert calc["status"] == "Present"
    assert calc["is_late"] is False

    # Half day (4.5 hours from 09:00 to 13:30)
    t_out_half = datetime(2026, 6, 15, 13, 30, 0)
    calc_half = calculate_work_hours_and_status(t_in, t_out_half)
    assert calc_half["status"] == "Half Day"

def test_api_clock_in_facial_and_geofence(db):
    emp = db.query(Employee).first()
    assert emp is not None

    # Clean existing today's record for clean test run
    db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id,
        AttendanceRecord.attendance_date == date.today()
    ).delete()
    db.commit()

    payload = ClockInRequest(
        employee_id=emp.id,
        source="FACIAL_KIOSK",
        latitude=13.035820,
        longitude=77.653410,
        selfie_base64_or_hash="simulated_selfie_image_stream"
    )
    rec = api_clock_in(payload, db=db)
    assert rec.geofence_verified is True
    assert rec.facial_recognition_verified is True
    assert rec.facial_match_confidence_pct >= 90.0
    assert rec.status in ["Present", "Late Mark"]

def test_api_clock_out(db):
    emp = db.query(Employee).first()
    payload = ClockOutRequest(
        employee_id=emp.id,
        source="FACIAL_KIOSK",
        latitude=13.035820,
        longitude=77.653410
    )
    rec = api_clock_out(payload, db=db)
    assert rec.clock_out_time is not None
    assert rec.total_work_hours >= 0.0

def test_api_whatsapp_webhook(db):
    emp = db.query(Employee).first()
    emp.phone = "+919886099999"
    db.commit()

    # Clear today's record to test WhatsApp check-in
    db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id,
        AttendanceRecord.attendance_date == date.today()
    ).delete()
    db.commit()

    wa_payload = WhatsAppWebhookPayload(
        phone_number="+919886099999",
        message_body="IN",
        latitude=13.035820,
        longitude=77.653410
    )
    res = api_whatsapp_webhook(wa_payload, db=db)
    assert res["status"] == "success"
    assert "Clock-IN Recorded" in res["reply_message"]

def test_api_auto_fix_and_self_heal_engine(db):
    res = api_auto_fix_anomalies(db=db)
    assert "auto_fixed_count" in res
    assert "scanned_records_count" in res
    assert isinstance(res["details"], list)

def test_api_daily_attendance_summary(db):
    summary = get_daily_attendance_summary(None, db=db)
    assert summary.total_employees >= 1
    assert summary.present_count >= 1
    assert summary.biometric_compliance_pct >= 0.0
