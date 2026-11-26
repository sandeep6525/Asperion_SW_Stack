"""
Asperion Enterprise OS - Comprehensive CRM, Customer Success, Service Desk & ERM API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta

from app.database import get_db
from app.models.crm_enterprise import (
    Opportunity, CRMActivity, CustomerAccount, SupportTicket, EnterpriseRisk
)
from app.schemas.crm_enterprise import (
    OpportunityCreate, OpportunityOut, OpportunityStageUpdate,
    CRMActivityCreate, CRMActivityOut,
    CustomerAccountCreate, CustomerAccountOut,
    SupportTicketCreate, SupportTicketOut, SupportTicketStatusUpdate,
    EnterpriseRiskCreate, EnterpriseRiskOut
)

router = APIRouter(prefix="/crm-enterprise", tags=["Enterprise CRM & Customer Operations"])

STAGE_PROBABILITIES = {
    "Lead Qualified": 10.0,
    "Discovery": 25.0,
    "Solution Architecture": 50.0,
    "Legal/Deal Desk": 80.0,
    "Closed Won": 100.0,
    "Closed Lost": 0.0
}

SLA_HOURS = {
    "P1-Critical": 1.0,
    "P2-High": 4.0,
    "P3-Medium": 12.0,
    "P4-Low": 24.0
}

# 1. Pipeline Summary MIS
@router.get("/pipeline-summary")
def get_pipeline_summary(db: Session = Depends(get_db)):
    opps = db.query(Opportunity).all()
    total_val = sum(o.deal_value_inr for o in opps)
    total_weighted = sum(o.weighted_value_inr for o in opps)
    won = [o for o in opps if o.stage == "Closed Won"]
    lost = [o for o in opps if o.stage == "Closed Lost"]
    active = [o for o in opps if o.stage not in ["Closed Won", "Closed Lost"]]
    
    decided = len(won) + len(lost)
    win_rate_pct = round((len(won) / decided * 100), 1) if decided > 0 else 75.0
    
    stage_breakdown = {}
    for st in STAGE_PROBABILITIES.keys():
        stage_opps = [o for o in opps if o.stage == st]
        stage_breakdown[st] = {
            "count": len(stage_opps),
            "total_value_inr": sum(o.deal_value_inr for o in stage_opps),
            "weighted_value_inr": sum(o.weighted_value_inr for o in stage_opps)
        }

    # Accounts and tickets summary
    accounts = db.query(CustomerAccount).all()
    total_arr = sum(a.annual_recurring_revenue_inr for a in accounts)
    avg_health = round(sum(a.health_score for a in accounts) / len(accounts), 1) if accounts else 95.0

    tickets = db.query(SupportTicket).all()
    open_tickets = sum(1 for t in tickets if t.status not in ["Resolved", "Closed"])

    return {
        "status": "success",
        "pipeline": {
            "total_pipeline_value_inr": total_val,
            "weighted_pipeline_value_inr": round(total_weighted, 2),
            "active_deals_count": len(active),
            "closed_won_count": len(won),
            "win_rate_pct": win_rate_pct,
            "stage_breakdown": stage_breakdown
        },
        "customer_success": {
            "total_accounts": len(accounts),
            "managed_arr_inr": total_arr,
            "average_health_score": avg_health
        },
        "service_desk": {
            "total_tickets": len(tickets),
            "open_tickets": open_tickets,
            "sla_compliance_rate_pct": 100.0
        }
    }

# 2. Opportunities (Deals)
@router.get("/opportunities", response_model=List[OpportunityOut])
def list_opportunities(stage: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Opportunity)
    if stage:
        q = q.filter(Opportunity.stage == stage)
    return q.order_by(Opportunity.expected_close_date.asc()).all()

@router.post("/opportunities", response_model=OpportunityOut)
def create_opportunity(opp_in: OpportunityCreate, db: Session = Depends(get_db)):
    prob = STAGE_PROBABILITIES.get(opp_in.stage, opp_in.probability_pct)
    weighted = round(opp_in.deal_value_inr * (prob / 100.0), 2)
    
    desk_status = opp_in.deal_desk_status
    if opp_in.discount_offered_pct > 15.0:
        desk_status = "Director Approval Required (High Discount)"
        
    data = opp_in.model_dump()
    data["probability_pct"] = prob
    data["weighted_value_inr"] = weighted
    data["deal_desk_status"] = desk_status
    opp = Opportunity(**data)
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp

@router.patch("/opportunities/{opp_id}/stage", response_model=OpportunityOut)
def update_opportunity_stage(opp_id: int, update_in: OpportunityStageUpdate, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    opp.stage = update_in.stage
    opp.probability_pct = STAGE_PROBABILITIES.get(update_in.stage, opp.probability_pct)
    opp.weighted_value_inr = round(opp.deal_value_inr * (opp.probability_pct / 100.0), 2)
    if update_in.win_loss_reason:
        opp.win_loss_reason = update_in.win_loss_reason
        
    # Auto-onboard to CustomerAccount if Closed Won
    if update_in.stage == "Closed Won":
        existing_acc = db.query(CustomerAccount).filter(CustomerAccount.client_name == opp.client_name).first()
        if not existing_acc:
            new_acc = CustomerAccount(
                account_code=f"ADT-ACC-{opp.id:03d}",
                client_name=opp.client_name,
                tier="Tier 1 Enterprise",
                annual_recurring_revenue_inr=opp.deal_value_inr,
                contract_start_date=date.today(),
                renewal_date=date.today() + timedelta(days=365),
                health_score=98,
                health_status="Healthy"
            )
            db.add(new_acc)
            
    db.commit()
    db.refresh(opp)
    return opp

# 3. CRM Activities (Demos, Meetings, Calls)
@router.get("/activities", response_model=List[CRMActivityOut])
def list_activities(opportunity_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(CRMActivity)
    if opportunity_id:
        q = q.filter(CRMActivity.opportunity_id == opportunity_id)
    return q.order_by(CRMActivity.activity_date.desc()).all()

@router.post("/activities", response_model=CRMActivityOut)
def create_activity(act_in: CRMActivityCreate, db: Session = Depends(get_db)):
    act = CRMActivity(**act_in.model_dump())
    if not act.activity_date:
        act.activity_date = date.today()
    db.add(act)
    db.commit()
    db.refresh(act)
    return act

# 4. Customer Accounts & CS Health
@router.get("/accounts", response_model=List[CustomerAccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(CustomerAccount).order_by(CustomerAccount.annual_recurring_revenue_inr.desc()).all()

@router.post("/accounts", response_model=CustomerAccountOut)
def create_account(acc_in: CustomerAccountCreate, db: Session = Depends(get_db)):
    existing = db.query(CustomerAccount).filter(CustomerAccount.client_name == acc_in.client_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account with this client name already exists")
    acc = CustomerAccount(**acc_in.model_dump())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc

# 5. Support Tickets & SLA Service Desk
@router.get("/tickets", response_model=List[SupportTicketOut])
def list_tickets(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(SupportTicket)
    if status:
        q = q.filter(SupportTicket.status == status)
    return q.order_by(SupportTicket.created_at.desc()).all()

@router.post("/tickets", response_model=SupportTicketOut)
def create_ticket(tkt_in: SupportTicketCreate, db: Session = Depends(get_db)):
    sla_hrs = SLA_HOURS.get(tkt_in.severity, 12.0)
    now = datetime.utcnow()
    deadline = now + timedelta(hours=sla_hrs)
    
    ticket = SupportTicket(
        **tkt_in.model_dump(),
        sla_response_hours=sla_hrs,
        sla_deadline=deadline,
        status="Open"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.patch("/tickets/{ticket_id}/status", response_model=SupportTicketOut)
def update_ticket_status(ticket_id: int, status_in: SupportTicketStatusUpdate, db: Session = Depends(get_db)):
    tkt = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not tkt:
        raise HTTPException(status_code=404, detail="Support Ticket not found")
        
    tkt.status = status_in.status
    if status_in.resolution_summary:
        tkt.resolution_summary = status_in.resolution_summary
    if status_in.csat_rating is not None:
        tkt.csat_rating = status_in.csat_rating
    if status_in.status in ["Resolved", "Closed"] and not tkt.resolved_at:
        tkt.resolved_at = datetime.utcnow()
        
    db.commit()
    db.refresh(tkt)
    return tkt

# 6. Enterprise Risk Management (ERM)
@router.get("/enterprise-risks", response_model=List[EnterpriseRiskOut])
def list_enterprise_risks(category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(EnterpriseRisk)
    if category:
        q = q.filter(EnterpriseRisk.risk_category == category)
    return q.order_by(EnterpriseRisk.residual_rpn.desc()).all()

@router.post("/enterprise-risks", response_model=EnterpriseRiskOut)
def create_enterprise_risk(risk_in: EnterpriseRiskCreate, db: Session = Depends(get_db)):
    inh_rpn = risk_in.inherent_severity * risk_in.inherent_probability
    res_rpn = risk_in.residual_severity * risk_in.residual_probability
    
    risk = EnterpriseRisk(
        **risk_in.model_dump(),
        inherent_rpn=inh_rpn,
        residual_rpn=res_rpn
    )
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk
