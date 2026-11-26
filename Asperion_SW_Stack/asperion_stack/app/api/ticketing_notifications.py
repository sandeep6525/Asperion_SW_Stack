"""
Asperion Enterprise OS - Internal Ticketing, Alerts & Notifications API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import json

from app.database import get_db
from app.models.ticketing_notifications import InternalTicket, SystemNotification, NotificationRule
from app.schemas.ticketing_notifications import (
    InternalTicketCreate, InternalTicketUpdate, InternalTicketOut,
    InternalTicketCommentCreate, SystemNotificationCreate, SystemNotificationOut,
    NotificationRuleOut, TicketServiceDeskSummary, DepartmentSummaryItem,
    ActiveAlertBannerOut
)
from app.engines.notification_engine import (
    generate_ticket_number, calculate_sla_target, broadcast_alert,
    scan_and_sync_system_alerts
)

router = APIRouter(prefix="/internal-support", tags=["Internal Service Desk & Notification Bus"])

# -----------------------------------------------------------------------------
# INTERNAL TICKETING SYSTEM
# -----------------------------------------------------------------------------

@router.get("/tickets", response_model=List[InternalTicketOut])
def list_internal_tickets(
    department: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    requester_email: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    """
    Lists internal tickets across IT, HR, Finance, Legal, Admin, SecOps, and PMO.
    """
    query = db.query(InternalTicket)
    if department and department != "ALL":
        query = query.filter(InternalTicket.department == department)
    if priority and priority != "ALL":
        query = query.filter(InternalTicket.priority == priority)
    if status and status != "ALL":
        query = query.filter(InternalTicket.status == status)
    if requester_email:
        query = query.filter(InternalTicket.requester_email == requester_email)
        
    return query.order_by(InternalTicket.id.desc()).offset(skip).limit(limit).all()

@router.post("/tickets", response_model=InternalTicketOut, status_code=201)
def create_internal_ticket(ticket_in: InternalTicketCreate, db: Session = Depends(get_db)):
    """
    Creates a new internal departmental ticket with auto-generated ticket ID and SLA target.
    """
    ticket_num = generate_ticket_number(db, ticket_in.department)
    sla_hours, target_time = calculate_sla_target(ticket_in.priority)
    
    ticket = InternalTicket(
        ticket_number=ticket_num,
        department=ticket_in.department,
        category=ticket_in.category,
        subject=ticket_in.subject,
        description=ticket_in.description,
        priority=ticket_in.priority,
        status="Open",
        requester_name=ticket_in.requester_name,
        requester_email=ticket_in.requester_email,
        requester_department=ticket_in.requester_department,
        assigned_to="Unassigned",
        sla_deadline_hours=sla_hours,
        target_resolution_at=target_time,
        comments_json=json.dumps([{
            "author": ticket_in.requester_name,
            "message": "Ticket created and dispatched to department queue.",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "is_internal": False
        }])
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Automatically broadcast notification to relevant department
    severity = "CRITICAL" if ticket_in.priority == "P1-Critical" else ("WARNING" if ticket_in.priority == "P2-High" else "INFO")
    broadcast_alert(
        db,
        module_source="TICKETING",
        title=f"New {ticket_in.priority} Ticket: {ticket_num}",
        message=f"{ticket_in.subject} [{ticket_in.department}] filed by {ticket_in.requester_name}.",
        severity=severity,
        target_role="ALL",
        action_url="#view-internal-support",
        action_label="Open Ticket"
    )

    return ticket

@router.get("/tickets/{ticket_id}", response_model=InternalTicketOut)
def get_internal_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(InternalTicket).filter(InternalTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Internal ticket not found")
    return ticket

@router.patch("/tickets/{ticket_id}", response_model=InternalTicketOut)
def update_internal_ticket(ticket_id: int, update_in: InternalTicketUpdate, db: Session = Depends(get_db)):
    """
    Updates ticket status, assignee, resolution, and satisfaction rating.
    """
    ticket = db.query(InternalTicket).filter(InternalTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Internal ticket not found")

    if update_in.status:
        ticket.status = update_in.status
        if update_in.status == "Resolved" and not ticket.resolved_at:
            ticket.resolved_at = datetime.utcnow()
            if ticket.target_resolution_at and ticket.resolved_at > ticket.target_resolution_at:
                ticket.sla_breached = True

    if update_in.assigned_to:
        ticket.assigned_to = update_in.assigned_to
    if update_in.assigned_department:
        ticket.assigned_department = update_in.assigned_department
    if update_in.resolution_summary:
        ticket.resolution_summary = update_in.resolution_summary
    if update_in.satisfaction_score is not None:
        ticket.satisfaction_score = update_in.satisfaction_score

    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/tickets/{ticket_id}/comments", response_model=InternalTicketOut)
def add_ticket_comment(ticket_id: int, comment_in: InternalTicketCommentCreate, db: Session = Depends(get_db)):
    """
    Adds a threaded comment or internal note to the ticket.
    """
    ticket = db.query(InternalTicket).filter(InternalTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Internal ticket not found")

    try:
        comments = json.loads(ticket.comments_json or "[]")
    except Exception:
        comments = []

    comments.append({
        "author": comment_in.author_name,
        "message": comment_in.message,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "is_internal": comment_in.is_internal_note
    })

    ticket.comments_json = json.dumps(comments)
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/summary", response_model=TicketServiceDeskSummary)
def get_service_desk_summary(db: Session = Depends(get_db)):
    """
    Aggregates departmental internal ticketing metrics and SLA adherence.
    """
    all_tickets = db.query(InternalTicket).all()
    total = len(all_tickets)
    open_count = sum(1 for t in all_tickets if t.status == "Open")
    in_prog = sum(1 for t in all_tickets if t.status == "In Progress")
    resolved = sum(1 for t in all_tickets if t.status in ["Resolved", "Closed"])
    p1_count = sum(1 for t in all_tickets if t.priority == "P1-Critical")
    breached = sum(1 for t in all_tickets if t.sla_breached)
    
    compliance_pct = round(((total - breached) / total) * 100, 1) if total > 0 else 100.0

    dept_names = {
        "IT_INFRASTRUCTURE": "IT & Infrastructure",
        "HR_PEOPLE": "HR & People Operations",
        "FINANCE_ACCOUNTS": "Finance & Accounts",
        "LEGAL_COMPLIANCE": "Legal & Corporate Compliance",
        "ADMIN_WORKPLACE": "Workplace & Administration",
        "SECOPS_CYBER": "Cybersecurity & SecOps",
        "PMO_ENGINEERING": "PMO & Engineering Delivery"
    }

    dept_items = []
    for dept_key, display in dept_names.items():
        dept_tkts = [t for t in all_tickets if t.department == dept_key]
        d_total = len(dept_tkts)
        d_open = sum(1 for t in dept_tkts if t.status in ["Open", "In Progress", "Pending Approval"])
        d_res = sum(1 for t in dept_tkts if t.status in ["Resolved", "Closed"])
        d_brch = sum(1 for t in dept_tkts if t.sla_breached)
        d_comp = round(((d_total - d_brch) / d_total) * 100, 1) if d_total > 0 else 100.0
        
        # Avg resolution calculation
        res_times = []
        for t in dept_tkts:
            if t.resolved_at and t.created_at:
                diff_hours = (t.resolved_at - t.created_at).total_seconds() / 3600.0
                res_times.append(diff_hours)
        avg_res = round(sum(res_times) / len(res_times), 1) if res_times else 4.0

        dept_items.append(DepartmentSummaryItem(
            department=dept_key,
            display_name=display,
            total_tickets=d_total,
            open_tickets=d_open,
            resolved_tickets=d_res,
            sla_breached_count=d_brch,
            sla_compliance_pct=d_comp,
            avg_resolution_hours=avg_res
        ))

    return TicketServiceDeskSummary(
        total_tickets=total,
        open_tickets=open_count,
        in_progress_tickets=in_prog,
        resolved_tickets=resolved,
        critical_p1_tickets=p1_count,
        sla_compliance_pct=compliance_pct,
        departments=dept_items
    )

# -----------------------------------------------------------------------------
# OMNI-CHANNEL ALERTS & NOTIFICATIONS
# -----------------------------------------------------------------------------

@router.get("/notifications", response_model=List[SystemNotificationOut])
def list_system_notifications(
    severity: Optional[str] = None,
    target_role: Optional[str] = None,
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lists system notifications with filters for severity, role, and unread state.
    """
    query = db.query(SystemNotification).filter(SystemNotification.is_dismissed == False)
    if severity and severity != "ALL":
        query = query.filter(SystemNotification.severity == severity.upper())
    if target_role and target_role != "ALL":
        query = query.filter(SystemNotification.target_role.in_([target_role.upper(), "ALL"]))
    if unread_only:
        query = query.filter(SystemNotification.is_read == False)

    return query.order_by(SystemNotification.id.desc()).limit(limit).all()

@router.patch("/notifications/{notification_id}/read", response_model=SystemNotificationOut)
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(SystemNotification).filter(SystemNotification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    notif.read_at = datetime.utcnow()
    db.commit()
    db.refresh(notif)
    return notif

@router.post("/notifications/mark-all-read")
def mark_all_notifications_read(db: Session = Depends(get_db)):
    """
    Marks all notifications as read.
    """
    now = datetime.utcnow()
    db.query(SystemNotification).filter(SystemNotification.is_read == False).update({
        "is_read": True,
        "read_at": now
    })
    db.commit()
    return {"status": "success", "message": "All notifications marked as read."}

@router.patch("/notifications/{notification_id}/dismiss", response_model=SystemNotificationOut)
def dismiss_notification(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(SystemNotification).filter(SystemNotification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_dismissed = True
    db.commit()
    db.refresh(notif)
    return notif

@router.post("/notifications/broadcast", response_model=SystemNotificationOut, status_code=201)
def broadcast_custom_notification(notif_in: SystemNotificationCreate, db: Session = Depends(get_db)):
    """
    Broadcasts a custom enterprise notification across groups.
    """
    return broadcast_alert(
        db,
        module_source=notif_in.module_source,
        title=notif_in.title,
        message=notif_in.message,
        severity=notif_in.severity,
        target_role=notif_in.target_role,
        action_url=notif_in.action_url,
        action_label=notif_in.action_label
    )

@router.get("/alerts/active-banner", response_model=ActiveAlertBannerOut)
def get_active_alert_banner(db: Session = Depends(get_db)):
    """
    Computes global header alert banner status.
    """
    crit_count = db.query(SystemNotification).filter(
        SystemNotification.severity == "CRITICAL",
        SystemNotification.is_dismissed == False,
        SystemNotification.is_read == False
    ).count()

    warn_count = db.query(SystemNotification).filter(
        SystemNotification.severity == "WARNING",
        SystemNotification.is_dismissed == False,
        SystemNotification.is_read == False
    ).count()

    unread_count = db.query(SystemNotification).filter(
        SystemNotification.is_read == False,
        SystemNotification.is_dismissed == False
    ).count()

    top_crit = db.query(SystemNotification).filter(
        SystemNotification.severity == "CRITICAL",
        SystemNotification.is_dismissed == False
    ).order_by(SystemNotification.id.desc()).first()

    return ActiveAlertBannerOut(
        has_active_critical=crit_count > 0,
        critical_count=crit_count,
        warning_count=warn_count,
        unread_notifications_count=unread_count,
        top_critical_alert=top_crit
    )

@router.post("/sync-alerts")
def trigger_sync_alerts(db: Session = Depends(get_db)):
    """
    Triggers automated scan and creation of active alerts.
    """
    created = scan_and_sync_system_alerts(db)
    return {"status": "success", "created_alerts_count": created}
