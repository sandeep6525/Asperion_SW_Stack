"""
Asperion Enterprise Operations, BCP/DR & Cryptographic Event Ledger API Router
Endpoint prefix: /api/v1/operations
Complies with ISO 27001 A.12.4, SOC 2 Type II CC7.2, and India DPDP Act 2023.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enterprise_operations import (
    EnterpriseEventLedger,
    DisasterRecoverySnapshot,
    DPDPConsentRecord,
    SystemDiagnosticTelemetry
)
from app.schemas.enterprise_operations import (
    OperationsOverviewResponse,
    EnterpriseEventLedgerOut,
    EnterpriseEventLedgerCreate,
    LedgerVerificationResult,
    DisasterRecoverySnapshotOut,
    DisasterRecoverySnapshotCreate,
    DRRestoreTestResponse,
    DPDPConsentRecordOut,
    DPDPConsentRecordCreate,
    SystemDiagnosticTelemetryOut,
    DBVacuumResponse
)
from app.engines.operations_engine import (
    append_event_ledger,
    verify_ledger_integrity,
    create_database_backup_snapshot,
    simulate_dr_restore_test,
    record_dpdp_consent,
    harvest_system_telemetry,
    execute_db_vacuum_and_checkpoint
)

router = APIRouter(prefix="/operations", tags=["Enterprise Operations & BCP/DR"])


@router.get("/overview", response_model=OperationsOverviewResponse)
def get_operations_overview(db: Session = Depends(get_db)):
    """
    Returns executive operational overview including cryptographic ledger health,
    BCP/DR RTO/RPO SLAs, DPDP statutory consent statistics, and live telemetry.
    """
    verification = verify_ledger_integrity(db)
    telemetry = harvest_system_telemetry(db)
    
    total_events = db.query(EnterpriseEventLedger).count()
    
    # BCP/DR Metrics
    total_snapshots = db.query(DisasterRecoverySnapshot).count()
    latest_snapshot = db.query(DisasterRecoverySnapshot).order_by(
        DisasterRecoverySnapshot.created_at.desc()
    ).first()

    # DPDP Metrics
    total_consents = db.query(DPDPConsentRecord).count()
    granted_consents = db.query(DPDPConsentRecord).filter(
        DPDPConsentRecord.consent_status == "Granted"
    ).count()

    return OperationsOverviewResponse(
        status="OPERATIONAL",
        corporate_entity="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        cin="U85500KA2026OPC222069",
        ledger_summary={
            "total_events": total_events,
            "is_tamper_evident": verification["is_tamper_evident"],
            "verification_status": verification["verification_status"],
            "latest_hash": verification["latest_hash"],
            "genesis_hash": verification["genesis_hash"]
        },
        bcp_dr_summary={
            "total_snapshots": total_snapshots,
            "target_rpo_minutes": 15.0,
            "target_rto_minutes": 5.0,
            "latest_snapshot_code": latest_snapshot.snapshot_code if latest_snapshot else None,
            "latest_restore_status": latest_snapshot.restore_test_status if latest_snapshot else "N/A"
        },
        dpdp_summary={
            "total_consents": total_consents,
            "granted_consents": granted_consents,
            "statutory_act": "India Digital Personal Data Protection Act 2023",
            "dpo_designated": "AGT-COMPLY-01 (Compliance Officer)"
        },
        telemetry_summary={
            "db_size_formatted": telemetry["db_size_formatted"],
            "wal_size_formatted": telemetry["wal_size_formatted"],
            "wal_status": telemetry["wal_checkpoint_status"],
            "query_latency_ms": telemetry["db_query_latency_ms"],
            "system_health_score": telemetry["system_health_score"]
        }
    )


@router.get("/ledger", response_model=List[EnterpriseEventLedgerOut])
def get_event_ledger(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    aggregate_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns paginated tamper-evident cryptographic event ledger entries.
    """
    query = db.query(EnterpriseEventLedger)
    if aggregate_type:
        query = query.filter(EnterpriseEventLedger.aggregate_type == aggregate_type)
    
    entries = query.order_by(EnterpriseEventLedger.id.desc()).offset(offset).limit(limit).all()
    return entries


@router.post("/ledger/append", response_model=EnterpriseEventLedgerOut)
def append_event(
    payload: EnterpriseEventLedgerCreate,
    db: Session = Depends(get_db)
):
    """
    Appends an event to the immutable SHA-256 event ledger.
    """
    entry = append_event_ledger(
        db=db,
        aggregate_type=payload.aggregate_type,
        aggregate_id=payload.aggregate_id,
        event_type=payload.event_type,
        actor_name=payload.actor_name or "System Autonomous Controller",
        actor_role=payload.actor_role or "Director / System",
        department=payload.department or "Enterprise Core",
        payload=payload.payload or {}
    )
    return entry


@router.post("/ledger/verify", response_model=LedgerVerificationResult)
def verify_ledger(db: Session = Depends(get_db)):
    """
    Recomputes SHA-256 cryptographic chain starting from Genesis Block.
    Guarantees non-repudiation and detects data tampering.
    """
    result = verify_ledger_integrity(db)
    return LedgerVerificationResult(**result)


@router.get("/bcp-dr/snapshots", response_model=List[DisasterRecoverySnapshotOut])
def list_dr_snapshots(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lists disaster recovery and database backup snapshots.
    """
    snapshots = db.query(DisasterRecoverySnapshot).order_by(
        DisasterRecoverySnapshot.created_at.desc()
    ).limit(limit).all()
    return snapshots


@router.post("/bcp-dr/snapshots/create", response_model=DisasterRecoverySnapshotOut)
def create_backup_snapshot(
    payload: DisasterRecoverySnapshotCreate,
    db: Session = Depends(get_db)
):
    """
    Initiates hot SQLite database snapshot with SHA-256 integrity digest and AES-256-GCM envelope.
    """
    snapshot = create_database_backup_snapshot(
        db=db,
        backup_type=payload.backup_type,
        notes=payload.notes or "Manual snapshot initiated via Enterprise Operations Cockpit."
    )
    return snapshot


@router.post("/bcp-dr/snapshots/{snapshot_id}/test-restore", response_model=DRRestoreTestResponse)
def execute_dr_restore_drill(
    snapshot_id: int,
    db: Session = Depends(get_db)
):
    """
    Executes automated sandbox recovery drill validating RTO SLA (< 5 mins).
    """
    result = simulate_dr_restore_test(db, snapshot_id)
    return DRRestoreTestResponse(**result)


@router.get("/dpdp/consents", response_model=List[DPDPConsentRecordOut])
def list_dpdp_consents(
    principal_type: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Lists statutory consent records under the Digital Personal Data Protection (DPDP) Act 2023.
    """
    query = db.query(DPDPConsentRecord)
    if principal_type:
        query = query.filter(DPDPConsentRecord.data_principal_type == principal_type)
    if status_filter:
        query = query.filter(DPDPConsentRecord.consent_status == status_filter)
    
    records = query.order_by(DPDPConsentRecord.granted_at.desc()).limit(limit).all()
    return records


@router.post("/dpdp/consents", response_model=DPDPConsentRecordOut)
def record_consent(
    payload: DPDPConsentRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Registers affirmative consent under DPDP Act 2023 with cryptographic signature.
    """
    record = record_dpdp_consent(
        db=db,
        data_principal_name=payload.data_principal_name,
        data_principal_type=payload.data_principal_type,
        principal_identifier=payload.principal_identifier,
        purpose_category=payload.purpose_category,
        notice_reference=payload.notice_reference or "ADT/DPDP/NOTICE/2026/V1",
        consent_status=payload.consent_status or "Granted",
        audit_notes=payload.audit_notes or "Affirmative consent logged with cryptographic IP attestation."
    )
    return record


@router.get("/telemetry/live", response_model=SystemDiagnosticTelemetryOut)
def get_live_telemetry(db: Session = Depends(get_db)):
    """
    Returns real-time SQLite database, disk, WAL checkpoint, and memory RSS telemetry.
    """
    telemetry = harvest_system_telemetry(db)
    return SystemDiagnosticTelemetryOut(**telemetry)


@router.post("/telemetry/vacuum", response_model=DBVacuumResponse)
def execute_vacuum(db: Session = Depends(get_db)):
    """
    Executes WAL truncation checkpoint and database vacuum optimization.
    """
    result = execute_db_vacuum_and_checkpoint(db)
    return DBVacuumResponse(**result)
