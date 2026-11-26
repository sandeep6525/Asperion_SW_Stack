"""
Unit tests for the Document & Letter Generation Engine
"""
import pytest
from app.engines.letter_generator import generate_document_html
from app.engines.ctc_calculator import compute_salary_breakup

def test_generate_offer_letter():
    breakup = compute_salary_breakup(1200000.0)
    doc = generate_document_html("HR-ONB-01", {
        "candidate_name": "Rohan Deshmukh",
        "candidate_address": "Koramangala, Bangalore",
        "designation": "Backend Engineer",
        "department": "Engineering",
        "location": "Bangalore",
        "joining_date": "01 August 2026",
        "annual_ctc": 1200000.0,
        "salary_breakup": breakup
    })
    
    html = doc["html_content"]
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html
    assert "U85500KA2026OPC222069" in html
    assert "Rohan Deshmukh" in html
    assert "Backend Engineer" in html
    assert "Basic Salary" in html

def test_generate_relieving_letter():
    doc = generate_document_html("HR-SEP-15", {
        "employee_name": "Siddharth Verma",
        "emp_code": "ADT-EMP-005",
        "doj": "01 Jan 2025",
        "lwd": "30 Jun 2026",
        "designation": "Product Manager",
        "department": "Product"
    })
    
    html = doc["html_content"]
    assert "RELIEVING LETTER" in html
    assert "Siddharth Verma" in html
    assert "ADT-EMP-005" in html

def test_generate_nda():
    doc = generate_document_html("LEG-NDA-01", {
        "counterparty_name": "Acme Ventures Pvt Ltd",
        "counterparty_address": "MG Road, Bangalore",
        "project_purpose": "API Integration and Data Analytics",
        "effective_date": "15 July 2026"
    })
    
    html = doc["html_content"]
    assert "MUTUAL NON-DISCLOSURE AGREEMENT" in html
    assert "Acme Ventures Pvt Ltd" in html
