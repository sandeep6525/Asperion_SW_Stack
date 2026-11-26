"""
Asperion Enterprise OS - Enterprise Guardrails & Architectural Integrity Models
Enforces active runtime compliance and verification across FinOps, SecOps, HRMS, PMO, SDLC and Procurement.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GuardrailRule(Base):
    """Core Enterprise Guardrail Policy Specification"""
    __tablename__ = "guardrail_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_code = Column(String(50), unique=True, index=True) # e.g. GRD-FIN-001
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False) # FinOps, SecOps, HRMS_Mobility, DevSecOps, Governance_DOA, Procurement_MSME
    regulatory_framework = Column(String(100), default="Internal Financial Controls (IFC)") # IFC, MSMED Act 2006, DPDP Act 2023, ISO 27001, CERT-In, IEEE 1044
    severity = Column(String(30), default="Critical_Blocker") # Critical_Blocker, High_Warning, Compliance_Audit
    enforcement_mode = Column(String(30), default="Active_Blocking") # Active_Blocking, Auto_Heal, Alert_Escalate
    description = Column(Text, nullable=False)
    enforcement_logic = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    total_evaluations = Column(Integer, default=0)
    total_passed = Column(Integer, default=0)
    total_blocked = Column(Integer, default=0)
    total_auto_healed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("GuardrailExecutionLog", back_populates="rule")

class GuardrailExecutionLog(Base):
    """Immutable Audit Trail of Guardrail Evaluations & Interventions"""
    __tablename__ = "guardrail_execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(String(50), unique=True, index=True) # e.g. GEX-2026-001
    rule_code = Column(String(50), ForeignKey("guardrail_rules.rule_code"))
    module = Column(String(50), nullable=False) # Finance, Attendance, Sourcing, PMO, SDLC, SecOps
    entity_reference = Column(String(100), nullable=False) # e.g. APB-2026-001, ATT-BLR-092, PR-2026-004
    evaluation_result = Column(String(30), nullable=False) # PASSED, BLOCKED, AUTO_HEALED
    trigger_payload_summary = Column(Text, nullable=True)
    action_taken = Column(String(255), nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    rule = relationship("GuardrailRule", back_populates="logs")

class ArchitectureBlueprint(Base):
    """Enterprise System Architecture & Flowchart Catalog"""
    __tablename__ = "architecture_blueprints"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_code = Column(String(50), unique=True, index=True) # e.g. ARCH-E2E-001
    title = Column(String(255), nullable=False)
    architecture_type = Column(String(50), default="System_Architecture") # System_Architecture, Data_Flowchart, Sequence_Diagram, Security_Boundary
    module_pillar = Column(String(100), default="Core Enterprise Platform")
    standard_alignment = Column(String(100), default="ISO 27001 / TOGAF / CMMI")
    diagram_mermaid = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    key_components = Column(Text, nullable=False)
    guardrail_linkage = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
