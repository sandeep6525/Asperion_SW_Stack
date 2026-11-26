"""
Asperion Enterprise OS - CRM, Legal Contracting & Prospect Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Prospect(Base):
    __tablename__ = "prospects"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    contact_person = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    industry = Column(String(100), default="Technology / Software")
    pipeline_stage = Column(String(50), default="Lead Qualified") # Lead Qualified, Discovery, Proposal Sent, Negotiation, Closed Won, Closed Lost
    deal_value = Column(Float, default=0.0)
    lead_source = Column(String(100), default="Direct / Referral")
    owner = Column(String(100), default="Sales Lead")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    contracts = relationship("ClientContract", back_populates="prospect")

class ClientContract(Base):
    __tablename__ = "client_contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_reference = Column(String(50), unique=True, index=True)
    prospect_id = Column(Integer, ForeignKey("prospects.id"), nullable=True)
    client_name = Column(String(255), nullable=False)
    contract_type = Column(String(50), nullable=False) # Mutual NDA, Non-Mutual NDA, Master Services Agreement (MSA), SOW, MOU, LOI
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    value_inr = Column(Float, default=0.0)
    status = Column(String(50), default="Drafted") # Drafted, Under Legal Review, Client Review, Fully Executed, Expired, Terminated
    stamp_duty_paid = Column(Boolean, default=False)
    governing_law = Column(String(100), default="Laws of India, Jurisdiction of Bangalore, Karnataka")
    ip_ownership_clause = Column(String(255), default="Asperion Retains Background IP; Work Product Transferred upon Full Payment")
    special_conditions = Column(Text, nullable=True)
    signed_copy_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    prospect = relationship("Prospect", back_populates="contracts")

class ClientOnboardingRecord(Base):
    __tablename__ = "client_onboardings"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    pan_verified = Column(Boolean, default=False)
    gstin_verified = Column(Boolean, default=False)
    kyc_status = Column(String(50), default="Pending") # Pending, Approved, Rejected
    billing_contact_email = Column(String(100))
    payment_terms_days = Column(Integer, default=30)
    credit_limit_inr = Column(Float, default=500000.0)
    nda_executed = Column(Boolean, default=False)
    msa_executed = Column(Boolean, default=False)
    sow_executed = Column(Boolean, default=False)
    delivery_handover_status = Column(String(50), default="In Progress")
    created_at = Column(DateTime, default=datetime.utcnow)

class LegalRiskObligation(Base):
    __tablename__ = "legal_risks_obligations"
    
    id = Column(Integer, primary_key=True, index=True)
    obligation_title = Column(String(255), nullable=False)
    source_contract = Column(String(100))
    party = Column(String(255))
    nature = Column(String(100)) # Confidentiality, Non-Compete, SLA Guarantee, Indemnity, IP Warranty, DPDP Compliance
    risk_level = Column(String(50), default="Medium") # Low, Medium, High, Critical
    mitigation_control = Column(Text, nullable=True)
    monitoring_frequency = Column(String(50), default="Quarterly")
    status = Column(String(50), default="Compliant")
    created_at = Column(DateTime, default=datetime.utcnow)
