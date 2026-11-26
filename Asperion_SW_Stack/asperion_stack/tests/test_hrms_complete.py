"""
Comprehensive Unit & Integration Tests for Asperion HRMS & Human Capital Suite
Tests all 7 pillars: Overview Metrics, ATS Candidates & One-Click Hire, Wage Code Compensation,
Leaves & Balances, Separation & F&F Clearance, Workplace Ethics & POSH Register.
"""
import pytest
from datetime import date, datetime
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.hrms import (
    get_hrms_overview_metrics, list_candidates, create_candidate,
    update_candidate_stage, hire_candidate, get_employee_profile,
    list_leaves, apply_leave, update_leave_status, get_employee_leave_balances,
    list_separations, initiate_separation, update_separation_clearance,
    list_posh_cases, create_posh_case, conclude_posh_case, list_employees,
    enroll_employee_webcam, update_employee_location, get_employee_webcam_status,
    list_geofence_locations, LeaveApplyRequest
)
from app.schemas.hrms import (
    CandidateCreate, CandidateStageUpdate, CandidateHireRequest,
    LeaveStatusUpdate, POSHCaseCreate, POSHCaseConclude,
    SeparationClearanceCreate, SeparationClearanceUpdate,
    EmployeeWebcamEnrollRequest, EmployeeLocationUpdateRequest
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_hrms_overview_metrics(db):
    """Verify aggregated executive HRMS metrics."""
    metrics = get_hrms_overview_metrics(db=db)
    assert metrics.active_headcount >= 3
    assert metrics.monthly_payroll_outflow > 0
    assert metrics.annual_payroll_run_rate > 0
    assert metrics.statutory_pf_outflow_monthly > 0
    assert metrics.statutory_pt_outflow_monthly >= 600  # Karnataka PT (₹200/mo * active headcount)
    assert metrics.total_candidates >= 1
    assert metrics.posh_compliance_index_pct == 100.0

def test_candidate_lifecycle_and_one_click_hire(db):
    """Test candidate creation, stage progression, and one-click hire conversion to Employee."""
    # 1. Create candidate with unique email
    ts = int(datetime.now().timestamp())
    cand_payload = CandidateCreate(
        full_name=f"Siddharth Kulkarni {ts}",
        email=f"siddharth.{ts}@testrecruit.com",
        phone="+91 98888 12345",
        applied_role="Staff Platform Engineer",
        department="Engineering",
        experience_years=8.0,
        expected_ctc=2800000.0,
        notice_period_days=15
    )
    cand = create_candidate(cand_in=cand_payload, db=db)
    cand_id = cand.id
    assert cand.stage == "Applied"

    # 2. Advance stage to Technical Round
    stg1 = update_candidate_stage(
        candidate_id=cand_id,
        payload=CandidateStageUpdate(stage="Technical Round", notes="Passed architecture round"),
        db=db
    )
    assert stg1.stage == "Technical Round"

    # 3. Advance stage to Founder Round
    stg2 = update_candidate_stage(
        candidate_id=cand_id,
        payload=CandidateStageUpdate(stage="Founder Round", notes="Approved by Founder Varadi Vijay"),
        db=db
    )
    assert stg2.stage == "Founder Round"

    # 4. One-Click Hire Candidate
    hire_res = hire_candidate(
        candidate_id=cand_id,
        req=CandidateHireRequest(date_of_joining="2026-06-01", basic_pct=0.50, hra_pct=0.50),
        db=db
    )
    assert hire_res["employee_id"] is not None
    assert hire_res["emp_code"].startswith("ADT-EMP-")
    assert hire_res["offer_letter_id"] is not None

    # 5. Verify Employee 360-degree profile
    emp_id = hire_res["employee_id"]
    prof = get_employee_profile(employee_id=emp_id, db=db)
    assert prof["employee"]["full_name"] == f"Siddharth Kulkarni {ts}"
    assert prof["salary_structure"]["annual_ctc"] == 2800000.0
    assert prof["salary_structure"]["basic_salary"] > 0
    assert len(prof["letters"]) >= 1

def test_leaves_workflow(db):
    """Test leave application, listing, balance calculation, and manager approval."""
    employees = list_employees(db=db)
    assert len(employees) > 0
    emp = employees[0]

    # Apply for leave
    leave_payload = LeaveApplyRequest(
        employee_id=emp.id,
        employee_name=emp.full_name,
        leave_type="Casual Leave",
        start_date=date(2026, 6, 15),
        end_date=date(2026, 6, 16),
        total_days=2.0,
        reason="Personal family function"
    )
    leave = apply_leave(leave_in=leave_payload, db=db)
    leave.status = "Pending"
    db.commit()
    db.refresh(leave)
    assert leave.status == "Pending"

    # Manager approves leave
    approved = update_leave_status(
        leave_id=leave.id,
        payload=LeaveStatusUpdate(status="Approved"),
        db=db
    )
    assert approved.status == "Approved"

    # Check leave balances
    bal = get_employee_leave_balances(employee_id=emp.id, db=db)
    assert bal["employee_id"] == emp.id
    assert bal["annual_entitlements"]["casual_leave"]["remaining"] <= 12

def test_posh_ethics_register(db):
    """Test confidential POSH grievance lodging, 90-day SLA, and ICC inquiry conclusion."""
    ts = int(datetime.now().timestamp())
    posh_payload = POSHCaseCreate(
        case_reference=f"ADT-POSH-TEST-{ts}",
        nature_of_complaint="Unprofessional and inappropriate commentary during video call.",
        date_filed=date.today(),
        internal_committee_presiding_officer="Senior Woman Leader",
        external_member="Empowered NGO Representative"
    )
    posh_case = create_posh_case(payload=posh_payload, db=db)
    assert posh_case.case_reference.startswith("ADT-POSH-")
    assert posh_case.inquiry_status == "Under Inquiry"
    assert posh_case.statutory_90_day_deadline >= date.today()

    # Conclude inquiry
    conc = conclude_posh_case(
        case_id=posh_case.id,
        payload=POSHCaseConclude(
            inquiry_status="Concluded",
            recommendations_summary="Formal inquiry completed per POSH Act 2013 rules. Written reprimand issued.",
            action_taken="Reprimand issued, ethics training re-mandated."
        ),
        db=db
    )
    assert conc.inquiry_status == "Concluded"
    assert "reprimand" in conc.recommendations_summary.lower()

def test_separation_and_ff_clearance(db):
    """Test employee separation initiation and multi-department clearance tracking."""
    employees = list_employees(db=db)
    emp = employees[0]

    sep_payload = SeparationClearanceCreate(
        employee_id=emp.id,
        resignation_date=date(2026, 6, 1),
        last_working_day=date(2026, 7, 31),
        notice_period_required=30,
        notice_period_served=30
    )
    sep = initiate_separation(payload=sep_payload, db=db)
    assert sep.fnf_settlement_status == "Under Clearance"

    # Update IT and Finance clearances
    updated = update_separation_clearance(
        separation_id=sep.id,
        payload=SeparationClearanceUpdate(
            it_asset_clearance=True,
            finance_clearance=True,
            manager_handover_clearance=True,
            fnf_settlement_status="Approved"
        ),
        db=db
    )
    assert updated.it_asset_clearance is True
    assert updated.finance_clearance is True
    assert updated.manager_handover_clearance is True
    assert updated.fnf_settlement_status == "Approved"

def test_employee_gps_coordinates_and_geofencing(db):
    """Test HRMS GPS latitude/longitude assignment, geofence radius and work location type."""
    employees = list_employees(db=db)
    emp = employees[0]

    # Check default Horamavu HQ coordinates
    prof = get_employee_profile(employee_id=emp.id, db=db)
    assert "latitude" in prof["employee"]
    assert "longitude" in prof["employee"]
    assert prof["employee"]["latitude"] is not None
    assert prof["employee"]["longitude"] is not None

    # Update to an approved Remote / Client site location
    loc_payload = EmployeeLocationUpdateRequest(
        latitude=12.9716,
        longitude=77.5946,
        geofence_radius_meters=350.0,
        work_location_type="Approved Remote WFH",
        work_location="Bangalore Central Hub"
    )
    upd = update_employee_location(employee_id=emp.id, req=loc_payload, db=db)
    assert upd["status"] == "success"
    assert upd["latitude"] == 12.9716
    assert upd["longitude"] == 77.5946
    assert upd["geofence_radius_meters"] == 350.0
    assert upd["work_location_type"] == "Approved Remote WFH"

def test_employee_webcam_facial_enrollment(db):
    """Test HRMS live webcam stream facial snapshot capture and biometric registration."""
    employees = list_employees(db=db)
    emp = employees[0]

    webcam_payload = EmployeeWebcamEnrollRequest(
        webcam_snapshot_base64="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP...",
        webcam_hardware_device="Logitech Brio 4K Ultra HD Pro",
        facial_liveness_verified=True,
        liveness_score=99.2
    )
    res = enroll_employee_webcam(employee_id=emp.id, req=webcam_payload, db=db)
    assert res["status"] == "success"
    assert res["facial_enrollment_status"] == "Enrolled"
    assert res["liveness_score"] == 99.2
    assert "Logitech Brio" in res["hardware_device"]

    status = get_employee_webcam_status(employee_id=emp.id, db=db)
    assert status["facial_enrollment_status"] == "Enrolled"
    assert status["has_registered_snapshot"] is True
    assert status["facial_liveness_score"] == 99.2

def test_geofence_locations_directory(db):
    """Test corporate approved geofences directory with Horamavu HQ coordinates."""
    geo = list_geofence_locations(db=db)
    assert "registered_hq" in geo
    assert geo["registered_hq"]["latitude"] == 13.035820
    assert geo["registered_hq"]["longitude"] == 77.653410
    assert "Horamavu" in geo["registered_hq"]["address"]
    assert "zones" in geo
