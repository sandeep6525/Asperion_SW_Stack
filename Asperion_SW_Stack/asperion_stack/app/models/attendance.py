"""
Asperion Enterprise OS - Smart Attendance, WhatsApp Webhook, Biometric Facial Recognition & Geofencing Models
Part of Module 04 (HRMS & People Operations)
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GeofenceZone(Base):
    """
    Approved Geofence perimeters for physical office and verified client sites.
    HQ: Lakshith Properties, Horamavu, Bangalore - 560043 (13.0358, 77.6534).
    """
    __tablename__ = "geofence_zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_code = Column(String(50), unique=True, index=True, nullable=False) # GEO-HQ-01, GEO-CLIENT-01
    zone_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False) # e.g. 13.035820
    longitude = Column(Float, nullable=False) # e.g. 77.653410
    radius_meters = Column(Float, default=250.0) # Geofence radius tolerance
    zone_type = Column(String(50), default="Registered Office") # Registered Office, Client Site, Co-Working, WFH Approved
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AttendanceRecord(Base):
    """
    Daily biometric and multi-modal attendance log.
    Captures facial match confidence, GPS coordinates, WhatsApp check-ins, and self-healing auto-fix states.
    """
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), index=True, nullable=False)
    attendance_date = Column(Date, index=True, nullable=False)
    
    clock_in_time = Column(DateTime, nullable=True)
    clock_out_time = Column(DateTime, nullable=True)
    total_work_hours = Column(Float, default=0.0)
    effective_work_hours = Column(Float, default=0.0)
    
    status = Column(String(50), default="Present", index=True) # Present, Half Day, Late Mark, Early Exit, Absent, Regularized
    in_source = Column(String(50), default="WEB") # WEB, WHATSAPP, MOBILE_APP, FACIAL_KIOSK, AUTO_FIX
    out_source = Column(String(50), nullable=True)
    
    # Location & Geofencing
    in_latitude = Column(Float, nullable=True)
    in_longitude = Column(Float, nullable=True)
    out_latitude = Column(Float, nullable=True)
    out_longitude = Column(Float, nullable=True)
    geofence_verified = Column(Boolean, default=False)
    geofence_zone_code = Column(String(50), nullable=True)
    geofence_distance_meters = Column(Float, nullable=True)
    
    # Biometric Facial Recognition
    facial_recognition_verified = Column(Boolean, default=False)
    facial_match_confidence_pct = Column(Float, default=0.0) # 0.0 to 100.0%
    facial_liveness_verified = Column(Boolean, default=False)
    selfie_image_url = Column(String(255), nullable=True)
    
    # WhatsApp Integration
    whatsapp_message_id = Column(String(100), nullable=True)
    
    # Auto-Fixing & Self-Healing Anomalies
    is_anomalous = Column(Boolean, default=False)
    anomaly_reason = Column(String(255), nullable=True) # e.g. Missing Clock Out, Outside Geofence
    auto_fixed = Column(Boolean, default=False)
    auto_fix_summary = Column(Text, nullable=True)
    regularization_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee")
    anomalies = relationship("AttendanceAnomalyLog", back_populates="attendance", cascade="all, delete-orphan")

class AttendanceAnomalyLog(Base):
    """
    Self-healing anomaly audit log.
    Tracks detection and resolution of missing punches, GPS drift, and facial recognition discrepancies.
    """
    __tablename__ = "attendance_anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance_records.id"), index=True, nullable=False)
    anomaly_type = Column(String(50), nullable=False) # MISSING_CLOCK_OUT, GEOFENCE_BREACH, FACIAL_CONFIDENCE_LOW, TIME_DRIFT
    severity = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW
    detected_at = Column(DateTime, default=datetime.utcnow)
    auto_healed = Column(Boolean, default=False)
    action_taken = Column(Text, nullable=True)
    resolved_by = Column(String(100), default="Asperion Self-Healing Engine")

    attendance = relationship("AttendanceRecord", back_populates="anomalies")

class WhatsAppAttendanceSession(Base):
    """
    Active conversational state for Meta WhatsApp Cloud API workforce attendance.
    """
    __tablename__ = "whatsapp_attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. +919876543210
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    last_message_text = Column(String(255), nullable=True)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    session_state = Column(String(50), default="AWAITING_COMMAND") # AWAITING_COMMAND, AWAITING_LOCATION, AWAITING_SELFIE, CONFIRMED
    pending_clock_action = Column(String(20), nullable=True) # IN or OUT
    
    employee = relationship("Employee")
