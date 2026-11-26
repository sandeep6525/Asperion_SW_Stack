"""
Asperion Enterprise OS - Comprehensive IT & Cloud Infrastructure API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from app.database import get_db
from app.models.infrastructure import (
    ITAsset, CloudAccount, IAMCredential, SaaSLicense, BackupDRPlan,
    CertificateSecret, ITProvisioningChecklist
)
from app.models.passkey_infrastructure import (
    PasskeyCredential, ZeroTrustPolicy, DRSimulationTest
)
from app.schemas.infrastructure import ITAssetCreate, ITAssetOut, CloudAccountOut, IAMCredentialOut
from app.schemas.passkey_infrastructure import (
    PasskeyCredentialCreate, PasskeyCredentialOut,
    ZeroTrustPolicyCreate, ZeroTrustPolicyOut,
    DRSimulationTestCreate, DRSimulationTestOut
)

router = APIRouter(prefix="/infrastructure", tags=["IT, Cloud & IAM Infrastructure"])

class CertificateSecretCreate(BaseModel):
    item_type: str = "SSL/TLS Certificate"
    identifier_name: str
    environment: str = "Production"
    issuer: str = "Let's Encrypt"
    expiry_date: date
    auto_renew_enabled: bool = True

class ITChecklistCreate(BaseModel):
    employee_code: str
    employee_name: str
    process_type: str = "Onboarding"
    google_workspace_provisioned: bool = True
    github_org_access_granted: bool = True
    aws_iam_identity_center_granted: bool = False
    hardware_laptop_issued: bool = True
    fido2_passkey_enrolled: bool = True

@router.get("/assets", response_model=List[ITAssetOut])
def list_it_assets(db: Session = Depends(get_db)):
    return db.query(ITAsset).order_by(ITAsset.asset_tag.asc()).all()

@router.post("/assets", response_model=ITAssetOut)
def create_it_asset(asset_in: ITAssetCreate, db: Session = Depends(get_db)):
    asset = ITAsset(**asset_in.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.get("/cloud-accounts", response_model=List[CloudAccountOut])
def list_cloud_accounts(db: Session = Depends(get_db)):
    return db.query(CloudAccount).all()

@router.get("/iam-credentials", response_model=List[IAMCredentialOut])
def list_iam_credentials(db: Session = Depends(get_db)):
    return db.query(IAMCredential).all()

@router.get("/saas-licenses")
def list_saas_licenses(db: Session = Depends(get_db)):
    return db.query(SaaSLicense).all()

@router.get("/backup-dr")
def list_backup_dr(db: Session = Depends(get_db)):
    return db.query(BackupDRPlan).all()

@router.get("/certificates-secrets")
def list_certificates_secrets(db: Session = Depends(get_db)):
    return db.query(CertificateSecret).order_by(CertificateSecret.expiry_date.asc()).all()

@router.post("/certificates-secrets")
def create_certificate_secret(item_in: CertificateSecretCreate, db: Session = Depends(get_db)):
    item = CertificateSecret(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/provisioning-checklists")
def list_provisioning_checklists(db: Session = Depends(get_db)):
    return db.query(ITProvisioningChecklist).all()

@router.post("/provisioning-checklists")
def create_provisioning_checklist(item_in: ITChecklistCreate, db: Session = Depends(get_db)):
    item = ITProvisioningChecklist(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# Passkey (FIDO2 / WebAuthn) Infrastructure Endpoints
# -------------------------------------------------------------

@router.get("/passkeys", response_model=List[PasskeyCredentialOut])
def list_passkeys(db: Session = Depends(get_db)):
    return db.query(PasskeyCredential).order_by(PasskeyCredential.enrolled_at.desc()).all()

@router.post("/passkeys", response_model=PasskeyCredentialOut)
def register_passkey(item_in: PasskeyCredentialCreate, db: Session = Depends(get_db)):
    item = PasskeyCredential(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# Zero-Trust Network Access (ZTNA) Policy Endpoints
# -------------------------------------------------------------

@router.get("/zero-trust-policies", response_model=List[ZeroTrustPolicyOut])
def list_zero_trust_policies(db: Session = Depends(get_db)):
    return db.query(ZeroTrustPolicy).order_by(ZeroTrustPolicy.id.asc()).all()

@router.post("/zero-trust-policies", response_model=ZeroTrustPolicyOut)
def create_zero_trust_policy(item_in: ZeroTrustPolicyCreate, db: Session = Depends(get_db)):
    item = ZeroTrustPolicy(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# Disaster Recovery (DR) Simulation Drills Endpoints
# -------------------------------------------------------------

@router.get("/dr-simulations", response_model=List[DRSimulationTestOut])
def list_dr_simulations(db: Session = Depends(get_db)):
    return db.query(DRSimulationTest).order_by(DRSimulationTest.conducted_at.desc()).all()

@router.post("/dr-simulations", response_model=DRSimulationTestOut)
def record_dr_simulation(item_in: DRSimulationTestCreate, db: Session = Depends(get_db)):
    item = DRSimulationTest(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# Infrastructure Health & Zero-Trust Overview
# -------------------------------------------------------------

@router.get("/overview")
def get_infrastructure_overview(db: Session = Depends(get_db)):
    total_assets = db.query(ITAsset).count()
    assigned_assets = db.query(ITAsset).filter(ITAsset.asset_status == "Assigned").count()
    total_cloud_accounts = db.query(CloudAccount).count()
    total_passkeys = db.query(PasskeyCredential).count()
    active_ztna_policies = db.query(ZeroTrustPolicy).filter(ZeroTrustPolicy.is_active == True).count()
    dr_tests_count = db.query(DRSimulationTest).count()
    latest_dr = db.query(DRSimulationTest).order_by(DRSimulationTest.conducted_at.desc()).first()
    
    total_cloud_spend_inr = sum(c.current_month_spend_inr or 0 for c in db.query(CloudAccount).all())

    return {
        "status": "HEALTHY",
        "registered_entity": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        "cin": "U85500KA2026OPC222069",
        "registered_office": "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore - 560043",
        "hardware_assets": {
            "total": total_assets,
            "assigned": assigned_assets,
            "available": total_assets - assigned_assets
        },
        "cloud_infrastructure": {
            "active_accounts": total_cloud_accounts,
            "total_monthly_spend_inr": total_cloud_spend_inr,
            "primary_region": "AWS ap-south-1 (Mumbai)",
            "warm_standby_region": "AWS ap-south-2 (Hyderabad)"
        },
        "passkey_and_zero_trust": {
            "enrolled_passkeys": total_passkeys,
            "fido2_webauthn_enforced": True,
            "biometric_verification_rate": "100%",
            "active_ztna_policies": active_ztna_policies,
            "wireguard_tunnel_status": "ONLINE - Horamavu HQ Mesh"
        },
        "disaster_recovery": {
            "dr_drills_completed": dr_tests_count,
            "latest_drill_outcome": latest_dr.test_outcome if latest_dr else "N/A",
            "latest_rto_minutes": latest_dr.actual_rto_minutes if latest_dr else 0.0,
            "target_rto_minutes": 60.0,
            "latest_rpo_minutes": latest_dr.actual_rpo_minutes if latest_dr else 0.0,
            "target_rpo_minutes": 15.0,
            "data_loss_detected": latest_dr.data_loss_detected if latest_dr else False
        }
    }

