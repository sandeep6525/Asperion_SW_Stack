"""
Asperion Enterprise OS - IT Service Management (ITSM) Schemas
Pydantic schemas for CMDB, Problem KEDB, CAB Changes, Self-Healing Runbooks,
Procurement Letters of Intent (LOIs), and SLAs.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, date

# -------------------------------------------------------------
# CMDB Configuration Items
# -------------------------------------------------------------
class ConfigurationItemBase(BaseModel):
    ci_code: str
    ci_name: str
    ci_type: str
    category: str = "Compute"
    environment: str = "Production"
    tier: str = "Tier-0 Mission Critical"
    ip_address: Optional[str] = "10.0.1.15"
    fqdn: Optional[str] = "api.asperion.internal"
    cloud_provider: Optional[str] = "AWS ap-south-1 (Mumbai)"
    status: str = "Operational"
    health_score: float = 99.5
    cpu_utilization_pct: float = 42.5
    memory_utilization_pct: float = 58.2
    disk_utilization_pct: float = 36.0
    upstream_dependencies_json: Optional[str] = "[]"
    downstream_dependencies_json: Optional[str] = "[]"
    technical_custodian: Optional[str] = "DevOps & SRE Lead"
    patch_level: Optional[str] = "Linux Kernel 6.8 / Hardened LTS"

class ConfigurationItemCreate(ConfigurationItemBase):
    pass

class ConfigurationItemOut(ConfigurationItemBase):
    id: int
    last_heartbeat: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------
# Problem Management & KEDB
# -------------------------------------------------------------
class ITSMProblemBase(BaseModel):
    problem_code: str
    title: str
    category: str = "Database Connection Pool"
    priority: str = "P2-High"
    status: str = "Known Error (KEDB)"
    impacted_ci_code: str = "CI-DB-PROD-01"
    root_cause_analysis: str
    temporary_workaround: str
    permanent_fix_plan: str
    kedb_published: bool = True
    assigned_engineer: Optional[str] = "Principal Systems Architect"
    related_incidents_count: int = 3

class ITSMProblemCreate(ITSMProblemBase):
    pass

class ITSMProblemOut(ITSMProblemBase):
    id: int
    identified_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------
# Change Enablement & CAB
# -------------------------------------------------------------
class ITSMChangeRequestBase(BaseModel):
    cr_code: str
    title: str
    change_type: str = "Normal"
    reason_for_change: str
    impact_scope: str = "Core API Gateway & PostgreSQL Shard"
    risk_level: str = "Medium"
    risk_score: int = 45
    cab_status: str = "Approved"
    cab_review_notes: Optional[str] = None
    cab_approvers_json: Optional[str] = '["Varadi Vijay (Director)", "DevOps Lead", "SecOps Lead"]'
    implementation_plan: str
    backout_rollback_plan: str
    test_validation_procedure: str
    scheduled_start_time: datetime
    scheduled_end_time: datetime
    outage_required: bool = False
    lead_implementer: str = "Release Engineering Lead"
    actual_outcome: Optional[str] = None

class ITSMChangeRequestCreate(ITSMChangeRequestBase):
    pass

class ITSMChangeReviewRequest(BaseModel):
    action: str = Field(..., description="'APPROVE', 'REJECT', or 'SCHEDULE'")
    reviewer_name: str = "Varadi Vijay"
    reviewer_role: str = "Founder & Sole Director"
    review_notes: Optional[str] = "Approved by CAB for scheduled execution window."

class ITSMChangeRequestOut(ITSMChangeRequestBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------
# Automated Runbook Fixes
# -------------------------------------------------------------
class ITSMRunbookFixBase(BaseModel):
    fix_code: str
    fix_name: str
    target_ci_type: str = "Relational Database"
    trigger_alert_pattern: str = "DB_CONNECTION_EXHAUSTION"
    procedure_steps_json: str
    execution_type: str = "Supervised 1-Click"
    execution_count: int = 14
    success_rate_pct: float = 98.8
    average_mttr_reduction_mins: float = 24.5
    status: str = "Active"

class ITSMRunbookFixCreate(ITSMRunbookFixBase):
    pass

class ITSMRunbookFixOut(ITSMRunbookFixBase):
    id: int
    last_executed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ITSMRunbookExecuteResponse(BaseModel):
    status: str = "success"
    message: str
    fix_code: str
    target_node: str
    execution_timestamp: str
    output_log: List[str]
    health_restored: bool = True

# -------------------------------------------------------------
# IT Procurement Letter of Intent (LOI)
# -------------------------------------------------------------
class ITSMProcurementLOIBase(BaseModel):
    loi_number: str
    vendor_name: str
    vendor_address: str
    vendor_contact_person: str
    vendor_email: str
    asset_category: str = "AI GPU Compute Nodes & Server Infrastructure"
    scope_of_procurement: str
    equipment_specifications: str
    estimated_contract_value_inr: float
    payment_milestones: Optional[str] = "30% Advance on LOI Acceptance, 50% on Delivery & QC Verification, 20% post 30-day burn-in test"
    delivery_sla_weeks: int = 3
    warranty_sla_terms: Optional[str] = "36-Month 24x7 4-Hour On-Site Replacement & Hardware OEM Guarantee"
    valid_until_date: date
    director_signatory: str = "Varadi Vijay"
    director_title: str = "Founder & Sole Director"
    company_name: str = "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    company_cin: str = "U85500KA2026OPC222069"
    registered_office: str = "Horamavu, Bangalore North, Bangalore - 560043, Karnataka"
    status: str = "Approved & Issued"

class ITSMProcurementLOICreate(ITSMProcurementLOIBase):
    pass

class ITSMProcurementLOIOut(ITSMProcurementLOIBase):
    id: int
    generated_html: Optional[str] = None
    issued_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# -------------------------------------------------------------
# SLA Contracts
# -------------------------------------------------------------
class ITSMSLAContractBase(BaseModel):
    service_code: str
    service_name: str
    service_tier: str = "Tier-0 Mission Critical"
    target_uptime_pct: float = 99.95
    current_monthly_uptime_pct: float = 99.98
    p1_response_mins: int = 15
    p1_resolution_hours: float = 2.0
    p2_response_mins: int = 30
    p2_resolution_hours: float = 6.0
    p3_resolution_hours: float = 24.0
    sla_penalty_clause: Optional[str] = "5% service credit per 0.1% breach below 99.95% monthly uptime threshold"
    status: str = "Active"

class ITSMSLAContractCreate(ITSMSLAContractBase):
    pass

class ITSMSLAContractOut(ITSMSLAContractBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
