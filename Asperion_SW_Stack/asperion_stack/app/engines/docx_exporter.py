"""
Asperion Enterprise OS - DOCX Document Export Engine
Generates official Microsoft Word (.docx) documents with corporate letterhead,
metadata, formatted tables, and authorized signature blocks.
"""
import io
import os
import re
from pathlib import Path
from typing import Optional
from datetime import date, datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from app.config import settings

VAULT_HR_DIR = Path(__file__).resolve().parent.parent / "static" / "templates_vault" / "hr_letters"

def set_cell_background(cell, fill_hex: str):
    """Sets background color of a table cell in hex without '#'."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def find_authentic_hr_template(letter_code: str) -> Optional[Path]:
    """Finds matching authentic .docx template from the extracted pack."""
    if not VAULT_HR_DIR.exists():
        return None
    for root, dirs, files in os.walk(VAULT_HR_DIR):
        for f in files:
            if f.startswith(f"{letter_code}_") and f.endswith(".docx"):
                return Path(root) / f
    return None

def generate_authentic_hr_letter_docx(
    letter_code: str,
    letter_title: str,
    recipient_name: str,
    context: dict,
    salary_breakup: dict = None
) -> io.BytesIO:
    """
    Populates an authentic Asperion master Word template or falls back to standard letterhead.
    """
    template_path = find_authentic_hr_template(letter_code)
    
    if not template_path:
        # Fall back to custom corporate letterhead generator
        clean_lines = [
            f"Subject: {letter_title}",
            f"Issued to: {recipient_name}",
            f"Designation: {context.get('designation', 'Professional')}",
            context.get("body_summary", "Terms and conditions as approved under Asperion Digital Technologies policies.")
        ]
        return create_corporate_letter_docx(
            letter_title=letter_title,
            recipient_name=recipient_name,
            body_text_lines=clean_lines,
            salary_breakup=salary_breakup,
            issue_date=context.get("issue_date")
        )

    doc = Document(str(template_path))
    
    first_name = recipient_name.split()[0] if recipient_name else "Candidate"
    issue_dt = context.get("issue_date", date.today().strftime("%d %B %Y"))
    
    replacements = {
        "[[REFERENCE_NUMBER]]": f"ADT/HR/{date.today().year}/{letter_code}",
        "[[DATE]]": issue_dt,
        "[[FULL_NAME]]": recipient_name,
        "[[SALUTATION / FIRST_NAME]]": first_name,
        "[[FIRST_NAME]]": first_name,
        "[[ROLE_TITLE]]": context.get("designation", "Software Engineer"),
        "[[ROLE_TITLE / GRADE]]": context.get("designation", "Software Engineer"),
        "[[MANAGER_TITLE]]": context.get("manager_title", f"{settings.FOUNDER_DIRECTOR}"),
        "[[ADDRESS_LINE_1]]": context.get("candidate_address", "Bangalore, Karnataka"),
        "[[CITY, STATE, PIN]]": "Bangalore - 560043, Karnataka",
        "[[EMAIL]]": context.get("recipient_email", "employee@asperion.in"),
        "[[MOBILE]]": context.get("mobile", "+91 98765 43210"),
        "[[LOCATION_AND_MOBILITY_TERM]]": context.get("location", "Bangalore Head Office (Hybrid)"),
        "[[DURATION_AND_EXTENSION_RULE]]": "3 Months (Extendable upon performance review)",
        "[[FULL-TIME / PART-TIME / FIXED-TERM]]": "Full-Time Employment",
        "[[EMPLOYER_LEGAL_NAME]]": settings.COMPANY_NAME,
        "[[REGISTERED_OFFICE]]": settings.REGISTERED_OFFICE
    }

    # Replace placeholders in paragraphs
    for p in doc.paragraphs:
        for placeholder, val in replacements.items():
            if placeholder in p.text:
                p.text = p.text.replace(placeholder, val)

    # Replace placeholders in existing tables
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for placeholder, val in replacements.items():
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, val)

    # If salary breakup is provided, append the exact Annexure A table
    if salary_breakup and "annual_ctc" in salary_breakup:
        p_annex = doc.add_paragraph()
        p_annex.paragraph_format.space_before = Pt(18)
        p_annex.paragraph_format.space_after = Pt(6)
        r_ann = p_annex.add_run("ANNEXURE A: STATUTORY COMPENSATION STRUCTURE (INR)")
        r_ann.bold = True
        r_ann.font.size = Pt(11)
        r_ann.font.color.rgb = RGBColor(30, 58, 138)

        table = doc.add_table(rows=1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Salary Component", "Monthly (₹)", "Annual (₹)"]
        hdr_cells = table.rows[0].cells
        for idx, text in enumerate(headers):
            hdr_cells[idx].text = text
            set_cell_background(hdr_cells[idx], "1E3A8A")
            p = hdr_cells[idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(9)

        rows_data = [
            ("Basic Salary (50%)", salary_breakup.get("monthly_basic", 0), salary_breakup.get("annual_basic", 0)),
            ("House Rent Allowance (HRA 40%)", salary_breakup.get("monthly_hra", 0), salary_breakup.get("annual_hra", 0)),
            ("Special Allowance", salary_breakup.get("monthly_special_allowance", 0), salary_breakup.get("annual_special_allowance", 0)),
            ("Gross Salary (A)", salary_breakup.get("monthly_gross", 0), salary_breakup.get("annual_gross", 0)),
            ("Employer PF Contribution (EPFO Capped)", salary_breakup.get("monthly_pf_employer", 0), salary_breakup.get("annual_pf_employer", 0)),
            ("Statutory Gratuity Provision (4.81%)", salary_breakup.get("monthly_gratuity", 0), salary_breakup.get("annual_gratuity", 0)),
            ("Total Cost to Company (CTC)", salary_breakup.get("monthly_ctc", 0), salary_breakup.get("annual_ctc", 0)),
            ("Employee PF Deduction", salary_breakup.get("monthly_pf_employee", 0), salary_breakup.get("annual_pf_employee", 0)),
            ("Karnataka Professional Tax (PT)", salary_breakup.get("monthly_pt", 0), salary_breakup.get("annual_pt", 0)),
            ("Net Take-Home Salary (Estimate)", salary_breakup.get("monthly_net_take_home", 0), salary_breakup.get("annual_net_take_home", 0)),
        ]

        for comp, m_val, a_val in rows_data:
            row_cells = table.add_row().cells
            row_cells[0].text = comp
            row_cells[1].text = f"₹{m_val:,.2f}"
            row_cells[2].text = f"₹{a_val:,.2f}"
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            is_highlight = "CTC" in comp or "Take-Home" in comp or "Gross" in comp
            for cell in row_cells:
                p = cell.paragraphs[0]
                for r in p.runs:
                    r.font.size = Pt(8.5)
                    if is_highlight:
                        r.bold = True
                        r.font.color.rgb = RGBColor(15, 23, 42)
                if is_highlight:
                    set_cell_background(cell, "F1F5F9")

    # Append Authorized Signatory block if not present
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(25)
    r_sig1 = p_sig.add_run(f"\nFor {settings.COMPANY_NAME}\n\n\n")
    r_sig2 = p_sig.add_run(f"{settings.FOUNDER_DIRECTOR}\n")
    r_sig2.bold = True
    r_sig3 = p_sig.add_run("Authorized Signatory & Sole Director")
    r_sig3.font.size = Pt(9)
    r_sig3.font.color.rgb = RGBColor(100, 116, 139)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream


def create_corporate_letter_docx(
    letter_title: str,
    recipient_name: str,
    body_text_lines: list,
    salary_breakup: dict = None,
    category: str = "Corporate Letter",
    issue_date: str = None
) -> io.BytesIO:
    """
    Creates an official corporate letter .docx document matching the Asperion letterhead.
    Returns in-memory BytesIO stream.
    """
    doc = Document()
    
    # Page Margins: 1 inch all around
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        
    # --- Corporate Header ---
    logo_path = Path(__file__).resolve().parent.parent / "static" / "img" / "logo.png"
    has_logo = logo_path.exists()
    
    if has_logo:
        header_table = doc.add_table(rows=1, cols=3)
        header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        header_table.autofit = False
        col_widths = [Inches(1.0), Inches(4.1), Inches(1.8)]
        for i, w in enumerate(col_widths):
            header_table.columns[i].width = w
            header_table.cell(0, i).width = w

        c_logo = header_table.cell(0, 0)
        p_logo = c_logo.paragraphs[0]
        p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_logo.add_run().add_picture(str(logo_path), width=Inches(0.85))

        c0 = header_table.cell(0, 1)
        c1 = header_table.cell(0, 2)
    else:
        header_table = doc.add_table(rows=1, cols=2)
        header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        header_table.autofit = False
        col_widths = [Inches(4.8), Inches(1.9)]
        for i, w in enumerate(col_widths):
            header_table.columns[i].width = w
            header_table.cell(0, i).width = w
        c0 = header_table.cell(0, 0)
        c1 = header_table.cell(0, 1)

    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r_title = p0.add_run(settings.COMPANY_NAME + "\n")
    r_title.bold = True
    r_title.font.size = Pt(12)
    r_title.font.color.rgb = RGBColor(30, 58, 138) # Deep navy #1e3a8a
    
    r_info = p0.add_run(
        f"CIN: {settings.CIN} | PAN: {settings.PAN} | GSTIN: {settings.GSTIN}\n"
        f"Registered Office: {settings.REGISTERED_OFFICE}"
    )
    r_info.font.size = Pt(7.5)
    r_info.font.color.rgb = RGBColor(100, 116, 139) # Slate
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tag = p1.add_run("OFFICIAL CORRESPONDENCE\n")
    r_tag.bold = True
    r_tag.font.size = Pt(8.5)
    r_tag.font.color.rgb = RGBColor(29, 78, 216)
    
    dt_str = issue_date or date.today().strftime("%B %d, %Y")
    r_dt = p1.add_run(f"Date: {dt_str}")
    r_dt.font.size = Pt(8)
    r_dt.font.color.rgb = RGBColor(71, 85, 105)

    # Dividing line / spacing
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(14)
    run_line = p_div.add_run("―" * 58)
    run_line.font.color.rgb = RGBColor(203, 213, 225)
    run_line.font.size = Pt(10)

    # --- Document Title ---
    p_doc_title = doc.add_paragraph()
    p_doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc_title.paragraph_format.space_after = Pt(14)
    r_main_t = p_doc_title.add_run(letter_title.upper())
    r_main_t.bold = True
    r_main_t.font.size = Pt(13)
    r_main_t.font.color.rgb = RGBColor(15, 23, 42)

    # --- Body Content ---
    for item in body_text_lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(7)
        p.paragraph_format.line_spacing = 1.15
        
        # Check if line is a subheader
        if item.startswith("### ") or item.startswith("Subject:"):
            run = p.add_run(item.replace("### ", ""))
            run.bold = True
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(30, 41, 59)
        elif item.startswith("- ") or item.startswith("* "):
            p.paragraph_format.left_indent = Inches(0.25)
            run = p.add_run("•  " + item[2:])
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(51, 65, 85)
        else:
            run = p.add_run(item)
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(51, 65, 85)

    # --- Optional Salary Annexure Table ---
    if salary_breakup and "annual_ctc" in salary_breakup:
        p_annex = doc.add_paragraph()
        p_annex.paragraph_format.space_before = Pt(14)
        p_annex.paragraph_format.space_after = Pt(6)
        r_ann = p_annex.add_run("ANNEXURE A: COMPENSATION STRUCTURE (INR)")
        r_ann.bold = True
        r_ann.font.size = Pt(10.5)
        r_ann.font.color.rgb = RGBColor(30, 58, 138)

        table = doc.add_table(rows=1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Salary Component", "Monthly (₹)", "Annual (₹)"]
        hdr_cells = table.rows[0].cells
        for idx, text in enumerate(headers):
            hdr_cells[idx].text = text
            set_cell_background(hdr_cells[idx], "1E3A8A")
            p = hdr_cells[idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(9)

        rows_data = [
            ("Basic Salary (50%)", salary_breakup.get("monthly_basic", 0), salary_breakup.get("annual_basic", 0)),
            ("House Rent Allowance (HRA 40%)", salary_breakup.get("monthly_hra", 0), salary_breakup.get("annual_hra", 0)),
            ("Special Allowance", salary_breakup.get("monthly_special_allowance", 0), salary_breakup.get("annual_special_allowance", 0)),
            ("Gross Salary (A)", salary_breakup.get("monthly_gross", 0), salary_breakup.get("annual_gross", 0)),
            ("Employer PF Contribution (Capped)", salary_breakup.get("monthly_pf_employer", 0), salary_breakup.get("annual_pf_employer", 0)),
            ("Statutory Gratuity Provision (4.81%)", salary_breakup.get("monthly_gratuity", 0), salary_breakup.get("annual_gratuity", 0)),
            ("Total Cost to Company (CTC)", salary_breakup.get("monthly_ctc", 0), salary_breakup.get("annual_ctc", 0)),
            ("Employee PF Deduction", salary_breakup.get("monthly_pf_employee", 0), salary_breakup.get("annual_pf_employee", 0)),
            ("Karnataka Professional Tax (PT)", salary_breakup.get("monthly_pt", 0), salary_breakup.get("annual_pt", 0)),
            ("Net Take-Home Salary (Estimate)", salary_breakup.get("monthly_net_take_home", 0), salary_breakup.get("annual_net_take_home", 0)),
        ]

        for comp, m_val, a_val in rows_data:
            row_cells = table.add_row().cells
            row_cells[0].text = comp
            row_cells[1].text = f"₹{m_val:,.2f}"
            row_cells[2].text = f"₹{a_val:,.2f}"
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            # Format row
            is_highlight = "CTC" in comp or "Take-Home" in comp or "Gross" in comp
            for cell in row_cells:
                p = cell.paragraphs[0]
                for r in p.runs:
                    r.font.size = Pt(8.5)
                    if is_highlight:
                        r.bold = True
                        r.font.color.rgb = RGBColor(15, 23, 42)
                if is_highlight:
                    set_cell_background(cell, "F1F5F9")

    # --- Authorized Signature Block ---
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(25)
    p_sig.paragraph_format.space_after = Pt(2)
    r_sig1 = p_sig.add_run(f"For {settings.COMPANY_NAME}\n\n\n\n")
    r_sig1.font.size = Pt(10)
    
    r_sig2 = p_sig.add_run(f"{settings.FOUNDER_DIRECTOR}\n")
    r_sig2.bold = True
    r_sig2.font.size = Pt(10.5)
    r_sig2.font.color.rgb = RGBColor(15, 23, 42)
    
    r_sig3 = p_sig.add_run("Authorized Signatory & Sole Director")
    r_sig3.font.size = Pt(9)
    r_sig3.font.color.rgb = RGBColor(100, 116, 139)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

def create_certin_report_docx(incident_dict: dict) -> io.BytesIO:
    """
    Creates an official CERT-In Incident Reporting Form .docx document.
    """
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)

    # Top Logo Crest
    logo_path = Path(__file__).resolve().parent.parent / "static" / "img" / "logo.png"
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(6)
        p_logo.add_run().add_picture(str(logo_path), width=Inches(0.9))

    # Header
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hdr.paragraph_format.space_after = Pt(2)
    r1 = p_hdr.add_run("INDIAN COMPUTER EMERGENCY RESPONSE TEAM (CERT-In)\n")
    r1.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = RGBColor(185, 28, 28) # Red #b91c1c
    
    r2 = p_hdr.add_run("MANDATORY CYBER SECURITY INCIDENT REPORTING FORM (6-HOUR SLA)\n")
    r2.bold = True
    r2.font.size = Pt(10)
    
    r3 = p_hdr.add_run(f"Under Section 70B(6) of IT Act, 2000 | Reporting Entity: {settings.COMPANY_NAME} (CIN: {settings.CIN})")
    r3.font.size = Pt(8.5)
    r3.font.color.rgb = RGBColor(100, 116, 139)

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(4)
    p_div.paragraph_format.space_after = Pt(12)
    r_line = p_div.add_run("―" * 58)
    r_line.font.color.rgb = RGBColor(220, 38, 38)

    # Details Table
    table = doc.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(4.4)

    fields = [
        ("Incident Reference ID", incident_dict.get("incident_id", "INC-XXXX")),
        ("Title / Summary", incident_dict.get("title", "Cybersecurity Incident")),
        ("Severity Level", incident_dict.get("severity", "P1")),
        ("Incident Category", incident_dict.get("incident_type", "Malware / Intrusion")),
        ("CERT-In SLA Deadline", incident_dict.get("cert_in_deadline", "Within 6 hours")),
        ("Affected System / Asset", incident_dict.get("affected_systems", "Corporate Systems")),
        ("Detection Timestamp (UTC)", str(incident_dict.get("detected_at", datetime.now()))),
        ("Status", incident_dict.get("status", "Under Investigation")),
        ("Containment Status", incident_dict.get("containment_status", "Active Isolation")),
        ("DPDP Act 2023 Breach Notice", "Applicable (Breach of Personal Data Assessed)" if incident_dict.get("dpdp_breach") else "Not Triggered"),
        ("Remediation / Mitigations", incident_dict.get("remediation_steps", "Host isolated, credentials rotated, logs preserved.")),
        ("Reporting Officer", f"{settings.FOUNDER_DIRECTOR} (Sole Director / Authorized Officer)"),
        ("Designated Email", f"incident-response@{settings.PRIMARY_DOMAIN}")
    ]

    for label, val in fields:
        row_cells = table.add_row().cells
        row_cells[0].text = label
        row_cells[1].text = str(val)
        set_cell_background(row_cells[0], "F8FAFC")
        
        p0 = row_cells[0].paragraphs[0]
        p0.runs[0].bold = True
        p0.runs[0].font.size = Pt(9)
        p0.runs[0].font.color.rgb = RGBColor(51, 65, 85)
        
        p1 = row_cells[1].paragraphs[0]
        p1.runs[0].font.size = Pt(9)
        p1.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    # Signature
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(25)
    r_s = p_sig.add_run(
        f"Submitted by:\n{settings.FOUNDER_DIRECTOR}\n"
        f"Chief Information Security Authority / Director\n"
        f"{settings.COMPANY_NAME}"
    )
    r_s.font.size = Pt(9.5)
    r_s.font.color.rgb = RGBColor(30, 41, 59)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream
