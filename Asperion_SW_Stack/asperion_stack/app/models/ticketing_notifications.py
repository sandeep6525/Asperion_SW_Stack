"""
Asperion Enterprise OS - Internal Ticketing, Alerts & Notifications Models
Multi-department service desk and cross-functional notification bus.
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from datetime import datetime
from app.database import Base

class InternalTicket(Base):
    """
    Cross-departmental internal service desk ticket.
    Serves IT, HR, Finance, Legal, Admin, SecOps, and PMO.
    """
    __tablename__ = "internal_service_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. IT-TKT-2026-001
    department = Column(String(50), index=True, nullable=False) # IT_INFRASTRUCTURE, HR_PEOPLE, FINANCE_ACCOUNTS, etc.
    category = Column(String(100), nullable=False) # Hardware, Access, Payroll, Expense, NDA Review, etc.
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="P3-Medium") # P1-Critical, P2-High, P3-Medium, P4-Low
    status = Column(String(30), default="Open", index=True) # Open, In Progress, Pending Approval, Resolved, Closed
    
    requester_name = Column(String(100), nullable=False)
    requester_email = Column(String(120), nullable=False)
    requester_department = Column(String(50), nullable=False)
    
    assigned_to = Column(String(100), default="Unassigned")
    assigned_department = Column(String(50), nullable=True)
    
    sla_deadline_hours = Column(Float, default=24.0)
    sla_breached = Column(Boolean, default=False)
    target_resolution_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_summary = Column(Text, nullable=True)
    satisfaction_score = Column(Integer, nullable=True) # 1 to 5 stars
    
    comments_json = Column(Text, default="[]") # JSON list of threaded comments/notes
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemNotification(Base):
    """
    Omni-channel system alert and notification entity across all operational pillars.
    """
    __tablename__ = "system_notifications"

    id = Column(Integer, primary_key=True, index=True)
    notification_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. NOTIF-2026-001
    module_source = Column(String(50), index=True, nullable=False) # GOVERNANCE, FINANCE, HRMS, PMO, SECOPS, etc.
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="INFO", index=True) # CRITICAL, WARNING, INFO, SUCCESS
    target_role = Column(String(50), default="ALL", index=True) # ALL, DIRECTOR, FINANCE_HEAD, HR_LEAD, etc.
    
    is_read = Column(Boolean, default=False, index=True)
    is_dismissed = Column(Boolean, default=False, index=True)
    
    action_url = Column(String(255), nullable=True) # #view-finance, #view-secops, #view-tickets
    action_label = Column(String(100), nullable=True) # Inspect, Review, Resolve
    
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)

class NotificationRule(Base):
    """
    Automated notification trigger rule.
    """
    __tablename__ = "notification_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(100), nullable=False)
    event_trigger = Column(String(100), nullable=False, unique=True)
    department = Column(String(50), nullable=False)
    severity = Column(String(20), default="INFO")
    channel = Column(String(50), default="ALL") # IN_APP, EMAIL_SIMULATED, WEBHOOK, ALL
    is_active = Column(Boolean, default=True)
