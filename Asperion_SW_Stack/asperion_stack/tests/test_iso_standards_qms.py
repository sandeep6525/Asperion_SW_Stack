"""
Asperion Enterprise OS - Comprehensive Test Suite for ISO Standards, QMS, CAPA & Grievance Redressal
Validates:
1. ISO Standards Executive Overview Telemetry
2. 5 Acquired ISO Certifications (ISO 9001, ISO 27001, ISO 42001, ISO 20000-1, ISO 22301)
3. ISO Clause Controls Implementation Worksheets & Filtering
4. Audit Inspection Records & Findings (Major NC, Minor NC, OFI)
5. Corrective and Preventive Action (CAPA) Detailed Worksheets (5 Whys Analysis)
6. Formal Multi-Stakeholder Grievance Redressal & CSAT Rating Flow
"""
import uuid
from datetime import date
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.iso_standards import (
    get_iso_overview,
    list_iso_certifications, register_iso_certification,
    list_iso_clause_controls, create_iso_clause_control,
    list_iso_audits, record_iso_audit,
    list_iso_capas, create_iso_capa,
    list_formal_grievances, lodge_formal_grievance, resolve_formal_grievance
)
from app.schemas.iso_standards import (
    ISOCertificationCreate, ISOClauseControlCreate,
    ISOAuditInspectionCreate, ISOCorrectiveActionWorksheetCreate,
    FormalGrievanceCreate, GrievanceResolutionUpdate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_iso_overview_telemetry(db_session):
    overview = get_iso_overview(db=db_session)
    assert overview is not None
    assert overview["status"] == "CONFORMING"
    assert overview["total_iso_certifications"] >= 5
    assert "ISO-9001:2015" in overview["standards_acquired"]
    assert "ISO/IEC-27001:2022" in overview["standards_acquired"]
    assert "ISO/IEC-42001:2023" in overview["standards_acquired"]
    assert "ISO/IEC-20000-1:2018" in overview["standards_acquired"]
    assert "ISO-22301:2019" in overview["standards_acquired"]
    assert overview["overall_compliance_score_pct"] >= 95.0
    assert overview["total_major_non_conformances"] == 0

def test_iso_certifications_directory(db_session):
    certs = list_iso_certifications(db=db_session)
    assert len(certs) >= 5
    std_codes = [c.standard_code for c in certs]
    assert "ISO-9001:2015" in std_codes
    assert "ISO/IEC-27001:2022" in std_codes
    assert "ISO/IEC-42001:2023" in std_codes
    assert "ISO/IEC-20000-1:2018" in std_codes
    assert "ISO-22301:2019" in std_codes

    qms = next(c for c in certs if c.standard_code == "ISO-9001:2015")
    assert "IAF" in qms.accreditation_body or "BSI" in qms.accreditation_body
    assert qms.status == "Active & Certified"

def test_iso_clause_controls_and_filtering(db_session):
    all_ctrls = list_iso_clause_controls(standard=None, db=db_session)
    assert len(all_ctrls) >= 10

    qms_ctrls = list_iso_clause_controls(standard="ISO-9001:2015", db=db_session)
    assert len(qms_ctrls) >= 4
    for ctrl in qms_ctrls:
        assert ctrl.standard_code == "ISO-9001:2015"
        assert ctrl.compliance_score_pct >= 90.0
        assert ctrl.is_compliant is True

def test_iso_audit_inspections(db_session):
    audits = list_iso_audits(db=db_session)
    assert len(audits) >= 3
    audit_codes = [a.audit_code for a in audits]
    assert "AUD-ISO9001-2026-SURV1" in audit_codes

    surv = next(a for a in audits if a.audit_code == "AUD-ISO9001-2026-SURV1")
    assert surv.major_nc_count == 0
    assert surv.status == "Completed & Closed"

def test_iso_capa_worksheets(db_session):
    capas = list_iso_capas(db=db_session)
    assert len(capas) >= 2
    capa_nums = [cp.capa_number for cp in capas]
    assert "CAPA-QMS-2026-001" in capa_nums

    qms_capa = next(cp for cp in capas if cp.capa_number == "CAPA-QMS-2026-001")
    assert "5 Whys" in qms_capa.root_cause_analysis_method
    assert qms_capa.effectiveness_verified is True
    assert qms_capa.status == "Closed & Verified"

def test_formal_grievance_lifecycle(db_session):
    # 1. List existing grievances
    grievances = list_formal_grievances(status_filter=None, db=db_session)
    assert len(grievances) >= 2
    grv_ids = [g.grievance_id for g in grievances]
    assert "GRV-2026-001" in grv_ids

    # 2. Lodge new grievance
    unique_id = f"GRV-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_grv = FormalGrievanceCreate(
        grievance_id=unique_id,
        stakeholder_type="Client",
        stakeholder_name="Acme Corp Sponsor",
        stakeholder_email="sponsor@acme.com",
        category="Quality of Deliverable",
        severity="High",
        subject="Integration Testing Mock Environment Request",
        description="Request for dedicated sandbox API token with increased rate limits."
    )
    lodged = lodge_formal_grievance(payload=new_grv, db=db_session)
    assert lodged.id is not None
    assert lodged.grievance_id == unique_id
    assert lodged.acknowledgment_sent is True

    # 3. Resolve the grievance
    resolved = resolve_formal_grievance(
        grievance_id=unique_id,
        payload=GrievanceResolutionUpdate(
            investigation_notes="Issued dedicated test sandbox API token with 600 RPM quota.",
            resolution_details="Provided high-throughput test credential; verified by client team.",
            complainant_satisfied=True,
            csat_score=5,
            status="Resolved & Closed"
        ),
        db=db_session
    )
    assert resolved.status == "Resolved & Closed"
    assert resolved.csat_score == 5
    assert resolved.closure_date == date.today()
