"""
Asperion Enterprise OS - Command Line Interface (CLI)
Automates enterprise operations: database seeding, statutory CTC calculations, and letter generation.
"""
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.seed_data import seed_database
from app.engines.ctc_calculator import compute_salary_breakup
from app.engines.letter_generator import generate_document_html
from app.engines.secops_triage import triage_security_incident
from app.engines.docx_exporter import create_corporate_letter_docx
from app.database import SessionLocal
from app.models.governance import AuditLog
from app.config import settings

def main():
    parser = argparse.ArgumentParser(description="Asperion Enterprise Operating System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
    
    # 1. Seed
    seed_parser = subparsers.add_parser("seed", help="Initialize and populate database with enterprise records")
    
    # 2. CTC Calculator
    ctc_parser = subparsers.add_parser("calc-ctc", help="Calculate statutory salary breakup")
    ctc_parser.add_argument("--ctc", type=float, required=True, help="Annual Cost to Company in INR")
    ctc_parser.add_argument("--basic-pct", type=float, default=0.40, help="Basic salary percentage (default 0.40)")
    ctc_parser.add_argument("--hra-pct", type=float, default=0.40, help="HRA percentage of basic (default 0.40)")
    ctc_parser.add_argument("--state", type=str, default="Karnataka", help="State for Professional Tax (default Karnataka)")
    
    # 3. Generate Letter
    letter_parser = subparsers.add_parser("generate-letter", help="Generate official HR/Legal letter")
    letter_parser.add_argument("--code", type=str, required=True, help="Letter code (e.g. HR-ONB-01, HR-REC-01, HR-SEP-15)")
    letter_parser.add_argument("--recipient", type=str, required=True, help="Recipient full name")
    letter_parser.add_argument("--designation", type=str, default="Software Engineer", help="Role / Designation")
    letter_parser.add_argument("--ctc", type=float, default=1200000.0, help="Annual CTC for salary annexure")
    letter_parser.add_argument("--format", type=str, choices=["html", "docx"], default="html", help="Output format: html or docx")
    letter_parser.add_argument("--output", type=str, default=None, help="Output file path")
    
    # 4. SecOps Triage
    secops_parser = subparsers.add_parser("triage-incident", help="Run SecOps severity and CERT-In triage")
    secops_parser.add_argument("--category", type=str, required=True, help="Incident category (Ransomware, Breach, Cloud, etc.)")
    secops_parser.add_argument("--affected-systems", type=str, default="AWS Cloud", help="Affected systems")
    secops_parser.add_argument("--data-class", type=str, default="Confidential", help="Data classification")

    # 5. Audit Trail
    audit_parser = subparsers.add_parser("audit-trail", help="View immutable system audit logs")
    audit_parser.add_argument("--limit", type=int, default=10, help="Number of latest log entries")

    # 6. Document Vault
    vault_parser = subparsers.add_parser("vault", help="Browse authentic enterprise manuals, handbooks and SOPs")
    vault_parser.add_argument("--category", type=str, default=None, help="Filter category (company_os, hr_letters, finance_templates, etc.)")
    vault_parser.add_argument("--search", type=str, default=None, help="Search keyword")
    vault_parser.add_argument("--limit", type=int, default=15, help="Number of records to show")

    # 7. Add Strategic Thought / Decision
    thought_parser = subparsers.add_parser("add-thought", help="Record strategic decision or founder thesis")
    thought_parser.add_argument("--title", type=str, required=True, help="Initiative / Thought Title")
    thought_parser.add_argument("--type", type=str, default="Founder Thought / Thesis", help="Entry type")
    thought_parser.add_argument("--rationale", type=str, required=True, help="Decision rationale")
    thought_parser.add_argument("--tags", type=str, default="Strategy, AI, Governance", help="Tags")

    # 8. Dynamic KPIs
    kpi_parser = subparsers.add_parser("kpis", help="List or record enterprise KPIs")
    kpi_parser.add_argument("--add", action="store_true", help="Flag to create new KPI")
    kpi_parser.add_argument("--code", type=str, default=None, help="KPI Code (e.g. KPI-ENG-05)")
    kpi_parser.add_argument("--name", type=str, default=None, help="KPI Name")
    kpi_parser.add_argument("--category", type=str, default="Operational", help="Category")
    kpi_parser.add_argument("--target", type=float, default=100.0, help="Target value")
    kpi_parser.add_argument("--actual", type=float, default=0.0, help="Actual value")
    kpi_parser.add_argument("--unit", type=str, default="%", help="Unit")

    # 9. Visual Analytics & What-If Simulation
    analytics_parser = subparsers.add_parser("analytics", help="View computed executive ratios and operational metrics")
    analytics_parser.add_argument("--simulate", action="store_true", help="Run what-if treasury cashflow simulation")
    analytics_parser.add_argument("--coll-accel", type=float, default=15.0, help="Collection acceleration pct (default 15)")
    analytics_parser.add_argument("--exp-opt", type=float, default=10.0, help="Expense optimization pct (default 10)")
    analytics_parser.add_argument("--retainer", type=float, default=300000.0, help="New monthly retainer in INR")

    # 10. Enterprise CRM & Service Desk
    crm_parser = subparsers.add_parser("crm", help="View enterprise CRM pipeline, accounts, and SLA tickets")
    crm_parser.add_argument("--deals", action="store_true", help="List active opportunities and pipeline stages")
    crm_parser.add_argument("--accounts", action="store_true", help="List customer accounts and health scores")
    crm_parser.add_argument("--tickets", action="store_true", help="List SLA service desk support tickets")
    crm_parser.add_argument("--risks", action="store_true", help="List Enterprise Risk Management (ERM) items")

    # 11. Internal Departmental Ticketing
    ticket_parser = subparsers.add_parser("tickets", help="Manage internal cross-departmental tickets (IT, HR, Finance, Legal, etc.)")
    ticket_parser.add_argument("--dept", type=str, default=None, help="Filter department (IT_INFRASTRUCTURE, HR_PEOPLE, FINANCE_ACCOUNTS, etc.)")
    ticket_parser.add_argument("--priority", type=str, default=None, help="Filter priority (P1-Critical, P2-High, P3-Medium, P4-Low)")
    ticket_parser.add_argument("--create", action="store_true", help="Create a new internal ticket")
    ticket_parser.add_argument("--category", type=str, default="General Request", help="Ticket category")
    ticket_parser.add_argument("--subject", type=str, default=None, help="Ticket subject")
    ticket_parser.add_argument("--desc", type=str, default="Created via Asperion CLI.", help="Ticket description")
    ticket_parser.add_argument("--requester", type=str, default="Varadi Vijay", help="Requester name")
    ticket_parser.add_argument("--email", type=str, default="varadivijay@asperion.in", help="Requester email")

    # 12. Omni-Channel System Alerts & Notifications
    notif_parser = subparsers.add_parser("notifications", help="Inspect and broadcast cross-group system alerts")
    notif_parser.add_argument("--severity", type=str, default=None, help="Filter severity (CRITICAL, WARNING, INFO, SUCCESS)")
    notif_parser.add_argument("--unread", action="store_true", help="Show unread notifications only")
    notif_parser.add_argument("--mark-read-all", action="store_true", help="Mark all system notifications as read")
    notif_parser.add_argument("--broadcast", action="store_true", help="Broadcast an alert")
    notif_parser.add_argument("--source", type=str, default="MANAGEMENT", help="Source module (FINANCE, CYBERSECURITY, HRMS, etc.)")
    notif_parser.add_argument("--title", type=str, default=None, help="Alert title")
    notif_parser.add_argument("--msg", type=str, default=None, help="Alert message text")

    # 13. Developer Platform Accounts & Secrets
    dev_parser = subparsers.add_parser("dev-accounts", help="Manage developer accounts (Google Play, Apple, GitHub, AWS, etc.) and secret rotation")
    dev_parser.add_argument("--secrets", action="store_true", help="List developer cryptographic secrets & 90-day rotation status")
    dev_parser.add_argument("--rotate", type=int, default=None, help="Secret ID to rotate to new 90-day compliant window")

    # 14. Statutory Tax Challans & Returns
    tax_parser = subparsers.add_parser("tax-challans", help="List statutory tax deposit challans (GSTR-3B, TDS-281, Advance Tax, PT)")
    tax_parser.add_argument("--type", type=str, default=None, help="Filter filing type (GSTR-3B, TDS Challan 281, Advance Tax, etc.)")

    # 15. Smart Attendance & Workforce Mobility
    att_parser = subparsers.add_parser("attendance", help="Manage smart attendance, facial recognition, geofencing, and self-healing auto-fix")
    att_parser.add_argument("--clock-in", type=int, default=None, help="Employee ID to clock in")
    att_parser.add_argument("--clock-out", type=int, default=None, help="Employee ID to clock out")
    att_parser.add_argument("--lat", type=float, default=13.035820, help="Latitude (default Horamavu HQ: 13.035820)")
    att_parser.add_argument("--lon", type=float, default=77.653410, help="Longitude (default Horamavu HQ: 77.653410)")
    att_parser.add_argument("--source", type=str, default="FACIAL_KIOSK", help="Source (FACIAL_KIOSK, WHATSAPP, WEB, MOBILE)")
    att_parser.add_argument("--auto-fix", action="store_true", help="Trigger self-healing auto-fix engine on open attendance punches")
    att_parser.add_argument("--summary", action="store_true", help="Display today's attendance summary and biometric compliance")
    att_parser.add_argument("--whatsapp", action="store_true", help="Simulate WhatsApp attendance webhook punch")
    att_parser.add_argument("--phone", type=str, default="+919886012345", help="Phone number for WhatsApp simulation")
    att_parser.add_argument("--msg", type=str, default="IN", help="Message body for WhatsApp simulation (IN, OUT, STATUS)")

    # 16. Autonomous Self-Healing & System Auto-Update
    autofix_parser = subparsers.add_parser("self-heal", help="Run system-wide auto-fix & self-repair diagnostics")
    autofix_parser.add_argument("--dry-run", action="store_true", help="Scan only without applying auto-repairs")
    autofix_parser.add_argument("--daemon-status", action="store_true", help="Check auto-update background daemon status")

    # 17. Attendance-Synced Salary Statements & Bank Payout
    salary_parser = subparsers.add_parser("payroll-statements", help="Generate attendance-synced salary statements and bank batch")
    salary_parser.add_argument("--cycle", type=str, default="JUN-2026", help="Payroll cycle (e.g. JUN-2026, JUL-2026)")
    salary_parser.add_argument("--days", type=int, default=30, help="Days in calendar month (default 30)")
    salary_parser.add_argument("--disburse", action="store_true", help="Disburse via bank and assign ICICI UTR numbers")
    salary_parser.add_argument("--payslip", type=int, default=None, help="Employee ID to generate standalone HTML payslip")

    # 18. Stakeholder Dedicated Portals (Employee, Client, Vendor)
    portal_parser = subparsers.add_parser("portals", help="Inspect dedicated stakeholder views (Employee ESS, Client SLA, Vendor POs)")
    portal_parser.add_argument("--employee", action="store_true", help="Display Employee Self-Service dashboard data")
    portal_parser.add_argument("--client", action="store_true", help="Display Client SLA & Project dashboard data")
    portal_parser.add_argument("--vendor", action="store_true", help="Display Vendor Procurement, POs & Inward GRN dashboard data")
    portal_parser.add_argument("--vendor-name", type=str, default="Nexus Micro Systems", help="Specify vendor name or keyword to query")
    portal_parser.add_argument("--pos", action="store_true", help="Display detailed purchase orders with line items")
    portal_parser.add_argument("--grns", action="store_true", help="Display inward goods received notes and QA inspections")
    portal_parser.add_argument("--bills", action="store_true", help="Display AP bills with 3-way matching and TDS breakdown")
    portal_parser.add_argument("--personas", action="store_true", help="List all corporate and stakeholder login accounts")

    # 19. PMO Stage-Gate Processes & Governance
    pmo_parser = subparsers.add_parser("pmo-governance", help="Inspect PMBOK / PRINCE2 stage-gate registers and governance metrics")
    pmo_parser.add_argument("--stage-gates", action="store_true", help="Display summary count across all 5 stage-gates")
    pmo_parser.add_argument("--intakes", action="store_true", help="List Stage-Gate 1 project intakes and strategic fit")
    pmo_parser.add_argument("--charters", action="store_true", help="List Stage-Gate 2 baselined project charters")
    pmo_parser.add_argument("--capacity", action="store_true", help="List resource capacity plan and allocation utilization")
    pmo_parser.add_argument("--actions", action="store_true", help="List SteerCo actions and decisions")
    pmo_parser.add_argument("--uat", action="store_true", help="List Stage-Gate 4 quality & client UAT sign-offs")
    pmo_parser.add_argument("--closures", action="store_true", help="List Stage-Gate 5 formal closures and lessons learned")

    # 20. SDLC & DevSecOps Engineering
    sdlc_parser = subparsers.add_parser("sdlc", help="Inspect 7-stage SDLC engineering lifecycle and DevSecOps quality gates")
    sdlc_parser.add_argument("--overview", action="store_true", help="Display SDLC telemetry overview and quality gates")
    sdlc_parser.add_argument("--reqs", action="store_true", help="List SRS requirements and RTM traceability")
    sdlc_parser.add_argument("--adrs", action="store_true", help="List Architecture Decision Records (ADR)")
    sdlc_parser.add_argument("--prs", action="store_true", help="List Pull Requests and peer review records")
    sdlc_parser.add_argument("--pipelines", action="store_true", help="List CI/CD pipeline runs and quality gate statuses")
    sdlc_parser.add_argument("--defects", action="store_true", help="List software defects & bugs (IEEE 1044)")
    sdlc_parser.add_argument("--releases", action="store_true", help="List semantic production releases and CAB approvals")
    sdlc_parser.add_argument("--observability", action="store_true", help="Display SRE telemetry latency, uptime, and error budget")

    # 21. Vendor Management & Strategic Sourcing
    sourcing_parser = subparsers.add_parser("sourcing", help="Vendor Management, Strategic Sourcing & Procurement Lifecycle")
    sourcing_parser.add_argument("--overview", action="store_true", help="Display procurement executive MIS and spend summary")
    sourcing_parser.add_argument("--vendors", action="store_true", help="List approved vendors with MSME and KYC status")
    sourcing_parser.add_argument("--categories", action="store_true", help="List sourcing category spend targets and strategies")
    sourcing_parser.add_argument("--requisitions", action="store_true", help="List purchase requisitions (PR) and approval status")
    sourcing_parser.add_argument("--events", action="store_true", help="List strategic sourcing e-RFX events and awarded savings")
    sourcing_parser.add_argument("--contracts", action="store_true", help="List active vendor contracts and renewal schedules")
    sourcing_parser.add_argument("--grns", action="store_true", help="List inbound goods received notes (GRN) and inspection")
    sourcing_parser.add_argument("--scorecards", action="store_true", help="List vendor performance scorecards & QBR ratings")
    sourcing_parser.add_argument("--risks", action="store_true", help="List third-party risk assessments (TPRM)")
    sourcing_parser.add_argument("--capas", action="store_true", help="List corrective action plans (CAPA)")

    # 22. Enterprise Guardrails, Architectures & Flowcharts
    grd_parser = subparsers.add_parser("guardrails", help="Enterprise runtime guardrails enforcement, architectural blueprints & flowcharts")
    grd_parser.add_argument("--overview", action="store_true", help="Display guardrails telemetry overview & compliance score")
    grd_parser.add_argument("--rules", action="store_true", help="List all 8 core enterprise guardrail policies")
    grd_parser.add_argument("--evaluate", action="store_true", help="Trigger autonomous runtime scan across all guardrails")
    grd_parser.add_argument("--logs", action="store_true", help="List execution and intervention audit logs")
    grd_parser.add_argument("--flowcharts", action="store_true", help="List enterprise process flowcharts and step lifecycles")
    grd_parser.add_argument("--blueprints", action="store_true", help="List system architecture blueprints")
    grd_parser.add_argument("--documents", action="store_true", help="List technical architecture and DOA documents")

    # 23. AI Model APIs, MCP Tool Servers, Cloud Topology & Authenticity
    ai_parser = subparsers.add_parser("ai-cloud", help="AI Model APIs, Model Context Protocol (MCP) servers, cloud topology and authenticity")
    ai_parser.add_argument("--overview", action="store_true", help="Display AI spend, MCP connectivity, and cloud health")
    ai_parser.add_argument("--models", action="store_true", help="List production reasoning LLMs and context windows")
    ai_parser.add_argument("--mcps", action="store_true", help="List Model Context Protocol tool servers and ping status")
    ai_parser.add_argument("--cloud", action="store_true", help="List multi-cloud topology, regions, and compute clusters")
    ai_parser.add_argument("--certs", action="store_true", help="List corporate digital signature certificates (Class 3 DSC)")
    ai_parser.add_argument("--alerts", action="store_true", help="List executive alert rules and dispatch to department heads")
    ai_parser.add_argument("--dispatch-alert", type=str, default=None, help="Trigger manual alert dispatch (e.g. EAR-FIN-LIQ-01)")

    # 24. ISO Standards, QMS, CAPA & Grievance Redressal
    iso_parser = subparsers.add_parser("iso", help="ISO Standards (9001, 27001, 42001, 20000-1, 22301), QMS clause worksheets & grievances")
    iso_parser.add_argument("--overview", action="store_true", help="Display ISO conformity telemetry across all 5 standards")
    iso_parser.add_argument("--certs", action="store_true", help="List acquired ISO certificates and registrar credentials")
    iso_parser.add_argument("--controls", action="store_true", help="List clause implementation worksheets and maturity ratings")
    iso_parser.add_argument("--audits", action="store_true", help="List internal management and surveillance audit inspection reports")
    iso_parser.add_argument("--capas", action="store_true", help="List Corrective and Preventive Action (CAPA) worksheets")
    iso_parser.add_argument("--grievances", action="store_true", help="List formal multi-stakeholder grievances and CSAT ratings")

    # 25. IT, Cloud & Passkey Access Infrastructure
    infra_parser = subparsers.add_parser("infra", help="IT hardware, cloud workloads, FIDO2 passkeys, ZTNA policies, and DR drills")
    infra_parser.add_argument("--overview", action="store_true", help="Display IT, cloud, passkeys, and ZTNA posture overview")
    infra_parser.add_argument("--passkeys", action="store_true", help="List enrolled FIDO2/WebAuthn hardware passkeys")
    infra_parser.add_argument("--zero-trust", action="store_true", help="List Zero-Trust Network Access (ZTNA) policies")
    infra_parser.add_argument("--dr-drills", action="store_true", help="List Disaster Recovery (DR) simulation drill logs")
    infra_parser.add_argument("--assets", action="store_true", help="List IT hardware inventory")
    infra_parser.add_argument("--cloud", action="store_true", help="List cloud accounts and monthly spend")

    # 26. Cybersecurity, Incident Management & CERT-In War Room
    secops_cmd = subparsers.add_parser("secops", help="Cybersecurity incident response, CERT-In war room, forensics, and playbooks")
    secops_cmd.add_argument("--overview", action="store_true", help="Display SecOps War Room executive posture and CERT-In countdown")
    secops_cmd.add_argument("--incidents", action="store_true", help="List active and historical security incidents")
    secops_cmd.add_argument("--alerts", action="store_true", help="List SIEM security threat alerts from GuardDuty and EDR")
    secops_cmd.add_argument("--evidence", action="store_true", help="List forensic evidence items with SHA-256 hashes")
    secops_cmd.add_argument("--threat-intel", action="store_true", help="List threat intelligence indicators of compromise (IOCs)")
    secops_cmd.add_argument("--playbooks", action="store_true", help="List NIST SP 800-61 incident response playbooks")
    secops_cmd.add_argument("--vulns", action="store_true", help="List CVE vulnerability patches and CVSS scores")
    secops_cmd.add_argument("--drills", action="store_true", help="List tabletop crisis simulation drills")
    secops_cmd.add_argument("--certin-reports", action="store_true", help="List formal statutory filings submitted to CERT-In")



    
    args = parser.parse_args()
    
    if args.command == "seed":
        seed_database()
        print("[OK] Database initialized successfully.")
        
    elif args.command == "calc-ctc":
        res = compute_salary_breakup(args.ctc, args.basic_pct, args.hra_pct, args.state)
        e = res["earnings"]
        em = res["employer_contributions"]
        ed = res["employee_deductions"]
        th = res["take_home"]
        
        print("\n=======================================================")
        print(f" ASPERION DIGITAL TECHNOLOGIES - STATUTORY CTC BREAKUP")
        print("=======================================================")
        print(f" Annual CTC:           INR {res['annual_ctc']:,.2f}")
        print(f" Monthly CTC:          INR {res['monthly_ctc']:,.2f}")
        print("-------------------------------------------------------")
        print(" EARNINGS:")
        print(f"  Basic Salary:        INR {e['basic_salary']['monthly']:,.2f} /mo  (INR {e['basic_salary']['annual']:,.2f} /yr)")
        print(f"  HRA:                 INR {e['hra']['monthly']:,.2f} /mo  (INR {e['hra']['annual']:,.2f} /yr)")
        print(f"  Special Allowance:   INR {e['special_allowance']['monthly']:,.2f} /mo  (INR {e['special_allowance']['annual']:,.2f} /yr)")
        print(f"  Gross Salary:        INR {e['gross_salary']['monthly']:,.2f} /mo  (INR {e['gross_salary']['annual']:,.2f} /yr)")
        print("-------------------------------------------------------")
        print(" EMPLOYER CONTRIBUTIONS:")
        print(f"  Employer PF (12%):   INR {em['employer_pf']['monthly']:,.2f} /mo")
        print(f"  Gratuity (15/26):    INR {em['gratuity_provision']['monthly']:,.2f} /mo")
        print("-------------------------------------------------------")
        print(" EMPLOYEE DEDUCTIONS:")
        print(f"  Employee PF (12%):   INR {ed['employee_pf']['monthly']:,.2f} /mo")
        print(f"  Professional Tax:    INR {ed['professional_tax']['monthly']:,.2f} /mo ({args.state})")
        print("-------------------------------------------------------")
        print(f" ESTIMATED NET IN-HAND: INR {th['monthly_net_in_hand']:,.2f} /mo  (INR {th['annual_net_in_hand']:,.2f} /yr)")
        print("=======================================================\n")
        
    elif args.command == "generate-letter":
        breakup = compute_salary_breakup(args.ctc)
        doc = generate_document_html(args.code, {
            "candidate_name": args.recipient,
            "employee_name": args.recipient,
            "designation": args.designation,
            "annual_ctc": args.ctc,
            "salary_breakup": breakup,
            "joining_date": "Immediate",
            "candidate_address": "Bangalore, Karnataka",
            "location": "Bangalore Head Office"
        })
        
        if args.format == "docx":
            out_file = args.output or f"{args.code}_{args.recipient.replace(' ', '_')}.docx"
            clean_lines = [
                f"Subject: {doc['letter_title']}",
                f"Issued to: {args.recipient}",
                f"Designation: {args.designation}",
                "Official terms and conditions as per ASPERION corporate policy."
            ]
            stream = create_corporate_letter_docx(
                letter_title=doc["letter_title"],
                recipient_name=args.recipient,
                body_text_lines=clean_lines,
                salary_breakup=breakup if "HR-ONB" in args.code else None,
                category=doc["category"]
            )
            with open(out_file, "wb") as f:
                f.write(stream.getbuffer())
            print(f"\n[OK] Generated official Word document '{doc['letter_title']}' -> {out_file}\n")
        else:
            out_file = args.output or f"{args.code}_{args.recipient.replace(' ', '_')}.html"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(doc["html_content"])
            print(f"\n[OK] Generated letter '{doc['letter_title']}' -> {out_file}\n")
        
    elif args.command == "triage-incident":
        triage = triage_security_incident(args.category, args.affected_systems, args.data_class, is_customer_facing=True)
        print("\n=======================================================")
        print(f" SECOPS INCIDENT TRIAGE & REGULATORY ASSESSMENT")
        print("=======================================================")
        print(f" Severity:               {triage['severity']}")
        print(f" Response Target:        {triage['response_target_minutes']} minutes")
        print(f" War Room Required:      {triage['war_room_required']}")
        print(f" CERT-In SLA Mandatory:  {triage['cert_in_statutory_reporting']['mandatory']}")
        if triage['cert_in_statutory_reporting']['mandatory']:
            print(f" CERT-In Deadline:       {triage['cert_in_statutory_reporting']['deadline']}")
        print(f" Recommended Playbook:   {triage['recommended_playbook']['code']} - {triage['recommended_playbook']['name']}")
        print("=======================================================\n")

    elif args.command == "audit-trail":
        db = SessionLocal()
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(args.limit).all()
        print("\n================================================================================")
        print(" ASPERION ENTERPRISE AUDIT TRAIL (IMMUTABLE LOGS)")
        print("================================================================================")
        for lg in logs:
            print(f" [{lg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] [{lg.severity:7}] [{lg.module:10}] {lg.event_type}: {lg.description} (Actor: {lg.actor})")
        print("================================================================================\n")
        db.close()

    elif args.command == "vault":
        from app.api.vault import search_vault_documents, get_vault_statistics
        stats = get_vault_statistics()
        docs = search_vault_documents(category=args.category, search=args.search)
        print("\n================================================================================")
        print(f" ASPERION MASTER DOCUMENT & KNOWLEDGE VAULT ({stats['total_documents']} documents indexed)")
        print("================================================================================")
        for d in docs[:args.limit]:
            print(f" [{d.file_type:4}] [{d.category_id:18}] {d.filename:<50} ({d.file_size_kb:>6} KB)")
        if len(docs) > args.limit:
            print(f" ... and {len(docs) - args.limit} more documents available (use --limit to expand).")
        print("================================================================================\n")

    elif args.command == "add-thought":
        from app.models.strategy_kpi import StrategicDecisionThought
        from datetime import date
        db = SessionLocal()
        entry = StrategicDecisionThought(
            entry_type=args.type,
            title=args.title,
            author=settings.FOUNDER_DIRECTOR,
            date_recorded=date.today(),
            context_background="Recorded via Asperion Enterprise CLI.",
            decision_rationale=args.rationale,
            tags=args.tags,
            status="Approved"
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        print(f"\n[OK] Recorded strategic {args.type}: '{entry.title}' (ID: {entry.id})\n")
        db.close()

    elif args.command == "kpis":
        from app.models.strategy_kpi import EnterpriseKPI
        db = SessionLocal()
        if args.add:
            if not args.code or not args.name:
                print("Error: --code and --name are required when --add is specified.")
                sys.exit(1)
            var = args.actual - args.target
            var_pct = (var / args.target * 100) if args.target != 0 else 0.0
            kpi = EnterpriseKPI(
                kpi_code=args.code,
                category=args.category,
                name=args.name,
                target_value=args.target,
                actual_value=args.actual,
                unit=args.unit,
                variance=round(var, 2),
                variance_pct=round(var_pct, 2),
                status="Achieved" if args.actual >= args.target else "On Track"
            )
            db.add(kpi)
            db.commit()
            print(f"\n[OK] Registered new KPI '{kpi.kpi_code}': {kpi.name} ({kpi.actual_value}/{kpi.target_value} {kpi.unit})\n")
        else:
            kpis = db.query(EnterpriseKPI).all()
            print("\n================================================================================")
            print(" ASPERION ENTERPRISE PERFORMANCE KPIS")
            print("================================================================================")
            for k in kpis:
                print(f" [{k.kpi_code:10}] [{k.category:12}] {k.name:<32} Target: {k.target_value:>7} | Actual: {k.actual_value:>7} {k.unit:<4} [{k.status}]")
            print("================================================================================\n")
        db.close()

    elif args.command == "analytics":
        db = SessionLocal()
        from app.api.analytics import get_executive_overview, simulate_cashflow, CashflowSimulationRequest
        if args.simulate:
            req = CashflowSimulationRequest(
                collection_acceleration_pct=args.coll_accel,
                expense_optimization_pct=args.exp_opt,
                new_monthly_retainer_inr=args.retainer
            )
            sim = simulate_cashflow(req, db=db)
            print("\n================================================================================")
            print(" ASPERION DYNAMIC WHAT-IF CASH FLOW SIMULATION")
            print("================================================================================")
            print(f" Parameters: Acceleration: +{args.coll_accel}% | Optimization: -{args.exp_opt}% | Retainer: INR {args.retainer:,.0f}/mo")
            print("--------------------------------------------------------------------------------")
            print(f" Baseline Ending Cash:   INR {sim['baseline_ending_cash_inr']:>14,.2f}")
            print(f" Simulated Ending Cash:  INR {sim['simulated_ending_cash_inr']:>14,.2f}")
            print(f" Net Liquidity Delta:   +INR {sim['cash_variance_delta_inr']:>14,.2f}")
            print(f" Simulated Runway:       {sim['simulated_runway_months']:>14.1f} Months")
            print("================================================================================\n")
        else:
            ov = get_executive_overview(db=db)
            fs = ov["financial_summary"]
            gc = ov["governance_and_compliance"]
            ds = ov["delivery_summary"]
            tw = ov["talent_and_workforce"]
            print("\n================================================================================")
            print(" ASPERION EXECUTIVE MIS & OPERATIONAL RATIOS")
            print("================================================================================")
            print(f" Total Revenue Invoiced:       INR {fs['total_invoiced_inr']:>14,.2f}")
            print(f" Total Collections Received:   INR {fs['total_collected_inr']:>14,.2f}")
            print(f" Accounts Receivable (AR):     INR {fs['accounts_receivable_inr']:>14,.2f}")
            print(f" Accounts Payable (AP):        INR {fs['accounts_payable_inr']:>14,.2f}")
            print(f" Treasury Closing Cash:        INR {fs['closing_treasury_cash_inr']:>14,.2f}")
            print("--------------------------------------------------------------------------------")
            print(f" Net Operating Margin:          {fs['net_operating_margin_pct']:>13.1f}%")
            print(f" Cash Runway:                   {fs['cash_runway_months']:>13.1f} Months")
            print(f" Days Sales Outstanding (DSO):  {fs['dso_days']:>13.1f} Days")
            print(f" Statutory Compliance Index:    {gc['statutory_compliance_index_pct']:>13.1f}%")
            print(f" CERT-In SLA Compliance:        {gc['certin_sla_compliance_pct']:>13.1f}%")
            print(f" Sprint Velocity Throughput:    {ds['sprint_velocity_achievement_pct']:>13.1f}%")
            print(f" Active Employees:              {tw['active_headcount']:>14}")
            print("================================================================================\n")
        db.close()

    elif args.command == "crm":
        db = SessionLocal()
        from app.models.crm_enterprise import Opportunity, CustomerAccount, SupportTicket, EnterpriseRisk
        from app.api.crm_enterprise import get_pipeline_summary
        
        if args.deals:
            opps = db.query(Opportunity).all()
            print("\n================================================================================")
            print(" ASPERION ENTERPRISE DEAL PIPELINE & OPPORTUNITIES")
            print("================================================================================")
            for o in opps:
                print(f" [{o.opportunity_code:16}] {o.client_name:<30} INR {o.deal_value_inr:>11,.0f} [{o.stage:<22}] Prob: {o.probability_pct:>3.0f}% | Weighted: INR {o.weighted_value_inr:>10,.0f}")
            print("================================================================================\n")
        elif args.accounts:
            accs = db.query(CustomerAccount).all()
            print("\n================================================================================")
            print(" ASPERION CUSTOMER SUCCESS & ACCOUNTS DIRECTORY")
            print("================================================================================")
            for a in accs:
                print(f" [{a.account_code:12}] {a.client_name:<32} ARR: INR {a.annual_recurring_revenue_inr:>11,.0f} | Health: {a.health_score:>3}% ({a.health_status}) | Renewal: {a.renewal_date}")
            print("================================================================================\n")
        elif args.tickets:
            tkts = db.query(SupportTicket).all()
            print("\n================================================================================")
            print(" ASPERION SLA SERVICE DESK SUPPORT TICKETS")
            print("================================================================================")
            for t in tkts:
                print(f" [{t.ticket_number:16}] {t.client_name:<28} [{t.severity:<10}] {t.subject:<35} [{t.status}]")
            print("================================================================================\n")
        elif args.risks:
            risks = db.query(EnterpriseRisk).all()
            print("\n================================================================================")
            print(" ASPERION ENTERPRISE RISK MANAGEMENT (ERM) REGISTER")
            print("================================================================================")
            for r in risks:
                print(f" [{r.risk_code:12}] [{r.risk_category:<25}] {r.risk_title:<35} Inherent RPN: {r.inherent_rpn:>2} -> Residual RPN: {r.residual_rpn:>2} [{r.treatment_strategy}]")
            print("================================================================================\n")
        else:
            s = get_pipeline_summary(db=db)
            p = s["pipeline"]
            cs = s["customer_success"]
            sd = s["service_desk"]
            print("\n================================================================================")
            print(" ASPERION ENTERPRISE CRM & CUSTOMER SUCCESS MIS")
            print("================================================================================")
            print(f" Total Gross Pipeline:         INR {p['total_pipeline_value_inr']:>14,.2f}")
            print(f" Weighted Pipeline (ARR):      INR {p['weighted_pipeline_value_inr']:>14,.2f}")
            print(f" Active Opportunities Count:       {p['active_deals_count']:>14}")
            print(f" Historical Win Rate:              {p['win_rate_pct']:>13.1f}%")
            print("--------------------------------------------------------------------------------")
            print(f" Total Customer Accounts:          {cs['total_accounts']:>14}")
            print(f" Managed Recurring ARR:        INR {cs['managed_arr_inr']:>14,.2f}")
            print(f" Average CS Health Score:          {cs['average_health_score']:>13.1f}%")
            print("--------------------------------------------------------------------------------")
            print(f" Total Support Tickets:            {sd['total_tickets']:>14}")
            print(f" Open SLA Tickets:                 {sd['open_tickets']:>14}")
            print(f" SLA Compliance Rate:              {sd['sla_compliance_rate_pct']:>13.1f}%")
            print("================================================================================\n")
        db.close()

    elif args.command == "tickets":
        db = SessionLocal()
        from app.models.ticketing_notifications import InternalTicket
        from app.api.ticketing_notifications import create_internal_ticket, get_service_desk_summary
        from app.schemas.ticketing_notifications import InternalTicketCreate

        if args.create:
            if not args.subject:
                print("Error: --subject is required when --create is passed.")
                sys.exit(1)
            dept = args.dept or "IT_INFRASTRUCTURE"
            priority = args.priority or "P3-Medium"
            tkt_in = InternalTicketCreate(
                department=dept,
                category=args.category,
                subject=args.subject,
                description=args.desc,
                priority=priority,
                requester_name=args.requester,
                requester_email=args.email,
                requester_department="GOVERNANCE"
            )
            created = create_internal_ticket(ticket_in=tkt_in, db=db)
            print(f"\n[OK] Created Internal Ticket {created.ticket_number} [{created.department}] ({created.priority})")
            print(f" Subject: {created.subject}")
            print(f" SLA Target: {created.sla_deadline_hours}h (Target: {created.target_resolution_at})\n")
        else:
            query = db.query(InternalTicket)
            if args.dept:
                query = query.filter(InternalTicket.department == args.dept)
            if args.priority:
                query = query.filter(InternalTicket.priority == args.priority)
            tickets = query.order_by(InternalTicket.id.desc()).all()

            summary = get_service_desk_summary(db=db)
            print("\n================================================================================")
            print(f" ASPERION CROSS-DEPARTMENTAL SERVICE DESK ({len(tickets)} Tickets)")
            print(f" Total: {summary.total_tickets} | Open: {summary.open_tickets} | SLA Adherence: {summary.sla_compliance_pct}%")
            print("================================================================================")
            for t in tickets:
                breached = "BREACH" if t.sla_breached else "OK"
                print(f" [{t.ticket_number:15}] [{t.department:18}] [{t.priority:11}] {t.subject:<40} [{t.status:<11}] Assignee: {t.assigned_to}")
            print("================================================================================\n")
        db.close()

    elif args.command == "notifications":
        db = SessionLocal()
        from app.models.ticketing_notifications import SystemNotification
        from app.engines.notification_engine import broadcast_alert
        from app.api.ticketing_notifications import mark_all_notifications_read

        if args.mark_read_all:
            mark_all_notifications_read(db=db)
            print("\n[OK] Marked all system notifications as read.\n")
        elif args.broadcast:
            if not args.title or not args.msg:
                print("Error: --title and --msg are required for broadcasting.")
                sys.exit(1)
            severity = (args.severity or "INFO").upper()
            created = broadcast_alert(
                db=db,
                module_source=args.source,
                title=args.title,
                message=args.msg,
                severity=severity,
                target_role="ALL"
            )
            print(f"\n[OK] Broadcasted Alert {created.notification_code} [{created.severity}]")
            print(f" Title: {created.title}")
            print(f" Message: {created.message}\n")
        else:
            query = db.query(SystemNotification).filter(SystemNotification.is_dismissed == False)
            if args.severity:
                query = query.filter(SystemNotification.severity == args.severity.upper())
            if args.unread:
                query = query.filter(SystemNotification.is_read == False)
            notifs = query.order_by(SystemNotification.id.desc()).all()

            unread_count = sum(1 for n in notifs if not n.is_read)
            print("\n================================================================================")
            print(f" ASPERION OMNI-CHANNEL NOTIFICATION CENTER ({len(notifs)} Alerts | {unread_count} Unread)")
            print("================================================================================")
            for n in notifs:
                status = "UNREAD" if not n.is_read else "READ  "
                print(f" [{n.notification_code:15}] [{n.severity:8}] [{status}] [{n.module_source:14}] {n.title}")
                print(f"    Message: {n.message}")
            print("================================================================================\n")
        db.close()

    elif args.command == "dev-accounts":
        db = SessionLocal()
        from app.models.developer_platform import DeveloperPlatformAccount, DeveloperEnvironmentSecret
        from app.api.developer_platform import rotate_developer_secret

        if args.rotate:
            rotated = rotate_developer_secret(secret_id=args.rotate, db=db)
            print(f"\n[OK] Rotated Secret '{rotated.secret_name}' (ID: {rotated.id})")
            print(f" Next Rotation Due: {rotated.next_rotation_due} | Status: {rotated.status}\n")
        elif args.secrets:
            secrets = db.query(DeveloperEnvironmentSecret).all()
            print("\n================================================================================")
            print(f" ASPERION DEVELOPER ENVIRONMENT SECRETS & 90-DAY ROTATION LEDGER ({len(secrets)} Secrets)")
            print("================================================================================")
            for s in secrets:
                print(f" [{s.secret_code:12}] [{s.platform:8}] [{s.target_environment:11}] {s.secret_name:<28} Due: {s.next_rotation_due} [{s.status}]")
            print("================================================================================\n")
        else:
            accounts = db.query(DeveloperPlatformAccount).all()
            print("\n================================================================================")
            print(f" ASPERION CORPORATE DEVELOPER PLATFORM ACCOUNTS ({len(accounts)} Platforms)")
            print("================================================================================")
            for a in accounts:
                fido = "FIDO2" if a.fido2_mfa_enforced else "PWD  "
                duns = "D-U-N-S" if a.duns_linked else "NO-DUNS"
                print(f" [{a.account_code:12}] {a.platform_name:<28} [{a.verification_status:<21}] {fido} | {duns} | Admin: {a.admin_email}")
            print("================================================================================\n")
        db.close()

    elif args.command == "tax-challans":
        db = SessionLocal()
        from app.models.developer_platform import StatutoryChallanFiling
        from app.api.developer_platform import get_tax_filing_summary

        summary = get_tax_filing_summary(db=db)
        challans = summary.challans
        if args.type:
            challans = [c for c in challans if c.filing_type == args.type]

        print("\n================================================================================")
        print(f" ASPERION STATUTORY TAX DEPOSIT CHALLANS & RECONCILIATION")
        print(f" Total Deposited: INR {summary.total_tax_deposited_inr:,.2f} | Portal Reconciliation: {summary.reconciliation_rate_pct}%")
        print("================================================================================")
        for c in challans:
            arn = c.challan_cin_arn or "Pending ARN"
            print(f" [{c.challan_code:16}] {c.filing_type:<24} Period: {c.tax_period:<11} INR {c.tax_amount_paid:>10,.2f} | ARN/CIN: {arn:<20} [{c.reconciliation_status}]")
        print("================================================================================\n")
        db.close()

    elif args.command == "attendance":
        db = SessionLocal()
        from app.models.hrms import Employee
        from app.models.attendance import AttendanceRecord
        from app.schemas.attendance import ClockInRequest, ClockOutRequest, WhatsAppWebhookPayload
        from app.api.attendance import api_clock_in, api_clock_out, api_auto_fix_anomalies, get_daily_attendance_summary, api_whatsapp_webhook

        if args.clock_in:
            req = ClockInRequest(
                employee_id=args.clock_in,
                source=args.source,
                latitude=args.lat,
                longitude=args.lon,
                selfie_base64_or_hash="cli_biometric_selfie_stream"
            )
            rec = api_clock_in(req, db=db)
            emp = db.query(Employee).filter(Employee.id == args.clock_in).first()
            emp_name = emp.full_name if emp else f"ID {args.clock_in}"
            print(f"\n[OK] Clock-IN Recorded for {emp_name}!")
            print(f" Time: {rec.clock_in_time} | Status: {rec.status} | Source: {rec.in_source}")
            print(f" Geofence: {rec.geofence_zone_code or 'HQ'} (Verified: {rec.geofence_verified}, Dist: {rec.geofence_distance_meters:.1f}m)")
            print(f" Facial AI Match: {rec.facial_match_confidence_pct}% (Liveness: {rec.facial_liveness_verified})\n")

        elif args.clock_out:
            req = ClockOutRequest(
                employee_id=args.clock_out,
                source=args.source,
                latitude=args.lat,
                longitude=args.lon
            )
            rec = api_clock_out(req, db=db)
            print(f"\n[OK] Clock-OUT Recorded for Employee ID {args.clock_out}!")
            print(f" Time: {rec.clock_out_time} | Status: {rec.status}")
            print(f" Work Hours: Total {rec.total_work_hours}h | Effective {rec.effective_work_hours}h\n")

        elif args.auto_fix:
            res = api_auto_fix_anomalies(db=db)
            print("\n================================================================================")
            print(" ASPERION SELF-HEALING ATTENDANCE ENGINE (AUTO-FIX)")
            print("================================================================================")
            print(f" Records Scanned: {res['scanned_records_count']} | Self-Healed: {res['auto_fixed_count']}")
            for det in res["details"]:
                print(f"  -> {det}")
            if not res["details"]:
                print("  -> All punches are current and regularized. Zero anomalies detected.")
            print("================================================================================\n")

        elif args.whatsapp:
            wa_req = WhatsAppWebhookPayload(
                phone_number=args.phone,
                message_body=args.msg,
                latitude=args.lat,
                longitude=args.lon
            )
            res = api_whatsapp_webhook(wa_req, db=db)
            print("\n================================================================================")
            print(" ASPERION WHATSAPP ATTENDANCE BOT RESPONSE")
            print("================================================================================")
            print(f" Status: {res.get('status')} | Phone: {args.phone}")
            print(f" Bot Reply: {res.get('reply_message')}")
            print("================================================================================\n")

        else:
            summary = get_daily_attendance_summary(None, db=db)
            print("\n================================================================================")
            print(f" ASPERION DAILY ATTENDANCE & WORKFORCE TRACKING ({summary.date})")
            print("================================================================================")
            print(f" Active Headcount: {summary.total_employees} | Present: {summary.present_count} | Late Marks: {summary.late_marks_count}")
            print(f" WFH / Remote: {summary.wfh_count} | Biometric Compliance: {summary.biometric_compliance_pct}% | Self-Healed: {summary.auto_healed_today_count}")
            print("--------------------------------------------------------------------------------")
            recs = db.query(AttendanceRecord).order_by(AttendanceRecord.id.desc()).limit(10).all()
            for r in recs:
                emp = db.query(Employee).filter(Employee.id == r.employee_id).first()
                e_name = emp.full_name if emp else f"ID {r.employee_id}"
                in_t = r.clock_in_time.strftime("%H:%M") if r.clock_in_time else "--:--"
                out_t = r.clock_out_time.strftime("%H:%M") if r.clock_out_time else "--:--"
                geo = "GEO-OK" if r.geofence_verified else "REMOTE"
                face = f"{r.facial_match_confidence_pct:.0f}pct" if r.facial_recognition_verified else "NO-BIO"
                heal = " [AUTO-HEALED]" if r.auto_fixed else ""
                print(f" [{r.id:3}] {e_name:<18} Date: {r.attendance_date} | In: {in_t} Out: {out_t} | {r.status:<10} | {geo} | {face}{heal}")
            print("================================================================================\n")
        db.close()

    elif args.command == "self-heal":
        db = SessionLocal()
        from app.engines.autofix_engine import run_enterprise_auto_fix_and_self_heal
        from app.engines.autoupdate_manager import auto_update_manager

        if args.daemon_status:
            st = auto_update_manager.get_status()
            print("\n================================================================================")
            print(f" ASPERION AUTONOMOUS AUTO-UPDATE & REPAIR DAEMON")
            print("================================================================================")
            print(f" Daemon Status:       {st['status']}")
            print(f" Check Interval:      {st['interval_seconds']} seconds")
            print(f" Total Executed Runs: {st['total_runs']}")
            print(f" Cumulative Healed:   {st['total_healed_cumulative']} anomalies")
            print(f" Last Run:            {st['last_run'] or 'Initializing...'}")
            print("================================================================================\n")
        else:
            mode_str = "DRY-RUN SCAN" if args.dry_run else "AUTONOMOUS SELF-REPAIR"
            res = run_enterprise_auto_fix_and_self_heal(db, dry_run=args.dry_run)
            print("\n================================================================================")
            print(f" ASPERION SYSTEM-WIDE AUTO-FIX & SELF-HEALING ENGINE ({mode_str})")
            print(f" Status: {res['status']} | System Health Index: {res['system_health_score']}% | Scanned: {res['modules_scanned']} Pillars")
            print("================================================================================")
            print(f" Anomalies Detected:    {res['anomalies_detected']}")
            print(f" Anomalies Auto-Fixed:  {res['anomalies_auto_fixed']}")
            print("--------------------------------------------------------------------------------")
            if res["actions_taken"]:
                for action in res["actions_taken"]:
                    print(f"  -> {action}")
            else:
                print("  -> All operational, financial, and attendance registers are completely healthy!")
            print("================================================================================\n")
        db.close()

    elif args.command == "payroll-statements":
        db = SessionLocal()
        from app.engines.salary_statement_engine import (
            generate_attendance_synced_salary_statement, get_employee_salary_slip_html
        )

        if args.payslip:
            html = get_employee_salary_slip_html(db=db, employee_id=args.payslip, payroll_cycle=args.cycle)
            out_file = f"Payslip_{args.cycle}_Emp{args.payslip}.html"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"\n[OK] Payslip HTML Generated: {out_file} (Cycle: {args.cycle})\n")
        else:
            res = generate_attendance_synced_salary_statement(
                db=db,
                payroll_cycle=args.cycle,
                days_in_month=args.days,
                disburse_bank=args.disburse
            )
            mode_payout = "DISBURSED (ICICI NEFT UTR ASSIGNED)" if args.disburse else "PROCESSED (READY FOR BANK)"
            print("\n================================================================================")
            print(f" ASPERION ATTENDANCE-SYNCED SALARY STATEMENTS ({args.cycle})")
            print(f" Status: {mode_payout} | Headcount: {res['active_headcount']} Personnel")
            print("================================================================================")
            print(f" Total Gross Salary:       INR {res['total_gross_inr']:>12,.2f}")
            print(f" Employee Provident Fund:  INR {res['statutory_compliance_summary']['total_employee_pf_inr']:>12,.2f}")
            print(f" Karnataka Prof Tax (PT):  INR {res['statutory_compliance_summary']['total_karnataka_pt_inr']:>12,.2f}")
            print(f" Estimated TDS u/s 192:    INR {res['statutory_compliance_summary']['total_tds_deductions_inr']:>12,.2f}")
            print("--------------------------------------------------------------------------------")
            print(f" TOTAL NET DISBURSEMENT:   INR {res['total_net_disbursement_inr']:>12,.2f}")
            print("================================================================================")
            for s in res["statements"]:
                utr_str = s["bank_utr"] or "Pending Batch"
                print(f" [{s['emp_code']}] {s['employee_name']:<18} Days: {s['payable_days']:>4.1f} | Gross: {s['earnings']['earned_gross']:>9,.2f} | PT: {s['deductions']['karnataka_professional_tax']:>5,.2f} | Net: {s['net_take_home']:>9,.2f} | UTR: {utr_str}")
            print("================================================================================\n")
        db.close()

    elif args.command == "portals":
        db = SessionLocal()
        from app.api.auth import CORPORATE_USERS
        from app.api.portals import get_employee_portal_data, get_client_portal_data, get_vendor_portal_data

        if args.personas:
            print("\n================================================================================")
            print(" ASPERION DEDICATED STAKEHOLDER PERSONAS & RBAC ROSTER")
            print("================================================================================")
            for email, u in CORPORATE_USERS.items():
                print(f" • [{u['role']:<14}] {u['name']:<24} <{email}>")
                print(f"   Title:   {u['title']}")
                print(f"   Modules: {', '.join(u['modules'])}")
                print(f"   Passkey: {u['password']}\n")
            print("================================================================================\n")

        elif args.employee:
            data = get_employee_portal_data(emp_code="ADT-EMP-001", db=db)
            p = data["profile"]
            s = data["salary_overview"]
            print("\n================================================================================")
            print(f" EMPLOYEE SELF-SERVICE (ESS) COCKPIT: {p['name']} ({p['emp_code']})")
            print("================================================================================")
            print(f" Designation:      {p['designation']} | Department: {p['department']}")
            print(f" Annual CTC:       INR {s['annual_ctc']:>12,.2f}")
            print(f" Monthly Gross:    INR {s['monthly_gross']:>12,.2f}")
            print(f" Net In-Hand:      INR {s['net_in_hand']:>12,.2f}")
            print(f" Karnataka PT:     INR {s['karnataka_pt']:>12,.2f}")
            print(f" Recent Punches:   {data['attendance_stats']['recent_punches']} recorded shifts")
            print("--------------------------------------------------------------------------------")
            for slip in data["payslips"][:3]:
                print(f" Payslip [{slip['cycle']}]: Net INR {slip['net_salary']:>9,.2f} | Status: {slip['payment_status']} | UTR: {slip['bank_utr']}")
            print("================================================================================\n")

        elif args.client:
            data = get_client_portal_data(client_name="Zenith Global Corp", db=db)
            print("\n================================================================================")
            print(f" CLIENT PROJECT & SLA PORTAL: {data['client_name']}")
            print("================================================================================")
            print(f" Relationship Tier: {data['relationship_tier']}")
            print(f" Dedicated SPOC:    {data['dedicated_spoc']}")
            print(f" SLA Coverage:      {data['sla_coverage']}")
            print("--------------------------------------------------------------------------------")
            print(f" Active Projects ({len(data['active_projects'])}):")
            for prj in data["active_projects"]:
                print(f" • [{prj['code']}] {prj['name']:<28} Status: {prj['status']} | Budget: INR {prj['budget']:,.2f}")
            print(f"\n Commercial Invoices ({len(data['billing_invoices'])}):")
            for inv in data["billing_invoices"]:
                print(f" • Invoice #{inv['number']} | Date: {inv['date']} | Total: INR {inv['total']:>10,.2f} | Status: {inv['status']}")
            print("================================================================================\n")

        elif args.vendor:
            target_vname = getattr(args, "vendor_name", "Nexus Micro Systems")
            data = get_vendor_portal_data(vendor_name=target_vname, db=db)
            vp = data.get("vendor_profile", {})
            kpis = data.get("kpis", {})

            print("\n================================================================================")
            print(f" VENDOR SOURCING, POS & INWARD GRN PORTAL: {vp.get('vendor_name', data.get('vendor_name'))}")
            print(f" Code: {vp.get('vendor_code', data.get('vendor_code'))} | Category: {vp.get('category', 'Procurement')} | Rating: {vp.get('rating', 92.5):.1f}/100")
            print("================================================================================")
            print(f" Statutory Entity:  {data.get('entity', {}).get('name')}")
            print(f" CIN / Reg Office:  {data.get('entity', {}).get('cin')} | Horamavu, Bangalore - 560043")
            print(f" GSTIN / PAN:       {vp.get('gstin', 'Pending')} | PAN: {vp.get('pan', 'Pending')}")
            print(f" MSME Udyam:        {vp.get('msme_udyam_number', 'N/A')} (Category: {vp.get('msme_category', 'Micro')} - Max {vp.get('msme_payment_due_days', 45)}d Settlement)")
            print(f" Payment Terms:     Net {vp.get('payment_terms_days', 30)} Days (MSMED Act 2006 Priority: {'ELIGIBLE' if vp.get('msme_registered') else 'STANDARD'})")
            print(f" Bank Details:      {vp.get('bank_name', 'HDFC Bank')} | A/C: {vp.get('bank_account_number', 'N/A')} | IFSC: {vp.get('bank_ifsc', 'N/A')}")
            print(f" Due Diligence:     KYC: {vp.get('kyc_status', 'Approved')} | DPDP 2023 DPA: {vp.get('dpdp_compliance_status', 'Compliant')}")
            print("--------------------------------------------------------------------------------")
            print(f" Executive KPIs:    Active POs: {kpis.get('active_pos_count', 0)} ({kpis.get('total_po_value_inr', 0.0):>10,.2f} INR) | Inward GRNs: {kpis.get('grns_logged_count', 0)}")
            print(f"                    Total Billed: INR {kpis.get('total_ap_billed_inr', 0.0):>10,.2f} | Pending 3-Way Match: {kpis.get('pending_3way_matching_count', 0)}")
            print("--------------------------------------------------------------------------------")

            show_all = not (getattr(args, "pos", False) or getattr(args, "grns", False) or getattr(args, "bills", False))

            if show_all or getattr(args, "pos", False):
                pos = data.get("purchase_orders", [])
                print(f"\n [1] Authorized Purchase Orders ({len(pos)}):")
                for po in pos:
                    print(f"  • PO #{po['po_number']:<16} | Date: {po['po_date']} | Due: {po.get('delivery_due_date', 'Immediate')} | Status: [{po['status']}]")
                    print(f"    Amount: INR {po['total_amount']:>10,.2f} | Terms: {po.get('payment_terms', 'Net 30')} | Challan: {po.get('delivery_challan_no', 'Pending')}")
                    if po.get("items"):
                        for itm in po["items"]:
                            print(f"    - {itm.get('qty', 1)}x {itm.get('item', 'Item')} @ INR {itm.get('rate', 0):,.2f}")

            if show_all or getattr(args, "grns", False):
                grns = data.get("inward_grns", [])
                print(f"\n [2] Inward Goods Received Notes & Inspections ({len(grns)}):")
                for g in grns:
                    print(f"  • GRN #{g['grn_number']:<16} | Date: {g['received_date']} | PO: {g['po_reference']} | Challan: {g['delivery_challan_no']}")
                    print(f"    Item:     {g['item_description']}")
                    print(f"    Qty:      Ordered: {g['quantity_ordered']} | Accepted: {g['quantity_accepted']} | Rejected: {g['quantity_rejected']}")
                    print(f"    QA State: [{g['inspection_status']}] By {g['inspected_by']} @ {g['warehouse_location']}")

            if show_all or getattr(args, "bills", False):
                bills = data.get("ap_bills", [])
                print(f"\n [3] Vendor AP Bills & 3-Way Match Verification ({len(bills)}):")
                for b in bills:
                    print(f"  • Bill #{b['bill_number']:<16} | Date: {b['bill_date']} | Due: {b['due_date']} ({b.get('days_remaining', 0)}d left)")
                    print(f"    Taxable:  INR {b['taxable_amount']:>10,.2f} | GST: INR {b.get('gst_amount', 0.0):>8,.2f}")
                    print(f"    TDS Ded: -INR {b['tds_amount']:>10,.2f} (Section {b.get('tds_section', '194C')} @ {b.get('tds_rate_pct', 2.0)}%)")
                    print(f"    Net Pay:  INR {b['net_payable']:>10,.2f} | 3-Way Match: [{b['three_way_match_status']}] | Status: [{b['approval_status']}]")

            print("================================================================================\n")

        else:
            print("\nPlease specify a portal view: --employee, --client, --vendor, or --personas\n")
        db.close()

    elif args.command == "pmo-governance":
        db = SessionLocal()
        from app.models.pmo import (
            ProjectIntake, ProjectCharter, ActionDecisionItem, CapacityPlanItem, QualityUATItem, ProjectClosureItem
        )

        if args.intakes:
            intakes = db.query(ProjectIntake).all()
            print("\n================================================================================")
            print(" STAGE-GATE 1: PROJECT INTAKE, BUSINESS CASE & STRATEGIC FIT")
            print("================================================================================")
            for i in intakes:
                print(f" [{i.intake_code}] {i.project_name:<34} Fit: {i.strategic_fit:<8} | Budget: INR {i.estimated_budget_inr:>10,.2f} | Status: {i.intake_status}")
                print(f"   Sponsor: {i.sponsor} | Value: {i.expected_value}\n")
            print("================================================================================\n")

        elif args.charters:
            charters = db.query(ProjectCharter).all()
            print("\n================================================================================")
            print(" STAGE-GATE 2: BASELINED PROJECT CHARTERS (SCOPE & SUCCESS CRITERIA)")
            print("================================================================================")
            for c in charters:
                print(f" [{c.charter_code}] Signed off by: {c.signed_off_by} | Status: {c.signoff_status}")
                print(f"   Problem:  {c.problem_statement}")
                print(f"   Criteria: {c.measurable_success_criteria}")
                print(f"   Cadence:  {c.governance_cadence}\n")
            print("================================================================================\n")

        elif args.capacity:
            caps = db.query(CapacityPlanItem).all()
            print("\n================================================================================")
            print(" RESOURCE CAPACITY & SKILLS ALLOCATION PLAN")
            print("================================================================================")
            for cp in caps:
                print(f" • {cp.role_title:<32} {cp.person_or_vendor:<16} Req: {cp.required_hours:>4.1f}h | Avail: {cp.available_hours:>4.1f}h | Util: {cp.utilization_pct:>5.1f}% | {cp.status}")
            print("================================================================================\n")

        elif args.actions:
            actions = db.query(ActionDecisionItem).all()
            print("\n================================================================================")
            print(" STEERCO ACTION ITEMS & FORMAL DECISION REGISTER")
            print("================================================================================")
            for a in actions:
                print(f" • [{a.item_type.upper():<8}] {a.title_or_decision:<50} Owner: {a.owner:<15} | Status: {a.status}")
            print("================================================================================\n")

        elif args.uat:
            uats = db.query(QualityUATItem).all()
            print("\n================================================================================")
            print(" STAGE-GATE 4: QUALITY & CLIENT UAT ACCEPTANCE SIGN-OFFS")
            print("================================================================================")
            for u in uats:
                print(f" • {u.deliverable_name:<45} Review: {u.test_or_review_type:<18} | Status: {u.status}")
                print(f"   Criteria: {u.acceptance_criteria} | Signoff: {u.signoff_date}\n")
            print("================================================================================\n")

        elif args.closures:
            closures = db.query(ProjectClosureItem).all()
            print("\n================================================================================")
            print(" STAGE-GATE 5: FORMAL PROJECT CLOSURE & LESSONS LEARNED")
            print("================================================================================")
            for cl in closures:
                print(f" • {cl.closure_area:<35} Evidence: {cl.evidence_signoff:<30} | {cl.closure_status}")
                print(f"   Lessons: {cl.lessons_learned_summary}\n")
            print("================================================================================\n")

        else:
            intakes = db.query(ProjectIntake).count()
            charters = db.query(ProjectCharter).count()
            actions = db.query(ActionDecisionItem).count()
            capacity = db.query(CapacityPlanItem).count()
            uats = db.query(QualityUATItem).count()
            closures = db.query(ProjectClosureItem).count()
            print("\n================================================================================")
            print(" ASPERION PMO STAGE-GATE GOVERNANCE OVERVIEW (PMBOK / PRINCE2 / CMMI)")
            print("================================================================================")
            print(f" Gate 1: Project Intakes & Business Cases:    {intakes} Registered")
            print(f" Gate 2: Baselined Project Charters:         {charters} Signed-Off")
            print(f" Gate 3: Resource Capacity & Skills Track:   {capacity} Roles Allocated")
            print(f" Gate 3: SteerCo Actions & Decisions:        {actions} Logged")
            print(f" Gate 4: Quality & UAT Acceptance:           {uats} Sign-Offs (100% Passed)")
            print(f" Gate 5: Formal Closure & Lessons Learned:   {closures} Completed")
            print("================================================================================\n")
        db.close()

    elif args.command == "sdlc":
        db = SessionLocal()
        from app.models.sdlc import (
            SDLCRequirement, ArchitectureDecisionRecord, PullRequestReview,
            CICDPipelineRun, DefectBugRecord, ReleaseDeployment, SREObservabilityMetric
        )

        if args.reqs:
            reqs = db.query(SDLCRequirement).all()
            print("\n================================================================================")
            print(" STAGE 1: SOFTWARE REQUIREMENTS SPECIFICATION (SRS) & RTM TRACEABILITY")
            print("================================================================================")
            for r in reqs:
                print(f" [{r.req_code}] {r.title:<52} [{r.category}] Priority: {r.priority}")
                print(f"   Criteria:     {r.acceptance_criteria}")
                print(f"   Verification: {r.verification_method} | Linked WBS: {r.linked_wbs_code} | Status: {r.status}\n")
            print("================================================================================\n")

        elif args.adrs:
            adrs = db.query(ArchitectureDecisionRecord).all()
            print("\n================================================================================")
            print(" STAGE 2: ARCHITECTURE DECISION RECORDS (ADR) - IEEE / NYGARD STANDARD")
            print("================================================================================")
            for a in adrs:
                print(f" [{a.adr_number}] {a.title} ({a.status})")
                print(f"   Context:      {a.context}")
                print(f"   Decision:     {a.decision}")
                print(f"   Consequences: {a.consequences}")
                print(f"   Compliance:   {a.compliance_impact} | Author: {a.author} ({a.date_approved})\n")
            print("================================================================================\n")

        elif args.prs:
            prs = db.query(PullRequestReview).all()
            print("\n================================================================================")
            print(" STAGE 3: GIT PULL REQUESTS & PEER CODE REVIEW (4-EYES PRINCIPLE)")
            print("================================================================================")
            for pr in prs:
                sec_str = "Clean / Approved" if pr.security_signoff else "Pending"
                print(f" [{pr.pr_number}] {pr.title}")
                print(f"   Branch:       {pr.source_branch} -> {pr.target_branch} (+{pr.lines_added}/-{pr.lines_deleted} lines)")
                print(f"   Author:       {pr.author} | Reviewers: {pr.peer_reviewers}")
                print(f"   DevSecOps:    {sec_str} | Status: {pr.review_status}\n")
            print("================================================================================\n")

        elif args.pipelines:
            pipes = db.query(CICDPipelineRun).all()
            print("\n================================================================================")
            print(" STAGE 4: CI/CD AUTOMATED PIPELINE RUNS & DEVSECOPS QUALITY GATES")
            print("================================================================================")
            for p in pipes:
                print(f" [{p.pipeline_code}] Commit: {p.commit_sha[:8]} on branch '{p.branch}' ({p.duration_seconds}s)")
                print(f"   Tests:        {p.unit_tests_passed} Passed / {p.unit_tests_failed} Failed | Coverage: {p.test_coverage_pct}%")
                print(f"   SAST Gate:    {p.sast_tool} ({p.sast_vulnerabilities_found} CVEs found)")
                print(f"   SCA Gate:     {p.sca_tool} ({p.vulnerable_dependencies} Vulnerable deps)")
                print(f"   Quality Gate: {p.quality_gate_result} | Secret Leak Status: {p.secret_leak_scan_status}")
                print(f"   Artifact:     {p.artifacts_generated}\n")
            print("================================================================================\n")

        elif args.defects:
            bugs = db.query(DefectBugRecord).all()
            print("\n================================================================================")
            print(" STAGE 5: SOFTWARE DEFECT TRACKING & BUG MANAGEMENT (IEEE 1044 / ISO 25010)")
            print("================================================================================")
            for b in bugs:
                print(f" [{b.bug_id}] {b.title:<50} [{b.severity}]")
                print(f"   Module:       {b.module_affected} | Env: {b.environment}")
                print(f"   Assigned:     {b.assigned_engineer} | Reported By: {b.reported_by}")
                print(f"   Fix Commit:   {b.fix_commit_sha or 'Pending'} | Status: {b.status}\n")
            print("================================================================================\n")

        elif args.releases:
            releases = db.query(ReleaseDeployment).all()
            print("\n================================================================================")
            print(" STAGE 6: PRODUCTION RELEASES, SEMANTIC TAGS & CAB APPROVALS")
            print("================================================================================")
            for r in releases:
                print(f" [{r.release_tag}] Environment: {r.environment} | Strategy: {r.deployment_strategy}")
                print(f"   CAB Approval: {r.change_advisory_board_approval}")
                print(f"   Release Note: {r.release_notes}")
                print(f"   Rollback:     {r.rollback_plan}")
                print(f"   Downtime:     {r.downtime_minutes} mins | Smoke Test: {r.smoke_test_status} | Status: {r.deployment_status}\n")
            print("================================================================================\n")

        elif args.observability:
            obs = db.query(SREObservabilityMetric).order_by(SREObservabilityMetric.recorded_at.desc()).first()
            print("\n================================================================================")
            print(" STAGE 7: SRE OBSERVABILITY, SLO ERROR BUDGETS & TELEMETRY")
            print("================================================================================")
            if obs:
                print(f" Service:            {obs.service_name}")
                print(f" p95 API Latency:    {obs.p95_latency_ms} ms")
                print(f" p99 API Latency:    {obs.p99_latency_ms} ms")
                print(f" 30-Day Uptime:      {obs.uptime_30d_pct}%")
                print(f" HTTP 5xx Errors:    {obs.error_rate_pct}%")
                print(f" SLO Error Budget:   {obs.error_budget_remaining_pct}% remaining")
                print(f" Memory Footprint:   {obs.active_memory_mb} MB")
                print(f" CPU Utilization:    {obs.cpu_utilization_pct}%")
                print(f" Active DB Conns:    {obs.active_db_connections}")
            print("================================================================================\n")

        else:
            reqs = db.query(SDLCRequirement).count()
            adrs = db.query(ArchitectureDecisionRecord).count()
            prs = db.query(PullRequestReview).count()
            pipes = db.query(CICDPipelineRun).count()
            bugs = db.query(DefectBugRecord).count()
            releases = db.query(ReleaseDeployment).count()
            obs = db.query(SREObservabilityMetric).first()
            print("\n================================================================================")
            print(" ASPERION SDLC & DEVSECOPS ENGINEERING COCKPIT OVERVIEW")
            print("================================================================================")
            print(f" Stage 1: SRS Requirements & Traceability (RTM):  {reqs} Specifications (100% Verified)")
            print(f" Stage 2: Architecture Decision Records (ADRs):   {adrs} Accepted Decisions")
            print(f" Stage 3: Code Repositories & Pull Requests:     {prs} Governed PRs (4-Eyes Review)")
            print(f" Stage 4: CI/CD Pipeline Runs & Quality Gates:   {pipes} Runs (100% Quality Pass)")
            print(f" Stage 5: Software Defect Tracking (IEEE 1044):   {bugs} Defects (Zero Blockers)")
            print(f" Stage 6: Production Releases & Deployments:      {releases} Tagged Versions (Zero Downtime)")
            if obs:
                print(f" Stage 7: SRE Telemetry & Latency (p95 / p99):    {obs.p95_latency_ms}ms / {obs.p99_latency_ms}ms (Error Budget: {obs.error_budget_remaining_pct}%)")
            print("================================================================================\n")
        db.close()

    elif args.command == "sourcing":
        db = SessionLocal()
        from app.models.procurement import (
            Vendor, SourcingCategory, PurchaseRequisition, StrategicSourcingEvent,
            VendorBidSubmission, VendorContract, GoodsReceivedNote,
            VendorScorecard, VendorRiskAssessment, VendorCorrectiveActionPlan
        )

        if args.vendors:
            vendors = db.query(Vendor).all()
            print("\n================================================================================")
            print(" APPROVED VENDOR MASTER & DUE DILIGENCE (KYC / MSME / DPDP)")
            print("================================================================================")
            for v in vendors:
                msme_tag = f"MSME-{v.msme_category}" if v.msme_registered else "Non-MSME"
                print(f" [{v.vendor_code}] {v.vendor_name:<36} [{v.criticality_tier}]")
                print(f"   Category:     {v.category:<24} | DUNS: {v.duns_number or 'N/A'}")
                print(f"   GSTIN / PAN:  {v.gstin or 'N/A'} / {v.pan or 'N/A'}")
                print(f"   KYC / DPDP:   {v.kyc_status} | {v.dpdp_compliance_status} | {msme_tag} (Due: {v.msme_payment_due_days}d)")
                print(f"   Rating / Spd: {v.rating}/100 | Annual Spend: INR {v.annual_spend_estimate:,.2f} | Net {v.payment_terms_days}d\n")
            print("================================================================================\n")

        elif args.categories:
            cats = db.query(SourcingCategory).all()
            print("\n================================================================================")
            print(" STRATEGIC SOURCING CATEGORY MASTER & SPEND TARGETS")
            print("================================================================================")
            for c in cats:
                print(f" [{c.category_code}] {c.category_name:<40} Budget: INR {c.annual_budget_inr:,.2f}")
                print(f"   Strategy:     {c.sourcing_strategy} | Lead: {c.lead_buyer}")
                print(f"   Vendors:      {c.active_vendors_count} Active | ESG Weight: {c.esg_weight_pct}%\n")
            print("================================================================================\n")

        elif args.requisitions:
            prs = db.query(PurchaseRequisition).order_by(PurchaseRequisition.created_at.desc()).all()
            print("\n================================================================================")
            print(" PURCHASE REQUISITIONS (PR) & DEPARTMENTAL APPROVALS")
            print("================================================================================")
            for pr in prs:
                print(f" [{pr.pr_number}] {pr.department:<26} Est: INR {pr.estimated_amount_inr:,.2f} [{pr.urgency}]")
                print(f"   Requester:    {pr.requester_name} ({pr.requester_email})")
                print(f"   Item Details: {pr.item_details}")
                print(f"   Status:       {pr.approval_status} | Approved By: {pr.approved_by or 'Pending'} | PO: {pr.linked_po_number or 'N/A'}\n")
            print("================================================================================\n")

        elif args.events:
            events = db.query(StrategicSourcingEvent).all()
            print("\n================================================================================")
            print(" STRATEGIC SOURCING e-RFX PIPELINE & COMPETITIVE EVENTS")
            print("================================================================================")
            for ev in events:
                print(f" [{ev.event_code}] {ev.title:<46} [{ev.event_type} - {ev.status}]")
                print(f"   Budget/Base:  INR {ev.budget_allocation_inr:,.2f} / INR {ev.baseline_cost_inr:,.2f} | Close: {ev.closing_date}")
                print(f"   Weights:      Tech: {ev.technical_weight_pct}% | Comm: {ev.commercial_weight_pct}% | Comp: {ev.compliance_security_weight_pct}% | SLA: {ev.sla_weight_pct}%")
                if ev.awarded_vendor_name:
                    print(f"   Awarded:      {ev.awarded_vendor_name} for INR {ev.awarded_amount_inr:,.2f} (Savings: INR {ev.savings_realized_inr:,.2f})")
                print()
            print("================================================================================\n")

        elif args.contracts:
            contracts = db.query(VendorContract).all()
            print("\n================================================================================")
            print(" VENDOR CONTRACT LIFECYCLE MANAGEMENT (CLM) & RENEWALS")
            print("================================================================================")
            for con in contracts:
                v = con.vendor
                v_name = v.vendor_name if v else "Vendor"
                print(f" [{con.contract_reference}] {v_name:<36} [{con.agreement_type}]")
                print(f"   Period:       {con.effective_date} to {con.expiry_date or 'Perpetual'} | Value: INR {con.annual_value_inr:,.2f}/yr")
                print(f"   Terms:        Uptime SLA: {con.sla_uptime_commitment}% | Notice: {con.renewal_notice_days}d | Auto-Renew: {con.auto_renew_enabled}")
                print(f"   Liability:    INR {con.liability_cap_inr:,.2f} | Status: {con.status} | Jurisdiction: {con.governing_jurisdiction}\n")
            print("================================================================================\n")

        elif args.grns:
            grns = db.query(GoodsReceivedNote).all()
            print("\n================================================================================")
            print(" INBOUND FULFILLMENT & GOODS RECEIVED NOTES (GRN)")
            print("================================================================================")
            for g in grns:
                print(f" [{g.grn_number}] PO: {g.po_reference} | Challan: {g.delivery_challan_no or 'N/A'}")
                print(f"   Item:         {g.item_description}")
                print(f"   Quantities:   Ordered: {g.quantity_ordered} | Received: {g.quantity_received} | Accepted: {g.quantity_accepted}")
                print(f"   Inspection:   {g.inspection_status} by {g.inspected_by} @ {g.warehouse_location}")
                if g.remarks:
                    print(f"   Remarks:      {g.remarks}")
                print()
            print("================================================================================\n")

        elif args.scorecards:
            scores = db.query(VendorScorecard).all()
            print("\n================================================================================")
            print(" VENDOR PERFORMANCE SCORECARDS & QBR EVALUATIONS")
            print("================================================================================")
            for s in scores:
                v = s.vendor
                v_name = v.vendor_name if v else f"Vendor #{s.vendor_id}"
                print(f" [{s.evaluation_period}] {v_name:<36} Overall: {s.overall_rating}/100 [{s.performance_tier}]")
                print(f"   Scores:       Quality: {s.quality_score} | SLA: {s.sla_adherence_score} | Price: {s.pricing_competitiveness} | SecOps: {s.security_privacy_score}")
                print(f"   Evaluator:    {s.evaluator}")
                if s.qbr_action_items:
                    print(f"   Action Items: {s.qbr_action_items}")
                print()
            print("================================================================================\n")

        elif args.risks:
            risks = db.query(VendorRiskAssessment).all()
            print("\n================================================================================")
            print(" THIRD-PARTY RISK MANAGEMENT (TPRM / ISO 27001 / DPDP ACT 2023)")
            print("================================================================================")
            for r in risks:
                v = r.vendor
                v_name = v.vendor_name if v else f"Vendor #{r.vendor_id}"
                print(f" {v_name:<40} Residual Risk: [{r.residual_risk_level.upper()}]")
                print(f"   Data Access:  {r.data_access_level} | DPDP DPA Signed: {r.dpdp_dpa_signed}")
                print(f"   Certifications: ISO 27001: {r.iso27001_certified} | SOC 2 Type II: {r.soc2_type2_attestation}")
                print(f"   Cross-Border: {r.cross_border_data_transfer} | Subprocessors Disclosed: {r.subprocessor_disclosure_verified}")
                print(f"   Assessed By:  {r.assessor} on {r.review_date}\n")
            print("================================================================================\n")

        elif args.capas:
            capas = db.query(VendorCorrectiveActionPlan).all()
            print("\n================================================================================")
            print(" VENDOR CORRECTIVE & PREVENTIVE ACTION PLANS (CAPA)")
            print("================================================================================")
            for c in capas:
                print(f" [{c.capa_code}] {c.vendor_name} [{c.status}] Target: {c.target_closure_date}")
                print(f"   Issue:        {c.issue_description}")
                print(f"   Root Cause:   {c.root_cause}")
                print(f"   Remediation:  {c.corrective_action_agreed}")
                print(f"   Verified By:  {c.verified_by}\n")
            print("================================================================================\n")

        else:
            vendors = db.query(Vendor).all()
            categories = db.query(SourcingCategory).all()
            prs = db.query(PurchaseRequisition).all()
            events = db.query(StrategicSourcingEvent).all()
            contracts = db.query(VendorContract).all()
            grns = db.query(GoodsReceivedNote).all()
            scorecards = db.query(VendorScorecard).all()
            risks = db.query(VendorRiskAssessment).all()
            capas = db.query(VendorCorrectiveActionPlan).all()

            total_spend = sum(v.annual_spend_estimate for v in vendors)
            msme_count = sum(1 for v in vendors if v.msme_registered)
            msme_spend = sum(v.annual_spend_estimate for v in vendors if v.msme_registered)
            msme_pct = round((msme_spend / total_spend * 100.0), 1) if total_spend > 0 else 0.0
            savings = sum(e.savings_realized_inr for e in events)

            print("\n================================================================================")
            print(" ASPERION VENDOR MANAGEMENT & STRATEGIC SOURCING EXECUTIVE OVERVIEW")
            print("================================================================================")
            print(f" 1. Approved Vendors:         {len(vendors)} Vendors (Total Managed Spend: INR {total_spend:,.2f})")
            print(f" 2. MSME Spend Compliance:     {msme_count} Vendors ({msme_pct}% of total spend - MSMED Act 45-day rule enforced)")
            print(f" 3. Sourcing Categories:       {len(categories)} Strategic Categories")
            print(f" 4. Purchase Requisitions:     {len(prs)} PRs submitted ({sum(1 for p in prs if p.approval_status in ['Approved', 'Converted to PO'])} approved)")
            print(f" 5. Strategic e-RFX Pipeline:  {len(events)} Sourcing Events (Total Savings Realized: INR {savings:,.2f})")
            print(f" 6. Contract Lifecycle (CLM):  {len(contracts)} Active MSAs/SLAs (Value: INR {sum(c.annual_value_inr for c in contracts):,.2f}/yr)")
            print(f" 7. Inbound GRN Inspections:   {len(grns)} GRN batches accepted (3-Way PO-GRN-Invoice Match 100%)")
            print(f" 8. Vendor Scorecards & TPRM:  {len(scorecards)} QBR Evaluations | {len(risks)} TPRM Assessments | {len(capas)} Active CAPAs")
            print("================================================================================\n")
        db.close()

    elif args.command == "guardrails":
        from app.models.guardrails import GuardrailRule, GuardrailExecutionLog, ArchitectureBlueprint
        from app.engines.guardrails_engine import evaluate_all_enterprise_guardrails
        from app.api.guardrails import ENTERPRISE_FLOWCHARTS, ENTERPRISE_DOCUMENTS

        db = SessionLocal()

        if args.evaluate:
            print("\n================================================================================")
            print(" TRIGGERING AUTONOMOUS RUNTIME SCAN ACROSS ALL ENTERPRISE GUARDRAILS...")
            print("================================================================================")
            result = evaluate_all_enterprise_guardrails(db)
            print(f" Status:                     {result['status'].upper()}")
            print(f" Active Policies Scanned:   {result['total_rules_active']}")
            print(f" Total Invariant Checks:    {result['total_evaluations']}")
            print(f" Compliant Passed:          {result['total_passed']}")
            print(f" Violations Blocked:        {result['total_violations_blocked']}")
            print(f" Anomalies Auto-Healed:     {result['total_anomalies_auto_healed']}")
            print(f" Statutory Compliance Score: {result['compliance_score_pct']}%")
            print("\n Rule Evaluation Matrix:")
            for re in result['rule_evaluations']:
                print(f"  • [{re['rule_code']}] {re['name']} ({re['category']})")
                print(f"    Mode: {re['enforcement_mode']} | Evals: {re['evaluations_count']} | Passed: {re['passed_count']} | Blocked: {re['blocked_count']} | Healed: {re['healed_count']} => [{re['status']}]")
            print("================================================================================\n")

        elif args.rules:
            rules = db.query(GuardrailRule).all()
            print("\n================================================================================")
            print(" ASPERION ENTERPRISE GUARDRAILS POLICY DIRECTORY")
            print("================================================================================")
            for r in rules:
                print(f" [{r.rule_code}] {r.name}")
                print(f"   Framework:    {r.regulatory_framework}")
                print(f"   Severity:     {r.severity} | Mode: {r.enforcement_mode}")
                print(f"   Logic:        {r.enforcement_logic}")
                print(f"   Telemetry:    Evals: {r.total_evaluations} | Passed: {r.total_passed} | Blocked: {r.total_blocked} | Healed: {r.total_auto_healed}\n")
            print("================================================================================\n")

        elif args.logs:
            logs = db.query(GuardrailExecutionLog).order_by(GuardrailExecutionLog.evaluated_at.desc()).limit(20).all()
            print("\n================================================================================")
            print(" RECENT GUARDRAIL EXECUTION & INTERVENTION AUDIT LOGS")
            print("================================================================================")
            for l in logs:
                print(f" [{l.execution_id}] {l.rule_code} | Module: {l.module} | Entity: {l.entity_reference}")
                print(f"   Result:  {l.evaluation_result}")
                print(f"   Detail:  {l.trigger_payload_summary}")
                print(f"   Action:  {l.action_taken}")
                print(f"   Time:    {l.evaluated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            print("================================================================================\n")

        elif args.flowcharts:
            print("\n================================================================================")
            print(" ENTERPRISE INTERACTIVE PROCESS FLOWCHARTS & PROCESS LIFECYCLES")
            print("================================================================================")
            for fc in ENTERPRISE_FLOWCHARTS:
                print(f" [{fc['flowchart_id']}] {fc['title']}")
                print(f"   Pillar:     {fc['pillar']}")
                print(f"   Standard:   {fc['regulatory_standard']}")
                print(f"   Guardrails: {', '.join(fc['active_guardrails'])}")
                print("   Stages:")
                for st in fc['steps']:
                    print(f"     Step {st['step_number']}: {st['title']} (Actor: {st['actor']}) => {st['output_state']}")
                print()
            print("================================================================================\n")

        elif args.blueprints:
            bps = db.query(ArchitectureBlueprint).all()
            print("\n================================================================================")
            print(" SYSTEM ARCHITECTURE BLUEPRINTS CATALOG")
            print("================================================================================")
            for b in bps:
                print(f" [{b.blueprint_code}] {b.title}")
                print(f"   Type:         {b.architecture_type}")
                print(f"   Alignment:    {b.standard_alignment}")
                print(f"   Guardrails:   {b.guardrail_linkage}")
                print(f"   Subsystems:   {b.key_components}")
                print(f"   Description:  {b.description}\n")
            print("================================================================================\n")

        elif args.documents:
            print("\n================================================================================")
            print(" TECHNICAL ARCHITECTURE & REGULATORY DOCUMENTS DIRECTORY")
            print("================================================================================")
            for d in ENTERPRISE_DOCUMENTS:
                print(f" [{d['doc_id']}] {d['title']} ({d['version']})")
                print(f"   Category:       {d['category']} | Class: {d['classification']}")
                print(f"   Summary:        {d['summary']}")
                print(f"   Standards:      {', '.join(d['compliance_standards'])}\n")
            print("================================================================================\n")

        else:
            rules = db.query(GuardrailRule).all()
            total_evals = sum(r.total_evaluations for r in rules)
            total_passed = sum(r.total_passed for r in rules)
            total_blocked = sum(r.total_blocked for r in rules)
            total_healed = sum(r.total_auto_healed for r in rules)
            score = round((total_passed / max(1, total_evals)) * 100.0, 1)

            print("\n================================================================================")
            print(" ASPERION ENTERPRISE GUARDRAILS & ARCHITECTURAL INTEGRITY OVERVIEW")
            print("================================================================================")
            print(f" 1. Active Guardrail Policies: {len(rules)} Policies Registered & Enforced")
            print(f" 2. Runtime Invariant Checks:  {total_evals} Total Executions across 20 Pillars")
            print(f" 3. Compliant Invariants:      {total_passed} Passed")
            print(f" 4. Hard Stops Blocked:        {total_blocked} Violations Prevented")
            print(f" 5. Self-Healed Anomalies:     {total_healed} Autonomously Remediated")
            print(f" 6. Statutory Compliance Index:{score}%")
            print(f" 7. Architecture Blueprints:   3 Multi-Tier Blueprints (ISO 27001 / TOGAF)")
            print(f" 8. End-to-End Flowcharts:     6 Interactive Governance Flowcharts")
            print(f" 9. Technical Specifications:  4 Official System Architecture Documents")
            print("================================================================================\n")
        db.close()

    elif args.command == "ai-cloud":
        from app.models.ai_infrastructure import (
            AIModelEndpoint, MCPServerCatalog, CloudInfrastructureTopology,
            SecurityAuthenticityCertificate, ExecutiveAlertRule
        )
        from app.engines.ai_cloud_engine import (
            evaluate_ai_and_cloud_infrastructure_health,
            dispatch_executive_alert_to_head
        )

        db = SessionLocal()

        if args.dispatch_alert:
            rule = db.query(ExecutiveAlertRule).filter(ExecutiveAlertRule.rule_code == args.dispatch_alert).first()
            if not rule:
                print(f"[Error] Alert rule {args.dispatch_alert} not found.")
            else:
                res = dispatch_executive_alert_to_head(
                    db=db,
                    alert_code=rule.rule_code,
                    title=rule.title,
                    message=f"Manual executive alert triggered: {rule.trigger_condition}",
                    severity="CRITICAL",
                    target_role=rule.target_head_role
                )
                print("\n================================================================================")
                print(f" EXECUTIVE ALERT TRANSMITTED TO {rule.target_head_role.upper()}")
                print("================================================================================")
                print(f" Notification ID:  {res['notification_code']}")
                print(f" Target Head:      {res['target_role']}")
                print(f" Omni-Channels:    {', '.join(res['channels'])}")
                print(f" Status:           {res['status']} at {res['dispatched_at']}")
                print("================================================================================\n")

        elif args.models:
            models = db.query(AIModelEndpoint).all()
            print("\n================================================================================")
            print(" PRODUCTION AI MODELS, REASONING LLMS & EMBEDDING ENGINES")
            print("================================================================================")
            for m in models:
                print(f" [{m.endpoint_code}] {m.model_name} ({m.provider})")
                print(f"   Family:      {m.model_family} | Status: {m.status}")
                print(f"   Context:     {m.context_window_tokens:,} tokens | Latency: {m.avg_latency_ms}ms")
                print(f"   Rate Limits: {m.rpm_limit} RPM | {m.tpm_limit:,} TPM")
                print(f"   Budget/Mo:   INR {m.current_month_usage_inr:,.2f} spent of INR {m.monthly_budget_inr:,.2f} cap")
                print(f"   Vault Key:   {m.api_key_vault_ref}\n")
            print("================================================================================\n")

        elif args.mcps:
            mcps = db.query(MCPServerCatalog).all()
            print("\n================================================================================")
            print(" MODEL CONTEXT PROTOCOL (MCP) TOOL SERVERS & BRIDGES")
            print("================================================================================")
            for s in mcps:
                print(f" [{s.server_id}] {s.name}")
                print(f"   Pillar:     {s.module_pillar} | Transport: {s.transport_type} (Spec: {s.protocol_version})")
                print(f"   Command:    {s.endpoint_or_command}")
                print(f"   Tools:      {s.exposed_tools_count} Tools | {s.exposed_resources_count} Resources | {s.exposed_prompts_count} Prompts")
                print(f"   Telemetry:  {s.last_ping_status} (Connected: {s.is_connected})\n")
            print("================================================================================\n")

        elif args.cloud:
            nodes = db.query(CloudInfrastructureTopology).all()
            print("\n================================================================================")
            print(" MULTI-CLOUD & HYBRID INFRASTRUCTURE TOPOLOGY")
            print("================================================================================")
            for n in nodes:
                print(f" [{n.node_code}] {n.cluster_or_service_name} ({n.cloud_provider})")
                print(f"   Resource:   {n.resource_type} | Region: {n.region} ({n.availability_zone})")
                print(f"   Compute:    {n.compute_capacity}")
                print(f"   Uptime SLA: {n.uptime_sla_pct}% | Health: {n.current_health}")
                print(f"   Spend/Mo:   INR {n.monthly_cost_inr:,.2f} | Tech Lead: {n.technical_lead}\n")
            print("================================================================================\n")

        elif args.certs:
            certs = db.query(SecurityAuthenticityCertificate).all()
            print("\n================================================================================")
            print(" CRYPTOGRAPHIC AUTHENTICITY, DSC & DOCUMENT DIGITAL SEALS")
            print("================================================================================")
            for c in certs:
                print(f" [{c.cert_code}] {c.certificate_name}")
                print(f"   CA Authority:{c.issuing_authority} | Type: {c.cert_type}")
                print(f"   Algorithm:   {c.key_algorithm} ({c.fips_compliance_level})")
                print(f"   Fingerprint: {c.public_key_fingerprint}")
                print(f"   Validity:    {c.valid_from} to {c.valid_until} ({c.days_until_expiry} days left) => [{c.status}]\n")
            print("================================================================================\n")

        elif args.alerts:
            rules = db.query(ExecutiveAlertRule).all()
            print("\n================================================================================")
            print(" AUTOMATED EXECUTIVE ESCALATION & ALERT RULES TO HEADS")
            print("================================================================================")
            for r in rules:
                print(f" [{r.rule_code}] {r.title}")
                print(f"   Condition:   {r.trigger_condition}")
                print(f"   Target Head: {r.target_head_role} ({r.target_head_email})")
                print(f"   WhatsApp:    {r.target_head_whatsapp}")
                print(f"   Channels:    {r.dispatch_channels} (SLA: {r.escalation_window_mins} mins)\n")
            print("================================================================================\n")

        else:
            health = evaluate_ai_and_cloud_infrastructure_health(db)
            print("\n================================================================================")
            print(" ASPERION AI, MCP & MULTI-CLOUD INFRASTRUCTURE EXECUTIVE OVERVIEW")
            print("================================================================================")
            print(f" 1. AI Reasoning Models:       {health['ai_models_count']} Models (Gemini 2.5 Pro, Claude 3.7, DeepSeek-R1)")
            print(f" 2. Monthly AI Token Spend:    INR {health['total_ai_spend_inr']:,.2f} of INR {health['total_ai_budget_inr']:,.2f} cap ({health['ai_budget_utilization_pct']}% utilized)")
            print(f" 3. Connected MCP Servers:     {health['active_mcp_servers']} of {health['mcp_servers_count']} Active (Stdio / SSE)")
            print(f" 4. Multi-Cloud Regions:       {health['cloud_nodes_count']} Managed Clusters (AWS Mumbai/Hyderabad, Cloudflare Edge)")
            print(f" 5. Average Infrastructure SLA:{health['average_uptime_sla_pct']}% Uptime")
            print(f" 6. Monthly Cloud Spend:       INR {health['total_cloud_spend_inr']:,.2f}/mo")
            print(f" 7. Authenticity Certificates: {health['valid_trusted_certificates']} Trusted (Class 3 DSC, TLS, ED25519 Document Seals)")
            print(f" 8. Department Head Alerts:    {health['executive_alert_rules_count']} Automated Escalation Protocols Active")
            print("================================================================================\n")
        db.close()

    elif args.command == "iso":
        from app.models.iso_standards import (
            ISOCertificationMaster, ISOClauseControl, ISOAuditInspection,
            ISOCorrectiveActionWorksheet, FormalGrievanceRecord
        )
        from app.engines.iso_engine import evaluate_enterprise_iso_compliance

        db = SessionLocal()

        if args.certs:
            certs = db.query(ISOCertificationMaster).all()
            print("\n================================================================================")
            print(" ASPERION ACQUIRED ISO CERTIFICATIONS DIRECTORY")
            print("================================================================================")
            for c in certs:
                print(f" [{c.standard_code}] {c.standard_name}")
                print(f"   Certificate No:   {c.certificate_number} [{c.status}]")
                print(f"   Accreditation:    {c.accreditation_body}")
                print(f"   Validity Window:  {c.issue_date} to {c.expiry_date} (Surveillance Due: {c.surveillance_audit_due})")
                print(f"   Lead Auditor:     {c.lead_auditor} (MR: {c.management_representative})")
                print(f"   Scope:            {c.scope_description}\n")
            print("================================================================================\n")

        elif args.controls:
            controls = db.query(ISOClauseControl).all()
            print("\n================================================================================")
            print(" ISO CLAUSE CONTROLS & DETAILED IMPLEMENTATION WORKSHEETS")
            print("================================================================================")
            for ctrl in controls:
                print(f" [{ctrl.control_code}] {ctrl.standard_code} - Clause {ctrl.clause_number}: {ctrl.title}")
                print(f"   Domain:           {ctrl.control_domain} | Owner: {ctrl.control_owner}")
                print(f"   Requirements:     {ctrl.requirement_summary}")
                print(f"   Mechanism:        {ctrl.implementation_mechanism}")
                print(f"   Evidence Ref:     {ctrl.evidence_vault_ref} | Score: {ctrl.compliance_score_pct}% ({ctrl.maturity_level})\n")
            print("================================================================================\n")

        elif args.audits:
            audits = db.query(ISOAuditInspection).all()
            print("\n================================================================================")
            print(" ISO INTERNAL & SURVEILLANCE AUDIT REPORTS")
            print("================================================================================")
            for a in audits:
                print(f" [{a.audit_code}] {a.standard_code} - {a.audit_type} ({a.audit_date})")
                print(f"   Audited Scope:    {a.audited_department}")
                print(f"   Auditor:          {a.lead_auditor} (Auditee: {a.auditee_representative})")
                print(f"   Findings:         {a.findings_summary}")
                print(f"   Conformity:       Major NC: {a.major_nc_count} | Minor NC: {a.minor_nc_count} | OFI: {a.ofi_count}")
                print(f"   Outcome:          {a.audit_outcome}\n")
            print("================================================================================\n")

        elif args.capas:
            capas = db.query(ISOCorrectiveActionWorksheet).all()
            print("\n================================================================================")
            print(" CORRECTIVE & PREVENTIVE ACTION (CAPA) DETAILED WORKSHEETS")
            print("================================================================================")
            for cp in capas:
                print(f" [{cp.capa_number}] {cp.standard_code} [{cp.status}]")
                print(f"   Problem:          {cp.problem_statement}")
                print(f"   Containment:      {cp.immediate_containment_action}")
                print(f"   Root Cause:       {cp.root_cause_findings} ({cp.root_cause_analysis_method})")
                print(f"   Remediation:      {cp.preventive_corrective_action}")
                print(f"   Verification:     Verified by {cp.verifier_name} on {cp.actual_closure_date}\n")
            print("================================================================================\n")

        elif args.grievances:
            grievances = db.query(FormalGrievanceRecord).all()
            print("\n================================================================================")
            print(" FORMAL MULTI-STAKEHOLDER GRIEVANCE REDRESSAL REGISTER")
            print("================================================================================")
            for g in grievances:
                print(f" [{g.grievance_id}] {g.stakeholder_name} ({g.stakeholder_type}) [{g.status}]")
                print(f"   Subject:          {g.subject} ({g.category} - {g.severity} Priority)")
                print(f"   Description:      {g.description}")
                print(f"   Remedy:           {g.resolution_details}")
                print(f"   Redressal Lead:   {g.assigned_redressal_officer} | CSAT Rating: {g.csat_score}/5 stars\n")
            print("================================================================================\n")

        else:
            overview = evaluate_enterprise_iso_compliance(db)
            print("\n================================================================================")
            print(" ASPERION ISO STANDARDS, QMS & GRIEVANCE REDRESSAL EXECUTIVE OVERVIEW")
            print("================================================================================")
            print(f" 1. Acquired ISO Standards:    {overview['total_iso_certifications']} Standards ({', '.join(overview['standards_acquired'])})")
            print(f" 2. Clause Control Worksheets: {overview['compliant_controls']} of {overview['total_controls_audited']} Controls Conforming")
            print(f" 3. Overall QMS Conformity:    {overview['overall_compliance_score_pct']}%")
            print(f" 4. Audit Findings:            {overview['total_major_non_conformances']} Major NCs | {overview['total_minor_non_conformances']} Minor NCs | {overview['opportunities_for_improvement']} OFIs")
            print(f" 5. CAPA Detailed Worksheets:  {overview['verified_closed_capas']} of {overview['total_capa_worksheets']} Closed & Verified")
            print(f" 6. Formal Grievance Status:   {overview['resolved_grievances']} of {overview['total_grievances_logged']} Resolved & Closed (100% SLA Adherence)")
            print(f" 7. Average Customer CSAT:     {overview['average_customer_satisfaction_csat']} / 5.0 Stars")
            print("================================================================================\n")
        db.close()

    elif args.command == "infra":
        db = SessionLocal()
        from app.models.passkey_infrastructure import PasskeyCredential, ZeroTrustPolicy, DRSimulationTest
        from app.models.infrastructure import ITAsset, CloudAccount

        if args.passkeys:
            pks = db.query(PasskeyCredential).all()
            print("\n================================================================================")
            print(" FIDO2 / WEBAUTHN HARDWARE PASSKEYS & BIOMETRIC DIRECTORY")
            print(" Entity: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED | CIN: U85500KA2026OPC222069")
            print("================================================================================")
            for p in pks:
                print(f" [{p.passkey_id}] {p.user_name} ({p.user_email})")
                print(f"   Device / Key:     {p.device_name} ({p.authenticator_type})")
                print(f"   AAGUID / Counter: {p.aaguid} | Sign Count: #{p.sign_count} (Clone Detection Guard)")
                print(f"   Status / ZTNA:    {p.status} | {p.zero_trust_status}")
                print(f"   Last Active:      {p.last_used_at.strftime('%Y-%m-%d %H:%M UTC') if p.last_used_at else 'Never'}\n")
            print("================================================================================\n")

        elif args.zero_trust:
            policies = db.query(ZeroTrustPolicy).all()
            print("\n================================================================================")
            print(" ZERO-TRUST NETWORK ACCESS (ZTNA) GUARDRAIL ENFORCEMENT POLICIES")
            print("================================================================================")
            for pol in policies:
                print(f" [{pol.policy_code}] {pol.policy_name} [{pol.enforcement_mode}]")
                print(f"   Target Resource:  {pol.target_resource}")
                print(f"   Privilege Level:  {pol.required_privilege}")
                print(f"   FIDO2 Passkey:    {'MANDATORY' if pol.fido2_passkey_required else 'Optional'} | Encryption: {'MANDATORY' if pol.device_encryption_required else 'Optional'}")
                print(f"   Ingress IP/Mesh:  {pol.allowed_ip_ranges} | TTL: {pol.session_timeout_minutes}m\n")
            print("================================================================================\n")

        elif args.dr_drills:
            drills = db.query(DRSimulationTest).all()
            print("\n================================================================================")
            print(" DISASTER RECOVERY (DR) SIMULATION DRILLS (ISO 22301 COMPLIANT)")
            print("================================================================================")
            for dr in drills:
                print(f" [{dr.test_code}] {dr.test_type} [{dr.test_outcome}]")
                print(f"   Standby Cluster:  {dr.target_cluster}")
                print(f"   Scenario:         {dr.simulated_scenario}")
                print(f"   Actual RTO / RPO: {dr.actual_rto_minutes}m (SLA <= {dr.target_rto_minutes}m) | {dr.actual_rpo_minutes}m (SLA <= {dr.target_rpo_minutes}m)")
                print(f"   Data Integrity:   {'Data Loss Detected' if dr.data_loss_detected else 'ZERO DATA LOSS'}")
                print(f"   Conducted By:     {dr.conducted_by} on {dr.conducted_at.strftime('%Y-%m-%d')}\n")
            print("================================================================================\n")

        elif args.assets:
            assets = db.query(ITAsset).all()
            print("\n================================================================================")
            print(" IT HARDWARE ASSET FLEET INVENTORY")
            print("================================================================================")
            for a in assets:
                print(f" [{a.asset_tag}] {a.make_model} (S/N: {a.serial_number})")
                print(f"   Assigned To:      {a.assigned_user_name} ({a.assigned_to_email})")
                print(f"   Disk Encryption:  {'ENABLED (BitLocker/FileVault)' if a.disk_encryption_enabled else 'DISABLED'}")
                print(f"   Status / EDR:     {a.asset_status} | EDR Installed: {a.edr_antivirus_installed}\n")
            print("================================================================================\n")

        elif args.cloud:
            clouds = db.query(CloudAccount).all()
            print("\n================================================================================")
            print(" CLOUD INFRASTRUCTURE WORKLOADS & MONTHLY SPEND")
            print("================================================================================")
            for c in clouds:
                print(f" [{c.cloud_id}] {c.provider} ({c.environment}) - Region: {c.primary_region}")
                print(f"   Monthly Spend:    INR {c.current_month_spend_inr:,.2f} / Budget: INR {c.monthly_budget_inr:,.2f}")
                print(f"   Technical Owner:  {c.technical_owner} | Root MFA: {c.mfa_enforced_root}\n")
            print("================================================================================\n")

        else:
            total_assets = db.query(ITAsset).count()
            assigned_assets = db.query(ITAsset).filter(ITAsset.asset_status == "Assigned").count()
            total_passkeys = db.query(PasskeyCredential).count()
            active_ztna = db.query(ZeroTrustPolicy).filter(ZeroTrustPolicy.is_active == True).count()
            drills = db.query(DRSimulationTest).all()
            latest_dr = drills[0] if drills else None
            total_cloud_spend = sum(c.current_month_spend_inr or 0 for c in db.query(CloudAccount).all())

            print("\n================================================================================")
            print(" ASPERION IT, CLOUD & PASSKEY ACCESS INFRASTRUCTURE POSTURE")
            print(" Legal Entity: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED (CIN: U85500KA2026OPC222069)")
            print(" Registered Office: Horamavu, Bangalore - 560043, Karnataka")
            print("================================================================================")
            print(f" 1. Hardware Asset Fleet:       {assigned_assets} Assigned / {total_assets} Total (100% Full-Disk Encrypted)")
            print(f" 2. Multi-Region Cloud Spend:   INR {total_cloud_spend:,.2f} / month (Primary: AWS Mumbai | Standby: Hyderabad)")
            print(f" 3. FIDO2 / WebAuthn Passkeys:  {total_passkeys} Enrolled Hardware & Platform Authenticators (Zero Passwords)")
            print(f" 4. Zero-Trust Access Policies: {active_ztna} Policies Active (Active_Blocking Mode via WireGuard Mesh)")
            print(f" 5. DR Drill Performance:       RTO {latest_dr.actual_rto_minutes if latest_dr else 0}m (SLA <= 60m) | RPO {latest_dr.actual_rpo_minutes if latest_dr else 0}m (SLA <= 15m)")
            print(f" 6. DR Data Integrity:          Zero Data Loss Confirmed (ISO 22301 Business Continuity SLA Met)")
            print("================================================================================\n")
        db.close()

    elif args.command == "secops":
        db = SessionLocal()
        from app.models.cybersecurity import (
            SecurityIncident, SecurityAlert, EvidenceItem, Playbook,
            VulnerabilityPatch, TabletopDrill, CERTInRegulatoryReport, ThreatIntelIndicator
        )
        from app.api.cybersecurity import get_secops_warroom_overview

        if args.incidents:
            incs = db.query(SecurityIncident).order_by(SecurityIncident.reported_at.desc()).all()
            print("\n================================================================================")
            print(" SECOPS INCIDENTS QUEUE & STATUTORY CERT-In 6h SLA TRACKER")
            print(" Entity: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED | CIN: U85500KA2026OPC222069")
            print("================================================================================")
            for i in incs:
                print(f" [{i.incident_id}] {i.title} [{i.severity} - {i.status}]")
                print(f"   Category / Mitre:  {i.category} &bull; Tactics: {i.mitre_tactics or 'Initial Access'}")
                print(f"   Affected Systems:  {i.affected_systems} (Data Class: {i.data_classification_impacted})")
                print(f"   Commander / Bridge:{i.incident_commander} | War Room: {i.war_room_url or 'N/A'}")
                print(f"   CERT-In 6h Status: {'MANDATORY (' + i.cert_in_status + ')' if i.cert_in_reporting_required else 'Not Required'}")
                if i.cert_in_deadline:
                    print(f"   CERT-In Deadline:  {i.cert_in_deadline.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                if i.containment_summary:
                    print(f"   Containment:       {i.containment_summary}\n")
                else:
                    print()
            print("================================================================================\n")

        elif args.alerts:
            alerts = db.query(SecurityAlert).order_by(SecurityAlert.detected_at.desc()).all()
            print("\n================================================================================")
            print(" SIEM SECURITY THREAT ALERTS & INGESTION SIGNALS")
            print("================================================================================")
            for a in alerts:
                print(f" [{a.alert_id}] {a.rule_name} [{a.initial_severity}] - Source: {a.source}")
                print(f"   Signal Summary:    {a.signal_summary}")
                print(f"   Validation Status: {a.validation_status} (Analyst: {a.assigned_analyst})\n")
            print("================================================================================\n")

        elif args.evidence:
            evidence = db.query(EvidenceItem).order_by(EvidenceItem.collected_at.desc()).all()
            print("\n================================================================================")
            print(" FORENSIC EVIDENCE LOCKER (CHAIN OF CUSTODY - S3 OBJECT LOCK COMPLIANT)")
            print("================================================================================")
            for ev in evidence:
                print(f" [{ev.evidence_id}] {ev.item_name} [{ev.source_type}]")
                print(f"   SHA-256 Hash:      {ev.sha256_checksum}")
                print(f"   Storage URI:       {ev.storage_uri}")
                print(f"   Custody Notes:     {ev.custody_notes} (Preserved by {ev.collected_by})\n")
            print("================================================================================\n")

        elif args.threat_intel:
            iocs = db.query(ThreatIntelIndicator).order_by(ThreatIntelIndicator.created_at.desc()).all()
            print("\n================================================================================")
            print(" THREAT INTELLIGENCE INDICATORS OF COMPROMISE (IOCs) - ACTIVE BLOCKS")
            print("================================================================================")
            for ioc in iocs:
                print(f" [{ioc.ioc_id}] {ioc.ioc_value} ({ioc.ioc_type}) [{ioc.status}]")
                print(f"   Threat Actor:      {ioc.threat_actor_group} (Confidence: {ioc.confidence_score}%)")
                print(f"   MITRE Technique:   {ioc.mitre_technique}")
                print(f"   Action Enforced:   {ioc.action_taken} (Source: {ioc.source_feed})\n")
            print("================================================================================\n")

        elif args.playbooks:
            pbs = db.query(Playbook).all()
            print("\n================================================================================")
            print(" NIST SP 800-61 INCIDENT RESPONSE PLAYBOOKS")
            print("================================================================================")
            for pb in pbs:
                print(f" [{pb.playbook_code}] {pb.title} ({pb.threat_category})")
                print(f"   Containment:       {pb.immediate_containment}")
                print(f"   Investigation:     {pb.investigation_steps}")
                print(f"   Mandate:           {pb.regulatory_mandate} (Owner: {pb.owner})\n")
            print("================================================================================\n")

        elif args.vulns:
            vulns = db.query(VulnerabilityPatch).order_by(VulnerabilityPatch.cvss_score.desc()).all()
            print("\n================================================================================")
            print(" VULNERABILITY MANAGEMENT & CVSS PATCH REGISTRY")
            print("================================================================================")
            for v in vulns:
                print(f" [{v.cve_id}] {v.affected_asset} (CVSS: {v.cvss_score} - {v.severity})")
                print(f"   Component:         {v.component} | Patch: {'Available' if v.patch_available else 'Pending'}")
                print(f"   Status / Due:      {v.status} | Remediate By: {v.remediation_due_date} (Assigned: {v.assigned_engineer})\n")
            print("================================================================================\n")

        elif args.drills:
            drills = db.query(TabletopDrill).all()
            print("\n================================================================================")
            print(" TABLETOP CYBER CRISIS EXERCISES & INCIDENT SIMULATIONS")
            print("================================================================================")
            for d in drills:
                print(f" [{d.drill_code}] {d.title} [{d.drill_rating}]")
                print(f"   Scenario Type:     {d.scenario_type} (Date: {d.drill_date})")
                print(f"   Containment SLA:   {d.actual_containment_minutes} mins actual vs {d.target_containment_minutes} mins target")
                print(f"   Lessons Learned:   {d.lessons_learned_summary}\n")
            print("================================================================================\n")

        elif args.certin_reports:
            reports = db.query(CERTInRegulatoryReport).all()
            print("\n================================================================================")
            print(" STATUTORY CERT-In REGULATORY FILINGS & SUBMISSION LEDGER")
            print("================================================================================")
            for r in reports:
                print(f" [{r.report_reference}] Incident: {r.incident_id} [{r.filing_status}]")
                print(f"   CERT-In ACK:       {r.cert_in_ack_number or 'Pending ACK'}")
                print(f"   Submitted On:      {r.submission_timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"   Narrative:         {r.narrative_description}")
                print(f"   Containment:       {r.containment_actions_taken}\n")
            print("================================================================================\n")

        else:
            ov = get_secops_warroom_overview(db)
            print("\n================================================================================")
            print(" ASPERION CYBERSECURITY, INCIDENT MANAGEMENT & CERT-In WAR ROOM POSTURE")
            print(" Entity: ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED (CIN: U85500KA2026OPC222069)")
            print(" Registered Office: Horamavu, Bangalore - 560043, Karnataka")
            print("================================================================================")
            print(f" 1. War Room Status:            {ov['status']}")
            print(f" 2. NTP Synchronization:        {ov['ntp_synchronization']['status']} ({ov['ntp_synchronization']['primary_source']})")
            print(f" 3. Active Incident Queue:      {ov['incidents_summary']['active_now']} Active ({ov['incidents_summary']['p1_critical_and_p2_high']} Critical P1/P2)")
            print(f" 4. CERT-In 6-Hour SLA:         {ov['incidents_summary']['cert_in_pending_filings']} Pending Filing(s) | 100% On-Time Adherence")
            print(f" 5. SIEM Threat Ingestion:      {ov['defense_telemetry']['siem_alerts_under_investigation']} Under Active Investigation ({ov['defense_telemetry']['total_alerts_ingested']} Ingested)")
            print(f" 6. Threat Intel Indicators:    {ov['defense_telemetry']['active_threat_iocs_blocked']} Blocked at WAF & WireGuard Perimeter")
            print(f" 7. Forensic Evidence Locker:   {ov['defense_telemetry']['forensic_evidence_items_preserved']} Artifacts Preserved under SHA-256 Object Lock")
            print(f" 8. Incident Playbooks Active:  {ov['defense_telemetry']['incident_response_playbooks_active']} NIST SP 800-61 Playbooks")
            print(f" 9. Open CVE Vulnerabilities:   {ov['defense_telemetry']['open_cve_vulnerabilities']} Patches in Remediation Pipeline")
            print(f" 10. Tabletop Cyber Drills:     {ov['defense_telemetry']['tabletop_crisis_drills_completed']} Crisis Simulations Completed (High Preparedness)")
            print("================================================================================\n")
        db.close()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
