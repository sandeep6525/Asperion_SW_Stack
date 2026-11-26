"""
Asperion Enterprise OS - Expanded IT, Cloud & Passkey Access Infrastructure Models
Pillars: Passkey (FIDO2/WebAuthn), Zero Trust Network Access (ZTNA), MDM Device Compliance, Backup/Restore DR Tests
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from app.database import Base

class PasskeyCredential(Base):
    """
    FIDO2 / WebAuthn Hardware & Biometric Passkey Registration Ledger.
    Replaces legacy passwords with phishing-resistant public key cryptography.
    Supports YubiKey 5 Series, Apple TouchID/FaceID Secure Enclave, and Windows Hello.
    """
    __tablename__ = "passkey_credentials"

    id = Column(Integer, primary_key=True, index=True)
    passkey_id = Column(String(50), unique=True, index=True) # e.g. FIDO-2026-001
    user_email = Column(String(100), index=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    device_name = Column(String(100), default="MacBook Touch ID / YubiKey 5C NFC")
    authenticator_type = Column(String(50), default="Platform Authenticator (TouchID / Windows Hello)") # Platform, Cross-Platform (Hardware Token)
    aaguid = Column(String(64), default="00000000-0000-0000-0000-000000000000") # Authenticator Attestation GUID
    public_key_spki = Column(Text, nullable=False) # Public key in SubjectPublicKeyInfo PEM format
    sign_count = Column(Integer, default=0) # Clone detection counter
    user_verified = Column(Boolean, default=True) # Biometric or PIN verified
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Active - Enforced") # Active - Enforced, Suspended, Revoked
    zero_trust_status = Column(String(50), default="Compliant - Hardware Bound")

class ZeroTrustPolicy(Base):
    """
    Zero-Trust Network Access (ZTNA) & Context-Aware Access Policies.
    Evaluates device compliance, geographic IP, passkey authentication, and role authorization.
    """
    __tablename__ = "zero_trust_policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_code = Column(String(50), unique=True, index=True) # e.g. ZT-POL-PROD-01
    policy_name = Column(String(150), nullable=False)
    target_resource = Column(String(100), nullable=False) # Production Database, AWS Console, GitLab Repos, HRMS Financials
    required_privilege = Column(String(50), default="Elevated / Superadmin")
    fido2_passkey_required = Column(Boolean, default=True)
    device_encryption_required = Column(Boolean, default=True)
    allowed_ip_ranges = Column(String(200), default="Horamavu HQ Office IP / ZTNA WireGuard Tunnel")
    session_timeout_minutes = Column(Integer, default=60)
    enforcement_mode = Column(String(30), default="Active_Blocking") # Active_Blocking, Audit_Only
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DRSimulationTest(Base):
    """
    Disaster Recovery (DR) Simulation Drill & Database Restore Log.
    Tracks RTO (Recovery Time Objective) and RPO (Recovery Point Objective) verification against AWS Hyderabad warm standby.
    """
    __tablename__ = "dr_simulation_tests"

    id = Column(Integer, primary_key=True, index=True)
    test_code = Column(String(50), unique=True, index=True) # e.g. DR-TEST-2026-Q1
    test_type = Column(String(50), default="Full Failover Simulation") # Full Failover Simulation, Tabletop Drill, Database Point-in-Time Restore
    simulated_scenario = Column(String(255), nullable=False) # AWS ap-south-1 Mumbai AZ blackout simulation
    target_cluster = Column(String(100), default="Secondary EKS Warm Standby (ap-south-2 Hyderabad)")
    database_backup_point = Column(DateTime, nullable=False)
    actual_rto_minutes = Column(Float, default=18.5) # RTO achieved
    target_rto_minutes = Column(Float, default=60.0) # SLA: 60 mins
    actual_rpo_minutes = Column(Float, default=2.1) # RPO achieved
    target_rpo_minutes = Column(Float, default=15.0) # SLA: 15 mins
    data_loss_detected = Column(Boolean, default=False)
    test_outcome = Column(String(50), default="PASSED - RTO/RPO SLA Met")
    conducted_by = Column(String(100), default="Head of Infrastructure (Priya Nair)")
    conducted_at = Column(DateTime, default=datetime.utcnow)
    report_url = Column(String(200), default="DOC-DR-REPORT-2026-01")
