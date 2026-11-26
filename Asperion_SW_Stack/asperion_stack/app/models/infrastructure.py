"""
Asperion Enterprise OS - IT, Cloud Infrastructure, IAM & Passkey Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float
from app.database import Base

class ITAsset(Base):
    __tablename__ = "it_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, index=True) # ADT-LAP-001
    asset_type = Column(String(50), default="Laptop") # Laptop, Desktop, Server, Network Firewall, Monitor
    make_model = Column(String(100), default="MacBook Pro M3 / ThinkPad")
    serial_number = Column(String(100), unique=True)
    assigned_to_email = Column(String(100), nullable=True)
    assigned_user_name = Column(String(100), nullable=True)
    os_version = Column(String(50), default="macOS / Windows 11 Pro")
    disk_encryption_enabled = Column(Boolean, default=True) # BitLocker / FileVault
    edr_antivirus_installed = Column(Boolean, default=True)
    purchase_date = Column(Date, nullable=False)
    warranty_expiry_date = Column(Date, nullable=True)
    asset_status = Column(String(50), default="Assigned") # In Stock, Assigned, Under Repair, Retired, Lost
    created_at = Column(DateTime, default=datetime.utcnow)

class CloudAccount(Base):
    __tablename__ = "cloud_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    cloud_id = Column(String(50), unique=True, index=True) # ADT-AWS-PROD
    provider = Column(String(50), default="AWS") # AWS, Azure, GCP, Cloudflare, DigitalOcean
    account_subscription_id = Column(String(100))
    environment = Column(String(50), default="Production") # Production, Staging, Development
    primary_region = Column(String(50), default="ap-south-1 (Mumbai)")
    technical_owner = Column(String(100), default="CloudOps Lead")
    monthly_budget_inr = Column(Float, default=50000.0)
    current_month_spend_inr = Column(Float, default=32000.0)
    mfa_enforced_root = Column(Boolean, default=True)
    backup_enabled = Column(Boolean, default=True)
    status = Column(String(50), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

class IAMCredential(Base):
    __tablename__ = "iam_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    credential_id = Column(String(50), unique=True, index=True) # ADT-IAM-001
    user_email = Column(String(100), index=True)
    user_name = Column(String(100))
    system = Column(String(100)) # AWS Console, GitHub Org, Google Workspace, Jira/Confluence, Production DB
    role_assigned = Column(String(100), default="Developer")
    privilege_level = Column(String(50), default="Standard") # Standard, Elevated, Admin/Superadmin
    mfa_enabled = Column(Boolean, default=True)
    passkey_fido2_enabled = Column(Boolean, default=True)
    passwordless_enforced = Column(Boolean, default=True)
    last_access_review_date = Column(Date, nullable=True)
    review_status = Column(String(50), default="Approved") # Approved, Flagged, Revoked
    created_at = Column(DateTime, default=datetime.utcnow)

class SaaSLicense(Base):
    __tablename__ = "saas_licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    software_name = Column(String(100), nullable=False) # Google Workspace, GitHub Enterprise, Slack, JetBrains, Figma
    vendor = Column(String(100))
    license_type = Column(String(50), default="Per User / Monthly")
    seats_purchased = Column(Integer, default=10)
    seats_assigned = Column(Integer, default=8)
    annual_cost_inr = Column(Float, default=120000.0)
    renewal_date = Column(Date, nullable=False)
    billing_owner = Column(String(100), default="Finance & Admin Lead")
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class BackupDRPlan(Base):
    __tablename__ = "backup_dr_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    system_name = Column(String(100), nullable=False) # Production Database, Code Repositories, Customer Data
    backup_frequency = Column(String(50), default="Daily Automated Snapshot")
    retention_period_days = Column(Integer, default=90)
    storage_target = Column(String(100), default="AWS S3 Glacier (Cross-Region Encrypted)")
    rpo_target_hours = Column(Float, default=1.0) # Recovery Point Objective
    rto_target_hours = Column(Float, default=4.0) # Recovery Time Objective
    last_restore_test_date = Column(Date, nullable=True)
    test_result = Column(String(50), default="Successful")
    tested_by = Column(String(100), default="DevOps Lead")
    created_at = Column(DateTime, default=datetime.utcnow)

class CertificateSecret(Base):
    __tablename__ = "certificates_secrets"
    
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(50), default="SSL/TLS Certificate") # SSL/TLS Certificate, OAuth Secret, API Key, SSH Master Key
    identifier_name = Column(String(255), nullable=False) # e.g. "*.asperion.in Wildcard Cert", "AWS KMS Master Key"
    environment = Column(String(50), default="Production")
    issuer = Column(String(100), default="Let's Encrypt / DigiCert / AWS")
    expiry_date = Column(Date, nullable=False)
    auto_renew_enabled = Column(Boolean, default=True)
    alert_lead_time_days = Column(Integer, default=30)
    status = Column(String(50), default="Active") # Active, Expiring Soon, Expired, Revoked
    owner_email = Column(String(100), default="devops@asperion.in")

class ITProvisioningChecklist(Base):
    __tablename__ = "it_provisioning_checklists"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), index=True)
    employee_name = Column(String(100), nullable=False)
    process_type = Column(String(50), default="Onboarding") # Onboarding, Offboarding
    google_workspace_provisioned = Column(Boolean, default=True)
    github_org_access_granted = Column(Boolean, default=True)
    aws_iam_identity_center_granted = Column(Boolean, default=False)
    hardware_laptop_issued = Column(Boolean, default=True)
    fido2_passkey_enrolled = Column(Boolean, default=True)
    vpn_network_access_granted = Column(Boolean, default=True)
    security_awareness_completed = Column(Boolean, default=True)
    signoff_status = Column(String(50), default="Completed")
    completed_date = Column(Date, nullable=True)
    admin_lead = Column(String(100), default="IT Admin Lead")

