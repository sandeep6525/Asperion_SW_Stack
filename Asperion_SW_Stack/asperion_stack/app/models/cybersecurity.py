"""
Asperion Enterprise OS - Cybersecurity, Incident Management & SOC Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SecurityIncident(Base):
    __tablename__ = "security_incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(50), unique=True, index=True) # ADT-SEC-2026-001
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Unauthorized Access Attempt") # Ransomware, Data Breach, Phishing, Unauthorized Cloud Access, Credential Compromise, DDoS
    severity = Column(String(20), default="P2-High") # P1-Critical, P2-High, P3-Medium, P4-Low
    status = Column(String(50), default="Triage") # New, Triage, Contained, Eradicated, Recovered, Closed
    incident_commander = Column(String(100), default="SecOps Lead")
    affected_systems = Column(String(255), default="Cloud Infrastructure")
    data_classification_impacted = Column(String(50), default="Confidential") # Public, Internal, Confidential, Restricted/PII
    reported_at = Column(DateTime, default=datetime.utcnow)
    containment_at = Column(DateTime, nullable=True)
    resolution_at = Column(DateTime, nullable=True)
    
    # Statutory Notifications (India CERT-In & DPDP Act 2023)
    cert_in_reporting_required = Column(Boolean, default=False)
    cert_in_deadline = Column(DateTime, nullable=True) # 6 hours from confirmation
    cert_in_status = Column(String(50), default="Not Required") # Not Required, Drafted, Submitted, Acknowledged
    cert_in_incident_ref = Column(String(100), nullable=True)
    dpdp_breach_notice_required = Column(Boolean, default=False)
    dpdp_data_protection_board_notified = Column(Boolean, default=False)
    affected_users_count = Column(Integer, default=0)
    
    war_room_url = Column(String(255), nullable=True)
    mitre_tactics = Column(String(255), default="Initial Access, Defense Evasion")
    ntp_synchronized = Column(Boolean, default=True) # CERT-In mandatory time sync validation (NPL / NIC NTP)
    containment_summary = Column(Text, nullable=True)
    root_cause_analysis = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    evidence_items = relationship("EvidenceItem", back_populates="incident")

class SecurityAlert(Base):
    __tablename__ = "security_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, index=True) # ADT-ALT-001
    source = Column(String(100), default="AWS GuardDuty") # GuardDuty, CloudTrail, SentinelOne, GitHub Secret Scanning
    rule_name = Column(String(255), nullable=False)
    signal_summary = Column(Text, nullable=False)
    initial_severity = Column(String(20), default="Medium")
    validation_status = Column(String(50), default="Under Investigation") # Under Investigation, True Positive (Escalated to Incident), False Positive, Ignored
    assigned_analyst = Column(String(100), default="SOC Analyst")
    detected_at = Column(DateTime, default=datetime.utcnow)

class EvidenceItem(Base):
    __tablename__ = "incident_evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String(50), unique=True, index=True) # ADT-EVD-001
    incident_id = Column(Integer, ForeignKey("security_incidents.id"))
    item_name = Column(String(255), nullable=False)
    source_type = Column(String(100), default="VPC Flow Logs") # Memory Dump, Disk Image, VPC Flow Logs, SIEM Logs, Email Headers
    sha256_checksum = Column(String(64), nullable=False)
    storage_uri = Column(String(255), default="s3://asperion-sec-evidence-vault/2026/")
    collected_by = Column(String(100), default="Forensic Investigator")
    custody_notes = Column(Text, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("SecurityIncident", back_populates="evidence_items")

class Playbook(Base):
    __tablename__ = "security_playbooks"
    
    id = Column(Integer, primary_key=True, index=True)
    playbook_code = Column(String(50), unique=True, index=True) # PB-SEC-01
    title = Column(String(255), nullable=False)
    threat_category = Column(String(100), nullable=False)
    triggers = Column(Text, nullable=False)
    immediate_containment = Column(Text, nullable=False)
    investigation_steps = Column(Text, nullable=False)
    eradication_and_recovery = Column(Text, nullable=False)
    regulatory_mandate = Column(String(255), default="CERT-In Cybersecurity Directions 2022")
    owner = Column(String(100), default="CISO / IT Security Lead")
    last_reviewed_date = Column(Date, nullable=False)

class VulnerabilityPatch(Base):
    __tablename__ = "vulnerabilities_patches"
    
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(50), index=True) # CVE-2026-1234
    affected_asset = Column(String(255), nullable=False)
    component = Column(String(100)) # OpenSSL, Linux Kernel, Node.js, Python Package
    cvss_score = Column(Float, default=7.5)
    severity = Column(String(20), default="High") # Low, Medium, High, Critical
    patch_available = Column(Boolean, default=True)
    remediation_due_date = Column(Date, nullable=False)
    status = Column(String(50), default="Open") # Open, Patch Testing, Applied & Verified, Risk Accepted
    assigned_engineer = Column(String(100), default="DevOps Engineer")
    created_at = Column(DateTime, default=datetime.utcnow)

class TabletopDrill(Base):
    __tablename__ = "security_drills"
    
    id = Column(Integer, primary_key=True, index=True)
    drill_code = Column(String(50), unique=True, index=True) # ADT-DRILL-2026-001
    title = Column(String(255), nullable=False)
    drill_date = Column(Date, nullable=False)
    scenario_type = Column(String(100), default="Ransomware Extortion Simulation")
    facilitator = Column(String(100), default="External Security Auditor / CISO")
    participants_roles = Column(String(255), default="Founder, SecOps Lead, DevOps Lead, Legal Counsel")
    target_containment_minutes = Column(Integer, default=30)
    actual_containment_minutes = Column(Integer, default=24)
    lessons_learned_summary = Column(Text, nullable=False)
    drill_rating = Column(String(50), default="Satisfactory - High Preparedness")

class CERTInRegulatoryReport(Base):
    __tablename__ = "cert_in_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_reference = Column(String(50), unique=True, index=True) # CERT-IN-REP-2026-001
    incident_id = Column(String(50), nullable=False)
    submission_timestamp = Column(DateTime, default=datetime.utcnow)
    cert_in_ack_number = Column(String(100), nullable=True) # e.g. "CERTIN/INC/2026/0981"
    affected_organization = Column(String(255), default="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED")
    contact_phone = Column(String(50), default="+91-80-XXXXXXXX")
    contact_email = Column(String(100), default="security@asperion.in")
    narrative_description = Column(Text, nullable=False)
    containment_actions_taken = Column(Text, nullable=False)
    filing_status = Column(String(50), default="Submitted") # Draft, Submitted, Acknowledged, Closed

class ThreatIntelIndicator(Base):
    """
    Threat Intelligence IOC (Indicators of Compromise) Repository.
    Synchronizes malicious IPs, domains, hashes, and URLs with Cloudflare WAF,
    AWS Network Firewall, and endpoint EDR engines.
    """
    __tablename__ = "threat_intel_indicators"

    id = Column(Integer, primary_key=True, index=True)
    ioc_id = Column(String(50), unique=True, index=True) # ADT-IOC-001
    ioc_type = Column(String(50), default="IP_Address") # IP_Address, Domain, SHA256_Hash, URL, YARA_Signature
    ioc_value = Column(String(255), nullable=False, index=True)
    threat_actor_group = Column(String(100), default="APT / Ransomware Syndicate")
    confidence_score = Column(Integer, default=90) # 0 to 100
    mitre_technique = Column(String(100), default="T1078 Valid Accounts")
    action_taken = Column(String(100), default="Blocked at Cloudflare WAF & AWS Firewall")
    source_feed = Column(String(100), default="CERT-In Threat Advisory & Feeds")
    status = Column(String(50), default="Active_Blocked") # Active_Blocked, Monitoring, Deprecated
    created_at = Column(DateTime, default=datetime.utcnow)


