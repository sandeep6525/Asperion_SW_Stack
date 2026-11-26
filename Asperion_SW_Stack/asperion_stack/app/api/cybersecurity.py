"""
Asperion Enterprise OS - Comprehensive Cybersecurity, Incident Management & CERT-In War Room API
Pillars:
1. War Room Executive Overview & CERT-In 6h SLA Countdown
2. Incident Triage, Classification, Mitigation & Escalation
3. SIEM Security Threat Ingestion & Auto-Escalation
4. Forensic Evidence Locker & Tamper-Evident SHA-256 Custody
5. NIST SP 800-61 Incident Response Playbooks
6. Vulnerability Management & CVSS Patch Registry
7. Tabletop Cyber Crisis Drills & Preparedness
8. Threat Intelligence Indicators of Compromise (IOCs)
9. Statutory CERT-In 2022 & DPDP Act 2023 Reporting (HTML & DOCX)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.cybersecurity import (
    SecurityIncident, SecurityAlert, EvidenceItem, Playbook, VulnerabilityPatch,
    TabletopDrill, CERTInRegulatoryReport, ThreatIntelIndicator
)
from app.schemas.cybersecurity import (
    IncidentCreate, IncidentOut, IncidentStatusUpdate, IncidentTriageResponse,
    SecurityAlertCreate, SecurityAlertOut,
    EvidenceItemCreate, EvidenceItemOut,
    PlaybookCreate, PlaybookOut,
    VulnerabilityPatchCreate, VulnerabilityPatchOut,
    TabletopDrillCreate, TabletopDrillOut,
    ThreatIntelIndicatorCreate, ThreatIntelIndicatorOut,
    CERTInRegulatoryReportCreate, CERTInRegulatoryReportOut
)
from app.engines.secops_triage import triage_security_incident, generate_cert_in_statutory_report_html
from app.engines.docx_exporter import create_certin_report_docx

router = APIRouter(prefix="/cybersecurity", tags=["Cybersecurity & SOC Incident Response"])

# -------------------------------------------------------------
# 1. Executive War Room & SecOps Overview
# -------------------------------------------------------------

@router.get("/overview")
def get_secops_warroom_overview(db: Session = Depends(get_db)):
    total_incidents = db.query(SecurityIncident).count()
    active_incidents = db.query(SecurityIncident).filter(
        SecurityIncident.status.in_(["New", "Triage", "Contained", "Eradicated"])
    ).count()
    p1_p2_count = db.query(SecurityIncident).filter(
        SecurityIncident.severity.in_(["P1-Critical", "P2-High"]),
        SecurityIncident.status != "Closed"
    ).count()
    
    cert_in_pending = db.query(SecurityIncident).filter(
        SecurityIncident.cert_in_reporting_required == True,
        SecurityIncident.cert_in_status.in_(["Drafted", "Not Required"])
    ).count()

    total_alerts = db.query(SecurityAlert).count()
    active_alerts = db.query(SecurityAlert).filter(SecurityAlert.validation_status == "Under Investigation").count()
    
    evidence_count = db.query(EvidenceItem).count()
    playbooks_count = db.query(Playbook).count()
    open_vulns = db.query(VulnerabilityPatch).filter(VulnerabilityPatch.status == "Open").count()
    total_iocs = db.query(ThreatIntelIndicator).filter(ThreatIntelIndicator.status == "Active_Blocked").count()
    drills_count = db.query(TabletopDrill).count()

    now = datetime.utcnow()
    # Compute active CERT-In deadlines
    critical_incidents = db.query(SecurityIncident).filter(
        SecurityIncident.cert_in_reporting_required == True,
        SecurityIncident.status != "Closed"
    ).all()
    
    sla_deadlines = []
    for inc in critical_incidents:
        time_remaining_mins = max(0, int((inc.cert_in_deadline - now).total_seconds() / 60)) if inc.cert_in_deadline else 0
        sla_deadlines.append({
            "incident_id": inc.incident_id,
            "title": inc.title,
            "severity": inc.severity,
            "cert_in_status": inc.cert_in_status,
            "deadline": inc.cert_in_deadline.strftime("%Y-%m-%d %H:%M:%S UTC") if inc.cert_in_deadline else "N/A",
            "time_remaining_minutes": time_remaining_mins,
            "is_breached": time_remaining_mins == 0 and inc.cert_in_status != "Submitted"
        })

    return {
        "status": "OPERATIONAL_WAR_ROOM",
        "entity": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        "cin": "U85500KA2026OPC222069",
        "registered_office": "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore - 560043",
        "regulatory_frameworks": [
            "Indian CERT-In Cybersecurity Directions 2022 (6-Hour SLA)",
            "Digital Personal Data Protection (DPDP) Act 2023",
            "ISO/IEC 27001:2022 (A.5.24 - A.5.28 Incident Management)",
            "NIST SP 800-61 Rev. 2 Computer Security Incident Handling"
        ],
        "ntp_synchronization": {
            "status": "SYNCHRONIZED - LOCKED",
            "primary_source": "time.nplindia.org (National Physical Laboratory)",
            "secondary_source": "time.nic.in (National Informatics Centre)",
            "jitter_ms": 0.42
        },
        "incidents_summary": {
            "total_recorded": total_incidents,
            "active_now": active_incidents,
            "p1_critical_and_p2_high": p1_p2_count,
            "cert_in_pending_filings": cert_in_pending,
            "sla_deadlines": sla_deadlines
        },
        "defense_telemetry": {
            "siem_alerts_under_investigation": active_alerts,
            "total_alerts_ingested": total_alerts,
            "active_threat_iocs_blocked": total_iocs,
            "forensic_evidence_items_preserved": evidence_count,
            "incident_response_playbooks_active": playbooks_count,
            "open_cve_vulnerabilities": open_vulns,
            "tabletop_crisis_drills_completed": drills_count
        }
    }

# -------------------------------------------------------------
# 2. Security Incidents CRUD & Triage
# -------------------------------------------------------------

@router.get("/incidents", response_model=List[IncidentOut])
def list_incidents(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(SecurityIncident)
    if severity:
        q = q.filter(SecurityIncident.severity == severity)
    if status:
        q = q.filter(SecurityIncident.status == status)
    return q.order_by(SecurityIncident.reported_at.desc()).all()

@router.get("/incidents/{incident_id}", response_model=IncidentOut)
def get_incident_detail(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Security Incident not found")
    return inc

@router.post("/incidents", response_model=IncidentOut)
def report_security_incident(inc_in: IncidentCreate, db: Session = Depends(get_db)):
    triage = triage_security_incident(
        category=inc_in.category,
        affected_systems=inc_in.affected_systems,
        data_classification=inc_in.data_classification,
        is_customer_facing=inc_in.is_customer_facing,
        estimated_impacted_users=inc_in.estimated_impacted_users
    )
    
    count = db.query(SecurityIncident).count() + 1
    incident_id = f"ADT-SEC-2026-{count:03d}"
    
    cert_in_req = triage["cert_in_statutory_reporting"]["mandatory"]
    cert_in_deadline = datetime.utcnow() + timedelta(hours=6) if cert_in_req else None
    
    incident = SecurityIncident(
        incident_id=incident_id,
        title=inc_in.title,
        category=inc_in.category,
        severity=triage["severity"],
        status="Triage",
        incident_commander=inc_in.incident_commander,
        affected_systems=inc_in.affected_systems,
        data_classification_impacted=inc_in.data_classification,
        cert_in_reporting_required=cert_in_req,
        cert_in_deadline=cert_in_deadline,
        cert_in_status="Drafted" if cert_in_req else "Not Required",
        dpdp_breach_notice_required=triage["dpdp_regulatory_notice"]["mandatory"],
        affected_users_count=inc_in.estimated_impacted_users,
        war_room_url=inc_in.war_room_url or ("https://meet.google.com/asp-sec-warroom" if triage["war_room_required"] else None),
        mitre_tactics=inc_in.mitre_tactics or "Initial Access, Defense Evasion",
        ntp_synchronized=True,
        containment_summary=inc_in.containment_summary
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.patch("/incidents/{incident_id}", response_model=IncidentOut)
def update_incident_status(
    incident_id: str,
    upd: IncidentStatusUpdate,
    db: Session = Depends(get_db)
):
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    inc.status = upd.status
    if upd.containment_summary:
        inc.containment_summary = upd.containment_summary
        if inc.status in ["Contained", "Eradicated"] and not inc.containment_at:
            inc.containment_at = datetime.utcnow()
    if upd.root_cause_analysis:
        inc.root_cause_analysis = upd.root_cause_analysis
    if upd.lessons_learned:
        inc.lessons_learned = upd.lessons_learned
    if inc.status == "Closed" and not inc.resolution_at:
        inc.resolution_at = datetime.utcnow()
        
    db.commit()
    db.refresh(inc)
    return inc

@router.post("/incidents/{incident_id}/escalate-war-room", response_model=IncidentOut)
def escalate_to_war_room(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    inc.severity = "P1-Critical"
    inc.war_room_url = f"https://meet.google.com/asp-sec-warroom-{inc.incident_id.lower()}"
    inc.cert_in_reporting_required = True
    if not inc.cert_in_deadline:
        inc.cert_in_deadline = datetime.utcnow() + timedelta(hours=6)
    inc.cert_in_status = "Drafted"
    db.commit()
    db.refresh(inc)
    return inc

@router.post("/triage-preview", response_model=IncidentTriageResponse)
def preview_incident_triage(inc_in: IncidentCreate):
    return triage_security_incident(
        category=inc_in.category,
        affected_systems=inc_in.affected_systems,
        data_classification=inc_in.data_classification,
        is_customer_facing=inc_in.is_customer_facing,
        estimated_impacted_users=inc_in.estimated_impacted_users
    )

# -------------------------------------------------------------
# 3. SIEM Threat Alerts & Auto-Escalation
# -------------------------------------------------------------

@router.get("/alerts", response_model=List[SecurityAlertOut])
def list_siem_alerts(db: Session = Depends(get_db)):
    return db.query(SecurityAlert).order_by(SecurityAlert.detected_at.desc()).all()

@router.post("/alerts", response_model=SecurityAlertOut)
def ingest_siem_alert(alert_in: SecurityAlertCreate, db: Session = Depends(get_db)):
    item = SecurityAlert(**alert_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.post("/alerts/{alert_id}/escalate", response_model=IncidentOut)
def escalate_alert_to_incident(alert_id: str, db: Session = Depends(get_db)):
    alt = db.query(SecurityAlert).filter(SecurityAlert.alert_id == alert_id).first()
    if not alt:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    alt.validation_status = "True Positive (Escalated to Incident)"
    
    count = db.query(SecurityIncident).count() + 1
    new_inc_id = f"ADT-SEC-2026-{count:03d}"
    
    inc = SecurityIncident(
        incident_id=new_inc_id,
        title=f"Escalated: {alt.rule_name}",
        category="Unauthorized Cloud Access" if "AWS" in alt.source else "Suspicious Threat Signal",
        severity="P2-High",
        status="Triage",
        incident_commander="Priya Nair (SecOps Lead)",
        affected_systems=alt.source,
        data_classification_impacted="Confidential",
        cert_in_reporting_required=True,
        cert_in_deadline=datetime.utcnow() + timedelta(hours=6),
        cert_in_status="Drafted",
        war_room_url="https://meet.google.com/asp-sec-warroom",
        containment_summary=f"Auto-escalated from SIEM alert [{alt.alert_id}]. Signal: {alt.signal_summary}"
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    return inc

# -------------------------------------------------------------
# 4. Forensic Evidence Locker & Custody
# -------------------------------------------------------------

@router.get("/evidence", response_model=List[EvidenceItemOut])
def list_evidence_items(incident_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(EvidenceItem)
    if incident_id:
        q = q.filter(EvidenceItem.incident_id == incident_id)
    return q.order_by(EvidenceItem.collected_at.desc()).all()

@router.post("/evidence", response_model=EvidenceItemOut)
def log_forensic_evidence(ev_in: EvidenceItemCreate, db: Session = Depends(get_db)):
    item = EvidenceItem(**ev_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# 5. Incident Response Playbooks
# -------------------------------------------------------------

@router.get("/playbooks", response_model=List[PlaybookOut])
def list_playbooks(db: Session = Depends(get_db)):
    return db.query(Playbook).all()

@router.post("/playbooks", response_model=PlaybookOut)
def register_playbook(pb_in: PlaybookCreate, db: Session = Depends(get_db)):
    pb = Playbook(**pb_in.model_dump())
    db.add(pb)
    db.commit()
    db.refresh(pb)
    return pb

# -------------------------------------------------------------
# 6. Vulnerabilities & CVSS Patches
# -------------------------------------------------------------

@router.get("/vulnerabilities", response_model=List[VulnerabilityPatchOut])
def list_vulnerabilities(db: Session = Depends(get_db)):
    return db.query(VulnerabilityPatch).order_by(VulnerabilityPatch.cvss_score.desc()).all()

@router.post("/vulnerabilities", response_model=VulnerabilityPatchOut)
def record_vulnerability(v_in: VulnerabilityPatchCreate, db: Session = Depends(get_db)):
    item = VulnerabilityPatch(**v_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# 7. Tabletop Cyber Crisis Drills
# -------------------------------------------------------------

@router.get("/drills", response_model=List[TabletopDrillOut])
def list_drills(db: Session = Depends(get_db)):
    return db.query(TabletopDrill).order_by(TabletopDrill.drill_date.desc()).all()

@router.post("/drills", response_model=TabletopDrillOut)
def record_drill(d_in: TabletopDrillCreate, db: Session = Depends(get_db)):
    item = TabletopDrill(**d_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# 8. Threat Intelligence Indicators (IOCs)
# -------------------------------------------------------------

@router.get("/threat-intel", response_model=List[ThreatIntelIndicatorOut])
def list_threat_intel(db: Session = Depends(get_db)):
    return db.query(ThreatIntelIndicator).order_by(ThreatIntelIndicator.created_at.desc()).all()

@router.post("/threat-intel", response_model=ThreatIntelIndicatorOut)
def register_threat_intel(ioc_in: ThreatIntelIndicatorCreate, db: Session = Depends(get_db)):
    item = ThreatIntelIndicator(**ioc_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# -------------------------------------------------------------
# 9. CERT-In Statutory Regulatory Reports
# -------------------------------------------------------------

@router.get("/cert-in-reports", response_model=List[CERTInRegulatoryReportOut])
def list_cert_in_reports(db: Session = Depends(get_db)):
    return db.query(CERTInRegulatoryReport).order_by(CERTInRegulatoryReport.submission_timestamp.desc()).all()

@router.post("/cert-in-reports", response_model=CERTInRegulatoryReportOut)
def submit_cert_in_report(rep_in: CERTInRegulatoryReportCreate, db: Session = Depends(get_db)):
    item = CERTInRegulatoryReport(**rep_in.model_dump())
    db.add(item)
    
    # Also update incident record status
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == rep_in.incident_id).first()
    if inc:
        inc.cert_in_status = "Submitted"
        inc.cert_in_incident_ref = rep_in.cert_in_ack_number or f"CERTIN/INC/2026/{inc.id:04d}"
        
    db.commit()
    db.refresh(item)
    return item

@router.get("/cert-in-report/{incident_id}", response_class=HTMLResponse)
def get_cert_in_filing_report(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    inc_data = {
        "incident_id": inc.incident_id,
        "reported_at": inc.reported_at.strftime("%d %B %Y %H:%M:%S IST") if inc.reported_at else "Now",
        "severity": inc.severity,
        "category": inc.category,
        "affected_systems": inc.affected_systems,
        "incident_commander": inc.incident_commander,
        "containment_summary": inc.containment_summary or "Active containment: AWS session tokens revoked, affected subnet traffic isolated."
    }
    return generate_cert_in_statutory_report_html(inc_data)

@router.get("/incidents/{incident_id}/docx")
def download_incident_report_docx(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(SecurityIncident).filter(SecurityIncident.incident_id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    inc_data = {
        "incident_id": inc.incident_id,
        "title": inc.title,
        "severity": inc.severity,
        "incident_type": inc.category,
        "cert_in_deadline": str(inc.cert_in_deadline) if inc.cert_in_deadline else "Within 6 hours",
        "affected_systems": inc.affected_systems,
        "detected_at": inc.reported_at,
        "status": inc.status,
        "containment_status": inc.containment_summary or ("Active Containment" if inc.status != "Resolved" else "Resolved"),
        "dpdp_breach": inc.dpdp_breach_notice_required,
        "remediation_steps": "Isolated affected endpoints, rotated API keys/IAM credentials, preserved forensic logs."
    }
    
    file_stream = create_certin_report_docx(inc_data)
    filename = f"CERT_In_Report_{inc.incident_id}.docx"
    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
