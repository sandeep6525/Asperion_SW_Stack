"""
Asperion Enterprise OS - Comprehensive Test Suite for Developer Platform & Statutory Tax Challans
Tests organization developer accounts, secret rotation, and statutory tax deposit reconciliation.
"""
import pytest
from datetime import date, timedelta
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.developer_platform import (
    DeveloperPlatformAccount, DeveloperEnvironmentSecret, StatutoryChallanFiling
)
from app.api.developer_platform import (
    get_developer_ecosystem_overview, list_developer_accounts, create_developer_account,
    list_developer_secrets, register_developer_secret, rotate_developer_secret,
    list_statutory_challans, create_statutory_challan, get_tax_filing_summary
)
from app.schemas.developer_platform import (
    DeveloperPlatformAccountCreate, DeveloperEnvironmentSecretCreate, StatutoryChallanFilingCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_developer_ecosystem_overview(db_session):
    overview = get_developer_ecosystem_overview(db=db_session)
    assert overview.status == "success"
    assert overview.total_accounts >= 7
    assert overview.verified_accounts >= 6
    assert overview.fido2_compliance_pct >= 90.0
    assert overview.total_secrets >= 3

def test_developer_accounts_list_and_create(db_session):
    accounts = list_developer_accounts(db=db_session)
    assert len(accounts) >= 7

    platform_names = [a.platform_name for a in accounts]
    assert "Google Play Console" in platform_names
    assert "Apple Developer Program" in platform_names
    assert "GitHub Organization" in platform_names
    assert "Microsoft Entra ID" in platform_names

    # Clean up test code if exists
    db_session.query(DeveloperPlatformAccount).filter(DeveloperPlatformAccount.account_code == "DEV-ACC-TEST-001").delete()
    db_session.commit()

    # Create new account
    new_acc = DeveloperPlatformAccountCreate(
        account_code="DEV-ACC-TEST-001",
        platform_name="Anthropic Claude API Enterprise",
        admin_email="ai-admin@asperion.in",
        organization_id="org_anthropic_asperion",
        duns_linked=True,
        fido2_mfa_enforced=True,
        verification_status="Verified Organization",
        tier_or_plan="Scale Tier",
        annual_fee_inr=50000.0
    )
    created = create_developer_account(account_in=new_acc, db=db_session)
    assert created.account_code == "DEV-ACC-TEST-001"
    assert created.platform_name == "Anthropic Claude API Enterprise"

def test_developer_secrets_and_rotation(db_session):
    secrets = list_developer_secrets(db=db_session)
    assert len(secrets) >= 3

    target_sec = secrets[0]
    initial_due = target_sec.next_rotation_due

    # Test rotation endpoint
    rotated = rotate_developer_secret(
        secret_id=target_sec.id,
        new_sha256_fingerprint="e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4",
        db=db_session
    )
    assert rotated.status == "Active & Compliant"
    assert rotated.last_rotated_at is not None
    assert rotated.next_rotation_due > date.today()
    assert rotated.sha256_fingerprint.startswith("e5f4a3b2")

def test_statutory_challan_filings_and_summary(db_session):
    challans = list_statutory_challans(db=db_session)
    assert len(challans) >= 4

    types = [c.filing_type for c in challans]
    assert "GSTR-3B" in types
    assert "TDS Challan 281" in types
    assert "Advance Tax Installment 1" in types
    assert "Karnataka PT Form 5" in types

    summary = get_tax_filing_summary(db=db_session)
    assert summary.status == "success"
    assert summary.total_challans_filed >= 4
    assert summary.total_tax_deposited_inr > 100000.0
    assert summary.reconciliation_rate_pct == 100.0
