"""
Asperion Enterprise OS - Enterprise Operations, BCP/DR & Ledger Schemas (Pydantic V2)
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class EnterpriseEventLedgerBase(BaseModel):
    event_code: str
    aggregate_type: str
    aggregate_id: str
    event_type: str
    actor_name: str = "System Autonomous Controller"
    actor_role: str = "Director / System"
    department: str = "Enterprise Core"
    payload_json: str = "{}"
    prev_hash: str
    current_hash: str
    signature: str = "ED25519-VERIFIED"
    ip_address: str = "127.0.0.1"
    timestamp: datetime

class EnterpriseEventLedgerCreate(BaseModel):
    aggregate_type: str
    aggregate_id: str
    event_type: str
    actor_name: Optional[str] = "System Autonomous Controller"
    actor_role: Optional[str] = "Director / System"
    department: Optional[str] = "Enterprise Core"
    payload: Optional[Dict[str, Any]] = None

class EnterpriseEventLedgerOut(EnterpriseEventLedgerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LedgerVerificationResult(BaseModel):
    is_tamper_evident: bool
    total_events_verified: int
    genesis_hash: str
    latest_hash: str
    tampered_event_id: Optional[int] = None
    verification_status: str # "VERIFIED_GENUINE_ZERO_TAMPERING" or "CORRUPTION_DETECTED"
    verified_at: str


class DisasterRecoverySnapshotBase(BaseModel):
    snapshot_code: str
    backup_type: str = "Full SQLite Hot Backup"
    storage_path: str
    file_size_bytes: int = 0
    sha256_checksum: str
    encryption_algorithm: str = "AES-256-GCM"
    is_verified: bool = True
    rpo_minutes: float = 15.0
    rto_minutes: float = 5.0
    last_restore_test_at: Optional[datetime] = None
    restore_test_status: str = "Verified Successful"
    notes: Optional[str] = None
    created_at: datetime

class DisasterRecoverySnapshotCreate(BaseModel):
    backup_type: str = "Full SQLite Hot Backup"
    notes: Optional[str] = "On-demand administrator backup snapshot."

class DisasterRecoverySnapshotOut(DisasterRecoverySnapshotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DRRestoreTestResponse(BaseModel):
    snapshot_code: str
    restore_simulation_status: str # "PASSED_WITHIN_SLA"
    measured_rto_seconds: float
    target_rto_seconds: float = 300.0 # 5 minutes
    checksum_match: bool
    data_integrity_score: float = 100.0
    tested_at: str
    attestation: str


class DPDPConsentRecordBase(BaseModel):
    consent_ref: str
    data_principal_name: str
    data_principal_type: str = "Employee"
    principal_identifier: str
    purpose_category: str
    notice_reference: str = "ADT/DPDP/NOTICE/2026/V1"
    consent_status: str = "Granted"
    granted_at: datetime
    withdrawn_at: Optional[datetime] = None
    expiry_date: Optional[date] = None
    data_protection_officer: str = "AGT-COMPLY-01 (Compliance Officer)"
    audit_notes: Optional[str] = None

class DPDPConsentRecordCreate(BaseModel):
    data_principal_name: str
    data_principal_type: str = "Employee"
    principal_identifier: str
    purpose_category: str
    notice_reference: Optional[str] = "ADT/DPDP/NOTICE/2026/V1"
    consent_status: Optional[str] = "Granted"
    audit_notes: Optional[str] = "Affirmative consent logged with cryptographic IP attestation."

class DPDPConsentRecordOut(DPDPConsentRecordBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SystemDiagnosticTelemetryOut(BaseModel):
    db_size_bytes: int
    db_size_formatted: str
    wal_size_bytes: int
    wal_size_formatted: str
    wal_checkpoint_status: str
    active_connection_count: int
    db_query_latency_ms: float
    process_rss_mb: float
    system_health_score: float
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class DBVacuumResponse(BaseModel):
    status: str
    initial_db_size_bytes: int
    reclaimed_bytes: int
    final_db_size_bytes: int
    wal_checkpoint_pages: int
    vacuum_duration_sec: float
    message: str


class OperationsOverviewResponse(BaseModel):
    status: str
    corporate_entity: str
    cin: str
    ledger_summary: Dict[str, Any]
    bcp_dr_summary: Dict[str, Any]
    dpdp_summary: Dict[str, Any]
    telemetry_summary: Dict[str, Any]
