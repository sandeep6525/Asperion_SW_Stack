"""
Asperion Enterprise OS - Governance Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class EntityMasterBase(BaseModel):
    entity_name: str
    cin: str
    registered_office: Optional[str] = None
    pan: Optional[str] = None
    tan: Optional[str] = None
    gstin: Optional[str] = None
    sole_member_director: Optional[str] = None
    authorized_capital: float = 100000.0
    paid_up_capital: float = 100000.0
    status: str = "Active"

class EntityMasterOut(EntityMasterBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class BoardResolutionCreate(BaseModel):
    resolution_number: str
    title: str
    resolution_type: str = "OPC Member Resolution"
    date_passed: date
    subject_category: str
    resolution_text: str
    authorized_signatory: str
    mca_filing_required: bool = False
    mca_srn: Optional[str] = None

class BoardResolutionOut(BoardResolutionCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ComplianceCalendarItemCreate(BaseModel):
    compliance_name: str
    statutory_authority: str
    form_or_return: str
    due_date: date
    frequency: str = "Monthly"
    financial_year: str = "2026-2027"
    owner: str = "Finance & Legal Lead"
    penalty_risk: str = "Medium"

class ComplianceCalendarItemOut(ComplianceCalendarItemCreate):
    id: int
    status: str
    filing_reference: Optional[str] = None
    class Config:
        from_attributes = True

class AuditLogCreate(BaseModel):
    event_type: str
    severity: str = "INFO"
    actor: str = "System"
    module: str
    description: str
    ip_address: Optional[str] = "127.0.0.1"

class AuditLogOut(AuditLogCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

