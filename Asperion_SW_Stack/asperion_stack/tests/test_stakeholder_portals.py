"""
Unit & Integration Tests for Dedicated Stakeholder Portals (Employee, Client, Vendor)
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.portals import (
    get_employee_portal_data, get_client_portal_data, get_vendor_portal_data,
    portal_quick_clock_in, portal_apply_leave, portal_raise_ticket, get_employee_id_card_html,
    PortalQuickClockInRequest, PortalLeaveApplyRequest, PortalRaiseTicketRequest
)
from datetime import date, timedelta
from app.api.auth import login, LoginRequest

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    yield session
    session.close()

def test_employee_portal_data(db):
    res = get_employee_portal_data(emp_code="ADT-EMP-001", db=db)
    assert "profile" in res
    assert res["profile"]["emp_code"] == "ADT-EMP-001"
    assert "salary_overview" in res
    assert res["salary_overview"]["annual_ctc"] > 0
    assert "attendance_stats" in res
    assert "payslips" in res

def test_client_portal_data(db):
    res = get_client_portal_data(client_name="Zenith Global Corp", db=db)
    assert res["relationship_tier"] == "Enterprise Retainer Partner"
    assert "active_projects" in res
    assert "billing_invoices" in res
    assert "sla_tickets" in res

def test_vendor_portal_data(db):
    res = get_vendor_portal_data(vendor_name="Nexus Micro Systems", db=db)
    assert "vendor_name" in res
    assert "purchase_orders" in res
    assert "submitted_bills" in res

def test_stakeholder_login_personas():
    # Employee Login
    emp_log = login(LoginRequest(email="employee@asperion.in", password="Password123!"))
    assert emp_log.role == "EMPLOYEE"
    assert "portal-employee" in emp_log.authorized_modules

    # Client Login
    clt_log = login(LoginRequest(email="client@zenith.com", password="Password123!"))
    assert clt_log.role == "CLIENT"
    assert "portal-client" in clt_log.authorized_modules

    # Vendor Login
    vnd_log = login(LoginRequest(email="vendor@nexuscables.in", password="Password123!"))
    assert vnd_log.role == "VENDOR"
    assert "portal-vendor" in vnd_log.authorized_modules

def test_employee_portal_roster_and_breakup(db):
    # Test Arjun Sharma
    res1 = get_employee_portal_data(emp_code="ADT-EMP-001", db=db)
    assert res1["corporate_entity"]["cin"] == "U85500KA2026OPC222069"
    assert res1["corporate_entity"]["director"] == "Varadi Vijay"
    assert len(res1["employees_roster"]) >= 4
    assert "salary_breakup" in res1
    assert res1["salary_breakup"]["annual_ctc"] > 0
    assert "leave_ledger" in res1
    assert len(res1["leave_ledger"]["statutory_holidays_2026"]) == 10
    assert "learning_and_probation" in res1
    assert "it_assets_and_security" in res1
    assert "internal_tickets" in res1
    assert "handbooks_and_playbooks" in res1

    # Test Priya Nair
    res2 = get_employee_portal_data(emp_code="ADT-EMP-002", db=db)
    assert res2["profile"]["emp_code"] == "ADT-EMP-002"
    assert res2["profile"]["name"] == "Priya Nair"

def test_employee_portal_quick_clock_in_geofence(db):
    # Within Horamavu HQ Geofence (13.035820, 77.653410)
    req_hq = PortalQuickClockInRequest(
        emp_code="ADT-EMP-001",
        latitude=13.035820,
        longitude=77.653410
    )
    punch_hq = portal_quick_clock_in(req=req_hq, db=db)
    assert punch_hq["status"] == "success"
    assert punch_hq["geofence_verified"] is True
    assert punch_hq["distance_m"] <= 10.0

    # Outside Geofence (e.g. 10km away)
    req_remote = PortalQuickClockInRequest(
        emp_code="ADT-EMP-001",
        latitude=12.9716,
        longitude=77.5946
    )
    punch_remote = portal_quick_clock_in(req=req_remote, db=db)
    assert punch_remote["status"] == "success"
    assert punch_remote["geofence_verified"] is False
    assert punch_remote["distance_m"] > 200.0

def test_employee_portal_apply_leave(db):
    req_leave = PortalLeaveApplyRequest(
        emp_code="ADT-EMP-001",
        leave_type="Casual Leave",
        start_date=date.today() + timedelta(days=5),
        end_date=date.today() + timedelta(days=6),
        total_days=2.0,
        reason="Family personal engagement"
    )
    leave_res = portal_apply_leave(req=req_leave, db=db)
    assert leave_res["status"] == "success"
    assert leave_res["leave_record"]["total_days"] == 2.0
    assert leave_res["leave_record"]["leave_type"] == "Casual Leave"

def test_employee_portal_raise_ticket(db):
    req_tkt = PortalRaiseTicketRequest(
        emp_code="ADT-EMP-001",
        department="IT_INFRASTRUCTURE",
        category="Hardware & Peripheral Support",
        priority="P2-High",
        subject="Secondary 4K Monitor DisplayPort adapter required",
        description="Need an active USB-C to DP 1.4 adapter for dual display workstation setup."
    )
    tkt_res = portal_raise_ticket(req=req_tkt, db=db)
    assert tkt_res["status"] == "success"
    assert tkt_res["ticket"]["ticket_number"].startswith("IT-TKT-")
    assert tkt_res["ticket"]["sla_deadline_hours"] == 24.0

def test_employee_id_card_html(db):
    html_resp = get_employee_id_card_html(emp_code="ADT-EMP-001", db=db)
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html_resp.body.decode("utf-8")
    assert "U85500KA2026OPC222069" in html_resp.body.decode("utf-8")
    assert "Varadi Vijay" in html_resp.body.decode("utf-8")
    assert "ADT-EMP-001" in html_resp.body.decode("utf-8")
    assert "Horamavu" in html_resp.body.decode("utf-8")
