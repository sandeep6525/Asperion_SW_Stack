"""
Asperion Enterprise OS - Developer Platform Accounts, Secret Rotation & Statutory Tax Challan Models
Derived from Developer Accounts Roadmap, Statutory Tax Manuals and ROC Corporate Records.
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date
from datetime import datetime
from app.database import Base

class DeveloperPlatformAccount(Base):
    """
    Corporate Developer Account & Publishing Platform Master.
    Mandates Organization identity, D-U-N-S verification, and FIDO2 MFA posture.
    """
    __tablename__ = "developer_platform_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. DEV-ACC-001
    platform_name = Column(String(100), nullable=False) # Google Play Console, Apple Developer, GitHub Org, etc.
    account_type = Column(String(50), default="Organization / Corporate Entity")
    admin_email = Column(String(120), nullable=False) # admin@asperion.in / founder@asperion.in
    organization_id = Column(String(100), nullable=True) # e.g. Team ID, Org Slug, Tenant ID
    duns_linked = Column(Boolean, default=True)
    fido2_mfa_enforced = Column(Boolean, default=True)
    verification_status = Column(String(50), default="Verified Organization") # Verified Organization, In Review, Pending
    tier_or_plan = Column(String(50), default="Enterprise")
    annual_fee_inr = Column(Float, default=0.0)
    renewal_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DeveloperEnvironmentSecret(Base):
    """
    Cryptographic Deploy Keys, API Gateway Secrets & Automated 90-Day Rotation Ledger.
    """
    __tablename__ = "developer_environment_secrets"

    id = Column(Integer, primary_key=True, index=True)
    secret_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. SEC-ROT-001
    secret_name = Column(String(100), nullable=False)
    target_environment = Column(String(30), default="Production") # Production, Staging, Development
    platform = Column(String(50), nullable=False) # GitHub, AWS, OpenAI, Meta, Firebase
    sha256_fingerprint = Column(String(64), nullable=False)
    rotation_cadence_days = Column(Integer, default=90)
    last_rotated_at = Column(DateTime, default=datetime.utcnow)
    next_rotation_due = Column(Date, nullable=False)
    status = Column(String(30), default="Active & Compliant") # Active & Compliant, Rotation Due, Revoked
    created_at = Column(DateTime, default=datetime.utcnow)

class StatutoryChallanFiling(Base):
    """
    Formal Statutory Tax Deposit Challans, BSR Code verification & Government ARN Tracking.
    Covers GSTR-3B, GSTR-1, TDS Form 24Q/26Q, Karnataka PT, and Advance Tax.
    """
    __tablename__ = "statutory_challan_filings"

    id = Column(Integer, primary_key=True, index=True)
    challan_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CHL-GST-2026-05
    filing_type = Column(String(50), nullable=False) # GSTR-3B, GSTR-1, TDS Challan 281, Karnataka PT, Advance Tax
    statutory_authority = Column(String(50), nullable=False) # GSTN, Income Tax Dept, Karnataka Commercial Taxes, MCA
    assessment_year = Column(String(20), default="2027-2028")
    tax_period = Column(String(50), nullable=False) # e.g. MAY-2026, Q1 FY2026-27
    statutory_due_date = Column(Date, nullable=False)
    actual_filing_date = Column(Date, nullable=True)
    challan_cin_arn = Column(String(50), nullable=True) # Govt ARN or CIN (Challan Identification Number)
    bsr_code = Column(String(10), default="0001234") # 7-digit bank branch code (ICICI Bank)
    tax_amount_paid = Column(Float, nullable=False)
    interest_penalty = Column(Float, default=0.0)
    payment_mode = Column(String(30), default="NEFT / NetBanking")
    reconciliation_status = Column(String(30), default="Reconciled with Portal") # Reconciled, Pending Deposit, Overdue
    created_at = Column(DateTime, default=datetime.utcnow)
