"""
Comprehensive API and ORM Endpoint Integration Tests
Directly tests router business logic, database transactions, engines, and data schemas.
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.dashboard import get_dashboard_overview
from app.api.governance import get_entity_profile, list_board_resolutions, list_compliance_items
from app.api.finance import get_chart_of_accounts, list_invoices, list_ap_bills, get_detailed_13_week_forecast
from app.api.hrms import (
    list_employees, api_calculate_ctc, api_generate_letter,
    get_all_letter_templates, api_run_payroll, RunPayrollRequest
)
from app.api.pmo import list_projects, list_raid_items, list_wbs_tasks, update_task_status, TaskStatusUpdate
from app.api.procurement import list_vendors, list_scorecards, list_rfp_comparisons
from app.api.infrastructure import list_it_assets, list_cloud_accounts, list_certificates_secrets
from app.api.cybersecurity import list_incidents, preview_incident_triage, get_cert_in_filing_report
from app.schemas.hrms import CTCCalculatorRequest, GenerateLetterRequest
from app.schemas.cybersecurity import IncidentCreate

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_dashboard_overview(db_session):
    res = get_dashboard_overview(db=db_session)
    assert res["status"] == "success"
    assert res["cin"] == "U85500KA2026OPC222069"
    assert "kpis" in res
    assert res["kpis"]["financials"]["total_invoiced_inr"] > 0
    assert res["kpis"]["people_hrms"]["active_headcount"] >= 1

def test_governance_entity(db_session):
    entity = get_entity_profile(db=db_session)
    assert entity.cin == "U85500KA2026OPC222069"
    assert "Horamavu" in entity.registered_office
    
    resolutions = list_board_resolutions(db=db_session)
    assert len(resolutions) >= 2
    
    compliance = list_compliance_items(db=db_session)
    assert len(compliance) >= 5

def test_finance_endpoints(db_session):
    coa = get_chart_of_accounts(db=db_session)
    assert len(coa) >= 12
    
    invoices = list_invoices(db=db_session)
    assert len(invoices) >= 1
    assert any(inv.total_invoice_value == 708000.0 for inv in invoices)
    
    bills = list_ap_bills(db=db_session)
    assert len(bills) >= 1
    assert bills[0].three_way_match_status == "Matched"

def test_13_week_cashflow_engine(db_session):
    cf = get_detailed_13_week_forecast(db=db_session)
    assert "weeks" in cf
    assert len(cf["weeks"]) == 13
    assert cf["starting_cash_inr"] > 0
    assert cf["estimated_runway_months"] > 0

def test_hrms_letter_templates_catalogue():
    templates = get_all_letter_templates()
    assert len(templates) >= 50
    codes = [t["code"] for t in templates]
    assert "HR-REC-01" in codes
    assert "HR-ONB-01" in codes
    assert "HR-ADM-01" in codes
    assert "HR-ER-02" in codes
    assert "HR-SEP-15" in codes
    assert "LEG-NDA-01" in codes

def test_hrms_automated_payroll_run(db_session):
    req = RunPayrollRequest(payroll_cycle="JUN-2026", days_in_month=30)
    res = api_run_payroll(req, db=db_session)
    assert res["payroll_cycle"] == "JUN-2026"
    assert res["employees_count"] >= 4
    assert res["total_gross_inr"] > 0
    assert res["total_net_disbursement_inr"] > 0
    assert "SALARY" in res["bank_neft_batch_csv"]

def test_hrms_endpoints(db_session):
    employees = list_employees(db=db_session)
    assert len(employees) >= 4
    
    req = CTCCalculatorRequest(annual_ctc=1200000.0)
    ctc_res = api_calculate_ctc(req)
    assert ctc_res["reconciliation"]["is_balanced"] is True
    
    let_req = GenerateLetterRequest(
        letter_code="HR-ONB-01",
        recipient_name="Aditi Rao",
        designation="Lead Architect",
        annual_ctc=1600000.0
    )
    let_res = api_generate_letter(let_req, db=db_session)
    assert let_res["letter_id"] is not None
    assert "Aditi Rao" in let_res["recipient"]

def test_pmo_kanban_and_procurement(db_session):
    projects = list_projects(db=db_session)
    assert len(projects) >= 1
    
    tasks = list_wbs_tasks(db=db_session)
    assert len(tasks) >= 1
    
    # Test task status change
    first_task = tasks[0]
    updated = update_task_status(first_task.id, TaskStatusUpdate(status="Done"), db=db_session)
    assert updated.status == "Done"
    
    vendors = list_vendors(db=db_session)
    assert len(vendors) >= 1
    
    rfps = list_rfp_comparisons(db=db_session)
    assert len(rfps) >= 1
    assert rfps[0].rfp_reference == "ADT-RFP-2026-001"

def test_secops_and_infrastructure(db_session):
    assets = list_it_assets(db=db_session)
    assert len(assets) >= 1
    assert assets[0].disk_encryption_enabled is True
    
    certs = list_certificates_secrets(db=db_session)
    assert len(certs) >= 1
    
    incidents = list_incidents(db=db_session)
    assert len(incidents) >= 1
    assert incidents[0].cert_in_reporting_required is True
    
    # Test CERT-In filing form generation
    cert_html = get_cert_in_filing_report(incidents[0].incident_id, db=db_session)
    assert "CYBERSECURITY INCIDENT REPORTING FORM" in cert_html
    assert "ASPERION DIGITAL TECHNOLOGIES" in cert_html
