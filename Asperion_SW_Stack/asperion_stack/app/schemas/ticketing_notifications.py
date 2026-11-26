"""
Asperion Enterprise OS - Internal Ticketing, Alerts & Notifications Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class InternalTicketBase(BaseModel):
    department: str = Field(..., description="Target department (IT_INFRASTRUCTURE, HR_PEOPLE, FINANCE_ACCOUNTS, etc.)")
    category: str = Field(..., description="Category (Hardware, Access, Payroll, Expense, etc.)")
    subject: str = Field(..., description="Short summary of issue or request")
    description: str = Field(..., description="Detailed description")
    priority: str = Field("P3-Medium", description="Priority (P1-Critical, P2-High, P3-Medium, P4-Low)")
    requester_name: str
    requester_email: str
    requester_department: str

class InternalTicketCreate(InternalTicketBase):
    pass

class InternalTicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_department: Optional[str] = None
    resolution_summary: Optional[str] = None
    satisfaction_score: Optional[int] = Field(None, ge=1, le=5)

class InternalTicketCommentCreate(BaseModel):
    author_name: str
    message: str
    is_internal_note: bool = False

class InternalTicketOut(InternalTicketBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    ticket_number: str
    status: str
    assigned_to: str
    assigned_department: Optional[str] = None
    sla_deadline_hours: float
    sla_breached: bool
    target_resolution_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_summary: Optional[str] = None
    satisfaction_score: Optional[int] = None
    comments_json: str
    created_at: datetime
    updated_at: datetime

class SystemNotificationBase(BaseModel):
    module_source: str
    title: str
    message: str
    severity: str = "INFO" # CRITICAL, WARNING, INFO, SUCCESS
    target_role: str = "ALL"
    action_url: Optional[str] = None
    action_label: Optional[str] = None

class SystemNotificationCreate(SystemNotificationBase):
    pass

class SystemNotificationOut(SystemNotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notification_code: str
    is_read: bool
    is_dismissed: bool
    created_at: datetime
    read_at: Optional[datetime] = None

class NotificationRuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rule_name: str
    event_trigger: str
    department: str
    severity: str
    channel: str
    is_active: bool

class DepartmentSummaryItem(BaseModel):
    department: str
    display_name: str
    total_tickets: int
    open_tickets: int
    resolved_tickets: int
    sla_breached_count: int
    sla_compliance_pct: float
    avg_resolution_hours: float

class TicketServiceDeskSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    critical_p1_tickets: int
    sla_compliance_pct: float
    departments: List[DepartmentSummaryItem]

class ActiveAlertBannerOut(BaseModel):
    has_active_critical: bool
    critical_count: int
    warning_count: int
    unread_notifications_count: int
    top_critical_alert: Optional[SystemNotificationOut] = None
