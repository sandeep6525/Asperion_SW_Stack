"""
Unit & Integration Tests for Complete & Comprehensive Client Project Delivery, Billing & SLA Portal
Validates:
1. Executive Telemetry, KPIs & Corporate Entity verification (Director Varadi Vijay, CIN U85500KA2026OPC222069)
2. Agile Deliverables, Epics & Milestone UAT Sign-off lifecycle
3. 24x7 SLA Support Incident Dispatch & automatic SLA Deadline Calculation (P1 < 1.0h, P2 < 4.0h)
4. Commercial B2B Tax Invoicing & Bank Wire Remittance Recording
5. Scope Change Request (CR) Review & Approval workflow
6. High-Fidelity Printable B2B Tax Invoice HTML Document generation (SAC 998314, GSTIN, Corporate Seal)
7. Formal Client Statement of Account (SOA) Ledger generation
"""
import uuid
import pytest
from datetime import date, datetime, timedelta
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.portals import (
    get_client_portal_data, create_client_ticket, signoff_client_milestone,
    review_client_change_request, record_client_invoice_payment,
    get_client_invoice_html, get_client_statement_of_account_html,
    ClientTicketCreateRequest, ClientMilestoneSignoffRequest,
    ClientChangeRequestReview, ClientPaymentRecordRequest
)
from app.models.pmo import Project, ProjectMilestone, ChangeRequest
from app.models.finance import Invoice
from app.models.crm_enterprise import SupportTicket

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_client_portal_overview_and_telemetry(db_session):
    data = get_client_portal_data(client_name="Zenith Global Corp", db=db_session)
    assert data["status"] == "success"
    assert data["client_name"] == "Zenith Global Corp"
    assert "Enterprise Retainer" in data["relationship_tier"]
    assert "Varadi Vijay" in data["dedicated_spoc"]
    assert "99.98%" in data["sla_coverage"]

    # Corporate Entity
    corp = data["corporate_entity"]
    assert corp["entity_name"] == "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    assert corp["cin"] == "U85500KA2026OPC222069"
    assert corp["director"] == "Varadi Vijay"
    assert corp["gstin"] == "29AABCU9603R1ZM"
    assert corp["bank_name"] == "ICICI Bank Limited"

    # Client Profile
    profile = data["client_profile"]
    assert profile["account_code"] == "CUST-ZENITH-01"
    assert profile["health_score"] >= 90.0
    assert profile["nps_score"] >= 70

    # Executive KPIs
    kpis = data["executive_kpis"]
    assert kpis["contracted_uptime_pct"] >= 99.9
    assert kpis["p1_sla_target_hours"] == 1.0
    assert kpis["total_sow_value_inr"] >= 3600000.0
    assert kpis["total_billed_inr"] > 0.0
    assert kpis["milestones_total"] >= 4
    assert kpis["milestones_progress_pct"] >= 50.0

    # Collections
    assert len(data["active_projects"]) >= 1
    assert len(data["project_milestones"]) >= 4
    assert len(data["billing_invoices"]) >= 3
    assert len(data["sla_tickets"]) >= 3
    assert len(data["change_orders"]) >= 2
    assert len(data["contracts_and_agreements"]) >= 3
    assert len(data["wbs_tasks"]) >= 5


def test_client_ticket_logging_and_sla_deadline(db_session):
    # Log P1 Critical Ticket (1h SLA)
    test_subject = f"API Webhook Latency Spike Test {uuid.uuid4().hex[:6]}"
    req_p1 = ClientTicketCreateRequest(
        client_name="Zenith Global Corp",
        contact_email="sre@zenith.com",
        subject=test_subject,
        description="Observed 1200ms round-trip latency on checkout endpoints.",
        category="Performance Latency",
        severity="P1-Critical"
    )
    res_p1 = create_client_ticket(req=req_p1, db=db_session)
    assert res_p1["status"] == "success"
    assert res_p1["ticket"]["severity"] == "P1-Critical"
    assert res_p1["ticket"]["sla_response_hours"] == 1.0

    # Verify presence in portal
    portal_data = get_client_portal_data(client_name="Zenith Global Corp", db=db_session)
    assert any(t["subject"] == test_subject for t in portal_data["sla_tickets"])


def test_client_milestone_signoff_lifecycle(db_session):
    # Find milestone that is not yet client approved
    milestone = db_session.query(ProjectMilestone).filter(ProjectMilestone.status != "Client Approved").first()
    if not milestone:
        # Create a test milestone
        proj = db_session.query(Project).first()
        milestone = ProjectMilestone(
            project_id=proj.id,
            milestone_name=f"Test Sprint 15 Cutover {uuid.uuid4().hex[:4]}",
            target_date=date(2026, 12, 1),
            deliverable_summary="Test automated blue/green cutover",
            payment_linked_percent=20.0,
            billing_amount=500000.0,
            status="UAT Under Review"
        )
        db_session.add(milestone)
        db_session.commit()
        db_session.refresh(milestone)

    signoff_req = ClientMilestoneSignoffRequest(
        client_signatory_name="Michael Chang (VP Engineering)",
        approval_status="Client Approved",
        acceptance_notes="All UAT test criteria 100% verified in staging environment."
    )
    res = signoff_client_milestone(milestone_id=milestone.id, req=signoff_req, db=db_session)
    assert res["status"] == "success"
    assert res["status_now"] == "Client Approved"
    assert res["signoff_by"] == "Michael Chang (VP Engineering)"

    # Verify db record
    db_session.refresh(milestone)
    assert milestone.status == "Client Approved"
    assert milestone.completion_date == date.today()
    assert milestone.signoff_by == "Michael Chang (VP Engineering)"


def test_client_change_request_review(db_session):
    # Find or create a submitted change request
    cr = db_session.query(ChangeRequest).filter(ChangeRequest.status == "Submitted / Under Evaluation").first()
    if not cr:
        proj = db_session.query(Project).first()
        cr = ChangeRequest(
            cr_number=f"ADT-CR-TEST-{uuid.uuid4().hex[:6].upper()}",
            project_id=proj.id,
            title="Integrate Apple Pay & Google Wallet Express Checkout",
            reason="Reduce mobile checkout friction for North American customers.",
            scope_impact="iOS and Android SDK integration",
            cost_impact_inr=250000.0,
            schedule_impact_days=7,
            status="Submitted"
        )
        db_session.add(cr)
        db_session.commit()
        db_session.refresh(cr)

    review_req = ClientChangeRequestReview(
        action="APPROVE",
        client_approver_name="Michael Chang (VP Engineering)",
        review_notes="Approved express checkout scope and commercial delta."
    )
    res = review_client_change_request(cr_id=cr.id, req=review_req, db=db_session)
    assert res["status"] == "success"
    assert res["status_now"] == "Client Approved"

    db_session.refresh(cr)
    assert cr.status == "Client Approved"
    assert cr.decision_date == date.today()


def test_client_invoice_payment_recording(db_session):
    # Find invoice with positive balance
    inv = db_session.query(Invoice).filter(Invoice.outstanding_balance > 0).first()
    if not inv:
        inv = Invoice(
            invoice_number=f"ADT/INV/TEST/{uuid.uuid4().hex[:4].upper()}",
            invoice_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            customer_name="Zenith Global Corp",
            customer_gstin="29AABCZ9988P1Z5",
            taxable_value=100000.0,
            cgst_amount=9000.0,
            sgst_amount=9000.0,
            total_tax=18000.0,
            total_invoice_value=118000.0,
            amount_received=0.0,
            outstanding_balance=118000.0,
            status="Issued / Due"
        )
        db_session.add(inv)
        db_session.commit()
        db_session.refresh(inv)

    prev_balance = inv.outstanding_balance
    pay_amount = min(50000.0, prev_balance)

    pay_req = ClientPaymentRecordRequest(
        payment_reference=f"UTR-{uuid.uuid4().hex[:8].upper()}",
        amount_inr=pay_amount,
        payment_mode="NEFT / RTGS"
    )
    res = record_client_invoice_payment(invoice_id=inv.id, req=pay_req, db=db_session)
    assert res["status"] == "success"
    assert res["outstanding_balance"] == prev_balance - pay_amount


def test_client_invoice_html_document_generation(db_session):
    inv = db_session.query(Invoice).first()
    assert inv is not None

    resp = get_client_invoice_html(invoice_id=inv.id, db=db_session)
    html_content = resp.body.decode()

    assert "TAX INVOICE" in html_content
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html_content
    assert "U85500KA2026OPC222069" in html_content
    assert "29AABCU9603R1ZM" in html_content
    assert "Varadi Vijay" in html_content
    assert "Founder & Sole Director" in html_content
    assert "ICICI Bank Limited" in html_content
    assert "998314" in html_content
    assert "@media print" in html_content


def test_client_statement_of_account_html_generation(db_session):
    resp = get_client_statement_of_account_html(client_name="Zenith Global Corp", db=db_session)
    html_content = resp.body.decode()

    assert "STATEMENT OF ACCOUNT" in html_content
    assert "Zenith Global Corp" in html_content
    assert "Total Billed" in html_content
    assert "Total Remitted" in html_content
    assert "Current Outstanding Due" in html_content
    assert "Varadi Vijay" in html_content
    assert "U85500KA2026OPC222069" in html_content
