"""
Asperion Enterprise OS - Expanded IT, Cloud & Passkey Access Infrastructure Schemas
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class PasskeyCredentialCreate(BaseModel):
    passkey_id: str
    user_email: str
    user_name: str
    device_name: str = "MacBook Touch ID / YubiKey 5C NFC"
    authenticator_type: str = "Platform Authenticator (TouchID / Windows Hello)"
    public_key_spki: str
    user_verified: bool = True

class PasskeyCredentialOut(PasskeyCredentialCreate):
    id: int
    sign_count: int
    enrolled_at: datetime
    last_used_at: datetime
    status: str
    zero_trust_status: str
    class Config:
        from_attributes = True

class ZeroTrustPolicyCreate(BaseModel):
    policy_code: str
    policy_name: str
    target_resource: str
    required_privilege: str = "Elevated / Superadmin"
    fido2_passkey_required: bool = True
    device_encryption_required: bool = True
    allowed_ip_ranges: str = "Horamavu HQ Office IP / ZTNA WireGuard Tunnel"
    session_timeout_minutes: int = 60
    enforcement_mode: str = "Active_Blocking"

class ZeroTrustPolicyOut(ZeroTrustPolicyCreate):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class DRSimulationTestCreate(BaseModel):
    test_code: str
    test_type: str = "Full Failover Simulation"
    simulated_scenario: str
    target_cluster: str = "Secondary EKS Warm Standby (ap-south-2 Hyderabad)"
    database_backup_point: datetime
    actual_rto_minutes: float
    actual_rpo_minutes: float
    data_loss_detected: bool = False
    test_outcome: str = "PASSED - RTO/RPO SLA Met"
    conducted_by: str = "Head of Infrastructure (Priya Nair)"

class DRSimulationTestOut(DRSimulationTestCreate):
    id: int
    target_rto_minutes: float
    target_rpo_minutes: float
    conducted_at: datetime
    report_url: str
    class Config:
        from_attributes = True
