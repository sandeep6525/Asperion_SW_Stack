"""
Unit & Integration Tests for Attendance-Synced Salary Statements,
Statutory Professional Tax (Karnataka), Bank Batch Generation, and Alerts.
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.hrms import Employee
from app.engines.salary_statement_engine import (
    calculate_karnataka_pt, compute_employee_attendance_days,
    generate_attendance_synced_salary_statement, get_employee_salary_slip_html
)
from app.api.hrms import api_run_payroll, api_get_payslip_html, RunPayrollRequest

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    yield session
    session.close()

def test_karnataka_pt_calculation():
    # Below Rs. 15,000 gross
    assert calculate_karnataka_pt(12000.0) == 0.0
    # Above or equal Rs. 15,000 gross
    assert calculate_karnataka_pt(15000.0) == 200.0
    assert calculate_karnataka_pt(85000.0) == 200.0

def test_compute_employee_attendance_days(db):
    emp = db.query(Employee).first()
    assert emp is not None
    metrics = compute_employee_attendance_days(
        db=db,
        employee_id=emp.id,
        cycle_year=2026,
        cycle_month=6,
        days_in_month=30
    )
    assert metrics["days_in_month"] == 30.0
    assert metrics["payable_days"] >= 0.0
    assert metrics["lop_days"] >= 0.0

def test_attendance_synced_salary_statement_generation(db):
    res = generate_attendance_synced_salary_statement(
        db=db,
        payroll_cycle="JUN-2026",
        days_in_month=30,
        disburse_bank=False
    )
    assert res["status"] == "success"
    assert res["active_headcount"] >= 1
    assert res["total_gross_inr"] > 0
    assert res["statutory_compliance_summary"]["total_karnataka_pt_inr"] >= 200.0
    assert res["total_net_disbursement_inr"] > 0
    assert "bank_neft_batch_csv" in res
    assert "SALARY" in res["bank_neft_batch_csv"]

def test_bank_disbursement_and_utr(db):
    res = generate_attendance_synced_salary_statement(
        db=db,
        payroll_cycle="JUN-2026",
        days_in_month=30,
        disburse_bank=True
    )
    assert res["disbursement_status"] == "Disbursed via Bank Batch"
    assert len(res["statements"]) >= 1
    assert "UTR-ICICI" in res["statements"][0]["bank_utr"]

def test_employee_salary_slip_html(db):
    emp = db.query(Employee).first()
    html = get_employee_salary_slip_html(db, emp.id, "JUN-2026")
    assert "SALARY STATEMENT" in html
    assert emp.full_name in html
    assert "Karnataka Professional Tax" in html
    assert "Bank UTR" in html

def test_api_run_payroll_endpoint(db):
    req = RunPayrollRequest(payroll_cycle="JUL-2026", days_in_month=31, disburse_bank=False)
    res = api_run_payroll(req, db=db)
    assert res["status"] == "success"
    assert res["active_headcount"] >= 1
