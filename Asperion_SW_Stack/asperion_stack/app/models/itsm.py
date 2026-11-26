"""
Asperion Enterprise OS - Comprehensive IT Service Management (ITSM) Models
Aligned with ITIL v4, ISO 20000, ISO 27001, and SOC-2.
Covers CMDB Configuration Items, Incident/Problem KEDB, CAB Change Management,
Self-Healing Automated Runbook Fixes, Procurement Letters of Intent (LOIs), and SLAs.
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float
from app.database import Base

class ConfigurationItem(Base):
    """
    CMDB (Configuration Management Database) Node.
    Tracks all hardware, cloud compute, databases, network gear, microservices, and dependencies.
    """
    __tablename__ = "itsm_configuration_items"

    id = Column(Integer, primary_key=True, index=True)
    ci_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CI-SRV-PROD-01
    ci_name = Column(String(150), nullable=False) # Primary Core API Gateway
    ci_type = Column(String(50), nullable=False) # Cloud Server, Database, Kubernetes Cluster, API Gateway, Firewall, Laptop
    category = Column(String(50), default="Compute") # Compute, Database, Network, Security, Endpoint, Platform
    environment = Column(String(30), default="Production") # Production, Staging, Disaster Recovery, Development
    tier = Column(String(30), default="Tier-0 Mission Critical") # Tier-0 Mission Critical, Tier-1 Business Critical, Tier-2 Standard
    
    ip_address = Column(String(50), default="10.0.1.15")
    fqdn = Column(String(150), default="api.asperion.internal")
    cloud_provider = Column(String(50), default="AWS ap-south-1 (Mumbai)")
    
    status = Column(String(30), default="Operational", index=True) # Operational, Degraded, Under Maintenance, Offline
    health_score = Column(Float, default=99.5)
    cpu_utilization_pct = Column(Float, default=42.5)
    memory_utilization_pct = Column(Float, default=58.2)
    disk_utilization_pct = Column(Float, default=36.0)
    
    upstream_dependencies_json = Column(Text, default="[]") # JSON list of CIs this node depends on
    downstream_dependencies_json = Column(Text, default="[]") # JSON list of CIs dependent on this node
    
    technical_custodian = Column(String(100), default="DevOps & SRE Lead")
    patch_level = Column(String(50), default="Linux Kernel 6.8 / Hardened LTS")
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ITSMProblem(Base):
    """
    ITIL Problem Management & Known Error Database (KEDB).
    Conducts root-cause analyses (5-Whys, Fishbone) and publishes standard workarounds and permanent fixes.
    """
    __tablename__ = "itsm_problems"

    id = Column(Integer, primary_key=True, index=True)
    problem_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. PRB-2026-001
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Database Connection Pool")
    priority = Column(String(20), default="P2-High") # P1-Critical, P2-High, P3-Medium, P4-Low
    status = Column(String(40), default="Known Error (KEDB)", index=True) # RCA in Progress, Workaround Found, Known Error (KEDB), Permanent Fix Deployed, Closed
    
    impacted_ci_code = Column(String(50), default="CI-DB-PROD-01")
    root_cause_analysis = Column(Text, nullable=False) # Structured 5-Whys analysis
    temporary_workaround = Column(Text, nullable=False) # SOP instructions for L1/L2 support
    permanent_fix_plan = Column(Text, nullable=False) # Permanent architectural or code fix
    
    kedb_published = Column(Boolean, default=True) # Published to internal support KEDB
    assigned_engineer = Column(String(100), default="Principal Systems Architect")
    related_incidents_count = Column(Integer, default=3)
    
    identified_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ITSMChangeRequest(Base):
    """
    ITIL Change Enablement & Change Advisory Board (CAB).
    Manages normal, standard, and emergency changes with rollback procedures and risk assessments.
    """
    __tablename__ = "itsm_change_requests"

    id = Column(Integer, primary_key=True, index=True)
    cr_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CR-2026-0042
    title = Column(String(255), nullable=False)
    change_type = Column(String(30), default="Normal") # Normal, Standard, Emergency
    reason_for_change = Column(Text, nullable=False)
    impact_scope = Column(String(150), default="Core API Gateway & PostgreSQL Shard")
    
    risk_level = Column(String(20), default="Medium") # Low, Medium, High, Critical
    risk_score = Column(Integer, default=45) # 1 to 100
    cab_status = Column(String(30), default="Approved", index=True) # Draft, Submitted, Under CAB Review, Approved, Rejected, Scheduled, Completed, Rolled Back
    cab_review_notes = Column(Text, nullable=True)
    cab_approvers_json = Column(Text, default='["Varadi Vijay (Director)", "DevOps Lead", "SecOps Lead"]')
    
    implementation_plan = Column(Text, nullable=False) # Step-by-step rollout plan
    backout_rollback_plan = Column(Text, nullable=False) # Mandatory rollback procedure
    test_validation_procedure = Column(Text, nullable=False)
    
    scheduled_start_time = Column(DateTime, nullable=False)
    scheduled_end_time = Column(DateTime, nullable=False)
    outage_required = Column(Boolean, default=False)
    
    lead_implementer = Column(String(100), default="Release Engineering Lead")
    actual_outcome = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ITSMRunbookFix(Base):
    """
    Automated Self-Healing Fixes & Runbooks.
    Contains actionable remediation procedures triggered automatically or via supervised 1-click execution.
    """
    __tablename__ = "itsm_runbook_fixes"

    id = Column(Integer, primary_key=True, index=True)
    fix_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. FIX-RUN-01
    fix_name = Column(String(150), nullable=False)
    target_ci_type = Column(String(50), default="Relational Database")
    trigger_alert_pattern = Column(String(150), default="DB_CONNECTION_EXHAUSTION")
    
    procedure_steps_json = Column(Text, nullable=False) # JSON array of step titles & commands
    execution_type = Column(String(30), default="Supervised 1-Click") # Fully Automated, Supervised 1-Click, Manual SOP
    
    execution_count = Column(Integer, default=14)
    success_rate_pct = Column(Float, default=98.8)
    average_mttr_reduction_mins = Column(Float, default=24.5)
    
    last_executed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

class ITSMProcurementLOI(Base):
    """
    Official Letter of Intent (LOI) for IT Infrastructure & Procurement.
    Generates formal legally binding or non-binding letters of intent for hardware,
    cloud reservations, high-performance GPU compute, and colocation facilities.
    """
    __tablename__ = "itsm_procurement_lois"

    id = Column(Integer, primary_key=True, index=True)
    loi_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. LOI-IT-2026-001
    vendor_name = Column(String(150), nullable=False)
    vendor_address = Column(Text, nullable=False)
    vendor_contact_person = Column(String(100), nullable=False)
    vendor_email = Column(String(120), nullable=False)
    
    asset_category = Column(String(100), default="AI GPU Compute Nodes & Server Infrastructure")
    scope_of_procurement = Column(Text, nullable=False)
    equipment_specifications = Column(Text, nullable=False)
    estimated_contract_value_inr = Column(Float, nullable=False)
    payment_milestones = Column(Text, default="30% Advance on LOI Acceptance, 50% on Delivery & QC Verification, 20% post 30-day burn-in test")
    
    delivery_sla_weeks = Column(Integer, default=3)
    warranty_sla_terms = Column(Text, default="36-Month 24x7 4-Hour On-Site Replacement & Hardware OEM Guarantee")
    valid_until_date = Column(Date, nullable=False)
    
    director_signatory = Column(String(100), default="Varadi Vijay")
    director_title = Column(String(100), default="Founder & Sole Director")
    company_name = Column(String(150), default="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED")
    company_cin = Column(String(50), default="U85500KA2026OPC222069")
    registered_office = Column(Text, default="Horamavu, Bangalore North, Bangalore - 560043, Karnataka")
    
    status = Column(String(30), default="Approved & Issued", index=True) # Draft, Approved & Issued, Accepted by Vendor, Converted to PO, Archived
    generated_html = Column(Text, nullable=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class ITSMSLAContract(Base):
    """
    ITSM Operational Service Level Agreements.
    Defines uptime commitments, severity resolution targets, and penalty mechanisms.
    """
    __tablename__ = "itsm_sla_contracts"

    id = Column(Integer, primary_key=True, index=True)
    service_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. SLA-CORE-PLATFORM
    service_name = Column(String(150), nullable=False)
    service_tier = Column(String(50), default="Tier-0 Mission Critical")
    
    target_uptime_pct = Column(Float, default=99.95)
    current_monthly_uptime_pct = Column(Float, default=99.98)
    
    p1_response_mins = Column(Integer, default=15)
    p1_resolution_hours = Column(Float, default=2.0)
    p2_response_mins = Column(Integer, default=30)
    p2_resolution_hours = Column(Float, default=6.0)
    p3_resolution_hours = Column(Float, default=24.0)
    
    sla_penalty_clause = Column(Text, default="5% service credit per 0.1% breach below 99.95% monthly uptime threshold")
    status = Column(String(20), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
