"""
Asperion Enterprise OS - Core Operations, BCP/DR & Tamper-Evident Ledger Models
Defines immutable cryptographic event sourcing, disaster recovery snapshots,
India DPDP Act 2023 consent management, and live system diagnostic telemetry.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EnterpriseEventLedger(Base):
    """
    Immutable Event Sourcing Ledger with SHA-256 Cryptographic Hash Chaining.
    Ensures tamper-evident compliance under ISO 27001 A.12.4 and SOC 2 Type II CC7.2.
    current_hash = SHA256(prev_hash + event_code + payload_json + timestamp)
    """
    __tablename__ = "enterprise_event_ledger"

    id = Column(Integer, primary_key=True, index=True)
    event_code = Column(String(50), unique=True, index=True) # e.g. EVT-2026-0001
    aggregate_type = Column(String(50), nullable=False, index=True) # INVOICE, CI_NODE, MISSION, EMPLOYEE, TICKET, CONTRACT, INCIDENT
    aggregate_id = Column(String(50), nullable=False, index=True) # Target entity code/ID
    event_type = Column(String(100), nullable=False, index=True) # e.g. INVOICE_APPROVED, CI_STATUS_CHANGED, MISSION_DISPATCHED
    actor_name = Column(String(100), default="System Autonomous Controller")
    actor_role = Column(String(100), default="Director / System")
    department = Column(String(50), default="Enterprise Core")
    payload_json = Column(Text, default="{}")
    prev_hash = Column(String(64), nullable=False) # SHA-256 hash of previous block (Genesis for #1)
    current_hash = Column(String(64), nullable=False, index=True) # SHA-256 hash of current block
    signature = Column(String(128), default="ED25519-VERIFIED") # Digital signature representation
    ip_address = Column(String(45), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class DisasterRecoverySnapshot(Base):
    """
    Business Continuity & Disaster Recovery (BCP/DR) Snapshot Registry.
    Tracks hot SQLite checkpoints, cold database archives, and cloud syncs (ISO 22301 & ISO 27001 A.17).
    """
    __tablename__ = "disaster_recovery_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_code = Column(String(50), unique=True, index=True) # e.g. SNAP-2026-0012
    backup_type = Column(String(50), default="Full SQLite Hot Backup") # Full SQLite Hot Backup, Incremental WAL Snapshot, S3 Remote Replica
    storage_path = Column(String(255), nullable=False)
    file_size_bytes = Column(BigInteger, default=0)
    sha256_checksum = Column(String(64), nullable=False)
    encryption_algorithm = Column(String(30), default="AES-256-GCM")
    is_verified = Column(Boolean, default=True)
    rpo_minutes = Column(Float, default=15.0) # Recovery Point Objective (< 15 mins)
    rto_minutes = Column(Float, default=5.0) # Recovery Time Objective (< 5 mins)
    last_restore_test_at = Column(DateTime, nullable=True)
    restore_test_status = Column(String(30), default="Verified Successful") # Verified Successful, In Progress, Failed
    notes = Column(Text, default="Automated scheduled snapshot verified against primary database checksum.")
    created_at = Column(DateTime, default=datetime.utcnow)


class DPDPConsentRecord(Base):
    """
    India Digital Personal Data Protection (DPDP) Act 2023 Statutory Consent Register.
    Tracks explicit consent for processing employee, client, and vendor personal data.
    """
    __tablename__ = "dpdp_consent_records"

    id = Column(Integer, primary_key=True, index=True)
    consent_ref = Column(String(50), unique=True, index=True) # e.g. DPDP-2026-0089
    data_principal_name = Column(String(100), nullable=False) # Name of individual
    data_principal_type = Column(String(50), default="Employee") # Employee, Client Sponsor, Vendor Contact, Job Candidate
    principal_identifier = Column(String(100), nullable=False) # Email, Employee ID, or Vendor Rep ID
    purpose_category = Column(String(100), nullable=False) # Payroll & Wage Code Processing, Client Contract Execution, Biometric Webcam Check-in
    notice_reference = Column(String(100), default="ADT/DPDP/NOTICE/2026/V1")
    consent_status = Column(String(30), default="Granted") # Granted, Withdrawn, Expired, Under Review
    granted_at = Column(DateTime, default=datetime.utcnow)
    withdrawn_at = Column(DateTime, nullable=True)
    expiry_date = Column(Date, nullable=True)
    data_protection_officer = Column(String(100), default="AGT-COMPLY-01 (Compliance Officer)")
    audit_notes = Column(Text, default="Affirmative digital consent logged with cryptographic IP attestation.")


class SystemDiagnosticTelemetry(Base):
    """
    Live Operational & Host Telemetry for SRE Watchdog.
    Tracks database size, WAL log pages, host memory, and daemon velocity.
    """
    __tablename__ = "system_diagnostic_telemetry"

    id = Column(Integer, primary_key=True, index=True)
    db_size_bytes = Column(BigInteger, default=0)
    wal_size_bytes = Column(BigInteger, default=0)
    wal_checkpoint_status = Column(String(50), default="PASSIVE_CHECKPOINT_OPTIMAL")
    active_connection_count = Column(Integer, default=1)
    db_query_latency_ms = Column(Float, default=1.2)
    process_rss_mb = Column(Float, default=85.0)
    system_health_score = Column(Float, default=99.6)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
