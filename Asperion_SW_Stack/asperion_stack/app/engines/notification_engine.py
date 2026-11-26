"""
Asperion Enterprise OS - Cross-Functional Notification & Alert Engine
Scans operational pillars and dispatches multi-channel alerts and warnings.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

from app.models.ticketing_notifications import SystemNotification, InternalTicket
from app.models.governance import ComplianceCalendarItem
from app.models.finance import Invoice, CashFlowEntry
from app.models.cybersecurity import SecurityIncident
from app.models.infrastructure import CertificateSecret, CloudAccount
from app.models.crm_enterprise import Opportunity

# Department prefix mapping for ticket numbers
DEPT_PREFIXES = {
    "IT_INFRASTRUCTURE": "IT-TKT",
    "HR_PEOPLE": "HR-TKT",
    "FINANCE_ACCOUNTS": "FIN-TKT",
    "LEGAL_COMPLIANCE": "LEG-TKT",
    "ADMIN_WORKPLACE": "ADM-TKT",
    "SECOPS_CYBER": "SEC-TKT",
    "PMO_ENGINEERING": "PMO-TKT"
}

# SLA Hours by Priority
SLA_HOURS_MAP = {
    "P1-Critical": 2.0,   # 2 hours
    "P2-High": 8.0,       # 8 hours
    "P3-Medium": 24.0,    # 24 hours
    "P4-Low": 48.0        # 48 hours
}

def generate_ticket_number(db: Session, department: str) -> str:
    """
    Generates authentic sequential departmental ticket number: e.g. IT-TKT-2026-001
    """
    prefix = DEPT_PREFIXES.get(department, "GEN-TKT")
    year = datetime.utcnow().year
    pattern = f"{prefix}-{year}-%"
    
    count = db.query(InternalTicket).filter(InternalTicket.ticket_number.like(pattern)).count()
    return f"{prefix}-{year}-{count + 1:03d}"

def calculate_sla_target(priority: str) -> (float, datetime):
    """
    Calculates SLA deadline hours and target resolution timestamp.
    """
    hours = SLA_HOURS_MAP.get(priority, 24.0)
    target_time = datetime.utcnow() + timedelta(hours=hours)
    return hours, target_time

def broadcast_alert(
    db: Session,
    module_source: str,
    title: str,
    message: str,
    severity: str = "INFO",
    target_role: str = "ALL",
    action_url: str = None,
    action_label: str = None
) -> SystemNotification:
    """
    Emits an enterprise system alert/notification.
    """
    code_count = db.query(SystemNotification).count() + 1
    code = f"NOTIF-{datetime.utcnow().year}-{code_count:04d}"
    
    notif = SystemNotification(
        notification_code=code,
        module_source=module_source,
        title=title,
        message=message,
        severity=severity.upper(),
        target_role=target_role.upper(),
        action_url=action_url,
        action_label=action_label,
        is_read=False,
        is_dismissed=False,
        created_at=datetime.utcnow()
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def scan_and_sync_system_alerts(db: Session) -> int:
    """
    Scans system state across all modules and creates real-time notifications.
    Returns count of active alerts created.
    """
    now = datetime.utcnow()
    created_count = 0

    # 1. Check Compliance Filings due within 15 days
    fifteen_days = (now + timedelta(days=15)).date()
    upcoming_filings = db.query(ComplianceCalendarItem).filter(
        ComplianceCalendarItem.status == "Active",
        ComplianceCalendarItem.due_date <= fifteen_days
    ).all()
    for f in upcoming_filings:
        exists = db.query(SystemNotification).filter(
            SystemNotification.title.like(f"%{f.filing_code}%")
        ).first()
        if not exists:
            broadcast_alert(
                db,
                module_source="GOVERNANCE",
                title=f"Statutory Filing Due Soon: {f.filing_code} ({f.statutory_authority})",
                message=f"{f.obligation_name} due on {f.due_date}. Mandatory compliance under {f.statutory_authority}.",
                severity="WARNING",
                target_role="DIRECTOR",
                action_url="#view-governance",
                action_label="Review Compliance"
            )
            created_count += 1

    # 2. Check Overdue Invoices > 30 Days
    overdue_invoices = db.query(Invoice).filter(
        Invoice.status != "Paid",
        Invoice.due_date < now.date()
    ).all()
    for inv in overdue_invoices:
        exists = db.query(SystemNotification).filter(
            SystemNotification.title.like(f"%{inv.invoice_number}%")
        ).first()
        if not exists:
            broadcast_alert(
                db,
                module_source="FINANCE",
                title=f"Accounts Receivable Overdue: {inv.invoice_number} ({inv.client_name})",
                message=f"Outstanding balance ₹{inv.outstanding_balance:,.2f} past due since {inv.due_date}.",
                severity="WARNING",
                target_role="FINANCE_HEAD",
                action_url="#view-finance",
                action_label="View AR Ledger"
            )
            created_count += 1

    # 3. Check Active P1 Cybersecurity Incidents
    crit_incidents = db.query(SecurityIncident).filter(
        SecurityIncident.severity.in_(["P1-Critical", "P1"]),
        SecurityIncident.status.in_(["Triaged", "Open", "War Room Active"])
    ).all()
    for inc in crit_incidents:
        exists = db.query(SystemNotification).filter(
            SystemNotification.title.like(f"%{inc.incident_code}%")
        ).first()
        if not exists:
            broadcast_alert(
                db,
                module_source="CYBERSECURITY",
                title=f"CRITICAL Incident: {inc.incident_code} - {inc.category}",
                message=f"War room activated. Statutory CERT-In 6-hour reporting window active for {inc.affected_systems}.",
                severity="CRITICAL",
                target_role="SECOPS_LEAD",
                action_url="#view-secops",
                action_label="Open War Room"
            )
            created_count += 1

    # 4. Check Internal P1 Service Desk Tickets
    crit_tickets = db.query(InternalTicket).filter(
        InternalTicket.priority == "P1-Critical",
        InternalTicket.status.in_(["Open", "In Progress"])
    ).all()
    for tkt in crit_tickets:
        exists = db.query(SystemNotification).filter(
            SystemNotification.title.like(f"%{tkt.ticket_number}%")
        ).first()
        if not exists:
            broadcast_alert(
                db,
                module_source="TICKETING",
                title=f"P1 Service Desk Alert: {tkt.ticket_number} ({tkt.department})",
                message=f"{tkt.subject} submitted by {tkt.requester_name}. 2-hour SLA deadline active.",
                severity="CRITICAL",
                target_role="ALL",
                action_url="#view-internal-support",
                action_label="Respond Ticket"
            )
            created_count += 1

    # 5. Check Deal Desk Approvals Required
    pending_deals = db.query(Opportunity).filter(
        Opportunity.deal_desk_status == "Director Approval Required"
    ).all()
    for opp in pending_deals:
        exists = db.query(SystemNotification).filter(
            SystemNotification.title.like(f"%{opp.deal_code}%")
        ).first()
        if not exists:
            broadcast_alert(
                db,
                module_source="CRM_LEGAL",
                title=f"Deal Desk Authorization Required: {opp.deal_code}",
                message=f"{opp.client_name} requested {opp.discount_pct}% discount on ₹{opp.contract_value:,.2f} deal.",
                severity="WARNING",
                target_role="DIRECTOR",
                action_url="#view-crm",
                action_label="Review Deal Desk"
            )
            created_count += 1

    return created_count
