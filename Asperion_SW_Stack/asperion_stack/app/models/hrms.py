"""
Asperion Enterprise OS - HRMS, Payroll & Lifecycle Letter Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    applied_role = Column(String(100), nullable=False)
    department = Column(String(100), default="Engineering")
    experience_years = Column(Float, default=0.0)
    current_ctc = Column(Float, default=0.0)
    expected_ctc = Column(Float, default=0.0)
    notice_period_days = Column(Integer, default=30)
    stage = Column(String(50), default="Applied") # Applied, Interview Scheduled, Technical Cleared, Intent to Offer, Offer Sent, Accepted, Rejected
    resume_url = Column(String(255), nullable=True)
    interview_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String(50), unique=True, index=True) # ADT-EMP-001
    full_name = Column(String(255), nullable=False)
    official_email = Column(String(100), unique=True, index=True, nullable=False)
    personal_email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    designation = Column(String(100), nullable=False)
    department = Column(String(100), default="Engineering") # Engineering, Product, Sales, Finance, HR, IT & SecOps
    employment_type = Column(String(50), default="Full-Time") # Full-Time, Consultant, Intern, Fixed-Term
    date_of_joining = Column(Date, nullable=False)
    probation_period_months = Column(Integer, default=6)
    probation_status = Column(String(50), default="Under Probation") # Under Probation, Confirmed, Extended
    reporting_manager = Column(String(100), default="Founder / CEO")
    pan_number = Column(String(20), nullable=True)
    aadhaar_number = Column(String(20), nullable=True)
    uan_number = Column(String(30), nullable=True) # EPFO UAN
    esic_number = Column(String(30), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_ifsc = Column(String(20), nullable=True)
    bank_name = Column(String(100), nullable=True)
    work_location = Column(String(100), default="Bangalore")
    employment_status = Column(String(50), default="Active") # Active, On Notice, Resigned, Terminated, Separated
    
    # Geolocation, Coordinates & Perimeter Tracking
    latitude = Column(Float, default=13.035820) # Horamavu HQ Coordinates
    longitude = Column(Float, default=77.653410) # Horamavu HQ Coordinates
    geofence_radius_meters = Column(Float, default=200.0)
    geofence_enforced = Column(Boolean, default=True)
    work_location_type = Column(String(50), default="HQ Office") # HQ Office, Approved Remote WFH, Client On-Site, Hybrid

    # Webcam & Biometric Facial Recognition Details
    webcam_registered_face_url = Column(Text, nullable=True) # Data URL or Photo Path
    facial_enrollment_status = Column(String(50), default="Enrolled") # Enrolled, Pending, Exempt
    facial_descriptor_json = Column(Text, nullable=True) # 128-d or 512-d landmarks/embeddings
    webcam_hardware_device = Column(String(100), default="Integrated HD Webcam (1080p)")
    last_biometric_verification_at = Column(DateTime, nullable=True)
    facial_liveness_score = Column(Float, default=98.5)

    # Personal, Emergency & Statutory Details
    blood_group = Column(String(10), default="O+")
    emergency_contact_name = Column(String(100), default="Family Member")
    emergency_contact_phone = Column(String(50), default="+91-9876543210")
    residential_address = Column(Text, default="Horamavu, Bangalore North, Bangalore - 560043, Karnataka")

    created_at = Column(DateTime, default=datetime.utcnow)
    
    salary_structure = relationship("SalaryStructure", back_populates="employee", uselist=False)
    payroll_records = relationship("PayrollRecord", back_populates="employee")
    letters = relationship("HRLetter", back_populates="employee")

class SalaryStructure(Base):
    __tablename__ = "salary_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    annual_ctc = Column(Float, nullable=False) # e.g. 1,200,000
    monthly_ctc = Column(Float, nullable=False)
    # Monthly Earnings
    basic_salary = Column(Float, nullable=False) # 40-50% of fixed
    hra = Column(Float, nullable=False)          # 40-50% of basic
    special_allowance = Column(Float, nullable=False) # Balancer
    gross_salary = Column(Float, nullable=False)
    # Monthly Employer Contributions
    employer_pf = Column(Float, default=0.0)     # 12% on min(Basic, 15000) or actual
    employer_esi = Column(Float, default=0.0)    # 3.25% if gross <= 21000
    gratuity_provision = Column(Float, default=0.0) # 4.81% of basic
    # Monthly Employee Deductions
    employee_pf = Column(Float, default=0.0)     # 12%
    employee_esi = Column(Float, default=0.0)    # 0.75%
    professional_tax = Column(Float, default=200.0) # Karnataka slab
    estimated_tds = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)
    net_in_hand = Column(Float, nullable=False)  # Gross - Deductions
    effective_from = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    
    employee = relationship("Employee", back_populates="salary_structure")

class PayrollRecord(Base):
    __tablename__ = "payroll_records"
    
    id = Column(Integer, primary_key=True, index=True)
    payroll_cycle = Column(String(20), nullable=False, index=True) # e.g. "JUN-2026", "JUL-2026"
    employee_id = Column(Integer, ForeignKey("employees.id"))
    days_in_month = Column(Integer, default=30)
    payable_days = Column(Float, default=30.0)
    lop_days = Column(Float, default=0.0)
    earned_basic = Column(Float, default=0.0)
    earned_hra = Column(Float, default=0.0)
    earned_special_allowance = Column(Float, default=0.0)
    earned_gross = Column(Float, default=0.0)
    pf_deduction = Column(Float, default=0.0)
    esi_deduction = Column(Float, default=0.0)
    pt_deduction = Column(Float, default=200.0)
    tds_deduction = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)
    net_salary = Column(Float, default=0.0)
    payment_status = Column(String(50), default="Pending") # Pending, Processed, Disbursed, Hold
    bank_utr = Column(String(100), nullable=True)
    payslip_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("Employee", back_populates="payroll_records")

class HRLetter(Base):
    __tablename__ = "hr_letters"
    
    id = Column(Integer, primary_key=True, index=True)
    letter_code = Column(String(50), index=True) # HR-REC-01, HR-ONB-01, HR-ADM-01, HR-ER-08, HR-SEP-15, etc.
    letter_title = Column(String(255), nullable=False)
    category = Column(String(100)) # Recruitment, Onboarding, Employment, Employee Relations, Separation
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    recipient_name = Column(String(255), nullable=False)
    recipient_email = Column(String(100), nullable=True)
    issue_date = Column(Date, nullable=False)
    generated_content_html = Column(Text, nullable=False)
    status = Column(String(50), default="Issued") # Draft, Issued, Signed, Archived
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("Employee", back_populates="letters")

class SeparationClearance(Base):
    __tablename__ = "separation_clearances"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    resignation_date = Column(Date, nullable=False)
    last_working_day = Column(Date, nullable=False)
    notice_period_required = Column(Integer, default=30)
    notice_period_served = Column(Integer, default=30)
    notice_buyout_days = Column(Integer, default=0)
    it_asset_clearance = Column(Boolean, default=False) # Laptops, monitors, keys
    it_access_revoked = Column(Boolean, default=False)  # Google Workspace, AWS, GitHub, Slack
    admin_id_card_clearance = Column(Boolean, default=False)
    finance_clearance = Column(Boolean, default=False)  # Travel claims, advances
    manager_handover_clearance = Column(Boolean, default=False)
    hr_clearance = Column(Boolean, default=False)
    fnf_gross_payable = Column(Float, default=0.0)
    fnf_deductions = Column(Float, default=0.0)
    fnf_net_payable = Column(Float, default=0.0)
    fnf_settlement_status = Column(String(50), default="Pending") # Pending, Approved, Disbursed
    relieving_letter_issued = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LeaveRecord(Base):
    __tablename__ = "leave_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee_name = Column(String(100), nullable=False)
    leave_type = Column(String(50), default="Casual Leave") # Casual Leave (CL), Sick Leave (SL), Earned Leave (EL), Maternity, Paternity, Bereavement
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Float, default=1.0)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="Approved") # Pending, Approved, Rejected, Cancelled
    approver = Column(String(100), default="Reporting Manager")
    created_at = Column(DateTime, default=datetime.utcnow)

class POSHCase(Base):
    __tablename__ = "posh_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_reference = Column(String(50), unique=True, index=True) # ADT-POSH-2026-001
    date_filed = Column(Date, nullable=False)
    nature_of_complaint = Column(String(100), nullable=False)
    internal_committee_presiding_officer = Column(String(100), default="Senior Woman Leader")
    external_member = Column(String(100), default="Empowered NGO Representative")
    inquiry_status = Column(String(50), default="Under Inquiry") # Received, Preliminary Review, Under Inquiry, Concluded, Closed
    interim_relief_granted = Column(Boolean, default=False)
    statutory_90_day_deadline = Column(Date, nullable=False)
    recommendations_summary = Column(Text, nullable=True)
    action_taken = Column(Text, nullable=True)
    annual_report_disclosed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

