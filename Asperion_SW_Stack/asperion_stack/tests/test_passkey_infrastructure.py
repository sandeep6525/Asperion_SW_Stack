"""
Asperion Enterprise OS - Comprehensive Test Suite for IT, Cloud & Passkey Access Infrastructure
Validates:
1. Infrastructure Executive Overview & Posture Telemetry
2. FIDO2 / WebAuthn Hardware Passkeys Directory & Registration
3. Zero-Trust Network Access (ZTNA) Guardrail Policies
4. Disaster Recovery (DR) Simulation Drills & ISO 22301 RTO/RPO SLAs
5. Hardware Fleet Inventory & Cloud Workload Verification
"""
import uuid
from datetime import datetime, date
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.infrastructure import (
    get_infrastructure_overview,
    list_passkeys, register_passkey,
    list_zero_trust_policies, create_zero_trust_policy,
    list_dr_simulations, record_dr_simulation,
    list_it_assets, list_cloud_accounts
)
from app.schemas.passkey_infrastructure import (
    PasskeyCredentialCreate, ZeroTrustPolicyCreate, DRSimulationTestCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_infrastructure_overview_telemetry(db_session):
    overview = get_infrastructure_overview(db=db_session)
    assert overview is not None
    assert overview["status"] == "HEALTHY"
    assert overview["registered_entity"] == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert overview["cin"] == "U85500KA2026OPC222069"
    assert "Horamavu, Bangalore" in overview["registered_office"]
    
    # Hardware assertions
    assert overview["hardware_assets"]["total"] >= 1
    assert overview["hardware_assets"]["assigned"] >= 1
    
    # Cloud assertions
    assert overview["cloud_infrastructure"]["active_accounts"] >= 1
    assert overview["cloud_infrastructure"]["total_monthly_spend_inr"] > 0
    assert "ap-south-1" in overview["cloud_infrastructure"]["primary_region"]
    assert "ap-south-2" in overview["cloud_infrastructure"]["warm_standby_region"]
    
    # Passkeys & ZTNA assertions
    assert overview["passkey_and_zero_trust"]["enrolled_passkeys"] >= 4
    assert overview["passkey_and_zero_trust"]["fido2_webauthn_enforced"] is True
    assert overview["passkey_and_zero_trust"]["active_ztna_policies"] >= 3
    assert "Horamavu HQ" in overview["passkey_and_zero_trust"]["wireguard_tunnel_status"]
    
    # Disaster Recovery assertions
    assert overview["disaster_recovery"]["dr_drills_completed"] >= 2
    assert overview["disaster_recovery"]["latest_rto_minutes"] <= overview["disaster_recovery"]["target_rto_minutes"]
    assert overview["disaster_recovery"]["latest_rpo_minutes"] <= overview["disaster_recovery"]["target_rpo_minutes"]
    assert overview["disaster_recovery"]["data_loss_detected"] is False

def test_passkeys_listing_and_registration(db_session):
    passkeys = list_passkeys(db=db_session)
    assert len(passkeys) >= 4
    
    emails = [p.user_email for p in passkeys]
    assert "varadivijay@asperiondigital.com" in emails
    assert "priya.nair@asperiondigital.com" in emails
    assert "arjun.sharma@asperiondigital.com" in emails
    assert "ananya.sen@asperiondigital.com" in emails
    
    # Verify founder key characteristics
    founder_pk = next(p for p in passkeys if p.user_email == "varadivijay@asperiondigital.com")
    assert "YubiKey 5" in founder_pk.authenticator_type
    assert founder_pk.sign_count >= 1
    assert founder_pk.user_verified is True
    assert "Compliant" in founder_pk.zero_trust_status
    
    # Register a new FIDO2 passkey
    new_id = f"fido2-test-{uuid.uuid4().hex[:8]}"
    created = register_passkey(
        item_in=PasskeyCredentialCreate(
            passkey_id=new_id,
            user_email="qa.lead@asperiondigital.com",
            user_name="Kavita Rao (QA Lead)",
            device_name="YubiKey 5 Nano NFC",
            authenticator_type="Cross-Platform Hardware FIDO2",
            public_key_spki="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAERANDOMTESTKEY...",
            user_verified=True
        ),
        db=db_session
    )
    assert created.id is not None
    assert created.passkey_id == new_id
    assert created.sign_count == 0
    assert created.status == "Active - Enforced"

def test_zero_trust_policies_enforcement(db_session):
    policies = list_zero_trust_policies(db=db_session)
    assert len(policies) >= 3
    
    codes = [p.policy_code for p in policies]
    assert "ZTNA-POL-001" in codes
    assert "ZTNA-POL-002" in codes
    assert "ZTNA-POL-003" in codes
    
    # Check Active Blocking and FIDO2 requirement
    for p in policies:
        assert p.fido2_passkey_required is True
        assert p.device_encryption_required is True
        assert p.enforcement_mode == "Active_Blocking"
        assert p.is_active is True
        
    # Create new ZTNA policy
    new_pol = create_zero_trust_policy(
        item_in=ZeroTrustPolicyCreate(
            policy_code=f"ZTNA-POL-{uuid.uuid4().hex[:4].upper()}",
            policy_name="Internal Vault API Zero-Trust Access Gate",
            target_resource="vault.asperion.in:8200",
            required_privilege="Security Officer",
            fido2_passkey_required=True,
            device_encryption_required=True,
            allowed_ip_ranges="10.8.0.0/24 (WireGuard Tunnel)",
            session_timeout_minutes=45,
            enforcement_mode="Active_Blocking"
        ),
        db=db_session
    )
    assert new_pol.id is not None
    assert new_pol.is_active is True

def test_dr_simulation_drills_and_sla(db_session):
    drills = list_dr_simulations(db=db_session)
    assert len(drills) >= 2
    
    codes = [d.test_code for d in drills]
    assert "DR-DRILL-2026-Q2" in codes
    assert "DR-DRILL-2026-Q1" in codes
    
    # Verify RTO and RPO meet or exceed SLA
    for d in drills:
        assert d.actual_rto_minutes <= d.target_rto_minutes, f"RTO violated in {d.test_code}"
        assert d.actual_rpo_minutes <= d.target_rpo_minutes, f"RPO violated in {d.test_code}"
        assert d.data_loss_detected is False
        assert "PASSED" in d.test_outcome
        
    # Record a new DR Drill test
    drill_in = DRSimulationTestCreate(
        test_code=f"DR-TEST-{uuid.uuid4().hex[:6].upper()}",
        test_type="Automated Standby Health Drill",
        simulated_scenario="Simulated API gateway failover to Hyderabad warm standby under synthetic load.",
        target_cluster="Secondary EKS Warm Standby (ap-south-2 Hyderabad)",
        database_backup_point=datetime.utcnow(),
        actual_rto_minutes=14.2,
        actual_rpo_minutes=1.5,
        data_loss_detected=False,
        test_outcome="PASSED - RTO/RPO SLA Met",
        conducted_by="Automated SecOps CI/CD Daemon"
    )
    recorded = record_dr_simulation(item_in=drill_in, db=db_session)
    assert recorded.id is not None
    assert recorded.actual_rto_minutes == 14.2
    assert recorded.data_loss_detected is False

def test_hardware_and_cloud_posture(db_session):
    assets = list_it_assets(db=db_session)
    assert len(assets) >= 1
    assert any(a.disk_encryption_enabled for a in assets)
    
    clouds = list_cloud_accounts(db=db_session)
    assert len(clouds) >= 1
    assert any(c.mfa_enforced_root for c in clouds)
