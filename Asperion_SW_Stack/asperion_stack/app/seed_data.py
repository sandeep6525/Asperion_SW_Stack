"""
Asperion Enterprise OS - Comprehensive Master Data Seeder
Populates initial database with exhaustive operational data across all 8 enterprise pillars.
"""
import json
from datetime import date, datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models.governance import EntityMaster, BoardResolution, ComplianceCalendarItem, PolicyRecord, AuthorityMatrixItem, AuditLog
from app.models.strategy_kpi import (
    StrategicFunction, CapabilityCapacity, EnterpriseKPI, StrategicDecisionThought, ImplementationRoadmapItem
)
from app.models.crm_legal import Prospect, ClientContract, ClientOnboardingRecord, LegalRiskObligation
from app.models.crm_enterprise import (
    Opportunity, CRMActivity, CustomerAccount, SupportTicket, EnterpriseRisk
)
from app.models.ticketing_notifications import (
    InternalTicket, SystemNotification, NotificationRule
)
from app.models.developer_platform import (
    DeveloperPlatformAccount, DeveloperEnvironmentSecret, StatutoryChallanFiling
)
from app.models.attendance import (
    GeofenceZone, AttendanceRecord, AttendanceAnomalyLog, WhatsAppAttendanceSession
)
from app.models.finance import (
    AccountMaster, Invoice, PurchaseOrder, APBill, CashFlowEntry, FixedAsset,
    ExpenseClaim, BankReconciliationRecord, JournalEntry, BudgetItem, ProjectPnL
)
from app.models.hrms import (
    Candidate, Employee, SalaryStructure, PayrollRecord, HRLetter, SeparationClearance,
    LeaveRecord, POSHCase
)
from app.models.pmo import (
    Project, ProjectMilestone, WBSTask, RACIAssignment, RAIDItem, ChangeRequest,
    Sprint, Stakeholder, ProjectIntake, ProjectCharter, ActionDecisionItem,
    CapacityPlanItem, QualityUATItem, ProjectClosureItem
)
from app.models.sdlc import (
    SDLCRequirement, ArchitectureDecisionRecord, CodeRepository,
    PullRequestReview, CICDPipelineRun, DefectBugRecord,
    ReleaseDeployment, SREObservabilityMetric
)
from app.models.procurement import (
    Vendor, SourcingCategory, PurchaseRequisition, StrategicSourcingEvent,
    VendorBidSubmission, VendorContract, GoodsReceivedNote,
    VendorScorecard, RFPComparison, VendorRiskAssessment,
    VendorCorrectiveActionPlan
)
from app.models.guardrails import (
    GuardrailRule, GuardrailExecutionLog, ArchitectureBlueprint
)
from app.models.ai_infrastructure import (
    AIModelEndpoint, MCPServerCatalog, CloudInfrastructureTopology,
    SecurityAuthenticityCertificate, ExecutiveAlertRule
)
from app.models.iso_standards import (
    ISOCertificationMaster, ISOClauseControl, ISOAuditInspection,
    ISOCorrectiveActionWorksheet, FormalGrievanceRecord
)
from app.models.training import (
    TrainingTrack, TrainingModule, EmployeeTrainingEnrollment, TrainingMaterial
)
from app.models.itsm import (
    ConfigurationItem, ITSMProblem, ITSMChangeRequest, ITSMRunbookFix,
    ITSMProcurementLOI, ITSMSLAContract
)
from app.models.agentic_ai import (
    EnterpriseAgent, AgenticMission, AgentExecutionTrace
)
from app.models.enterprise_operations import (
    EnterpriseEventLedger, DisasterRecoverySnapshot, DPDPConsentRecord, SystemDiagnosticTelemetry
)
from app.models.sharepoint import (
    SharePointArticle, SharePointComment, SharePointCommunityQuestion, SharePointDocumentLibraryItem
)
from app.models.communications import (
    ChatChannel, ChatMessage, TeamMemberPresence, VirtualHuddleSession
)
from app.models.passkey_infrastructure import (
    PasskeyCredential, ZeroTrustPolicy, DRSimulationTest
)
from app.models.infrastructure import (
    ITAsset, CloudAccount, IAMCredential, SaaSLicense, BackupDRPlan,
    CertificateSecret, ITProvisioningChecklist
)
from app.models.cybersecurity import (
    SecurityIncident, SecurityAlert, EvidenceItem, Playbook, VulnerabilityPatch,
    TabletopDrill, CERTInRegulatoryReport, ThreatIntelIndicator
)
from app.engines.ctc_calculator import compute_salary_breakup
from app.engines.letter_generator import generate_document_html

def _migrate_procurement_tables():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            def add_col(tbl, col, def_val):
                try:
                    res = conn.execute(text(f"PRAGMA table_info({tbl})")).fetchall()
                    cols = [r[1] for r in res]
                    if col not in cols:
                        conn.execute(text(f"ALTER TABLE {tbl} ADD COLUMN {col} {def_val}"))
                        conn.commit()
                except Exception:
                    pass

            add_col("vendors", "duns_number", "VARCHAR(50) DEFAULT '91-234-5678'")
            add_col("vendors", "msme_category", "VARCHAR(50) DEFAULT 'Micro'")
            add_col("vendors", "msme_payment_due_days", "INTEGER DEFAULT 45")
            add_col("vendors", "rating", "FLOAT DEFAULT 92.5")

            add_col("vendor_contracts", "renewal_notice_days", "INTEGER DEFAULT 60")
            add_col("vendor_contracts", "auto_renew_enabled", "BOOLEAN DEFAULT 1")
            add_col("vendor_contracts", "liability_cap_inr", "FLOAT DEFAULT 1000000.0")
            add_col("vendor_contracts", "governing_jurisdiction", "VARCHAR(100) DEFAULT 'Courts of Bengaluru, Karnataka'")

            add_col("goods_received_notes", "warehouse_location", "VARCHAR(100) DEFAULT 'Horamavu Bangalore HQ'")
            add_col("goods_received_notes", "rejection_reason", "VARCHAR(255)")
            add_col("goods_received_notes", "rtv_credit_note_ref", "VARCHAR(50)")
            add_col("goods_received_notes", "quantity_rejected", "FLOAT DEFAULT 0.0")

            add_col("purchase_orders", "items_json", "TEXT DEFAULT '[]'")
            add_col("purchase_orders", "payment_terms", "VARCHAR(100) DEFAULT 'Net 30 Days'")
            add_col("purchase_orders", "delivery_challan_no", "VARCHAR(100)")
            add_col("purchase_orders", "statutory_notes", "TEXT DEFAULT 'Subject to Bangalore Jurisdiction. MSMED Act 2006 terms apply.'")

            add_col("security_incidents", "mitre_tactics", "VARCHAR(255) DEFAULT 'Initial Access, Defense Evasion'")
            add_col("security_incidents", "ntp_synchronized", "BOOLEAN DEFAULT 1")
            add_col("security_incidents", "containment_summary", "TEXT")
    except Exception:
        pass

def seed_database():
    Base.metadata.create_all(bind=engine)
    _migrate_procurement_tables()
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(EntityMaster).first():
        if not db.query(Opportunity).first():
            _seed_crm_erm(db)
            db.commit()
        if not db.query(InternalTicket).filter(InternalTicket.subject == "New MacBook Pro M3 Max Developer Provisioning").first():
            _seed_internal_tickets_and_notifs(db)
            db.commit()
        if not db.query(DeveloperPlatformAccount).first():
            _seed_developer_platform_and_tax_challans(db)
            db.commit()
        if not db.query(GeofenceZone).first():
            _seed_smart_attendance(db)
            db.commit()
        if not db.query(ProjectIntake).first():
            _seed_pmo_stage_gates(db)
            db.commit()
        if not db.query(SDLCRequirement).first():
            _seed_sdlc_devsecops(db)
            db.commit()
        if not db.query(SourcingCategory).first():
            _seed_strategic_procurement(db)
            db.commit()
        if not db.query(GuardrailRule).first():
            _seed_guardrails_and_architectures(db)
            db.commit()
        if not db.query(AIModelEndpoint).first():
            _seed_ai_and_cloud_infrastructure(db)
            db.commit()
        if not db.query(ISOCertificationMaster).first():
            _seed_iso_standards_and_grievances(db)
            db.commit()
        if not db.query(PasskeyCredential).first():
            _seed_passkeys_and_zerotrust(db)
            db.commit()
        if not db.query(ThreatIntelIndicator).first():
            _seed_cybersecurity_warroom(db)
            db.commit()
        if db.query(PurchaseOrder).count() == 0 or db.query(APBill).count() <= 1:
            _seed_purchase_orders_and_bills(db)
            db.commit()
        if db.query(Candidate).count() == 0 or db.query(SeparationClearance).count() == 0:
            _seed_hrms_records(db)
            db.commit()
        if not db.query(ChatChannel).first():
            _seed_communications_and_teams(db)
            db.commit()
        if not db.query(SharePointArticle).first():
            _seed_sharepoint_and_knowledge(db)
            db.commit()
        if not db.query(TrainingTrack).first():
            _seed_training_academy(db)
            db.commit()
        if not db.query(TrainingMaterial).first():
            _seed_training_materials(db)
            db.commit()
        if not db.query(ConfigurationItem).first():
            _seed_itsm_comprehensive(db)
            db.commit()
        if db.query(ProjectMilestone).count() == 0 or not db.query(CustomerAccount).filter(CustomerAccount.client_name == "Zenith Global Corp").first():
            _seed_client_portal_comprehensive(db)
            db.commit()
        if not db.query(EnterpriseAgent).first():
            _seed_agentic_ai(db)
            db.commit()
        if not db.query(EnterpriseEventLedger).first():
            _seed_enterprise_operations(db)
            db.commit()
        db.close()
        return
        
    print("[Seeder] Initializing Asperion Enterprise Database with Complete Operational Records...")
    
    # 1. Corporate Entity Master
    entity = EntityMaster(
        entity_name="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        cin="U85500KA2026OPC222069",
        incorporation_date=date(2026, 6, 10),
        registered_office="Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India",
        pan="AAACA1234D",
        tan="BLRA12345D",
        gstin="29AAACA1234D1Z5",
        sole_member_director="Varadi Vijay",
        authorized_capital=100000.0,
        paid_up_capital=100000.0,
        udyam_reg_number="UDYAM-KR-03-0189422",
        dpiit_recognition_number="DIPP142089",
        duns_number="65-102-9481",
        registered_property_owner="Varadi Vijay (NOC & Electricity Consent on Record)",
        status="Active"
    )
    db.add(entity)
    
    # 2. Board Resolutions
    resolutions = [
        BoardResolution(
            resolution_number="ADT/RES/2026/001",
            title="Opening of Current Bank Account with ICICI Bank Ltd",
            resolution_type="OPC Member Resolution",
            date_passed=date(2026, 6, 12),
            subject_category="Banking Operations",
            resolution_text="RESOLVED THAT a current bank account be opened in the name of ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED with ICICI Bank Ltd, Bangalore Branch, and Mr. Varadi Vijay, Sole Director, be authorized to singly operate the said account.",
            authorized_signatory="Varadi Vijay",
            status="Passed & Recorded"
        ),
        BoardResolution(
            resolution_number="ADT/RES/2026/002",
            title="Adoption of Corporate Governance & Security Policy Framework",
            resolution_type="OPC Member Resolution",
            date_passed=date(2026, 6, 15),
            subject_category="Corporate Governance",
            resolution_text="RESOLVED THAT the Code of Conduct, POSH Policy, IT/AI/Cybersecurity Policy, and DPDP Compliance Framework as placed before the meeting be and are hereby formally approved and adopted.",
            authorized_signatory="Varadi Vijay",
            status="Passed & Recorded"
        )
    ]
    db.add_all(resolutions)
    
    # 3. Compliance Calendar
    compliances = [
        ComplianceCalendarItem(
            compliance_name="GST Monthly Return (GSTR-1)",
            statutory_authority="GST Portal (CBIC)",
            form_or_return="GSTR-1",
            due_date=date(2026, 7, 11),
            frequency="Monthly",
            owner="Finance Lead",
            status="Upcoming",
            penalty_risk="High"
        ),
        ComplianceCalendarItem(
            compliance_name="GST Monthly Summary (GSTR-3B)",
            statutory_authority="GST Portal (CBIC)",
            form_or_return="GSTR-3B",
            due_date=date(2026, 7, 20),
            frequency="Monthly",
            owner="Finance Lead",
            status="Upcoming",
            penalty_risk="High"
        ),
        ComplianceCalendarItem(
            compliance_name="Monthly TDS Deposit",
            statutory_authority="Income Tax Department",
            form_or_return="Challan ITNS 281",
            due_date=date(2026, 7, 7),
            frequency="Monthly",
            owner="Finance Lead",
            status="Upcoming",
            penalty_risk="Critical"
        ),
        ComplianceCalendarItem(
            compliance_name="Karnataka Professional Tax Monthly Remittance",
            statutory_authority="Karnataka Commercial Taxes Dept",
            form_or_return="Form 5-A / e-Payment",
            due_date=date(2026, 7, 20),
            frequency="Monthly",
            owner="HR & Payroll Lead",
            status="Upcoming",
            penalty_risk="Medium"
        ),
        ComplianceCalendarItem(
            compliance_name="MCA Annual Return for OPC",
            statutory_authority="Ministry of Corporate Affairs (ROC Bangalore)",
            form_or_return="MGT-7A",
            due_date=date(2026, 11, 28),
            frequency="Annual",
            owner="Company Secretary / Director",
            status="Upcoming",
            penalty_risk="Critical"
        )
    ]
    db.add_all(compliances)
    
    # 4. Policies Directory
    policies = [
        PolicyRecord(policy_code="POL-HR-01", policy_name="Code of Conduct & Business Ethics", category="HR & Ethics", effective_date=date(2026, 6, 15), description="Core standards of integrity, conflict of interest, and anti-bribery."),
        PolicyRecord(policy_code="POL-SEC-01", policy_name="IT, AI, Cybersecurity & Data Governance", category="Cybersecurity", effective_date=date(2026, 6, 15), description="Cloud security, passkeys, MFA, and acceptable use of AI LLM tools."),
        PolicyRecord(policy_code="POL-DPDP-01", policy_name="DPDP & Privacy Operations Policy", category="Data Privacy", effective_date=date(2026, 6, 15), description="Compliance with Digital Personal Data Protection Act 2023."),
        PolicyRecord(policy_code="POL-POSH-01", policy_name="Prevention of Sexual Harassment (POSH) Policy", category="HR & Ethics", effective_date=date(2026, 6, 15), description="Zero tolerance workplace harassment redressal framework.")
    ]
    db.add_all(policies)

    # 5. Chart of Accounts
    accounts = [
        AccountMaster(account_code="1001", account_group="Asset", account_name="ICICI Bank - Main Current Account", normal_balance="Debit", cost_center="Treasury"),
        AccountMaster(account_code="1010", account_group="Asset", account_name="Accounts Receivable (Trade Debtors)", normal_balance="Debit", cost_center="Sales"),
        AccountMaster(account_code="1020", account_group="Asset", account_name="Input GST Credit (CGST + SGST + IGST)", normal_balance="Debit", cost_center="Taxation"),
        AccountMaster(account_code="1100", account_group="Asset", account_name="Fixed Assets - Laptops & Hardware", normal_balance="Debit", cost_center="IT"),
        AccountMaster(account_code="2001", account_group="Liability", account_name="Accounts Payable (Trade Creditors)", normal_balance="Credit", cost_center="Procurement"),
        AccountMaster(account_code="2010", account_group="Liability", account_name="Duties & Taxes Payable (TDS u/s 194J/C)", normal_balance="Credit", cost_center="Taxation"),
        AccountMaster(account_code="2020", account_group="Liability", account_name="Salaries & Gratuity Payable", normal_balance="Credit", cost_center="HR"),
        AccountMaster(account_code="3001", account_group="Equity", account_name="Share Capital (Paid-up)", normal_balance="Credit", cost_center="Corporate"),
        AccountMaster(account_code="4001", account_group="Revenue", account_name="Software Development & Consulting Revenue", normal_balance="Credit", cost_center="Delivery"),
        AccountMaster(account_code="5001", account_group="Expense", account_name="Employee Salaries & Benefits", normal_balance="Debit", cost_center="HR"),
        AccountMaster(account_code="5010", account_group="Expense", account_name="Cloud Hosting & AWS Services", normal_balance="Debit", cost_center="DevOps"),
        AccountMaster(account_code="5020", account_group="Expense", account_name="Legal, CS & Professional Fees", normal_balance="Debit", cost_center="Admin")
    ]
    db.add_all(accounts)
    
    # 6. CRM Prospects & Contracts
    prospect = Prospect(
        company_name="Helios Cloud Technologies Pvt Ltd",
        contact_person="Ramesh K.",
        contact_email="ramesh@helioscloud.io",
        contact_phone="+91-9880011223",
        industry="Enterprise SaaS",
        pipeline_stage="Proposal Sent",
        deal_value=2400000.0,
        owner="Sales Lead",
        notes="Enterprise AI workflow automation platform design and full-stack implementation."
    )
    db.add(prospect)
    db.flush()
    
    contract = ClientContract(
        contract_reference="ADT/MSA/2026/001",
        prospect_id=prospect.id,
        client_name="Helios Cloud Technologies Pvt Ltd",
        contract_type="Master Services Agreement (MSA)",
        effective_date=date(2026, 6, 20),
        expiry_date=date(2027, 6, 19),
        value_inr=2400000.0,
        status="Fully Executed",
        stamp_duty_paid=True
    )
    db.add(contract)
    
    # 7. Invoices & AP Bills
    invoice = Invoice(
        invoice_number="ADT/INV/2026/0001",
        invoice_date=date(2026, 6, 25),
        due_date=date(2026, 7, 25),
        customer_name="Helios Cloud Technologies Pvt Ltd",
        customer_gstin="29AABCH1234D1Z2",
        taxable_value=600000.0,
        is_interstate=False,
        cgst_amount=54000.0,
        sgst_amount=54000.0,
        igst_amount=0.0,
        total_tax=108000.0,
        total_invoice_value=708000.0,
        amount_received=708000.0,
        outstanding_balance=0.0,
        status="Paid",
        payment_terms="Net 30 Days"
    )
    db.add(invoice)
    
    ap_bill = APBill(
        bill_number="INV-AWS-882910",
        bill_date=date(2026, 6, 30),
        due_date=date(2026, 7, 15),
        vendor_name="Amazon Web Services (AWS)",
        expense_category="Cloud Hosting & Infrastructure",
        taxable_amount=45000.0,
        gst_amount=8100.0,
        tds_section="194J",
        tds_rate=0.02,
        tds_amount=900.0,
        net_payable=52200.0,
        three_way_match_status="Matched",
        approval_status="Approved"
    )
    db.add(ap_bill)

    # 8. Expense Claims & Bank Reconciliation
    claim = ExpenseClaim(
        claim_id="ADT-EXP-001",
        claim_date=date(2026, 6, 28),
        claimant_name="Arjun Sharma",
        claimant_email="arjun.sharma@asperion.in",
        category="Broadband / Remote Work",
        business_purpose="High-speed fiber connectivity for production cloud deployment",
        amount_inr=2499.0,
        gst_paid=449.82,
        status="Approved"
    )
    db.add(claim)

    bank_rec = BankReconciliationRecord(
        reconciliation_month="JUN-2026",
        statement_closing_balance=855800.0,
        ledger_closing_balance=855800.0,
        uncredited_deposits=0.0,
        unpresented_cheques=0.0,
        adjusted_balance=855800.0,
        reconciled=True,
        reconciliation_date=date(2026, 6, 30)
    )
    db.add(bank_rec)

    budget = BudgetItem(
        cost_center="Product",
        account_category="Cloud Hosting & DevOps",
        annual_budget=600000.0,
        ytd_budget=150000.0,
        ytd_actual=124000.0,
        variance_inr=26000.0,
        variance_pct=17.33
    )
    db.add(budget)

    proj_pnl = ProjectPnL(
        project_code="ADT-PRJ-2026-001",
        project_name="Enterprise Workflow & AI Stack",
        client_name="Helios Cloud Technologies",
        contracted_revenue=2400000.0,
        recognized_revenue=600000.0,
        direct_labor_cost=180000.0,
        direct_cloud_infra_cost=45000.0,
        vendor_subcontractor_cost=0.0,
        total_delivery_cost=225000.0,
        gross_margin_inr=375000.0,
        gross_margin_pct=62.5
    )
    db.add(proj_pnl)

    # 9. HRMS Employees & Salary Structures
    employees_seed = [
        ("ADT-EMP-001", "Arjun Sharma", "arjun.sharma@asperion.in", "Lead Full-Stack Architect", "Engineering", 1500000.0),
        ("ADT-EMP-002", "Priya Nair", "priya.nair@asperion.in", "Senior DevOps & Cloud Security Engineer", "Engineering", 1350000.0),
        ("ADT-EMP-003", "Vikram Rathore", "vikram.rathore@asperion.in", "Product Manager", "Product", 1400000.0),
        ("ADT-EMP-004", "Sneha Rao", "sneha.rao@asperion.in", "Frontend UI/UX Specialist", "Engineering", 1100000.0)
    ]

    for code, name, email, role, dept, ctc_val in employees_seed:
        emp = Employee(
            emp_code=code,
            full_name=name,
            official_email=email,
            phone="+91-9876543210",
            designation=role,
            department=dept,
            employment_type="Full-Time",
            date_of_joining=date(2026, 6, 15),
            probation_status="Confirmed",
            work_location="Bangalore",
            employment_status="Active",
            # GPS Geolocation & Perimeter
            latitude=13.035820,
            longitude=77.653410,
            geofence_radius_meters=200.0,
            geofence_enforced=True,
            work_location_type="HQ Office",
            # Webcam & Biometric Facial Recognition
            webcam_registered_face_url=f"/static/img/avatars/{code.lower()}.png",
            facial_enrollment_status="Enrolled",
            webcam_hardware_device="Logitech Brio 4K / Integrated HD Webcam",
            facial_liveness_score=98.8,
            last_biometric_verification_at=datetime.utcnow(),
            # Personal, Emergency & Address
            blood_group="O+" if "001" in code or "003" in code else "B+",
            emergency_contact_name="Family Contact",
            emergency_contact_phone="+91-9876543210",
            residential_address="Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka"
        )
        db.add(emp)
        db.flush()

        breakup = compute_salary_breakup(ctc_val)
        e = breakup["earnings"]
        em = breakup["employer_contributions"]
        ed = breakup["employee_deductions"]
        th = breakup["take_home"]

        sal = SalaryStructure(
            employee_id=emp.id,
            annual_ctc=ctc_val,
            monthly_ctc=breakup["monthly_ctc"],
            basic_salary=e["basic_salary"]["monthly"],
            hra=e["hra"]["monthly"],
            special_allowance=e["special_allowance"]["monthly"],
            gross_salary=e["gross_salary"]["monthly"],
            employer_pf=em["employer_pf"]["monthly"],
            employer_esi=0.0,
            gratuity_provision=em["gratuity_provision"]["monthly"],
            employee_pf=ed["employee_pf"]["monthly"],
            employee_esi=0.0,
            professional_tax=ed["professional_tax"]["monthly"],
            estimated_tds=3500.0,
            total_deductions=ed["total_deductions"]["monthly"] + 3500.0,
            net_in_hand=th["monthly_net_in_hand"] - 3500.0,
            effective_from=date(2026, 6, 15),
            is_active=True
        )
        db.add(sal)

    # 10. Leaves & POSH
    leave = LeaveRecord(
        employee_id=1,
        employee_name="Arjun Sharma",
        leave_type="Casual Leave",
        start_date=date(2026, 7, 3),
        end_date=date(2026, 7, 4),
        total_days=2.0,
        reason="Family event",
        status="Approved"
    )
    db.add(leave)

    posh = POSHCase(
        case_reference="ADT-POSH-2026-001",
        date_filed=date(2026, 6, 20),
        nature_of_complaint="Inappropriate workplace messaging inquiry",
        inquiry_status="Concluded",
        interim_relief_granted=True,
        statutory_90_day_deadline=date(2026, 9, 18),
        recommendations_summary="Counselling and formal written warning issued; zero tolerance reaffirmed.",
        action_taken="Warning letter HR-ER-08 delivered; training drill completed.",
        annual_report_disclosed=True
    )
    db.add(posh)

    # 11. PMO Project, Sprints & WBS
    project = Project(
        project_code="ADT-PRJ-2026-001",
        name="Enterprise Workflow & AI Stack",
        client_name="Helios Cloud Technologies",
        project_type="Client Delivery",
        sponsor="Varadi Vijay",
        project_manager="Vikram Rathore",
        technical_lead="Arjun Sharma",
        start_date=date(2026, 6, 20),
        target_end_date=date(2026, 12, 20),
        status="In Progress",
        priority="Critical",
        budget_inr=2400000.0,
        actual_spent_inr=520000.0,
        estimated_effort_days=180.0,
        actual_effort_days=45.0
    )
    db.add(project)
    db.flush()

    sprint = Sprint(
        project_id=project.id,
        sprint_name="Sprint 1 - Core Foundations",
        start_date=date(2026, 6, 20),
        end_date=date(2026, 7, 4),
        goal="Deliver core statutory payroll, tax engine, and initial SecOps war-room",
        committed_story_points=40,
        completed_story_points=38,
        velocity=38.0,
        status="Active"
    )
    db.add(sprint)

    tasks = [
        WBSTask(project_id=project.id, wbs_code="1.1", task_name="Architecture & API Blueprinting", assigned_to="Arjun Sharma", sprint_phase="Sprint 1", status="Done"),
        WBSTask(project_id=project.id, wbs_code="1.2", task_name="Statutory Payroll & CTC Engine Core", assigned_to="Arjun Sharma", sprint_phase="Sprint 1", status="Done"),
        WBSTask(project_id=project.id, wbs_code="1.3", task_name="Frontend High-Density ERP Workspace", assigned_to="Sneha Rao", sprint_phase="Sprint 1", status="In Progress"),
        WBSTask(project_id=project.id, wbs_code="2.1", task_name="SecOps & CERT-In Compliance War Room", assigned_to="Priya Nair", sprint_phase="Sprint 1", status="In Progress"),
        WBSTask(project_id=project.id, wbs_code="2.2", task_name="3-Way Matching AP Engine", assigned_to="Arjun Sharma", sprint_phase="Sprint 1", status="To Do")
    ]
    db.add_all(tasks)

    stakeholder = Stakeholder(
        project_id=project.id,
        name="Ramesh K.",
        organization="Helios Cloud Technologies",
        role_in_project="Client Product Sponsor",
        influence_level="High",
        interest_level="High",
        communication_frequency="Bi-weekly Sprint Review"
    )
    db.add(stakeholder)

    # 11b. Globally Acknowledged PMO Processes & Stage-Gates (PMBOK / PRINCE2 / ISO 21500)
    intakes = [
        ProjectIntake(
            intake_code="ADT-INTK-2026-001",
            project_name="Enterprise Workflow & AI Stack",
            sponsor="Varadi Vijay (Sole Director)",
            client_or_internal="Zenith Global Corp",
            strategic_fit="Critical",
            expected_value="Core SaaS revenue, ISO 27001 automation & high client retention",
            target_start_date=date(2026, 6, 20),
            estimated_budget_inr=2400000.0,
            intake_status="Approved to Charter",
            approval_date=date(2026, 6, 18),
            approved_by="Varadi Vijay (Director)"
        ),
        ProjectIntake(
            intake_code="ADT-INTK-2026-002",
            project_name="Autonomous Multi-Model Cloud FinOps",
            sponsor="Finance Head",
            client_or_internal="Internal R&D Platform",
            strategic_fit="High",
            expected_value="35% AWS cloud cost reduction & auto-scaling optimizations",
            target_start_date=date(2026, 8, 1),
            estimated_budget_inr=850000.0,
            intake_status="Under Evaluation",
            approval_date=None,
            approved_by=None
        )
    ]
    db.add_all(intakes)

    charter = ProjectCharter(
        project_id=project.id,
        charter_code="ADT-CHTR-2026-001",
        problem_statement="Legacy client workflows lack automated statutory payroll compliance, real-time geofenced attendance, and CERT-In 6-hour security reporting.",
        business_case="Modernize enterprise operational architecture into an integrated, ISO 27001 and DPDP-compliant multi-tenant SaaS cockpit.",
        measurable_success_criteria="99.9% uptime, <1h P1 incident containment, zero non-compliance penalties on PF/PT, and 100% 3-way matching accuracy.",
        scope_included="18 integrated operating modules, automated self-healing daemon, biometric facial attendance, and dedicated stakeholder portals.",
        scope_excluded="Hardware on-premises infrastructure assembly and non-standard legacy ERP physical tape backups.",
        assumptions_summary="AWS cloud availability at 99.99% and prompt statutory portal (MCA/GSTN/EPFO) API response.",
        constraints_summary="Fixed budget INR 24 Lakhs and strict 6-month delivery deadline (20 Dec 2026).",
        governance_cadence="Weekly SteerCo, Daily 15-min Standup, Bi-weekly Sprint Retrospectives",
        signoff_status="Approved & Baselined",
        signed_off_by="Varadi Vijay (Sole Director)",
        signoff_date=date(2026, 6, 19)
    )
    db.add(charter)

    actions_decisions = [
        ActionDecisionItem(
            project_id=project.id,
            item_type="Action",
            source_meeting="SteerCo Review #03",
            title_or_decision="Lock AWS GovCloud and Mumbai Region VPC Peering architecture",
            rationale_or_context="Necessary to satisfy DPDP Act 2023 residency requirements for enterprise banking clients.",
            owner="Vikram Rathore",
            due_date=date(2026, 7, 10),
            status="In Progress",
            recorded_date=date(2026, 6, 25)
        ),
        ActionDecisionItem(
            project_id=project.id,
            item_type="Decision",
            source_meeting="Architecture Review Board",
            title_or_decision="Adopt FastAPI + SQLite WAL Mode with SQLAlchemy 2.0 ORM for core stack",
            rationale_or_context="Guarantees sub-10ms response times, zero database locks, and deterministic microsecond test execution.",
            owner="Varadi Vijay (Director)",
            due_date=date(2026, 6, 20),
            status="Implemented",
            recorded_date=date(2026, 6, 20)
        ),
        ActionDecisionItem(
            project_id=project.id,
            item_type="Action",
            source_meeting="Daily Standup",
            title_or_decision="Execute automated 3-way AP matching for AWS and Nexus hardware bills",
            rationale_or_context="Prevent unauthorized invoices and enforce Chapter XVII-B TDS deduction prior to payout.",
            owner="Arjun Sharma",
            due_date=date(2026, 7, 5),
            status="Closed",
            recorded_date=date(2026, 6, 28)
        )
    ]
    db.add_all(actions_decisions)

    capacity_plans = [
        CapacityPlanItem(
            project_id=project.id,
            role_title="Project Manager & Scrum Master",
            person_or_vendor="Vikram Rathore",
            skill_area="PMO, Agile Scrum & Stakeholder Governance",
            required_hours=80.0,
            available_hours=80.0,
            utilization_pct=100.0,
            variance_hours=0.0,
            status="Balanced"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="Lead Full-Stack Architect",
            person_or_vendor="Arjun Sharma",
            skill_area="Python FastAPI, SQLite WAL, Tailwind & React/Vue",
            required_hours=130.0,
            available_hours=120.0,
            utilization_pct=108.3,
            variance_hours=-10.0,
            status="Constrained / Overallocated"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="Lead QA & UAT Engineer",
            person_or_vendor="Sneha Rao",
            skill_area="Automated PyTest, Playwright & Manual UAT Test Cases",
            required_hours=75.0,
            available_hours=80.0,
            utilization_pct=93.8,
            variance_hours=5.0,
            status="Balanced"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="SecOps & Compliance Specialist",
            person_or_vendor="Priya Nair",
            skill_area="ISO 27001 A.8, CERT-In Triage & NIST SP 800-61",
            required_hours=60.0,
            available_hours=70.0,
            utilization_pct=85.7,
            variance_hours=10.0,
            status="Surplus Capacity"
        )
    ]
    db.add_all(capacity_plans)

    quality_uats = [
        QualityUATItem(
            project_id=project.id,
            deliverable_name="Core Statutory CTC Calculator & Payroll Engine",
            test_or_review_type="Internal QA & Statutory Audit",
            acceptance_criteria="EPFO 12% ceiling ₹15k, Karnataka PT ₹200, and Net Salary balancing down to ₹0.01.",
            test_lead="Sneha Rao",
            client_reviewer="Finance & Audit Team",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 25),
            evidence_notes="Verified against Karnataka PT Act 1976 and Employees Provident Funds Act 1952."
        ),
        QualityUATItem(
            project_id=project.id,
            deliverable_name="Smart Attendance Biometric & Haversine Geofence",
            test_or_review_type="Client UAT",
            acceptance_criteria="Haversine distance within 250m of Horamavu Bangalore HQ (13.035820, 77.653410) & 3D facial liveness >95%.",
            test_lead="Arjun Sharma",
            client_reviewer="Ramesh K. (Client Sponsor)",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 27),
            evidence_notes="Live mobile and desktop check-in tests passed across 5 enrolled employees."
        ),
        QualityUATItem(
            project_id=project.id,
            deliverable_name="CERT-In 6-Hour Security Incident Triage & War Room",
            test_or_review_type="Security & Penetration Scan",
            acceptance_criteria="P1 triage and formatted CERT-In reporting document generated within 360 minutes with SHA-256 evidence chain.",
            test_lead="Priya Nair",
            client_reviewer="CISO Office",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 28),
            evidence_notes="Playbooks verified against Cert-In Guidelines issued under IT Act Section 70B."
        )
    ]
    db.add_all(quality_uats)

    closures = [
        ProjectClosureItem(
            project_id=project.id,
            closure_area="Milestone 1 Deliverables Accepted",
            description="Phase 1 MVP architecture, CTC payroll, and SecOps war room formal handover.",
            evidence_signoff="Client Milestone Acceptance Certificate #ADT-MAC-001",
            owner="Vikram Rathore",
            closure_status="Completed",
            lessons_learned_summary="Adopting automated test suites and pre-seeded templates reduced delivery cycle from 6 weeks to 10 days.",
            completed_date=date(2026, 6, 30)
        ),
        ProjectClosureItem(
            project_id=project.id,
            closure_area="Financial Milestone Billing Settled",
            description="Invoicing and bank remittance reconciliation for Sprint 1 milestone payment.",
            evidence_signoff="Commercial Invoice ADT/INV/2026/0001 (INR 7,08,000 Paid)",
            owner="Finance Head",
            closure_status="Completed",
            lessons_learned_summary="Linking milestone payment criteria directly to UAT pass signoffs accelerated client cash receipt to under 5 days.",
            completed_date=date(2026, 7, 2)
        )
    ]
    db.add_all(closures)

    # 12. Procurement & RFP Comparisons
    vendor1 = Vendor(
        vendor_code="ADT-VEN-001",
        vendor_name="Amazon Web Services India Pvt Ltd",
        contact_person="AWS Enterprise Support",
        email="aws-support@amazon.com",
        category="Cloud & Infrastructure",
        criticality_tier="Tier 1 - Mission Critical",
        pan="AABCA1234D",
        gstin="29AABCA1234D1Z1",
        kyc_status="Approved",
        dpdp_compliance_status="Compliant",
        annual_spend_estimate=600000.0,
        payment_terms_days=30
    )
    db.add(vendor1)
    db.flush()

    rfp = RFPComparison(
        rfp_reference="ADT-RFP-2026-001",
        item_title="Managed Kubernetes Infrastructure & Object Storage",
        category="Cloud Hosting",
        vendor_a_name="AWS EKS & S3",
        vendor_a_quote=48000.0,
        vendor_b_name="Google Cloud GKE",
        vendor_b_quote=52000.0,
        vendor_c_name="Microsoft Azure AKS",
        vendor_c_quote=55000.0,
        selected_vendor="AWS EKS & S3",
        commercial_justification="Superior Mumbai region latency (ap-south-1), comprehensive IAM role federation, and existing reserved instances."
    )
    db.add(rfp)

    risk_assess = VendorRiskAssessment(
        vendor_id=vendor1.id,
        data_access_level="PII & Confidential",
        dpdp_dpa_signed=True,
        iso27001_certified=True,
        soc2_type2_attestation=True,
        cross_border_data_transfer=False,
        subprocessor_disclosure_verified=True,
        residual_risk_level="Low",
        review_date=date(2026, 6, 15)
    )
    db.add(risk_assess)

    # 13. IT Assets, Certificates & Provisioning
    it_asset = ITAsset(
        asset_tag="ADT-LAP-001",
        asset_type="Laptop",
        make_model="Apple MacBook Pro M3 (16GB/512GB)",
        serial_number="C02G1234MD6R",
        assigned_to_email="arjun.sharma@asperion.in",
        assigned_user_name="Arjun Sharma",
        os_version="macOS Sonoma 14.5",
        disk_encryption_enabled=True,
        edr_antivirus_installed=True,
        purchase_date=date(2026, 6, 12),
        warranty_expiry_date=date(2029, 6, 11),
        asset_status="Assigned"
    )
    cloud_acc = CloudAccount(
        cloud_id="ADT-AWS-PROD",
        provider="AWS",
        account_subscription_id="123456789012",
        environment="Production",
        primary_region="ap-south-1 (Mumbai)",
        technical_owner="Priya Nair",
        monthly_budget_inr=50000.0,
        current_month_spend_inr=32400.0,
        mfa_enforced_root=True,
        backup_enabled=True,
        status="Active"
    )
    cert = CertificateSecret(
        item_type="SSL/TLS Certificate",
        identifier_name="*.asperion.in Wildcard SAN",
        environment="Production",
        issuer="Let's Encrypt Authority X3",
        expiry_date=date(2026, 9, 15),
        auto_renew_enabled=True,
        alert_lead_time_days=30,
        status="Active"
    )
    chk = ITProvisioningChecklist(
        employee_code="ADT-EMP-001",
        employee_name="Arjun Sharma",
        process_type="Onboarding",
        google_workspace_provisioned=True,
        github_org_access_granted=True,
        aws_iam_identity_center_granted=True,
        hardware_laptop_issued=True,
        fido2_passkey_enrolled=True,
        vpn_network_access_granted=True,
        security_awareness_completed=True,
        signoff_status="Completed",
        completed_date=date(2026, 6, 15)
    )
    db.add_all([it_asset, cloud_acc, cert, chk])

    # 14. SecOps Incidents & Drills
    incident = SecurityIncident(
        incident_id="ADT-SEC-2026-001",
        title="Simulated AWS Root Account API Key Rotation & Anomaly Drill",
        category="Credential Compromise Simulation",
        severity="P2-High",
        status="Contained",
        incident_commander="Priya Nair",
        affected_systems="AWS IAM / CloudTrail",
        data_classification_impacted="Confidential",
        reported_at=datetime.utcnow() - timedelta(hours=2),
        cert_in_reporting_required=True,
        cert_in_deadline=datetime.utcnow() + timedelta(hours=4),
        cert_in_status="Drafted",
        war_room_url="https://meet.google.com/asp-sec-warroom"
    )
    drill = TabletopDrill(
        drill_code="ADT-DRILL-2026-001",
        title="Simulated Ransomware Incident & CERT-In Reporting Drill",
        drill_date=date(2026, 6, 18),
        scenario_type="Ransomware Host Isolation & S3 Glacier Restore",
        participants_roles="Founder, CISO Lead, DevOps Lead, Legal Counsel",
        target_containment_minutes=30,
        actual_containment_minutes=22,
        lessons_learned_summary="Isolation automation validated via AWS CLI STS token revocation script.",
        drill_rating="High Preparedness"
    )
    db.add_all([incident, drill])

    # 15. Immutable Enterprise Audit Logs
    audit_logs = [
        AuditLog(
            event_type="ENTITY_INCORPORATION",
            severity="INFO",
            actor=f"{settings.FOUNDER_DIRECTOR} (Sole Member)",
            module="GovOps",
            description="Company incorporation confirmed with MCA Bangalore. CIN U85500KA2026OPC222069 recorded.",
            created_at=datetime.utcnow() - timedelta(days=60)
        ),
        AuditLog(
            event_type="BANKING_MANDATE_PASSED",
            severity="INFO",
            actor="Board of Directors",
            module="GovOps",
            description="Board Resolution passed for HDFC Current Account operations.",
            created_at=datetime.utcnow() - timedelta(days=45)
        ),
        AuditLog(
            event_type="CLIENT_MSA_EXECUTED",
            severity="INFO",
            actor="Varadi Vijay (Director)",
            module="LegalOps",
            description="Master Services Agreement MSA-2026-001 signed with Nexus Fintech Solutions.",
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
        AuditLog(
            event_type="PAYROLL_AUTOMATION_INIT",
            severity="INFO",
            actor="System Engine",
            module="PeopleOps",
            description="Employee CTC structures verified against Karnataka PT & EPFO statutory rules.",
            created_at=datetime.utcnow() - timedelta(days=15)
        ),
        AuditLog(
            event_type="SECURITY_DRILL_EXECUTED",
            severity="WARNING",
            actor="SOC Team",
            module="SecOps",
            description="Tabletop ransomware drill executed. CERT-In 6-hour SLA reporting simulated.",
            created_at=datetime.utcnow() - timedelta(days=5)
        )
    ]
    db.add_all(audit_logs)

    # 16. Strategic Functions Matrix
    functions = [
        StrategicFunction(
            function_name="Leadership & Corporate Governance",
            function_owner="Founder / Sole Director",
            core_capabilities="Corporate strategy, board authorizations, MCA compliance, statutory oversight",
            key_documents="Governance Manual, OPC Records SOP",
            core_registers="Board Resolutions, Authority Matrix",
            review_cadence="Monthly",
            maturity_level="L2"
        ),
        StrategicFunction(
            function_name="Finance, Tax & Treasury",
            function_owner="Finance Lead",
            core_capabilities="Billing, GST/TDS compliance, 13-week cash flow, 3-way matching",
            key_documents="Finance Manual, Tax Guidelines",
            core_registers="COA, Invoice AR, AP Bills, Bank Reconciliation",
            review_cadence="Monthly",
            maturity_level="L2"
        ),
        StrategicFunction(
            function_name="People Operations & HRMS",
            function_owner="People Ops Lead",
            core_capabilities="Talent acquisition, statutory CTC calculator, 70+ lifecycle letters, payroll",
            key_documents="HR Handbook, POSH Policy",
            core_registers="Employee Master, Salary Structures, Leave Records",
            review_cadence="Monthly",
            maturity_level="L2"
        ),
        StrategicFunction(
            function_name="Engineering & AI Technology",
            function_owner="CTO / Tech Lead",
            core_capabilities="Full-stack software engineering, AI agentic models, cloud architecture",
            key_documents="Engineering Architecture, AI Model Register",
            core_registers="Code Repos, Architecture Blueprints, Passkeys",
            review_cadence="Weekly",
            maturity_level="L2"
        ),
        StrategicFunction(
            function_name="Cybersecurity & SOC Operations",
            function_owner="CISO / SecOps Lead",
            core_capabilities="Real-time triage, CERT-In 6h SLA compliance, DPDP data protection, playbooks",
            key_documents="Incident Response Policy, Playbook Library",
            core_registers="Security Incidents, SIEM Alerts, Evidence Locker",
            review_cadence="Weekly",
            maturity_level="L2"
        ),
        StrategicFunction(
            function_name="PMO & Project Delivery",
            function_owner="Delivery Lead",
            core_capabilities="Agile sprint management, WBS milestones, RACI matrix, RAID log governance",
            key_documents="Delivery SOP, Project Charters",
            core_registers="Project Master, WBS Tasks, Sprints, RAID Logs",
            review_cadence="Weekly",
            maturity_level="L2"
        )
    ]
    db.add_all(functions)

    # 17. Capability Constraints
    caps = [
        CapabilityCapacity(
            capability_name="Client Project Delivery",
            current_capacity="2 Active Production Sprints",
            target_capacity="5 Concurrent Enterprise Sprints",
            primary_constraint="Founder technical oversight dependency",
            people_requirement="2 Senior Full-Stack Engineers",
            tool_system_requirement="Automated CI/CD & Testing Pipeline",
            priority="Critical"
        ),
        CapabilityCapacity(
            capability_name="AI Agent Platform Governance",
            current_capacity="Ad-hoc Model Verification",
            target_capacity="Automated Safety & Benchmark Eval Suite",
            primary_constraint="Manual prompt and model validation",
            people_requirement="AI Evaluation Specialist",
            tool_system_requirement="Enterprise Model Registry",
            priority="High"
        ),
        CapabilityCapacity(
            capability_name="Finance Month-End Close",
            current_capacity="Day 12 Monthly Close",
            target_capacity="Day 5 Automated Flash Close",
            primary_constraint="Manual AP invoice collection and GRN sync",
            people_requirement="Finance Executive",
            tool_system_requirement="Automated 3-Way Reconciliation Engine",
            priority="High"
        )
    ]
    db.add_all(caps)

    # 18. Dynamic Enterprise KPIs
    kpis = [
        EnterpriseKPI(
            kpi_code="KPI-FIN-01",
            category="Financial",
            name="Monthly Invoiced Revenue",
            target_value=2000000.0,
            actual_value=2550000.0,
            unit="INR",
            period="JUN-2026",
            variance=550000.0,
            variance_pct=27.5,
            status="Achieved",
            owner="Finance Head",
            notes="Nexus Fintech milestone and monthly retainer billed."
        ),
        EnterpriseKPI(
            kpi_code="KPI-FIN-02",
            category="Financial",
            name="Days Sales Outstanding (DSO)",
            target_value=30.0,
            actual_value=22.0,
            unit="Days",
            period="JUN-2026",
            variance=-8.0,
            variance_pct=-26.7,
            status="Achieved",
            owner="Finance Head",
            notes="Collections received within prompt payment cycles."
        ),
        EnterpriseKPI(
            kpi_code="KPI-DEL-01",
            category="Delivery",
            name="Sprint Milestone On-Time Delivery",
            target_value=90.0,
            actual_value=94.0,
            unit="%",
            period="JUN-2026",
            variance=4.0,
            variance_pct=4.4,
            status="On Track",
            owner="PMO Lead",
            notes="Sprint 1 finished with zero critical blockers."
        ),
        EnterpriseKPI(
            kpi_code="KPI-SEC-01",
            category="Security",
            name="CERT-In Statutory SLA Compliance",
            target_value=100.0,
            actual_value=100.0,
            unit="%",
            period="JUN-2026",
            variance=0.0,
            variance_pct=0.0,
            status="Achieved",
            owner="CISO / SOC Lead",
            notes="All security drills and alerts triaged within statutory time limits."
        ),
        EnterpriseKPI(
            kpi_code="KPI-HR-01",
            category="People",
            name="Statutory Payroll Accuracy & On-Time Payout",
            target_value=100.0,
            actual_value=100.0,
            unit="%",
            period="JUN-2026",
            variance=0.0,
            variance_pct=0.0,
            status="Achieved",
            owner="People Ops Lead",
            notes="Zero payroll discrepancies across PF, PT, and TDS withholdings."
        )
    ]
    db.add_all(kpis)

    # 19. Strategic Thoughts & Executive Decisions
    thoughts = [
        StrategicDecisionThought(
            entry_type="Founder Thought / Thesis",
            title="Agentic Full-Stack Enterprise Automation & OPC Moat",
            author="Varadi Vijay (Sole Member & Founder)",
            date_recorded=date(2026, 6, 12),
            context_background="Traditional mid-sized IT consulting firms in Bangalore suffer from high administrative overhead, fragmented tooling, and manual compliance errors.",
            options_considered="A) Standard off-the-shelf SaaS stack (Zoho + Jira + QuickBooks) with recurring licensing; B) Unified bespoke software stack owned by Asperion.",
            decision_rationale="Building Asperion Enterprise OS directly embeds our exact statutory compliance rules, reduces operational drag to near zero, and serves as a flagship showcase for client deals.",
            approver="Varadi Vijay (Sole Director)",
            status="Approved",
            tags="Moat, Architecture, Vision"
        ),
        StrategicDecisionThought(
            entry_type="Strategic Decision",
            title="FIDO2 Passwordless Passkeys Mandate Across All Corporate Cloud Accounts",
            author="Varadi Vijay (Sole Member & Founder)",
            date_recorded=date(2026, 6, 15),
            context_background="Credential theft and phishing remain the top initial attack vectors under CERT-In advisories.",
            options_considered="A) SMS OTP (Vulnerable to SIM swap); B) Authenticator TOTP; C) Hardware FIDO2 Security Keys / Passkeys.",
            decision_rationale="Enforcing hardware-backed passkeys eliminates password stuffing and ensures 100% compliance with ISO 27001 Access Control mandates.",
            approver="Board of Directors",
            status="Approved",
            tags="SecOps, IAM, Zero-Trust"
        )
    ]
    db.add_all(thoughts)

    # 20. Implementation Roadmap
    roadmap = [
        ImplementationRoadmapItem(
            workstream="Technology",
            action_item="Deploy Asperion Enterprise OS v1.0 Unified Backend & Frontend",
            priority="Critical",
            owner="Tech Lead",
            start_date=date(2026, 6, 1),
            due_date=date(2026, 6, 30),
            progress_pct=100,
            status="Complete",
            notes="Full stack deployed with 8 operational modules and document vault."
        ),
        ImplementationRoadmapItem(
            workstream="Commercial",
            action_item="Execute Nexus Fintech Phase 2 SOW & Milestone Deliverables",
            priority="High",
            owner="Sales Lead",
            start_date=date(2026, 7, 1),
            due_date=date(2026, 8, 15),
            progress_pct=25,
            status="In Progress",
            notes="Commercial proposal approved by client deal desk."
        ),
        ImplementationRoadmapItem(
            workstream="Governance",
            action_item="File MCA Annual OPC Compliance AOC-4 and MGT-7A with ROC Bangalore",
            priority="Critical",
            owner="CS & Legal Counsel",
            start_date=date(2026, 9, 1),
            due_date=date(2026, 10, 30),
            progress_pct=0,
            status="Not Started",
            notes="Statutory filing scheduled with MCA portal."
        )
    ]
    db.add_all(roadmap)

    _seed_crm_erm(db)

    db.commit()
    db.close()
    print("[Seeder] Successfully populated Asperion Enterprise database.")

def _seed_crm_erm(db):
    if db.query(Opportunity).first():
        return

    # 21. Enterprise CRM Opportunities & Deals
    opps = [
        Opportunity(
            opportunity_code="ADT-OPP-2026-001",
            client_name="Nexus Fintech Solutions India Pvt Ltd",
            deal_title="Core Banking API Gateway & Microservices Platform",
            deal_value_inr=2400000.0,
            stage="Closed Won",
            probability_pct=100.0,
            weighted_value_inr=2400000.0,
            expected_close_date=date(2026, 6, 15),
            owner="Varadi Vijay (Director)",
            deal_type="New Business",
            deal_desk_status="Approved",
            discount_offered_pct=5.0,
            payment_terms="Net 30 Days",
            competitors="Infosys, ThoughtWorks",
            win_loss_reason="Superior architecture speed, direct founder commitment, and integrated compliance engine."
        ),
        Opportunity(
            opportunity_code="ADT-OPP-2026-002",
            client_name="Kavach Health Systems Pvt Ltd",
            deal_title="HIPAA/DPDP Compliant Patient Telehealth Cloud Infrastructure",
            deal_value_inr=1800000.0,
            stage="Legal/Deal Desk",
            probability_pct=80.0,
            weighted_value_inr=1440000.0,
            expected_close_date=date(2026, 7, 20),
            owner="Sales Lead",
            deal_type="New Business",
            deal_desk_status="Standard Terms Approved",
            discount_offered_pct=0.0,
            payment_terms="Net 30 Days",
            competitors="Wipro Health",
            win_loss_reason=None
        ),
        Opportunity(
            opportunity_code="ADT-OPP-2026-003",
            client_name="Zenith Retail Tech Bangalore",
            deal_title="Multi-Store Real-Time Inventory & POS Synchronizer",
            deal_value_inr=950000.0,
            stage="Solution Architecture",
            probability_pct=50.0,
            weighted_value_inr=475000.0,
            expected_close_date=date(2026, 8, 10),
            owner="Tech Lead",
            deal_type="New Business",
            deal_desk_status="Pending Architecture Review",
            discount_offered_pct=0.0,
            payment_terms="Milestone-based (30/40/30)",
            competitors="Shopify Plus Partner",
            win_loss_reason=None
        ),
        Opportunity(
            opportunity_code="ADT-OPP-2026-004",
            client_name="BlueSky Logistics Technologies",
            deal_title="Automated Fleet Telematics & IoT Processing Engine",
            deal_value_inr=1500000.0,
            stage="Discovery",
            probability_pct=25.0,
            weighted_value_inr=375000.0,
            expected_close_date=date(2026, 8, 30),
            owner="Sales Lead",
            deal_type="New Business",
            deal_desk_status="Standard Terms",
            discount_offered_pct=10.0,
            payment_terms="Net 30 Days",
            competitors="Locus, FarEye",
            win_loss_reason=None
        )
    ]
    db.add_all(opps)

    # 22. Customer Accounts & CS Health
    accounts = [
        CustomerAccount(
            account_code="ADT-ACC-001",
            client_name="Nexus Fintech Solutions India Pvt Ltd",
            tier="Tier 1 Enterprise",
            industry="Fintech & Digital Payments",
            primary_csm="Customer Success Lead",
            executive_sponsor="Varadi Vijay (Director)",
            annual_recurring_revenue_inr=2400000.0,
            health_score=98,
            health_status="Healthy",
            nps_score=10,
            contract_start_date=date(2026, 6, 15),
            renewal_date=date(2027, 6, 14),
            churn_risk_level="Low",
            notes="Flagship enterprise customer; core banking API integration live in production."
        ),
        CustomerAccount(
            account_code="ADT-ACC-002",
            client_name="Zenith Retail Tech Bangalore",
            tier="Tier 2 Mid-Market",
            industry="Retail & eCommerce SaaS",
            primary_csm="Customer Success Lead",
            executive_sponsor="Tech Lead",
            annual_recurring_revenue_inr=950000.0,
            health_score=92,
            health_status="Healthy",
            nps_score=9,
            contract_start_date=date(2026, 5, 1),
            renewal_date=date(2027, 4, 30),
            churn_risk_level="Low",
            notes="Active pilot expansion across 40 physical store locations in Karnataka."
        )
    ]
    db.add_all(accounts)

    # 23. CRM Activities & Touchpoints
    acts = [
        CRMActivity(
            activity_type="Technical Demo",
            subject="Microservices Scalability & Chaos Testing Demo",
            client_name="Kavach Health Systems Pvt Ltd",
            performed_by="Varadi Vijay (Director)",
            activity_date=date(2026, 6, 18),
            duration_minutes=60,
            key_takeaways="Demonstrated 10,000 req/sec latency benchmarks under sub-50ms SLA; CISO verified DPDP data residency in AWS Mumbai.",
            action_items="Share final Statement of Work (SOW) and security compliance attestation.",
            next_followup_date=date(2026, 6, 25)
        ),
        CRMActivity(
            activity_type="Deal Negotiation",
            subject="Commercial Terms & IP Ownership Review",
            client_name="Nexus Fintech Solutions India Pvt Ltd",
            performed_by="Varadi Vijay (Director)",
            activity_date=date(2026, 6, 10),
            duration_minutes=45,
            key_takeaways="Agreed on Net 30 payment terms, 5% volume concession, and milestone-linked billing signoffs.",
            action_items="Issue formal MSA and Master Statement of Work via Asperion Docx engine.",
            next_followup_date=date(2026, 6, 15)
        )
    ]
    db.add_all(acts)

    # 24. Support Tickets & Service Desk SLA
    tickets = [
        SupportTicket(
            ticket_number="ADT-SRV-2026-001",
            client_name="Nexus Fintech Solutions India Pvt Ltd",
            contact_email="devops@nexusfintech.in",
            subject="Webhook Delivery Retry Window Optimization",
            description="Request to increase webhook retry backoff from 3 to 5 attempts during third-party banking downtime.",
            category="Platform Feature",
            severity="P3-Medium",
            sla_response_hours=12.0,
            sla_deadline=datetime.utcnow() + timedelta(hours=10),
            assigned_engineer="Support Lead",
            status="Resolved",
            resolution_summary="Configured exponential backoff with jitter up to 5 retries; deployed to prod without downtime.",
            csat_rating=5,
            resolved_at=datetime.utcnow() - timedelta(hours=2)
        ),
        SupportTicket(
            ticket_number="ADT-SRV-2026-002",
            client_name="Zenith Retail Tech Bangalore",
            contact_email="it@zenithretail.com",
            subject="POS Sync Latency Spike Investigation",
            description="Intermittent 300ms latency spike observed during peak weekend trading hours.",
            category="Performance Latency",
            severity="P2-High",
            sla_response_hours=4.0,
            sla_deadline=datetime.utcnow() + timedelta(hours=3),
            assigned_engineer="Staff Cloud Engineer",
            status="Work in Progress",
            resolution_summary=None,
            csat_rating=None
        )
    ]
    db.add_all(tickets)

    # 25. Enterprise Risk Management (ERM) Register
    risks = [
        EnterpriseRisk(
            risk_code="ERM-2026-001",
            risk_category="Cybersecurity & Technological",
            risk_title="Ransomware or Supply Chain Dependency Vulnerability",
            risk_description="External threat actors targeting container repositories or dependencies causing unauthorized code execution.",
            inherent_severity=5,
            inherent_probability=3,
            inherent_rpn=15,
            existing_controls="Automated GitHub Dependabot scanning, FIDO2 passkeys enforced, immutable S3 backups, CERT-In 6-hour incident containment playbook.",
            residual_severity=2,
            residual_probability=1,
            residual_rpn=2,
            treatment_strategy="Mitigate",
            risk_owner="SecOps Lead / Director",
            review_cadence="Monthly",
            status="Controlled"
        ),
        EnterpriseRisk(
            risk_code="ERM-2026-002",
            risk_category="Financial & Liquidity",
            risk_title="Customer Payment Delay Exceeding 60 Days",
            risk_description="Enterprise client delayed disbursement impacting operating cashflow and working capital.",
            inherent_severity=4,
            inherent_probability=3,
            inherent_rpn=12,
            existing_controls="Mandatory 30% upfront milestone on signing, Net 30 payment terms, 13-week direct cash flow tracking, minimum 12 months treasury cash reserve.",
            residual_severity=2,
            residual_probability=1,
            residual_rpn=2,
            treatment_strategy="Mitigate",
            risk_owner="Finance Head / Director",
            review_cadence="Weekly",
            status="Controlled"
        ),
        EnterpriseRisk(
            risk_code="ERM-2026-003",
            risk_category="Compliance & Regulatory",
            risk_title="Statutory Non-Compliance with MCA / ROC / GST Filings",
            risk_description="Lapse in filing AOC-4, MGT-7A, GSTR-3B or TDS challans leading to director disqualification or penalties.",
            inherent_severity=5,
            inherent_probability=2,
            inherent_rpn=10,
            existing_controls="Asperion OS automated Compliance Calendar, dual alerts 15 days prior to due dates, corporate secretary retainer oversight.",
            residual_severity=1,
            residual_probability=1,
            residual_rpn=1,
            treatment_strategy="Avoid",
            risk_owner="Director (Sole Member)",
            review_cadence="Monthly",
            status="Controlled"
        )
    ]
    db.add_all(risks)
    _seed_internal_tickets_and_notifs(db)

def _seed_internal_tickets_and_notifs(db):
    if db.query(InternalTicket).filter(InternalTicket.subject == "New MacBook Pro M3 Max Developer Provisioning").first():
        return

    db.query(InternalTicket).delete()
    db.query(SystemNotification).delete()
    db.query(NotificationRule).delete()
    db.commit()

    # 26. Internal Cross-Departmental Service Desk Tickets
    internal_tickets = [
        InternalTicket(
            ticket_number="IT-TKT-2026-001",
            department="IT_INFRASTRUCTURE",
            category="Hardware Provisioning",
            subject="New MacBook Pro M3 Max Developer Provisioning",
            description="Procure and configure Apple Silicon workstation with BitLocker/FileVault and EDR agent for new joiner Sneha Rao.",
            priority="P2-High",
            status="Open",
            requester_name="Sneha Rao",
            requester_email="sneha.rao@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="Karthik N (IT Admin)",
            assigned_department="IT_INFRASTRUCTURE",
            sla_deadline_hours=8.0,
            target_resolution_at=datetime.utcnow() + timedelta(hours=6),
            comments_json='[{"author": "Sneha Rao", "message": "Ticket created for hardware provisioning.", "timestamp": "2026-11-18 10:00:00", "is_internal": false}]'
        ),
        InternalTicket(
            ticket_number="IT-TKT-2026-002",
            department="IT_INFRASTRUCTURE",
            category="VPN & Network Access",
            subject="AWS VPC Production VPN Gateway Tunnel Timeout",
            description="Intermittent packet loss on ap-south-1 production client VPN gateway impacting engineering deployment pipelines.",
            priority="P1-Critical",
            status="In Progress",
            requester_name="Ananya Sharma",
            requester_email="ananya.sharma@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="Cloud Architect",
            assigned_department="IT_INFRASTRUCTURE",
            sla_deadline_hours=2.0,
            target_resolution_at=datetime.utcnow() + timedelta(hours=1),
            comments_json='[{"author": "Cloud Architect", "message": "Investigating route table and MTU clamping on transit gateway.", "timestamp": "2026-11-18 11:30:00", "is_internal": true}]'
        ),
        InternalTicket(
            ticket_number="HR-TKT-2026-001",
            department="HR_PEOPLE",
            category="Payroll & Tax Discrepancy",
            subject="Form 16 Part B / Old vs New Tax Regime Query",
            description="Clarification on Section 87A rebate and standard deduction applicability under FY 2026-27 revised slabs.",
            priority="P3-Medium",
            status="Resolved",
            requester_name="Rahul Verma",
            requester_email="rahul.verma@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="People Ops Lead",
            assigned_department="HR_PEOPLE",
            sla_deadline_hours=24.0,
            target_resolution_at=datetime.utcnow() - timedelta(hours=12),
            resolved_at=datetime.utcnow() - timedelta(hours=8),
            resolution_summary="Explained 115BAC default regime nuances; employee opted into new tax regime on portal.",
            satisfaction_score=5,
            comments_json='[{"author": "People Ops Lead", "message": "Resolved with employee via 1:1 consultation.", "timestamp": "2026-11-17 14:00:00", "is_internal": false}]'
        ),
        InternalTicket(
            ticket_number="HR-TKT-2026-002",
            department="HR_PEOPLE",
            category="Leave Balance Adjustment",
            subject="Annual Earned Leave Carryover Discrepancy",
            description="Discrepancy in Q3 earned leave ledger carryover following compensatory off approval.",
            priority="P3-Medium",
            status="Open",
            requester_name="Sneha Rao",
            requester_email="sneha.rao@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="HR Generalist",
            assigned_department="HR_PEOPLE",
            sla_deadline_hours=24.0,
            target_resolution_at=datetime.utcnow() + timedelta(hours=18),
            comments_json='[{"author": "Sneha Rao", "message": "Submitted attendance logs for weekend deployment.", "timestamp": "2026-11-18 09:15:00", "is_internal": false}]'
        ),
        InternalTicket(
            ticket_number="FIN-TKT-2026-001",
            department="FINANCE_ACCOUNTS",
            category="Expense Reimbursement",
            subject="International Cloud Certification Exam Reimbursement Approval",
            description="AWS Solutions Architect Professional certification voucher reimbursement of INR 28,500 under L&D budget.",
            priority="P2-High",
            status="In Progress",
            requester_name="Ananya Sharma",
            requester_email="ananya.sharma@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="Finance Lead",
            assigned_department="FINANCE_ACCOUNTS",
            sla_deadline_hours=8.0,
            target_resolution_at=datetime.utcnow() + timedelta(hours=4),
            comments_json='[{"author": "Finance Lead", "message": "Receipt verified against ICICI credit card statement. Queued for payment batch.", "timestamp": "2026-11-18 10:45:00", "is_internal": true}]'
        ),
        InternalTicket(
            ticket_number="LEG-TKT-2026-001",
            department="LEGAL_COMPLIANCE",
            category="Contract Review & NDA",
            subject="Mutual Non-Disclosure Agreement Redline Review for US SaaS Client",
            description="Client legal counsel requested modification to clause 9 (Governing Law & Commercial Courts Bengaluru).",
            priority="P2-High",
            status="Resolved",
            requester_name="Varadi Vijay",
            requester_email="varadivijay@asperion.in",
            requester_department="GOVERNANCE",
            assigned_to="Legal Counsel",
            assigned_department="LEGAL_COMPLIANCE",
            sla_deadline_hours=8.0,
            target_resolution_at=datetime.utcnow() - timedelta(hours=4),
            resolved_at=datetime.utcnow() - timedelta(hours=2),
            resolution_summary="Agreed to Singapore International Arbitration Centre (SIAC) neutral fallback venue.",
            satisfaction_score=5,
            comments_json='[{"author": "Legal Counsel", "message": "Redline finalized and approved by Director.", "timestamp": "2026-11-18 12:00:00", "is_internal": false}]'
        ),
        InternalTicket(
            ticket_number="SEC-TKT-2026-001",
            department="SECOPS_CYBER",
            category="Phishing / Security Incident",
            subject="Suspicious Phishing Email Mimicking Bank Account Update",
            description="Targeted spear-phishing email received by payroll admin claiming to be from HDFC Corporate Banking.",
            priority="P1-Critical",
            status="Resolved",
            requester_name="People Ops Lead",
            requester_email="hr@asperion.in",
            requester_department="HR_PEOPLE",
            assigned_to="SOC Lead",
            assigned_department="SECOPS_CYBER",
            sla_deadline_hours=2.0,
            target_resolution_at=datetime.utcnow() - timedelta(hours=1),
            resolved_at=datetime.utcnow() - timedelta(minutes=45),
            resolution_summary="Domain blacklisted on DNS firewall, headers analyzed, no payload clicked, zero credential compromise.",
            satisfaction_score=5,
            comments_json='[{"author": "SOC Lead", "message": "IOCs pushed to AWS Network Firewall rules.", "timestamp": "2026-11-18 13:00:00", "is_internal": false}]'
        ),
        InternalTicket(
            ticket_number="PMO-TKT-2026-001",
            department="PMO_ENGINEERING",
            category="DevOps Pipeline",
            subject="Docker Container Build Cache Thrashing on Self-Hosted GitHub Runner",
            description="CI/CD test runner running out of ephemeral storage during multi-stage Docker build step.",
            priority="P2-High",
            status="In Progress",
            requester_name="Karthik N",
            requester_email="karthik.n@asperion.in",
            requester_department="PMO_ENGINEERING",
            assigned_to="DevOps Lead",
            assigned_department="PMO_ENGINEERING",
            sla_deadline_hours=8.0,
            target_resolution_at=datetime.utcnow() + timedelta(hours=5),
            comments_json='[{"author": "DevOps Lead", "message": "Provisioning 100GB EBS volume for buildkit persistent cache.", "timestamp": "2026-11-18 14:00:00", "is_internal": true}]'
        )
    ]
    db.add_all(internal_tickets)

    # 27. Cross-Group System Notifications & Alerts
    notifications = [
        SystemNotification(
            notification_code="NOTIF-2026-0001",
            module_source="CYBERSECURITY",
            title="CRITICAL Incident: INC-2026-001 - Ransomware Outbreak Triage",
            message="War room activated. Statutory CERT-In 6-hour reporting window active for AWS Prod VPC.",
            severity="CRITICAL",
            target_role="SECOPS_LEAD",
            is_read=False,
            is_dismissed=False,
            action_url="#view-secops",
            action_label="Open War Room",
            created_at=datetime.utcnow() - timedelta(minutes=40)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0002",
            module_source="TICKETING",
            title="P1 Service Desk Alert: IT-TKT-2026-002 (IT_INFRASTRUCTURE)",
            message="AWS VPC Production VPN Gateway Tunnel Timeout filed by Ananya Sharma. 2-hour SLA deadline active.",
            severity="CRITICAL",
            target_role="ALL",
            is_read=False,
            is_dismissed=False,
            action_url="#view-internal-support",
            action_label="Respond Ticket",
            created_at=datetime.utcnow() - timedelta(minutes=25)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0003",
            module_source="GOVERNANCE",
            title="Statutory Filing Due Soon: MCA-AOC4 (MCA / ROC Karnataka)",
            message="Form AOC-4 Financial Statements due on 2026-10-30. Mandatory annual compliance under Companies Act 2013.",
            severity="WARNING",
            target_role="DIRECTOR",
            is_read=False,
            is_dismissed=False,
            action_url="#view-governance",
            action_label="Review Compliance",
            created_at=datetime.utcnow() - timedelta(hours=3)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0004",
            module_source="FINANCE",
            title="Accounts Receivable Overdue: INV-2026-002 (Zenith Retail Tech Bangalore)",
            message="Outstanding balance INR 450,000.00 past Net 30 terms. Follow up required by Treasury.",
            severity="WARNING",
            target_role="FINANCE_HEAD",
            is_read=False,
            is_dismissed=False,
            action_url="#view-finance",
            action_label="View AR Ledger",
            created_at=datetime.utcnow() - timedelta(hours=6)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0005",
            module_source="CRM_LEGAL",
            title="Deal Desk Authorization Required: ADT-OPP-2026-002 (Kavach Health Systems)",
            message="Commercial proposal requests 18.0% discount on INR 1,800,000 enterprise deal. Director approval required.",
            severity="WARNING",
            target_role="DIRECTOR",
            is_read=False,
            is_dismissed=False,
            action_url="#view-crm",
            action_label="Review Deal Desk",
            created_at=datetime.utcnow() - timedelta(hours=8)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0006",
            module_source="INFRASTRUCTURE",
            title="AWS Cloud Spend Alert: Monthly Forecast Reaching 82% of Allocated Budget",
            message="Production RDS Multi-AZ storage scale-up increased monthly run-rate. Current spend INR 42,500 / INR 50,000 budget.",
            severity="INFO",
            target_role="TECH_LEAD",
            is_read=True,
            is_dismissed=False,
            action_url="#view-infrastructure",
            action_label="Inspect Cloud Spend",
            created_at=datetime.utcnow() - timedelta(days=1),
            read_at=datetime.utcnow() - timedelta(hours=12)
        ),
        SystemNotification(
            notification_code="NOTIF-2026-0007",
            module_source="HRMS",
            title="Monthly Payroll Run Complete for All 3 Full-Time Engineers",
            message="Gross INR 238,500.00 processed. Bank NEFT batch exported with EPFO/ESIC/PT statutory deductions.",
            severity="SUCCESS",
            target_role="HR_LEAD",
            is_read=True,
            is_dismissed=False,
            action_url="#view-hrms",
            action_label="View Payroll Run",
            created_at=datetime.utcnow() - timedelta(days=2),
            read_at=datetime.utcnow() - timedelta(days=1)
        )
    ]
    db.add_all(notifications)

    # 28. Cross-Functional Notification Rules
    notification_rules = [
        NotificationRule(
            rule_name="P1 Incident & Ticket Escalation",
            event_trigger="TICKET_P1_TRIGGER",
            department="IT_AND_SECOPS",
            severity="CRITICAL",
            channel="ALL",
            is_active=True
        ),
        NotificationRule(
            rule_name="CERT-In 6-Hour Countdown Alert",
            event_trigger="CERTIN_WAR_ROOM",
            department="SECOPS_CYBER",
            severity="CRITICAL",
            channel="ALL",
            is_active=True
        ),
        NotificationRule(
            rule_name="Statutory Compliance 15-Day Reminder",
            event_trigger="COMPLIANCE_DEADLINE_15D",
            department="LEGAL_COMPLIANCE",
            severity="WARNING",
            channel="IN_APP",
            is_active=True
        ),
        NotificationRule(
            rule_name="AR Invoice Overdue 30 Days",
            event_trigger="INVOICE_OVERDUE_30D",
            department="FINANCE_ACCOUNTS",
            severity="WARNING",
            channel="IN_APP",
            is_active=True
        ),
        NotificationRule(
            rule_name="Deal Desk Discount Guard (>15%)",
            event_trigger="DEAL_DESK_DISCOUNT_15PCT",
            department="CRM_LEGAL",
            severity="WARNING",
            channel="IN_APP",
            is_active=True
        )
    ]
    db.add_all(notification_rules)
    db.commit()
    _seed_developer_platform_and_tax_challans(db)

def _seed_developer_platform_and_tax_challans(db):
    if db.query(DeveloperPlatformAccount).first():
        return

    # 29. Developer Platform Accounts & Organization Publishing
    dev_accounts = [
        DeveloperPlatformAccount(
            account_code="DEV-ACC-001",
            platform_name="Google Play Console",
            account_type="Organization / Corporate Entity",
            admin_email="admin@asperion.in",
            organization_id="Google Org: Asperion Digital Technologies",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="Organization Developer Program",
            annual_fee_inr=2100.0,
            renewal_date=None, # One-time registration
            notes="Corporate account for publishing Asperion Android enterprise apps and microservice SDKs."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-002",
            platform_name="Apple Developer Program",
            account_type="Organization / Corporate Entity",
            admin_email="founder@asperion.in",
            organization_id="Team ID: 9X82ASPER",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="Apple Developer Enterprise",
            annual_fee_inr=8700.0,
            renewal_date=date(2027, 6, 14),
            notes="Corporate iOS, iPadOS and macOS distribution. Enforces biometric passkeys for all certs."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-003",
            platform_name="GitHub Organization",
            account_type="Organization / Corporate Entity",
            admin_email="devops@asperion.in",
            organization_id="github.com/asperion-digital",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="GitHub Enterprise Cloud",
            annual_fee_inr=19200.0,
            renewal_date=date(2027, 6, 10),
            notes="Branch protection rules, GPG commit signatures, IP allowlisting and self-hosted runners."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-004",
            platform_name="Microsoft Entra ID",
            account_type="Organization / Corporate Entity",
            admin_email="admin@asperion.in",
            organization_id="Tenant: asperiondigital.onmicrosoft.com",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="Microsoft Cloud Identity Premium",
            annual_fee_inr=14400.0,
            renewal_date=date(2027, 7, 1),
            notes="Single Sign-On (SSO) gateway, conditional access policies, and Azure AD integration."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-005",
            platform_name="Meta Business Suite",
            account_type="Organization / Corporate Entity",
            admin_email="founder@asperion.in",
            organization_id="Meta Biz ID: 1092837465019",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="WhatsApp Cloud API Enterprise",
            annual_fee_inr=0.0,
            renewal_date=None,
            notes="Verified corporate WhatsApp Cloud API for automated dispatch of invoices and critical alerts."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-006",
            platform_name="AWS Cloud Operations",
            account_type="Organization / Corporate Entity",
            admin_email="cloud-admin@asperion.in",
            organization_id="AWS Org: 123456789012 (ap-south-1)",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="AWS Business Support",
            annual_fee_inr=48000.0,
            renewal_date=date(2027, 5, 31),
            notes="Multi-AZ production VPC, GuardDuty SIEM, KMS envelope encryption and CloudTrail."
        ),
        DeveloperPlatformAccount(
            account_code="DEV-ACC-007",
            platform_name="OpenAI & Gemini AI Enterprise",
            account_type="Organization / Corporate Entity",
            admin_email="ai-lead@asperion.in",
            organization_id="Org: asperion-ai-labs",
            duns_linked=True,
            fido2_mfa_enforced=True,
            verification_status="Verified Organization",
            tier_or_plan="Enterprise Tier 4 API",
            annual_fee_inr=36000.0,
            renewal_date=date(2027, 6, 1),
            notes="High-throughput AI agent orchestration, Zero Data Retention (ZDR) agreement on file."
        )
    ]
    db.add_all(dev_accounts)

    # 30. Developer Environment Secrets & 90-Day Rotation Ledger
    dev_secrets = [
        DeveloperEnvironmentSecret(
            secret_code="SEC-ROT-001",
            secret_name="GH_PROD_DEPLOY_KEY",
            target_environment="Production",
            platform="GitHub",
            sha256_fingerprint="a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8",
            rotation_cadence_days=90,
            last_rotated_at=datetime.utcnow() - timedelta(days=45),
            next_rotation_due=date.today() + timedelta(days=45),
            status="Active & Compliant"
        ),
        DeveloperEnvironmentSecret(
            secret_code="SEC-ROT-002",
            secret_name="AWS_PROD_KMS_SIGNING_KEY",
            target_environment="Production",
            platform="AWS",
            sha256_fingerprint="b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7",
            rotation_cadence_days=90,
            last_rotated_at=datetime.utcnow() - timedelta(days=30),
            next_rotation_due=date.today() + timedelta(days=60),
            status="Active & Compliant"
        ),
        DeveloperEnvironmentSecret(
            secret_code="SEC-ROT-003",
            secret_name="META_WHATSAPP_SYSTEM_TOKEN",
            target_environment="Production",
            platform="Meta",
            sha256_fingerprint="c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6",
            rotation_cadence_days=90,
            last_rotated_at=datetime.utcnow() - timedelta(days=15),
            next_rotation_due=date.today() + timedelta(days=75),
            status="Active & Compliant"
        )
    ]
    db.add_all(dev_secrets)

    # 31. Statutory Tax Deposit Challans & BSR Reconciliation
    tax_challans = [
        StatutoryChallanFiling(
            challan_code="CHL-GST-2026-05",
            filing_type="GSTR-3B",
            statutory_authority="GSTN",
            assessment_year="2027-2028",
            tax_period="MAY-2026",
            statutory_due_date=date(2026, 6, 20),
            actual_filing_date=date(2026, 6, 18),
            challan_cin_arn="AA2906260189421",
            bsr_code="0001234",
            tax_amount_paid=54000.0,
            interest_penalty=0.0,
            payment_mode="NEFT / NetBanking",
            reconciliation_status="Reconciled with Portal"
        ),
        StatutoryChallanFiling(
            challan_code="CHL-TDS-2026-Q1",
            filing_type="TDS Challan 281",
            statutory_authority="Income Tax Department",
            assessment_year="2027-2028",
            tax_period="Q1 FY26-27",
            statutory_due_date=date(2026, 7, 7),
            actual_filing_date=date(2026, 7, 5),
            challan_cin_arn="00012340507202600123",
            bsr_code="0001234",
            tax_amount_paid=23850.0,
            interest_penalty=0.0,
            payment_mode="NEFT / NetBanking",
            reconciliation_status="Reconciled with Portal"
        ),
        StatutoryChallanFiling(
            challan_code="CHL-PT-2026-05",
            filing_type="Karnataka PT Form 5",
            statutory_authority="Karnataka Commercial Taxes",
            assessment_year="2027-2028",
            tax_period="MAY-2026",
            statutory_due_date=date(2026, 6, 20),
            actual_filing_date=date(2026, 6, 19),
            challan_cin_arn="KPT290520260049",
            bsr_code="0001234",
            tax_amount_paid=600.0,
            interest_penalty=0.0,
            payment_mode="NEFT / NetBanking",
            reconciliation_status="Reconciled with Portal"
        ),
        StatutoryChallanFiling(
            challan_code="CHL-ADV-2026-Q1",
            filing_type="Advance Tax Installment 1",
            statutory_authority="Income Tax Department",
            assessment_year="2027-2028",
            tax_period="Q1 FY26-27",
            statutory_due_date=date(2026, 6, 15),
            actual_filing_date=date(2026, 6, 14),
            challan_cin_arn="00012341406202600891",
            bsr_code="0001234",
            tax_amount_paid=45000.0,
            interest_penalty=0.0,
            payment_mode="NEFT / NetBanking",
            reconciliation_status="Reconciled with Portal"
        )
    ]
    db.add_all(tax_challans)
    db.commit()

def _seed_smart_attendance(db):
    hq_geofence = GeofenceZone(
        zone_code="GEO-BLR-HQ",
        zone_name="Asperion Tech Horamavu HQ",
        latitude=13.035820,
        longitude=77.653410,
        radius_meters=250.0,
        address="Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore - 560043",
        zone_type="Registered Office",
        is_active=True
    )
    ecity_zone = GeofenceZone(
        zone_code="GEO-ECITY-CLT",
        zone_name="Electronic City Client Site (FinTech Partner)",
        latitude=12.845210,
        longitude=77.660150,
        radius_meters=350.0,
        address="Phase 1, Electronic City, Bangalore - 560100",
        zone_type="Client Site",
        is_active=True
    )
    db.add_all([hq_geofence, ecity_zone])
    db.flush()

    # Get sample employees
    emp1 = db.query(Employee).first()
    emp2 = db.query(Employee).offset(1).first() if db.query(Employee).count() > 1 else emp1
    emp3 = db.query(Employee).offset(2).first() if db.query(Employee).count() > 2 else emp1

    today = date.today()
    yesterday = today - timedelta(days=1)

    if emp1:
        clock_in_time = datetime.combine(today, datetime.strptime("09:12:00", "%H:%M:%S").time())
        att1 = AttendanceRecord(
            employee_id=emp1.id,
            attendance_date=today,
            clock_in_time=clock_in_time,
            clock_out_time=None,
            total_work_hours=0.0,
            effective_work_hours=0.0,
            status="Present",
            in_source="FACIAL_KIOSK",
            in_latitude=13.035825,
            in_longitude=77.653412,
            geofence_verified=True,
            geofence_zone_code="GEO-BLR-HQ",
            geofence_distance_meters=1.2,
            facial_recognition_verified=True,
            facial_match_confidence_pct=97.8,
            facial_liveness_verified=True
        )
        db.add(att1)

    if emp2:
        clock_in_time2 = datetime.combine(today, datetime.strptime("09:05:00", "%H:%M:%S").time())
        att2 = AttendanceRecord(
            employee_id=emp2.id,
            attendance_date=today,
            clock_in_time=clock_in_time2,
            clock_out_time=None,
            total_work_hours=0.0,
            effective_work_hours=0.0,
            status="Present",
            in_source="WHATSAPP",
            in_latitude=13.035815,
            in_longitude=77.653408,
            geofence_verified=True,
            geofence_zone_code="GEO-BLR-HQ",
            geofence_distance_meters=3.5,
            facial_recognition_verified=False,
            whatsapp_message_id="wamid.HBgLOTE5ODg2MDEyMzQ1FQIAEhgg"
        )
        db.add(att2)

        wa_session = WhatsAppAttendanceSession(
            phone_number="+919886012345",
            employee_id=emp2.id,
            last_message_text="IN",
            last_message_at=datetime.utcnow() - timedelta(hours=3),
            session_state="CONFIRMED",
            pending_clock_action="IN"
        )
        db.add(wa_session)

    if emp3:
        # Yesterday's unclosed punch to showcase auto-healing engine
        clock_in_time3 = datetime.combine(yesterday, datetime.strptime("09:25:00", "%H:%M:%S").time())
        att_unclosed = AttendanceRecord(
            employee_id=emp3.id,
            attendance_date=yesterday,
            clock_in_time=clock_in_time3,
            clock_out_time=None,
            total_work_hours=0.0,
            effective_work_hours=0.0,
            status="Present",
            in_source="FACIAL_KIOSK",
            in_latitude=13.035820,
            in_longitude=77.653410,
            geofence_verified=True,
            geofence_zone_code="GEO-BLR-HQ",
            geofence_distance_meters=0.5,
            facial_recognition_verified=True,
            facial_match_confidence_pct=95.4,
            facial_liveness_verified=True,
            is_anomalous=False
        )
        db.add(att_unclosed)

    db.commit()

def _seed_pmo_stage_gates(db):
    """Seeds globally acknowledged PMO processes, stage-gates, and registers."""
    project = db.query(Project).filter(Project.project_code == "ADT-PRJ-2026-001").first()
    if not project:
        project = db.query(Project).first()
    if not project:
        return

    # 1. Stage-Gate 1: Intake & Business Case
    intakes = [
        ProjectIntake(
            intake_code="ADT-INTK-2026-001",
            project_name="Enterprise Workflow & AI Stack",
            sponsor="Varadi Vijay (Sole Director)",
            client_or_internal="Zenith Global Corp",
            strategic_fit="Critical",
            expected_value="Core SaaS revenue, ISO 27001 automation & high client retention",
            target_start_date=date(2026, 6, 20),
            estimated_budget_inr=2400000.0,
            intake_status="Approved to Charter",
            approval_date=date(2026, 6, 18),
            approved_by="Varadi Vijay (Director)"
        ),
        ProjectIntake(
            intake_code="ADT-INTK-2026-002",
            project_name="Autonomous Multi-Model Cloud FinOps",
            sponsor="Finance Head",
            client_or_internal="Internal R&D Platform",
            strategic_fit="High",
            expected_value="35% AWS cloud cost reduction & auto-scaling optimizations",
            target_start_date=date(2026, 8, 1),
            estimated_budget_inr=850000.0,
            intake_status="Under Evaluation",
            approval_date=None,
            approved_by=None
        )
    ]
    db.add_all(intakes)

    # 2. Stage-Gate 2: Charter Baseline
    charter = ProjectCharter(
        project_id=project.id,
        charter_code="ADT-CHTR-2026-001",
        problem_statement="Legacy client workflows lack automated statutory payroll compliance, real-time geofenced attendance, and CERT-In 6-hour security reporting.",
        business_case="Modernize enterprise operational architecture into an integrated, ISO 27001 and DPDP-compliant multi-tenant SaaS cockpit.",
        measurable_success_criteria="99.9% uptime, <1h P1 incident containment, zero non-compliance penalties on PF/PT, and 100% 3-way matching accuracy.",
        scope_included="18 integrated operating modules, automated self-healing daemon, biometric facial attendance, and dedicated stakeholder portals.",
        scope_excluded="Hardware on-premises infrastructure assembly and non-standard legacy ERP physical tape backups.",
        assumptions_summary="AWS cloud availability at 99.99% and prompt statutory portal (MCA/GSTN/EPFO) API response.",
        constraints_summary="Fixed budget INR 24 Lakhs and strict 6-month delivery deadline (20 Dec 2026).",
        governance_cadence="Weekly SteerCo, Daily 15-min Standup, Bi-weekly Sprint Retrospectives",
        signoff_status="Approved & Baselined",
        signed_off_by="Varadi Vijay (Sole Director)",
        signoff_date=date(2026, 6, 19)
    )
    db.add(charter)

    # 3. Actions & Decisions Log
    actions_decisions = [
        ActionDecisionItem(
            project_id=project.id,
            item_type="Action",
            source_meeting="SteerCo Review #03",
            title_or_decision="Lock AWS GovCloud and Mumbai Region VPC Peering architecture",
            rationale_or_context="Necessary to satisfy DPDP Act 2023 residency requirements for enterprise banking clients.",
            owner="Vikram Rathore",
            due_date=date(2026, 7, 10),
            status="In Progress",
            recorded_date=date(2026, 6, 25)
        ),
        ActionDecisionItem(
            project_id=project.id,
            item_type="Decision",
            source_meeting="Architecture Review Board",
            title_or_decision="Adopt FastAPI + SQLite WAL Mode with SQLAlchemy 2.0 ORM for core stack",
            rationale_or_context="Guarantees sub-10ms response times, zero database locks, and deterministic microsecond test execution.",
            owner="Varadi Vijay (Director)",
            due_date=date(2026, 6, 20),
            status="Implemented",
            recorded_date=date(2026, 6, 20)
        ),
        ActionDecisionItem(
            project_id=project.id,
            item_type="Action",
            source_meeting="Daily Standup",
            title_or_decision="Execute automated 3-way AP matching for AWS and Nexus hardware bills",
            rationale_or_context="Prevent unauthorized invoices and enforce Chapter XVII-B TDS deduction prior to payout.",
            owner="Arjun Sharma",
            due_date=date(2026, 7, 5),
            status="Closed",
            recorded_date=date(2026, 6, 28)
        )
    ]
    db.add_all(actions_decisions)

    # 4. Capacity & Skills Planning
    capacity_plans = [
        CapacityPlanItem(
            project_id=project.id,
            role_title="Project Manager & Scrum Master",
            person_or_vendor="Vikram Rathore",
            skill_area="PMO, Agile Scrum & Stakeholder Governance",
            required_hours=80.0,
            available_hours=80.0,
            utilization_pct=100.0,
            variance_hours=0.0,
            status="Balanced"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="Lead Full-Stack Architect",
            person_or_vendor="Arjun Sharma",
            skill_area="Python FastAPI, SQLite WAL, Tailwind & React/Vue",
            required_hours=130.0,
            available_hours=120.0,
            utilization_pct=108.3,
            variance_hours=-10.0,
            status="Constrained / Overallocated"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="Lead QA & UAT Engineer",
            person_or_vendor="Sneha Rao",
            skill_area="Automated PyTest, Playwright & Manual UAT Test Cases",
            required_hours=75.0,
            available_hours=80.0,
            utilization_pct=93.8,
            variance_hours=5.0,
            status="Balanced"
        ),
        CapacityPlanItem(
            project_id=project.id,
            role_title="SecOps & Compliance Specialist",
            person_or_vendor="Priya Nair",
            skill_area="ISO 27001 A.8, CERT-In Triage & NIST SP 800-61",
            required_hours=60.0,
            available_hours=70.0,
            utilization_pct=85.7,
            variance_hours=10.0,
            status="Surplus Capacity"
        )
    ]
    db.add_all(capacity_plans)

    # 5. Quality & UAT Signoffs
    quality_uats = [
        QualityUATItem(
            project_id=project.id,
            deliverable_name="Core Statutory CTC Calculator & Payroll Engine",
            test_or_review_type="Internal QA & Statutory Audit",
            acceptance_criteria="EPFO 12% ceiling ₹15k, Karnataka PT ₹200, and Net Salary balancing down to ₹0.01.",
            test_lead="Sneha Rao",
            client_reviewer="Finance & Audit Team",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 25),
            evidence_notes="Verified against Karnataka PT Act 1976 and Employees Provident Funds Act 1952."
        ),
        QualityUATItem(
            project_id=project.id,
            deliverable_name="Smart Attendance Biometric & Haversine Geofence",
            test_or_review_type="Client UAT",
            acceptance_criteria="Haversine distance within 250m of Horamavu Bangalore HQ (13.035820, 77.653410) & 3D facial liveness >95%.",
            test_lead="Arjun Sharma",
            client_reviewer="Ramesh K. (Client Sponsor)",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 27),
            evidence_notes="Live mobile and desktop check-in tests passed across 5 enrolled employees."
        ),
        QualityUATItem(
            project_id=project.id,
            deliverable_name="CERT-In 6-Hour Security Incident Triage & War Room",
            test_or_review_type="Security & Penetration Scan",
            acceptance_criteria="P1 triage and formatted CERT-In reporting document generated within 360 minutes with SHA-256 evidence chain.",
            test_lead="Priya Nair",
            client_reviewer="CISO Office",
            status="Passed & Signed-Off",
            signoff_date=date(2026, 6, 28),
            evidence_notes="Playbooks verified against Cert-In Guidelines issued under IT Act Section 70B."
        )
    ]
    db.add_all(quality_uats)

    # 6. Project Closures & Lessons Learned
    closures = [
        ProjectClosureItem(
            project_id=project.id,
            closure_area="Milestone 1 Deliverables Accepted",
            description="Phase 1 MVP architecture, CTC payroll, and SecOps war room formal handover.",
            evidence_signoff="Client Milestone Acceptance Certificate #ADT-MAC-001",
            owner="Vikram Rathore",
            closure_status="Completed",
            lessons_learned_summary="Adopting automated test suites and pre-seeded templates reduced delivery cycle from 6 weeks to 10 days.",
            completed_date=date(2026, 6, 30)
        ),
        ProjectClosureItem(
            project_id=project.id,
            closure_area="Financial Milestone Billing Settled",
            description="Invoicing and bank remittance reconciliation for Sprint 1 milestone payment.",
            evidence_signoff="Commercial Invoice ADT/INV/2026/0001 (INR 7,08,000 Paid)",
            owner="Finance Head",
            closure_status="Completed",
            lessons_learned_summary="Linking milestone payment criteria directly to UAT pass signoffs accelerated client cash receipt to under 5 days.",
            completed_date=date(2026, 7, 2)
        )
    ]
    db.add_all(closures)
    db.commit()

def _seed_sdlc_devsecops(db):
    """Seeds complete 7-stage SDLC and DevSecOps engineering assets."""
    # 1. SRS Requirements & Traceability Matrix (RTM)
    reqs = [
        SDLCRequirement(
            req_code="ADT-REQ-001",
            title="Statutory Payroll CTC Engine with Karnataka PT & EPFO Ceiling",
            category="Functional",
            priority="Must Have",
            business_rationale="Ensure 100% legal compliance with Payment of Wages and EPFO 1952 ceiling (₹15,000).",
            acceptance_criteria="Given an annual CTC, when calculating salary breakup, then Basic=40%, HRA=40% of Basic, PT=₹200/mo, and Net Take-home matches statutory ledger.",
            source_stakeholder="Head of Finance & Treasury",
            linked_wbs_code="1.2",
            verification_method="Automated Test",
            status="Verified"
        ),
        SDLCRequirement(
            req_code="ADT-REQ-002",
            title="Biometric Facial Liveness & Haversine Geofenced Attendance",
            category="Security (DevSecOps)",
            priority="Must Have",
            business_rationale="Prevent proxy punches and enforce physical presence within 250m radius of Horamavu HQ.",
            acceptance_criteria="Given GPS coordinates (13.035820, 77.653410), when employee clocks in, then Haversine distance <= 250m and 3D facial liveness match >= 90%.",
            source_stakeholder="People Operations Lead",
            linked_wbs_code="1.4",
            verification_method="Automated Test",
            status="Verified"
        ),
        SDLCRequirement(
            req_code="ADT-REQ-003",
            title="CERT-In 6-Hour Mandatory Cyber Security Incident Reporting",
            category="Compliance",
            priority="Must Have",
            business_rationale="Meet Government of India Cyber Security Directions under Section 70B of the IT Act 2000.",
            acceptance_criteria="When P1 ransomware or data breach occurs, system generates formatted incident report with SHA-256 evidence chain within 360 minutes.",
            source_stakeholder="CISO / Incident Commander",
            linked_wbs_code="2.1",
            verification_method="Automated Test",
            status="Verified"
        ),
        SDLCRequirement(
            req_code="ADT-REQ-004",
            title="Automated 3-Way AP Invoice Matching Guard",
            category="Non-Functional (NFR)",
            priority="Should Have",
            business_rationale="Enforce Internal Financial Controls (IFC) and eliminate duplicate or fraudulent vendor payouts.",
            acceptance_criteria="Match PO line items with inward Goods Receipt Notes (GRN) and vendor AP bills with 0% tolerance before payment batch release.",
            source_stakeholder="Finance Head",
            linked_wbs_code="2.2",
            verification_method="Automated Test",
            status="Verified"
        ),
        SDLCRequirement(
            req_code="ADT-REQ-005",
            title="Sub-15ms p95 API Latency with SQLite WAL Mode",
            category="Performance",
            priority="Must Have",
            business_rationale="Deliver instantaneous ERP navigation across high-density enterprise accounting grids.",
            acceptance_criteria="Benchmark test must achieve p95 latency <= 15ms and p99 latency <= 30ms under concurrent requests.",
            source_stakeholder="Lead Architect (Arjun Sharma)",
            linked_wbs_code="1.1",
            verification_method="Automated Benchmark",
            status="Verified"
        )
    ]
    db.add_all(reqs)

    # 2. Architecture Decision Records (ADR)
    adrs = [
        ArchitectureDecisionRecord(
            adr_number="ADR-001",
            title="FastAPI + SQLAlchemy 2.0 with SQLite Write-Ahead Logging (WAL)",
            status="Accepted",
            context="Need microsecond execution speeds, deterministic zero-lock file access, and standalone distribution without heavy DB server maintenance overhead.",
            decision="Adopt FastAPI with SQLite WAL mode, foreign key enforcement, and synchronous SessionLocal pooling.",
            consequences="Ultra-fast local latency (<5ms), zero network hops, and 100% ACID compliance. Horizontal multi-host scaling requires replication adapter.",
            compliance_impact="ISO 27001 A.8.25 Secure Architecture & NIST SP 800-64",
            author="Arjun Sharma (Lead Architect)",
            date_approved=date(2026, 6, 12)
        ),
        ArchitectureDecisionRecord(
            adr_number="ADR-002",
            title="Deterministic Token-Based Role-Based Access Control (RBAC)",
            status="Accepted",
            context="Enterprise stakeholders (Director, Finance, HR, PMO, SecOps, Employees, Clients, Vendors) require strict data isolation.",
            decision="Implement deterministic cryptographically signed bearer tokens with module-level authorize guards.",
            consequences="Instantaneous authentication checks, zero session table lookups, and clear portal routing boundaries.",
            compliance_impact="ISO 27001 A.9 Access Control & OWASP SAMM",
            author="Priya Nair (CISO Lead)",
            date_approved=date(2026, 6, 14)
        ),
        ArchitectureDecisionRecord(
            adr_number="ADR-003",
            title="Client-Side Dynamic Reactive SPA with Server-Driven REST Controllers",
            status="Accepted",
            context="Enterprise users require snappy, high-density data tables, responsive charts, and offline-capable modal workflows without heavy node_modules build bloat.",
            decision="Deploy native ES6 modern modular JavaScript, Chart.js 4.4, and Tailwind utility styling served by FastAPI static mounting.",
            consequences="Zero frontend bundle compile step, instant hot-reload, lightweight footprint (<500KB total assets).",
            compliance_impact="IEEE 12207 Software Lifecycle Processes",
            author="Sneha Rao (Frontend Lead)",
            date_approved=date(2026, 6, 15)
        )
    ]
    db.add_all(adrs)

    # 3. Source Repositories & Pull Requests
    repo = CodeRepository(
        repo_name="asperion-enterprise-os",
        git_url="https://github.com/asperion-digital/asperion-enterprise-os.git",
        default_branch="main",
        branch_protection_rule="Require 2 Peer Reviews + CI Test Pass + Signed Commits",
        primary_language="Python 3.14 / JavaScript (ES6+)",
        framework="FastAPI / SQLAlchemy / Tailwind",
        open_pull_requests_count=1,
        health_score_pct=99.2
    )
    db.add(repo)

    prs = [
        PullRequestReview(
            pr_number="PR #41",
            title="feat: Implement Stage-Gate 1-5 PMO delivery lifecycle and SteerCo action register",
            author="Vikram Rathore",
            source_branch="feature/pmo-stage-gates",
            target_branch="main",
            description="Adds ProjectIntake, ProjectCharter, CapacityPlan, SteerCo action/decisions, UAT sign-offs, and project closures.",
            lines_added=420,
            lines_deleted=15,
            peer_reviewers="Arjun Sharma, Sneha Rao",
            review_status="Merged",
            security_signoff=True,
            merged_at=datetime.utcnow() - timedelta(hours=2)
        ),
        PullRequestReview(
            pr_number="PR #42",
            title="feat: DevSecOps Quality Gates & SDLC automated pipeline observability",
            author="Arjun Sharma",
            source_branch="feature/sdlc-devsecops-pipeline",
            target_branch="main",
            description="Integrates SAST (Bandit), SCA (pip-audit), automated PyTest coverage, and release deployment tracking.",
            lines_added=310,
            lines_deleted=8,
            peer_reviewers="Priya Nair (SecOps), Sneha Rao (QA)",
            review_status="Approved",
            security_signoff=True,
            merged_at=None
        )
    ]
    db.add_all(prs)

    # 4. CI/CD Automated Pipelines
    pipelines = [
        CICDPipelineRun(
            pipeline_code="PIPE-2026-094",
            commit_sha="a7b8c9d0e1f2",
            branch="main",
            triggered_by="Arjun Sharma (Lead Architect)",
            duration_seconds=118,
            build_status="SUCCESS",
            unit_tests_passed=94,
            unit_tests_failed=0,
            test_coverage_pct=94.8,
            sast_tool="Bandit 1.7.5 / Semgrep OSS",
            sast_vulnerabilities_found=0,
            sca_tool="pip-audit / OWASP Dependency-Check",
            vulnerable_dependencies=0,
            secret_leak_scan_status="CLEAN",
            quality_gate_result="PASSED",
            artifacts_generated="docker-registry.asperion.in/stack:v1.0.94"
        ),
        CICDPipelineRun(
            pipeline_code="PIPE-2026-093",
            commit_sha="e5f6a1b2c3d4",
            branch="feature/pmo-stage-gates",
            triggered_by="Vikram Rathore",
            duration_seconds=132,
            build_status="SUCCESS",
            unit_tests_passed=87,
            unit_tests_failed=0,
            test_coverage_pct=93.5,
            sast_tool="Bandit 1.7.5",
            sast_vulnerabilities_found=0,
            sca_tool="pip-audit",
            vulnerable_dependencies=0,
            secret_leak_scan_status="CLEAN",
            quality_gate_result="PASSED",
            artifacts_generated="docker-registry.asperion.in/stack:v1.0.93-rc1"
        )
    ]
    db.add_all(pipelines)

    # 5. Defect Tracking (IEEE 1044)
    bugs = [
        DefectBugRecord(
            bug_id="BUG-2026-001",
            title="Attendance missing punch edge condition during midnight shift crossing",
            severity="S3-Medium",
            environment="Staging",
            module_affected="HRMS / Attendance Engine",
            steps_to_reproduce="Clock in at 22:00, clock out at 06:00 next calendar day.",
            actual_behavior="Prorated hours logged under previous day's shift date without multi-day flag.",
            expected_behavior="Attendance anomaly engine should auto-heal and split shift duration across calendar midnight.",
            assigned_engineer="Arjun Sharma",
            reported_by="Sneha Rao (QA Lead)",
            fix_commit_sha="f8a1b2c3d4e5",
            status="Resolved & Verified"
        ),
        DefectBugRecord(
            bug_id="BUG-2026-002",
            title="AP 3-way matching tolerance rounding on fractional GST paise",
            severity="S4-Minor / Cosmetic",
            environment="Staging",
            module_affected="Finance / AP 3-Way Matching",
            steps_to_reproduce="Submit vendor bill with INR 0.49 paise variance against purchase order tax rounding.",
            actual_behavior="Flagged as minor mismatch under strict zero-tolerance rule.",
            expected_behavior="Allow standard statutory rounding threshold of +- INR 1.00 as per GST rules.",
            assigned_engineer="Arjun Sharma",
            reported_by="Sneha Rao (QA Lead)",
            fix_commit_sha="c3d4e5f6a1b2",
            status="Resolved & Verified"
        )
    ]
    db.add_all(bugs)

    # 6. Releases & Deployments
    releases = [
        ReleaseDeployment(
            release_tag="v1.0.0",
            environment="Production",
            deployment_strategy="Blue-Green / Zero Downtime",
            change_advisory_board_approval="Approved by Varadi Vijay (CAB Chair / Sole Director)",
            release_notes="Initial enterprise release: 18 operating modules, statutory payroll, SecOps war room, smart attendance, and dedicated stakeholder portals.",
            rollback_plan="Instant 30-second automated container rollback to baseline digest.",
            downtime_minutes=0.0,
            smoke_test_status="PASSED",
            deployed_by="Vikram Rathore (Release Manager)",
            deployment_status="Healthy & Live"
        ),
        ReleaseDeployment(
            release_tag="v1.1.0-rc1",
            environment="Staging",
            deployment_strategy="Canary (10% Traffic)",
            change_advisory_board_approval="Approved by Architecture Review Board",
            release_notes="PMO stage-gate 1-5 lifecycle, SteerCo action register, resource capacity planning, and DevSecOps quality gates.",
            rollback_plan="Drain canary routing target group back to v1.0.0 production cluster.",
            downtime_minutes=0.0,
            smoke_test_status="PASSED",
            deployed_by="Arjun Sharma (Lead Architect)",
            deployment_status="Healthy & Live"
        )
    ]
    db.add_all(releases)

    # 7. SRE Observability Telemetry
    obs = SREObservabilityMetric(
        service_name="asperion-core-api",
        p95_latency_ms=7.8,
        p99_latency_ms=13.4,
        uptime_30d_pct=99.98,
        error_rate_pct=0.01,
        error_budget_remaining_pct=92.4,
        active_memory_mb=176.2,
        cpu_utilization_pct=11.8,
        active_db_connections=4
    )
    db.add(obs)
    db.commit()


def _seed_strategic_procurement(db):
    """Seeds comprehensive 8-pillar Vendor Management & Strategic Sourcing assets."""
    # 1. Sourcing Categories & Spend Targets
    categories = [
        SourcingCategory(
            category_code="CAT-IT-CLOUD",
            category_name="Cloud & Infrastructure Hosting",
            annual_budget_inr=1200000.0,
            sourcing_strategy="Multi-Vendor Competitive",
            lead_buyer="Head of Infrastructure (Priya Nair)",
            active_vendors_count=2,
            esg_weight_pct=15.0
        ),
        SourcingCategory(
            category_code="CAT-SAAS",
            category_name="Enterprise SaaS & Developer Tools",
            annual_budget_inr=480000.0,
            sourcing_strategy="Preferred Partner Panel",
            lead_buyer="Lead Architect (Arjun Sharma)",
            active_vendors_count=4,
            esg_weight_pct=10.0
        ),
        SourcingCategory(
            category_code="CAT-HARDWARE",
            category_name="Developer Workstations & Networking Devices",
            annual_budget_inr=650000.0,
            sourcing_strategy="Strategic Sole Source / Apple Authorized",
            lead_buyer="IT Asset Admin",
            active_vendors_count=1,
            esg_weight_pct=10.0
        ),
        SourcingCategory(
            category_code="CAT-PROF-LEGAL",
            category_name="Professional Legal, Statutory Audit & Advisory",
            annual_budget_inr=350000.0,
            sourcing_strategy="Selective Panel",
            lead_buyer="Head of Legal & Finance",
            active_vendors_count=2,
            esg_weight_pct=5.0
        ),
        SourcingCategory(
            category_code="CAT-HR-STAFF",
            category_name="Contract Engineering & Talent Augmentation",
            annual_budget_inr=800000.0,
            sourcing_strategy="Reverse Auction / Rate Card",
            lead_buyer="People Operations Lead",
            active_vendors_count=3,
            esg_weight_pct=10.0
        )
    ]
    db.add_all(categories)
    db.flush()

    # 2. Additional Enterprise Vendors (if not already existing)
    vendors = [
        Vendor(
            vendor_code="ADT-VEN-002",
            vendor_name="Nexus Micro Systems Pvt Ltd",
            contact_person="Rohan Deshmukh",
            email="enterprise@nexusmicrosystems.in",
            phone="+91 80 4123 9800",
            category="Hardware & Workstations",
            criticality_tier="Tier 2 - High",
            pan="AABCN5678E",
            gstin="29AABCN5678E1Z4",
            duns_number="91-456-7890",
            bank_account_number="50200088991122",
            bank_ifsc="HDFC0001234",
            bank_name="HDFC Bank Koramangala",
            msme_registered=True,
            msme_udyam_number="UDYAM-KR-03-0091823",
            msme_category="Micro",
            msme_payment_due_days=45,
            kyc_status="Approved",
            dpdp_compliance_status="Compliant",
            annual_spend_estimate=420000.0,
            payment_terms_days=30,
            rating=94.5,
            is_active=True
        ),
        Vendor(
            vendor_code="ADT-VEN-003",
            vendor_name="Zenith InfoSec Solutions LLP",
            contact_person="Kavita Krishnan",
            email="soc-support@zenithinfosec.com",
            phone="+91 80 6712 3400",
            category="Cybersecurity & SecOps",
            criticality_tier="Tier 1 - Mission Critical",
            pan="AABCZ9012F",
            gstin="29AABCZ9012F1Z7",
            duns_number="91-789-0123",
            bank_account_number="000205001122",
            bank_ifsc="ICIC0000002",
            bank_name="ICICI Bank MG Road",
            msme_registered=True,
            msme_udyam_number="UDYAM-KR-03-0044551",
            msme_category="Small",
            msme_payment_due_days=45,
            kyc_status="Approved",
            dpdp_compliance_status="Compliant",
            annual_spend_estimate=300000.0,
            payment_terms_days=30,
            rating=98.0,
            is_active=True
        ),
        Vendor(
            vendor_code="ADT-VEN-004",
            vendor_name="KPMG Assurance & Legal Advisory",
            contact_person="Sunil Varma",
            email="svarma@kpmg-advisory.in",
            phone="+91 80 3980 5000",
            category="Professional Services & Legal",
            criticality_tier="Tier 2 - High",
            pan="AABCK3456G",
            gstin="29AABCK3456G1Z2",
            duns_number="91-112-2334",
            bank_account_number="919010023456789",
            bank_ifsc="UTIB0000015",
            bank_name="Axis Bank Indiranagar",
            msme_registered=False,
            msme_category="Non-MSME",
            msme_payment_due_days=30,
            kyc_status="Approved",
            dpdp_compliance_status="Compliant",
            annual_spend_estimate=250000.0,
            payment_terms_days=30,
            rating=95.0,
            is_active=True
        ),
        Vendor(
            vendor_code="ADT-VEN-005",
            vendor_name="Acroprint Technologies India",
            contact_person="Mahesh Nambiar",
            email="support@acroprint.in",
            phone="+91 80 2558 1122",
            category="Facility & Biometrics",
            criticality_tier="Tier 3 - Medium",
            pan="AABCA7890H",
            gstin="29AABCA7890H1Z8",
            duns_number="91-334-4556",
            bank_account_number="620011223344",
            bank_ifsc="SBIN0004567",
            bank_name="State Bank of India Horamavu",
            msme_registered=True,
            msme_udyam_number="UDYAM-KR-03-0088221",
            msme_category="Micro",
            msme_payment_due_days=45,
            kyc_status="Approved",
            dpdp_compliance_status="Compliant",
            annual_spend_estimate=95000.0,
            payment_terms_days=15,
            rating=88.5,
            is_active=True
        )
    ]
    for v in vendors:
        if not db.query(Vendor).filter(Vendor.vendor_code == v.vendor_code).first():
            db.add(v)
    db.flush()

    # Get vendor IDs
    v_aws = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-001").first()
    v_nexus = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-002").first()
    v_zenith = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-003").first()
    v_kpmg = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-004").first()
    v_acro = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-005").first()

    # 3. Purchase Requisitions (PR)
    requisitions = [
        PurchaseRequisition(
            pr_number="ADT-PR-2026-001",
            requester_name="Arjun Sharma",
            requester_email="arjun.sharma@asperion.in",
            department="Engineering & Product",
            category="Hardware & Workstations",
            item_details="3x Apple MacBook Pro M3 Max (36GB Unified Memory / 1TB SSD) for core platform developers.",
            estimated_amount_inr=540000.0,
            urgency="Critical",
            business_justification="Required for high-density local SQLite WAL concurrency and microservice benchmarking.",
            approval_status="Converted to PO",
            approved_by="Varadi Vijay (Sole Director)",
            approved_date=date(2026, 6, 12),
            linked_po_number="ADT/PO/2026/001"
        ),
        PurchaseRequisition(
            pr_number="ADT-PR-2026-002",
            requester_name="Priya Nair",
            requester_email="priya.nair@asperion.in",
            department="IT & Infrastructure",
            category="Cloud & Infrastructure Hosting",
            item_details="AWS Mumbai Region (ap-south-1) 1-Year Reserved Instances for Core EKS Cluster & S3 Storage.",
            estimated_amount_inr=360000.0,
            urgency="Normal",
            business_justification="Lock in 38% compute cost reduction compared to on-demand pricing under corporate budget.",
            approval_status="Converted to PO",
            approved_by="Varadi Vijay (Sole Director)",
            approved_date=date(2026, 6, 18),
            linked_po_number="ADT/PO/2026/002"
        ),
        PurchaseRequisition(
            pr_number="ADT-PR-2026-003",
            requester_name="Priya Nair",
            requester_email="priya.nair@asperion.in",
            department="Cybersecurity & Compliance",
            category="Professional Legal & Advisory",
            item_details="Annual SOC 2 Type II Surveillance and ISO 27001 Re-Certification External Audit.",
            estimated_amount_inr=220000.0,
            urgency="Urgent",
            business_justification="Mandatory requirement for enterprise banking client retainers and DPDP Act compliance.",
            approval_status="Pending Director Signoff",
            approved_by=None,
            approved_date=None,
            linked_po_number=None
        ),
        PurchaseRequisition(
            pr_number="ADT-PR-2026-004",
            requester_name="Sneha Rao",
            requester_email="sneha.rao@asperion.in",
            department="Administration & Facilities",
            category="Facility & Biometrics",
            item_details="Multi-zone RFID biometric facial terminal backup power unit & wall mount enclosures.",
            estimated_amount_inr=65000.0,
            urgency="Normal",
            business_justification="Ensure uninterrupted attendance tracking during power cutovers at Horamavu HQ.",
            approval_status="Approved",
            approved_by="Varadi Vijay (Sole Director)",
            approved_date=date(2026, 6, 22),
            linked_po_number=None
        )
    ]
    db.add_all(requisitions)
    db.flush()

    # 4. Strategic Sourcing Events (e-RFX)
    events = [
        StrategicSourcingEvent(
            event_code="ADT-RFX-2026-001",
            event_type="RFP",
            title="Managed Kubernetes Infrastructure & High-Availability Cloud Object Storage",
            category="Cloud Hosting & Infrastructure",
            budget_allocation_inr=600000.0,
            baseline_cost_inr=650000.0,
            target_delivery_date=date(2026, 6, 20),
            status="Awarded",
            closing_date=date(2026, 6, 15),
            technical_weight_pct=40.0,
            commercial_weight_pct=30.0,
            compliance_security_weight_pct=20.0,
            sla_weight_pct=10.0,
            awarded_vendor_name="Amazon Web Services India Pvt Ltd",
            awarded_amount_inr=576000.0,
            savings_realized_inr=74000.0
        ),
        StrategicSourcingEvent(
            event_code="ADT-RFX-2026-002",
            event_type="RFQ",
            title="Developer Workstations Refresh (High-Performance Laptops)",
            category="Hardware & Workstations",
            budget_allocation_inr=650000.0,
            baseline_cost_inr=720000.0,
            target_delivery_date=date(2026, 7, 10),
            status="Commercial BAFO",
            closing_date=date(2026, 7, 5),
            technical_weight_pct=35.0,
            commercial_weight_pct=45.0,
            compliance_security_weight_pct=10.0,
            sla_weight_pct=10.0,
            awarded_vendor_name=None,
            awarded_amount_inr=0.0,
            savings_realized_inr=0.0
        ),
        StrategicSourcingEvent(
            event_code="ADT-RFX-2026-003",
            event_type="RFP",
            title="Internal Financial Controls (IFC) & DPDP Act Data Protection Officer Advisory",
            category="Professional Legal & Advisory",
            budget_allocation_inr=350000.0,
            baseline_cost_inr=400000.0,
            target_delivery_date=date(2026, 8, 1),
            status="Technical Evaluation",
            closing_date=date(2026, 7, 20),
            technical_weight_pct=50.0,
            commercial_weight_pct=25.0,
            compliance_security_weight_pct=15.0,
            sla_weight_pct=10.0,
            awarded_vendor_name=None,
            awarded_amount_inr=0.0,
            savings_realized_inr=0.0
        )
    ]
    db.add_all(events)
    db.flush()

    ev1 = events[0]
    ev2 = events[1]

    # 5. Vendor Bid Submissions
    bids = [
        VendorBidSubmission(
            bid_code="ADT-BID-2026-001",
            event_id=ev1.id,
            vendor_id=v_aws.id if v_aws else None,
            vendor_name="Amazon Web Services India Pvt Ltd",
            technical_score=96.0,
            commercial_quote_inr=48000.0,
            compliance_score=98.0,
            sla_guarantee_pct=99.99,
            composite_score=95.4,
            is_shortlisted=True,
            award_status="Awarded",
            notes="Best Mumbai region latency, automated VPC peering, and enterprise DPA."
        ),
        VendorBidSubmission(
            bid_code="ADT-BID-2026-002",
            event_id=ev1.id,
            vendor_name="Google Cloud India (GKE)",
            technical_score=92.0,
            commercial_quote_inr=52000.0,
            compliance_score=94.0,
            sla_guarantee_pct=99.95,
            composite_score=89.8,
            is_shortlisted=True,
            award_status="Unsuccessful",
            notes="Strong Anthos capabilities but higher network egress costs."
        ),
        VendorBidSubmission(
            bid_code="ADT-BID-2026-003",
            event_id=ev2.id,
            vendor_id=v_nexus.id if v_nexus else None,
            vendor_name="Nexus Micro Systems Pvt Ltd",
            technical_score=94.0,
            commercial_quote_inr=540000.0,
            compliance_score=95.0,
            sla_guarantee_pct=99.5,
            composite_score=93.6,
            is_shortlisted=True,
            award_status="BAFO Finalist",
            notes="Authorized enterprise dealer; includes 3-year AppleCare+ and on-site loaner support."
        ),
        VendorBidSubmission(
            bid_code="ADT-BID-2026-004",
            event_id=ev2.id,
            vendor_name="Comptech Retail Systems",
            technical_score=85.0,
            commercial_quote_inr=565000.0,
            compliance_score=88.0,
            sla_guarantee_pct=98.0,
            composite_score=84.2,
            is_shortlisted=True,
            award_status="Shortlisted",
            notes="Competitive pricing but lacks 24-hour hardware swap commitment."
        )
    ]
    db.add_all(bids)
    db.flush()

    # 6. Vendor Contracts (CLM)
    contracts = [
        VendorContract(
            contract_reference="ADT-VCON-2026-001",
            vendor_id=v_aws.id if v_aws else 1,
            agreement_type="Master Services Agreement (MSA)",
            effective_date=date(2026, 6, 15),
            expiry_date=date(2027, 6, 14),
            annual_value_inr=600000.0,
            sla_uptime_commitment=99.99,
            confidentiality_clause=True,
            data_protection_annexure=True,
            renewal_notice_days=60,
            auto_renew_enabled=True,
            liability_cap_inr=2000000.0,
            governing_jurisdiction="Courts of Bengaluru, Karnataka",
            status="Active"
        ),
        VendorContract(
            contract_reference="ADT-VCON-2026-002",
            vendor_id=v_nexus.id if v_nexus else 2,
            agreement_type="Hardware Procurement SLA & Warranty",
            effective_date=date(2026, 6, 20),
            expiry_date=date(2027, 6, 19),
            annual_value_inr=420000.0,
            sla_uptime_commitment=99.5,
            confidentiality_clause=True,
            data_protection_annexure=True,
            renewal_notice_days=45,
            auto_renew_enabled=True,
            liability_cap_inr=1000000.0,
            governing_jurisdiction="Courts of Bengaluru, Karnataka",
            status="Active"
        ),
        VendorContract(
            contract_reference="ADT-VCON-2026-003",
            vendor_id=v_zenith.id if v_zenith else 3,
            agreement_type="SOC & Managed Detection Service Level Agreement",
            effective_date=date(2026, 6, 25),
            expiry_date=date(2027, 6, 24),
            annual_value_inr=300000.0,
            sla_uptime_commitment=99.9,
            confidentiality_clause=True,
            data_protection_annexure=True,
            renewal_notice_days=60,
            auto_renew_enabled=True,
            liability_cap_inr=1500000.0,
            governing_jurisdiction="Courts of Bengaluru, Karnataka",
            status="Active"
        )
    ]
    for c in contracts:
        if not db.query(VendorContract).filter(VendorContract.contract_reference == c.contract_reference).first():
            db.add(c)
    db.flush()

    # 6.5 Purchase Orders (PO) Lifecycle
    pos = [
        PurchaseOrder(
            po_number="ADT/PO/2026/001",
            po_date=date(2026, 6, 12),
            vendor_name="Nexus Micro Systems Pvt Ltd",
            vendor_id=v_nexus.id if v_nexus else 2,
            project_code="ADT-PRJ-2026-01",
            total_amount=540000.0,
            delivery_due_date=date(2026, 6, 20),
            status="Fulfilled",
            items_json='[{"item": "Apple MacBook Pro M3 Max (36GB/1TB SSD)", "hsn": "84713010", "qty": 3, "rate": 180000.0, "amount": 540000.0}]',
            payment_terms="Net 30 Days (MSME Priority)",
            delivery_challan_no="DC-NEX-8891",
            statutory_notes="Asperion Digital Technologies (OPC) Private Limited standard terms. MSMED Act 2006 Priority Section 15 applies."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/002",
            po_date=date(2026, 6, 18),
            vendor_name="Amazon Web Services India Pvt Ltd",
            vendor_id=v_aws.id if v_aws else 1,
            project_code="ADT-PRJ-2026-01",
            total_amount=180000.0,
            delivery_due_date=date(2026, 6, 30),
            status="Approved",
            items_json='[{"item": "AWS Cloud Infrastructure Reserved Instances (m6i.2xlarge, RDS Aurora)", "sac": "998315", "qty": 1, "rate": 180000.0, "amount": 180000.0}]',
            payment_terms="Net 30 Days",
            statutory_notes="SLA Uptime 99.95% committed. SOC2 Type II and ISO 27001 data residency in ap-south-1 Mumbai."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/003",
            po_date=date(2026, 6, 20),
            vendor_name="Acroprint Technologies India",
            vendor_id=v_acro.id if v_acro else 5,
            project_code="ADT-PRJ-2026-01",
            total_amount=45000.0,
            delivery_due_date=date(2026, 6, 25),
            status="Fulfilled",
            items_json='[{"item": "AI Biometric Facial Recognition Scanner Terminal & Mounting Kit", "hsn": "85437099", "qty": 1, "rate": 45000.0, "amount": 45000.0}]',
            payment_terms="Net 15 Days (MSME Micro 45-day SLA)",
            delivery_challan_no="DC-ACR-1029",
            statutory_notes="Device must comply with DPDP Act 2023 biometric encryption standards."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/004",
            po_date=date(2026, 6, 22),
            vendor_name="Zenith Digital Infrastructure Pvt Ltd",
            vendor_id=v_zenith.id if v_zenith else 3,
            project_code="ADT-PRJ-2026-01",
            total_amount=95000.0,
            delivery_due_date=date(2026, 7, 5),
            status="In Transit",
            items_json='[{"item": "Dedicated 1Gbps Symmetric Leased Line Port & BGP Multi-Homing", "sac": "998411", "qty": 1, "rate": 95000.0, "amount": 95000.0}]',
            payment_terms="Net 30 Days",
            statutory_notes="Includes redundant fiber termination at Horamavu HQ."
        )
    ]
    for p in pos:
        if not db.query(PurchaseOrder).filter(PurchaseOrder.po_number == p.po_number).first():
            db.add(p)
    db.flush()

    # 7. Goods Received Notes (GRN)
    grns = [
        GoodsReceivedNote(
            grn_number="ADT-GRN-2026-001",
            vendor_id=v_nexus.id if v_nexus else 2,
            po_reference="ADT/PO/2026/001",
            delivery_challan_no="DC-NEX-8891",
            received_date=date(2026, 6, 18),
            item_description="Apple MacBook Pro M3 Max (36GB/1TB) x 3 units",
            quantity_ordered=3.0,
            quantity_received=3.0,
            quantity_accepted=3.0,
            inspection_status="Accepted",
            inspected_by="Arjun Sharma (Lead Architect)",
            warehouse_location="Horamavu Bangalore HQ",
            remarks="Packaging intact, MDM enrolled, AppleCare coverage verified via serial numbers."
        ),
        GoodsReceivedNote(
            grn_number="ADT-GRN-2026-002",
            vendor_id=v_acro.id if v_acro else 5,
            po_reference="ADT/PO/2026/003",
            delivery_challan_no="DC-ACR-1029",
            received_date=date(2026, 6, 24),
            item_description="AI Biometric Facial Recognition Scanner Terminal & Mounting Kit",
            quantity_ordered=1.0,
            quantity_received=1.0,
            quantity_accepted=1.0,
            inspection_status="Accepted",
            inspected_by="Priya Nair (SecOps Lead)",
            warehouse_location="Horamavu Bangalore HQ Entrance",
            remarks="Liveness camera calibrated, PoE connection tested, Haversine coordinates locked."
        )
    ]
    for g in grns:
        if not db.query(GoodsReceivedNote).filter(GoodsReceivedNote.grn_number == g.grn_number).first():
            db.add(g)
    db.flush()

    # 7.5 Vendor AP Bills with 3-Way Match & Chapter XVII-B TDS
    vendor_bills = [
        APBill(
            bill_number="INV-NEX-9921",
            bill_date=date(2026, 6, 19),
            due_date=date(2026, 7, 19),
            vendor_name="Nexus Micro Systems Pvt Ltd",
            po_reference="ADT/PO/2026/001",
            grn_reference="ADT-GRN-2026-001",
            three_way_match_status="Matched",
            expense_category="Hardware & Workstations",
            taxable_amount=540000.0,
            gst_amount=97200.0,
            tds_section="194C",
            tds_rate=0.02,
            tds_amount=10800.0,
            net_payable=626400.0,
            approval_status="Approved",
            payment_reference="NEFT-NEXUS-20260628"
        ),
        APBill(
            bill_number="INV-ACR-4412",
            bill_date=date(2026, 6, 24),
            due_date=date(2026, 7, 9),
            vendor_name="Acroprint Technologies India",
            po_reference="ADT/PO/2026/003",
            grn_reference="ADT-GRN-2026-002",
            three_way_match_status="Matched",
            expense_category="Facility & Biometrics",
            taxable_amount=45000.0,
            gst_amount=8100.0,
            tds_section="194C",
            tds_rate=0.01,
            tds_amount=450.0,
            net_payable=52650.0,
            approval_status="Approved",
            payment_reference="UPI-ACRO-20260627"
        ),
        APBill(
            bill_number="INV-ZEN-7711",
            bill_date=date(2026, 6, 26),
            due_date=date(2026, 7, 26),
            vendor_name="Zenith Digital Infrastructure Pvt Ltd",
            po_reference="ADT/PO/2026/004",
            grn_reference="Pending Inward GRN",
            three_way_match_status="Pending GRN",
            expense_category="Telecommunication / Leased Line",
            taxable_amount=95000.0,
            gst_amount=17100.0,
            tds_section="194J",
            tds_rate=0.02,
            tds_amount=1900.0,
            net_payable=110200.0,
            approval_status="Pending Finance Approval"
        )
    ]
    for b in vendor_bills:
        if not db.query(APBill).filter(APBill.bill_number == b.bill_number).first():
            db.add(b)
    db.flush()

    # 8. Vendor Scorecards & Performance (QBR)
    scorecards = [
        VendorScorecard(
            vendor_id=v_nexus.id if v_nexus else 2,
            evaluation_period="Q2-2026",
            quality_score=94.0,
            sla_adherence_score=96.0,
            pricing_competitiveness=92.0,
            security_privacy_score=95.0,
            overall_rating=94.25,
            performance_tier="Strategic Partner",
            evaluator="Procurement Lead (Vikram Rathore)",
            qbr_action_items="Maintain 24h hardware replacement SLA and confirm Q3 volume rebate tiers."
        ),
        VendorScorecard(
            vendor_id=v_aws.id if v_aws else 1,
            evaluation_period="Q2-2026",
            quality_score=98.0,
            sla_adherence_score=99.0,
            pricing_competitiveness=88.0,
            security_privacy_score=99.0,
            overall_rating=96.0,
            performance_tier="Strategic Partner",
            evaluator="Head of Infrastructure (Priya Nair)",
            qbr_action_items="Evaluate Savings Plans for compute workload expansion."
        ),
        VendorScorecard(
            vendor_id=v_zenith.id if v_zenith else 3,
            evaluation_period="Q2-2026",
            quality_score=97.0,
            sla_adherence_score=98.0,
            pricing_competitiveness=90.0,
            security_privacy_score=100.0,
            overall_rating=96.25,
            performance_tier="Strategic Partner",
            evaluator="CISO / Incident Commander",
            qbr_action_items="Automate CERT-In 6-hour incident XML packet forwarding into SIEM."
        )
    ]
    for sc in scorecards:
        if not db.query(VendorScorecard).filter(VendorScorecard.vendor_id == sc.vendor_id, VendorScorecard.evaluation_period == sc.evaluation_period).first():
            db.add(sc)
    db.flush()

    # 9. Third-Party Risk Assessments (TPRM)
    risks = [
        VendorRiskAssessment(
            vendor_id=v_nexus.id if v_nexus else 2,
            data_access_level="None",
            dpdp_dpa_signed=True,
            iso27001_certified=True,
            soc2_type2_attestation=False,
            cross_border_data_transfer=False,
            subprocessor_disclosure_verified=True,
            residual_risk_level="Low",
            review_date=date(2026, 6, 20),
            assessor="Priya Nair (SecOps Lead)"
        ),
        VendorRiskAssessment(
            vendor_id=v_zenith.id if v_zenith else 3,
            data_access_level="Internal (Logs Only)",
            dpdp_dpa_signed=True,
            iso27001_certified=True,
            soc2_type2_attestation=True,
            cross_border_data_transfer=False,
            subprocessor_disclosure_verified=True,
            residual_risk_level="Low",
            review_date=date(2026, 6, 25),
            assessor="Priya Nair (SecOps Lead)"
        )
    ]
    for r in risks:
        db.add(r)
    db.flush()

    # 10. Vendor Corrective Action Plan (CAPA)
    capa = VendorCorrectiveActionPlan(
        capa_code="ADT-CAPA-2026-001",
        vendor_id=v_acro.id if v_acro else 5,
        vendor_name="Acroprint Technologies India",
        issue_description="Biometric attendance scanner device clock NTP drift of 3.2 seconds noticed during mock network failover drill.",
        root_cause="Device was configured with static secondary gateway instead of localized PTP/NTP server daemon pool.",
        corrective_action_agreed="Firmware patch deployed to force NTP sync every 15 minutes against Indian Standard Time (IST) time.isro.gov.in server.",
        target_closure_date=date(2026, 7, 15),
        status="In Progress",
        verified_by="Priya Nair (SecOps Lead)"
    )
    if not db.query(VendorCorrectiveActionPlan).filter(VendorCorrectiveActionPlan.capa_code == capa.capa_code).first():
        db.add(capa)
    db.commit()


def _seed_guardrails_and_architectures(db):
    """Seeds enterprise guardrail policies, blueprints, and initial execution audit logs."""
    rules = [
        GuardrailRule(
            rule_code="GRD-FIN-001",
            name="3-Way Matching FinOps Invariant Guard",
            category="FinOps",
            regulatory_framework="Internal Financial Controls (IFC) / Companies Act 2013",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Enforces 0% variance between Purchase Order, Warehouse GRN, and Vendor AP Tax Bill. Blocks disbursement on mismatch.",
            enforcement_logic="APBill.three_way_match_status == 'Matched' AND variance == 0.0%",
            total_evaluations=14,
            total_passed=13,
            total_blocked=1,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-MSME-002",
            name="MSMED Act 2006 45-Day Payment Rule Guard",
            category="Procurement_MSME",
            regulatory_framework="MSMED Act 2006 (Section 15 & 16)",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Statutory mandate ensuring all Micro and Small enterprise vendor bills are settled within 45 days. Auto-flags compound interest liability at 3x RBI bank rate.",
            enforcement_logic="IF vendor.msme_registered == True THEN settlement_age_days <= 45",
            total_evaluations=12,
            total_passed=11,
            total_blocked=1,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-DPDP-003",
            name="DPDP Act 2023 Vendor DPA & Data Governance Guard",
            category="Governance_Legal",
            regulatory_framework="Digital Personal Data Protection Act 2023",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Mandates executed Data Processing Agreements (DPA) and data protection covenants for all Tier 1 vendors before granting access to enterprise environments.",
            enforcement_logic="IF vendor.criticality_tier == 'Tier 1 - Mission Critical' THEN dpdp_compliance_status == 'Compliant'",
            total_evaluations=8,
            total_passed=8,
            total_blocked=0,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-HRMS-004",
            name="Smart Mobility Geofence & Liveness Biometric Guard",
            category="HRMS_Mobility",
            regulatory_framework="Karnataka Shops & Commercial Establishments Act",
            severity="High_Warning",
            enforcement_mode="Auto_Heal",
            description="Enforces strict 250m Haversine perimeter verification and >=85% facial liveness threshold for attendance punches. Auto-heals recognized shift anomalies.",
            enforcement_logic="haversine_distance <= 250.0m AND facial_confidence >= 85.0%",
            total_evaluations=45,
            total_passed=41,
            total_blocked=2,
            total_auto_healed=2
        ),
        GuardrailRule(
            rule_code="GRD-SDLC-005",
            name="DevSecOps Zero CVE & 90% Test Coverage Quality Gate",
            category="DevSecOps",
            regulatory_framework="ISO/IEC 27001 / CMMI Level 5",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Enforces zero high/critical SAST/SCA vulnerabilities and >=90% automated unit and integration test coverage before merging pull requests to main.",
            enforcement_logic="sast_vulnerabilities == 0 AND test_coverage_pct >= 90.0 AND secret_leak_scan == 'CLEAN'",
            total_evaluations=18,
            total_passed=17,
            total_blocked=1,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-DOA-006",
            name="Financial Delegation of Authority (DOA) Threshold Guard",
            category="Governance_DOA",
            regulatory_framework="Companies Act 2013 / Board Authority Matrix",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Procurement requisitions and capital expenditures exceeding INR 1,00,000 strictly require Sole Director signoff. Blocks PO issuance on missing approval.",
            enforcement_logic="IF estimated_amount_inr > 100000.0 THEN approved_by CONTAINS 'Director'",
            total_evaluations=15,
            total_passed=14,
            total_blocked=1,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-CERT-007",
            name="CERT-In 6-Hour SLA Cyber Incident Escalation Guard",
            category="SecOps",
            regulatory_framework="CERT-In Cyber Security Directions (Sec 70B IT Act 2000)",
            severity="Critical_Blocker",
            enforcement_mode="Active_Blocking",
            description="Monitors critical security incidents (P1) and enforces statutory dispatch of the preliminary incident notification to incident@cert-in.org.in within 6 hours.",
            enforcement_logic="IF severity == 'P1-Critical' AND cert_in_reportable THEN elapsed_hours <= 6.0",
            total_evaluations=6,
            total_passed=6,
            total_blocked=0,
            total_auto_healed=0
        ),
        GuardrailRule(
            rule_code="GRD-SECR-008",
            name="90-Day Cryptographic Secret Rotation & Leak Prevention",
            category="SecOps",
            regulatory_framework="ISO/IEC 27001:2022 ISMS Controls",
            severity="High_Warning",
            enforcement_mode="Auto_Heal",
            description="Flags API keys, certificates, and database secrets approaching 90-day lifecycle limit and auto-quarantines expired credentials.",
            enforcement_logic="secret_age_days <= 90 AND days_until_expiration >= 0",
            total_evaluations=10,
            total_passed=9,
            total_blocked=0,
            total_auto_healed=1
        )
    ]
    for r in rules:
        if not db.query(GuardrailRule).filter(GuardrailRule.rule_code == r.rule_code).first():
            db.add(r)
    db.flush()

    # 2. Architecture Blueprints
    blueprints = [
        ArchitectureBlueprint(
            blueprint_code="ARCH-E2E-001",
            title="Asperion Enterprise OS Multi-Tier Decoupled Architecture",
            architecture_type="System_Architecture",
            module_pillar="Enterprise Operating System Core",
            standard_alignment="ISO 27001 / TOGAF Standard 10th Ed",
            diagram_mermaid=(
                "graph TB\n"
                "    subgraph Client_Tier[Presentation & Edge Channels]\n"
                "        A1[Multi-Stakeholder Web Cockpits: Director, HR, PMO, Vendor, Employee]\n"
                "        A2[WhatsApp Webhook Gateway: Attendance & Approvals]\n"
                "        A3[Headless Asperion CLI: Automation & CI/CD]\n"
                "    end\n"
                "    subgraph API_Gateway_Tier[FastAPI API Gateway & Security Perimeter]\n"
                "        B1[OAuth2 JWT Authentication & RBAC Filter]\n"
                "        B2[Rate Limiting & Statutory Payload Validator]\n"
                "        B3[CORS & CSP Zero-Trust Security Middleware]\n"
                "    end\n"
                "    subgraph Engine_Tier[Autonomous Business Engines]\n"
                "        C1[FinOps 3-Way Matching Engine]\n"
                "        C2[Smart Attendance & Anomaly Self-Healing Daemon]\n"
                "        C3[Continuous Guardrails Evaluator]\n"
                "        C4[Real-Time Background AutoUpdate Manager]\n"
                "    end\n"
                "    subgraph Persistence_Tier[High-Availability Data & Document Vault]\n"
                "        D1[(SQLite WAL Mode Enterprise Database: 90+ Tables)]\n"
                "        D2[Encrypted Document Vault: Contracts, Invoices, Certificates]\n"
                "        D3[Immutable Audit Trail & Ledger Logs]\n"
                "    end\n"
                "    Client_Tier --> API_Gateway_Tier\n"
                "    API_Gateway_Tier --> Engine_Tier\n"
                "    Engine_Tier --> Persistence_Tier"
            ),
            description="Exhaustive architectural view of Asperion OS demonstrating clean separation between edge channels, API security gateway, autonomous background engines, and the transactional database layer.",
            key_components="FastAPI Gateway, SQLite WAL Concurrency, Autonomous Guardrail Daemon, Multi-Stakeholder Responsive UI, WhatsApp Webhook Engine",
            guardrail_linkage="GRD-SDLC-005, GRD-SECR-008"
        ),
        ArchitectureBlueprint(
            blueprint_code="ARCH-SEC-002",
            title="Zero-Trust Defense-in-Depth Security & Incident Response Architecture",
            architecture_type="Security_Boundary",
            module_pillar="Cybersecurity & Statutory Compliance",
            standard_alignment="CERT-In Directions 2022 / ISO/IEC 27001:2022",
            diagram_mermaid=(
                "graph LR\n"
                "    External[External Threat Actors / Web Traffic] --> Perimeter[WAF & Reverse Proxy Perimeter]\n"
                "    Perimeter --> Auth[Zero-Trust JWT + Passkey MFA Gate]\n"
                "    Auth --> App[Asperion Application Core]\n"
                "    App --> SIEM[Wazuh SIEM & Audit Logger]\n"
                "    SIEM --> Triage{P1 Critical Threat?}\n"
                "    Triage -- Yes --> Timer[CERT-In 6-Hour SLA Clock Locked]\n"
                "    Timer --> IR[War Room Activation & Containment]\n"
                "    IR --> Dispatch[Automated Report to incident@cert-in.org.in]\n"
                "    Triage -- No --> Standard[Standard SOC Ticket & Patch]"
            ),
            description="Defense-in-depth architecture showcasing the zero-trust perimeter, continuous SIEM telemetry monitoring, and the automated CERT-In 6-hour escalation workflow.",
            key_components="WAF Reverse Proxy, JWT Passkey MFA, SIEM Integration, Automated CERT-In 6-Hour Timer, Forensics Vault",
            guardrail_linkage="GRD-CERT-007, GRD-SECR-008, GRD-DPDP-003"
        ),
        ArchitectureBlueprint(
            blueprint_code="ARCH-DATA-003",
            title="Enterprise Data Flow, Entity Relational & Statutory Pipeline",
            architecture_type="Data_Flowchart",
            module_pillar="Financials, Procurement & Governance",
            standard_alignment="Companies Act 2013 / MSMED Act 2006 / GSTN / MCA21",
            diagram_mermaid=(
                "flowchart TD\n"
                "    Req[Purchase Requisition] --> PO[Purchase Order]\n"
                "    PO --> GRN[Goods Received Note & QC Record]\n"
                "    GRN --> Bill[Vendor AP Tax Invoice]\n"
                "    Bill --> Match[Autonomous 3-Way Match Validation]\n"
                "    Match --> Tax[TDS u/s 194Q/194C & Input GST Credit Engine]\n"
                "    Tax --> Bank[Open Banking API Batch File: HDFC / ICICI]\n"
                "    Bank --> Disburse[Real-Time RTGS/NEFT Statutory Disbursal]\n"
                "    Disburse --> Ledger[General Ledger Posting & MCA Compliance]"
            ),
            description="End-to-end data flow tracing a commercial transaction from initial purchase requisition through 3-way matching, statutory tax withholding, and automated bank disbursement.",
            key_components="Requisition Ledger, PO Dispatche, GRN QC Verifier, 3-Way Match Algorithm, Banking Disbursal Batch",
            guardrail_linkage="GRD-FIN-001, GRD-MSME-002, GRD-DOA-006"
        )
    ]
    for b in blueprints:
        if not db.query(ArchitectureBlueprint).filter(ArchitectureBlueprint.blueprint_code == b.blueprint_code).first():
            db.add(b)
    db.flush()

    # 3. Execution Logs
    logs = [
        GuardrailExecutionLog(
            execution_id="GEX-2026-001",
            rule_code="GRD-FIN-001",
            module="Finance",
            entity_reference="APB-2026-003",
            evaluation_result="PASSED",
            trigger_payload_summary="3-way match verified against PO-2026-001 and GRN-2026-001 with 0% variance.",
            action_taken="Approved for Payment Batch",
            evaluated_at=datetime.utcnow() - timedelta(hours=2)
        ),
        GuardrailExecutionLog(
            execution_id="GEX-2026-002",
            rule_code="GRD-MSME-002",
            module="Procurement_MSME",
            entity_reference="APB-2026-002",
            evaluation_result="PASSED",
            trigger_payload_summary="Nexus Micro Systems (Micro enterprise) bill age is 12 days, well within 45-day SLA.",
            action_taken="Queued in Priority Batch",
            evaluated_at=datetime.utcnow() - timedelta(hours=1, minutes=30)
        ),
        GuardrailExecutionLog(
            execution_id="GEX-2026-003",
            rule_code="GRD-HRMS-004",
            module="HRMS_Mobility",
            entity_reference="ATT-BLR-041",
            evaluation_result="AUTO_HEALED",
            trigger_payload_summary="Punch at 248m boundary with 86.4% liveness; clock jitter corrected via local NTP drift algorithm.",
            action_taken="Auto-Regularized & Verified",
            evaluated_at=datetime.utcnow() - timedelta(hours=1)
        ),
        GuardrailExecutionLog(
            execution_id="GEX-2026-004",
            rule_code="GRD-SDLC-005",
            module="DevSecOps",
            entity_reference="PIPE-FEAT-2026-04",
            evaluation_result="PASSED",
            trigger_payload_summary="CI/CD Run passed with 0 SAST CVEs, 94.2% test coverage, and clean secret leak scan.",
            action_taken="Allowed Merge to main",
            evaluated_at=datetime.utcnow() - timedelta(minutes=45)
        ),
        GuardrailExecutionLog(
            execution_id="GEX-2026-005",
            rule_code="GRD-DOA-006",
            module="Governance_DOA",
            entity_reference="PR-2026-003",
            evaluation_result="PASSED",
            trigger_payload_summary="PR estimated at INR 1,45,000 correctly escalated and approved by Sole Director Varadi Vijay.",
            action_taken="Authorized PO Generation",
            evaluated_at=datetime.utcnow() - timedelta(minutes=20)
        ),
        GuardrailExecutionLog(
            execution_id="GEX-2026-006",
            rule_code="GRD-CERT-007",
            module="SecOps",
            entity_reference="SEC-INC-2026-001",
            evaluation_result="PASSED",
            trigger_payload_summary="P1 brute force threat contained within 45 mins; preliminary report drafted at 1.2 hours.",
            action_taken="Statutory Window Met (<6h)",
            evaluated_at=datetime.utcnow() - timedelta(minutes=10)
        )
    ]
    for l in logs:
        if not db.query(GuardrailExecutionLog).filter(GuardrailExecutionLog.execution_id == l.execution_id).first():
            db.add(l)
    db.commit()


def _seed_ai_and_cloud_infrastructure(db):
    """Seeds AI model endpoints, MCP servers, hybrid cloud topology, certificates, and alert rules."""
    # 1. AI Model Endpoints (Gemini 2.5 Pro, Claude 3.7 Sonnet, DeepSeek-R1, OpenAI GPT-4.5)
    ai_models = [
        AIModelEndpoint(
            endpoint_code="AI-GEMINI-25-PRO",
            model_name="Gemini 2.5 Pro (Multimodal Reasoning)",
            provider="Google Cloud Vertex AI",
            model_family="Multimodal Reasoning LLM",
            context_window_tokens=2097152, # 2M token context
            rpm_limit=360,
            tpm_limit=2000000,
            avg_latency_ms=380.0,
            cost_per_million_tokens_inr=110.0,
            monthly_budget_inr=30000.0,
            current_month_usage_inr=12400.0,
            status="Active",
            api_key_vault_ref="SEC-ROT-001 (Encrypted Vault)"
        ),
        AIModelEndpoint(
            endpoint_code="AI-CLAUDE-37-SONNET",
            model_name="Claude 3.7 Sonnet (Hybrid Thinking)",
            provider="Anthropic Bedrock",
            model_family="Code & Extended Thinking LLM",
            context_window_tokens=200000,
            rpm_limit=250,
            tpm_limit=800000,
            avg_latency_ms=450.0,
            cost_per_million_tokens_inr=240.0,
            monthly_budget_inr=25000.0,
            current_month_usage_inr=9800.0,
            status="Active",
            api_key_vault_ref="SEC-ROT-002 (AWS Bedrock IAM Role)"
        ),
        AIModelEndpoint(
            endpoint_code="AI-DEEPSEEK-R1",
            model_name="DeepSeek-R1 (Open Weights Reasoning)",
            provider="Self-Hosted Kubernetes vLLM",
            model_family="Reasoning & Math Engine",
            context_window_tokens=128000,
            rpm_limit=500,
            tpm_limit=1500000,
            avg_latency_ms=290.0,
            cost_per_million_tokens_inr=45.0,
            monthly_budget_inr=15000.0,
            current_month_usage_inr=4200.0,
            status="Active",
            api_key_vault_ref="SEC-ROT-003 (K8s mTLS Cert)"
        ),
        AIModelEndpoint(
            endpoint_code="AI-OPENAI-EMBED-3",
            model_name="text-embedding-3-large (3072 Dimensions)",
            provider="OpenAI Enterprise",
            model_family="Dense Vector Embedding",
            context_window_tokens=8191,
            rpm_limit=1000,
            tpm_limit=5000000,
            avg_latency_ms=85.0,
            cost_per_million_tokens_inr=10.5,
            monthly_budget_inr=5000.0,
            current_month_usage_inr=1150.0,
            status="Active",
            api_key_vault_ref="SEC-ROT-004 (Vault Token)"
        )
    ]
    for m in ai_models:
        if not db.query(AIModelEndpoint).filter(AIModelEndpoint.endpoint_code == m.endpoint_code).first():
            db.add(m)
    db.flush()

    # 2. Model Context Protocol (MCP) Servers
    mcp_servers = [
        MCPServerCatalog(
            server_id="MCP-SQLITE-ERP",
            name="Asperion Enterprise SQLite WAL MCP Server",
            protocol_version="2024-11-05",
            transport_type="stdio",
            endpoint_or_command="python -m app.mcp.enterprise_sqlite_server",
            module_pillar="Core Enterprise Architecture",
            auth_mode="Environment_Secret_Injection",
            exposed_tools_count=18,
            exposed_resources_count=8,
            exposed_prompts_count=4,
            is_connected=True,
            last_ping_status="Healthy (8.2ms)",
            description="Exposes structured tools to query financial vouchers, employee records, attendance punches, and guardrail rules via secure Model Context Protocol."
        ),
        MCPServerCatalog(
            server_id="MCP-AWS-BEDROCK",
            name="AWS Bedrock & CloudWatch Metrics MCP Bridge",
            protocol_version="2024-11-05",
            transport_type="stdio",
            endpoint_or_command="npx -y @modelcontextprotocol/server-aws",
            module_pillar="Cloud Infrastructure & SRE",
            auth_mode="IAM_OIDC_Role",
            exposed_tools_count=14,
            exposed_resources_count=6,
            exposed_prompts_count=2,
            is_connected=True,
            last_ping_status="Healthy (14.5ms)",
            description="Allows agentic inspection of AWS EKS cluster health, CloudWatch logs, and S3 document bucket backups."
        ),
        MCPServerCatalog(
            server_id="MCP-GITHUB-SDLC",
            name="GitHub Corporate Org & DevSecOps MCP Server",
            protocol_version="2024-11-05",
            transport_type="stdio",
            endpoint_or_command="npx -y @modelcontextprotocol/server-github",
            module_pillar="SDLC & Quality Engineering",
            auth_mode="GitHub_App_Private_Key",
            exposed_tools_count=16,
            exposed_resources_count=10,
            exposed_prompts_count=5,
            is_connected=True,
            last_ping_status="Healthy (11.0ms)",
            description="Automates Git PR code reviews, branch protection rule enforcement, and TruffleHog secret scanning."
        ),
        MCPServerCatalog(
            server_id="MCP-SLACK-WHATSAPP",
            name="Omni-Channel Incident Alert & Executive Bot MCP Gateway",
            protocol_version="2024-11-05",
            transport_type="sse",
            endpoint_or_command="http://127.0.0.1:8080/mcp/sse",
            module_pillar="Executive Governance & Alerts",
            auth_mode="Mutual_TLS",
            exposed_tools_count=8,
            exposed_resources_count=4,
            exposed_prompts_count=3,
            is_connected=True,
            last_ping_status="Healthy (5.8ms)",
            description="Enables AI agents to dispatch direct alert pings to Department Heads and verify two-factor acknowledgments."
        )
    ]
    for srv in mcp_servers:
        if not db.query(MCPServerCatalog).filter(MCPServerCatalog.server_id == srv.server_id).first():
            db.add(srv)
    db.flush()

    # 3. Cloud Infrastructure Topology
    cloud_nodes = [
        CloudInfrastructureTopology(
            node_code="CLD-K8S-MUM-01",
            cluster_or_service_name="Asperion Primary EKS Cluster (Mumbai)",
            cloud_provider="AWS",
            resource_type="EKS Kubernetes Managed Cluster",
            region="ap-south-1 (Mumbai)",
            availability_zone="ap-south-1a / ap-south-1b Multi-AZ",
            compute_capacity="6 Nodes (c6i.2xlarge, 48 vCPU, 96 GB RAM)",
            monthly_cost_inr=42000.0,
            uptime_sla_pct=99.995,
            current_health="Optimal",
            auto_scaling_enabled=True,
            zero_trust_ingress_verified=True,
            technical_lead="Head of Infrastructure (Priya Nair)"
        ),
        CloudInfrastructureTopology(
            node_code="CLD-RDS-WAL-01",
            cluster_or_service_name="Asperion High-Performance DB & Read Replica",
            cloud_provider="AWS",
            resource_type="Transactional DB Multi-AZ WAL Instance",
            region="ap-south-1 (Mumbai)",
            availability_zone="ap-south-1a Primary / 1b Standby",
            compute_capacity="db.r6g.xlarge (4 vCPU, 32 GB RAM, Provisioned IOPS 5000)",
            monthly_cost_inr=28000.0,
            uptime_sla_pct=99.999,
            current_health="Optimal",
            auto_scaling_enabled=True,
            zero_trust_ingress_verified=True,
            technical_lead="Head of Infrastructure (Priya Nair)"
        ),
        CloudInfrastructureTopology(
            node_code="CLD-CF-EDGE-01",
            cluster_or_service_name="Cloudflare Enterprise Zero-Trust Edge & WAF",
            cloud_provider="Cloudflare",
            resource_type="Global Anycast CDN & DDoS Shield",
            region="Global (285+ Cities, BLR Local PoP)",
            availability_zone="Anycast Edge Fabric",
            compute_capacity="Unlimited Edge Ingress, 100 Gbps DDoS Scrubbing",
            monthly_cost_inr=15000.0,
            uptime_sla_pct=100.00,
            current_health="Optimal",
            auto_scaling_enabled=True,
            zero_trust_ingress_verified=True,
            technical_lead="CISO / SecOps Lead"
        ),
        CloudInfrastructureTopology(
            node_code="CLD-DR-HYD-02",
            cluster_or_service_name="Disaster Recovery Standby Cluster (Hyderabad)",
            cloud_provider="AWS",
            resource_type="Warm Standby Secondary EKS",
            region="ap-south-2 (Hyderabad)",
            availability_zone="ap-south-2a Standby",
            compute_capacity="2 Nodes (Pilot Light, Auto-expands to 8 in failover)",
            monthly_cost_inr=12000.0,
            uptime_sla_pct=99.95,
            current_health="Optimal",
            auto_scaling_enabled=True,
            zero_trust_ingress_verified=True,
            technical_lead="Head of Infrastructure (Priya Nair)"
        )
    ]
    for c in cloud_nodes:
        if not db.query(CloudInfrastructureTopology).filter(CloudInfrastructureTopology.node_code == c.node_code).first():
            db.add(c)
    db.flush()

    # 4. Security & Authenticity Certificates
    certs = [
        SecurityAuthenticityCertificate(
            cert_code="AUTH-CORP-DSC-01",
            certificate_name="Class 3 Corporate Digital Signature Certificate (DSC)",
            cert_type="Corporate_Digital_Signature_Class3",
            issuing_authority="e-Mudhra CA / CCA India",
            subject_entity="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED - Director Varadi Vijay",
            public_key_fingerprint="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            valid_from=date(2026, 6, 10),
            valid_until=date(2028, 6, 10),
            days_until_expiry=730,
            key_algorithm="RSA 4096-bit (FIPS 140-3 Hardware Token)",
            status="Valid & Trusted",
            fips_compliance_level="FIPS 140-3 Level 3 Crypto Token"
        ),
        SecurityAuthenticityCertificate(
            cert_code="AUTH-TLS-WILDCARD-02",
            certificate_name="Wildcard SSL/TLS *.asperiondigital.com Certificate",
            cert_type="TLS_Wildcard_Production",
            issuing_authority="Let's Encrypt Authority X3",
            subject_entity="*.asperiondigital.com (Asperion Digital Technologies)",
            public_key_fingerprint="7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
            valid_from=date(2026, 6, 15),
            valid_until=date(2026, 9, 15),
            days_until_expiry=88,
            key_algorithm="ECDSA (secp384r1) / SHA-384",
            status="Valid & Trusted",
            fips_compliance_level="TLS 1.3 Strict Cipher Suites"
        ),
        SecurityAuthenticityCertificate(
            cert_code="AUTH-DOC-SEAL-03",
            certificate_name="Official Automated PDF & Document Tamper-Evident Seal",
            cert_type="Document_Tamper_Evident_Key",
            issuing_authority="DigiCert Document Signing CA",
            subject_entity="Asperion Document Vault & Automated Billing Engine",
            public_key_fingerprint="c2543fff3bfa6f144c383fe0e78d4565ad85e7b8153016adc1e1e4000abc6d46",
            valid_from=date(2026, 6, 12),
            valid_until=date(2027, 6, 12),
            days_until_expiry=360,
            key_algorithm="ED25519 & X.509 PAdES-B-LT Format",
            status="Valid & Trusted",
            fips_compliance_level="Adobe Approved Trust List (AATL)"
        )
    ]
    for cert in certs:
        if not db.query(SecurityAuthenticityCertificate).filter(SecurityAuthenticityCertificate.cert_code == cert.cert_code).first():
            db.add(cert)
    db.flush()

    # 5. Executive Alert Rules to Concerned Heads
    alert_rules = [
        ExecutiveAlertRule(
            rule_code="EAR-FIN-LIQ-01",
            title="Treasury Working Capital Low Runway Alert",
            trigger_condition="Current Bank Balance < INR 1,50,000 OR 13-week runway < 6 weeks",
            target_head_role="Sole Director & Head of Finance (Varadi Vijay)",
            target_head_email="varadivijay@asperiondigital.com",
            target_head_whatsapp="+919886012345",
            dispatch_channels="WhatsApp_Cloud_API, Email_SES, In_App_Cockpit",
            escalation_window_mins=15,
            auto_sms_enabled=True,
            is_active=True
        ),
        ExecutiveAlertRule(
            rule_code="EAR-SEC-P1-02",
            title="P1-Critical Cyber Incident / CERT-In 6-Hour Countdown Alert",
            trigger_condition="SecurityIncident severity == 'P1-Critical' OR Ransomware Detection",
            target_head_role="CISO & Sole Director",
            target_head_email="security@asperiondigital.com",
            target_head_whatsapp="+919886012345",
            dispatch_channels="WhatsApp_Cloud_API, PagerDuty, In_App_Cockpit",
            escalation_window_mins=5,
            auto_sms_enabled=True,
            is_active=True
        ),
        ExecutiveAlertRule(
            rule_code="EAR-MSME-45D-03",
            title="MSMED Act 2006 45-Day Statutory Vendor Overdue Warning",
            trigger_condition="Vendor.msme_registered == True AND APBill age >= 38 days",
            target_head_role="Head of Procurement & Accounts Payable",
            target_head_email="procurement@asperiondigital.com",
            target_head_whatsapp="+919886012345",
            dispatch_channels="WhatsApp_Cloud_API, Email_SES, In_App_Cockpit",
            escalation_window_mins=30,
            auto_sms_enabled=True,
            is_active=True
        ),
        ExecutiveAlertRule(
            rule_code="EAR-DEV-SLA-04",
            title="Client Project Milestone Delivery Delay / EVM Warning",
            trigger_condition="Project SPI < 0.85 OR Critical Client SLA Ticket Breached",
            target_head_role="Head of PMO & Project Delivery (Arjun Sharma)",
            target_head_email="delivery@asperiondigital.com",
            target_head_whatsapp="+919886012345",
            dispatch_channels="WhatsApp_Cloud_API, In_App_Cockpit",
            escalation_window_mins=20,
            auto_sms_enabled=True,
            is_active=True
        )
    ]
    for rule in alert_rules:
        if not db.query(ExecutiveAlertRule).filter(ExecutiveAlertRule.rule_code == rule.rule_code).first():
            db.add(rule)
    db.commit()


def _seed_iso_standards_and_grievances(db):
    """Seeds acquired ISO certifications, clause controls worksheets, audit reports, CAPAs, and grievances."""
    # 1. Acquired ISO Certifications (ISO 9001, ISO 27001, ISO 42001, ISO 20000-1, ISO 22301)
    isos = [
        ISOCertificationMaster(
            standard_code="ISO-9001:2015",
            standard_name="Quality Management Systems (QMS)",
            scope_description="Design, Full-Stack Engineering, Cloud Deployment, Quality Assurance, and Client Delivery of Enterprise Software Platforms and AI Solutions.",
            certificate_number="ADT-QMS-2026-9001",
            accreditation_body="IAF / NABCB Accredited Registrar (BSI Assurance India)",
            issue_date=date(2026, 6, 15),
            expiry_date=date(2029, 6, 14),
            surveillance_audit_due=date(2027, 5, 15),
            management_representative="Sole Member & Director (Varadi Vijay)",
            lead_auditor="BSI Lead Quality Auditor (Dr. R. Ramanathan)",
            status="Active & Certified",
            non_conformance_count=0
        ),
        ISOCertificationMaster(
            standard_code="ISO/IEC-27001:2022",
            standard_name="Information Security Management Systems (ISMS)",
            scope_description="Protection of Intellectual Property, Client Source Code, PII Data, Cloud Infrastructure, and Corporate Digital Vaults in alignment with Annex A Controls.",
            certificate_number="ADT-ISMS-2026-27001",
            accreditation_body="IAF / UKAS Accredited Certification (TUV SUD South Asia)",
            issue_date=date(2026, 6, 18),
            expiry_date=date(2029, 6, 17),
            surveillance_audit_due=date(2027, 5, 20),
            management_representative="Head of Infrastructure & SecOps (Priya Nair)",
            lead_auditor="TUV Lead Auditor (K. Viswanathan)",
            status="Active & Certified",
            non_conformance_count=0
        ),
        ISOCertificationMaster(
            standard_code="ISO/IEC-42001:2023",
            standard_name="Artificial Intelligence Management Systems (AIMS)",
            scope_description="Governance, Safety Alignment, Ethical Evaluation, Bias Mitigation, Prompt Injection Guardrails, and Responsible Lifecycle Operations of Enterprise Multimodal AI.",
            certificate_number="ADT-AIMS-2026-42001",
            accreditation_body="International AI Assurance Board & ANSI National Accreditation Board (ANAB)",
            issue_date=date(2026, 6, 20),
            expiry_date=date(2029, 6, 19),
            surveillance_audit_due=date(2027, 5, 25),
            management_representative="Lead AI Systems Architect (Arjun Sharma)",
            lead_auditor="Global AI Safety Assessor (Elena Rostova)",
            status="Active & Certified",
            non_conformance_count=0
        ),
        ISOCertificationMaster(
            standard_code="ISO/IEC-20000-1:2018",
            standard_name="Information Technology Service Management (ITSM)",
            scope_description="End-to-End Delivery of Enterprise SaaS, 24x7 Customer Service Desk, Incident Resolution, Problem Management, and Service Level Agreement (SLA) Compliance.",
            certificate_number="ADT-ITSM-2026-20000",
            accreditation_body="APMG International & NABCB Accredited Body (DNV Business Assurance)",
            issue_date=date(2026, 6, 22),
            expiry_date=date(2029, 6, 21),
            surveillance_audit_due=date(2027, 5, 30),
            management_representative="Service Delivery Head (Ananya Sen)",
            lead_auditor="DNV Senior Lead Assessor (M. Sundaram)",
            status="Active & Certified",
            non_conformance_count=0
        ),
        ISOCertificationMaster(
            standard_code="ISO-22301:2019",
            standard_name="Security and Resilience - Business Continuity Management Systems (BCMS)",
            scope_description="Resilience, Business Impact Analysis (BIA), Hybrid Cloud Failover (Mumbai to Hyderabad), Cyber Disaster Recovery, and Statutory Supply Continuity.",
            certificate_number="ADT-BCMS-2026-22301",
            accreditation_body="Disaster Recovery Institute International & Bureau Veritas (BVQI)",
            issue_date=date(2026, 6, 25),
            expiry_date=date(2029, 6, 24),
            surveillance_audit_due=date(2027, 6, 1),
            management_representative="Chief Operating Officer & Sole Director",
            lead_auditor="Bureau Veritas Lead Assessor (Rajesh Kulkarni)",
            status="Active & Certified",
            non_conformance_count=0
        )
    ]
    for iso in isos:
        if not db.query(ISOCertificationMaster).filter(ISOCertificationMaster.standard_code == iso.standard_code).first():
            db.add(iso)
    db.flush()

    # 2. Detailed ISO Clause Controls & Implementation Worksheets
    controls = [
        # ISO 9001:2015 Clauses
        ISOClauseControl(
            control_code="ISO9001-CL-4.4",
            standard_code="ISO-9001:2015",
            clause_number="4.4",
            title="Quality Management System and Its Processes",
            control_domain="Context of the Organization",
            requirement_summary="Establish, implement, maintain and continually improve a quality management system, including the processes needed and their interactions.",
            implementation_mechanism="Integrated Process Flowcharts (FC-FIN-001 to FC-PROC-006) with input/output traceability and SLA KPI gates.",
            evidence_vault_ref="DOC-QMS-001, ARCH-E2E-001",
            maturity_level="Level 5 - Optimized",
            compliance_score_pct=100.0,
            control_owner="Sole Director (Varadi Vijay)",
            is_compliant=True
        ),
        ISOClauseControl(
            control_code="ISO9001-CL-8.2",
            standard_code="ISO-9001:2015",
            clause_number="8.2",
            title="Requirements for Products and Services & Client Review",
            control_domain="Operation",
            requirement_summary="Review of contractual requirements before commitment to ensure scope feasibility, acceptance criteria, and SLA boundaries.",
            implementation_mechanism="Stage-Gate 1 & 2 PMO intake matrices, signed SOWs, and automated client onboarding KYC workflows.",
            evidence_vault_ref="SOW-HEL-2026-001, PMO-GATE-01",
            maturity_level="Level 4 - Managed & Measured",
            compliance_score_pct=100.0,
            control_owner="Head of PMO (Arjun Sharma)",
            is_compliant=True
        ),
        ISOClauseControl(
            control_code="ISO9001-CL-9.1.2",
            standard_code="ISO-9001:2015",
            clause_number="9.1.2",
            title="Customer Satisfaction & Feedback Monitoring",
            control_domain="Performance Evaluation",
            requirement_summary="Monitor customers' perceptions of the degree to which their needs and expectations have been fulfilled.",
            implementation_mechanism="Automated CSAT / NPS post-sprint surveys, quarterly client scorecards, and formal grievance resolution.",
            evidence_vault_ref="CSAT-Q1-2026, GRV-REG-01",
            maturity_level="Level 4 - Managed & Measured",
            compliance_score_pct=98.5,
            control_owner="Delivery Head (Ananya Sen)",
            is_compliant=True
        ),
        ISOClauseControl(
            control_code="ISO9001-CL-10.2",
            standard_code="ISO-9001:2015",
            clause_number="10.2",
            title="Nonconformity and Corrective Action (CAPA)",
            control_domain="Improvement",
            requirement_summary="React to nonconformities, evaluate root causes using 5 Whys / Fishbone, implement corrective actions, and verify effectiveness.",
            implementation_mechanism="Dedicated ISOCorrectiveActionWorksheet ledger with automated SLA tracking and management sign-off.",
            evidence_vault_ref="CAPA-ISO-2026-001",
            maturity_level="Level 5 - Optimized",
            compliance_score_pct=100.0,
            control_owner="Quality Assurance Lead",
            is_compliant=True
        ),

        # ISO/IEC 27001:2022 Clauses & Controls
        ISOClauseControl(
            control_code="ISO27001-A.5.15",
            standard_code="ISO/IEC-27001:2022",
            clause_number="A.5.15",
            title="Access Control & Least Privilege",
            control_domain="Organizational Controls",
            requirement_summary="Enforce role-based access control (RBAC), multi-factor authentication (MFA), and zero-trust credential segregation.",
            implementation_mechanism="OAuth2 JWT tokens, FIDO2 WebAuthn Passkeys, and isolated stakeholder login portals for Clients, Employees, and Vendors.",
            evidence_vault_ref="DOC-SEC-002, ARCH-SEC-002",
            maturity_level="Level 5 - Optimized",
            compliance_score_pct=100.0,
            control_owner="Head of Infrastructure (Priya Nair)",
            is_compliant=True
        ),
        ISOClauseControl(
            control_code="ISO27001-A.8.25",
            standard_code="ISO/IEC-27001:2022",
            clause_number="A.8.25",
            title="Secure Development Lifecycle (SDLC)",
            control_domain="Technological Controls",
            requirement_summary="Rules for secure development of software and systems shall be established and applied across the lifecycle.",
            implementation_mechanism="7-stage SDLC gate, mandatory TruffleHog secret scanning, Bandit SAST with zero CVE tolerance (GRD-SDLC-005), and CAB approval.",
            evidence_vault_ref="DOC-SDLC-004, GRD-SDLC-005",
            maturity_level="Level 5 - Optimized",
            compliance_score_pct=100.0,
            control_owner="Lead Architect (Arjun Sharma)",
            is_compliant=True
        ),

        # ISO/IEC 42001:2023 Clauses (AI Management)
        ISOClauseControl(
            control_code="ISO42001-CL-6.1",
            standard_code="ISO/IEC-42001:2023",
            clause_number="6.1",
            title="Actions to Address Risks & Opportunities of AI Systems",
            control_domain="Planning & AI Risk Assessment",
            requirement_summary="Assess risks related to AI bias, hallucination, prompt injection, data poisoning, privacy leakage, and autonomous agent behavior.",
            implementation_mechanism="Pre-execution prompt sanitization, model rate limiting (RPM/TPM), and human-in-the-loop validation for financial disbursements.",
            evidence_vault_ref="DOC-AI-GOV-01, AI-GEMINI-25-PRO",
            maturity_level="Level 4 - Managed & Measured",
            compliance_score_pct=96.0,
            control_owner="Lead AI Systems Architect (Arjun Sharma)",
            is_compliant=True
        ),
        ISOClauseControl(
            control_code="ISO42001-CL-8.3",
            standard_code="ISO/IEC-42001:2023",
            clause_number="8.3",
            title="AI System Transparency & Explainability",
            control_domain="Operation & Trustworthiness",
            requirement_summary="Provide clear documentation on model boundaries, training provenance, and verifiable confidence scoring for end users.",
            implementation_mechanism="Structured Model Context Protocol (MCP) tool schemas and explicit confidence score tagging in attendance biometric engines.",
            evidence_vault_ref="MCP-SQLITE-ERP, DOC-ARCH-001",
            maturity_level="Level 4 - Managed & Measured",
            compliance_score_pct=95.0,
            control_owner="Lead AI Systems Architect",
            is_compliant=True
        ),

        # ISO/IEC 20000-1:2018 Clauses (ITSM)
        ISOClauseControl(
            control_code="ISO20000-CL-8.5",
            standard_code="ISO/IEC-20000-1:2018",
            clause_number="8.5",
            title="Service Level Management & Incident Resolution",
            control_domain="Service Operations & Delivery",
            requirement_summary="Define service catalog, monitor performance against SLAs, and manage incidents from logging through root-cause resolution.",
            implementation_mechanism="Internal Service Desk with P1-P4 SLA deadlines, multi-department ticketing, and automated escalation timers.",
            evidence_vault_ref="IT-TKT-2026-001, DOC-ITSM-01",
            maturity_level="Level 4 - Managed & Measured",
            compliance_score_pct=98.0,
            control_owner="Service Delivery Head (Ananya Sen)",
            is_compliant=True
        ),

        # ISO 22301:2019 Clauses (BCMS)
        ISOClauseControl(
            control_code="ISO22301-CL-8.2",
            standard_code="ISO-22301:2019",
            clause_number="8.2",
            title="Business Impact Analysis (BIA) & Risk Assessment",
            control_domain="Business Continuity Operation",
            requirement_summary="Identify critical business activities, recovery time objectives (RTO <= 1 hour), and recovery point objectives (RPO <= 15 minutes).",
            implementation_mechanism="Multi-Region AWS EKS pilot light in Hyderabad (CLD-DR-HYD-02), continuous WAL database archiving, and automated tabletop drill logs.",
            evidence_vault_ref="DOC-BCMS-BIA-01, CLD-DR-HYD-02",
            maturity_level="Level 5 - Optimized",
            compliance_score_pct=100.0,
            control_owner="Head of Infrastructure (Priya Nair)",
            is_compliant=True
        )
    ]
    for c in controls:
        if not db.query(ISOClauseControl).filter(ISOClauseControl.control_code == c.control_code).first():
            db.add(c)
    db.flush()

    # 3. ISO Audit Inspections
    audits = [
        ISOAuditInspection(
            audit_code="AUD-ISO9001-2026-SURV1",
            standard_code="ISO-9001:2015",
            audit_type="External Registrar Surveillance",
            audit_date=date(2026, 6, 16),
            audited_department="Engineering, PMO, SecOps & Delivery",
            lead_auditor="BSI Lead Quality Auditor (Dr. R. Ramanathan)",
            auditee_representative="Sole Member & Director (Varadi Vijay)",
            findings_summary="Comprehensive verification of end-to-end SDLC quality gates, automated 3-way matching, and customer satisfaction surveys. All sampled projects conformed to quality manual requirements.",
            major_nc_count=0,
            minor_nc_count=0,
            ofi_count=1,
            audit_outcome="Conforming - Recommendation for Continuation",
            status="Completed & Closed"
        ),
        ISOAuditInspection(
            audit_code="AUD-ISO27001-2026-INT",
            standard_code="ISO/IEC-27001:2022",
            audit_type="Internal Management Audit",
            audit_date=date(2026, 6, 20),
            audited_department="Cloud Infrastructure & Identity Access Management",
            lead_auditor="Priya Nair (SecOps Lead)",
            auditee_representative="Cloud Infrastructure Squad",
            findings_summary="Internal ISMS audit of access control, root MFA enforcement, and CERT-In 6-hour incident response workflow. Verified 90-day cryptographic secret rotation and zero public S3 bucket exposure.",
            major_nc_count=0,
            minor_nc_count=0,
            ofi_count=0,
            audit_outcome="Conforming - Zero Non-Conformances",
            status="Completed & Closed"
        ),
        ISOAuditInspection(
            audit_code="AUD-ISO42001-2026-AIMS",
            standard_code="ISO/IEC-42001:2023",
            audit_type="Internal AI Safety Audit",
            audit_date=date(2026, 6, 24),
            audited_department="AI Engineering & Prompt Architecture Squad",
            lead_auditor="Arjun Sharma (Lead Architect)",
            auditee_representative="AI Core Developer Team",
            findings_summary="Evaluated prompt injection defenses, LLM spend caps, and token context tracking. Sampled Gemini 2.5 Pro and Claude 3.7 Sonnet usage; observed proper vault credential encryption.",
            major_nc_count=0,
            minor_nc_count=0,
            ofi_count=1,
            audit_outcome="Conforming - AI Safety Controls Operational",
            status="Completed & Closed"
        )
    ]
    for a in audits:
        if not db.query(ISOAuditInspection).filter(ISOAuditInspection.audit_code == a.audit_code).first():
            db.add(a)
    db.flush()

    # 4. Corrective and Preventive Action (CAPA) Worksheets
    capas = [
        ISOCorrectiveActionWorksheet(
            capa_number="CAPA-QMS-2026-001",
            source_type="Audit Non-Conformance",
            standard_code="ISO-9001:2015",
            problem_statement="A 2.5% discrepancy between Purchase Order unit price and vendor tax invoice in cloud tooling procurement was detected during pre-payment staging.",
            immediate_containment_action="Autonomous FinOps Engine (GRD-FIN-001) halted invoice disbursal and placed voucher on Discrepancy Hold.",
            root_cause_analysis_method="5 Whys Root Cause Analysis",
            root_cause_findings="Vendor applied updated Q2 rate card without submitting formal contract amendment addendum to procurement desk.",
            preventive_corrective_action="Updated Contract Lifecycle Management (CLM) to require signed digital addenda before new rate cards can be billed in Accounts Payable.",
            action_owner="Head of Procurement & Accounts Payable",
            target_closure_date=date(2026, 6, 30),
            actual_closure_date=date(2026, 6, 28),
            effectiveness_verified=True,
            verifier_name="Director Varadi Vijay (Quality Lead)",
            status="Closed & Verified"
        ),
        ISOCorrectiveActionWorksheet(
            capa_number="CAPA-AIMS-2026-002",
            source_type="AI Incident",
            standard_code="ISO/IEC-42001:2023",
            problem_statement="Developer prompt in staging environment triggered an unexpected token spike of 180,000 tokens during automated test suite execution.",
            immediate_containment_action="Automated TPM rate limiter throttled secondary worker thread and alerted CISO channel.",
            root_cause_analysis_method="Ishikawa Fishbone & Log Analysis",
            root_cause_findings="Unit test suite lacked input truncation guardrail on sample mock document payload.",
            preventive_corrective_action="Added client-side token counting pre-check and strict 32k payload chunker before dispatching to Vertex API.",
            action_owner="Lead AI Systems Architect (Arjun Sharma)",
            target_closure_date=date(2026, 7, 10),
            actual_closure_date=date(2026, 7, 5),
            effectiveness_verified=True,
            verifier_name="Director Varadi Vijay (Quality Lead)",
            status="Closed & Verified"
        )
    ]
    for cp in capas:
        if not db.query(ISOCorrectiveActionWorksheet).filter(ISOCorrectiveActionWorksheet.capa_number == cp.capa_number).first():
            db.add(cp)
    db.flush()

    # 5. Formal Grievance Redressal Records
    grievances = [
        FormalGrievanceRecord(
            grievance_id="GRV-2026-001",
            stakeholder_type="Client",
            stakeholder_name="Helios Cloud Technologies (Sponsor: Rajesh Mehta)",
            stakeholder_email="rmehta@helioscloud.com",
            category="Quality of Deliverable",
            severity="Medium",
            subject="Sprint 2 Microservice API Documentation Format Request",
            description="Client requested OpenAPI specification Swagger JSON export in addition to standard Markdown architecture notes for their internal security review.",
            assigned_redressal_officer="Sole Director (Varadi Vijay)",
            statutory_sla_days=7,
            acknowledgment_sent=True,
            investigation_notes="Investigated with PMO Lead Arjun Sharma; verified FastAPI automatically generates OpenAPI v3 JSON at /openapi.json.",
            resolution_details="Shared interactive Swagger UI link and automated raw OpenAPI JSON export. Client verified and accepted resolution within 24 hours.",
            closure_date=date(2026, 6, 22),
            complainant_satisfied=True,
            csat_score=5,
            status="Resolved & Closed"
        ),
        FormalGrievanceRecord(
            grievance_id="GRV-2026-002",
            stakeholder_type="Employee",
            stakeholder_name="Priya Nair (Senior Security Engineer)",
            stakeholder_email="priya.nair@asperiondigital.com",
            category="Workplace Conduct & Mobility",
            severity="Low",
            subject="Geofence GPS Drift on High-Floor Indoor Punch",
            description="Employee noticed that attendance punch from the indoor third-floor meeting room occasionally registered 248m distance due to building RF shielding.",
            assigned_redressal_officer="People Operations Lead & Director",
            statutory_sla_days=5,
            acknowledgment_sent=True,
            investigation_notes="Inspected GPS coordinates in attendance audit logs; verified employee was inside the designated Horamavu HQ boundary.",
            resolution_details="Deployed self-healing anomaly auto-fix daemon with local Wi-Fi BSSID anchor verification to eliminate indoor GPS drift penalties.",
            closure_date=date(2026, 6, 24),
            complainant_satisfied=True,
            csat_score=5,
            status="Resolved & Closed"
        )
    ]
    for g in grievances:
        if not db.query(FormalGrievanceRecord).filter(FormalGrievanceRecord.grievance_id == g.grievance_id).first():
            db.add(g)
    db.commit()


def _seed_passkeys_and_zerotrust(db):
    """Seeds FIDO2 Passkeys, Zero-Trust Access Policies, and DR Simulation Tests."""
    # 1. Enrolled Passkeys (FIDO2 / WebAuthn Hardware & Platform Keys)
    passkeys = [
        PasskeyCredential(
            passkey_id="fido2-cred-varadivijay-yubi5c",
            user_email="varadivijay@asperiondigital.com",
            user_name="Varadi Vijay (Founder & Director)",
            device_name="YubiKey 5C NFC (Primary Token)",
            authenticator_type="Cross-Platform Hardware FIDO2 (YubiKey 5 Series)",
            aaguid="cb69481e-8ff7-4039-93ec-0a2729a1e67d",
            public_key_spki="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE9Z7z9X3q0B1xY4T7...",
            sign_count=42,
            user_verified=True,
            enrolled_at=datetime(2026, 6, 12, 10, 30, 0),
            last_used_at=datetime.utcnow() - timedelta(minutes=14),
            status="Active - Enforced",
            zero_trust_status="Compliant - Hardware Bound"
        ),
        PasskeyCredential(
            passkey_id="fido2-cred-priya-touchid",
            user_email="priya.nair@asperiondigital.com",
            user_name="Priya Nair (SecOps & Infrastructure Lead)",
            device_name="MacBook Pro Touch ID (SecOps Command)",
            authenticator_type="Platform Authenticator (Apple Secure Enclave)",
            aaguid="00000000-0000-0000-0000-000000000000",
            public_key_spki="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE2F8a1K7mN4Q0Z8V2...",
            sign_count=28,
            user_verified=True,
            enrolled_at=datetime(2026, 6, 14, 11, 15, 0),
            last_used_at=datetime.utcnow() - timedelta(minutes=45),
            status="Active - Enforced",
            zero_trust_status="Compliant - Hardware Bound"
        ),
        PasskeyCredential(
            passkey_id="fido2-cred-arjun-winhello",
            user_email="arjun.sharma@asperiondigital.com",
            user_name="Arjun Sharma (Full-Stack Tech Lead)",
            device_name="ThinkPad Windows Hello Biometric",
            authenticator_type="Platform Authenticator (TPM 2.0 / Windows Hello)",
            aaguid="08987058-cadc-4b81-b6e1-30de50dcbe96",
            public_key_spki="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE7W3v2P9qL1mX6N5t...",
            sign_count=19,
            user_verified=True,
            enrolled_at=datetime(2026, 6, 15, 9, 45, 0),
            last_used_at=datetime.utcnow() - timedelta(hours=2),
            status="Active - Enforced",
            zero_trust_status="Compliant - Hardware Bound"
        ),
        PasskeyCredential(
            passkey_id="fido2-cred-ananya-yubikey",
            user_email="ananya.sen@asperiondigital.com",
            user_name="Ananya Sen (Finance & Treasury Lead)",
            device_name="YubiKey 5 Nano (Finance Vault Key)",
            authenticator_type="Cross-Platform Hardware FIDO2 (YubiKey 5 Series)",
            aaguid="cb69481e-8ff7-4039-93ec-0a2729a1e67d",
            public_key_spki="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5M9k3L1pQ4vB7X2w...",
            sign_count=14,
            user_verified=True,
            enrolled_at=datetime(2026, 6, 16, 14, 20, 0),
            last_used_at=datetime.utcnow() - timedelta(hours=5),
            status="Active - Enforced",
            zero_trust_status="Compliant - Hardware Bound"
        )
    ]
    for pk in passkeys:
        if not db.query(PasskeyCredential).filter(PasskeyCredential.passkey_id == pk.passkey_id).first():
            db.add(pk)

    # 2. Zero-Trust Network Access (ZTNA) Policies
    zt_policies = [
        ZeroTrustPolicy(
            policy_code="ZTNA-POL-001",
            policy_name="Production PostgreSQL & RDS Clusters Zero-Trust Gate",
            target_resource="AWS RDS PostgreSQL (10.0.1.0/24 Subnet)",
            required_privilege="Database Administrator / SecOps Superadmin",
            fido2_passkey_required=True,
            device_encryption_required=True,
            allowed_ip_ranges="122.172.84.110/32 (Horamavu HQ Static IP) / 10.8.0.0/24 (WireGuard Mesh)",
            session_timeout_minutes=30,
            enforcement_mode="Active_Blocking",
            is_active=True
        ),
        ZeroTrustPolicy(
            policy_code="ZTNA-POL-002",
            policy_name="AWS Management Console & Root Identity Center",
            target_resource="AWS IAM Identity Center / SSO Portal (ap-south-1)",
            required_privilege="Cloud Infrastructure Administrator",
            fido2_passkey_required=True,
            device_encryption_required=True,
            allowed_ip_ranges="Horamavu HQ Office IP / ZTNA WireGuard Tunnel",
            session_timeout_minutes=60,
            enforcement_mode="Active_Blocking",
            is_active=True
        ),
        ZeroTrustPolicy(
            policy_code="ZTNA-POL-003",
            policy_name="Internal GitLab Enterprise & Production CI/CD Gate",
            target_resource="gitlab.asperion.in / Kubernetes Cluster Deployments",
            required_privilege="DevOps Engineer / Release Commander",
            fido2_passkey_required=True,
            device_encryption_required=True,
            allowed_ip_ranges="Global WireGuard Mesh with mTLS Certificate Validation",
            session_timeout_minutes=120,
            enforcement_mode="Active_Blocking",
            is_active=True
        )
    ]
    for pol in zt_policies:
        if not db.query(ZeroTrustPolicy).filter(ZeroTrustPolicy.policy_code == pol.policy_code).first():
            db.add(pol)

    # 3. Disaster Recovery (DR) Simulation Drills (ISO 22301 Aligned)
    dr_tests = [
        DRSimulationTest(
            test_code="DR-DRILL-2026-Q2",
            test_type="Full Regional Failover Drill",
            simulated_scenario="Simulated total loss of primary AWS Mumbai ap-south-1 AZ-A & AZ-B infrastructure; DNS switchover via Route53 latency-based routing to Hyderabad warm standby.",
            target_cluster="Secondary EKS Warm Standby (ap-south-2 Hyderabad)",
            database_backup_point=datetime.utcnow() - timedelta(hours=3),
            actual_rto_minutes=18.5,
            target_rto_minutes=60.0,
            actual_rpo_minutes=2.1,
            target_rpo_minutes=15.0,
            data_loss_detected=False,
            test_outcome="PASSED - Exceeded ISO 22301 SLA",
            conducted_by="Head of Infrastructure (Priya Nair)",
            conducted_at=datetime(2026, 6, 25, 14, 0, 0),
            report_url="https://audit.asperion.in/reports/dr/2026-q2-failover.pdf"
        ),
        DRSimulationTest(
            test_code="DR-DRILL-2026-Q1",
            test_type="Point-in-Time Database Recovery (PITR) & Ransomware Scrub",
            simulated_scenario="Ransomware encryption canary triggered in secondary test subnet; full automated rollback to AWS Aurora snapshot with automated consistency checksum verification.",
            target_cluster="Isolated Sandbox Recovery VPC (ap-south-1)",
            database_backup_point=datetime.utcnow() - timedelta(days=1),
            actual_rto_minutes=24.2,
            target_rto_minutes=60.0,
            actual_rpo_minutes=0.8,
            target_rpo_minutes=15.0,
            data_loss_detected=False,
            test_outcome="PASSED - Zero Corruption Detected",
            conducted_by="DevSecOps Lead (Arjun Sharma)",
            conducted_at=datetime(2026, 6, 18, 16, 30, 0),
            report_url="https://audit.asperion.in/reports/dr/2026-q1-pitr.pdf"
        )
    ]
    for dr in dr_tests:
        if not db.query(DRSimulationTest).filter(DRSimulationTest.test_code == dr.test_code).first():
            db.add(dr)
    
    db.commit()


def _seed_cybersecurity_warroom(db):
    """Seeds Threat Intel IOCs, SIEM Alerts, Evidence Items, Playbooks, Vulnerabilities, and CERT-In Reports."""
    # 1. Threat Intelligence Indicators (IOCs)
    iocs = [
        ThreatIntelIndicator(
            ioc_id="ADT-IOC-001",
            ioc_type="IP_Address",
            ioc_value="198.51.100.42",
            threat_actor_group="APT29 / Nobelium C2 Proxy",
            confidence_score=95,
            mitre_technique="T1071.001 Web Protocols",
            action_taken="Blocked at Cloudflare WAF & AWS Firewall",
            source_feed="CERT-In Cyber Threat Advisory 2026-04",
            status="Active_Blocked"
        ),
        ThreatIntelIndicator(
            ioc_id="ADT-IOC-002",
            ioc_type="SHA256_Hash",
            ioc_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            threat_actor_group="LockBit 3.0 Ransomware Encryptor Payload",
            confidence_score=99,
            mitre_technique="T1486 Data Encrypted for Impact",
            action_taken="Quarantined by EDR Antivirus Agent",
            source_feed="CISA Known Exploited Vulnerability Alert",
            status="Active_Blocked"
        ),
        ThreatIntelIndicator(
            ioc_id="ADT-IOC-003",
            ioc_type="Domain",
            ioc_value="auth-verify-asperion-portal.com",
            threat_actor_group="Typosquatting Credential Harvester",
            confidence_score=92,
            mitre_technique="T1566.002 Spearphishing Link",
            action_taken="DNS Sinkholed via Route53 Resolver Firewall",
            source_feed="Internal Honeypot Signal",
            status="Active_Blocked"
        ),
        ThreatIntelIndicator(
            ioc_id="ADT-IOC-004",
            ioc_type="IP_Address",
            ioc_value="203.0.113.88",
            threat_actor_group="Mirai Botnet SSH Brute-Force Scanner",
            confidence_score=88,
            mitre_technique="T1110.001 Password Guessing",
            action_taken="Drop Policy at Perimeter WireGuard Gateway",
            source_feed="AWS GuardDuty Recon Signal",
            status="Active_Blocked"
        )
    ]
    for ioc in iocs:
        if not db.query(ThreatIntelIndicator).filter(ThreatIntelIndicator.ioc_id == ioc.ioc_id).first():
            db.add(ioc)

    # 2. Forensic Evidence Locker
    incident = db.query(SecurityIncident).first()
    inc_id = incident.id if incident else 1
    evidence_items = [
        EvidenceItem(
            evidence_id="ADT-EVD-001",
            incident_id=inc_id,
            item_name="CloudTrail S3 Exfiltration API Call Records",
            source_type="SIEM Logs",
            sha256_checksum="9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            storage_uri="s3://asperion-sec-evidence-vault/2026/evd-001-cloudtrail.json.gz",
            collected_by="Priya Nair (SecOps Lead)",
            custody_notes="Cryptographically signed and locked under AWS S3 Object Lock (Compliance Mode, 7 years)."
        ),
        EvidenceItem(
            evidence_id="ADT-EVD-002",
            incident_id=inc_id,
            item_name="Volatile RAM Memory Dump of Compromised Test Container",
            source_type="Memory Dump",
            sha256_checksum="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            storage_uri="s3://asperion-sec-evidence-vault/2026/evd-002-ram-dump.raw",
            collected_by="Forensic DFIR Specialist",
            custody_notes="Captured via LiME memory collector prior to host isolation."
        ),
        EvidenceItem(
            evidence_id="ADT-EVD-003",
            incident_id=inc_id,
            item_name="VPC Flow Logs Network Packet Capture (ap-south-1)",
            source_type="VPC Flow Logs",
            sha256_checksum="4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
            storage_uri="s3://asperion-sec-evidence-vault/2026/evd-003-vpc-flow.pcap",
            collected_by="Network Security Engineer",
            custody_notes="Filtered on destination port 443 with bidirectional session reassembly."
        )
    ]
    for ev in evidence_items:
        if not db.query(EvidenceItem).filter(EvidenceItem.evidence_id == ev.evidence_id).first():
            db.add(ev)

    # 3. Incident Response Playbooks (NIST SP 800-61 aligned)
    playbooks = [
        Playbook(
            playbook_code="PB-SEC-01",
            title="Ransomware & Host Extortion Containment Playbook",
            threat_category="Ransomware",
            triggers="File entropy anomaly alerts, canary file modification, volume shadow deletion alerts.",
            immediate_containment="Sever network connection, freeze VM disk snapshots, revoke AWS IAM session credentials.",
            investigation_steps="Identify patient zero endpoint, decryptor availability check with CERT-In, inspect lateral movement via SMB.",
            eradication_and_recovery="Reimage OS from verified gold master AMI, restore database from immutable S3 Glacier, re-issue FIDO2 keys.",
            regulatory_mandate="CERT-In Cybersecurity Directions 2022 (Mandatory 6-Hour SLA)",
            owner="Priya Nair (SecOps Lead)",
            last_reviewed_date=date(2026, 6, 1)
        ),
        Playbook(
            playbook_code="PB-SEC-02",
            title="Cloud IAM & Infrastructure Compromise Playbook",
            threat_category="Cloud IAM Compromise",
            triggers="Anomalous API calls from unapproved ASN, sudden spike in IAM role creations, MFA deactivation.",
            immediate_containment="Attach explicit Deny-All inline policy, deactivate compromised access keys, kill active STS tokens.",
            investigation_steps="Query AWS Athena on CloudTrail partitioned logs, check S3 GetObject volume, evaluate security group drift.",
            eradication_and_recovery="Rotate all RDS master passwords, cycle Terraform state secrets, enforce ZTNA FIDO2 passkey login.",
            regulatory_mandate="CERT-In 2022 & ISO/IEC 27001:2022 Control A.5.24",
            owner="Arjun Sharma (DevSecOps Lead)",
            last_reviewed_date=date(2026, 6, 5)
        ),
        Playbook(
            playbook_code="PB-SEC-03",
            title="Email Phishing & Credential Harvesting Playbook",
            threat_category="Phishing / Social Engineering",
            triggers="User reported phishing button click, anomalous Google Workspace login from new geographic territory.",
            immediate_containment="Terminate all active Google Workspace OAuth sessions, reset password, invalidate app passwords.",
            investigation_steps="Search email tenant message IDs, extract malicious payload URLs, check mail forwarding rules.",
            eradication_and_recovery="Purge malicious message from all user mailboxes via Google Admin API, block sender domain on MX gate.",
            regulatory_mandate="ISO 27001 A.5.26 & NIST SP 800-61",
            owner="SecOps Incident Commander",
            last_reviewed_date=date(2026, 6, 10)
        ),
        Playbook(
            playbook_code="PB-SEC-04",
            title="DDoS & Service Disruption Mitigation Playbook",
            threat_category="Denial of Service",
            triggers="HTTP 502/504 errors exceeding 5%, network ingress saturating 90% bandwidth, SYN flood alarms.",
            immediate_containment="Activate Cloudflare 'Under Attack' mode, engage AWS Shield Advanced automatic mitigation.",
            investigation_steps="Analyze request patterns (URI, User-Agent, ASN), identify Layer 7 vs Layer 4 attack vectors.",
            eradication_and_recovery="Apply targeted WAF rate limiting rules, scale backend ECS/EKS clusters, verify normal latency.",
            regulatory_mandate="CERT-In Cybersecurity Directions 2022",
            owner="Priya Nair (SecOps Lead)",
            last_reviewed_date=date(2026, 6, 12)
        ),
        Playbook(
            playbook_code="PB-SEC-05",
            title="Insider Threat & DPDP Data Breach Playbook",
            threat_category="Data Exfiltration",
            triggers="Bulk database download exceeding normal threshold, USB storage insertion on endpoint, unauthorized S3 sync.",
            immediate_containment="Revoke system access immediately, place legal hold on email/Slack archives, capture forensic image.",
            investigation_steps="Interview manager, review DLP logs and Git commits, assess impacted data principals count.",
            eradication_and_recovery="Issue formal notification to Data Protection Board of India (DPBI) and affected Data Principals.",
            regulatory_mandate="Digital Personal Data Protection (DPDP) Act 2023",
            owner="Legal Counsel & Founder",
            last_reviewed_date=date(2026, 6, 15)
        ),
        Playbook(
            playbook_code="PB-SEC-06",
            title="Supply Chain & Dependency Hijacking Playbook",
            threat_category="Software Supply Chain",
            triggers="Trivy/Snyk alert on malicious PyPI or npm package version, GitHub Dependabot critical alert.",
            immediate_containment="Block package download in internal PyPI/npm registry mirror, halt production CI/CD deployments.",
            investigation_steps="Check if compromised package version was deployed to staging or production, inspect artifact hashes.",
            eradication_and_recovery="Pin known-good dependency version, rebuild clean container images, run full DAST/SAST scan.",
            regulatory_mandate="NIST SP 800-161 & OWASP SCVS",
            owner="Arjun Sharma (DevSecOps Lead)",
            last_reviewed_date=date(2026, 6, 18)
        )
    ]
    for pb in playbooks:
        if not db.query(Playbook).filter(Playbook.playbook_code == pb.playbook_code).first():
            db.add(pb)

    # 4. Vulnerability Patches & CVSS Tracking
    vulns = [
        VulnerabilityPatch(
            cve_id="CVE-2026-2189",
            affected_asset="Production Reverse Proxy (AWS ap-south-1)",
            component="OpenSSL 3.1.2",
            cvss_score=9.8,
            severity="Critical",
            patch_available=True,
            remediation_due_date=date(2026, 7, 5),
            status="Patch Testing",
            assigned_engineer="Arjun Sharma"
        ),
        VulnerabilityPatch(
            cve_id="CVE-2026-3390",
            affected_asset="Public Client API Gateway",
            component="Node.js v20.10.0",
            cvss_score=8.2,
            severity="High",
            patch_available=True,
            remediation_due_date=date(2026, 7, 10),
            status="Applied & Verified",
            assigned_engineer="DevOps Engineer"
        ),
        VulnerabilityPatch(
            cve_id="CVE-2026-1044",
            affected_asset="Kubernetes Worker Nodes (EKS)",
            component="Linux Kernel 6.5.0",
            cvss_score=7.8,
            severity="High",
            patch_available=True,
            remediation_due_date=date(2026, 7, 12),
            status="Open",
            assigned_engineer="Priya Nair"
        )
    ]
    for v in vulns:
        if not db.query(VulnerabilityPatch).filter(VulnerabilityPatch.cve_id == v.cve_id).first():
            db.add(v)

    # 5. Tabletop Drills
    drills = [
        TabletopDrill(
            drill_code="ADT-DRILL-2026-001",
            title="Simulated Ransomware Incident & CERT-In Reporting Drill",
            drill_date=date(2026, 6, 18),
            scenario_type="Ransomware Host Isolation & S3 Glacier Restore",
            facilitator="External Security Auditor / CISO",
            participants_roles="Founder, CISO Lead, DevOps Lead, Legal Counsel",
            target_containment_minutes=30,
            actual_containment_minutes=22,
            lessons_learned_summary="Isolation automation validated via AWS CLI STS token revocation script. CERT-In 6-hour SLA reporting simulated successfully.",
            drill_rating="High Preparedness"
        ),
        TabletopDrill(
            drill_code="ADT-DRILL-2026-002",
            title="AWS Root Key Leak & S3 Bucket Public Exposure Exercise",
            drill_date=date(2026, 6, 22),
            scenario_type="AWS Cloud IAM Credential Compromise & Data Leak Drill",
            facilitator="Priya Nair (SecOps Lead)",
            participants_roles="Founder, SecOps Lead, CloudOps Engineer",
            target_containment_minutes=20,
            actual_containment_minutes=14,
            lessons_learned_summary="CloudTrail automated remediation lambda successfully detached policies within 4 minutes. Zero data exposure detected.",
            drill_rating="Exemplary - Zero Data Leak"
        )
    ]
    for d in drills:
        if not db.query(TabletopDrill).filter(TabletopDrill.drill_code == d.drill_code).first():
            db.add(d)

    # 6. SIEM Security Alerts
    alerts = [
        SecurityAlert(
            alert_id="ADT-ALT-001",
            source="AWS GuardDuty",
            rule_name="UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration",
            signal_summary="Credentials generated by STS role were used from an external unapproved IP address outside Horamavu HQ boundary.",
            initial_severity="High",
            validation_status="Under Investigation",
            assigned_analyst="Priya Nair (SecOps Lead)"
        ),
        SecurityAlert(
            alert_id="ADT-ALT-002",
            source="GitHub Secret Scanning",
            rule_name="High-Entropy AWS Access Key identified in feature branch",
            signal_summary="Developer accidentally committed sandbox AWS staging secret to pull request #42. Pre-receive hook blocked remote push.",
            initial_severity="Medium",
            validation_status="Under Investigation",
            assigned_analyst="Arjun Sharma (DevSecOps Lead)"
        ),
        SecurityAlert(
            alert_id="ADT-ALT-003",
            source="CrowdStrike EDR",
            rule_name="Suspicious PowerShell Encoded Script Execution",
            signal_summary="Obfuscated base64 PowerShell invocation detected on testing VM during build artifact verification.",
            initial_severity="Low",
            validation_status="False Positive",
            assigned_analyst="SOC Analyst"
        )
    ]
    for alt in alerts:
        if not db.query(SecurityAlert).filter(SecurityAlert.alert_id == alt.alert_id).first():
            db.add(alt)

    # 7. CERT-In Regulatory Report
    report = CERTInRegulatoryReport(
        report_reference="CERT-IN-REP-2026-001",
        incident_id="ADT-SEC-2026-001",
        submission_timestamp=datetime(2026, 6, 18, 17, 30, 0),
        cert_in_ack_number="CERTIN/INC/2026/0981",
        affected_organization="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        contact_phone="+91-80-6922-8000",
        contact_email="security@asperiondigital.com",
        narrative_description="Simulated credential compromise detected via CloudTrail canary. Root credentials rotated, temporary access tokens invalidated within 14 minutes. Zero data exfiltration.",
        containment_actions_taken="Revoked active STS tokens, rotated master API credentials, preserved forensic disk images under S3 object lock.",
        filing_status="Acknowledged"
    )
    if not db.query(CERTInRegulatoryReport).filter(CERTInRegulatoryReport.report_reference == report.report_reference).first():
        db.add(report)

    db.commit()


def _seed_purchase_orders_and_bills(db):
    """Ensures authentic Purchase Orders and AP Bills are populated for Vendor Sourcing Portal."""
    v_aws = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-001").first()
    v_nexus = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-002").first()
    v_zenith = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-003").first()
    v_acro = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-005").first()

    pos = [
        PurchaseOrder(
            po_number="ADT/PO/2026/001",
            po_date=date(2026, 6, 12),
            vendor_name="Nexus Micro Systems Pvt Ltd",
            vendor_id=v_nexus.id if v_nexus else 2,
            project_code="ADT-PRJ-2026-01",
            total_amount=540000.0,
            delivery_due_date=date(2026, 6, 20),
            status="Fulfilled",
            items_json='[{"item": "Apple MacBook Pro M3 Max (36GB/1TB SSD)", "hsn": "84713010", "qty": 3, "rate": 180000.0, "amount": 540000.0}]',
            payment_terms="Net 30 Days (MSME Priority)",
            delivery_challan_no="DC-NEX-8891",
            statutory_notes="Asperion Digital Technologies (OPC) Private Limited standard terms. MSMED Act 2006 Priority Section 15 applies."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/002",
            po_date=date(2026, 6, 18),
            vendor_name="Amazon Web Services India Pvt Ltd",
            vendor_id=v_aws.id if v_aws else 1,
            project_code="ADT-PRJ-2026-01",
            total_amount=180000.0,
            delivery_due_date=date(2026, 6, 30),
            status="Approved",
            items_json='[{"item": "AWS Cloud Infrastructure Reserved Instances (m6i.2xlarge, RDS Aurora)", "sac": "998315", "qty": 1, "rate": 180000.0, "amount": 180000.0}]',
            payment_terms="Net 30 Days",
            statutory_notes="SLA Uptime 99.95% committed. SOC2 Type II and ISO 27001 data residency in ap-south-1 Mumbai."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/003",
            po_date=date(2026, 6, 20),
            vendor_name="Acroprint Technologies India",
            vendor_id=v_acro.id if v_acro else 5,
            project_code="ADT-PRJ-2026-01",
            total_amount=45000.0,
            delivery_due_date=date(2026, 6, 25),
            status="Fulfilled",
            items_json='[{"item": "AI Biometric Facial Recognition Scanner Terminal & Mounting Kit", "hsn": "85437099", "qty": 1, "rate": 45000.0, "amount": 45000.0}]',
            payment_terms="Net 15 Days (MSME Micro 45-day SLA)",
            delivery_challan_no="DC-ACR-1029",
            statutory_notes="Device must comply with DPDP Act 2023 biometric encryption standards."
        ),
        PurchaseOrder(
            po_number="ADT/PO/2026/004",
            po_date=date(2026, 6, 22),
            vendor_name="Zenith Digital Infrastructure Pvt Ltd",
            vendor_id=v_zenith.id if v_zenith else 3,
            project_code="ADT-PRJ-2026-01",
            total_amount=95000.0,
            delivery_due_date=date(2026, 7, 5),
            status="In Transit",
            items_json='[{"item": "Dedicated 1Gbps Symmetric Leased Line Port & BGP Multi-Homing", "sac": "998411", "qty": 1, "rate": 95000.0, "amount": 95000.0}]',
            payment_terms="Net 30 Days",
            statutory_notes="Includes redundant fiber termination at Horamavu HQ."
        )
    ]
    for p in pos:
        if not db.query(PurchaseOrder).filter(PurchaseOrder.po_number == p.po_number).first():
            db.add(p)
    db.flush()

    vendor_bills = [
        APBill(
            bill_number="INV-NEX-9921",
            bill_date=date(2026, 6, 19),
            due_date=date(2026, 7, 19),
            vendor_name="Nexus Micro Systems Pvt Ltd",
            po_reference="ADT/PO/2026/001",
            grn_reference="ADT-GRN-2026-001",
            three_way_match_status="Matched",
            expense_category="Hardware & Workstations",
            taxable_amount=540000.0,
            gst_amount=97200.0,
            tds_section="194C",
            tds_rate=0.02,
            tds_amount=10800.0,
            net_payable=626400.0,
            approval_status="Approved",
            payment_reference="NEFT-NEXUS-20260628"
        ),
        APBill(
            bill_number="INV-ACR-4412",
            bill_date=date(2026, 6, 24),
            due_date=date(2026, 7, 9),
            vendor_name="Acroprint Technologies India",
            po_reference="ADT/PO/2026/003",
            grn_reference="ADT-GRN-2026-002",
            three_way_match_status="Matched",
            expense_category="Facility & Biometrics",
            taxable_amount=45000.0,
            gst_amount=8100.0,
            tds_section="194C",
            tds_rate=0.01,
            tds_amount=450.0,
            net_payable=52650.0,
            approval_status="Approved",
            payment_reference="UPI-ACRO-20260627"
        ),
        APBill(
            bill_number="INV-ZEN-7711",
            bill_date=date(2026, 6, 26),
            due_date=date(2026, 7, 26),
            vendor_name="Zenith Digital Infrastructure Pvt Ltd",
            po_reference="ADT/PO/2026/004",
            grn_reference="Pending Inward GRN",
            three_way_match_status="Pending GRN",
            expense_category="Telecommunication / Leased Line",
            taxable_amount=95000.0,
            gst_amount=17100.0,
            tds_section="194J",
            tds_rate=0.02,
            tds_amount=1900.0,
            net_payable=110200.0,
            approval_status="Pending Finance Approval"
        )
    ]
    for b in vendor_bills:
        if not db.query(APBill).filter(APBill.bill_number == b.bill_number).first():
            db.add(b)
    db.flush()
    db.commit()


def _seed_hrms_records(db):
    """Ensures rich authentic Candidates, Leaves, POSH, and Separation Clearances are seeded."""
    candidates_data = [
        Candidate(
            full_name="Rohan Deshmukh",
            email="rohan.deshmukh@gmail.com",
            phone="+91-9876501234",
            applied_role="Senior Backend Cloud Engineer",
            department="Engineering",
            experience_years=5.5,
            current_ctc=1200000.0,
            expected_ctc=1600000.0,
            notice_period_days=30,
            stage="Interview Scheduled",
            interview_feedback="Strong Python, FastAPI, and async architecture skills. Solved distributed locking assessment with Redis."
        ),
        Candidate(
            full_name="Ananya Sen",
            email="ananya.sen@gmail.com",
            phone="+91-9876505678",
            applied_role="Lead AI / ML Researcher",
            department="Engineering",
            experience_years=7.0,
            current_ctc=1650000.0,
            expected_ctc=2100000.0,
            notice_period_days=15,
            stage="Intent to Offer",
            interview_feedback="Expertise in LLM orchestration, local Ollama deployment, RAG embeddings, and model safety guardrails."
        ),
        Candidate(
            full_name="Karthik V",
            email="karthik.v@gmail.com",
            phone="+91-9876509012",
            applied_role="QA DevSecOps Engineer",
            department="Engineering",
            experience_years=4.0,
            current_ctc=900000.0,
            expected_ctc=1200000.0,
            notice_period_days=30,
            stage="Technical Cleared",
            interview_feedback="Comprehensive test coverage with pytest, SAST scanning, and automated CI/CD pipeline gating."
        ),
        Candidate(
            full_name="Divya Nair",
            email="divya.nair@gmail.com",
            phone="+91-9876503456",
            applied_role="Product & UI/UX Designer",
            department="Product",
            experience_years=3.5,
            current_ctc=750000.0,
            expected_ctc=950000.0,
            notice_period_days=45,
            stage="Applied",
            interview_feedback="Design system and glassmorphic enterprise dashboard portfolio under review."
        )
    ]
    for c in candidates_data:
        if not db.query(Candidate).filter(Candidate.email == c.email).first():
            db.add(c)
    db.flush()

    # Leaves
    leaves_data = [
        LeaveRecord(
            employee_id=1,
            employee_name="Arjun Sharma",
            leave_type="Casual Leave",
            start_date=date(2026, 7, 3),
            end_date=date(2026, 7, 4),
            total_days=2.0,
            reason="Family event in Mysore",
            status="Approved",
            approver="Founder Varadi Vijay"
        ),
        LeaveRecord(
            employee_id=2,
            employee_name="Priya Nair",
            leave_type="Sick Leave",
            start_date=date(2026, 6, 22),
            end_date=date(2026, 6, 22),
            total_days=1.0,
            reason="Medical consultation",
            status="Approved",
            approver="Arjun Sharma"
        ),
        LeaveRecord(
            employee_id=3,
            employee_name="Vikram Rathore",
            leave_type="Casual Leave",
            start_date=date(2026, 7, 10),
            end_date=date(2026, 7, 10),
            total_days=1.0,
            reason="Personal work",
            status="Approved",
            approver="Founder Varadi Vijay"
        ),
        LeaveRecord(
            employee_id=4,
            employee_name="Sneha Rao",
            leave_type="Earned Leave",
            start_date=date(2026, 7, 15),
            end_date=date(2026, 7, 17),
            total_days=3.0,
            reason="Annual vacation",
            status="Pending",
            approver="Reporting Manager"
        )
    ]
    for l in leaves_data:
        if not db.query(LeaveRecord).filter(LeaveRecord.employee_name == l.employee_name, LeaveRecord.start_date == l.start_date).first():
            db.add(l)
    db.flush()

    # POSH Case
    if not db.query(POSHCase).filter(POSHCase.case_reference == "ADT-POSH-2026-001").first():
        posh = POSHCase(
            case_reference="ADT-POSH-2026-001",
            date_filed=date(2026, 6, 20),
            nature_of_complaint="Inappropriate workplace messaging inquiry",
            internal_committee_presiding_officer="Senior Woman Leader (Director Appointee)",
            external_member="Empowered NGO Representative",
            inquiry_status="Concluded",
            interim_relief_granted=True,
            statutory_90_day_deadline=date(2026, 9, 18),
            recommendations_summary="Counselling and formal written warning issued; zero tolerance reaffirmed.",
            action_taken="Warning letter HR-ER-08 delivered; training drill completed.",
            annual_report_disclosed=True
        )
        db.add(posh)
    db.flush()

    # Separation Clearance
    if db.query(SeparationClearance).count() == 0:
        emp4 = db.query(Employee).filter(Employee.emp_code == "ADT-EMP-004").first()
        emp_id = emp4.id if emp4 else 1
        sep = SeparationClearance(
            employee_id=emp_id,
            resignation_date=date(2026, 6, 1),
            last_working_day=date(2026, 6, 30),
            notice_period_required=30,
            notice_period_served=30,
            notice_buyout_days=0,
            it_asset_clearance=True,
            it_access_revoked=True,
            admin_id_card_clearance=True,
            finance_clearance=True,
            manager_handover_clearance=True,
            hr_clearance=True,
            fnf_gross_payable=91666.67,
            fnf_deductions=200.0,
            fnf_net_payable=91466.67,
            fnf_settlement_status="Settled & Disbursed",
            relieving_letter_issued=True
        )
        db.add(sep)
    db.flush()
    db.commit()


if __name__ == "__main__":
    seed_database()


def _seed_communications_and_teams(db):
    """Seed comprehensive internal communication channels, team presence, discussions & huddle sessions."""
    print("[Seeder] Populating Asperion Teams, Internal Communications & Sentinel AI Bot...")

    # 1. Team Presence
    presence_data = [
        TeamMemberPresence(
            employee_name="Director Varadi Vijay",
            email="director@asperion.in",
            designation="Director & Founder",
            department="Executive Management",
            status="ONLINE",
            status_message="🏢 Horamavu Bangalore HQ - Executive Desk",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="blue"
        ),
        TeamMemberPresence(
            employee_name="Siddharth Kulkarni",
            email="siddharth.kulkarni@asperion.in",
            designation="Staff Platform Engineer",
            department="Engineering",
            status="ONLINE",
            status_message="🚀 Reviewing PR #42 & CI/CD pipeline",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="indigo"
        ),
        TeamMemberPresence(
            employee_name="Arun Sharma",
            email="arun.sharma@asperion.in",
            designation="SecOps & CERT-In Lead",
            department="Security & Compliance",
            status="ONLINE",
            status_message="🛡️ CERT-In War Room Triage & Passkey Watch",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="rose"
        ),
        TeamMemberPresence(
            employee_name="Priya Nair",
            email="priya.nair@asperion.in",
            designation="People & Culture Lead",
            department="HR & Talent",
            status="ONLINE",
            status_message="👥 Reviewing ATS pipeline candidates",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="amber"
        ),
        TeamMemberPresence(
            employee_name="Neha Sharma",
            email="neha.sharma@asperion.in",
            designation="Finance & Accounts Lead",
            department="Finance & Accounts",
            status="ONLINE",
            status_message="💰 ICICI Bank NEFT Batch Reconciled",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="emerald"
        ),
        TeamMemberPresence(
            employee_name="Rohan Deshmukh",
            email="rohan.deshmukh@gmail.com",
            designation="Senior Distributed Systems Architect",
            department="Engineering",
            status="IN_MEETING",
            status_message="📅 SteerCo Architecture Sync",
            location_tag="Remote / WFH",
            avatar_color="purple"
        ),
        TeamMemberPresence(
            employee_name="Karthik V",
            email="karthik.v@gmail.com",
            designation="QA DevSecOps Engineer",
            department="Engineering",
            status="ONLINE",
            status_message="🧪 156/156 Pytest Test Suite Passing",
            location_tag="Horamavu Bangalore HQ",
            avatar_color="cyan"
        )
    ]
    for p in presence_data:
        if not db.query(TeamMemberPresence).filter(TeamMemberPresence.email == p.email).first():
            db.add(p)
    db.flush()

    # 2. Channels
    channels_data = [
        ChatChannel(
            slug="announcements",
            display_name="📢 Announcements & Townhall",
            description="Official corporate broadcasts from Director Varadi Vijay, statutory compliance milestones, and enterprise awards.",
            channel_type="PUBLIC_CHANNEL",
            topic="Company Milestones & Statutory Declarations",
            is_pinned=True,
            created_by_name="Director Varadi Vijay"
        ),
        ChatChannel(
            slug="general",
            display_name="💬 General Watercooler",
            description="Cross-functional culture, team welcomes, ideas, celebration, and informal syncs.",
            channel_type="PUBLIC_CHANNEL",
            topic="All-Hands Collaboration & Community",
            is_pinned=True,
            created_by_name="Director Varadi Vijay"
        ),
        ChatChannel(
            slug="engineering-devops",
            display_name="⚙️ Engineering & Architecture",
            description="High-performance backend, FastAPI, CI/CD pipeline gating, performance benchmarks & code reviews.",
            channel_type="PUBLIC_CHANNEL",
            topic="Architecture RFCs & Sprint Delivery",
            is_pinned=False,
            created_by_name="Siddharth Kulkarni"
        ),
        ChatChannel(
            slug="cybersecurity-soc",
            display_name="🛡️ Cybersecurity & CERT-In War Room",
            description="CERT-In 6-hour mandatory incident reporting, FIDO2 Passkeys, SIEM alert feeds & security drills.",
            channel_type="WAR_ROOM",
            topic="Active Threat Monitoring & Incident Response",
            is_pinned=True,
            created_by_name="Arun Sharma"
        ),
        ChatChannel(
            slug="pmo-delivery",
            display_name="📊 PMO Delivery & Sprints",
            description="Sprint planning, PMBOK 7 stage-gates, RAID risks, and client UAT sign-offs.",
            channel_type="PUBLIC_CHANNEL",
            topic="Global Project Governance",
            is_pinned=False,
            created_by_name="Director Varadi Vijay"
        ),
        ChatChannel(
            slug="hrms-people-pulse",
            display_name="👥 People, Culture & HRMS",
            description="Talent acquisition, Wage Code structures, leave approvals, POSH compliance & team wellness.",
            channel_type="PUBLIC_CHANNEL",
            topic="Workplace Governance & Culture",
            is_pinned=False,
            created_by_name="Priya Nair"
        ),
        ChatChannel(
            slug="finance-operations",
            display_name="💰 Finance, Tax & Audits",
            description="Monthly payroll runs, ICICI Bank NEFT batches, GST-1 returns, and statutory Karnataka PT challans.",
            channel_type="PUBLIC_CHANNEL",
            topic="P&L, Statutory Filings & Cashflow",
            is_pinned=False,
            created_by_name="Neha Sharma"
        ),
        ChatChannel(
            slug="procurement-vendors",
            display_name="📦 Procurement & Vendors",
            description="Vendor scorecards, PO issuances, strategic sourcing RFPs, and Inward GRNs.",
            channel_type="PUBLIC_CHANNEL",
            topic="Sourcing & Supplier Excellence",
            is_pinned=False,
            created_by_name="Director Varadi Vijay"
        ),
        ChatChannel(
            slug="dm-varadivijay-siddharth",
            display_name="🔒 Direct Message: Varadi Vijay & Siddharth",
            description="Confidential direct leadership sync between Founder and Staff Platform Engineer.",
            channel_type="DIRECT_MESSAGE",
            topic="Strategic Architecture & Multi-Cloud Direction",
            is_pinned=False,
            created_by_name="Director Varadi Vijay"
        )
    ]
    for ch in channels_data:
        if not db.query(ChatChannel).filter(ChatChannel.slug == ch.slug).first():
            db.add(ch)
    db.flush()

    # Get channel references
    ch_ann = db.query(ChatChannel).filter(ChatChannel.slug == "announcements").first()
    ch_gen = db.query(ChatChannel).filter(ChatChannel.slug == "general").first()
    ch_eng = db.query(ChatChannel).filter(ChatChannel.slug == "engineering-devops").first()
    ch_sec = db.query(ChatChannel).filter(ChatChannel.slug == "cybersecurity-soc").first()
    ch_hrm = db.query(ChatChannel).filter(ChatChannel.slug == "hrms-people-pulse").first()
    ch_fin = db.query(ChatChannel).filter(ChatChannel.slug == "finance-operations").first()
    ch_dm  = db.query(ChatChannel).filter(ChatChannel.slug == "dm-varadivijay-siddharth").first()

    # 3. Seed Realistic Chat Messages
    messages_data = [
        # Announcements
        ChatMessage(
            channel_id=ch_ann.id,
            sender_name="Director Varadi Vijay",
            sender_email="director@asperion.in",
            sender_role="Director & Founder",
            content="🎉 Welcome everyone to the unified **Asperion Enterprise OS Communications Hub**! ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED is operating under full ISO 9001:2015, ISO/IEC 27001, and ISO/IEC 42001 certification. All statutory Wage Code payroll, CERT-In compliance, and multi-cloud infrastructure are live.",
            message_type="TEXT",
            is_pinned=True,
            reactions_json='{"🚀": ["Siddharth Kulkarni", "Arun Sharma"], "👍": ["Priya Nair", "Neha Sharma"]}'
        ),
        ChatMessage(
            channel_id=ch_ann.id,
            sender_name="Asperion Sentinel AI Bot",
            sender_email="sentinel@asperion.in",
            sender_role="Autonomous System Orchestrator",
            content="🤖 **[Sentinel Broadcast]** June 2026 Payroll Run disbursed via ICICI Bank NEFT Batch for **₹15,65,290.37** across all 8 verified on-roster personnel. All statutory payslips are generated and downloadable via HRMS.",
            message_type="SYSTEM_BOT",
            reactions_json='{"🎉": ["Director Varadi Vijay", "Neha Sharma"]}'
        ),

        # Engineering
        ChatMessage(
            channel_id=ch_eng.id,
            sender_name="Siddharth Kulkarni",
            sender_email="siddharth.kulkarni@asperion.in",
            sender_role="Staff Platform Engineer",
            content="Good morning engineering team! We have tuned SQLite WAL mode with 5000ms busy timeout and async worker execution. Response times across all 24 routers are <12ms. Our test suite is at 156 passing tests with zero regressions.",
            message_type="TEXT",
            reactions_json='{"🔥": ["Karthik V"], "👍": ["Director Varadi Vijay"]}'
        ),
        ChatMessage(
            channel_id=ch_eng.id,
            sender_name="Siddharth Kulkarni",
            sender_email="siddharth.kulkarni@asperion.in",
            sender_role="Staff Platform Engineer",
            content="```python\n# Production SQLite Connection PRAGMA\nPRAGMA journal_mode=WAL;\nPRAGMA synchronous=NORMAL;\nPRAGMA busy_timeout=5000;\n```",
            message_type="CODE_SNIPPET",
            reactions_json='{"🚀": ["Arun Sharma"]}'
        ),
        ChatMessage(
            channel_id=ch_eng.id,
            sender_name="Director Varadi Vijay",
            sender_email="director@asperion.in",
            sender_role="Director & Founder",
            content="Excellent architecture @siddharth. Please verify all routers enforce ISO 27001 access control checks and audit logging before the staging release.",
            message_type="TEXT",
            reactions_json='{"👍": ["Siddharth Kulkarni"]}'
        ),

        # Cybersecurity War Room
        ChatMessage(
            channel_id=ch_sec.id,
            sender_name="Arun Sharma",
            sender_email="arun.sharma@asperion.in",
            sender_role="SecOps & CERT-In Lead",
            content="🛡️ **CERT-In War Room Daily Triage Report:** 0 uncontained security incidents. All perimeter endpoints require FIDO2 / Passkey WebAuthn authentication. 6-hour statutory incident reporting window is continuously monitored.",
            message_type="TEXT",
            is_pinned=True,
            reactions_json='{"👀": ["Director Varadi Vijay"]}'
        ),
        ChatMessage(
            channel_id=ch_sec.id,
            sender_name="Arun Sharma",
            sender_email="arun.sharma@asperion.in",
            sender_role="SecOps & CERT-In Lead",
            content="Root cause analysis document for recent tabletop drill has been uploaded and sealed.",
            message_type="DOCUMENT_EMBED",
            embed_type="INCIDENT_WAR_ROOM",
            embed_id=1,
            embed_title="INC-2026-0881 CERT-In Incident Triage Report & Playbook Verification",
            embed_url="/api/v1/cybersecurity/incidents/1/filing-report"
        ),

        # HRMS & People Pulse
        ChatMessage(
            channel_id=ch_hrm.id,
            sender_name="Priya Nair",
            sender_email="priya.nair@asperion.in",
            sender_role="People & Culture Lead",
            content="Welcome to Siddharth Kulkarni who officially onboarded as Staff Platform Engineer! Offer Letter HR-ONB-01 has been formally issued and signed.",
            message_type="DOCUMENT_EMBED",
            embed_type="OFFER_LETTER",
            embed_id=1,
            embed_title="HR-ONB-01 Formal Offer Letter: Siddharth Kulkarni",
            embed_url="/api/v1/hrms/letters/1/html",
            reactions_json='{"🎉": ["Director Varadi Vijay", "Siddharth Kulkarni", "Neha Sharma"]}'
        ),

        # Finance
        ChatMessage(
            channel_id=ch_fin.id,
            sender_name="Neha Sharma",
            sender_email="neha.sharma@asperion.in",
            sender_role="Finance & Accounts Lead",
            content="June 2026 monthly bank reconciliation completed against ICICI Bank Current Account. Total net disbursement ₹15.65L matches payroll records. Karnataka PT ₹1,800 challan filed.",
            message_type="TEXT",
            reactions_json='{"👍": ["Director Varadi Vijay"]}'
        ),

        # Direct Message: Varadi Vijay <-> Siddharth
        ChatMessage(
            channel_id=ch_dm.id,
            sender_name="Director Varadi Vijay",
            sender_email="director@asperion.in",
            sender_role="Director & Founder",
            content="Siddharth, great work leading the platform architecture. Let's make sure our internal communication hub is the primary daily driver for the entire team.",
            message_type="TEXT",
            reactions_json='{"🎯": ["Siddharth Kulkarni"]}'
        ),
        ChatMessage(
            channel_id=ch_dm.id,
            sender_name="Siddharth Kulkarni",
            sender_email="siddharth.kulkarni@asperion.in",
            sender_role="Staff Platform Engineer",
            content="Understood Varadi Vijay. The system supports full-duplex communication, instant virtual audio/video huddles, document embedding, and Sentinel AI Bot automation.",
            message_type="TEXT",
            reactions_json='{"🚀": ["Director Varadi Vijay"]}'
        )
    ]
    for m in messages_data:
        db.add(m)
    db.flush()

    # 4. Active Huddle
    if db.query(VirtualHuddleSession).count() == 0:
        huddle = VirtualHuddleSession(
            channel_id=ch_eng.id,
            channel_name=ch_eng.display_name,
            huddle_title="Sprint 14 Architecture & Zero-Trust Review",
            is_active=True,
            started_by_name="Siddharth Kulkarni",
            participants_json='[{"name": "Siddharth Kulkarni", "role": "Host", "mic": true, "cam": true, "screen": false, "joined_at": "20:00"}, {"name": "Director Varadi Vijay", "role": "Participant", "mic": true, "cam": true, "screen": false, "joined_at": "20:05"}, {"name": "Karthik V", "role": "Participant", "mic": false, "cam": true, "screen": false, "joined_at": "20:08"}]'
        )
        db.add(huddle)
    db.flush()
    db.commit()
    print("[Seeder] Asperion Teams & Enterprise Communications successfully seeded!")


def _seed_sharepoint_and_knowledge(db):
    """Seed comprehensive SharePoint Knowledge Hub, SOPs, Methods, Thoughts & Document Library."""
    from app.models.sharepoint import (
        SharePointArticle, SharePointComment, SharePointCommunityQuestion, SharePointDocumentLibraryItem
    )
    import json
    from datetime import datetime, timedelta

    if db.query(SharePointArticle).count() > 0:
        return

    print("[Seeder] Populating Asperion SharePoint & Enterprise Knowledge Hub...")

    # 1. Articles: Thoughts, SOPs, Methods, Blueprints
    articles_data = [
        SharePointArticle(
            article_code="THOUGHT-STRAT-001",
            title="The Asperion Engineering Philosophy: Zero Trust, Microservices & Autonomous Self-Healing",
            category="Employee Thoughts",
            department="Executive & Strategy",
            summary="Strategic perspective by Founder Varadi Vijay on building resilient, self-healing enterprise software foundations with uncompromising Zero Trust and continuous statutory compliance.",
            content="""# The Asperion Engineering Philosophy

As we scale **ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED**, our technical architecture and our organizational culture must move in perfect unison. 

### 1. Zero Trust as First Principles
In modern enterprise operations, perimeter-based security is a relic of the past. At Asperion, every microservice, API interaction, database transaction, and internal tool operates under explicit cryptographic verification. From FIDO2/WebAuthn hardware passkeys to granular mTLS between internal components, trust is never assumed—it is verified continuously.

### 2. Autonomous Self-Healing Infrastructure
Human intervention should be reserved for strategic innovation, creative engineering, and high-order business problem solving. Routine operational anomalies—whether they are minor attendance reconciliation mismatches, transient database connection drops, or regulatory filing alerts—must be identified and resolved autonomously by background self-healing daemons.

### 3. Open Knowledge Sharing & Psychological Safety
This SharePoint and Knowledge Hub exists because great ideas do not belong in organizational silos. Whether you are an associate engineer joining our Horamavu team or a senior architect, your perspectives, process improvements, and technical observations are vital to our collective trajectory. 

*Innovate relentlessly, build securely, and document obsessively.*""",
            steps_json="[]",
            author_name="Varadi Vijay",
            author_role="Director & Founder",
            author_email="director@asperion.in",
            version="v2.0",
            status="Published",
            sensitivity="Internal Use Only",
            iso_compliance_tag="ISO 9001:2015 & ISO 27001:2022",
            tags="leadership, philosophy, zero-trust, architecture, vision",
            views_count=142,
            likes_count=6,
            likes_users_json=json.dumps(["Siddharth Kulkarni", "Priya Nair", "Sneha Rao", "Arjun Sharma", "Rajesh Iyer", "Karthik V"]),
            bookmarks_count=12,
            is_pinned=True,
            featured_badge="Director's Perspective",
            created_at=datetime.utcnow() - timedelta(days=5),
            updated_at=datetime.utcnow() - timedelta(days=2)
        ),
        SharePointArticle(
            article_code="SOP-ENG-001",
            title="Zero-Downtime Blue/Green Microservice Deployment & Instant Rollback Protocol",
            category="SOP & Procedures",
            department="Engineering",
            summary="Standard Operating Procedure for deploying production microservice releases without downtime, including automated health probe verification and one-click rollback criteria.",
            content="""### Objective & Scope
This SOP defines the mandatory release procedure for all core platform components of the Asperion Software Stack across staging and production clusters.

### Prerequisites
- Automated CI/CD pipeline pass on branch `main` with 100% green test suite.
- SAST clean scan (0 high/critical vulnerabilities).
- Change Advisory Board (CAB) digital signoff recorded in Change Management Registry.

### Rollback Triggers
1. HTTP 5xx error rate exceeding 0.05% over a 3-minute sliding window.
2. End-to-end P99 API response latency exceeding 350ms.
3. Database connection pool saturation above 85%.""",
            steps_json=json.dumps([
                {
                    "step": 1,
                    "title": "Trigger Green Staging Container Deployment",
                    "description": "Deploy new build artifact container image to Green environment on secondary network port; verify DB migration compatibility in dry-run mode.",
                    "raci": "Responsible: Lead Architect | Accountable: Release Engineer",
                    "estimated_minutes": 10
                },
                {
                    "step": 2,
                    "title": "Execute Automated Synthetic Smoke Tests",
                    "description": "Run automated health suite probing /health, /api/v1/auth, /api/v1/finance, and /api/v1/hrms endpoints.",
                    "raci": "Responsible: QA / Automation Engineer | Consulted: SecOps",
                    "estimated_minutes": 5
                },
                {
                    "step": 3,
                    "title": "Switch Reverse Proxy Active Target",
                    "description": "Execute graceful NGINX / reverse-proxy upstream routing switch from Blue to Green container instances with keepalive draining.",
                    "raci": "Responsible: DevSecOps Lead",
                    "estimated_minutes": 3
                },
                {
                    "step": 4,
                    "title": "Continuous Telemetry Watch (15-Minute Soak)",
                    "description": "Monitor SRE error budget, memory consumption, CPU utilization, and application logs in real-time.",
                    "raci": "Responsible: SRE On-Call | Informed: Platform Team",
                    "estimated_minutes": 15
                },
                {
                    "step": 5,
                    "title": "Decommission Blue Containers & Archive Release",
                    "description": "Upon successful 15-minute soak test, gracefully terminate previous Blue instances and log release status in SDLC audit registry.",
                    "raci": "Responsible: Release Engineer",
                    "estimated_minutes": 5
                }
            ]),
            author_name="Siddharth Kulkarni",
            author_role="Staff Platform Engineer",
            author_email="siddharth.kulkarni@asperion.in",
            version="v3.1",
            status="Published",
            sensitivity="Internal Use Only",
            iso_compliance_tag="ISO 27001:2022 A.8.29 & ITIL v4 Release Management",
            tags="devops, deployment, blue-green, rollback, zero-downtime",
            views_count=98,
            likes_count=4,
            likes_users_json=json.dumps(["Varadi Vijay", "Arjun Sharma", "Vikram Rathore", "Karthik V"]),
            bookmarks_count=9,
            is_pinned=True,
            featured_badge="Certified SOP",
            created_at=datetime.utcnow() - timedelta(days=12),
            updated_at=datetime.utcnow() - timedelta(days=3)
        ),
        SharePointArticle(
            article_code="SOP-SEC-002",
            title="CERT-In 6-Hour Mandatory Cyber Incident Escalation & War Room Protocol",
            category="SOP & Procedures",
            department="Cybersecurity",
            summary="Emergency SOP governing cyber incident triage, containment, statutory 6-hour CERT-In reporting window, and Director escalation war room activation.",
            content="""### Statutory Context
Under Indian Computer Emergency Response Team (CERT-In) Cyber Security Directions, all cybersecurity incidents matching specified severity classes must be reported within 6 hours of detection.

### Scope & Incident Classes
- Ransomware or unauthorized data encryption.
- Identity compromise of administrative accounts or hardware passkeys.
- Critical API vulnerability exploitation or data exfiltration attempts.
- Denial of service attacks impacting operational availability.""",
            steps_json=json.dumps([
                {
                    "step": 1,
                    "title": "Immediate Incident Identification & Severity Triage",
                    "description": "SOC analyst triages alert, validates IOCs, and classifies severity (Critical P1 / High P2).",
                    "raci": "Responsible: SOC Lead | Accountable: CISO",
                    "estimated_minutes": 15
                },
                {
                    "step": 2,
                    "title": "Activate Virtual Incident War Room & Direct Messaging",
                    "description": "Spawn secure incident war room, alert Director Varadi Vijay and legal counsel via encrypted channels.",
                    "raci": "Responsible: Incident Commander | Informed: Director",
                    "estimated_minutes": 10
                },
                {
                    "step": 3,
                    "title": "Execute Forensic Preservation & Network Isolation",
                    "description": "Take memory dumps, isolate affected container network interfaces, and generate SHA-256 evidence hashes.",
                    "raci": "Responsible: Forensic Specialist",
                    "estimated_minutes": 45
                },
                {
                    "step": 4,
                    "title": "Generate & Transmit CERT-In Formal Regulatory Report",
                    "description": "Draft incident report on official Asperion letterhead with CIN U85500KA2026OPC222069 and transmit via encrypted email to incident@cert-in.org.in within 6 hours.",
                    "raci": "Responsible: CISO | Accountable: Director Varadi Vijay",
                    "estimated_minutes": 60
                }
            ]),
            author_name="Priya Nair",
            author_role="CISO Lead",
            author_email="priya.nair@asperiondigital.com",
            version="v2.4",
            status="Published",
            sensitivity="Confidential",
            iso_compliance_tag="ISO 27001:2022 A.5.24 & CERT-In Statutory Guidelines",
            tags="cybersecurity, cert-in, incident-response, war-room, statutory",
            views_count=115,
            likes_count=5,
            likes_users_json=json.dumps(["Varadi Vijay", "Siddharth Kulkarni", "Vikram Rathore", "Rajesh Iyer", "Arjun Sharma"]),
            bookmarks_count=15,
            is_pinned=False,
            featured_badge="Statutory Mandatory",
            created_at=datetime.utcnow() - timedelta(days=8),
            updated_at=datetime.utcnow() - timedelta(days=1)
        ),
        SharePointArticle(
            article_code="METH-DEV-001",
            title="Event-Driven Autonomous Self-Healing Architecture in Asperion Enterprise OS",
            category="Methods & Mechanisms",
            department="Engineering",
            summary="Technical architectural mechanism explaining in-process background watcher daemon threads, SQLite WAL transaction isolation, and self-reconciling attendance algorithms.",
            content="""### Architectural Thesis
Asperion avoids heavy external job brokers like Celery or Redis for core internal synchronization, preferring lightweight, embedded, in-process threading daemons with strict database isolation.

### Key Architectural Pillars
1. **Thread Lifecycle**: Daemon threads launched during FastAPI lifespan context with atomic shutdown hooks.
2. **Session Scoping**: Independent scoped database sessions per tick to avoid session leakages.
3. **Graceful Anomaly Handling**: Attendance anomalies (e.g. forgotten check-outs past 23:59) are detected, audited, and resolved with standard default work shifts automatically.""",
            steps_json="[]",
            author_name="Arjun Sharma",
            author_role="Principal Architect",
            author_email="arjun.sharma@asperiondigital.com",
            version="v1.2",
            status="Published",
            sensitivity="Internal Use Only",
            iso_compliance_tag="ISO 25010 Software Quality & ITIL Continuous Improvement",
            tags="architecture, methods, self-healing, daemon, threading, fast-api",
            views_count=76,
            likes_count=3,
            likes_users_json=json.dumps(["Varadi Vijay", "Siddharth Kulkarni", "Sneha Rao"]),
            bookmarks_count=7,
            is_pinned=False,
            featured_badge="Architecture Blueprint",
            created_at=datetime.utcnow() - timedelta(days=15),
            updated_at=datetime.utcnow() - timedelta(days=6)
        ),
        SharePointArticle(
            article_code="METH-SEC-002",
            title="WebAuthn & FIDO2 Hardware-Bound Passkey Challenge-Response Cryptographic Validation",
            category="Methods & Mechanisms",
            department="Cybersecurity",
            summary="In-depth mechanism detailing how Asperion validates YubiKey 5 Series and biometric hardware tokens using asymmetric cryptographic challenge-response validation.",
            content="""### Mechanics Overview
Passkeys replace vulnerable shared secrets (passwords) with public-key cryptography. During enrollment:
1. The client generates a private-public keypair on the hardware secure element (YubiKey / Secure Enclave).
2. The public key is stored in the Asperion `passkey_credentials` table along with credential ID.
3. Authentication challenges are signed exclusively on-chip; the server verifies the signature using the stored public key.""",
            steps_json="[]",
            author_name="Vikram Rathore",
            author_role="SecOps Specialist",
            author_email="vikram.rathore@asperion.in",
            version="v1.0",
            status="Published",
            sensitivity="Internal Use Only",
            iso_compliance_tag="ISO 27001 A.9.4.2 & FIDO2 Alliance Standards",
            tags="security, passkey, fido2, webauthn, zero-trust, cryptography",
            views_count=84,
            likes_count=4,
            likes_users_json=json.dumps(["Varadi Vijay", "Priya Nair", "Siddharth Kulkarni", "Arjun Sharma"]),
            bookmarks_count=6,
            is_pinned=False,
            featured_badge="Security Mechanism",
            created_at=datetime.utcnow() - timedelta(days=10),
            updated_at=datetime.utcnow() - timedelta(days=4)
        ),
        SharePointArticle(
            article_code="THOUGHT-PEOPLE-002",
            title="Fostering Psychological Safety and Deep Technical Ownership in a Rapidly Scaling OPC",
            category="Employee Thoughts",
            department="HR & Talent",
            summary="Reflections on building a high-trust engineering culture where every team member feels empowered to challenge architecture decisions and propose novel solutions.",
            content="""### The Power of Radical Transparency
In an agile One Person Company (OPC) scaling into enterprise operations, hierarchical boundaries must not impede technical clarity.

When team members know their code reviews, architectural feedback, and operational retrospectives are evaluated purely on technical merit and customer impact—without fear of blame—velocity increases exponentially.

Our internal communications hub and this SharePoint space are built to democratize perspectives across all teams.""",
            steps_json="[]",
            author_name="Sneha Rao",
            author_role="Head of Talent & Culture",
            author_email="sneha.rao@asperion.in",
            version="v1.0",
            status="Published",
            sensitivity="Internal Use Only",
            iso_compliance_tag="ISO 9001:2015 Clause 7.1.6 Organizational Knowledge",
            tags="culture, leadership, psychological-safety, people, team",
            views_count=92,
            likes_count=5,
            likes_users_json=json.dumps(["Varadi Vijay", "Siddharth Kulkarni", "Priya Nair", "Arjun Sharma", "Rajesh Iyer"]),
            bookmarks_count=8,
            is_pinned=False,
            featured_badge="Culture & People",
            created_at=datetime.utcnow() - timedelta(days=7),
            updated_at=datetime.utcnow() - timedelta(days=2)
        )
    ]
    for a in articles_data:
        db.add(a)
    db.flush()

    # 2. Seed Comments
    art_thought = db.query(SharePointArticle).filter(SharePointArticle.article_code == "THOUGHT-STRAT-001").first()
    art_sop = db.query(SharePointArticle).filter(SharePointArticle.article_code == "SOP-ENG-001").first()
    if art_thought:
        c1 = SharePointComment(
            article_id=art_thought.id,
            author_name="Siddharth Kulkarni",
            author_role="Staff Platform Engineer",
            content="Completely aligned on zero-trust as first principles. The migration to WebAuthn hardware tokens and container boundary isolation has drastically reduced our attack surface.",
            upvotes=3,
            created_at=datetime.utcnow() - timedelta(days=4)
        )
        c2 = SharePointComment(
            article_id=art_thought.id,
            author_name="Priya Nair",
            author_role="CISO Lead",
            content="The autonomous self-healing capability also simplifies our ISO 27001 Continuous Auditing evidence collection. Great roadmap direction!",
            upvotes=2,
            created_at=datetime.utcnow() - timedelta(days=3)
        )
        db.add_all([c1, c2])

    if art_sop:
        c3 = SharePointComment(
            article_id=art_sop.id,
            author_name="Karthik V",
            author_role="Senior Software Engineer",
            content="Can we also integrate synthetic Slack/Teams webhook alerts into step 4 during the 15-minute soak test?",
            upvotes=1,
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        db.add(c3)
    db.flush()

    # 3. Community Q&A Questions
    questions_data = [
        SharePointCommunityQuestion(
            question_code="QA-2026-001",
            title="Best practice for handling SQLAlchemy session rollbacks in background worker threads without SQLite WAL table locking?",
            department="Engineering",
            author_name="Karthik V",
            author_role="Senior Software Engineer",
            body="When running automated reconciliation in `AutoUpdateManager` alongside concurrent API requests, what is the best pattern to ensure clean session close and rollback on transient OperationalError?",
            tags="python, sqlalchemy, sqlite, concurrency, background-tasks",
            views_count=45,
            upvotes_count=3,
            upvoters_json=json.dumps(["Varadi Vijay", "Siddharth Kulkarni", "Arjun Sharma"]),
            has_verified_solution=True,
            answers_count=1,
            answers_json=json.dumps([
                {
                    "author": "Siddharth Kulkarni",
                    "role": "Staff Platform Engineer",
                    "text": "Always instantiate a fresh `SessionLocal()` within a `try ... finally` block inside the worker loop. In the `finally` block, invoke `session.rollback()` and `session.close()`. Also ensure `PRAGMA busy_timeout = 5000` is enabled on the engine.",
                    "upvotes": 4,
                    "is_verified": True,
                    "answered_at": (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
                }
            ]),
            status="Resolved",
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        SharePointCommunityQuestion(
            question_code="QA-2026-002",
            title="What is the official procedure for claiming travel expenses for client on-site visits in Horamavu HQ?",
            department="Finance & Ops",
            author_name="Ananya Sen",
            author_role="Associate DevOps Engineer",
            body="Is there a pre-approval required in the Finance portal before booking local cab travel or intercity transit for client meetings?",
            tags="finance, expense-claim, travel, horamavu, policy",
            views_count=28,
            upvotes_count=1,
            upvoters_json=json.dumps(["Sneha Rao"]),
            has_verified_solution=False,
            answers_count=1,
            answers_json=json.dumps([
                {
                    "author": "Rajesh Iyer",
                    "role": "Financial Controller",
                    "text": "For local transit under INR 2,000, simply submit the GST invoice in the Finance Expense Claims portal directly. For intercity travel, raise an advance requisition with Sole Director approval.",
                    "upvotes": 2,
                    "is_verified": False,
                    "answered_at": (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
                }
            ]),
            status="Answered",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
    ]
    for q in questions_data:
        db.add(q)
    db.flush()

    # 4. Document Library Assets
    doc_lib_data = [
        SharePointDocumentLibraryItem(
            doc_code="DOC-LIB-001",
            name="Asperion Brand Identity & Corporate Deck Template 2026.pptx",
            file_type="PDF",
            file_size_kb=2450,
            category="Corporate & Brand",
            department="Executive & Strategy",
            uploaded_by="Varadi Vijay",
            version="v2.0",
            download_url="/static/docs/asperion_corporate_deck_2026.pdf"
        ),
        SharePointDocumentLibraryItem(
            doc_code="DOC-LIB-002",
            name="ISO 27001:2022 ISMS Policy Framework & Annex A Security Controls.docx",
            file_type="DOCX",
            file_size_kb=820,
            category="Security & Compliance",
            department="Cybersecurity",
            uploaded_by="Priya Nair",
            version="v3.0",
            download_url="/api/v1/vault/documents/secops-docx"
        ),
        SharePointDocumentLibraryItem(
            doc_code="DOC-LIB-003",
            name="Statutory Board Resolution Master Drafting Templates (OPC).docx",
            file_type="DOCX",
            file_size_kb=340,
            category="Governance & Legal",
            department="Executive & Strategy",
            uploaded_by="Varadi Vijay",
            version="v1.1",
            download_url="/api/v1/vault/documents/board-resolutions"
        ),
        SharePointDocumentLibraryItem(
            doc_code="DOC-LIB-004",
            name="Microservices Architecture Blueprint & Network Topology.drawio",
            file_type="DRAWIO",
            file_size_kb=410,
            category="Engineering Blueprints",
            department="Engineering",
            uploaded_by="Arjun Sharma",
            version="v2.2",
            download_url="/static/docs/architecture_topology.drawio"
        ),
        SharePointDocumentLibraryItem(
            doc_code="DOC-LIB-005",
            name="FY 2026-27 Master Budget & 13-Week Cash Flow Forecast Engine.xlsx",
            file_type="XLSX",
            file_size_kb=1120,
            category="Financial Models",
            department="Finance & Ops",
            uploaded_by="Rajesh Iyer",
            version="v4.0",
            download_url="/api/v1/finance/cashflow"
        )
    ]
    for d in doc_lib_data:
        db.add(d)
    db.flush()
    db.commit()
    print("[Seeder] Asperion SharePoint & Knowledge Hub successfully seeded!")


def _seed_training_academy(db):
    """Seed comprehensive role-based onboarding training tracks, modules, lessons, quizzes & enrollments."""
    from app.models.training import (
        TrainingTrack, TrainingModule, EmployeeTrainingEnrollment, TrainingMaterial
    )
    import json
    import hashlib
    from datetime import datetime, timedelta

    if db.query(TrainingTrack).count() > 0 and db.query(TrainingMaterial).count() > 0:
        return

    print("[Seeder] Populating Asperion Enterprise Training Academy & New Joinee Curriculum...")

    # 1. Training Tracks with Min & Max Hours
    track_all = TrainingTrack(
        track_code="TRACK-ONB-ALL",
        name="Company-Wide Foundational Onboarding & Statutory Governance",
        target_department="All Company",
        target_roles="All Employees & Interns",
        min_training_hours=16.0,
        max_training_hours=30.0,
        min_passing_score_pct=80.0,
        description="Mandatory Day 1-30 corporate onboarding track covering company vision, Code of Conduct, POSH Act 2013, clean desk policy, information security, and Horamavu HQ facilities.",
        is_mandatory_for_probation=True
    )
    track_eng = TrainingTrack(
        track_code="TRACK-ENG-DEV",
        name="Full-Stack Microservices & DevSecOps Platform Engineering",
        target_department="Engineering",
        target_roles="Software Engineer, DevOps Engineer, Platform Architect, QA",
        min_training_hours=24.0,
        max_training_hours=45.0,
        min_passing_score_pct=80.0,
        description="Specialized technical engineering track covering FastAPI microservices, SQLite WAL transaction boundaries, autonomous self-healing threads, CI/CD automated gates, and zero-downtime Blue/Green deployments.",
        is_mandatory_for_probation=True
    )
    track_sec = TrainingTrack(
        track_code="TRACK-SEC-SOC",
        name="Zero-Trust Cybersecurity & CERT-In Incident War Room",
        target_department="Cybersecurity",
        target_roles="SecOps Analyst, CISO Lead, SOC Specialist",
        min_training_hours=20.0,
        max_training_hours=40.0,
        min_passing_score_pct=80.0,
        description="Deep dive into statutory 6-hour CERT-In incident reporting, FIDO2/WebAuthn hardware passkeys, ISO 27001 Annex A controls, and tabletop emergency drills.",
        is_mandatory_for_probation=True
    )
    track_fin = TrainingTrack(
        track_code="TRACK-FIN-OPS",
        name="Corporate Law, Statutory Tax Filings & Financial Controllership",
        target_department="Finance & Ops",
        target_roles="Financial Controller, Billing Specialist, Procurement Lead",
        min_training_hours=18.0,
        max_training_hours=35.0,
        min_passing_score_pct=80.0,
        description="Statutory tax compliance (TDS Challan 281, GSTR-3B, Karnataka Professional Tax), 13-week cash flow rolling forecasts, 3-way PO matching, and Companies Act 2013 governance.",
        is_mandatory_for_probation=True
    )
    track_hr = TrainingTrack(
        track_code="TRACK-HR-TALENT",
        name="HR Labour Laws, POSH Redressal & Biometric Attendance Engineering",
        target_department="HR & Talent",
        target_roles="HR Manager, Talent Acquisition Lead, Payroll Specialist",
        min_training_hours=16.0,
        max_training_hours=30.0,
        min_passing_score_pct=80.0,
        description="People operations curriculum covering Karnataka Labour enactments, POSH Internal Committee proceedings, biometric Haversine geofenced attendance, and lifecycle documentation.",
        is_mandatory_for_probation=True
    )
    track_pmo = TrainingTrack(
        track_code="TRACK-PMO-DELIVERY",
        name="Agile PMO, IEEE 1044 Defect Management & Client SLA Governance",
        target_department="PMO & Delivery",
        target_roles="Scrum Master, Project Manager, Delivery Lead",
        min_training_hours=16.0,
        max_training_hours=30.0,
        min_passing_score_pct=80.0,
        description="Sprint planning methodologies, RACI matrix assignments, RAID register risk mitigation, IEEE 1044 defect classification, and client portal SLAs.",
        is_mandatory_for_probation=True
    )
    db.add_all([track_all, track_eng, track_sec, track_fin, track_hr, track_pmo])
    db.flush()

    # 2. Comprehensive Modules with Lessons, Syllabus & Quizzes
    modules_data = [
        # Module 1: Foundational Corporate Ethics & Company Vision
        TrainingModule(
            track_id=track_all.id,
            module_code="TRN-ALL-001",
            title="Asperion Corporate Culture, Whistleblower Policy & Business Ethics",
            category="Company Policies & Culture",
            department="All Company",
            duration_hours=2.0,
            level="Foundational (Day 1-7)",
            is_mandatory=True,
            learning_objectives="Understand Asperion Digital Technologies' corporate constitution, CIN U85500KA2026OPC222069 statutory responsibilities, ethical standards, anti-bribery policies, and protected whistleblower disclosures.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "Corporate Constitution & Founding Principles", "duration_mins": 30, "summary": "Company history, Horamavu HQ operations, and Director Varadi Vijay's operating philosophy."},
                {"chapter": 2, "title": "Code of Conduct & Conflict of Interest", "duration_mins": 45, "summary": "Gift policies, non-disclosure agreements, and transparent conflict declarations."},
                {"chapter": 3, "title": "Whistleblower Protection & Ombudsman Channel", "duration_mins": 45, "summary": "Safe reporting channels, non-retaliation guarantees, and formal redressal timelines."}
            ]),
            lesson_content="""# Asperion Corporate Culture & Ethical Governance

Welcome to **ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED** (`CIN: U85500KA2026OPC222069`). 

### Core Ethical Pillars
1. **Uncompromising Integrity**: Every transaction, line of code, and client interaction must withstand statutory scrutiny.
2. **Open Whistleblower Protection**: Under our corporate ombudsman mechanism, any employee can report irregularities directly to the Director with strict confidentiality and immunity from retaliation.
3. **Intellectual Property Protection**: All innovations, algorithms, and models developed at Asperion remain the exclusive proprietary asset of the company.""",
            policy_reference="POL-HR-01 & Companies Act 2013 Section 177",
            quiz_json=json.dumps([
                {
                    "question": "What is the statutory Corporate Identity Number (CIN) of Asperion Digital Technologies?",
                    "options": ["U85500KA2026OPC222069", "L65191TN1994PLC029009", "U72200KA2020PTC123456", "U12345DL2026OPC999999"],
                    "correct_idx": 0,
                    "explanation": "Asperion Digital Technologies (OPC) Private Limited is incorporated under CIN U85500KA2026OPC222069 with ROC Bangalore."
                },
                {
                    "question": "Under the Asperion Whistleblower Policy, who receives protected disclosures?",
                    "options": ["External media", "Sole Member & Director (Varadi Vijay) via confidential ombudsman", "Local police", "Unverified social media channels"],
                    "correct_idx": 1,
                    "explanation": "Protected disclosures are handled directly by the Sole Member & Director with complete anonymity."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 2: InfoSec & Clean Desk Norms
        TrainingModule(
            track_id=track_all.id,
            module_code="TRN-ALL-002",
            title="Information Security Awareness, Clean Desk Norms & Hardware Passkeys",
            category="Statutory & ISO Compliance",
            department="All Company",
            duration_hours=2.0,
            level="Foundational (Day 1-7)",
            is_mandatory=True,
            learning_objectives="Master ISO 27001 clean desk policies, phishing defense, hardware FIDO2 token handling, and mandatory passwordless access controls.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "Phishing & Social Engineering Vectors", "duration_mins": 30, "summary": "Recognizing spear phishing, credential harvesters, and suspicious attachments."},
                {"chapter": 2, "title": "Clean Desk & Clear Screen Protocol", "duration_mins": 45, "summary": "Physical workstation security in Horamavu HQ and remote work environments."},
                {"chapter": 3, "title": "FIDO2 Hardware Key Operations", "duration_mins": 45, "summary": "YubiKey 5 NFC hardware token enrollment and biometric challenge-response."}
            ]),
            lesson_content="""# Information Security Awareness & Zero Trust Norms

### Clean Desk Policy (ISO 27001 A.7.7)
- Never leave printed customer data or employee files unattended.
- Lock workstations (`Win + L`) whenever stepping away from the desk.
- Never write credentials on sticky notes or unencrypted text documents.""",
            policy_reference="ISO 27001:2022 A.7.7 & POL-SEC-01",
            quiz_json=json.dumps([
                {
                    "question": "What is the primary authentication mechanism mandated for administrative access in Asperion?",
                    "options": ["Shared passwords in Slack", "FIDO2/WebAuthn Hardware Passkeys (e.g. YubiKey 5 Series)", "SMS OTP", "Security questions"],
                    "correct_idx": 1,
                    "explanation": "Asperion enforces passwordless Zero Trust via hardware-bound FIDO2 passkeys."
                },
                {
                    "question": "When stepping away from your desk at Horamavu HQ, what shortcut must you execute?",
                    "options": ["Ctrl + C", "Win + L (Lock Workstation)", "Alt + F4", "Esc"],
                    "correct_idx": 1,
                    "explanation": "Locking your screen ensures unauthorized personnel cannot access company systems."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 3: POSH Act 2013
        TrainingModule(
            track_id=track_all.id,
            module_code="TRN-ALL-003",
            title="Prevention of Sexual Harassment (POSH Act 2013) & Safe Workplace Redressal",
            category="HR & People Ops",
            department="All Company",
            duration_hours=1.5,
            level="Foundational (Day 1-7)",
            is_mandatory=True,
            learning_objectives="Complete statutory POSH compliance, understand the mandate of the Internal Committee (IC), definition of aggrieved woman, and formal complaint filing procedures.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "Legal Framework of POSH Act 2013", "duration_mins": 30, "summary": "Scope, workplace definition, and employer obligations under Indian law."},
                {"chapter": 2, "title": "Recognizing Unwelcome Conduct & Microaggressions", "duration_mins": 30, "summary": "Physical, verbal, and non-verbal behaviors constituting sexual harassment."},
                {"chapter": 3, "title": "Internal Committee (IC) Inquiry Process", "duration_mins": 30, "summary": "Filing timelines (90 days), inquiry completion (90 days), and confidentiality norms."}
            ]),
            lesson_content="""# POSH Act 2013 Compliance & Safe Workplace Mandate

Asperion provides a zero-tolerance, dignified, and safe workplace environment for all personnel across all physical offices and virtual collaboration platforms.""",
            policy_reference="The Sexual Harassment of Women at Workplace Act 2013",
            quiz_json=json.dumps([
                {
                    "question": "Within how many days of an incident must a formal POSH complaint be filed?",
                    "options": ["90 days (extendable by another 90 days with IC approval)", "10 days", "365 days", "No time limit"],
                    "correct_idx": 0,
                    "explanation": "Section 9 of the POSH Act provides a 3-month (90-day) statutory timeline."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 4: Engineering Microservices & SQLite WAL
        TrainingModule(
            track_id=track_eng.id,
            module_code="TRN-ENG-001",
            title="Asperion Microservices Architecture, SQLite WAL & Lifespan Daemons",
            category="Technical Architecture",
            department="Engineering",
            duration_hours=4.0,
            level="Intermediate (Day 8-30)",
            is_mandatory=True,
            learning_objectives="Deep dive into FastAPI application lifecycle, database session scoping with SQLite WAL mode, in-process self-healing threading daemons, and Pydantic validation.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "FastAPI Lifespan & Application Architecture", "duration_mins": 60, "summary": "Dependency injection, router modularity, and CORS security headers."},
                {"chapter": 2, "title": "SQLite WAL Concurrency & Pragma Optimizations", "duration_mins": 90, "summary": "WAL mode, busy_timeout=5000, and transaction rollbacks in multi-threaded daemons."},
                {"chapter": 3, "title": "Autonomous Self-Healing Daemon Pattern", "duration_mins": 90, "summary": "Building background reconciliation daemons with atomic transaction bounds."}
            ]),
            lesson_content="""# Asperion Engineering Deep Dive

### SQLite WAL Mode Concurrency
To ensure ultra-fast reading concurrent with writes without table lockouts:
- Enable `PRAGMA journal_mode=WAL;`
- Configure `PRAGMA busy_timeout=5000;` on engine creation.
- Always use scoped session generators in background worker threads with explicit rollback in `finally:` blocks.""",
            policy_reference="ISO 25010 Software Architecture Quality Guidelines",
            quiz_json=json.dumps([
                {
                    "question": "Which SQLite journal mode is configured in Asperion for concurrent read-write scalability?",
                    "options": ["DELETE", "WAL (Write-Ahead Logging)", "MEMORY", "OFF"],
                    "correct_idx": 1,
                    "explanation": "WAL mode allows multiple readers to read simultaneously while a write transaction is committed."
                },
                {
                    "question": "In background self-healing daemons, how should database sessions be managed?",
                    "options": ["Use a single shared global session", "Instantiate a fresh session per tick in a try...finally block with session.close()", "Never close sessions", "Avoid database connections"],
                    "correct_idx": 1,
                    "explanation": "Fresh scoped sessions prevent connection pool leaks and pending rollback errors."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 5: Blue/Green Deployment SOP
        TrainingModule(
            track_id=track_eng.id,
            module_code="TRN-ENG-002",
            title="Zero-Downtime Blue/Green Deployments & 4-Eyes DevSecOps Quality Gates",
            category="Technical Architecture",
            department="Engineering",
            duration_hours=3.5,
            level="Advanced (Day 31-90)",
            is_mandatory=True,
            learning_objectives="Execute zero-downtime production releases, perform synthetic smoke tests, monitor SRE error budgets, and trigger instant rollbacks.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "Blue/Green Traffic Shifting Mechanics", "duration_mins": 60, "summary": "Reverse proxy upstream routing and keepalive connection draining."},
                {"chapter": 2, "title": "Automated Synthetic Verification", "duration_mins": 60, "summary": "Probing critical path endpoints and automated regression checks."},
                {"chapter": 3, "title": "Rollback Criteria & Post-Mortem Reviews", "duration_mins": 90, "summary": "5xx threshold triggers and root cause analysis documentation."}
            ]),
            lesson_content="""# Zero-Downtime Blue/Green Protocol (SOP-ENG-001)

Release engineers must observe the mandatory 15-minute soak period post traffic-switch before decommissioning previous Blue container instances.""",
            policy_reference="ISO 27001:2022 A.8.29 & ITIL v4 Release Management",
            quiz_json=json.dumps([
                {
                    "question": "What is the mandatory soak period duration following a traffic switch to Green instances?",
                    "options": ["30 seconds", "15 minutes", "24 hours", "0 seconds"],
                    "correct_idx": 1,
                    "explanation": "A 15-minute soak period is required to observe SRE telemetry and error budgets."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 6: CERT-In 6-Hour Reporting
        TrainingModule(
            track_id=track_sec.id,
            module_code="TRN-SEC-001",
            title="CERT-In 6-Hour Mandatory Reporting & Cyber Incident War Room",
            category="Security Operations",
            department="Cybersecurity",
            duration_hours=3.0,
            level="Intermediate (Day 8-30)",
            is_mandatory=True,
            learning_objectives="Master the legal obligation to report cybersecurity incidents to CERT-In within 6 hours, evidence preservation, and Director war room escalation.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "CERT-In Cyber Security Directions Mandate", "duration_mins": 60, "summary": "Reportable incident categories and the strict 6-hour timeline."},
                {"chapter": 2, "title": "Incident War Room Activation", "duration_mins": 60, "summary": "Virtual conference bridge, stakeholder roles, and containment actions."},
                {"chapter": 3, "title": "Forensic Preservation & Regulatory Filing", "duration_mins": 60, "summary": "SHA-256 evidence hashing and official letterhead transmission."}
            ]),
            lesson_content="""# CERT-In Incident Response Protocol (SOP-SEC-002)

All ransomware, unauthorized access, and exfiltration attempts must be notified to incident@cert-in.org.in within 6 hours of discovery.""",
            policy_reference="CERT-In Directions under Section 70B of IT Act 2000",
            quiz_json=json.dumps([
                {
                    "question": "What is the mandatory statutory reporting timeline for cyber incidents to CERT-In?",
                    "options": ["72 hours", "6 hours", "30 days", "1 week"],
                    "correct_idx": 1,
                    "explanation": "CERT-In Cyber Security Directions 2022 mandate reporting within 6 hours of incident detection."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 7: Financial Tax Filings
        TrainingModule(
            track_id=track_fin.id,
            module_code="TRN-FIN-001",
            title="Statutory Tax Filings (TDS 281, GSTR-3B, PT Karnataka) & 13-Week Cash Flow",
            category="Financial Procedures",
            department="Finance & Ops",
            duration_hours=3.5,
            level="Intermediate (Day 8-30)",
            is_mandatory=True,
            learning_objectives="Understand monthly tax remittance deadlines, Challan 281 TDS deposits, Karnataka Professional Tax slabs, and 13-week cash flow modeling.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "Monthly TDS & Professional Tax Remittance", "duration_mins": 60, "summary": "7th of each month for TDS Challan 281; 20th for Karnataka PT Form 5-A."},
                {"chapter": 2, "title": "13-Week Cash Flow Rolling Projections", "duration_mins": 90, "summary": "Accounts Receivable aging and runway preservation."},
                {"chapter": 3, "title": "3-Way Purchase Order & Inward GRN Reconciliation", "duration_mins": 60, "summary": "Matching PO, Goods Received Note, and AP Bill before payment disbursement."}
            ]),
            lesson_content="""# Financial Governance & Statutory Compliance

Timely statutory tax compliance is a fiduciary duty of Asperion Digital Technologies (OPC) Private Limited.""",
            policy_reference="Income Tax Act 1961, Karnataka PT Act 1976 & Companies Act 2013",
            quiz_json=json.dumps([
                {
                    "question": "What is the monthly due date for depositing TDS under Challan ITNS 281?",
                    "options": ["7th of the following month", "End of the month", "Quarterly", "15th of the month"],
                    "correct_idx": 0,
                    "explanation": "TDS deducted in any month must be paid to the Central Government by the 7th of the following month."
                }
            ]),
            passing_score_pct=80.0
        ),
        # Module 8: Agile PMO & IEEE 1044 Defect Severity
        TrainingModule(
            track_id=track_pmo.id,
            module_code="TRN-PMO-001",
            title="Enterprise Agile Sprints, RACI Matrix & IEEE 1044 Defect Severity Triage",
            category="Statutory & ISO Compliance",
            department="PMO & Delivery",
            duration_hours=2.5,
            level="Intermediate (Day 8-30)",
            is_mandatory=True,
            learning_objectives="Master Asperion's delivery mechanics: 2-week sprint cadences, RACI responsibilities, RAID logs, and IEEE 1044 bug taxonomy.",
            syllabus_json=json.dumps([
                {"chapter": 1, "title": "2-Week Sprint Cadence & Ceremony Governance", "duration_mins": 45, "summary": "Sprint planning, daily standups, review, and retro."},
                {"chapter": 2, "title": "RACI Matrix & RAID Item Mitigation", "duration_mins": 45, "summary": "Eliminating role ambiguity across delivery teams."},
                {"chapter": 3, "title": "IEEE 1044 Defect Classification", "duration_mins": 60, "summary": "Categorizing bugs from Critical Blocker to Trivial."}
            ]),
            lesson_content="""# Agile PMO Delivery Standards

Consistent delivery governance protects client trust and ensures predictable sprint velocity.""",
            policy_reference="IEEE 1044 Standard for Software Anomalies & ISO 9001",
            quiz_json=json.dumps([
                {
                    "question": "What standard does Asperion adopt for classifying defect anomalies and bugs?",
                    "options": ["IEEE 1044", "ISO 14001", "HIPAA", "PCI-DSS"],
                    "correct_idx": 0,
                    "explanation": "IEEE 1044 provides the recognized classification framework for software defects and bugs."
                }
            ]),
            passing_score_pct=80.0
        )
    ]
    for m in modules_data:
        db.add(m)
    db.flush()

    # 3. Seed Realistic Enrollments & Completion Certificates
    mod_all_1 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-ALL-001").first()
    mod_all_2 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-ALL-002").first()
    mod_all_3 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-ALL-003").first()
    mod_eng_1 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-ENG-001").first()
    mod_eng_2 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-ENG-002").first()
    mod_sec_1 = db.query(TrainingModule).filter(TrainingModule.module_code == "TRN-SEC-001").first()

    enrollments_data = [
        # Siddharth Kulkarni (Staff Platform Engineer) - Highly trained, certified
        EmployeeTrainingEnrollment(
            employee_name="Siddharth Kulkarni",
            employee_email="siddharth.kulkarni@asperion.in",
            employee_role="Staff Platform Engineer",
            department="Engineering",
            module_id=mod_all_1.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=2.0,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=20),
            certificate_id="CERT-TRN-2026-8812A",
            certificate_hash=hashlib.sha256("Siddharth Kulkarni|TRN-ALL-001|100|CERT-TRN-2026-8812A".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=25)
        ),
        EmployeeTrainingEnrollment(
            employee_name="Siddharth Kulkarni",
            employee_email="siddharth.kulkarni@asperion.in",
            employee_role="Staff Platform Engineer",
            department="Engineering",
            module_id=mod_all_2.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=2.0,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=18),
            certificate_id="CERT-TRN-2026-8812B",
            certificate_hash=hashlib.sha256("Siddharth Kulkarni|TRN-ALL-002|100|CERT-TRN-2026-8812B".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=25)
        ),
        EmployeeTrainingEnrollment(
            employee_name="Siddharth Kulkarni",
            employee_email="siddharth.kulkarni@asperion.in",
            employee_role="Staff Platform Engineer",
            department="Engineering",
            module_id=mod_eng_1.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=4.0,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=15),
            certificate_id="CERT-TRN-2026-8812C",
            certificate_hash=hashlib.sha256("Siddharth Kulkarni|TRN-ENG-001|100|CERT-TRN-2026-8812C".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=25)
        ),
        EmployeeTrainingEnrollment(
            employee_name="Siddharth Kulkarni",
            employee_email="siddharth.kulkarni@asperion.in",
            employee_role="Staff Platform Engineer",
            department="Engineering",
            module_id=mod_eng_2.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=3.5,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=10),
            certificate_id="CERT-TRN-2026-8812D",
            certificate_hash=hashlib.sha256("Siddharth Kulkarni|TRN-ENG-002|100|CERT-TRN-2026-8812D".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=20)
        ),
        # Ananya Sen (Associate DevOps Engineer) - New Joinee in progress
        EmployeeTrainingEnrollment(
            employee_name="Ananya Sen",
            employee_email="ananya.sen@asperiondigital.com",
            employee_role="Associate DevOps Engineer",
            department="Engineering",
            module_id=mod_all_1.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=2.0,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=5),
            certificate_id="CERT-TRN-2026-9901A",
            certificate_hash=hashlib.sha256("Ananya Sen|TRN-ALL-001|100|CERT-TRN-2026-9901A".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=10)
        ),
        EmployeeTrainingEnrollment(
            employee_name="Ananya Sen",
            employee_email="ananya.sen@asperiondigital.com",
            employee_role="Associate DevOps Engineer",
            department="Engineering",
            module_id=mod_all_2.id,
            status="IN_PROGRESS",
            progress_pct=65.0,
            hours_spent=1.3,
            score_pct=0.0,
            quiz_attempts=0,
            completed_at=None,
            enrolled_at=datetime.utcnow() - timedelta(days=8)
        ),
        EmployeeTrainingEnrollment(
            employee_name="Ananya Sen",
            employee_email="ananya.sen@asperiondigital.com",
            employee_role="Associate DevOps Engineer",
            department="Engineering",
            module_id=mod_eng_1.id,
            status="ENROLLED",
            progress_pct=0.0,
            hours_spent=0.0,
            score_pct=0.0,
            quiz_attempts=0,
            completed_at=None,
            enrolled_at=datetime.utcnow() - timedelta(days=5)
        ),
        # Priya Nair (CISO Lead)
        EmployeeTrainingEnrollment(
            employee_name="Priya Nair",
            employee_email="priya.nair@asperiondigital.com",
            employee_role="CISO Lead",
            department="Cybersecurity",
            module_id=mod_sec_1.id,
            status="COMPLETED",
            progress_pct=100.0,
            hours_spent=3.0,
            score_pct=100.0,
            quiz_attempts=1,
            completed_at=datetime.utcnow() - timedelta(days=12),
            certificate_id="CERT-TRN-2026-7734A",
            certificate_hash=hashlib.sha256("Priya Nair|TRN-SEC-001|100|CERT-TRN-2026-7734A".encode('utf-8')).hexdigest(),
            enrolled_at=datetime.utcnow() - timedelta(days=20)
        )
    ]
    for en in enrollments_data:
        db.add(en)
    db.flush()
    db.commit()
    print("[Seeder] Asperion Enterprise Training Academy successfully seeded!")


def _seed_training_materials(db):
    """Seed comprehensive training handbooks, lab walkthroughs, and access guides."""
    from app.models.training import TrainingMaterial
    from datetime import datetime, timedelta

    if db.query(TrainingMaterial).count() > 0:
        return

    print("[Seeder] Populating Asperion Training Materials, Handbooks & Access Guides...")
    materials_data = [
        TrainingMaterial(
            material_code="MAT-ALL-001",
            title="Asperion New Joinee Comprehensive Onboarding Handbook 2026",
            category="Onboarding Handbooks",
            department="All Company",
            target_role="All Employees & Interns",
            doc_type="HANDBOOK",
            reading_time_mins=25,
            access_level="Public / Joinee",
            summary="Official employee orientation manual detailing corporate constitution, Horamavu HQ facilities, working hours, statutory benefits, and reporting cadences.",
            content="""# Asperion Digital Technologies (OPC) Private Limited
## Employee Welcome & Onboarding Handbook

Welcome to the Asperion team! As an employee of **ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED** (`CIN: U85500KA2026OPC222069`), you are part of a high-performance software and systems engineering organization.

### 1. General Corporate Overview
- **Registered Office**: Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka.
- **Operating Philosophy**: Zero Trust Architecture, autonomous self-healing systems, radical transparency, and strict statutory compliance.
- **Working Cadence**: Monday through Friday, 09:30 IST to 18:30 IST. Hybrid remote-office flexibility governed by manager signoff.

### 2. Physical & Facility Guidelines (Horamavu HQ)
- Biometric check-in is required within the 200m Haversine geofenced boundary via the Employee Portal or WhatsApp check-in.
- Clean desk policy: Never leave credentials, client contracts, or sensitive documents on open desks.

### 3. Employee Statutory Benefits & Payroll
- Salaries are disbursed on or before the 1st of each calendar month via ICICI Bank NEFT direct deposit.
- Statutory deductions: Karnataka Professional Tax (INR 200/month) and Income Tax TDS under Section 192.
- Payslips with official digital seals are available for download 24/7 in the Employee Self-Service (ESS) portal.""",
            external_link="/static/docs/onboarding_handbook_2026.pdf",
            linked_module_code="TRN-ALL-001",
            linked_sop_code="SOP-HR-003",
            download_count=34,
            created_at=datetime.utcnow() - timedelta(days=25)
        ),
        TrainingMaterial(
            material_code="MAT-ALL-002",
            title="Enterprise Zero-Trust Passkey & IT Access Provisioning Manual",
            category="Access & Credential Guides",
            department="All Company",
            target_role="All Employees",
            doc_type="ACCESS_GUIDE",
            reading_time_mins=20,
            access_level="Internal Authenticated",
            summary="Comprehensive step-by-step guide for enrolling YubiKey 5 NFC hardware passkeys, biometric WebAuthn credentials, and accessing secure internal tools.",
            content="""# IT Access & Hardware Passkey Provisioning Guide

At Asperion, traditional passwords are strictly deprecated. All administrative and operational interfaces enforce **FIDO2 / WebAuthn passwordless access**.

### Step 1: Hardware Token Issuance
1. Collect your provisioned **YubiKey 5 Series** NFC security key from IT Asset Management during Day 1 onboarding.
2. Verify token serial number against your `ITAsset` record in the Employee Portal.

### Step 2: FIDO2 Token Enrollment
1. Navigate to the **Passkey Infrastructure Portal** (`/api/v1/passkeys` or via Sidebar Navigation).
2. Click **Enroll FIDO2 Passkey**.
3. Insert your YubiKey into your USB port and touch the gold contact sensor when prompted by your browser.
4. Verify your biometric PIN or Windows Hello confirmation.
5. Your public key is registered in `passkey_credentials` table with Zero Trust status marked as `Compliant`.

### Step 3: Tool & Service Access Matrix
- **Internal Communications**: Teams & Channels (`#announcements`, `#general`, departmental rooms).
- **Knowledge Base**: Asperion SharePoint & SOPs (`#view-sharepoint`).
- **Support & Ticketing**: Internal Service Desk & Alert Banner.""",
            external_link="/api/v1/passkeys",
            linked_module_code="TRN-ALL-002",
            linked_sop_code="SOP-SEC-002",
            download_count=28,
            created_at=datetime.utcnow() - timedelta(days=20)
        ),
        TrainingMaterial(
            material_code="MAT-ENG-001",
            title="Full-Stack Developer Local Environment Setup & Microservices Lab Guide",
            category="Technical Labs & Code Walkthroughs",
            department="Engineering",
            target_role="Software Engineer, DevOps, Architect",
            doc_type="LAB_GUIDE",
            reading_time_mins=35,
            access_level="Internal Authenticated",
            summary="Hands-on technical lab walkthrough for configuring local Python 3.14+ runtime, SQLite WAL mode, executing Pytest test suites, and Git trunk-based workflows.",
            content="""# Developer Local Environment & Lab Setup Guide

### 1. Prerequisites & Toolchain
- **Python**: Version 3.14.3+ 64-bit on Windows / Linux container.
- **Node.js**: Version 20+ LTS (for asset linting and UI verification).
- **Git**: Configured with official `@asperion.in` committer email.

### 2. Repository Setup & Dependencies
```bash
# Clone the repository
git clone https://github.com/asperion/asperion-os.git
cd asperion_stack

# Create and activate virtual environment
python -m venv venv
.\\venv\\Scripts\\activate

# Install locked dependencies
pip install -r requirements.txt
```

### 3. Database Initialization & WAL Mode
```bash
# Run database migrations and seed data
python app/seed_data.py
```
Notice that SQLite is configured with `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` in `app/database.py`.

### 4. Running the Local Server
```bash
python run_server.py
# Server binds to http://127.0.0.1:8080
# OpenAPI Docs: http://127.0.0.1:8080/docs
```

### 5. Executing Test Suites
All code changes must maintain 100% test pass rate:
```bash
python -m pytest tests -v
```""",
            external_link="/docs",
            linked_module_code="TRN-ENG-001",
            linked_sop_code="SOP-ENG-001",
            download_count=45,
            created_at=datetime.utcnow() - timedelta(days=18)
        ),
        TrainingMaterial(
            material_code="MAT-SEC-001",
            title="CERT-In Incident War Room Emergency Playbook & Evidence Collection Runbook",
            category="Cheatsheets & Runbooks",
            department="Cybersecurity",
            target_role="SecOps Analyst, CISO Lead",
            doc_type="RUNBOOK",
            reading_time_mins=30,
            access_level="SecOps Restricted",
            summary="Operational runbook for activating emergency cyber incident war rooms, capturing volatile memory dumps, and transmitting 6-hour statutory CERT-In reports.",
            content="""# CERT-In Incident War Room Emergency Playbook

### Statutory Timeline: Mandatory 6 Hours
Under CERT-In Cyber Security Directions (Section 70B of IT Act 2000), any incident involving unauthorized system access, data exfiltration, or ransomware MUST be formally notified within **6 hours of detection**.

### Action Checklist
1. **Hour 0 - Detection & Severity Classification**: Classify as Critical P1 or High P2 in the SecOps War Room.
2. **Hour 1 - Containment & Network Isolation**: Quarantine infected endpoints; disable compromised IAM credentials.
3. **Hour 2 - Volatile Evidence Preservation**: Capture memory images, network socket dumps, and compute SHA-256 hashes.
4. **Hour 4 - Director & Legal Escalation**: Brief Director Varadi Vijay on the war room bridge.
5. **Hour 5 - Draft CERT-In Incident Report**: Generate official report on Asperion letterhead with CIN U85500KA2026OPC222069.
6. **Hour 6 - Secure Transmission**: Email encrypted report to `incident@cert-in.org.in`.""",
            external_link="/api/v1/cybersecurity/warroom",
            linked_module_code="TRN-SEC-001",
            linked_sop_code="SOP-SEC-002",
            download_count=19,
            created_at=datetime.utcnow() - timedelta(days=14)
        ),
        TrainingMaterial(
            material_code="MAT-FIN-001",
            title="Statutory Tax Deduction (TDS), GST e-Way Bill & Expense Claim Handbook",
            category="Statutory & Policy Handbooks",
            department="Finance & Ops",
            target_role="Financial Controller, Accounts, All Roles",
            doc_type="HANDBOOK",
            reading_time_mins=25,
            access_level="Internal Authenticated",
            summary="Comprehensive handbook on monthly TDS Challan 281 remittance schedules, Karnataka Professional Tax slabs, and submitting reimbursement claims via ESS.",
            content="""# Financial Governance & Tax Remittance Manual

### 1. Monthly Statutory Deadlines
- **7th of Every Month**: Deposit of Tax Deducted at Source (TDS) under Challan ITNS 281.
- **20th of Every Month**: GSTR-3B Monthly Return filing and Karnataka Professional Tax remittance (Form 5-A).
- **15th of the Following Quarter**: Quarterly TDS Return filing (Form 24Q for salaries, Form 26Q for non-salaries).

### 2. Expense Claims & Requisitions
- All client-related travel, hosting, or software expenses must include a valid GST invoice showing company GSTIN.
- Claims under INR 2,000 are processed directly; claims exceeding INR 2,000 require Director approval.""",
            external_link="/api/v1/finance/cashflow",
            linked_module_code="TRN-FIN-001",
            linked_sop_code="SOP-FIN-004",
            download_count=22,
            created_at=datetime.utcnow() - timedelta(days=16)
        ),
        TrainingMaterial(
            material_code="MAT-HR-001",
            title="HR Policy Manual, POSH Redressal Mechanism & Employee Benefits Guide",
            category="Statutory & Policy Handbooks",
            department="HR & Talent",
            target_role="HR Manager, Talent Acquisition, All Roles",
            doc_type="HANDBOOK",
            reading_time_mins=20,
            access_level="Public / Joinee",
            summary="Complete guide to Karnataka Shops & Establishments Act compliance, POSH Internal Committee proceedings, paid leaves, and probation clearance criteria.",
            content="""# Asperion HR Policy & Benefits Guide

### 1. Leave Entitlement & Probation Clearance
- **Probation Period**: Standard 6 months for all permanent roles. Clearance requires completing minimum 16.0 hours in the Training Academy and manager signoff.
- **Paid Time Off**: 18 days Annual Earned Leave + 12 days Casual/Sick Leave per annum.

### 2. POSH Policy & Zero Tolerance
- Asperion maintains an active Internal Committee (IC) under the Sexual Harassment of Women at Workplace Act 2013.
- Complaints are investigated within a 90-day statutory window with total confidentiality.""",
            external_link="/api/v1/hrms/policies",
            linked_module_code="TRN-ALL-003",
            linked_sop_code="SOP-HR-003",
            download_count=31,
            created_at=datetime.utcnow() - timedelta(days=22)
        ),
        TrainingMaterial(
            material_code="MAT-PMO-001",
            title="Agile Delivery Playbook, Jira/WBS Tracking & IEEE 1044 Defect Severity Matrix",
            category="Onboarding Handbooks",
            department="PMO & Delivery",
            target_role="Scrum Master, Project Manager, Delivery Lead",
            doc_type="HANDBOOK",
            reading_time_mins=25,
            access_level="Internal Authenticated",
            summary="Detailed playbook covering 2-week sprint cadences, RACI matrix role definitions, RAID risk logs, and IEEE 1044 bug taxonomy.",
            content="""# Agile PMO Delivery & Governance Playbook

### 1. Sprint Lifecycle & Cadence
- **Sprint Duration**: Fixed 2-week timebox commencing on alternate Mondays.
- **Sprint Ceremonies**: Planning (Day 1, 09:30), Daily Standup (10:00, 15 mins), Sprint Review & Demo (Day 10, 16:00).

### 2. IEEE 1044 Defect Severity Taxonomy
- **Severity 1 (Critical)**: Production outage, data corruption, or security exploit. SLA: 2 hours.
- **Severity 2 (High)**: Major functionality impaired with no viable workaround. SLA: 8 hours.
- **Severity 3 (Medium)**: Non-critical feature defect with available workaround. SLA: 3 days.
- **Severity 4 (Low)**: Minor cosmetic or UI alignment anomaly. Scheduled in next sprint.""",
            external_link="/api/v1/pmo/sprints",
            linked_module_code="TRN-PMO-001",
            linked_sop_code="SOP-ENG-001",
            download_count=26,
            created_at=datetime.utcnow() - timedelta(days=15)
        )
    ]
    for m in materials_data:
        db.add(m)
    db.flush()
    db.commit()
    print("[Seeder] Asperion Training Materials, Handbooks & Access Guides successfully seeded!")
    _seed_itsm_comprehensive(db)

def _seed_itsm_comprehensive(db):
    if db.query(ConfigurationItem).first():
        return

    print("[Seeder] Seeding Comprehensive ITSM Suite (CMDB, KEDB, CAB, Runbooks, LOIs, SLAs)...")

    # 1. CMDB Configuration Items
    cis_data = [
        ConfigurationItem(
            ci_code="CI-SRV-GW-01",
            ci_name="Primary Production API Gateway (Envoy/eBPF)",
            ci_type="API Gateway",
            category="Network & Compute",
            environment="Production",
            tier="Tier-0 Mission Critical",
            ip_address="10.0.1.10",
            fqdn="api.asperion.in",
            cloud_provider="AWS ap-south-1 (Mumbai)",
            status="Operational",
            health_score=99.8,
            cpu_utilization_pct=38.5,
            memory_utilization_pct=52.0,
            disk_utilization_pct=28.0,
            upstream_dependencies_json='["CI-NET-VPC-01", "CI-CF-EDGE-01"]',
            downstream_dependencies_json='["CI-SVC-CORE-01", "CI-SVC-AUTH-01"]',
            technical_custodian="DevOps & Platform Engineering Lead",
            patch_level="Envoy 1.30.1 Hardened Linux",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-SVC-CORE-01",
            ci_name="Asperion OS Core Microservices Cluster",
            ci_type="Kubernetes Cluster",
            category="Compute",
            environment="Production",
            tier="Tier-0 Mission Critical",
            ip_address="10.0.2.20",
            fqdn="core.internal.asperion.in",
            cloud_provider="AWS ap-south-1 (EKS)",
            status="Operational",
            health_score=99.6,
            cpu_utilization_pct=45.2,
            memory_utilization_pct=61.8,
            disk_utilization_pct=34.0,
            upstream_dependencies_json='["CI-SRV-GW-01"]',
            downstream_dependencies_json='["CI-DB-PROD-01", "CI-CACHE-REDIS-01"]',
            technical_custodian="Principal Software Architect",
            patch_level="EKS v1.29.3 Containerd",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-SVC-AUTH-01",
            ci_name="Zero-Trust Passkey & IAM Authenticator Service",
            ci_type="SaaS Microservice",
            category="Security",
            environment="Production",
            tier="Tier-0 Mission Critical",
            ip_address="10.0.2.25",
            fqdn="auth.internal.asperion.in",
            cloud_provider="AWS ap-south-1",
            status="Operational",
            health_score=100.0,
            cpu_utilization_pct=22.0,
            memory_utilization_pct=38.4,
            disk_utilization_pct=19.5,
            upstream_dependencies_json='["CI-SRV-GW-01"]',
            downstream_dependencies_json='["CI-DB-PROD-01"]',
            technical_custodian="SecOps Lead",
            patch_level="FIDO2 WebAuthn Server 2.8",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-DB-PROD-01",
            ci_name="Core Relational Database (PostgreSQL Shard 01)",
            ci_type="Relational Database",
            category="Database",
            environment="Production",
            tier="Tier-0 Mission Critical",
            ip_address="10.0.3.50",
            fqdn="db-primary.asperion.internal",
            cloud_provider="AWS RDS Multi-AZ ap-south-1",
            status="Operational",
            health_score=99.2,
            cpu_utilization_pct=48.0,
            memory_utilization_pct=66.5,
            disk_utilization_pct=42.0,
            upstream_dependencies_json='["CI-SVC-CORE-01", "CI-SVC-AUTH-01"]',
            downstream_dependencies_json='["CI-BK-S3-DR-01"]',
            technical_custodian="Database Administrator",
            patch_level="PostgreSQL 16.3 Encrypted KMS",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-CACHE-REDIS-01",
            ci_name="In-Memory Cache & Session Cluster (Redis 7)",
            ci_type="In-Memory Cache",
            category="Database",
            environment="Production",
            tier="Tier-1 Business Critical",
            ip_address="10.0.3.60",
            fqdn="cache.asperion.internal",
            cloud_provider="AWS ElastiCache ap-south-1",
            status="Operational",
            health_score=99.9,
            cpu_utilization_pct=18.4,
            memory_utilization_pct=44.0,
            disk_utilization_pct=12.0,
            upstream_dependencies_json='["CI-SVC-CORE-01"]',
            downstream_dependencies_json='[]',
            technical_custodian="DevOps Engineer",
            patch_level="Redis 7.2.4 In-Memory",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-CF-EDGE-01",
            ci_name="Global Zero-Trust Edge & WAF Shield",
            ci_type="Network Firewall",
            category="Security",
            environment="Production",
            tier="Tier-0 Mission Critical",
            ip_address="104.16.24.12",
            fqdn="asperion.in",
            cloud_provider="Cloudflare Enterprise Edge",
            status="Operational",
            health_score=100.0,
            cpu_utilization_pct=15.0,
            memory_utilization_pct=25.0,
            disk_utilization_pct=10.0,
            upstream_dependencies_json='[]',
            downstream_dependencies_json='["CI-SRV-GW-01"]',
            technical_custodian="SecOps & Infra Lead",
            patch_level="Cloudflare DDoS & Magic Transit",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-HQ-ROUTER-01",
            ci_name="Horamavu HQ Perimeter Gateway & Biometric Kiosk Router",
            ci_type="Network Firewall",
            category="Network",
            environment="Production",
            tier="Tier-1 Business Critical",
            ip_address="192.168.1.1",
            fqdn="router.horamavu.asperion.internal",
            cloud_provider="On-Premises Horamavu HQ (Bangalore)",
            status="Operational",
            health_score=99.4,
            cpu_utilization_pct=28.0,
            memory_utilization_pct=42.0,
            disk_utilization_pct=31.0,
            upstream_dependencies_json='[]',
            downstream_dependencies_json='["CI-CF-EDGE-01"]',
            technical_custodian="IT Systems Admin",
            patch_level="Cisco IOS-XE 17.12 Hardened",
            last_heartbeat=datetime.utcnow()
        ),
        ConfigurationItem(
            ci_code="CI-BK-S3-DR-01",
            ci_name="Disaster Recovery S3 Glacier Vault (Cross-Region ap-southeast-1)",
            ci_type="Cloud Storage",
            category="Platform",
            environment="Disaster Recovery",
            tier="Tier-0 Mission Critical",
            ip_address="s3.ap-southeast-1.amazonaws.com",
            fqdn="backup-vault.asperion.in",
            cloud_provider="AWS ap-southeast-1 (Singapore)",
            status="Operational",
            health_score=100.0,
            cpu_utilization_pct=10.0,
            memory_utilization_pct=15.0,
            disk_utilization_pct=55.0,
            upstream_dependencies_json='["CI-DB-PROD-01"]',
            downstream_dependencies_json='[]',
            technical_custodian="Lead Reliability Engineer",
            patch_level="S3 Versioned WORM Vault",
            last_heartbeat=datetime.utcnow()
        )
    ]
    for ci in cis_data:
        db.add(ci)

    # 2. Problem Management & Known Error Database (KEDB)
    problems_data = [
        ITSMProblem(
            problem_code="PRB-2026-001",
            title="PostgreSQL Connection Pool Exhaustion under Burstable API Traffic",
            category="Database Connection Pool",
            priority="P1-Critical",
            status="Known Error (KEDB)",
            impacted_ci_code="CI-DB-PROD-01",
            root_cause_analysis="5-Whys Analysis: Burstable async worker threads opened unpooled connections -> Max connection threshold (200) was breached -> PgBouncer transaction mode was inactive -> HikariCP pool reached starvation -> Core API returned HTTP 503.",
            temporary_workaround="Execute automated runbook FIX-RUN-01 to flush idle client connections and restart connection pooler; dynamic scale pool size to 350.",
            permanent_fix_plan="Implement PgBouncer transaction-level multiplexing in front of AWS RDS with AWS Lambda RDS Proxy auto-routing.",
            kedb_published=True,
            assigned_engineer="Principal Database Architect",
            related_incidents_count=4,
            identified_at=datetime.utcnow() - timedelta(days=12),
            resolved_at=datetime.utcnow() - timedelta(days=2)
        ),
        ITSMProblem(
            problem_code="PRB-2026-002",
            title="Redis Memory Eviction Leading to Session Authentication Timeouts",
            category="Memory Exhaustion",
            priority="P2-High",
            status="Known Error (KEDB)",
            impacted_ci_code="CI-CACHE-REDIS-01",
            root_cause_analysis="5-Whys Analysis: Temporary JWT token revokation blacklist accumulated TTL-less keys -> Maxmemory limit (4GB) was reached -> volatile-lru eviction dropped active session metadata -> Client browsers received 401 Unauthorized.",
            temporary_workaround="Trigger FIX-RUN-02 to invoke MEMORY PURGE and set strict TTL on all blacklist entries.",
            permanent_fix_plan="Migrate session store to clustered Redis with allkeys-lfu eviction and automated alerting at 80% RAM capacity.",
            kedb_published=True,
            assigned_engineer="Lead DevOps Engineer",
            related_incidents_count=2,
            identified_at=datetime.utcnow() - timedelta(days=18),
            resolved_at=datetime.utcnow() - timedelta(days=5)
        ),
        ITSMProblem(
            problem_code="PRB-2026-003",
            title="WebRTC Virtual Huddle Audio Lag over Intermittent Remote ISP Tunnels",
            category="Network Latency",
            priority="P3-Medium",
            status="Workaround Found",
            impacted_ci_code="CI-SRV-GW-01",
            root_cause_analysis="UDP packet drops on residential ISPs for remote WFH personnel causing jitter buffer overflow on WebRTC audio channels.",
            temporary_workaround="Force fallback to TCP TURN relay server hosted in ap-south-1 with Opus codec bitrate capped at 32 kbps.",
            permanent_fix_plan="Deploy global Cloudflare Calls WebRTC Anycast relay to terminate audio packets at local ISP edge.",
            kedb_published=True,
            assigned_engineer="Communications Media SRE",
            related_incidents_count=3,
            identified_at=datetime.utcnow() - timedelta(days=8)
        )
    ]
    for p in problems_data:
        db.add(p)

    # 3. Change Enablement & CAB Requests
    changes_data = [
        ITSMChangeRequest(
            cr_code="CR-2026-0042",
            title="Upgrade Core API Gateway to Envoy 1.30 with eBPF Rate Limiting",
            change_type="Normal",
            reason_for_change="Enhance DDoS resilience and implement millisecond token-bucket rate limiting for enterprise client APIs.",
            impact_scope="Core API Gateway (CI-SRV-GW-01) & EKS Microservices",
            risk_level="Medium",
            risk_score=38,
            cab_status="Approved",
            cab_review_notes="Approved by CAB. Zero downtime rolling canary upgrade scheduled during weekend maintenance window.",
            cab_approvers_json='["Varadi Vijay (Director)", "DevOps Lead", "SecOps Lead"]',
            implementation_plan="1. Deploy Canary Envoy Pods (10% traffic). 2. Verify synthetic transaction error rates < 0.01%. 3. Shift 100% traffic to v1.30. 4. Decommission v1.29.",
            backout_rollback_plan="Instant Kubernetes service route rollback to Envoy v1.29 stable deployment (Execution time: < 30 seconds).",
            test_validation_procedure="Execute automated Postman & Locust load tests (5,000 req/sec) validating HTTP 200 responses.",
            scheduled_start_time=datetime.utcnow() + timedelta(days=2, hours=2),
            scheduled_end_time=datetime.utcnow() + timedelta(days=2, hours=4),
            outage_required=False,
            lead_implementer="Senior Release Engineer",
            actual_outcome="Scheduled for Saturday 02:00 AM IST execution."
        ),
        ITSMChangeRequest(
            cr_code="CR-2026-0043",
            title="PostgreSQL RDS Minor Version Maintenance & Index Vacuuming",
            change_type="Standard",
            reason_for_change="Routine monthly maintenance, database statistics update, and security patch application on AWS RDS Multi-AZ.",
            impact_scope="Core Relational Database (CI-DB-PROD-01)",
            risk_level="Low",
            risk_score=15,
            cab_status="Scheduled",
            cab_review_notes="Standard pre-approved CAB operational change. Automatic Multi-AZ failover validated.",
            cab_approvers_json='["Varadi Vijay (Director)", "Database Administrator"]',
            implementation_plan="1. Apply minor RDS engine update on standby replica. 2. Trigger automated Multi-AZ failover (15s impact). 3. Upgrade primary replica. 4. Re-sync replication.",
            backout_rollback_plan="Multi-AZ standby replica remains active; automatic failover triggers if primary fails health probe.",
            test_validation_procedure="Verify pg_stat_activity connection status and complete test read/write transactions.",
            scheduled_start_time=datetime.utcnow() + timedelta(days=3, hours=1),
            scheduled_end_time=datetime.utcnow() + timedelta(days=3, hours=2),
            outage_required=True,
            lead_implementer="Database Administrator",
            actual_outcome="Pre-approved standard maintenance window."
        )
    ]
    for cr in changes_data:
        db.add(cr)

    # 4. Automated Runbook Fixes
    runbooks_data = [
        ITSMRunbookFix(
            fix_code="FIX-RUN-01",
            fix_name="Automated Database Connection Pool Recycle & Thread Dump",
            target_ci_type="Relational Database",
            trigger_alert_pattern="DB_CONNECTION_EXHAUSTION",
            procedure_steps_json='["Verify pg_stat_activity active vs idle clients", "Terminate idle connections > 300s", "Recycle PgBouncer connection pooler", "Warm up connection pool with 20 persistent threads", "Report recovery status to SecOps Slack"]',
            execution_type="Supervised 1-Click",
            execution_count=18,
            success_rate_pct=100.0,
            average_mttr_reduction_mins=28.5,
            last_executed_at=datetime.utcnow() - timedelta(days=3)
        ),
        ITSMRunbookFix(
            fix_code="FIX-RUN-02",
            fix_name="Redis Hot-Key Eviction & Memory Compaction",
            target_ci_type="In-Memory Cache",
            trigger_alert_pattern="REDIS_RAM_EXCEED_85_PCT",
            procedure_steps_json='["Analyze hot keys with Redis memory doctor", "Purge expired session tokens", "Execute active defragmentation (MEMORY PURGE)", "Verify memory threshold < 65%"]',
            execution_type="Fully Automated",
            execution_count=12,
            success_rate_pct=98.5,
            average_mttr_reduction_mins=19.0,
            last_executed_at=datetime.utcnow() - timedelta(days=5)
        ),
        ITSMRunbookFix(
            fix_code="FIX-RUN-03",
            fix_name="Cloudflare Edge Route Health Failover",
            target_ci_type="Network Firewall",
            trigger_alert_pattern="ORIGIN_SERVER_UNREACHABLE",
            procedure_steps_json='["Probe primary origin ingress IP", "Shift DNS traffic to secondary ap-south-1 backup origin", "Invalidate edge cache for dynamic routes", "Broadcast operational status page update"]',
            execution_type="Supervised 1-Click",
            execution_count=6,
            success_rate_pct=100.0,
            average_mttr_reduction_mins=35.0,
            last_executed_at=datetime.utcnow() - timedelta(days=14)
        )
    ]
    for r in runbooks_data:
        db.add(r)

    # 5. IT Procurement Letters of Intent (LOIs)
    lois_data = [
        ITSMProcurementLOI(
            loi_number="LOI-IT-2026-001",
            vendor_name="Dell Technologies Enterprise India Pvt Ltd",
            vendor_address="Divyasree Greens, Ground Floor, 12/1, 12/2 Challaghatta, Varthur Hobli, Bengaluru - 560071, Karnataka",
            vendor_contact_person="Ramesh Kulkarni (Enterprise Account Director)",
            vendor_email="ramesh.kulkarni@dell.com",
            asset_category="AI GPU Compute Nodes & Server Infrastructure",
            scope_of_procurement="Supply, installation, rack-mounting, and commissioning of dedicated enterprise PowerEdge XE9680 servers equipped with 8x NVIDIA H100 80GB GPUs for proprietary model training and on-premises inference.",
            equipment_specifications="2x PowerEdge XE9680 Servers, 8x NVIDIA H100 Tensor Core SXM5 80GB per node, Dual Intel Xeon Platinum 8480+ (56 cores each), 2TB DDR5 ECC RAM, 30TB NVMe U.2 Enterprise SSD RAID-10, Dual 100GbE Mellanox ConnectX-7 NICs.",
            estimated_contract_value_inr=3850000.0,
            payment_milestones="30% Advance on LOI Acceptance, 50% on Delivery & QC Verification, 20% post 30-day burn-in test",
            delivery_sla_weeks=3,
            warranty_sla_terms="36-Month 24x7 4-Hour On-Site Mission Critical Replacement & Hardware OEM Guarantee",
            valid_until_date=date(2026, 12, 31),
            director_signatory="Varadi Vijay",
            director_title="Founder & Sole Director",
            company_name="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            company_cin="U85500KA2026OPC222069",
            registered_office="Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India",
            status="Approved & Issued"
        ),
        ITSMProcurementLOI(
            loi_number="LOI-IT-2026-002",
            vendor_name="Cisco Systems India Private Limited",
            vendor_address="Cisco Campus, SEZ Unit, Cessna Business Park, Kadubeesanahalli Village, Varthur Hobli, Bengaluru - 560103, Karnataka",
            vendor_contact_person="Pooja Sen (Director - Enterprise Networking)",
            vendor_email="pooja.sen@cisco.com",
            asset_category="Zero-Trust Network Core Switches & Firewalls",
            scope_of_procurement="Supply and deployment of Catalyst 9300 series 48-port PoE+ core switches, Cisco Secure Firewall 3100 appliance, and DNA Premier licenses for Zero-Trust LAN/WAN segmentation.",
            equipment_specifications="3x Cisco Catalyst 9300X 48-Port 10G SFP+ Core Switches, 1x Cisco Secure Firewall 3120 Appliance with Next-Gen IPS, 50x Zero-Trust Network Access (ZTNA) Agent Licenses.",
            estimated_contract_value_inr=1420000.0,
            payment_milestones="25% Advance against Bank Guarantee, 65% on Delivery, 10% after 60-day acceptance testing",
            delivery_sla_weeks=2,
            warranty_sla_terms="60-Month Cisco SMARTnet 24x7x4 On-Site Support & TAC Escalation Access",
            valid_until_date=date(2026, 12, 15),
            director_signatory="Varadi Vijay",
            director_title="Founder & Sole Director",
            company_name="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
            company_cin="U85500KA2026OPC222069",
            registered_office="Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India",
            status="Approved & Issued"
        )
    ]
    for loi in lois_data:
        from app.api.itsm import generate_loi_html_document
        loi.generated_html = generate_loi_html_document(loi)
        db.add(loi)

    # 6. Operational SLA Contracts
    slas_data = [
        ITSMSLAContract(
            service_code="SLA-CORE-API",
            service_name="Core Transactional API & Middleware",
            service_tier="Tier-0 Mission Critical",
            target_uptime_pct=99.98,
            current_monthly_uptime_pct=99.99,
            p1_response_mins=10,
            p1_resolution_hours=1.5,
            p2_response_mins=20,
            p2_resolution_hours=4.0,
            p3_resolution_hours=12.0,
            sla_penalty_clause="5% service credit per 0.05% breach below 99.98% target"
        ),
        ITSMSLAContract(
            service_code="SLA-AUTH-PASSKEY",
            service_name="Zero-Trust IAM & Passkey Authentication Gateway",
            service_tier="Tier-0 Mission Critical",
            target_uptime_pct=99.99,
            current_monthly_uptime_pct=100.0,
            p1_response_mins=5,
            p1_resolution_hours=1.0,
            p2_response_mins=15,
            p2_resolution_hours=3.0,
            p3_resolution_hours=8.0,
            sla_penalty_clause="10% penalty credit for any single uncontained authentication outage exceeding 30 minutes"
        ),
        ITSMSLAContract(
            service_code="SLA-INTERNAL-PORTALS",
            service_name="Employee SharePoint & Workforce Portals",
            service_tier="Tier-1 Business Critical",
            target_uptime_pct=99.90,
            current_monthly_uptime_pct=99.95,
            p1_response_mins=30,
            p1_resolution_hours=4.0,
            p2_response_mins=60,
            p2_resolution_hours=8.0,
            p3_resolution_hours=24.0,
            sla_penalty_clause="Standard operational remedy and next-sprint prioritization"
        )
    ]
    for sla in slas_data:
        db.add(sla)

    db.flush()
    db.commit()
    print("[Seeder] Asperion ITSM Suite successfully initialized with 8 CMDB Nodes, 3 Problems in KEDB, 2 CAB Changes, 3 Runbooks, 2 LOIs, and 3 SLAs!")
    _seed_client_portal_comprehensive(db)


def _seed_client_portal_comprehensive(db):
    """
    Seeds comprehensive data for Client Project Delivery, Billing & SLA Portal.
    Includes Enterprise Customer Accounts, Active SOW Projects, Milestone Deliverables with UAT Sign-offs,
    Commercial Tax Invoices, Support SLA Tickets, Scope Change Requests, and Legal Agreements.
    """
    print("[Seeder] Seeding Client Project Delivery, Billing & SLA Portal data...")

    # 1. Customer Accounts
    zenith_account = db.query(CustomerAccount).filter(CustomerAccount.client_name == "Zenith Global Corp").first()
    if not zenith_account:
        zenith_account = CustomerAccount(
            account_code="CUST-ZENITH-01",
            client_name="Zenith Global Corp",
            tier="Tier-1 Enterprise Retainer",
            industry="Omni-Channel Retail & Supply Chain",
            primary_csm="Sneha Rao",
            executive_sponsor="Varadi Vijay (Founder & Sole Director)",
            annual_recurring_revenue_inr=3600000.0,
            health_score=98.5,
            health_status="Healthy",
            nps_score=78,
            contract_start_date=date(2026, 6, 1),
            renewal_date=date(2027, 5, 31),
            churn_risk_level="Low / Strategic Expansion",
            notes="Anchor enterprise partner for omni-channel retail architecture. 24x7 Mission-Critical SLA under active MSA."
        )
        db.add(zenith_account)
        db.flush()

    nexus_account = db.query(CustomerAccount).filter(CustomerAccount.client_name.like("%Nexus%")).first()
    if not nexus_account:
        nexus_account = CustomerAccount(
            account_code="CUST-NEXUS-02",
            client_name="Nexus Fintech Solutions India Pvt Ltd",
            tier="Tier-1 Enterprise Retainer",
            industry="Banking & Financial Technologies",
            primary_csm="Arjun Sharma",
            executive_sponsor="Varadi Vijay (Founder & Sole Director)",
            annual_recurring_revenue_inr=4800000.0,
            health_score=96.0,
            health_status="Healthy & Scaling",
            nps_score=72,
            contract_start_date=date(2026, 5, 1),
            renewal_date=date(2027, 4, 30),
            churn_risk_level="Low",
            notes="Core banking payment gateway integration and microservices delivery."
        )
        db.add(nexus_account)
        db.flush()

    # 2. Client Projects
    zenith_proj = db.query(Project).filter(Project.project_code == "ADT-PRJ-2026-002").first()
    if not zenith_proj:
        zenith_proj = Project(
            project_code="ADT-PRJ-2026-002",
            name="Zenith Global Omni-Channel Commerce & Logistics Engine",
            client_name="Zenith Global Corp",
            project_manager="Arjun Sharma (Lead Architect)",
            budget_inr=3600000.0,
            status="Active / In Sprint 14",
            start_date=date(2026, 6, 15),
            target_end_date=date(2026, 12, 20)
        )
        db.add(zenith_proj)
        db.flush()

    # 3. Project Milestones with UAT Sign-offs
    milestones_data = [
        {
            "name": "M1: Architecture Blueprint, Security Hardening & Zero-Trust IAM",
            "target": date(2026, 7, 15),
            "summary": "Multi-region cloud infrastructure, Kubernetes microservices, WebAuthn passkey IAM, and SOC2 / DPDP 2023 threat model.",
            "pct": 25.0,
            "amt": 900000.0,
            "status": "Client Approved",
            "comp": date(2026, 7, 14),
            "signby": "Michael Chang (VP Engineering, Zenith Global)",
            "signat": datetime(2026, 7, 14, 16, 30, 0),
            "notes": "Architecture and threat model reviewed by external auditor. Approved without reservations.",
            "criteria": "Architecture blueprint signed, zero critical/high CVE findings, 99.99% IAM SLA guarantee."
        },
        {
            "name": "M2: Core Microservices, Order Orchestration & Real-Time Inventory APIs",
            "target": date(2026, 9, 30),
            "summary": "Sub-second order processing microservice, Redis cache synchronization, distributed event bus, and webhook dispatcher.",
            "pct": 30.0,
            "amt": 1080000.0,
            "status": "Client Approved",
            "comp": date(2026, 9, 28),
            "signby": "Michael Chang (VP Engineering, Zenith Global)",
            "signat": datetime(2026, 9, 28, 11, 15, 0),
            "notes": "Load testing reached 5,200 RPS with p99 latency of 18ms. Excellent performance benchmarks.",
            "criteria": "Automated test coverage >90%, P99 response <25ms, automated rollback verification."
        },
        {
            "name": "M3: Omni-Channel Customer Cockpit, Automated Reconciliation & ITSM Gateway",
            "target": date(2026, 11, 25),
            "summary": "Responsive client web & mobile portal, automated bank reconciliation engine, and direct SLA incident ticketing.",
            "pct": 25.0,
            "amt": 900000.0,
            "status": "UAT Under Review",
            "comp": None,
            "signby": None,
            "signat": None,
            "notes": "Staging build deployed. Client QA and operations team conducting final acceptance test pass.",
            "criteria": "Pass 100% of UAT functional workflows, zero Sev-1/Sev-2 blockers."
        },
        {
            "name": "M4: Production Cutover, SRE Telemetry & 24x7 Hypercare Baseline",
            "target": date(2026, 12, 20),
            "summary": "Zero-downtime blue/green DNS cutover, full SRE observability dashboards, and 30-day 24x7 hypercare support.",
            "pct": 20.0,
            "amt": 720000.0,
            "status": "Pending",
            "comp": None,
            "signby": None,
            "signat": None,
            "notes": "Scheduled for December maintenance deployment window.",
            "criteria": "Successful zero-downtime cutover, all smoke tests green."
        }
    ]

    for m in milestones_data:
        existing_m = db.query(ProjectMilestone).filter(
            ProjectMilestone.project_id == zenith_proj.id,
            ProjectMilestone.milestone_name == m["name"]
        ).first()
        if not existing_m:
            new_m = ProjectMilestone(
                project_id=zenith_proj.id,
                milestone_name=m["name"],
                target_date=m["target"],
                deliverable_summary=m["summary"],
                payment_linked_percent=m["pct"],
                billing_amount=m["amt"],
                status=m["status"],
                completion_date=m["comp"],
                signoff_by=m["signby"],
                signoff_at=m["signat"],
                signoff_notes=m["notes"],
                acceptance_criteria=m["criteria"]
            )
            db.add(new_m)

    # 4. WBS Tasks for Sprint Progress
    wbs_tasks_data = [
        ("1.1", "VPC & WireGuard VPN Tunnel Hardening", "Arjun Sharma", "Sprint 12", 24.0, 24.0, "Done", "High"),
        ("1.2", "PostgreSQL Read-Replicas & Connection Pooling", "DevOps Lead", "Sprint 12", 18.0, 18.0, "Done", "High"),
        ("2.1", "Cart Checkout Microservice & Event Queue", "Sneha Rao", "Sprint 13", 32.0, 32.0, "Done", "Critical"),
        ("2.2", "Redis Distributed Lock Manager for Flash Sales", "Arjun Sharma", "Sprint 13", 20.0, 20.0, "Done", "High"),
        ("3.1", "Client Portal Dashboard & UAT Signoff Console", "Sneha Rao", "Sprint 14", 28.0, 26.0, "Review", "High"),
        ("3.2", "Automated GST 3-Way Match & SOA Ledger Export", "Finance Lead", "Sprint 14", 16.0, 14.0, "In Progress", "Medium"),
        ("4.1", "Canary Rollout Script & Blue-Green Traffic Switcher", "DevOps Lead", "Sprint 15", 30.0, 4.0, "To Do", "Critical")
    ]
    for code, tname, assignee, sprint, est, act, status, prio in wbs_tasks_data:
        if not db.query(WBSTask).filter(WBSTask.project_id == zenith_proj.id, WBSTask.wbs_code == code).first():
            db.add(WBSTask(
                project_id=zenith_proj.id,
                wbs_code=code,
                task_name=tname,
                assigned_to=assignee,
                sprint_phase=sprint,
                estimated_hours=est,
                actual_hours=act,
                status=status,
                priority=prio,
                start_date=date(2026, 6, 20),
                due_date=date(2026, 12, 10)
            ))

    # 5. Commercial Invoices
    invoices_data = [
        {
            "inv_num": "ADT/INV/2026/0012",
            "date": date(2026, 7, 20),
            "due": date(2026, 8, 19),
            "taxable": 900000.0,
            "cgst": 81000.0,
            "sgst": 81000.0,
            "igst": 0.0,
            "tot_tax": 162000.0,
            "total": 1062000.0,
            "recv": 1062000.0,
            "bal": 0.0,
            "status": "Paid"
        },
        {
            "inv_num": "ADT/INV/2026/0028",
            "date": date(2026, 10, 5),
            "due": date(2026, 11, 4),
            "taxable": 1080000.0,
            "cgst": 97200.0,
            "sgst": 97200.0,
            "igst": 0.0,
            "tot_tax": 194400.0,
            "total": 1274400.0,
            "recv": 1274400.0,
            "bal": 0.0,
            "status": "Paid"
        },
        {
            "inv_num": "ADT/INV/2026/0045",
            "date": date(2026, 11, 15),
            "due": date(2026, 12, 15),
            "taxable": 900000.0,
            "cgst": 81000.0,
            "sgst": 81000.0,
            "igst": 0.0,
            "tot_tax": 162000.0,
            "total": 1062000.0,
            "recv": 0.0,
            "bal": 1062000.0,
            "status": "Issued / Due"
        }
    ]
    for inv in invoices_data:
        if not db.query(Invoice).filter(Invoice.invoice_number == inv["inv_num"]).first():
            db.add(Invoice(
                invoice_number=inv["inv_num"],
                invoice_date=inv["date"],
                due_date=inv["due"],
                customer_name="Zenith Global Corp",
                customer_gstin="29AABCZ9988P1Z5",
                place_of_supply="29-Karnataka",
                project_ref=zenith_proj.project_code,
                taxable_value=inv["taxable"],
                is_interstate=False,
                cgst_amount=inv["cgst"],
                sgst_amount=inv["sgst"],
                igst_amount=inv["igst"],
                total_tax=inv["tot_tax"],
                total_invoice_value=inv["total"],
                amount_received=inv["recv"],
                outstanding_balance=inv["bal"],
                status=inv["status"],
                payment_terms="Net 30 Days"
            ))

    # 6. Support Tickets
    tickets_data = [
        {
            "num": "ADT-SRV-2026-002",
            "subj": "Spike in Redis cache eviction on batch reconciliation run",
            "desc": "During 02:00 UTC nightly settlement batch, Redis key eviction triggered elevated CPU load.",
            "cat": "Performance Latency",
            "sev": "P2-High",
            "sla": 4.0,
            "status": "Resolved",
            "assignee": "DevOps & SRE Lead",
            "res": "Optimized volatile-lru eviction policy and doubled maxmemory threshold in Redis cluster.",
            "csat": 5.0
        },
        {
            "num": "ADT-SRV-2026-008",
            "subj": "Intermittent webhook timeout during peak 11.11 shopping flash sale",
            "desc": "Third-party payment gateway webhook callbacks experienced 1.8s latency timeouts during burst traffic.",
            "cat": "Integration Bug",
            "sev": "P1-Critical",
            "sla": 1.0,
            "status": "Resolved",
            "assignee": "Arjun Sharma",
            "res": "Implemented asynchronous message broker queue with exponential backoff retry and 100% message replay guarantee.",
            "csat": 5.0
        },
        {
            "num": "ADT-SRV-2026-014",
            "subj": "Request to enable automated PDF tax invoice export via webhook",
            "desc": "Zenith ERP finance system requires automated webhook push of newly issued B2B tax invoices.",
            "cat": "Platform Feature",
            "sev": "P3-Medium",
            "sla": 12.0,
            "status": "In Progress",
            "assignee": "Sneha Rao",
            "res": None,
            "csat": None
        }
    ]
    for t in tickets_data:
        if not db.query(SupportTicket).filter(SupportTicket.ticket_number == t["num"]).first():
            db.add(SupportTicket(
                ticket_number=t["num"],
                account_id=zenith_account.id,
                client_name="Zenith Global Corp",
                contact_email="engineering@zenith.com",
                subject=t["subj"],
                description=t["desc"],
                category=t["cat"],
                severity=t["sev"],
                sla_response_hours=t["sla"],
                sla_deadline=datetime.utcnow() + timedelta(hours=t["sla"]),
                assigned_engineer=t["assignee"],
                status=t["status"],
                resolution_summary=t["res"],
                csat_rating=t["csat"],
                resolved_at=datetime.utcnow() - timedelta(days=5) if t["status"] == "Resolved" else None
            ))

    # 7. Scope Change Requests
    crs_data = [
        {
            "code": "ADT-CR-2026-004",
            "title": "Add Multi-Currency Settlement for MENA Region (AED & SAR)",
            "reason": "Retail expansion into UAE and Saudi Arabian consumer markets.",
            "scope": "Payment gateway connector and real-time forex rate caching for Dubai & Riyadh hubs.",
            "cost": 350000.0,
            "days": 10,
            "status": "Client Approved",
            "approver": "Michael Chang (VP Engineering, Zenith)",
            "date": date(2026, 10, 18)
        },
        {
            "code": "ADT-CR-2026-007",
            "title": "Integrate Real-time WhatsApp Notification Gateway for Logistics",
            "reason": "Provide end-consumers with instant dispatch and live driver tracking updates.",
            "scope": "Meta Cloud API webhook integration and HSM template submission for automated delivery alerts.",
            "cost": 180000.0,
            "days": 5,
            "status": "Submitted / Under Evaluation",
            "approver": "Client Authority",
            "date": None
        }
    ]
    for cr in crs_data:
        if not db.query(ChangeRequest).filter(ChangeRequest.cr_number == cr["code"]).first():
            db.add(ChangeRequest(
                cr_number=cr["code"],
                project_id=zenith_proj.id,
                title=cr["title"],
                reason=cr["reason"],
                scope_impact=cr["scope"],
                cost_impact_inr=cr["cost"],
                schedule_impact_days=cr["days"],
                status=cr["status"],
                approver=cr["approver"],
                decision_date=cr["date"]
            ))

    # 8. Legal Contracts & SOWs
    contracts_data = [
        {
            "ref": "ADT/MSA/2026/002",
            "type": "Master Services Agreement (MSA)",
            "eff": date(2026, 6, 1),
            "exp": date(2029, 5, 31),
            "val": 15000000.0,
            "status": "Fully Executed",
            "stamp": True,
            "law": "Courts of Bengaluru, Karnataka, India",
            "cond": "99.98% Service SLA, 24x7 Tier-1 Emergency Escalation to Director Varadi Vijay, Annual SOC2 Audit Rights."
        },
        {
            "ref": "ADT/SOW/2026/001",
            "type": "Statement of Work (SOW)",
            "eff": date(2026, 6, 15),
            "exp": date(2026, 12, 31),
            "val": 3600000.0,
            "status": "Fully Executed",
            "stamp": True,
            "law": "Courts of Bengaluru, Karnataka, India",
            "cond": "4-Phase Milestone Linked Billing with Mandatory Client UAT Signoff before Tax Invoicing."
        },
        {
            "ref": "ADT/NDA/2026/001",
            "type": "Mutual Non-Disclosure Agreement (MNDA)",
            "eff": date(2026, 5, 15),
            "exp": date(2031, 5, 14),
            "val": 0.0,
            "status": "Fully Executed",
            "stamp": True,
            "law": "Courts of Bengaluru, Karnataka, India",
            "cond": "Strict 5-year confidentiality obligation covering trade secrets, proprietary algorithms, and customer PII."
        }
    ]
    for c in contracts_data:
        if not db.query(ClientContract).filter(ClientContract.contract_reference == c["ref"]).first():
            db.add(ClientContract(
                contract_reference=c["ref"],
                client_name="Zenith Global Corp",
                contract_type=c["type"],
                effective_date=c["eff"],
                expiry_date=c["exp"],
                value_inr=c["val"],
                status=c["status"],
                stamp_duty_paid=c["stamp"],
                governing_law=c["law"],
                ip_ownership_clause="Asperion Digital Technologies retains core framework IP; Zenith Global owns bespoke business logic.",
                special_conditions=c["cond"]
            ))

    db.flush()
    db.commit()
    print("[Seeder] Client Project Delivery, Billing & SLA Portal successfully seeded with Zenith Global & Enterprise records!")
    _seed_agentic_ai(db)


def _seed_agentic_ai(db):
    """
    Seeds Asperion Enterprise Agentic AI & Autonomous Swarm Suite.
    Includes 5 specialized autonomous agent personas, initial missions with ReAct thought chains,
    and granular SOC2/ISO 27001 execution audit traces.
    """
    if db.query(EnterpriseAgent).first():
        return

    print("[Seeder] Initializing Asperion Agentic AI & Autonomous Multi-Agent Swarm...")
    
    # 1. Specialized Agent Personas
    agents_data = [
        {
            "agent_code": "AGT-SRE-01",
            "name": "SRE & DevSecOps Sentinel",
            "role": "Autonomous Systems Reliability Engineer",
            "department": "Engineering & Infrastructure",
            "model_endpoint": "Gemini 2.5 Pro (1M Context)",
            "autonomy_tier": "Level 4: Fully Autonomous",
            "system_prompt": (
                "You are the Lead Autonomous Systems Reliability Engineer for ASPERION DIGITAL TECHNOLOGIES "
                "(OPC) PRIVATE LIMITED. Your core directive is 99.98% uptime SLA assurance across all CMDB Tier-0 "
                "nodes, automated health checks, CVE dependency remediation, and self-healing runbook execution."
            ),
            "assigned_tools": [
                "mcp_cmdb_telemetry_scan", "runbook_health_check", "cve_dependency_audit",
                "auto_healing_circuit_breaker", "nginx_load_balancer_rebalance"
            ],
            "is_active": True,
            "health_status": "Optimal",
            "total_missions_executed": 38,
            "success_rate_pct": 99.7,
            "avg_execution_latency_sec": 1.9
        },
        {
            "agent_code": "AGT-COMPLY-01",
            "name": "Statutory & ISO 27001 Auditor",
            "role": "Autonomous Compliance & Data Protection Officer",
            "department": "Legal & Regulatory",
            "model_endpoint": "Gemini 2.5 Pro (1M Context)",
            "autonomy_tier": "Level 3: Supervised Autonomy",
            "system_prompt": (
                "You are the Autonomous Statutory Compliance & Data Protection Officer for ASPERION DIGITAL TECHNOLOGIES "
                "(OPC) PRIVATE LIMITED (CIN: U85500KA2026OPC222069). You verify MCA ROC filings, GST-1/3B statutory "
                "calendars, ISO 27001:2022 annex controls, and enforce India Digital Personal Data Protection (DPDP) Act 2023."
            ),
            "assigned_tools": [
                "mcp_statutory_calendar_audit", "gst_challan_cross_match", "iso_clause_verifier",
                "dpdp_pii_sanitizer", "mca_annual_return_verifier"
            ],
            "is_active": True,
            "health_status": "Optimal",
            "total_missions_executed": 24,
            "success_rate_pct": 100.0,
            "avg_execution_latency_sec": 2.6
        },
        {
            "agent_code": "AGT-FINOPS-01",
            "name": "FinOps & Invoice Reconciliation Engine",
            "role": "Autonomous Corporate Treasury & Invoicing Specialist",
            "department": "Finance & Accounts",
            "model_endpoint": "Gemini 2.5 Flash (Fast Execution)",
            "autonomy_tier": "Level 2: Human-in-the-Loop Required",
            "system_prompt": (
                "You are the Autonomous FinOps & Commercial Invoicing Specialist for Asperion Digital Technologies. "
                "You calculate 18% GST (CGST 9% + SGST 9% / IGST 18%), 10% TDS Section 194J deductions, match bank "
                "reconciliation statements, and require Director Varadi Vijay's explicit authorization for tax invoice issuance."
            ),
            "assigned_tools": [
                "mcp_tds_gst_calculator", "bank_statement_reconciler", "invoice_due_escalator",
                "e_invoice_qr_generator", "retention_ledger_auditor"
            ],
            "is_active": True,
            "health_status": "Optimal",
            "total_missions_executed": 42,
            "success_rate_pct": 98.8,
            "avg_execution_latency_sec": 1.4
        },
        {
            "agent_code": "AGT-TALENT-01",
            "name": "Talent & Smart Workforce Copilot",
            "role": "Autonomous HR & Workforce Intelligence Lead",
            "department": "Human Capital",
            "model_endpoint": "Gemini 2.5 Flash (Fast Execution)",
            "autonomy_tier": "Level 3: Supervised Autonomy",
            "system_prompt": (
                "You are the Autonomous HR & Workforce Intelligence Copilot for Asperion Digital Technologies. "
                "You validate GPS geofence radius check-ins, webcam snapshot liveness, POSH compliance policy adherence, "
                "and detect attendance anomalies across Bangalore HQ and remote workforce locations."
            ),
            "assigned_tools": [
                "mcp_geofence_attendance_validator", "posh_escalation_guardrail", "payroll_discrepancy_finder",
                "biometric_webcam_certifier", "separation_clearance_orchestrator"
            ],
            "is_active": True,
            "health_status": "Optimal",
            "total_missions_executed": 65,
            "success_rate_pct": 99.4,
            "avg_execution_latency_sec": 1.2
        },
        {
            "agent_code": "AGT-DELIVERY-01",
            "name": "Client Delivery & SLA Guardian",
            "role": "Autonomous Delivery Assurance & SLA Manager",
            "department": "Client Services",
            "model_endpoint": "Gemini 2.5 Pro (1M Context)",
            "autonomy_tier": "Level 4: Fully Autonomous",
            "system_prompt": (
                "You are the Autonomous Delivery Assurance & SLA Manager for Asperion Digital Technologies. "
                "You continuously evaluate enterprise client project milestones (e.g. Zenith Global Corp), track UAT "
                "acceptance signoffs, predict delivery delays, and assure SLA ticket response within 15 minutes."
            ),
            "assigned_tools": [
                "mcp_project_milestone_evaluator", "client_billing_burn_analyzer", "sla_breach_predictor",
                "uat_signoff_auditor", "scope_creep_detector"
            ],
            "is_active": True,
            "health_status": "Optimal",
            "total_missions_executed": 31,
            "success_rate_pct": 100.0,
            "avg_execution_latency_sec": 2.1
        }
    ]

    agent_records = {}
    for a in agents_data:
        agent = EnterpriseAgent(
            agent_code=a["agent_code"],
            name=a["name"],
            role=a["role"],
            department=a["department"],
            model_endpoint=a["model_endpoint"],
            autonomy_tier=a["autonomy_tier"],
            system_prompt=a["system_prompt"],
            assigned_tools_json=json.dumps(a["assigned_tools"]),
            is_active=a["is_active"],
            health_status=a["health_status"],
            total_missions_executed=a["total_missions_executed"],
            success_rate_pct=a["success_rate_pct"],
            avg_execution_latency_sec=a["avg_execution_latency_sec"]
        )
        db.add(agent)
        db.flush()
        agent_records[a["agent_code"]] = agent

    # 2. Seed Initial Missions with ReAct chains and execution traces
    # Mission 1: SRE
    sre_agent = agent_records["AGT-SRE-01"]
    m1 = AgenticMission(
        mission_code="MSN-2026-0081",
        agent_id=sre_agent.id,
        title="Autonomous CMDB Tier-0 Health Scan & Runbook Certification",
        trigger_type="Scheduled Autonomous Cron",
        input_parameters_json=json.dumps({"target_ci": "ALL_TIER_0", "scan_depth": "FULL_METRIC_HARVEST"}),
        status="Completed",
        thought_chain_json=json.dumps([
            {"step": 1, "phase": "GOAL_DECOMPOSITION", "thought": "Executing periodic Tier-0 infrastructure integrity scan across Bangalore HQ & VPC clusters."},
            {"step": 2, "phase": "POLICY_GUARDRAIL_EVALUATION", "thought": "Ensured scan operations use read-only telemetry metrics without affecting production traffic."},
            {"step": 3, "phase": "TOOL_EXECUTION", "tool": "mcp_cmdb_telemetry_scan", "observation": "8 Configuration Items scanned. Primary API Gateway and PostgreSQL node healthy (99.4% aggregate health)."},
            {"step": 4, "phase": "REFLECTION_AND_SYNTHESIS", "thought": "Tier-0 nodes fully conform to 99.98% uptime SLA commitments."}
        ]),
        executed_tools_json=json.dumps(["mcp_cmdb_telemetry_scan", "runbook_health_check", "cve_dependency_audit"]),
        output_summary="Autonomous SRE scan completed successfully. Evaluated 8 CMDB Configuration Items and verified Tier-0 uptime SLA at 99.98%. Runbook playbooks validated in standby mode. Zero critical anomalies detected.",
        artifacts_generated_json=json.dumps([{"title": "System Health Attestation", "type": "HEALTH_REPORT", "ref": "REP-SRE-2026-01"}]),
        started_at=datetime.utcnow() - timedelta(hours=3),
        completed_at=datetime.utcnow() - timedelta(hours=3) + timedelta(seconds=2),
        execution_duration_sec=2.1
    )
    db.add(m1)
    db.flush()

    traces_m1 = [
        AgentExecutionTrace(mission_id=m1.id, step_number=1, action_type="GOAL_DECOMPOSITION", latency_ms=65.0, tokens_consumed=380, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m1.id, step_number=2, action_type="POLICY_GUARDRAIL_CHECK", latency_ms=90.0, tokens_consumed=410, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m1.id, step_number=3, action_type="TOOL_CALL", tool_name="mcp_cmdb_telemetry_scan", tool_input_json=json.dumps({"target": "Tier-0"}), tool_output_json=json.dumps({"scanned_nodes": 8, "status": "Operational"}), latency_ms=420.0, tokens_consumed=620, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m1.id, step_number=4, action_type="REFLECTION", latency_ms=110.0, tokens_consumed=290, guardrail_passed=True)
    ]
    for t in traces_m1:
        db.add(t)

    # Mission 2: Compliance
    comply_agent = agent_records["AGT-COMPLY-01"]
    m2 = AgenticMission(
        mission_code="MSN-2026-0082",
        agent_id=comply_agent.id,
        title="Annual MCA ROC & DPDP Act 2023 Statutory Governance Audit",
        trigger_type="User Dispatched",
        input_parameters_json=json.dumps({"entity": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED", "scope": "STATUTORY_AND_PII"}),
        status="Completed",
        thought_chain_json=json.dumps([
            {"step": 1, "phase": "GOAL_DECOMPOSITION", "thought": "Auditing statutory calendar items, MCA Form AOC-4/MGT-7 filings, and DPDP 2023 employee consent records."},
            {"step": 2, "phase": "TOOL_EXECUTION", "tool": "mcp_statutory_calendar_audit", "observation": "Verified CIN U85500KA2026OPC222069. All 6 statutory compliance deadlines mapped with 0 penalties."},
            {"step": 3, "phase": "TOOL_EXECUTION", "tool": "dpdp_pii_sanitizer", "observation": "All employee national identifiers (PAN, Aadhaar) secured in encrypted vault with zero plaintext exposures."}
        ]),
        executed_tools_json=json.dumps(["mcp_statutory_calendar_audit", "gst_challan_cross_match", "dpdp_pii_sanitizer"]),
        output_summary="Statutory & DPDP Compliance verification complete. 100% adherence to MCA statutory calendar for FY 2026-27. Director Varadi Vijay's authorized signing powers verified in board resolution archive.",
        artifacts_generated_json=json.dumps([{"title": "Statutory Compliance Certificate", "type": "AUDIT_CERTIFICATE", "ref": "AUDIT-2026-Q1"}]),
        started_at=datetime.utcnow() - timedelta(hours=2),
        completed_at=datetime.utcnow() - timedelta(hours=2) + timedelta(seconds=3),
        execution_duration_sec=2.8
    )
    db.add(m2)
    db.flush()

    traces_m2 = [
        AgentExecutionTrace(mission_id=m2.id, step_number=1, action_type="GOAL_DECOMPOSITION", latency_ms=70.0, tokens_consumed=420, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m2.id, step_number=2, action_type="TOOL_CALL", tool_name="mcp_statutory_calendar_audit", tool_input_json=json.dumps({"fy": "2026-27"}), tool_output_json=json.dumps({"filings_checked": 6, "compliance_rate": "100%"}), latency_ms=390.0, tokens_consumed=550, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m2.id, step_number=3, action_type="REFLECTION", latency_ms=85.0, tokens_consumed=310, guardrail_passed=True)
    ]
    for t in traces_m2:
        db.add(t)

    # Mission 3: FinOps (Requires Human Approval)
    finops_agent = agent_records["AGT-FINOPS-01"]
    m3 = AgenticMission(
        mission_code="MSN-2026-0083",
        agent_id=finops_agent.id,
        title="Zenith Global Corp Retainer Invoice Verification & TDS Reconciliation",
        trigger_type="Incident Auto-Escalation",
        input_parameters_json=json.dumps({"client": "Zenith Global Corp", "invoice_ref": "ADT/INV/2026/001", "action": "TAX_RECONCILIATION"}),
        status="Requires Human Approval",
        thought_chain_json=json.dumps([
            {"step": 1, "phase": "GOAL_DECOMPOSITION", "thought": "Auditing invoice ADT/INV/2026/001 for Zenith Global Corp (Base INR 6,00,000 + 18% GST INR 1,08,000 = INR 7,08,000)."},
            {"step": 2, "phase": "TOOL_EXECUTION", "tool": "mcp_tds_gst_calculator", "observation": "Computed TDS Section 194J (10% of base) = INR 60,000. Net receivable expected: INR 6,48,000."},
            {"step": 3, "phase": "POLICY_GUARDRAIL_EVALUATION", "thought": "FinOps policy requires Director Varadi Vijay's explicit authorization before locking statutory ledger entry."},
            {"step": 4, "phase": "SUSPEND_FOR_HUMAN_IN_THE_LOOP", "observation": "Mission suspended. Awaiting Director approval gate."}
        ]),
        executed_tools_json=json.dumps(["mcp_tds_gst_calculator", "bank_statement_reconciler"]),
        output_summary="Invoice ADT/INV/2026/001 validated against SOW terms. GST 18% (INR 1,08,000) and TDS Section 194J (INR 60,000) verified. Ledger lock queued for Human-in-the-Loop authorization by Director Varadi Vijay.",
        artifacts_generated_json=json.dumps([{"title": "Commercial Tax Reconciliation Summary", "type": "FINANCE_RECON", "ref": "RECON-INV-001"}]),
        started_at=datetime.utcnow() - timedelta(minutes=45),
        completed_at=None,
        execution_duration_sec=1.5
    )
    db.add(m3)
    db.flush()

    traces_m3 = [
        AgentExecutionTrace(mission_id=m3.id, step_number=1, action_type="GOAL_DECOMPOSITION", latency_ms=50.0, tokens_consumed=340, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m3.id, step_number=2, action_type="TOOL_CALL", tool_name="mcp_tds_gst_calculator", tool_input_json=json.dumps({"base": 600000.0}), tool_output_json=json.dumps({"gst": 108000.0, "tds": 60000.0}), latency_ms=180.0, tokens_consumed=410, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m3.id, step_number=3, action_type="POLICY_GUARDRAIL_CHECK", latency_ms=95.0, tokens_consumed=290, guardrail_passed=True)
    ]
    for t in traces_m3:
        db.add(t)

    # Mission 4: Client Delivery
    delivery_agent = agent_records["AGT-DELIVERY-01"]
    m4 = AgenticMission(
        mission_code="MSN-2026-0084",
        agent_id=delivery_agent.id,
        title="Zenith Enterprise Cloud Transformation Milestone 3 SLA Assurance",
        trigger_type="Event-Driven Webhook",
        input_parameters_json=json.dumps({"project": "Zenith Global Enterprise Cloud Migration", "milestone": "Phase 3: Production Cutover"}),
        status="Completed",
        thought_chain_json=json.dumps([
            {"step": 1, "phase": "GOAL_DECOMPOSITION", "thought": "Auditing sprint progress, UAT test execution logs, and SLA ticket response times for Zenith Global."},
            {"step": 2, "phase": "TOOL_EXECUTION", "tool": "mcp_project_milestone_evaluator", "observation": "Milestones 1 & 2 100% completed with formal client UAT signoffs. Phase 3 tracking on schedule at 45%."},
            {"step": 3, "phase": "TOOL_EXECUTION", "tool": "sla_breach_predictor", "observation": "Mean First Response Time = 11.4 mins (well within 15 min Tier-1 SLA threshold). Zero SLA breaches."}
        ]),
        executed_tools_json=json.dumps(["mcp_project_milestone_evaluator", "client_billing_burn_analyzer", "sla_breach_predictor"]),
        output_summary="Client delivery assurance verification passed. Zenith Global Corp Cloud Transformation tracking at 100% on-time milestone delivery with zero SLA penalties and verified UAT attestations.",
        artifacts_generated_json=json.dumps([{"title": "Delivery SLA Assurance Dossier", "type": "SLA_REPORT", "ref": "SLA-ZENITH-2026-M3"}]),
        started_at=datetime.utcnow() - timedelta(minutes=20),
        completed_at=datetime.utcnow() - timedelta(minutes=20) + timedelta(seconds=2),
        execution_duration_sec=2.2
    )
    db.add(m4)
    db.flush()

    traces_m4 = [
        AgentExecutionTrace(mission_id=m4.id, step_number=1, action_type="GOAL_DECOMPOSITION", latency_ms=60.0, tokens_consumed=390, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m4.id, step_number=2, action_type="TOOL_CALL", tool_name="mcp_project_milestone_evaluator", tool_input_json=json.dumps({"project": "Zenith"}), tool_output_json=json.dumps({"milestones_verified": 4, "uat_signed": True}), latency_ms=310.0, tokens_consumed=480, guardrail_passed=True),
        AgentExecutionTrace(mission_id=m4.id, step_number=3, action_type="TOOL_CALL", tool_name="sla_breach_predictor", tool_input_json=json.dumps({"threshold": "15m"}), tool_output_json=json.dumps({"breach_risk": "None", "avg_response": "11.4m"}), latency_ms=290.0, tokens_consumed=430, guardrail_passed=True)
    ]
    for t in traces_m4:
        db.add(t)

    db.flush()
    db.commit()
    print("[Seeder] Agentic AI & Autonomous Swarm successfully initialized with 5 Enterprise Agents and 4 Mission Records!")

def _seed_enterprise_operations(db):
    """
    Seeds initial Cryptographic Tamper-Evident Event Ledger, BCP/DR Snapshots,
    India DPDP Act 2023 Statutory Consent Register, and Diagnostic Telemetry.
    """
    from app.engines.operations_engine import append_event_ledger, create_database_backup_snapshot, record_dpdp_consent

    # 1. Seed Cryptographically Chained Event Ledger starting from Genesis Block
    events_data = [
        {
            "aggregate_type": "SYSTEM",
            "aggregate_id": "SYS-INIT",
            "event_type": "GENESIS_INITIALIZATION",
            "actor_name": "Varadi Vijay",
            "actor_role": "Sole Director / Root Authority",
            "department": "Core Governance",
            "payload": {
                "system": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
                "cin": "U85500KA2026OPC222069",
                "hq": "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore - 560043",
                "charter": "Enterprise OS Baseline Initialization with Cryptographic Tamper-Evident Hash Chaining"
            }
        },
        {
            "aggregate_type": "BOARD_GOVERNANCE",
            "aggregate_id": "ADT/RES/2026/001",
            "event_type": "BOARD_RESOLUTION_PASSED",
            "actor_name": "Varadi Vijay",
            "actor_role": "Sole Director",
            "department": "Governance",
            "payload": {
                "resolution": "ADT/RES/2026/001",
                "title": "Opening of Corporate Current Bank Account with ICICI Bank Ltd",
                "signatory": "Varadi Vijay",
                "quorum": "100% Sole Member Quorum"
            }
        },
        {
            "aggregate_type": "STATUTORY_FINANCE",
            "aggregate_id": "CHALLAN-IT-2026-Q1",
            "event_type": "TDS_CHALLAN_FILING",
            "actor_name": "Kavita Krishnan",
            "actor_role": "Head of Finance",
            "department": "Finance & Accounts",
            "payload": {
                "challan_no": "ITNS-281-948102",
                "section": "194J - Professional & Technical Fees",
                "amount_inr": 60000.0,
                "bsr_code": "0001234",
                "tax_period": "Q1 2026-27"
            }
        },
        {
            "aggregate_type": "ITSM_CHANGE",
            "aggregate_id": "CHG-2026-0041",
            "event_type": "CAB_PRODUCTION_CUTOVER_APPROVED",
            "actor_name": "CAB Review Board",
            "actor_role": "Change Advisory Authority",
            "department": "IT Operations",
            "payload": {
                "change_ref": "CHG-2026-0041",
                "system": "Customer Support Gateway Blue-Green Deployment",
                "downtime_allowed_sec": 0,
                "rollback_digest": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
            }
        },
        {
            "aggregate_type": "CLIENT_DELIVERY",
            "aggregate_id": "ZENITH-MS-003",
            "event_type": "MILESTONE_SLA_ACCEPTANCE_ATTESTED",
            "actor_name": "Marcus Vance",
            "actor_role": "VP Engineering (Client Sponsor)",
            "department": "Client Delivery",
            "payload": {
                "project": "Zenith Cloud Transformation",
                "milestone": "Phase 3: Production Cutover",
                "sla_adherence_pct": 100.0,
                "client_signoff_by": "Marcus Vance (VP Engineering, Zenith Global)"
            }
        }
    ]

    for ev in events_data:
        append_event_ledger(
            db=db,
            aggregate_type=ev["aggregate_type"],
            aggregate_id=ev["aggregate_id"],
            event_type=ev["event_type"],
            actor_name=ev["actor_name"],
            actor_role=ev["actor_role"],
            department=ev["department"],
            payload=ev["payload"]
        )

    # 2. Seed Initial BCP/DR Snapshots
    create_database_backup_snapshot(
        db=db,
        backup_type="Full SQLite Hot Backup",
        notes="Daily automated enterprise baseline snapshot. SHA-256 verified."
    )

    create_database_backup_snapshot(
        db=db,
        backup_type="Incremental WAL Snapshot",
        notes="Hourly RPO transaction log snapshot. Verified against live database."
    )

    # 3. Seed India DPDP Act 2023 Statutory Consent Records
    consents_data = [
        {
            "data_principal_name": "Varadi Vijay",
            "data_principal_type": "Employee",
            "principal_identifier": "EMP-2026-001",
            "purpose_category": "Statutory Directorship & Corporate MCA Filings",
            "notice_reference": "ADT/DPDP/NOTICE/2026/V1",
            "consent_status": "Granted",
            "audit_notes": "Sole Member Director statutory consent logged with MCA Class-3 DSC token."
        },
        {
            "data_principal_name": "Kavita Krishnan",
            "data_principal_type": "Employee",
            "principal_identifier": "EMP-2026-002",
            "purpose_category": "Statutory Payroll, EPF/ESIC & Wage Code Compliance",
            "notice_reference": "ADT/DPDP/NOTICE/2026/V1",
            "consent_status": "Granted",
            "audit_notes": "Employee Portal affirmative clickwrap consent with Aadhaar / PAN mask verification."
        },
        {
            "data_principal_name": "Marcus Vance",
            "data_principal_type": "Client Sponsor",
            "principal_identifier": "CLIENT-ZENITH-01",
            "purpose_category": "Contractual Performance & Client Delivery Portal Access",
            "notice_reference": "ADT/DPDP/NOTICE/2026/V1",
            "consent_status": "Granted",
            "audit_notes": "Zenith Global Corp MSA Schedule D consent authorization."
        }
    ]

    for c in consents_data:
        record_dpdp_consent(
            db=db,
            data_principal_name=c["data_principal_name"],
            data_principal_type=c["data_principal_type"],
            principal_identifier=c["principal_identifier"],
            purpose_category=c["purpose_category"],
            notice_reference=c["notice_reference"],
            consent_status=c["consent_status"],
            audit_notes=c["audit_notes"]
        )

    db.commit()
    print("[Seeder] Enterprise Operations, Cryptographic Ledger & DPDP Consent successfully initialized!")


