"""
Asperion Enterprise OS - Comprehensive Test Suite for Cybersecurity, Incident Management & CERT-In War Room
Validates:
1. SecOps War Room Executive Posture & NTP Lock Telemetry
2. Incident Triage, Classification, Mitigation & Escalation
3. SIEM Threat Ingestion & Direct Auto-Escalation to P1/P2 Incident
4. Forensic Evidence Locker & SHA-256 Tamper-Evident Hashing
5. NIST SP 800-61 Incident Response Playbooks
6. Vulnerability Management & CVSS Patch Registry
7. Tabletop Cyber Crisis Drills & Containment SLAs
8. Threat Intelligence Indicators of Compromise (IOCs) Active Dropping
9. Statutory CERT-In 2022 Formal Filings & Dual-Format Reporting (HTML & DOCX)
"""
import uuid
from datetime import datetime, date, timedelta
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.cybersecurity import (
    get_secops_warroom_overview,
    list_incidents, report_security_incident, update_incident_status, escalate_to_war_room,
    list_siem_alerts, ingest_siem_alert, escalate_alert_to_incident,
    list_evidence_items, log_forensic_evidence,
    list_playbooks, register_playbook,
    list_vulnerabilities, record_vulnerability,
    list_drills, record_drill,
    list_threat_intel, register_threat_intel,
    list_cert_in_reports, submit_cert_in_report,
    get_cert_in_filing_report, download_incident_report_docx
)
from app.schemas.cybersecurity import (
    IncidentCreate, IncidentStatusUpdate,
    SecurityAlertCreate, EvidenceItemCreate,
    PlaybookCreate, VulnerabilityPatchCreate,
    TabletopDrillCreate, ThreatIntelIndicatorCreate,
    CERTInRegulatoryReportCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_secops_warroom_overview(db_session):
    ov = get_secops_warroom_overview(db=db_session)
    assert ov is not None
    assert ov["status"] == "OPERATIONAL_WAR_ROOM"
    assert ov["entity"] == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert ov["cin"] == "U85500KA2026OPC222069"
    assert "Horamavu, Bangalore" in ov["registered_office"]
    
    # NTP sync verification (CERT-In mandate)
    assert "SYNCHRONIZED" in ov["ntp_synchronization"]["status"]
    assert "time.nplindia.org" in ov["ntp_synchronization"]["primary_source"]
    
    # Telemetry
    assert ov["defense_telemetry"]["active_threat_iocs_blocked"] >= 4
    assert ov["defense_telemetry"]["forensic_evidence_items_preserved"] >= 3
    assert ov["defense_telemetry"]["incident_response_playbooks_active"] >= 6
    assert ov["defense_telemetry"]["tabletop_crisis_drills_completed"] >= 2

def test_security_incident_lifecycle(db_session):
    # 1. Report a new P1 Incident
    inc_in = IncidentCreate(
        title="Simulated Ransomware Canary Trip on S3 Glacier Storage",
        category="Ransomware Outbreak",
        affected_systems="S3 Storage & Worker VPC (ap-south-1)",
        data_classification="Restricted/PII",
        is_customer_facing=True,
        estimated_impacted_users=150,
        incident_commander="Priya Nair (SecOps Lead)",
        mitre_tactics="Defense Evasion, Impact",
        containment_summary="Automated canary triggered, IAM session tokens invalidated."
    )
    inc = report_security_incident(inc_in=inc_in, db=db_session)
    assert inc.id is not None
    assert inc.severity == "P1-Critical"
    assert inc.cert_in_reporting_required is True
    assert inc.cert_in_deadline is not None
    assert inc.war_room_url is not None
    assert "meet.google.com" in inc.war_room_url
    
    # 2. Update status to Contained
    upd = update_incident_status(
        incident_id=inc.incident_id,
        upd=IncidentStatusUpdate(
            status="Contained",
            containment_summary="EKS cluster isolated from VPC gateway, AWS S3 bucket policy set to Read-Only.",
            root_cause_analysis="Test ransomware simulator binary executed inside isolated sandbox."
        ),
        db=db_session
    )
    assert upd.status == "Contained"
    assert upd.containment_at is not None
    assert "EKS cluster isolated" in upd.containment_summary
    
    # 3. Test War Room Escalation endpoint
    esc = escalate_to_war_room(incident_id=inc.incident_id, db=db_session)
    assert esc.severity == "P1-Critical"
    assert esc.cert_in_status == "Drafted"

def test_siem_alerts_and_direct_escalation(db_session):
    # 1. Ingest alert
    alert_code = f"ADT-ALT-{uuid.uuid4().hex[:6].upper()}"
    alert_in = SecurityAlertCreate(
        alert_id=alert_code,
        source="AWS GuardDuty",
        rule_name="CryptoCurrency:EC2/BitcoinMining.B!DNS",
        signal_summary="EC2 instance performing DNS queries associated with crypto mining pools.",
        initial_severity="High",
        validation_status="Under Investigation",
        assigned_analyst="Priya Nair (SecOps Lead)"
    )
    alert = ingest_siem_alert(alert_in=alert_in, db=db_session)
    assert alert.id is not None
    assert alert.alert_id == alert_code
    
    # 2. Escalate directly to P1/P2 Incident
    escalated_inc = escalate_alert_to_incident(alert_id=alert.alert_id, db=db_session)
    assert escalated_inc.id is not None
    assert escalated_inc.severity == "P2-High"
    assert "CryptoCurrency" in escalated_inc.title
    assert escalated_inc.cert_in_reporting_required is True

def test_forensic_evidence_locker_custody(db_session):
    ev_id = f"ADT-EVD-{uuid.uuid4().hex[:6].upper()}"
    ev_in = EvidenceItemCreate(
        evidence_id=ev_id,
        item_name="Compromised Container Ext4 Disk Snapshot",
        source_type="Disk Image",
        sha256_checksum="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        storage_uri="s3://asperion-sec-evidence-vault/2026/disk-snap-001.raw",
        collected_by="Forensic DFIR Specialist",
        custody_notes="Acquired via dd over SSH tunnel; SHA-256 verified identical."
    )
    ev = log_forensic_evidence(ev_in=ev_in, db=db_session)
    assert ev.id is not None
    assert ev.evidence_id == ev_id
    assert ev.sha256_checksum == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

def test_threat_intel_iocs_active_dropping(db_session):
    ioc_id = f"ADT-IOC-{uuid.uuid4().hex[:6].upper()}"
    ioc_in = ThreatIntelIndicatorCreate(
        ioc_id=ioc_id,
        ioc_type="IP_Address",
        ioc_value="198.51.100.77",
        threat_actor_group="Lazarus Recon Campaign",
        confidence_score=98,
        mitre_technique="T1595 Active Scanning",
        action_taken="Blocked at Cloudflare WAF & AWS Network Firewall",
        source_feed="CERT-In Advisory C-2026",
        status="Active_Blocked"
    )
    ioc = register_threat_intel(ioc_in=ioc_in, db=db_session)
    assert ioc.id is not None
    assert ioc.status == "Active_Blocked"
    assert ioc.confidence_score == 98

def test_playbooks_and_vulnerabilities(db_session):
    # Playbooks check
    pbs = list_playbooks(db=db_session)
    assert len(pbs) >= 6
    codes = [p.playbook_code for p in pbs]
    assert "PB-SEC-01" in codes
    assert "PB-SEC-02" in codes
    assert "PB-SEC-05" in codes
    
    # Vulnerability check & registration
    cve_id = f"CVE-2026-{uuid.uuid4().hex[:4].upper()}"
    vuln_in = VulnerabilityPatchCreate(
        cve_id=cve_id,
        affected_asset="Core Redis Cache Cluster",
        component="Redis 7.2.4",
        cvss_score=8.8,
        severity="High",
        patch_available=True,
        remediation_due_date=date(2026, 7, 20),
        status="Patch Testing",
        assigned_engineer="Arjun Sharma"
    )
    v = record_vulnerability(v_in=vuln_in, db=db_session)
    assert v.id is not None
    assert v.cvss_score == 8.8

def test_tabletop_drills_and_certin_reports(db_session):
    # Drills check
    drills = list_drills(db=db_session)
    assert len(drills) >= 2
    for d in drills:
        assert d.actual_containment_minutes <= d.target_containment_minutes
        assert "Preparedness" in d.drill_rating or "Exemplary" in d.drill_rating
        
    # Lodge CERT-In Report
    rep_ref = f"CERT-IN-REP-2026-{uuid.uuid4().hex[:4].upper()}"
    rep_in = CERTInRegulatoryReportCreate(
        report_reference=rep_ref,
        incident_id="ADT-SEC-2026-001",
        affected_organization="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        contact_phone="+91-80-6922-8000",
        contact_email="security@asperiondigital.com",
        narrative_description="Automated report filing for incident ADT-SEC-2026-001. Credentials rotated successfully.",
        containment_actions_taken="AWS IAM keys revoked, security groups tightened.",
        cert_in_ack_number=f"CERTIN/ACK/{uuid.uuid4().hex[:6].upper()}",
        filing_status="Acknowledged"
    )
    rep = submit_cert_in_report(rep_in=rep_in, db=db_session)
    assert rep.id is not None
    assert rep.report_reference == rep_ref
    
    # Verify statutory report dual-format generation
    html_resp = get_cert_in_filing_report(incident_id="ADT-SEC-2026-001", db=db_session)
    assert "INDIAN COMPUTER EMERGENCY RESPONSE TEAM" in html_resp or "CERT-In" in html_resp
    
    docx_stream = download_incident_report_docx(incident_id="ADT-SEC-2026-001", db=db_session)
    assert docx_stream is not None
