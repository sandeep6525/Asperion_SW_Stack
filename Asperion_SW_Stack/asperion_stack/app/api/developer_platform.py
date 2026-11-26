"""
Asperion Enterprise OS - Developer Platform & Statutory Tax Challans API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, timedelta

from app.database import get_db
from app.models.developer_platform import (
    DeveloperPlatformAccount, DeveloperEnvironmentSecret, StatutoryChallanFiling
)
from app.schemas.developer_platform import (
    DeveloperPlatformAccountCreate, DeveloperPlatformAccountOut,
    DeveloperEnvironmentSecretCreate, DeveloperEnvironmentSecretOut,
    StatutoryChallanFilingCreate, StatutoryChallanFilingOut,
    DeveloperEcosystemOverviewOut, TaxFilingSummaryOut
)

router = APIRouter(prefix="/developer-platform", tags=["Developer Ecosystem & Statutory Tax Challans"])

# -----------------------------------------------------------------------------
# DEVELOPER PLATFORM ACCOUNTS
# -----------------------------------------------------------------------------

@router.get("/overview", response_model=DeveloperEcosystemOverviewOut)
def get_developer_ecosystem_overview(db: Session = Depends(get_db)):
    """
    Returns high-level governance status for Apple, Google, GitHub, Microsoft, Meta, and AWS platforms.
    """
    accounts = db.query(DeveloperPlatformAccount).all()
    secrets = db.query(DeveloperEnvironmentSecret).all()

    total_acc = len(accounts)
    verified = sum(1 for a in accounts if a.verification_status == "Verified Organization")
    fido2_mfa = sum(1 for a in accounts if a.fido2_mfa_enforced)
    fido2_pct = round((fido2_mfa / total_acc) * 100, 1) if total_acc > 0 else 100.0

    today = date.today()
    due_rot = sum(1 for s in secrets if s.next_rotation_due <= today or s.status == "Rotation Due")

    return DeveloperEcosystemOverviewOut(
        status="success",
        total_accounts=total_acc,
        verified_accounts=verified,
        fido2_compliance_pct=fido2_pct,
        total_secrets=len(secrets),
        secrets_due_rotation=due_rot,
        accounts=accounts,
        secrets=secrets
    )

@router.get("/accounts", response_model=List[DeveloperPlatformAccountOut])
def list_developer_accounts(db: Session = Depends(get_db)):
    return db.query(DeveloperPlatformAccount).order_by(DeveloperPlatformAccount.id.asc()).all()

@router.post("/accounts", response_model=DeveloperPlatformAccountOut, status_code=201)
def create_developer_account(account_in: DeveloperPlatformAccountCreate, db: Session = Depends(get_db)):
    exists = db.query(DeveloperPlatformAccount).filter(DeveloperPlatformAccount.account_code == account_in.account_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Developer account code already exists")
    
    account = DeveloperPlatformAccount(**account_in.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.get("/secrets", response_model=List[DeveloperEnvironmentSecretOut])
def list_developer_secrets(db: Session = Depends(get_db)):
    return db.query(DeveloperEnvironmentSecret).order_by(DeveloperEnvironmentSecret.next_rotation_due.asc()).all()

@router.post("/secrets", response_model=DeveloperEnvironmentSecretOut, status_code=201)
def register_developer_secret(secret_in: DeveloperEnvironmentSecretCreate, db: Session = Depends(get_db)):
    exists = db.query(DeveloperEnvironmentSecret).filter(DeveloperEnvironmentSecret.secret_code == secret_in.secret_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Secret code already exists")
    
    secret = DeveloperEnvironmentSecret(**secret_in.model_dump())
    db.add(secret)
    db.commit()
    db.refresh(secret)
    return secret

@router.patch("/secrets/{secret_id}/rotate", response_model=DeveloperEnvironmentSecretOut)
def rotate_developer_secret(secret_id: int, new_sha256_fingerprint: Optional[str] = None, db: Session = Depends(get_db)):
    secret = db.query(DeveloperEnvironmentSecret).filter(DeveloperEnvironmentSecret.id == secret_id).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret record not found")
    
    secret.last_rotated_at = datetime.utcnow()
    secret.next_rotation_due = date.today() + timedelta(days=secret.rotation_cadence_days)
    secret.status = "Active & Compliant"
    if new_sha256_fingerprint:
        secret.sha256_fingerprint = new_sha256_fingerprint
        
    db.commit()
    db.refresh(secret)
    return secret

# -----------------------------------------------------------------------------
# STATUTORY TAX CHALLANS & DEPOSITS
# -----------------------------------------------------------------------------

@router.get("/tax-challans", response_model=List[StatutoryChallanFilingOut])
def list_statutory_challans(filing_type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(StatutoryChallanFiling)
    if filing_type and filing_type != "ALL":
        query = query.filter(StatutoryChallanFiling.filing_type == filing_type)
    return query.order_by(StatutoryChallanFiling.statutory_due_date.desc()).all()

@router.post("/tax-challans", response_model=StatutoryChallanFilingOut, status_code=201)
def create_statutory_challan(challan_in: StatutoryChallanFilingCreate, db: Session = Depends(get_db)):
    exists = db.query(StatutoryChallanFiling).filter(StatutoryChallanFiling.challan_code == challan_in.challan_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="Statutory challan code already exists")
    
    challan = StatutoryChallanFiling(**challan_in.model_dump())
    db.add(challan)
    db.commit()
    db.refresh(challan)
    return challan

@router.get("/tax-summary", response_model=TaxFilingSummaryOut)
def get_tax_filing_summary(db: Session = Depends(get_db)):
    challans = db.query(StatutoryChallanFiling).all()
    total_paid = sum(c.tax_amount_paid for c in challans)
    reconciled = sum(1 for c in challans if c.reconciliation_status == "Reconciled with Portal")
    reconcile_rate = round((reconciled / len(challans)) * 100, 1) if challans else 100.0
    
    today = date.today()
    upcoming = sum(1 for c in challans if c.statutory_due_date >= today and c.reconciliation_status != "Reconciled with Portal")

    return TaxFilingSummaryOut(
        status="success",
        total_challans_filed=len(challans),
        total_tax_deposited_inr=round(total_paid, 2),
        reconciliation_rate_pct=reconcile_rate,
        upcoming_due_count=upcoming,
        challans=challans
    )
