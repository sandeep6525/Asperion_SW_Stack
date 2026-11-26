"""
Asperion Enterprise OS - Developer Platform & Statutory Tax Challan Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class DeveloperPlatformAccountBase(BaseModel):
    account_code: str
    platform_name: str
    account_type: str = "Organization / Corporate Entity"
    admin_email: str
    organization_id: Optional[str] = None
    duns_linked: bool = True
    fido2_mfa_enforced: bool = True
    verification_status: str = "Verified Organization"
    tier_or_plan: str = "Enterprise"
    annual_fee_inr: float = 0.0
    renewal_date: Optional[date] = None
    notes: Optional[str] = None

class DeveloperPlatformAccountCreate(DeveloperPlatformAccountBase):
    pass

class DeveloperPlatformAccountOut(DeveloperPlatformAccountBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class DeveloperEnvironmentSecretBase(BaseModel):
    secret_code: str
    secret_name: str
    target_environment: str = "Production"
    platform: str
    sha256_fingerprint: str
    rotation_cadence_days: int = 90
    last_rotated_at: Optional[datetime] = None
    next_rotation_due: date
    status: str = "Active & Compliant"

class DeveloperEnvironmentSecretCreate(DeveloperEnvironmentSecretBase):
    pass

class DeveloperEnvironmentSecretOut(DeveloperEnvironmentSecretBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class StatutoryChallanFilingBase(BaseModel):
    challan_code: str
    filing_type: str
    statutory_authority: str
    assessment_year: str = "2027-2028"
    tax_period: str
    statutory_due_date: date
    actual_filing_date: Optional[date] = None
    challan_cin_arn: Optional[str] = None
    bsr_code: str = "0001234"
    tax_amount_paid: float
    interest_penalty: float = 0.0
    payment_mode: str = "NEFT / NetBanking"
    reconciliation_status: str = "Reconciled with Portal"

class StatutoryChallanFilingCreate(StatutoryChallanFilingBase):
    pass

class StatutoryChallanFilingOut(StatutoryChallanFilingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class DeveloperEcosystemOverviewOut(BaseModel):
    status: str
    total_accounts: int
    verified_accounts: int
    fido2_compliance_pct: float
    total_secrets: int
    secrets_due_rotation: int
    accounts: List[DeveloperPlatformAccountOut]
    secrets: List[DeveloperEnvironmentSecretOut]

class TaxFilingSummaryOut(BaseModel):
    status: str
    total_challans_filed: int
    total_tax_deposited_inr: float
    reconciliation_rate_pct: float
    upcoming_due_count: int
    challans: List[StatutoryChallanFilingOut]
