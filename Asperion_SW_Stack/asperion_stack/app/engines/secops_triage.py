"""
Asperion Enterprise OS - Cybersecurity Triage & Statutory Notification Engine
Handles Incident Severity Classification, Playbook Mapping, and CERT-In 6-Hour SLA
"""
from datetime import datetime, timedelta
from typing import Dict, Any

def triage_security_incident(
    category: str,
    affected_systems: str,
    data_classification: str,
    is_customer_facing: bool,
    estimated_impacted_users: int = 0
) -> Dict[str, Any]:
    """
    Evaluates cybersecurity incident severity according to Asperion Security Framework,
    NIST SP 800-61, and Indian CERT-In Directions 2022.
    """
    category_lower = category.lower()
    data_class_lower = data_classification.lower()
    
    # 1. Severity Evaluation (P1 to P4)
    if "ransomware" in category_lower or (is_customer_facing and "confidential" in data_class_lower) or estimated_impacted_users > 100:
        severity = "P1-Critical"
        response_target_mins = 15
        escalation = "Immediate War Room; Founder, CISO, Legal Counsel, External DFIR"
        war_room_required = True
    elif "unauthorized" in category_lower or "breach" in category_lower or "cloud" in category_lower:
        severity = "P2-High"
        response_target_mins = 30
        escalation = "SecOps Lead, DevOps Lead, Engineering Head"
        war_room_required = True
    elif "phishing" in category_lower or "vulnerability" in category_lower:
        severity = "P3-Medium"
        response_target_mins = 120
        escalation = "SOC Analyst & IT Admin"
        war_room_required = False
    else:
        severity = "P4-Low"
        response_target_mins = 480
        escalation = "Helpdesk / Normal Queue"
        war_room_required = False
        
    # 2. Statutory Regulatory Triggers (CERT-In 6-hour mandate)
    # Under Indian CERT-In 2022 Directions, cybersecurity incidents like targeted scanning,
    # compromise of critical systems, ransomware, identity theft, or data breaches MUST be reported within 6 hours.
    now = datetime.utcnow()
    cert_in_mandatory = severity in ["P1-Critical", "P2-High"] or "breach" in category_lower or "ransomware" in category_lower
    cert_in_deadline = (now + timedelta(hours=6)).isoformat() if cert_in_mandatory else None
    
    # 3. Digital Personal Data Protection (DPDP) Act 2023 notification trigger
    dpdp_mandatory = ("confidential" in data_class_lower or "pii" in data_class_lower or "restricted" in data_class_lower) and estimated_impacted_users > 0
    
    # 4. Playbook Recommendation
    if "ransomware" in category_lower:
        playbook = {
            "code": "PB-SEC-01",
            "name": "Ransomware & Host Extortion Containment Playbook",
            "containment_steps": [
                "Isolate affected endpoints/VPCs from corporate network immediately.",
                "Disable compromised service accounts and revoke active AWS IAM sessions.",
                "Preserve volatile memory (RAM dump) and disk images before terminating VMs.",
                "Verify offline/immutable S3 Glacier backup integrity.",
                "Engage CERT-In incident reporting desk (incident@cert-in.org.in)."
            ]
        }
    elif "cloud" in category_lower or "unauthorized" in category_lower:
        playbook = {
            "code": "PB-SEC-02",
            "name": "Cloud IAM & Infrastructure Compromise Playbook",
            "containment_steps": [
                "Revoke compromised AWS access keys / STS session tokens via AWS CLI.",
                "Apply deny-all IAM inline policy to the affected principal.",
                "Rotate all database master credentials and API secrets in Secrets Manager.",
                "Review CloudTrail and GuardDuty findings for unauthorized S3 exfiltration.",
                "Audit security groups and close unexpected open ingress ports (0.0.0.0/0)."
            ]
        }
    elif "phishing" in category_lower:
        playbook = {
            "code": "PB-SEC-03",
            "name": "Email Phishing & Credential Harvesting Playbook",
            "containment_steps": [
                "Force logout Google Workspace session for affected user.",
                "Reset password and re-bind FIDO2 hardware passkey.",
                "Search and purge malicious email across all tenant inboxes using Google Workspace admin API.",
                "Block sender domain and malicious C2 URLs on firewall/DNS filters."
            ]
        }
    else:
        playbook = {
            "code": "PB-SEC-04",
            "name": "Standard Security Incident Investigation Playbook",
            "containment_steps": [
                "Establish baseline incident timeline and scope of impact.",
                "Collect system and application logs with SHA-256 evidence hashing.",
                "Verify patch status of affected components.",
                "Conduct post-incident review (RCA) within 72 hours."
            ]
        }
        
    return {
        "severity": severity,
        "response_target_minutes": response_target_mins,
        "war_room_required": war_room_required,
        "escalation_path": escalation,
        "cert_in_statutory_reporting": {
            "mandatory": cert_in_mandatory,
            "statutory_timeframe": "6 Hours (CERT-In 2022 Directions)",
            "deadline": cert_in_deadline,
            "email_target": "incident@cert-in.org.in",
            "portal": "https://www.cert-in.org.in"
        },
        "dpdp_regulatory_notice": {
            "mandatory": dpdp_mandatory,
            "authority": "Data Protection Board of India (DPBI)",
            "intimation_to_affected_data_principals_required": dpdp_mandatory
        },
        "recommended_playbook": playbook
    }

def generate_cert_in_statutory_report_html(
    incident_data: Dict[str, Any]
) -> str:
    """
    Generates official statutory cybersecurity incident filing for CERT-In
    under Section 70B(6) of the Information Technology Act and 2022 Directions.
    """
    now_str = datetime.now().strftime("%d %B %Y %H:%M:%S IST")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>CERT-In Statutory Incident Reporting Form</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.5; color: #0f172a; max-width: 850px; margin: 30px auto; padding: 25px; border: 2px solid #b91c1c; background: #fff; }}
            .header {{ border-bottom: 2px solid #b91c1c; padding-bottom: 12px; margin-bottom: 20px; }}
            .badge {{ background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; border: 1px solid #f87171; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin: 15px 0; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }}
            th {{ background: #f8fafc; font-weight: 600; width: 30%; }}
        </style>
    </head>
    <body>
        <div class="header">
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 8px;">
                <tr>
                    <td style="width: 62px; vertical-align: middle; border: none; padding: 0 14px 0 0;">
                        <img src="/static/img/logo.png" alt="Asperion Logo" style="width: 56px; height: 56px; border-radius: 50%; object-fit: contain; background: #0f172a; padding: 2px; border: 1.5px solid #ef4444; display: block;">
                    </td>
                    <td style="vertical-align: middle; border: none; padding: 0;">
                        <span class="badge">URGENT: STATUTORY NOTIFICATION UNDER CERT-IN DIRECTIONS 2022</span>
                        <h2 style="margin: 6px 0 2px 0; color: #b91c1c;">CYBERSECURITY INCIDENT REPORTING FORM</h2>
                        <p style="margin: 0; font-size: 11px; color: #64748b;">Submitted to: Indian Computer Emergency Response Team (incident@cert-in.org.in)</p>
                    </td>
                    <td style="text-align: right; vertical-align: middle; border: none; padding: 0;">
                        <span style="font-family: monospace; font-size: 11px; color: #b91c1c; font-weight: bold; background: #fef2f2; padding: 4px 8px; border: 1px solid #fecaca; border-radius: 4px;">6-HOUR SLA</span>
                    </td>
                </tr>
            </table>
        </div>

        <table>
            <tr><th>Reporting Entity</th><td><strong>ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</strong> (CIN: U85500KA2026OPC222069)</td></tr>
            <tr><th>Incident Reference ID</th><td>{incident_data.get('incident_id', 'ADT-SEC-2026-001')}</td></tr>
            <tr><th>Date & Time of Incident</th><td>{incident_data.get('reported_at', now_str)}</td></tr>
            <tr><th>Incident Severity</th><td><strong style="color:#b91c1c;">{incident_data.get('severity', 'P1-Critical')}</strong></td></tr>
            <tr><th>Category of Cyber Incident</th><td>{incident_data.get('category', 'Unauthorized Cloud Compromise')}</td></tr>
            <tr><th>Affected Systems / Cloud Perimeter</th><td>{incident_data.get('affected_systems', 'AWS Production VPC / IAM Infrastructure')}</td></tr>
            <tr><th>Incident Commander / Point of Contact</th><td>{incident_data.get('incident_commander', 'SecOps Lead')} (security@asperion.in)</td></tr>
            <tr><th>Immediate Containment Actions</th><td>{incident_data.get('containment_summary', 'Compromised IAM session tokens revoked, affected instances isolated, memory dumps preserved.')}</td></tr>
            <tr><th>Forensic Evidence Custody</th><td>Cryptographic SHA-256 hashes logged; forensic images stored in encrypted immutable storage.</td></tr>
        </table>

        <div style="margin-top: 25px; border-top: 1px solid #cbd5e1; padding-top: 15px; font-size: 12px; color: #64748b;">
            <p><strong>Declaration:</strong> I hereby certify that the information provided above is true and accurate to the best of my knowledge and is submitted in compliance with CERT-In directions.</p>
            <p><strong>Authorized Security Officer:</strong> Varadi Vijay (Director / Member) | ASPERION DIGITAL TECHNOLOGIES</p>
        </div>
    </body>
    </html>
    """
    return html

