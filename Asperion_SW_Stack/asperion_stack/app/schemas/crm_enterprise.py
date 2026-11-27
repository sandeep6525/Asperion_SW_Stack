"""
Asperion Enterprise OS - Comprehensive Pydantic Validation Schemas for Enterprise CRM, Accounts & ERM
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# 1. Opportunity Schemas
class OpportunityBase(BaseModel):
    opportunity_code: str
    prospect_id: Optional[int] = None
    client_name: str
    deal_title: str
    deal_value_inr: float = Field(..., gt=0)
    stage: str = "Lead Qualified"
    probability_pct: float = 10.0
    expected_close_date: date
    owner: str = "Director / Sales Lead"
    deal_type: str = "New Business"
    deal_desk_status: str = "Standard Terms"
    discount_offered_pct: float = 0.0
    payment_terms: str = "Net 30 Days"
    competitors: Optional[str] = None
    win_loss_reason: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityStageUpdate(BaseModel):
    stage: str # Lead Qualified, Discovery, Solution Architecture, Legal/Deal Desk, Closed Won, Closed Lost
    win_loss_reason: Optional[str] = None

class OpportunityOut(OpportunityBase):
    id: int
    weighted_value_inr: float
    created_at: datetime
    class Config:
        from_attributes = True

# 2. Activity Schemas
class CRMActivityBase(BaseModel):
    activity_type: str = "Discovery Call"
    subject: str
    opportunity_id: Optional[int] = None
    client_name: str
    performed_by: str = "Sales Lead"
    activity_date: Optional[date] = None
    duration_minutes: int = 45
    key_takeaways: str
    action_items: Optional[str] = None
    next_followup_date: Optional[date] = None

class CRMActivityCreate(CRMActivityBase):
    pass

class CRMActivityOut(CRMActivityBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# 3. Customer Account Schemas
class CustomerAccountBase(BaseModel):
    account_code: str
    client_name: str
    tier: str = "Tier 1 Enterprise"
    industry: str = "Enterprise Technology"
    primary_csm: str = "Customer Success Lead"
    executive_sponsor: str = "Varadi Vijay (Director)"
    annual_recurring_revenue_inr: float = 0.0
    health_score: float = 95.0
    health_status: str = "Healthy"
    nps_score: int = 9
    contract_start_date: date
    renewal_date: date
    churn_risk_level: str = "Low"
    notes: Optional[str] = None

class CustomerAccountCreate(CustomerAccountBase):
    pass

class CustomerAccountOut(CustomerAccountBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# 4. Support Ticket Schemas
class SupportTicketBase(BaseModel):
    ticket_number: str
    account_id: Optional[int] = None
    client_name: str
    contact_email: str
    subject: str
    description: str
    category: str = "Platform Feature"
    severity: str = "P3-Medium"
    assigned_engineer: str = "Support Engineering Lead"

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicketStatusUpdate(BaseModel):
    status: str # In Triage, Work in Progress, Resolved, Closed
    resolution_summary: Optional[str] = None
    csat_rating: Optional[int] = None

class SupportTicketOut(SupportTicketBase):
    id: int
    sla_response_hours: float
    sla_deadline: Optional[datetime] = None
    status: str
    resolution_summary: Optional[str] = None
    csat_rating: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    class Config:
        from_attributes = True

# 5. Enterprise Risk Schemas (ERM)
class EnterpriseRiskBase(BaseModel):
    risk_code: str
    risk_category: str = "Operational"
    risk_title: str
    risk_description: str
    inherent_severity: int = 3
    inherent_probability: int = 3
    existing_controls: Optional[str] = None
    residual_severity: int = 2
    residual_probability: int = 1
    treatment_strategy: str = "Mitigate"
    risk_owner: str = "Director / Governance Lead"
    review_cadence: str = "Quarterly"
    status: str = "Controlled"

class EnterpriseRiskCreate(EnterpriseRiskBase):
    pass

class EnterpriseRiskOut(EnterpriseRiskBase):
    id: int
    inherent_rpn: int
    residual_rpn: int
    created_at: datetime
    class Config:
        from_attributes = True
