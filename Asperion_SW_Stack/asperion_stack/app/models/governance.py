"""
Asperion Enterprise OS - Corporate Governance & Legal Entity Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float
from app.database import Base

class EntityMaster(Base):
    __tablename__ = "entity_master"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String(255), default="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED")
    cin = Column(String(50), default="U85500KA2026OPC222069")
    incorporation_date = Column(Date, nullable=True)
    registered_office = Column(Text, nullable=True)
    pan = Column(String(20), default="AAACA1234D")
    tan = Column(String(20), default="BLRA12345D")
    gstin = Column(String(30), default="29AAACA1234D1Z5")
    sole_member_director = Column(String(100), default="Varadi Vijay")
    authorized_capital = Column(Float, default=100000.0)
    paid_up_capital = Column(Float, default=100000.0)
    udyam_reg_number = Column(String(50), default="UDYAM-KR-03-0189422")
    dpiit_recognition_number = Column(String(50), default="DIPP142089")
    duns_number = Column(String(20), default="65-102-9481")
    registered_property_owner = Column(String(100), default="Varadi Vijay (NOC & Electricity Consent on Record)")
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

class BoardResolution(Base):
    __tablename__ = "board_resolutions"
    
    id = Column(Integer, primary_key=True, index=True)
    resolution_number = Column(String(50), unique=True, index=True)
    title = Column(String(255), nullable=False)
    resolution_type = Column(String(100), default="OPC Member Resolution") # Ordinary, Special, Circular, OPC
    date_passed = Column(Date, nullable=False)
    subject_category = Column(String(100)) # Banking, Commercial, Statutory, Borrowing, Appointment
    resolution_text = Column(Text, nullable=False)
    authorized_signatory = Column(String(100))
    status = Column(String(50), default="Passed & Recorded")
    mca_filing_required = Column(Boolean, default=False)
    mca_srn = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceCalendarItem(Base):
    __tablename__ = "compliance_calendar"
    
    id = Column(Integer, primary_key=True, index=True)
    compliance_name = Column(String(255), nullable=False)
    statutory_authority = Column(String(100)) # MCA/ROC, GST, Income Tax (TDS), EPFO, ESIC, PT
    form_or_return = Column(String(100)) # e.g. AOC-4, MGT-7A, GSTR-1, GSTR-3B, Form 24Q, Form 26Q
    due_date = Column(Date, nullable=False)
    frequency = Column(String(50)) # Monthly, Quarterly, Annual, Event-Based
    financial_year = Column(String(20), default="2026-2027")
    status = Column(String(50), default="Upcoming") # Upcoming, Filed, Delayed, Exempt
    filing_reference = Column(String(100), nullable=True)
    owner = Column(String(100), default="Finance & Legal Lead")
    penalty_risk = Column(String(100), default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow)

class PolicyRecord(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_code = Column(String(50), unique=True, index=True)
    policy_name = Column(String(255), nullable=False)
    category = Column(String(100)) # HR, Cybersecurity, Ethics/POSH, Data Privacy/DPDP, Finance, IT
    version = Column(String(20), default="1.0")
    effective_date = Column(Date, nullable=False)
    review_cycle = Column(String(50), default="Annual")
    approved_by = Column(String(100), default="Director / Founder")
    status = Column(String(50), default="Active")
    description = Column(Text, nullable=True)
    acknowledgement_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuthorityMatrixItem(Base):
    __tablename__ = "authority_matrix"
    
    id = Column(Integer, primary_key=True, index=True)
    functional_area = Column(String(100), nullable=False) # Financial, Contracting, Hiring, IT Procurement
    transaction_type = Column(String(255), nullable=False)
    threshold_limit = Column(String(100)) # e.g. Up to 50k, 50k to 5L, Above 5L
    initiator_role = Column(String(100))
    recommender_role = Column(String(100), nullable=True)
    approver_role = Column(String(100), nullable=False)
    documentation_required = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), default="INFO") # INFO, WARNING, CRITICAL
    actor = Column(String(100), default="System")
    module = Column(String(50), nullable=False, index=True) # GovOps, LegalOps, FinOps, PeopleOps, DeliveryOps, ProcureOps, CloudOps, SecOps
    description = Column(Text, nullable=False)
    ip_address = Column(String(45), default="127.0.0.1")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

