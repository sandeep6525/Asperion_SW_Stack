"""
Asperion Enterprise OS - Comprehensive Document & Letter Generation Engine
Contains exhaustive templates for all 70+ HR, Corporate, and Legal letter categories.
"""
from datetime import date
from typing import Dict, Any, Optional
from app.config import settings

CORPORATE_HEADER_HTML = f"""
<div style="border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 25px; font-family: 'Helvetica Neue', Arial, sans-serif;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="vertical-align: middle; width: 62px; padding-right: 14px;">
                <img src="/static/img/logo.png" alt="Asperion Logo" style="width: 54px; height: 54px; border-radius: 50%; object-fit: contain; background: #0f172a; padding: 2px; border: 1.5px solid #38bdf8; display: block;">
            </td>
            <td style="vertical-align: middle;">
                <h2 style="color: #1e3a8a; margin: 0 0 4px 0; font-size: 19px; font-weight: 800;">{settings.COMPANY_NAME}</h2>
                <p style="margin: 0; font-size: 11px; color: #475569; line-height: 1.4;">
                    <strong>CIN:</strong> {settings.CIN} | <strong>PAN:</strong> {settings.PAN} | <strong>GSTIN:</strong> {settings.GSTIN}<br>
                    <strong>Registered Office:</strong> {settings.REGISTERED_OFFICE}
                </p>
            </td>
            <td style="text-align: right; vertical-align: middle;">
                <span style="display: inline-block; padding: 6px 12px; background: #eff6ff; color: #1d4ed8; font-weight: 600; font-size: 11px; border-radius: 6px; border: 1px solid #bfdbfe; letter-spacing: 0.5px;">
                    OFFICIAL CORRESPONDENCE
                </span>
            </td>
        </tr>
    </table>
</div>
"""

SIGNATURE_BLOCK_HTML = f"""
<div style="margin-top: 40px; font-family: 'Helvetica Neue', Arial, sans-serif;">
    <p style="margin-bottom: 25px; font-size: 13px; color: #334155;">For <strong>{settings.COMPANY_NAME}</strong></p>
    <div style="display: inline-block; border-bottom: 1px solid #94a3b8; width: 220px; padding-bottom: 4px; margin-bottom: 5px;">
        <p style="margin: 0; font-weight: bold; font-size: 13px; color: #0f172a;">{settings.FOUNDER_DIRECTOR}</p>
        <p style="margin: 0; font-size: 11px; color: #64748b;">Founder & Sole Director &bull; Digitally Signed</p>
    </div>
</div>
"""

# Master Catalogue of all 70+ HR & Legal Letter Templates
LETTER_TEMPLATES = {
    # ==========================
    # 01 RECRUITMENT (HR-REC-01 to 10)
    # ==========================
    "HR-REC-01": {"title": "Interview Invitation", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>Thank you for expressing interest in joining <strong>{company_name}</strong>. Following our review of your profile, we are pleased to invite you for an interview for the position of <strong>{designation}</strong>.</p>
        <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 12px 16px; margin: 15px 0;">
            <p style="margin: 0 0 6px 0;"><strong>Date & Time:</strong> {interview_date} at {interview_time}</p>
            <p style="margin: 0 0 6px 0;"><strong>Mode:</strong> {interview_mode}</p>
            <p style="margin: 0;"><strong>Interview Panel:</strong> {interviewers}</p>
        </div>
        <p>Please confirm your availability by replying to this communication at your earliest convenience.</p>
    """},
    "HR-REC-02": {"title": "Interview Reschedule", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>Please note that your interview for the position of <strong>{designation}</strong> has been rescheduled to <strong>{interview_date} at {interview_time}</strong> via {interview_mode}. We regret any inconvenience caused and request your confirmation.</p>
    """},
    "HR-REC-03": {"title": "Interview Cancellation", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We write to inform you that the interview scheduled for the position of <strong>{designation}</strong> on {interview_date} stands cancelled due to unforeseen scheduling conflicts. Our recruitment team will reach out with revised slots.</p>
    """},
    "HR-REC-04": {"title": "Application Acknowledgement", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>Thank you for submitting your application for the position of <strong>{designation}</strong> at <strong>{company_name}</strong>. Our talent acquisition team is evaluating your credentials and will update you shortly on next steps.</p>
    """},
    "HR-REC-05": {"title": "Selection - Intent to Offer", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We are delighted to inform you that following your evaluations, you have been selected for the position of <strong>{designation}</strong> at <strong>{company_name}</strong>.</p>
        <p>We propose an annual Cost-to-Company (CTC) of <strong>INR {annual_ctc:,.2f}</strong>. A comprehensive formal offer letter containing detailed terms and salary breakup will be shared shortly.</p>
    """},
    "HR-REC-06": {"title": "Candidate Rejection Letter", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>Thank you for taking the time to interview for the position of <strong>{designation}</strong>. While your background is impressive, we have chosen to proceed with another candidate whose experience more closely matches our immediate requirements. We will retain your profile in our talent pool for future opportunities.</p>
    """},
    "HR-REC-07": {"title": "Reference Check Consent", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>As part of our standard onboarding due diligence for the position of <strong>{designation}</strong>, please provide contact details and written consent for professional reference checks from your previous employers.</p>
    """},
    "HR-REC-08": {"title": "Background Verification Authorization", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>This document authorizes <strong>{company_name}</strong> and its designated background verification partner to verify educational qualifications, prior employment records, address verification, and criminal background checks as required by company policy.</p>
    """},
    "HR-REC-09": {"title": "Conditional Offer Letter", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We are pleased to extend this Conditional Offer for the position of <strong>{designation}</strong> at an annual CTC of <strong>INR {annual_ctc:,.2f}</strong>, subject to satisfactory completion of background verification, reference checks, and receipt of relieving documentation from your current employer.</p>
    """},
    "HR-REC-10": {"title": "Offer Withdrawal Notice", "category": "Recruitment", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We regret to inform you that the conditional offer of employment extended to you for the position of <strong>{designation}</strong> is hereby withdrawn due to non-fulfillment of agreed pre-joining conditions.</p>
    """},

    # ==========================
    # 02 ONBOARDING (HR-ONB-01 to 10)
    # ==========================
    "HR-ONB-01": {"title": "Formal Offer of Employment", "category": "Onboarding", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{candidate_name}</strong><br>{candidate_address}</p>
        <h3 style="color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px;">Subject: Offer of Employment - {designation}</h3>
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We are pleased to offer you the position of <strong>{designation}</strong> in the <strong>{department}</strong> department at <strong>{company_name}</strong>, commencing on or before <strong>{joining_date}</strong>.</p>
        <h4 style="color: #0f172a; margin-bottom: 8px;">Key Employment Terms:</h4>
        <ul style="line-height: 1.6; color: #334155;">
            <li><strong>Designation:</strong> {designation}</li>
            <li><strong>Department:</strong> {department}</li>
            <li><strong>Work Location:</strong> {location}</li>
            <li><strong>Probation Period:</strong> 6 months from the date of joining.</li>
            <li><strong>Notice Period:</strong> 30 days during probation, 60 days upon confirmation.</li>
            <li><strong>Total Annual Fixed CTC:</strong> INR {annual_ctc:,.2f}</li>
        </ul>
        <h4 style="color: #0f172a; margin-top: 20px;">Annexure A - Compensation Structure:</h4>
        {salary_annexure_html}
        <p style="margin-top: 20px;">Please sign and return the duplicate copy of this letter as formal acceptance of this offer.</p>
    """},
    "HR-ONB-02": {"title": "Formal Appointment Letter", "category": "Onboarding", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">Subject: Letter of Appointment</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Consequent to your acceptance of our offer and joining on <strong>{joining_date}</strong>, we are pleased to issue your formal Letter of Appointment as <strong>{designation}</strong> in <strong>{company_name}</strong>.</p>
        <p>Your employment will be governed by the company's Code of Conduct, Information Security Policy, and Service Rules as amended from time to time.</p>
        {salary_annexure_html}
    """},
    "HR-ONB-03": {"title": "Internship Offer Letter", "category": "Onboarding", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>We are pleased to offer you an Internship as <strong>{designation} Intern</strong> at <strong>{company_name}</strong> for a duration of 6 months. You will receive a monthly stipend of <strong>INR {stipend_amount:,.2f}</strong> subject to attendance and performance.</p>
    """},
    "HR-ONB-04": {"title": "Consultant Engagement Confirmation", "category": "Onboarding", "body": """
        <p>Dear <strong>{consultant_name}</strong>,</p>
        <p>This confirms your professional engagement as an Independent Technical Consultant for <strong>{company_name}</strong>. Professional fees will be paid against monthly invoices with applicable TDS deductions under Section 194J of the Income Tax Act.</p>
    """},
    "HR-ONB-05": {"title": "Joining Date Extension", "category": "Onboarding", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>With reference to your request for extension of joining date, management has approved your revised joining date to <strong>{new_joining_date}</strong> for the role of <strong>{designation}</strong>.</p>
    """},
    "HR-ONB-06": {"title": "Document Deficiency Notice", "category": "Onboarding", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>During our audit of your onboarding dossier, the following statutory documents were found pending: {pending_documents}. Please submit these within 7 working days to ensure uninterrupted payroll processing.</p>
    """},
    "HR-ONB-07": {"title": "Joining Confirmation & Induction Kit", "category": "Onboarding", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Welcome to <strong>{company_name}</strong>! This confirms your official joining on <strong>{joining_date}</strong>. Your corporate email and Single Sign-On credentials have been provisioned.</p>
    """},
    "HR-ONB-08": {"title": "Probation Confirmation Letter", "category": "Onboarding", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">Subject: Confirmation of Employment</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We are pleased to inform you that your performance during the probationary period has been evaluated and found satisfactory. Consequently, your employment with <strong>{company_name}</strong> is hereby confirmed with effect from <strong>{confirmation_date}</strong>.</p>
    """},
    "HR-ONB-09": {"title": "Probation Extension Letter", "category": "Onboarding", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Following a review of your performance during the probationary period, management has decided to extend your probation by <strong>{extension_months} months</strong> until {new_probation_end_date} to provide an opportunity to demonstrate required benchmarks.</p>
    """},
    "HR-ONB-10": {"title": "Non-Joining Offer Lapse Notice", "category": "Onboarding", "body": """
        <p>Dear <strong>{candidate_name}</strong>,</p>
        <p>As you did not report for duty on your scheduled joining date of {joining_date} without prior authorization, the offer of employment extended to you stands cancelled and lapsed.</p>
    """},

    # ==========================
    # 03 EMPLOYMENT & ADMINISTRATION (HR-ADM-01 to 12)
    # ==========================
    "HR-ADM-01": {"title": "Salary Revision & Compensation Letter", "category": "Employment", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">Subject: Compensation Revision</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>In recognition of your performance and valuable contributions to <strong>{company_name}</strong>, management is pleased to revise your annual Cost to Company (CTC) to <strong>INR {new_annual_ctc:,.2f}</strong>, effective from <strong>{effective_date}</strong>.</p>
        {salary_annexure_html}
    """},
    "HR-ADM-02": {"title": "Promotion Letter", "category": "Employment", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">Subject: Promotion to {new_designation}</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We are delighted to promote you to the position of <strong>{new_designation}</strong> in recognition of your leadership, technical mastery, and performance. This promotion takes effect from <strong>{effective_date}</strong>.</p>
    """},
    "HR-ADM-03": {"title": "Role & Designation Change", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Consequent to internal organizational restructuring, your official designation is hereby realigned to <strong>{new_designation}</strong> in the <strong>{department}</strong> department effective {effective_date}.</p>
    """},
    "HR-ADM-04": {"title": "Transfer & Location Change", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>You are hereby transferred from your current base in {old_location} to our facility at <strong>{new_location}</strong> effective {effective_date}. Relocation support will be provided in line with corporate policy.</p>
    """},
    "HR-ADM-05": {"title": "Reporting Manager Realignment", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Please note that effective {effective_date}, your primary reporting manager will be <strong>{new_manager_name}</strong> ({new_manager_designation}).</p>
    """},
    "HR-ADM-06": {"title": "Remote / Hybrid Work Approval", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We are pleased to approve your transition to a <strong>{work_mode}</strong> working model. You must adhere strictly to information security protocols, disk encryption requirements, and VPN access policies.</p>
    """},
    "HR-ADM-07": {"title": "Deputation / Client Assignment Letter", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>You are hereby deputed to deliver software consulting services for our client <strong>{client_name}</strong> for a duration of {deputation_duration} effective {start_date}.</p>
    """},
    "HR-ADM-08": {"title": "Employment Verification Letter", "category": "Employment", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To Whom It May Concern,</p>
        <p>This is to certify that <strong>{employee_name}</strong> (Emp Code: <strong>{emp_code}</strong>) is a permanent, full-time employee of <strong>{company_name}</strong> since {doj}, presently working as <strong>{designation}</strong>.</p>
    """},
    "HR-ADM-09": {"title": "Leave Approval Letter", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Your request for {leave_days} days of {leave_type} from {start_date} to {end_date} has been approved by your reporting manager.</p>
    """},
    "HR-ADM-10": {"title": "Leave Rejection / Deferral Notice", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We regret that your requested leave from {start_date} to {end_date} cannot be approved at this time due to critical milestone deliverables and delivery commitments.</p>
    """},
    "HR-ADM-11": {"title": "Return to Work Confirmation", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We acknowledge your return to duty on {return_date} following your authorized leave of absence. Your workstation access and project roles have been reactivated.</p>
    """},
    "HR-ADM-12": {"title": "Letter of Recognition & Appreciation", "category": "Employment", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>On behalf of leadership at <strong>{company_name}</strong>, we commend your outstanding commitment and technical excellence on <strong>{project_name}</strong>. Thank you for setting a benchmark for the team!</p>
    """},

    # ==========================
    # 04 EMPLOYEE RELATIONS, PIP & POSH (HR-ER-01 to 12)
    # ==========================
    "HR-ER-01": {"title": "Performance Feedback Memo", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>This memorandum documents discussions regarding performance shortfalls identified in sprint execution and quality benchmarks. Please review the attached feedback points and schedule a follow-up with your manager.</p>
    """},
    "HR-ER-02": {"title": "Performance Improvement Plan (PIP)", "category": "Employee Relations", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #b91c1c;">Strictly Private & Confidential: Performance Improvement Plan</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>This document initiates a formal Performance Improvement Plan (PIP) for a duration of <strong>{pip_duration_days} days</strong>, commencing on <strong>{start_date}</strong>.</p>
        <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 12px; margin: 15px 0;">
            <strong>Key Focus Objectives:</strong><br>{performance_objectives}
        </div>
        <p>Failure to meet acceptable standards by the conclusion of this plan may result in further administrative actions up to and including separation.</p>
    """},
    "HR-ER-03": {"title": "PIP Review & Closure", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We have reviewed your progress over the PIP period. We are pleased to note satisfactory improvement across agreed parameters and formally close this Performance Improvement Plan.</p>
    """},
    "HR-ER-04": {"title": "Counselling Memo", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>This record documents a constructive counselling session conducted on {counselling_date} regarding workplace conduct and collaboration standards.</p>
    """},
    "HR-ER-05": {"title": "Show Cause Notice", "category": "Employee Relations", "body": """
        <p>To: <strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #dc2626;">SHOW CAUSE NOTICE</h3>
        <p>It has been reported that on {incident_date}, you engaged in {allegation_description}. You are hereby directed to show cause in writing within 48 hours why disciplinary action should not be initiated against you.</p>
    """},
    "HR-ER-06": {"title": "Suspension Pending Inquiry", "category": "Employee Relations", "body": """
        <p>To: <strong>{employee_name}</strong></p>
        <p>Pending formal domestic inquiry into serious misconduct allegations, you are placed under suspension with immediate effect. Subsistence allowance will be paid in compliance with applicable labor laws.</p>
    """},
    "HR-ER-07": {"title": "Domestic Inquiry Notice", "category": "Employee Relations", "body": """
        <p>To: <strong>{employee_name}</strong></p>
        <p>You are hereby summoned to appear before the Domestic Inquiry Committee on {inquiry_date} at {inquiry_time} regarding charges specified in Show Cause Notice ref {show_cause_ref}.</p>
    """},
    "HR-ER-08": {"title": "Formal Warning Letter", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Following our inquiry into {incident_description}, this constitutes a Formal Warning Letter. Continued non-compliance with company policies will lead to strict disciplinary actions.</p>
    """},
    "HR-ER-09": {"title": "Final Warning Letter", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>This serves as a FINAL WARNING regarding repeated violations of {policy_name}. Failure to maintain expected conduct will result in immediate termination of employment.</p>
    """},
    "HR-ER-10": {"title": "Grievance Acknowledgement", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We acknowledge receipt of your formal workplace grievance dated {grievance_date}. The Grievance Redressal Committee will review your submission and schedule a hearing within 7 working days.</p>
    """},
    "HR-ER-11": {"title": "Grievance Resolution Outcome", "category": "Employee Relations", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>The Grievance Redressal Committee has concluded its investigation into your grievance ref {grievance_ref}. The findings and corrective actions are detailed herein.</p>
    """},
    "HR-ER-12": {"title": "Workplace Harassment (POSH) Complaint Acknowledgement", "category": "Employee Relations", "body": """
        <p>Dear Complainant,</p>
        <p>The Internal Committee (IC) of <strong>{company_name}</strong> acknowledges receipt of your complaint under the POSH Act 2013. The Committee will conduct an inquiry in strict confidentiality with interim protective measures in force.</p>
    """},

    # ==========================
    # 05 SEPARATION & OFFBOARDING (HR-SEP-01 to 20)
    # ==========================
    "HR-SEP-01": {"title": "Resignation Acknowledgement", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We acknowledge receipt of your resignation notice dated <strong>{resignation_date}</strong>. Your request is being reviewed by management and your reporting manager.</p>
    """},
    "HR-SEP-02": {"title": "Resignation Acceptance & Exit Schedule", "category": "Separation", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To,<br><strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">Subject: Acceptance of Resignation</h3>
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We acknowledge and accept your resignation. Your last working day with <strong>{company_name}</strong> will be <strong>{last_working_day}</strong>.</p>
        <p>Please initiate knowledge transfer, hand over company assets, and complete clearance across IT, Admin, Finance, and HR departments.</p>
    """},
    "HR-SEP-03": {"title": "Notice Waiver / Buyout Confirmation", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Management has agreed to your request for notice period shortfall. A notice buyout of <strong>{buyout_days} days</strong> will be adjusted in your Full and Final settlement.</p>
    """},
    "HR-SEP-04": {"title": "Garden Leave Notice", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>You are hereby placed on Garden Leave effective {start_date} until {last_working_day}. You will remain in employment and receive full salary but shall not access company systems or represent the company.</p>
    """},
    "HR-SEP-05": {"title": "Unauthorized Absence & Abandonment Notice", "category": "Separation", "body": """
        <p>To: <strong>{employee_name}</strong></p>
        <p>You have remained absent from duty without authorization since {absence_start_date}. Please report for duty within 48 hours, failing which it will be presumed that you have voluntarily abandoned employment.</p>
    """},
    "HR-SEP-06": {"title": "Termination for Performance Shortfall", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Consequent to sustained performance shortfalls following the conclusion of your PIP, your employment with <strong>{company_name}</strong> stands terminated effective close of business hours today.</p>
    """},
    "HR-SEP-07": {"title": "Termination for Proven Misconduct", "category": "Separation", "body": """
        <p>To: <strong>{employee_name}</strong></p>
        <p>Following findings of the Domestic Inquiry proving gross misconduct, management has decided to dismiss you from service with immediate effect.</p>
    """},
    "HR-SEP-08": {"title": "Termination Due to Position Redundancy", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Due to restructuring of business operations, your position of <strong>{designation}</strong> has become redundant. You will be paid severance compensation in full compliance with labor laws.</p>
    """},
    "HR-SEP-09": {"title": "Probation Discontinuation Notice", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>We regret to inform you that your services will not be confirmed post-probation and stand discontinued with effect from {discontinuation_date}.</p>
    """},
    "HR-SEP-10": {"title": "Retirement Intimation", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>As per corporate records, you will attain the age of superannuation on {retirement_date}. We express our deepest gratitude for your decades of loyal service.</p>
    """},
    "HR-SEP-11": {"title": "Fixed-Term Contract Expiry Notice", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>This serves to inform you that your fixed-term employment contract will conclude upon its natural expiry on {expiry_date}.</p>
    """},
    "HR-SEP-12": {"title": "Internship Completion Certificate", "category": "Separation", "body": """
        <p>To Whom It May Concern,</p>
        <p>This certifies that <strong>{candidate_name}</strong> has successfully completed their software engineering internship with <strong>{company_name}</strong> from {doj} to {lwd}.</p>
    """},
    "HR-SEP-13": {"title": "No Dues & Multi-Department Clearance Form", "category": "Separation", "body": """
        <p>Employee: <strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">NO DUES CLEARANCE FORM</h3>
        <table style="width:100%; border:1px solid #cbd5e1; font-size:12px; border-collapse:collapse;">
            <tr style="background:#f8fafc;"><th class="p-2">Department</th><th class="p-2">Clearance Items</th><th class="p-2">Status</th><th class="p-2">Sign-Off</th></tr>
            <tr><td class="p-2">IT & Systems</td><td class="p-2">Laptops, Passkeys, AWS & Google Workspace Revoked</td><td class="p-2">Cleared</td><td class="p-2">IT Admin</td></tr>
            <tr><td class="p-2">Finance</td><td class="p-2">Travel Advances, Corporate Cards, Loan Dues</td><td class="p-2">Cleared</td><td class="p-2">Finance Lead</td></tr>
            <tr><td class="p-2">Admin / Facilities</td><td class="p-2">ID Card, Access Badges, Keys</td><td class="p-2">Cleared</td><td class="p-2">Admin Lead</td></tr>
            <tr><td class="p-2">Reporting Manager</td><td class="p-2">Code Repositories, Knowledge Transfer, Documentation</td><td class="p-2">Cleared</td><td class="p-2">Delivery Head</td></tr>
        </table>
    """},
    "HR-SEP-14": {"title": "Full and Final (F&F) Settlement Statement", "category": "Separation", "body": """
        <p>Employee: <strong>{employee_name}</strong> (Emp Code: {emp_code})</p>
        <h3 style="color: #1e3a8a;">FULL AND FINAL SETTLEMENT STATEMENT</h3>
        <p>Salary for Days Worked + Leave Encashment + Gratuity (if eligible) - Deductions (Notice shortfall, Tax, Advances) = Net Payable INR {fnf_amount:,.2f}.</p>
    """},
    "HR-SEP-15": {"title": "Formal Relieving Letter", "category": "Separation", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To Whom It May Concern,</p>
        <h3 style="color: #1e3a8a; text-align: center;">RELIEVING LETTER</h3>
        <p>This is to certify that <strong>{employee_name}</strong> (Employee ID: <strong>{emp_code}</strong>) was employed with <strong>{company_name}</strong> from <strong>{doj}</strong> to <strong>{lwd}</strong>.</p>
        <p>At the time of leaving, they held the designation of <strong>{designation}</strong> in the <strong>{department}</strong> department.</p>
        <p>They have completed all exit formalities and handover requirements, and stand relieved of their duties at the close of business hours on <strong>{lwd}</strong>.</p>
        <p>We wish them all the best in their future endeavors.</p>
    """},
    "HR-SEP-16": {"title": "Service and Experience Certificate", "category": "Separation", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>To Whom It May Concern,</p>
        <h3 style="color: #1e3a8a; text-align: center;">EXPERIENCE CERTIFICATE</h3>
        <p>This is to certify that <strong>{employee_name}</strong> was associated with <strong>{company_name}</strong> as <strong>{designation}</strong> from <strong>{doj}</strong> to <strong>{lwd}</strong>.</p>
        <p>During their tenure with us, they demonstrated professional competence, diligence, and integrity in carrying out their responsibilities.</p>
    """},
    "HR-SEP-17": {"title": "Service Certificate", "category": "Separation", "body": """
        <p>Date: <strong>{issue_date}</strong></p>
        <p>This certifies that <strong>{employee_name}</strong> rendered service as <strong>{designation}</strong> in <strong>{company_name}</strong> from {doj} to {lwd}.</p>
    """},
    "HR-SEP-18": {"title": "Asset & Data Return Demand Notice", "category": "Separation", "body": """
        <p>To: <strong>{employee_name}</strong></p>
        <p>This is a formal demand for immediate return of company property including {unreturned_assets}. Failure to return these items within 48 hours will compel legal action and withholding of F&F settlement.</p>
    """},
    "HR-SEP-19": {"title": "Confidentiality & Non-Solicitation Reminder", "category": "Separation", "body": """
        <p>Dear <strong>{employee_name}</strong>,</p>
        <p>Following your separation, this letter reminds you of your ongoing legal obligations under your Employment Agreement regarding Confidentiality, Non-Disclosure of Proprietary Source Code, and Non-Solicitation of clients and employees.</p>
    """},
    "HR-SEP-20": {"title": "Rehire Eligibility & Reference Response", "category": "Separation", "body": """
        <p>To Whom It May Concern,</p>
        <p>In response to your reference check request for <strong>{employee_name}</strong>, we confirm their employment as {designation} from {doj} to {lwd}. Their exit was in good standing and they remain eligible for rehire.</p>
    """},

    # ==========================
    # 06 CORPORATE & LEGAL (LEG-NDA, LEG-MSA, LEG-SOW)
    # ==========================
    "LEG-NDA-01": {"title": "Mutual Non-Disclosure Agreement (NDA)", "category": "Legal", "body": """
        <h3 style="color: #1e3a8a; text-align: center;">MUTUAL NON-DISCLOSURE AGREEMENT</h3>
        <p>This Mutual Non-Disclosure Agreement is entered into as of <strong>{effective_date}</strong> by and between <strong>{company_name}</strong> (CIN: {cin}) and <strong>{counterparty_name}</strong>.</p>
        <p>The parties will disclose proprietary information concerning <strong>{project_purpose}</strong>. Each party agrees to protect such Confidential Information with utmost confidentiality.</p>
    """},
    "LEG-MSA-01": {"title": "Master Services Agreement (MSA)", "category": "Legal", "body": """
        <h3 style="color: #1e3a8a; text-align: center;">MASTER SERVICES AGREEMENT</h3>
        <p>This Master Services Agreement governs the provision of software engineering, cloud architecture, and digital transformation consulting by <strong>{company_name}</strong> to <strong>{counterparty_name}</strong>.</p>
        <p>Detailed statements of work, deliverable milestones, and payment terms will be governed by supplementary Statements of Work (SOWs) executed hereunder.</p>
    """},
    "LEG-SOW-01": {"title": "Statement of Work (SOW)", "category": "Legal", "body": """
        <h3 style="color: #1e3a8a; text-align: center;">STATEMENT OF WORK</h3>
        <p>This Statement of Work is executed under Master Services Agreement ref {msa_ref} between <strong>{company_name}</strong> and <strong>{counterparty_name}</strong>.</p>
        <p>Scope: <strong>{project_purpose}</strong> | Deliverable Milestones: {milestone_schedule} | Commercial Value: INR {contract_value:,.2f}.</p>
    """}
}

def render_salary_annexure_table(breakup: Dict[str, Any]) -> str:
    """Renders a clean HTML table of the salary breakup for offer letters and revisions"""
    e = breakup.get("earnings", {})
    em = breakup.get("employer_contributions", {})
    ed = breakup.get("employee_deductions", {})
    th = breakup.get("take_home", {})
    
    html = f"""
    <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 10px; border: 1px solid #cbd5e1;">
        <thead>
            <tr style="background: #f1f5f9; color: #1e293b; border-bottom: 2px solid #cbd5e1;">
                <th style="padding: 8px 12px; text-align: left;">Component</th>
                <th style="padding: 8px 12px; text-align: right;">Monthly (INR)</th>
                <th style="padding: 8px 12px; text-align: right;">Annual (INR)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: #f8fafc; font-weight: bold; color: #1e3a8a;"><td colspan="3" style="padding: 6px 12px;">Part A: Gross Earnings</td></tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Basic Salary</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('basic_salary', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('basic_salary', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">House Rent Allowance (HRA)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('hra', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('hra', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Special Allowance / Balancer</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('special_allowance', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{e.get('special_allowance', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr style="font-weight: bold; background: #f1f5f9;">
                <td style="padding: 6px 12px; border-bottom: 1px solid #cbd5e1;">Gross Salary (A)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #cbd5e1;">{e.get('gross_salary', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #cbd5e1;">{e.get('gross_salary', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr style="background: #f8fafc; font-weight: bold; color: #1e3a8a;"><td colspan="3" style="padding: 6px 12px;">Part B: Employer Retirals & Statutory Contributions</td></tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Employer Provident Fund (PF 12%)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{em.get('employer_pf', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{em.get('employer_pf', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Gratuity Accrual Provision (4.81%)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{em.get('gratuity_provision', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{em.get('gratuity_provision', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr style="font-weight: bold; background: #e2e8f0; color: #0f172a;">
                <td style="padding: 8px 12px; border-bottom: 2px solid #94a3b8;">Total Annual Cost to Company (CTC = A + B)</td>
                <td style="padding: 8px 12px; text-align: right; border-bottom: 2px solid #94a3b8;">{breakup.get('monthly_ctc', 0):,.2f}</td>
                <td style="padding: 8px 12px; text-align: right; border-bottom: 2px solid #94a3b8;">{breakup.get('annual_ctc', 0):,.2f}</td>
            </tr>
            <tr style="background: #f8fafc; font-weight: bold; color: #1e3a8a;"><td colspan="3" style="padding: 6px 12px;">Part C: Employee Deductions (Estimated)</td></tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Employee PF Contribution (12%)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{ed.get('employee_pf', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{ed.get('employee_pf', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 6px 12px; border-bottom: 1px solid #e2e8f0;">Professional Tax (Karnataka)</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{ed.get('professional_tax', {}).get('monthly', 0):,.2f}</td>
                <td style="padding: 6px 12px; text-align: right; border-bottom: 1px solid #e2e8f0;">{ed.get('professional_tax', {}).get('annual', 0):,.2f}</td>
            </tr>
            <tr style="font-weight: bold; background: #ecfdf5; color: #065f46;">
                <td style="padding: 8px 12px;">Estimated Monthly Net In-Hand (Take-Home)</td>
                <td style="padding: 8px 12px; text-align: right;">{th.get('monthly_net_in_hand', 0):,.2f}</td>
                <td style="padding: 8px 12px; text-align: right;">{th.get('annual_net_in_hand', 0):,.2f}</td>
            </tr>
        </tbody>
    </table>
    """
    return html

def generate_document_html(
    letter_code: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generates a full HTML official document by injecting variables into corporate letterheads
    """
    tmpl = LETTER_TEMPLATES.get(letter_code)
    if not tmpl:
        tmpl = {
            "title": f"Official Letter - {letter_code}",
            "category": "General Correspondence",
            "body": "<p>Document Reference: {letter_code}</p><p>{custom_body}</p>"
        }
        
    default_fields = {
        "candidate_name": "[Candidate Name]",
        "employee_name": "[Employee Name]",
        "consultant_name": "[Consultant Name]",
        "emp_code": "ADT-EMP-001",
        "designation": "Software Engineer",
        "new_designation": "Lead Software Engineer",
        "department": "Engineering",
        "location": "Bangalore Head Office",
        "old_location": "Bangalore",
        "new_location": "Bangalore North",
        "new_manager_name": "Arjun Sharma",
        "new_manager_designation": "Director of Engineering",
        "joining_date": date.today().strftime("%d %B %Y"),
        "new_joining_date": date.today().strftime("%d %B %Y"),
        "confirmation_date": date.today().strftime("%d %B %Y"),
        "effective_date": date.today().strftime("%d %B %Y"),
        "resignation_date": date.today().strftime("%d %B %Y"),
        "last_working_day": date.today().strftime("%d %B %Y"),
        "doj": date.today().strftime("%d %B %Y"),
        "lwd": date.today().strftime("%d %B %Y"),
        "annual_ctc": 1200000.0,
        "new_annual_ctc": 1500000.0,
        "stipend_amount": 25000.0,
        "fnf_amount": 85000.0,
        "buyout_days": 15,
        "extension_months": 3,
        "new_probation_end_date": date.today().strftime("%d %B %Y"),
        "candidate_address": "Bangalore, Karnataka, India",
        "interview_date": date.today().strftime("%d %B %Y"),
        "interview_time": "11:00 AM IST",
        "interview_mode": "Google Meet Video Call",
        "interviewers": "Technical Lead & Engineering Manager",
        "pip_duration_days": 60,
        "start_date": date.today().strftime("%d %B %Y"),
        "end_date": date.today().strftime("%d %B %Y"),
        "leave_days": 3,
        "leave_type": "Casual Leave",
        "return_date": date.today().strftime("%d %B %Y"),
        "work_mode": "Hybrid (3 Days Office / 2 Days Remote)",
        "deputation_duration": "6 Months",
        "client_name": "Helios Cloud Technologies",
        "project_name": "Enterprise Cloud Platform",
        "counselling_date": date.today().strftime("%d %B %Y"),
        "incident_date": date.today().strftime("%d %B %Y"),
        "allegation_description": "unauthorized external disclosure of project documentation",
        "show_cause_ref": "ADT/SCN/2026/001",
        "inquiry_date": date.today().strftime("%d %B %Y"),
        "inquiry_time": "02:30 PM IST",
        "incident_description": "repeated unapproved absenteeism",
        "policy_name": "Asperion Information Security Policy",
        "grievance_date": date.today().strftime("%d %B %Y"),
        "grievance_ref": "ADT/GRV/2026/001",
        "absence_start_date": date.today().strftime("%d %B %Y"),
        "discontinuation_date": date.today().strftime("%d %B %Y"),
        "retirement_date": date.today().strftime("%d %B %Y"),
        "expiry_date": date.today().strftime("%d %B %Y"),
        "unreturned_assets": "MacBook Pro M3 and Security Access Token",
        "performance_objectives": "Adhere to pull request quality guidelines, maintain sprint velocity, and complete security compliance modules.",
        "counterparty_name": "[Counterparty Organization]",
        "counterparty_address": "[Counterparty Registered Office]",
        "project_purpose": "Software Engineering & Enterprise Digital Transformation",
        "msa_ref": "ADT/MSA/2026/001",
        "milestone_schedule": "Milestone 1: Architecture, Milestone 2: Core MVP, Milestone 3: Production Deployment",
        "contract_value": 2400000.0,
        "pending_documents": "PF UAN Declaration Form and Relieving Letter from previous employer"
    }

    full_context = {
        **default_fields,
        "company_name": settings.COMPANY_NAME,
        "cin": settings.CIN,
        "registered_office": settings.REGISTERED_OFFICE,
        "issue_date": date.today().strftime("%d %B %Y"),
        "letter_code": letter_code,
        **context
    }
    
    if "salary_breakup" in context and isinstance(context["salary_breakup"], dict):
        full_context["salary_annexure_html"] = render_salary_annexure_table(context["salary_breakup"])
    elif "salary_annexure_html" not in full_context:
        full_context["salary_annexure_html"] = ""
        
    try:
        body_content = tmpl["body"].format(**full_context)
    except KeyError as e:
        body_content = tmpl["body"] + f"<p style='color:red;'>[Missing parameter: {e}]</p>"
        
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{tmpl['title']}</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #1e293b; max-width: 800px; margin: 40px auto; padding: 30px; border: 1px solid #e2e8f0; background: #fff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
            h2, h3, h4 {{ margin-top: 15px; margin-bottom: 8px; }}
            p {{ margin-bottom: 12px; font-size: 13.5px; }}
            ul {{ margin-bottom: 12px; font-size: 13.5px; }}
            @media print {{ body {{ border: none; box-shadow: none; padding: 0; margin: 0; }} }}
        </style>
    </head>
    <body>
        {CORPORATE_HEADER_HTML}
        <div class="content-body">
            {body_content}
        </div>
        {SIGNATURE_BLOCK_HTML}
    </body>
    </html>
    """
    
    return {
        "letter_code": letter_code,
        "letter_title": tmpl["title"],
        "category": tmpl["category"],
        "html_content": full_html
    }
