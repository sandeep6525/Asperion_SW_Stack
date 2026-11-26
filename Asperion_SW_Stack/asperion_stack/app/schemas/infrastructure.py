"""
Asperion Enterprise OS - IT & Cloud Infrastructure Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class ITAssetCreate(BaseModel):
    asset_tag: str
    asset_type: str = "Laptop"
    make_model: str = "MacBook Pro M3 / ThinkPad"
    serial_number: str
    assigned_to_email: Optional[str] = None
    assigned_user_name: Optional[str] = None
    purchase_date: date
    warranty_expiry_date: Optional[date] = None

class ITAssetOut(ITAssetCreate):
    id: int
    disk_encryption_enabled: bool
    edr_antivirus_installed: bool
    asset_status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CloudAccountOut(BaseModel):
    id: int
    cloud_id: str
    provider: str
    environment: str
    primary_region: str
    technical_owner: str
    monthly_budget_inr: float
    current_month_spend_inr: float
    mfa_enforced_root: bool
    status: str
    class Config:
        from_attributes = True

class IAMCredentialOut(BaseModel):
    id: int
    credential_id: str
    user_email: str
    user_name: Optional[str]
    system: str
    role_assigned: str
    privilege_level: str
    mfa_enabled: bool
    passkey_fido2_enabled: bool
    passwordless_enforced: bool
    review_status: str
    class Config:
        from_attributes = True
