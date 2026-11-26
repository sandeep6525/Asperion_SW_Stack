"""
Asperion Enterprise OS - Comprehensive Test Suite for Internal Ticketing, Alerts & Notifications
Directly tests router functions, SLA calculations, departmental auto-numbering, and omni-channel alerts.
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.ticketing_notifications import InternalTicket, SystemNotification
from app.api.ticketing_notifications import (
    list_internal_tickets, create_internal_ticket, get_internal_ticket,
    update_internal_ticket, add_ticket_comment, get_service_desk_summary,
    list_system_notifications, mark_notification_read, mark_all_notifications_read,
    dismiss_notification, broadcast_custom_notification, get_active_alert_banner,
    trigger_sync_alerts
)
from app.schemas.ticketing_notifications import (
    InternalTicketCreate, InternalTicketUpdate, InternalTicketCommentCreate,
    SystemNotificationCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_internal_tickets_list_and_summary(db_session):
    # 1. List all tickets
    tickets = list_internal_tickets(db=db_session)
    assert isinstance(tickets, list)
    assert len(tickets) >= 8

    # 2. Filter by department
    it_tkts = list_internal_tickets(department="IT_INFRASTRUCTURE", db=db_session)
    assert len(it_tkts) >= 2
    assert all(t.department == "IT_INFRASTRUCTURE" for t in it_tkts)

    # 3. Summary metrics
    summary = get_service_desk_summary(db=db_session)
    assert summary.total_tickets >= 8
    assert summary.sla_compliance_pct >= 0.0
    assert len(summary.departments) >= 5

def test_internal_ticket_create_and_auto_numbering(db_session):
    payload_it = InternalTicketCreate(
        department="IT_INFRASTRUCTURE",
        category="Zero Trust Access",
        subject="WireGuard Client Certificate Renewal for Engineering Subnet",
        description="Developer subnet access certificate expiring in 48 hours.",
        priority="P2-High",
        requester_name="Dev Tester",
        requester_email="tester@asperion.in",
        requester_department="PMO_ENGINEERING"
    )
    created_it = create_internal_ticket(ticket_in=payload_it, db=db_session)
    assert created_it.ticket_number.startswith("IT-TKT-")
    assert created_it.sla_deadline_hours == 8.0
    assert created_it.status == "Open"
    assert created_it.target_resolution_at is not None

    # Test HR Department Auto-Numbering
    payload_hr = InternalTicketCreate(
        department="HR_PEOPLE",
        category="Payroll Discrepancy",
        subject="Gratuity Provision Calculation Query for 5+ Year Tenured Employee",
        description="Clarification on 15/26 calculation formula.",
        priority="P3-Medium",
        requester_name="Dev Tester",
        requester_email="tester@asperion.in",
        requester_department="PMO_ENGINEERING"
    )
    created_hr = create_internal_ticket(ticket_in=payload_hr, db=db_session)
    assert created_hr.ticket_number.startswith("HR-TKT-")
    assert created_hr.sla_deadline_hours == 24.0

def test_internal_ticket_patch_and_resolution(db_session):
    payload = InternalTicketCreate(
        department="FINANCE_ACCOUNTS",
        category="Expense Reimbursement",
        subject="Travel to Client Horamavu Site Cab Voucher",
        description="INR 450 Uber voucher reimbursement.",
        priority="P4-Low",
        requester_name="Dev Tester",
        requester_email="tester@asperion.in",
        requester_department="PMO_ENGINEERING"
    )
    created = create_internal_ticket(ticket_in=payload, db=db_session)
    tkt_id = created.id

    # Update to In Progress
    in_prog = update_internal_ticket(
        ticket_id=tkt_id,
        update_in=InternalTicketUpdate(status="In Progress", assigned_to="Finance Officer"),
        db=db_session
    )
    assert in_prog.status == "In Progress"
    assert in_prog.assigned_to == "Finance Officer"

    # Resolve ticket
    resolved = update_internal_ticket(
        ticket_id=tkt_id,
        update_in=InternalTicketUpdate(
            status="Resolved",
            resolution_summary="Reimbursement approved and scheduled in ICICI payout batch.",
            satisfaction_score=5
        ),
        db=db_session
    )
    assert resolved.status == "Resolved"
    assert resolved.resolved_at is not None
    assert resolved.satisfaction_score == 5

def test_internal_ticket_comment_thread(db_session):
    tickets = list_internal_tickets(db=db_session)
    tkt_id = tickets[0].id

    comment_in = InternalTicketCommentCreate(
        author_name="Lead Architect",
        message="Tested packet trace, MTU set to 1420 bytes fixes the drop.",
        is_internal_note=True
    )
    updated = add_ticket_comment(ticket_id=tkt_id, comment_in=comment_in, db=db_session)
    assert "MTU set to 1420" in updated.comments_json

def test_system_notifications_list_and_unread_count(db_session):
    notifs = list_system_notifications(db=db_session)
    assert len(notifs) >= 7

    # Filter by severity
    crit_notifs = list_system_notifications(severity="CRITICAL", db=db_session)
    assert len(crit_notifs) >= 1
    assert all(n.severity == "CRITICAL" for n in crit_notifs)

def test_notification_mark_read_and_dismiss(db_session):
    unread = list_system_notifications(unread_only=True, db=db_session)
    assert len(unread) > 0
    target_id = unread[0].id

    # Mark as read
    read_item = mark_notification_read(notification_id=target_id, db=db_session)
    assert read_item.is_read is True
    assert read_item.read_at is not None

    # Dismiss
    dismissed_item = dismiss_notification(notification_id=target_id, db=db_session)
    assert dismissed_item.is_dismissed is True

    # Mark all read
    res = mark_all_notifications_read(db=db_session)
    assert res["status"] == "success"

def test_active_alert_banner_and_sync(db_session):
    sync_res = trigger_sync_alerts(db=db_session)
    assert sync_res["status"] == "success"

    banner = get_active_alert_banner(db=db_session)
    assert isinstance(banner.has_active_critical, bool)
    assert hasattr(banner, "critical_count")
    assert hasattr(banner, "unread_notifications_count")

def test_broadcast_custom_notification(db_session):
    custom_in = SystemNotificationCreate(
        module_source="INFRASTRUCTURE",
        title="Scheduled Maintenance: AWS ap-south-1 DirectConnect Maintenance Window",
        message="Routine maintenance scheduled Sunday 02:00 AM IST. Failover to redundant IPSec tunnel tested.",
        severity="INFO",
        target_role="ALL",
        action_url="#view-infrastructure",
        action_label="View Maintenance Schedule"
    )
    broadcasted = broadcast_custom_notification(notif_in=custom_in, db=db_session)
    assert broadcasted.notification_code.startswith("NOTIF-")
    assert broadcasted.severity == "INFO"
    assert broadcasted.is_read is False
