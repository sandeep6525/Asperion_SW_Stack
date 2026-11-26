"""
Asperion Enterprise OS - Comprehensive ISO Standards, QMS, Grievance Redressal & Worksheets Models
Enforces:
1. ISO 9001:2015 - Quality Management Systems (QMS) & CAPA Worksheets
2. ISO/IEC 27001:2022 - Information Security Management Systems (ISMS) & Annex A Controls
3. ISO/IEC 42001:2023 - Artificial Intelligence Management Systems (AIMS) & AI Safety Worksheets
4. ISO/IEC 20000-1:2018 - Information Technology Service Management (ITSM) & Service Catalogs
5. ISO 22301:2019 - Security and Resilience - Business Continuity Management Systems (BCMS) & BIA
6. Formal Grievance Redressal & Customer Satisfaction (CSAT/NPS) System
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ISOCertificationMaster(Base):
    """
    Official ISO Certification Ledger.
    Tracks certificate numbers, accredited registrar (NABCB / IAF / UKAS / BSI / TUV),
    audit cycle (Surveillance 1/2, Recertification), scope of certification, and lead auditor.
    """
    __tablename__ = "iso_certifications"

    id = Column(Integer, primary_key=True, index=True)
    standard_code = Column(String(50), unique=True, index=True) # e.g. ISO-9001:2015, ISO-27001:2022, ISO-42001:2023, ISO-20000-1:2018, ISO-22301:2019
    standard_name = Column(String(100), nullable=False)
    scope_description = Column(Text, nullable=False)
    certificate_number = Column(String(100), unique=True, nullable=False) # e.g. ADT-QMS-2026-9001
    accreditation_body = Column(String(100), default="IAF / NABCB Accredited Registrar (BSI India)")
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    surveillance_audit_due = Column(Date, nullable=False)
    management_representative = Column(String(100), default="Management Representative (Director Varadi Vijay)")
    lead_auditor = Column(String(100), default="External Lead Auditor (BSI Group)")
    status = Column(String(30), default="Active & Certified") # Active & Certified, Surveillance Due, Under Renewal
    non_conformance_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    clauses = relationship("ISOClauseControl", back_populates="iso_standard", cascade="all, delete-orphan")
    audits = relationship("ISOAuditInspection", back_populates="iso_standard", cascade="all, delete-orphan")

class ISOClauseControl(Base):
    """
    Detailed ISO Clauses, Controls and Implementation Worksheets.
    Tracks compliance statement, maturity score (1-5), evidence document references, and control owner.
    """
    __tablename__ = "iso_clause_controls"

    id = Column(Integer, primary_key=True, index=True)
    control_code = Column(String(50), unique=True, index=True) # e.g. ISO9001-CL-8.2, ISO27001-A.8.25, ISO42001-CL-6.1
    standard_code = Column(String(50), ForeignKey("iso_certifications.standard_code"), nullable=False)
    clause_number = Column(String(30), nullable=False) # e.g. 4.1, 8.2, 9.2, A.5.1
    title = Column(String(200), nullable=False)
    control_domain = Column(String(100), nullable=False) # Context, Leadership, Operations, AI Risk, Incident Mgmt, BIA
    requirement_summary = Column(Text, nullable=False)
    implementation_mechanism = Column(Text, nullable=False)
    evidence_vault_ref = Column(String(200), nullable=True) # DOC-QMS-SOP-01, ADR-001, etc.
    maturity_level = Column(String(30), default="Level 4 - Managed & Measured") # Level 1 to 5
    compliance_score_pct = Column(Float, default=100.0)
    control_owner = Column(String(100), nullable=False)
    is_compliant = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    iso_standard = relationship("ISOCertificationMaster", back_populates="clauses")

class ISOAuditInspection(Base):
    """
    Internal and External ISO Audit Inspection Schedule & Worksheets.
    Evaluates conformity, minor non-conformities (MNC), major non-conformities (NC), and opportunities for improvement (OFI).
    """
    __tablename__ = "iso_audit_inspections"

    id = Column(Integer, primary_key=True, index=True)
    audit_code = Column(String(50), unique=True, index=True) # e.g. AUD-ISO-2026-Q1
    standard_code = Column(String(50), ForeignKey("iso_certifications.standard_code"), nullable=False)
    audit_type = Column(String(50), default="Internal Management Audit") # Internal Management Audit, External Registrar Surveillance, Pre-Assessment
    audit_date = Column(Date, nullable=False)
    audited_department = Column(String(100), default="Engineering, PMO, SecOps & Delivery")
    lead_auditor = Column(String(100), nullable=False)
    auditee_representative = Column(String(100), nullable=False)
    findings_summary = Column(Text, nullable=False)
    major_nc_count = Column(Integer, default=0)
    minor_nc_count = Column(Integer, default=0)
    ofi_count = Column(Integer, default=1) # Opportunities for improvement
    audit_outcome = Column(String(50), default="Conforming - Recommendation for Continuation")
    status = Column(String(30), default="Completed & Closed")
    created_at = Column(DateTime, default=datetime.utcnow)

    iso_standard = relationship("ISOCertificationMaster", back_populates="audits")

class ISOCorrectiveActionWorksheet(Base):
    """
    ISO Corrective and Preventive Action (CAPA) Detailed Worksheet.
    Root Cause Analysis (5 Whys / Ishikawa Fishbone), immediate containment, systemic corrective action, and verification.
    """
    __tablename__ = "iso_capa_worksheets"

    id = Column(Integer, primary_key=True, index=True)
    capa_number = Column(String(50), unique=True, index=True) # e.g. CAPA-ISO-2026-001
    source_type = Column(String(50), default="Audit Non-Conformance") # Audit Non-Conformance, Customer Grievance, AI Incident, Service Desk Breach
    standard_code = Column(String(50), nullable=False) # ISO 9001, ISO 27001, ISO 42001, etc.
    problem_statement = Column(Text, nullable=False)
    immediate_containment_action = Column(Text, nullable=False)
    root_cause_analysis_method = Column(String(50), default="5 Whys Root Cause Analysis")
    root_cause_findings = Column(Text, nullable=False)
    preventive_corrective_action = Column(Text, nullable=False)
    action_owner = Column(String(100), nullable=False)
    target_closure_date = Column(Date, nullable=False)
    actual_closure_date = Column(Date, nullable=True)
    effectiveness_verified = Column(Boolean, default=True)
    verifier_name = Column(String(100), default="Director Varadi Vijay (Quality Lead)")
    status = Column(String(30), default="Closed & Verified") # Open, Under Investigation, Action Implemented, Closed & Verified
    created_at = Column(DateTime, default=datetime.utcnow)

class FormalGrievanceRecord(Base):
    """
    Formal Multi-Stakeholder Grievance Redressal Register.
    Captures grievances from Clients, Employees, Vendors, and Partners with statutory escalation timelines.
    """
    __tablename__ = "formal_grievances"

    id = Column(Integer, primary_key=True, index=True)
    grievance_id = Column(String(50), unique=True, index=True) # e.g. GRV-2026-001
    stakeholder_type = Column(String(50), default="Client") # Client, Employee, Vendor, Partner
    stakeholder_name = Column(String(150), nullable=False)
    stakeholder_email = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False) # Quality of Deliverable, SLA Delay, Billing Discrepancy, Workplace Conduct, Data Privacy
    severity = Column(String(30), default="High") # Critical, High, Medium, Low
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    assigned_redressal_officer = Column(String(100), default="Sole Director (Varadi Vijay)")
    statutory_sla_days = Column(Integer, default=7) # Resolvable within 7 business days
    acknowledgment_sent = Column(Boolean, default=True)
    investigation_notes = Column(Text, nullable=True)
    resolution_details = Column(Text, nullable=True)
    closure_date = Column(Date, nullable=True)
    complainant_satisfied = Column(Boolean, default=True)
    csat_score = Column(Integer, default=5) # 1 to 5 scale
    status = Column(String(30), default="Resolved & Closed") # Open, Under Investigation, Resolution Proposed, Resolved & Closed
    created_at = Column(DateTime, default=datetime.utcnow)
