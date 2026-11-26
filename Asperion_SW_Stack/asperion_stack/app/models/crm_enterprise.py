"""
Asperion Enterprise OS - Comprehensive Enterprise CRM, Customer Success, Service Desk & ERM Models
Covers Deal Pipeline, Activities, Customer Accounts, SLA Support Tickets, and Enterprise Risk Management.
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Opportunity(Base):
    __tablename__ = "crm_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    opportunity_code = Column(String(50), unique=True, index=True) # e.g. ADT-OPP-2026-001
    prospect_id = Column(Integer, ForeignKey("prospects.id"), nullable=True)
    client_name = Column(String(255), nullable=False)
    deal_title = Column(String(255), nullable=False)
    deal_value_inr = Column(Float, default=0.0)
    stage = Column(String(50), default="Lead Qualified") 
    # Stages: Lead Qualified (10%), Discovery (25%), Solution Architecture (50%), Legal/Deal Desk (80%), Closed Won (100%), Closed Lost (0%)
    probability_pct = Column(Float, default=10.0)
    weighted_value_inr = Column(Float, default=0.0)
    expected_close_date = Column(Date, nullable=False)
    owner = Column(String(100), default="Director / Sales Lead")
    deal_type = Column(String(50), default="New Business") # New Business, Expansion, Renewal, Professional Services Retainer
    deal_desk_status = Column(String(50), default="Pending Review") # Pending Review, Approved, Standard Terms, Discount Exception Approved
    discount_offered_pct = Column(Float, default=0.0)
    payment_terms = Column(String(50), default="Net 30 Days")
    competitors = Column(String(255), nullable=True)
    win_loss_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    activities = relationship("CRMActivity", back_populates="opportunity")

class CRMActivity(Base):
    __tablename__ = "crm_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String(50), nullable=False) # Technical Demo, Architecture Review, Deal Negotiation, Discovery Call, QBR
    subject = Column(String(255), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("crm_opportunities.id"), nullable=True)
    client_name = Column(String(255), nullable=False)
    performed_by = Column(String(100), default="Sales Lead")
    activity_date = Column(Date, default=date.today)
    duration_minutes = Column(Integer, default=45)
    key_takeaways = Column(Text, nullable=False)
    action_items = Column(Text, nullable=True)
    next_followup_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    opportunity = relationship("Opportunity", back_populates="activities")

class CustomerAccount(Base):
    __tablename__ = "crm_customer_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_code = Column(String(50), unique=True, index=True) # e.g. ADT-ACC-001
    client_name = Column(String(255), nullable=False, unique=True)
    tier = Column(String(50), default="Tier 1 Enterprise") # Tier 1 Enterprise, Tier 2 Mid-Market, Tier 3 Growth
    industry = Column(String(100), default="Enterprise Technology")
    primary_csm = Column(String(100), default="Customer Success Lead")
    executive_sponsor = Column(String(100), default="Varadi Vijay (Director)")
    annual_recurring_revenue_inr = Column(Float, default=0.0)
    health_score = Column(Integer, default=95) # 0 to 100
    health_status = Column(String(30), default="Healthy") # Healthy, At Risk, Critical
    nps_score = Column(Integer, default=9) # Net Promoter Score 1 to 10
    contract_start_date = Column(Date, nullable=False)
    renewal_date = Column(Date, nullable=False)
    churn_risk_level = Column(String(20), default="Low") # Low, Medium, High
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("SupportTicket", back_populates="account")

class SupportTicket(Base):
    __tablename__ = "crm_support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True) # e.g. ADT-SRV-2026-001
    account_id = Column(Integer, ForeignKey("crm_customer_accounts.id"), nullable=True)
    client_name = Column(String(255), nullable=False)
    contact_email = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), default="Platform Feature") # Platform Feature, Integration Bug, Performance Latency, Security Query, Billing
    severity = Column(String(20), default="P3-Medium") # P1-Critical (1h), P2-High (4h), P3-Medium (12h), P4-Low (24h)
    sla_response_hours = Column(Float, default=12.0)
    sla_deadline = Column(DateTime, nullable=True)
    assigned_engineer = Column(String(100), default="Support Engineering Lead")
    status = Column(String(50), default="Open") # Open, In Triage, Work in Progress, Awaiting Client, Resolved, Closed
    resolution_summary = Column(Text, nullable=True)
    csat_rating = Column(Integer, nullable=True) # 1 to 5 stars
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("CustomerAccount", back_populates="tickets")

class EnterpriseRisk(Base):
    __tablename__ = "crm_enterprise_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    risk_code = Column(String(50), unique=True, index=True) # e.g. ERM-2026-001
    risk_category = Column(String(50), default="Operational") # Strategic, Operational, Financial, Compliance & Legal, Technological / Cyber
    risk_title = Column(String(255), nullable=False)
    risk_description = Column(Text, nullable=False)
    inherent_severity = Column(Integer, default=3) # 1 to 5
    inherent_probability = Column(Integer, default=3) # 1 to 5
    inherent_rpn = Column(Integer, default=9) # Inherent Severity x Probability
    existing_controls = Column(Text, nullable=True)
    residual_severity = Column(Integer, default=2) # 1 to 5
    residual_probability = Column(Integer, default=1) # 1 to 5
    residual_rpn = Column(Integer, default=2)
    treatment_strategy = Column(String(50), default="Mitigate") # Mitigate, Transfer, Avoid, Accept
    risk_owner = Column(String(100), default="Director / Governance Lead")
    review_cadence = Column(String(50), default="Quarterly")
    status = Column(String(50), default="Controlled") # Controlled, Under Treatment, Escalated, Closed
    created_at = Column(DateTime, default=datetime.utcnow)
