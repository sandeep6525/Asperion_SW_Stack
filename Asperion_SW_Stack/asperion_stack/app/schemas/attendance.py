"""
Asperion Enterprise OS - Attendance, Biometric & WhatsApp Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class GeofenceZoneBase(BaseModel):
    zone_code: str
    zone_name: str
    latitude: float
    longitude: float
    radius_meters: float = 250.0
    zone_type: str = "Registered Office"
    address: Optional[str] = None
    is_active: bool = True

class GeofenceZoneCreate(GeofenceZoneBase):
    pass

class GeofenceZoneOut(GeofenceZoneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ClockInRequest(BaseModel):
    employee_id: int
    source: str = "WEB" # WEB, WHATSAPP, MOBILE_APP, FACIAL_KIOSK
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    selfie_base64_or_hash: Optional[str] = None
    device_info: Optional[str] = None

class ClockOutRequest(BaseModel):
    employee_id: int
    source: str = "WEB"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class WhatsAppWebhookPayload(BaseModel):
    phone_number: str = Field(..., description="E.164 phone number, e.g. +919876543210")
    message_body: str = Field(..., description="Message text, e.g. 'IN', 'OUT', 'STATUS'")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    media_url: Optional[str] = None

class AttendanceAnomalyLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    anomaly_type: str
    severity: str
    detected_at: datetime
    auto_healed: bool
    action_taken: Optional[str] = None
    resolved_by: str

class AttendanceRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    attendance_date: date
    clock_in_time: Optional[datetime] = None
    clock_out_time: Optional[datetime] = None
    total_work_hours: float
    effective_work_hours: float
    status: str
    in_source: str
    out_source: Optional[str] = None
    in_latitude: Optional[float] = None
    in_longitude: Optional[float] = None
    geofence_verified: bool
    geofence_zone_code: Optional[str] = None
    geofence_distance_meters: Optional[float] = None
    facial_recognition_verified: bool
    facial_match_confidence_pct: float
    facial_liveness_verified: bool
    is_anomalous: bool
    anomaly_reason: Optional[str] = None
    auto_fixed: bool
    auto_fix_summary: Optional[str] = None
    regularization_notes: Optional[str] = None
    created_at: datetime

class AttendanceDailySummaryOut(BaseModel):
    status: str
    date: date
    total_employees: int
    present_count: int
    on_leave_count: int
    late_marks_count: int
    wfh_count: int
    biometric_compliance_pct: float
    auto_healed_today_count: int
    records: List[AttendanceRecordOut]

class AutoFixResponse(BaseModel):
    status: str
    scanned_records_count: int
    auto_fixed_count: int
    details: List[str]
