"""
Asperion Enterprise OS - HRMS & Payroll Schemas
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class CTCCalculatorRequest(BaseModel):
    annual_ctc: float
    basic_pct: float = 0.40
    hra_pct: float = 0.40
    state: str = "Karnataka"
    cap_pf_at_ceiling: bool = True
    include_gratuity: bool = True

class CandidateCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    applied_role: str
    department: str = "Engineering"
    experience_years: float = 0.0
    expected_ctc: float = 0.0
    notice_period_days: int = 30

class CandidateOut(CandidateCreate):
    id: int
    stage: str
    created_at: datetime
    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    emp_code: str
    full_name: str
    official_email: str
    personal_email: Optional[str] = None
    phone: Optional[str] = None
    designation: str
    department: str = "Engineering"
    employment_type: str = "Full-Time"
    date_of_joining: date
    probation_period_months: int = 6
    work_location: str = "Bangalore"
    annual_ctc: float = 1200000.0
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    uan_number: Optional[str] = None
    esic_number: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_name: Optional[str] = "ICICI Bank"
    # Geolocation & Geofence
    latitude: Optional[float] = 13.035820
    longitude: Optional[float] = 77.653410
    geofence_radius_meters: Optional[float] = 200.0
    geofence_enforced: Optional[bool] = True
    work_location_type: Optional[str] = "HQ Office"
    # Webcam & Biometric
    webcam_registered_face_url: Optional[str] = None
    facial_enrollment_status: Optional[str] = "Enrolled"
    webcam_hardware_device: Optional[str] = "Integrated HD Webcam (1080p)"
    # Personal & Emergency
    blood_group: Optional[str] = "O+"
    emergency_contact_name: Optional[str] = "Family Member"
    emergency_contact_phone: Optional[str] = "+91-9876543210"
    residential_address: Optional[str] = "Horamavu, Bangalore North, Bangalore - 560043, Karnataka"

class EmployeeOut(BaseModel):
    id: int
    emp_code: str
    full_name: str
    official_email: str
    designation: str
    department: str
    employment_type: str
    date_of_joining: date
    probation_status: str
    employment_status: str
    work_location: str
    pan_number: Optional[str] = None
    uan_number: Optional[str] = None
    # Geolocation & Geofence
    latitude: Optional[float] = 13.035820
    longitude: Optional[float] = 77.653410
    geofence_radius_meters: Optional[float] = 200.0
    geofence_enforced: Optional[bool] = True
    work_location_type: Optional[str] = "HQ Office"
    # Webcam & Biometric
    webcam_registered_face_url: Optional[str] = None
    facial_enrollment_status: Optional[str] = "Enrolled"
    webcam_hardware_device: Optional[str] = "Integrated HD Webcam (1080p)"
    last_biometric_verification_at: Optional[datetime] = None
    facial_liveness_score: Optional[float] = 98.5
    # Personal & Emergency
    blood_group: Optional[str] = "O+"
    emergency_contact_name: Optional[str] = "Family Member"
    emergency_contact_phone: Optional[str] = "+91-9876543210"
    residential_address: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class EmployeeWebcamEnrollRequest(BaseModel):
    webcam_snapshot_base64: str
    webcam_hardware_device: Optional[str] = "Integrated HD Webcam (1080p)"
    facial_liveness_verified: Optional[bool] = True
    liveness_score: Optional[float] = 98.5

class EmployeeLocationUpdateRequest(BaseModel):
    latitude: float
    longitude: float
    geofence_radius_meters: Optional[float] = 200.0
    geofence_enforced: Optional[bool] = True
    work_location_type: Optional[str] = "HQ Office"
    work_location: Optional[str] = "Bangalore"

class GenerateLetterRequest(BaseModel):
    letter_code: str # e.g. HR-REC-01, HR-ONB-01, HR-ADM-01, HR-SEP-15
    recipient_name: str
    recipient_email: Optional[str] = None
    employee_id: Optional[int] = None
    designation: Optional[str] = None
    department: Optional[str] = "Engineering"
    annual_ctc: Optional[float] = None
    context_data: Optional[Dict[str, Any]] = None

class HRLetterOut(BaseModel):
    id: int
    letter_code: str
    letter_title: str
    category: str
    recipient_name: str
    issue_date: date
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CandidateStageUpdate(BaseModel):
    stage: str # Applied, Screening, Interview Scheduled, Technical Cleared, Intent to Offer, Offer Sent, Accepted, Rejected
    interview_feedback: Optional[str] = None

class CandidateHireRequest(BaseModel):
    emp_code: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    annual_ctc: Optional[float] = None
    date_of_joining: Optional[date] = None

class LeaveRecordOut(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    leave_type: str
    start_date: date
    end_date: date
    total_days: float
    reason: str
    status: str
    approver: str
    created_at: datetime
    class Config:
        from_attributes = True

class LeaveStatusUpdate(BaseModel):
    status: str # Approved, Rejected, Cancelled
    approver: Optional[str] = "HR / Reporting Manager"

class POSHCaseCreate(BaseModel):
    case_reference: Optional[str] = None
    date_filed: date = date.today()
    nature_of_complaint: str
    internal_committee_presiding_officer: str = "Senior Woman Leader"
    external_member: str = "Empowered NGO Representative"
    interim_relief_granted: bool = False
    recommendations_summary: Optional[str] = None
    action_taken: Optional[str] = None

class POSHCaseOut(BaseModel):
    id: int
    case_reference: str
    date_filed: date
    nature_of_complaint: str
    internal_committee_presiding_officer: str
    external_member: str
    inquiry_status: str
    interim_relief_granted: bool
    statutory_90_day_deadline: date
    recommendations_summary: Optional[str]
    action_taken: Optional[str]
    annual_report_disclosed: bool
    created_at: datetime
    class Config:
        from_attributes = True

class POSHCaseConclude(BaseModel):
    inquiry_status: str = "Concluded"
    recommendations_summary: str
    action_taken: str

class SeparationClearanceCreate(BaseModel):
    employee_id: int
    resignation_date: date
    last_working_day: date
    notice_period_required: int = 30
    notice_period_served: int = 30
    notice_buyout_days: int = 0

class SeparationClearanceOut(BaseModel):
    id: int
    employee_id: int
    resignation_date: date
    last_working_day: date
    notice_period_required: int
    notice_period_served: int
    notice_buyout_days: int
    it_asset_clearance: bool
    it_access_revoked: bool
    admin_id_card_clearance: bool
    finance_clearance: bool
    manager_handover_clearance: bool
    hr_clearance: bool
    fnf_gross_payable: float
    fnf_deductions: float
    fnf_net_payable: float
    fnf_settlement_status: str
    relieving_letter_issued: bool
    created_at: datetime
    class Config:
        from_attributes = True

class SeparationClearanceUpdate(BaseModel):
    it_asset_clearance: Optional[bool] = None
    it_access_revoked: Optional[bool] = None
    admin_id_card_clearance: Optional[bool] = None
    finance_clearance: Optional[bool] = None
    manager_handover_clearance: Optional[bool] = None
    hr_clearance: Optional[bool] = None
    fnf_settlement_status: Optional[str] = None
    relieving_letter_issued: Optional[bool] = None

class HRMSOverviewMetricsOut(BaseModel):
    active_headcount: int
    total_candidates: int
    candidates_in_interview: int
    monthly_payroll_outflow: float
    annual_payroll_run_rate: float
    statutory_pf_outflow_monthly: float
    statutory_pt_outflow_monthly: float
    approved_leaves_count: int
    pending_leaves_count: int
    posh_compliance_index_pct: float
    active_separations_count: int

