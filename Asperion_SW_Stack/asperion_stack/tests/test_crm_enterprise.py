"""
Unit & Integration Tests for Enterprise CRM, Opportunity Pipeline, Customer Success & ERM
"""
import pytest
from datetime import date, timedelta
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.crm_enterprise import Opportunity, CustomerAccount, SupportTicket, EnterpriseRisk
from app.api.crm_enterprise import (
    get_pipeline_summary, list_opportunities, create_opportunity, update_opportunity_stage,
    list_activities, create_activity, list_accounts, create_account,
    list_tickets, create_ticket, update_ticket_status,
    list_enterprise_risks, create_enterprise_risk
)
from app.schemas.crm_enterprise import (
    OpportunityCreate, OpportunityStageUpdate, CRMActivityCreate,
    CustomerAccountCreate, SupportTicketCreate, SupportTicketStatusUpdate,
    EnterpriseRiskCreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_crm_pipeline_summary(db_session):
    summary = get_pipeline_summary(db=db_session)
    assert summary["status"] == "success"
    pipe = summary["pipeline"]
    assert pipe["total_pipeline_value_inr"] > 0
    assert pipe["active_deals_count"] >= 1
    assert "stage_breakdown" in pipe
    cs = summary["customer_success"]
    assert cs["total_accounts"] >= 1
    assert cs["managed_arr_inr"] > 0
    sd = summary["service_desk"]
    assert sd["total_tickets"] >= 1

def test_crm_opportunities_crud_and_weighted_calc(db_session):
    db_session.query(Opportunity).filter(Opportunity.opportunity_code == "ADT-OPP-TEST-001").delete()
    db_session.query(CustomerAccount).filter(CustomerAccount.client_name == "Test Enterprise Cloud Corp").delete()
    db_session.commit()
    opp_in = OpportunityCreate(
        opportunity_code="ADT-OPP-TEST-001",
        client_name="Test Enterprise Cloud Corp",
        deal_title="Microservices Cloud Modernization",
        deal_value_inr=1000000.0,
        stage="Solution Architecture",
        expected_close_date=date(2026, 9, 30),
        discount_offered_pct=5.0
    )
    saved = create_opportunity(opp_in, db=db_session)
    assert saved.id is not None
    assert saved.probability_pct == 50.0
    assert saved.weighted_value_inr == 500000.0 # 1000000 * 50%

    # Advance stage to Closed Won
    updated = update_opportunity_stage(
        opp_id=saved.id,
        update_in=OpportunityStageUpdate(stage="Closed Won", win_loss_reason="Strong ROI"),
        db=db_session
    )
    assert updated.stage == "Closed Won"
    assert updated.probability_pct == 100.0
    assert updated.weighted_value_inr == 1000000.0

    # Verify auto-created customer account
    acc = db_session.query(CustomerAccount).filter(CustomerAccount.client_name == "Test Enterprise Cloud Corp").first()
    assert acc is not None
    assert acc.annual_recurring_revenue_inr == 1000000.0

def test_crm_deal_desk_discount_guard(db_session):
    db_session.query(Opportunity).filter(Opportunity.opportunity_code == "ADT-OPP-TEST-002").delete()
    db_session.commit()
    opp_in = OpportunityCreate(
        opportunity_code="ADT-OPP-TEST-002",
        client_name="Discount Sensitive Retailer",
        deal_title="Custom Integration",
        deal_value_inr=500000.0,
        stage="Discovery",
        expected_close_date=date(2026, 10, 15),
        discount_offered_pct=20.0 # High discount > 15%
    )
    saved = create_opportunity(opp_in, db=db_session)
    assert "Director Approval Required" in saved.deal_desk_status

def test_crm_activities_logging(db_session):
    act_in = CRMActivityCreate(
        activity_type="Technical Demo",
        subject="AI Agent Platform Architectural Walkthrough",
        client_name="Test Enterprise Cloud Corp",
        duration_minutes=60,
        key_takeaways="CTO impressed with modular clean monolith DDD architecture and sub-50ms API latency."
    )
    act = create_activity(act_in, db=db_session)
    assert act.id is not None
    assert act.duration_minutes == 60

def test_crm_customer_accounts_and_health(db_session):
    accounts = list_accounts(db=db_session)
    assert len(accounts) >= 1
    acc = accounts[0]
    assert acc.health_score > 0
    assert acc.health_status in ["Healthy", "At Risk", "Critical"]

def test_crm_support_tickets_and_sla_deadlines(db_session):
    db_session.query(SupportTicket).filter(SupportTicket.ticket_number == "ADT-SRV-TST-001").delete()
    db_session.commit()
    # Test P1-Critical (1-hour response SLA)
    tkt_in = SupportTicketCreate(
        ticket_number="ADT-SRV-TST-001",
        client_name="Nexus Fintech Solutions India Pvt Ltd",
        contact_email="security@nexusfintech.in",
        subject="Payment Webhook Ingestion Latency Degraded",
        description="Response time exceeded 200ms threshold during peak clearing cycle.",
        category="Performance Latency",
        severity="P1-Critical"
    )
    tkt = create_ticket(tkt_in, db=db_session)
    assert tkt.id is not None
    assert tkt.sla_response_hours == 1.0 # 1-hr SLA for P1
    assert tkt.sla_deadline is not None
    assert tkt.status == "Open"

    # Resolve ticket with 5-star CSAT
    resolved = update_ticket_status(
        ticket_id=tkt.id,
        status_in=SupportTicketStatusUpdate(
            status="Resolved",
            resolution_summary="Optimized DB index on invoice_number and query plan.",
            csat_rating=5
        ),
        db=db_session
    )
    assert resolved.status == "Resolved"
    assert resolved.csat_rating == 5
    assert resolved.resolved_at is not None

def test_enterprise_risk_management_rpn_calc(db_session):
    db_session.query(EnterpriseRisk).filter(EnterpriseRisk.risk_code == "ERM-TST-001").delete()
    db_session.commit()
    risk_in = EnterpriseRiskCreate(
        risk_code="ERM-TST-001",
        risk_category="Technological",
        risk_title="Cloud Region Outage in AWS Mumbai (ap-south-1)",
        risk_description="Unplanned availability zone failure impacting API gateway.",
        inherent_severity=5,
        inherent_probability=2,
        residual_severity=2,
        residual_probability=1,
        treatment_strategy="Mitigate",
        risk_owner="Director / Cloud Lead"
    )
    saved = create_enterprise_risk(risk_in, db=db_session)
    assert saved.id is not None
    assert saved.inherent_rpn == 10 # 5 * 2
    assert saved.residual_rpn == 2  # 2 * 1
    assert saved.treatment_strategy == "Mitigate"
