"""
Asperion Enterprise OS - ISO Standards, QMS, Grievance Redressal & Worksheets Schemas
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ISOCertificationCreate(BaseModel):
    standard_code: str
    standard_name: str
    scope_description: str
    certificate_number: str
    accreditation_body: str = "IAF / NABCB Accredited Registrar (BSI India)"
    issue_date: date
    expiry_date: date
    surveillance_audit_due: date
    management_representative: str = "Management Representative (Director Varadi Vijay)"
    lead_auditor: str = "External Lead Auditor (BSI Group)"
    status: str = "Active & Certified"

class ISOCertificationOut(ISOCertificationCreate):
    id: int
    non_conformance_count: int
    created_at: datetime
    class Config:
        from_attributes = True

class ISOClauseControlCreate(BaseModel):
    control_code: str
    standard_code: str
    clause_number: str
    title: str
    control_domain: str
    requirement_summary: str
    implementation_mechanism: str
    evidence_vault_ref: Optional[str] = None
    maturity_level: str = "Level 4 - Managed & Measured"
    compliance_score_pct: float = 100.0
    control_owner: str

class ISOClauseControlOut(ISOClauseControlCreate):
    id: int
    is_compliant: bool
    updated_at: datetime
    class Config:
        from_attributes = True

class ISOAuditInspectionCreate(BaseModel):
    audit_code: str
    standard_code: str
    audit_type: str = "Internal Management Audit"
    audit_date: date
    audited_department: str = "Engineering, PMO, SecOps & Delivery"
    lead_auditor: str
    auditee_representative: str
    findings_summary: str
    major_nc_count: int = 0
    minor_nc_count: int = 0
    ofi_count: int = 1
    audit_outcome: str = "Conforming - Recommendation for Continuation"

class ISOAuditInspectionOut(ISOAuditInspectionCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ISOCorrectiveActionWorksheetCreate(BaseModel):
    capa_number: str
    source_type: str = "Audit Non-Conformance"
    standard_code: str
    problem_statement: str
    immediate_containment_action: str
    root_cause_analysis_method: str = "5 Whys Root Cause Analysis"
    root_cause_findings: str
    preventive_corrective_action: str
    action_owner: str
    target_closure_date: date

class ISOCorrectiveActionWorksheetOut(ISOCorrectiveActionWorksheetCreate):
    id: int
    actual_closure_date: Optional[date] = None
    effectiveness_verified: bool
    verifier_name: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class FormalGrievanceCreate(BaseModel):
    grievance_id: str
    stakeholder_type: str = "Client"
    stakeholder_name: str
    stakeholder_email: str
    category: str
    severity: str = "High"
    subject: str
    description: str
    assigned_redressal_officer: str = "Sole Director (Varadi Vijay)"
    statutory_sla_days: int = 7

class FormalGrievanceOut(FormalGrievanceCreate):
    id: int
    acknowledgment_sent: bool
    investigation_notes: Optional[str] = None
    resolution_details: Optional[str] = None
    closure_date: Optional[date] = None
    complainant_satisfied: bool
    csat_score: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class GrievanceResolutionUpdate(BaseModel):
    investigation_notes: str
    resolution_details: str
    complainant_satisfied: bool = True
    csat_score: int = 5
    status: str = "Resolved & Closed"
