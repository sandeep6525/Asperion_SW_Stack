"""
Unit & Integration Tests for Module 22 - Enterprise Operations, BCP/DR & Cryptographic Event Ledger
Covers:
1. Executive operational overview endpoint
2. Tamper-evident event sourcing ledger & SHA-256 hash chaining
3. Cryptographic hash-chain integrity verification
4. BCP/DR backup snapshot generation with real SHA-256 digest
5. Automated sandbox restore drill testing 5-minute RTO SLA
6. India DPDP Act 2023 statutory consent register
7. Live SRE host telemetry and WAL checkpoint/vacuum
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.enterprise_operations import (
    get_operations_overview, get_event_ledger, append_event, verify_ledger,
    list_dr_snapshots, create_backup_snapshot, execute_dr_restore_drill,
    list_dpdp_consents, record_consent, get_live_telemetry, execute_vacuum
)
from app.schemas.enterprise_operations import (
    EnterpriseEventLedgerCreate, DisasterRecoverySnapshotCreate,
    DPDPConsentRecordCreate
)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_operations_overview(db_session):
    data = get_operations_overview(db=db_session)
    assert data.corporate_entity == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert data.cin == "U85500KA2026OPC222069"
    assert data.ledger_summary["is_tamper_evident"] is True
    assert data.ledger_summary["total_events"] >= 5
    assert data.bcp_dr_summary["target_rpo_minutes"] == 15.0
    assert data.bcp_dr_summary["target_rto_minutes"] == 5.0
    assert data.dpdp_summary["total_consents"] >= 3
    assert "db_size_formatted" in data.telemetry_summary


def test_ledger_list_and_verification(db_session):
    # 1. List events
    events = get_event_ledger(limit=10, offset=0, aggregate_type=None, db=db_session)
    assert len(events) >= 5
    
    first_event = events[0]
    assert first_event.event_code is not None
    assert len(first_event.current_hash) == 64
    assert len(first_event.prev_hash) == 64

    # 2. Verify hash chain integrity
    verification = verify_ledger(db=db_session)
    assert verification.is_tamper_evident is True
    assert verification.verification_status == "VERIFIED_GENUINE_ZERO_TAMPERING"
    assert verification.total_events_verified >= 5


def test_append_event_and_verify_chain(db_session):
    payload = EnterpriseEventLedgerCreate(
        aggregate_type="AUDIT_TEST",
        aggregate_id="TEST-AGG-01",
        event_type="SECURITY_POLICY_ATTESTED",
        actor_name="Test SRE Auditor",
        actor_role="Security Engineer",
        department="Cybersecurity",
        payload={"test_field": "test_value_123"}
    )
    new_event = append_event(payload=payload, db=db_session)
    assert new_event.aggregate_type == "AUDIT_TEST"
    assert len(new_event.current_hash) == 64

    # Verify chain integrity
    verification = verify_ledger(db=db_session)
    assert verification.is_tamper_evident is True


def test_bcp_dr_snapshot_and_restore_simulation(db_session):
    # 1. Create a new backup snapshot
    req = DisasterRecoverySnapshotCreate(
        backup_type="Full SQLite Hot Backup",
        notes="Automated pytest verification backup snapshot."
    )
    snapshot = create_backup_snapshot(payload=req, db=db_session)
    assert snapshot.snapshot_code is not None
    assert len(snapshot.sha256_checksum) == 64
    assert snapshot.encryption_algorithm == "AES-256-GCM"

    # 2. Simulate restore test
    drill = execute_dr_restore_drill(snapshot_id=snapshot.id, db=db_session)
    assert drill.restore_simulation_status == "PASSED_WITHIN_SLA"
    assert drill.measured_rto_seconds < 300.0
    assert drill.data_integrity_score == 100.0


def test_dpdp_consent_register(db_session):
    # 1. Register a new statutory consent
    consent_req = DPDPConsentRecordCreate(
        data_principal_name="Ananya Sen",
        data_principal_type="Job Candidate",
        principal_identifier="ananya.sen@example.com",
        purpose_category="Background Verification & Employment Screening",
        notice_reference="ADT/DPDP/NOTICE/2026/V1",
        consent_status="Granted",
        audit_notes="Affirmative consent logged with webcam and IP verification."
    )
    record = record_consent(payload=consent_req, db=db_session)
    assert record.consent_ref is not None
    assert record.data_principal_name == "Ananya Sen"
    assert record.consent_status == "Granted"

    # 2. List consents
    all_consents = list_dpdp_consents(principal_type=None, status_filter=None, limit=50, db=db_session)
    assert any(c.principal_identifier == "ananya.sen@example.com" for c in all_consents)


def test_sre_telemetry_and_vacuum(db_session):
    # 1. Live telemetry
    telemetry = get_live_telemetry(db=db_session)
    assert telemetry.db_size_bytes > 0
    assert telemetry.wal_checkpoint_status is not None
    assert telemetry.db_query_latency_ms >= 0.0

    # 2. Database vacuum
    vac = execute_vacuum(db=db_session)
    assert vac.status == "SUCCESS"
    assert vac.reclaimed_bytes >= 0
    assert vac.vacuum_duration_sec >= 0.0
