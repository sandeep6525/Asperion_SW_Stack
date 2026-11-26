"""
Asperion Enterprise OS - Comprehensive Cybersecurity & SOC Schemas
Pillars: Incident Management, Forensics, Playbooks, SIEM Alerts, Vulnerabilities, Threat Intel, CERT-In Reporting
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class IncidentCreate(BaseModel):
    title: str
    category: str = "Unauthorized Access Attempt"
    affected_systems: str = "AWS VPC / Cloud Infrastructure"
    data_classification: str = "Confidential"
    is_customer_facing: bool = False
    estimated_impacted_users: int = 0
    incident_commander: str = "SecOps Lead (Priya Nair)"
    war_room_url: Optional[str] = None
    mitre_tactics: Optional[str] = "Initial Access, Defense Evasion"
    containment_summary: Optional[str] = None

class IncidentOut(BaseModel):
    id: int
    incident_id: str
    title: str
    category: str
    severity: str
    status: str
    incident_commander: str
    affected_systems: str
    data_classification_impacted: Optional[str] = "Confidential"
    reported_at: datetime
    containment_at: Optional[datetime] = None
    resolution_at: Optional[datetime] = None
    cert_in_reporting_required: bool
    cert_in_deadline: Optional[datetime]
    cert_in_status: str
    cert_in_incident_ref: Optional[str] = None
    dpdp_breach_notice_required: bool
    dpdp_data_protection_board_notified: Optional[bool] = False
    affected_users_count: Optional[int] = 0
    war_room_url: Optional[str] = None
    mitre_tactics: Optional[str] = "Initial Access"
    ntp_synchronized: Optional[bool] = True
    containment_summary: Optional[str] = None
    root_cause_analysis: Optional[str] = None
    lessons_learned: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class IncidentStatusUpdate(BaseModel):
    status: str # Triage, Contained, Eradicated, Recovered, Closed
    containment_summary: Optional[str] = None
    root_cause_analysis: Optional[str] = None
    lessons_learned: Optional[str] = None

class IncidentTriageResponse(BaseModel):
    severity: str
    response_target_minutes: int
    war_room_required: bool
    escalation_path: str
    cert_in_statutory_reporting: Dict[str, Any]
    dpdp_regulatory_notice: Dict[str, Any]
    recommended_playbook: Dict[str, Any]

class SecurityAlertCreate(BaseModel):
    alert_id: str
    source: str = "AWS GuardDuty"
    rule_name: str
    signal_summary: str
    initial_severity: str = "Medium"
    validation_status: str = "Under Investigation"
    assigned_analyst: str = "SOC Analyst (Priya Nair)"

class SecurityAlertOut(SecurityAlertCreate):
    id: int
    detected_at: datetime
    class Config:
        from_attributes = True

class EvidenceItemCreate(BaseModel):
    evidence_id: str
    incident_id: Optional[int] = None
    item_name: str
    source_type: str = "VPC Flow Logs"
    sha256_checksum: str
    storage_uri: str = "s3://asperion-sec-evidence-vault/2026/"
    collected_by: str = "Lead Forensic Investigator"
    custody_notes: Optional[str] = None

class EvidenceItemOut(EvidenceItemCreate):
    id: int
    collected_at: datetime
    class Config:
        from_attributes = True

class PlaybookCreate(BaseModel):
    playbook_code: str
    title: str
    threat_category: str
    triggers: str
    immediate_containment: str
    investigation_steps: str
    eradication_and_recovery: str
    regulatory_mandate: str = "CERT-In Cybersecurity Directions 2022"
    owner: str = "CISO / IT Security Lead"
    last_reviewed_date: date

class PlaybookOut(PlaybookCreate):
    id: int
    class Config:
        from_attributes = True

class VulnerabilityPatchCreate(BaseModel):
    cve_id: str
    affected_asset: str
    component: str = "Node.js / OpenSSL"
    cvss_score: float = 7.5
    severity: str = "High"
    patch_available: bool = True
    remediation_due_date: date
    status: str = "Open"
    assigned_engineer: str = "DevOps Engineer"

class VulnerabilityPatchOut(VulnerabilityPatchCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class TabletopDrillCreate(BaseModel):
    drill_code: str
    title: str
    drill_date: date
    scenario_type: str = "Ransomware Extortion Simulation"
    facilitator: str = "External Security Auditor / CISO"
    participants_roles: str = "Founder, SecOps Lead, DevOps Lead, Legal Counsel"
    target_containment_minutes: int = 30
    actual_containment_minutes: int = 24
    lessons_learned_summary: str
    drill_rating: str = "Satisfactory - High Preparedness"

class TabletopDrillOut(TabletopDrillCreate):
    id: int
    class Config:
        from_attributes = True

class ThreatIntelIndicatorCreate(BaseModel):
    ioc_id: str
    ioc_type: str = "IP_Address"
    ioc_value: str
    threat_actor_group: str = "APT / Ransomware Syndicate"
    confidence_score: int = 90
    mitre_technique: str = "T1078 Valid Accounts"
    action_taken: str = "Blocked at Cloudflare WAF & AWS Firewall"
    source_feed: str = "CERT-In Threat Advisory & Feeds"
    status: str = "Active_Blocked"

class ThreatIntelIndicatorOut(ThreatIntelIndicatorCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CERTInRegulatoryReportCreate(BaseModel):
    report_reference: str
    incident_id: str
    affected_organization: str = "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    contact_phone: str = "+91-80-6922-8000"
    contact_email: str = "security@asperiondigital.com"
    narrative_description: str
    containment_actions_taken: str
    cert_in_ack_number: Optional[str] = None
    filing_status: str = "Submitted"

class CERTInRegulatoryReportOut(CERTInRegulatoryReportCreate):
    id: int
    submission_timestamp: datetime
    class Config:
        from_attributes = True

