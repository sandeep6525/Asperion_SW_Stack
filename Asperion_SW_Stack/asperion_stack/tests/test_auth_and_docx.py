"""
Unit & Integration Tests for Authentication, RBAC, Audit Logging, and DOCX Export Engine
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.auth import login, get_current_user, list_personas, LoginRequest
from app.api.governance import record_audit_log, list_audit_logs, AuditLogCreate
from app.api.hrms import download_letter_docx, api_generate_letter, GenerateLetterRequest
from app.api.cybersecurity import download_incident_report_docx
from app.api.vault import list_vault_categories, search_vault_documents, get_vault_statistics
from app.engines.docx_exporter import create_corporate_letter_docx, create_certin_report_docx, generate_authentic_hr_letter_docx
from fastapi import HTTPException
from docx import Document

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()

def test_auth_login_director():
    req = LoginRequest(email="director@asperion.in", password="Password123!")
    res = login(req)
    assert res.role == "DIRECTOR"
    assert "all" in res.authorized_modules
    assert res.access_token.startswith("asp_sec_")

def test_auth_login_personas_and_invalid():
    # Valid HR login
    res_hr = login(LoginRequest(email="hr@asperion.in", password="Password123!"))
    assert res_hr.role == "HR_HEAD"
    assert "hrms" in res_hr.authorized_modules

    # Invalid password
    with pytest.raises(HTTPException) as exc:
        login(LoginRequest(email="director@asperion.in", password="WrongPassword!"))
    assert exc.value.status_code == 401

    # List personas
    personas = list_personas()
    assert len(personas) >= 5
    roles = [p.role for p in personas]
    assert "DIRECTOR" in roles
    assert "FINANCE_HEAD" in roles
    assert "SOC_LEAD" in roles

def test_audit_logs_system(db_session):
    # Record a new audit log
    entry = AuditLogCreate(
        event_type="TEST_EXECUTION",
        severity="INFO",
        actor="Pytest Suite",
        module="FinOps",
        description="Automated reconciliation test check.",
        ip_address="127.0.0.1"
    )
    saved = record_audit_log(entry, db=db_session)
    assert saved.id is not None
    assert saved.event_type == "TEST_EXECUTION"

    # Query audit logs
    logs = list_audit_logs(module="FinOps", db=db_session)
    assert len(logs) >= 1
    assert any(l.event_type == "TEST_EXECUTION" for l in logs)

def test_docx_letter_generation_in_memory():
    sample_lines = [
        "### Offer Details",
        "We are pleased to extend this offer for the position of Senior DevOps Engineer.",
        "- Core working hours: 09:30 AM to 06:30 PM",
        "- Location: Bangalore Head Office"
    ]
    breakup = {
        "annual_ctc": 1200000.0,
        "monthly_ctc": 100000.0,
        "monthly_basic": 40000.0,
        "annual_basic": 480000.0,
        "monthly_hra": 16000.0,
        "annual_hra": 192000.0,
        "monthly_special_allowance": 37190.0,
        "annual_special_allowance": 446280.0,
        "monthly_gross": 93190.0,
        "annual_gross": 1118280.0,
        "monthly_pf_employer": 1800.0,
        "annual_pf_employer": 21600.0,
        "monthly_gratuity": 1923.08,
        "annual_gratuity": 23076.92,
        "monthly_pf_employee": 1800.0,
        "annual_pf_employee": 21600.0,
        "monthly_pt": 200.0,
        "annual_pt": 2400.0,
        "monthly_net_take_home": 91190.0,
        "annual_net_take_home": 1094280.0
    }
    
    stream = create_corporate_letter_docx(
        letter_title="Formal Offer of Employment",
        recipient_name="Ramesh Rao",
        body_text_lines=sample_lines,
        salary_breakup=breakup
    )
    
    # Read generated docx to verify structure
    stream.seek(0)
    doc = Document(stream)
    assert len(doc.tables) >= 2  # Header table + Annexure table
    full_text = " ".join([p.text for p in doc.paragraphs])
    assert "FORMAL OFFER OF EMPLOYMENT" in full_text
    assert "Varadi Vijay" in full_text

def test_docx_certin_report_in_memory():
    inc_data = {
        "incident_id": "ADT-SEC-2026-999",
        "title": "Phishing Detection on Dev Environment",
        "severity": "P3-Medium",
        "incident_type": "Phishing Attempt",
        "cert_in_deadline": "Within 6 hours",
        "affected_systems": "Mail Server / Okta",
        "status": "Contained"
    }
    stream = create_certin_report_docx(inc_data)
    stream.seek(0)
    doc = Document(stream)
    assert len(doc.tables) >= 1
    full_text = " ".join([p.text for p in doc.paragraphs])
    assert "CERT-In" in full_text
    assert "MANDATORY CYBER SECURITY INCIDENT" in full_text

def test_hrms_docx_endpoint_download(db_session):
    # Generate a letter first
    gen_req = GenerateLetterRequest(
        letter_code="HR-ADM-01",
        recipient_name="Kavitha Reddy",
        recipient_email="kavitha@asperion.in",
        designation="Product Manager",
        department="Product"
    )
    res = api_generate_letter(gen_req, db=db_session)
    letter_id = res["letter_id"]

    # Call docx download endpoint
    resp = download_letter_docx(letter_id, db=db_session)
    assert resp.media_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert "attachment; filename=HR-ADM-01_Kavitha_Reddy.docx" in resp.headers["Content-Disposition"]

def test_secops_docx_endpoint_download(db_session):
    # Call docx incident download
    resp = download_incident_report_docx("ADT-SEC-2026-001", db=db_session)
    assert resp.media_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert "attachment; filename=CERT_In_Report_ADT-SEC-2026-001.docx" in resp.headers["Content-Disposition"]

def test_vault_api_categories_and_documents():
    categories = list_vault_categories()
    assert len(categories) == 10
    cat_ids = [c.category_id for c in categories]
    assert "company_os" in cat_ids
    assert "hr_letters" in cat_ids
    assert "founder_strategy" in cat_ids

    # Search documents
    docs = search_vault_documents(category="hr_letters", file_type="docx")
    assert len(docs) >= 60
    assert any("HR-ONB-01" in d.filename for d in docs)

    stats = get_vault_statistics()
    assert stats["total_documents"] >= 200

def test_authentic_hr_letter_docx_substitution():
    context = {
        "recipient_name": "Vikram Sethi",
        "designation": "Principal AI Architect",
        "issue_date": "15 July 2026",
        "location": "Bangalore North Office",
        "candidate_address": "Indiranagar, Bangalore"
    }
    salary_breakup = {
        "annual_ctc": 2400000.0,
        "monthly_ctc": 200000.0,
        "monthly_basic": 100000.0,
        "annual_basic": 1200000.0,
        "monthly_hra": 40000.0,
        "annual_hra": 480000.0,
        "monthly_special_allowance": 51590.0,
        "annual_special_allowance": 619080.0,
        "monthly_gross": 191590.0,
        "annual_gross": 2299080.0,
        "monthly_pf_employer": 1800.0,
        "annual_pf_employer": 21600.0,
        "monthly_gratuity": 4807.69,
        "annual_gratuity": 57692.31,
        "monthly_pf_employee": 1800.0,
        "annual_pf_employee": 21600.0,
        "monthly_pt": 200.0,
        "annual_pt": 2400.0,
        "monthly_net_take_home": 189590.0,
        "annual_net_take_home": 2275080.0
    }
    stream = generate_authentic_hr_letter_docx(
        letter_code="HR-ONB-01",
        letter_title="Formal Offer of Employment",
        recipient_name="Vikram Sethi",
        context=context,
        salary_breakup=salary_breakup
    )
    assert stream is not None
    doc = Document(stream)
    full_text = " ".join([p.text for p in doc.paragraphs])
    assert "Vikram Sethi" in full_text
    assert "Principal AI Architect" in full_text
    assert len(doc.tables) >= 2  # Includes populated compensation annexure

