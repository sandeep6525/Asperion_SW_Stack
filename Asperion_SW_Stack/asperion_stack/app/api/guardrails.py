"""
Asperion Enterprise OS - Guardrails, Architecture Blueprints, Flowcharts & Documents API Router
Pillar 15 & Cross-Pillar Enterprise Governance, ISO 27001 / CMMI / TOGAF / MSMED / DPDP Guardrails
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.guardrails import GuardrailRule, GuardrailExecutionLog, ArchitectureBlueprint
from app.schemas.guardrails import (
    GuardrailRuleCreate, GuardrailRuleOut,
    GuardrailExecutionLogOut,
    ArchitectureBlueprintCreate, ArchitectureBlueprintOut,
    FlowchartDefinitionOut, FlowchartStep
)
from app.engines.guardrails_engine import evaluate_all_enterprise_guardrails

router = APIRouter(prefix="/guardrails", tags=["Guardrails & Architecture"])

# --- ENTERPRISE FLOWCHARTS REPOSITORY (MERMAID + STRUCTURED STEPS) ---
ENTERPRISE_FLOWCHARTS: List[Dict[str, Any]] = [
    {
        "flowchart_id": "FC-FIN-001",
        "title": "FinOps 3-Way Matching & Statutory Payout Governance",
        "pillar": "Procurement & Finance",
        "regulatory_standard": "Companies Act 2013 / Internal Financial Controls (IFC)",
        "active_guardrails": ["GRD-FIN-001", "GRD-MSME-002", "GRD-DOA-006"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[Department PR Created] -->|DOA Approval| B{Spend > 1 Lakh?}\n"
            "    B -- Yes --> C[Sole Director Approval]\n"
            "    B -- No --> D[HOD Approval]\n"
            "    C --> E[Purchase Order Dispatched]\n"
            "    D --> E\n"
            "    E --> F[Vendor Ships Goods / Services]\n"
            "    F --> G[Warehouse QC Inspection & GRN]\n"
            "    G --> H[Vendor Submits Tax Invoice / AP Bill]\n"
            "    H --> I{3-Way Matching Engine}\n"
            "    I -- Discrepancy > 0% --> J[DISCREPANCY HOLD: Guardrail GRD-FIN-001]\n"
            "    I -- Perfect Match --> K[Auto-Calculate TDS & Section 194Q / 194C]\n"
            "    K --> L{MSME Vendor?}\n"
            "    L -- Yes --> M[45-Day Priority Queue: Guardrail GRD-MSME-002]\n"
            "    L -- No --> N[Standard Net 30/60 Days]\n"
            "    M --> O[HDFC / ICICI Corporate Open Banking Disbursal Batch]\n"
            "    N --> O\n"
            "    O --> P[Statutory Settlement Complete & Ledger Entry]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "Requisition & DOA Check",
                "actor": "Initiating Department & HOD",
                "input_data": "Item details, BoM, cost center, projected budget",
                "decision_or_processing": "Evaluate financial threshold: <= 1 Lakh HOD approval; > 1 Lakh escalates to Director",
                "guardrail_enforced": "GRD-DOA-006 (Financial Delegation of Authority)",
                "output_state": "Approved PR"
            },
            {
                "step_number": 2,
                "title": "Goods Receipt & QC Verification",
                "actor": "Warehouse Officer / QA Lead",
                "input_data": "Delivery Challan, physical items, serial numbers",
                "decision_or_processing": "Inspect physical goods, log accepted vs rejected quantities",
                "guardrail_enforced": "Quality Inspection Pass Threshold >= 98%",
                "output_state": "Goods Received Note (GRN) with QA Stamp"
            },
            {
                "step_number": 3,
                "title": "Autonomous 3-Way Match Validation",
                "actor": "Autonomous FinOps Engine",
                "input_data": "PO, GRN, and Vendor AP Tax Bill",
                "decision_or_processing": "Line-by-line validation of unit price, quantity received, GST rate, and HSN/SAC code",
                "guardrail_enforced": "GRD-FIN-001 (Zero Tolerance PO-GRN-Invoice Match)",
                "output_state": "Matched / Discrepancy Hold"
            },
            {
                "step_number": 4,
                "title": "Statutory Deduction & MSME SLA Prioritization",
                "actor": "Finance Accounts Payable System",
                "input_data": "Vendor MSME status, PAN, TDS Section (194C/194J/194Q)",
                "decision_or_processing": "Compute net payable; prioritize payment date within 45 days if MSME registered",
                "guardrail_enforced": "GRD-MSME-002 (MSMED Act 2006 45-Day Payment Rule)",
                "output_state": "Approved for Corporate Banking Batch Disbursal"
            }
        ]
    },
    {
        "flowchart_id": "FC-HRMS-002",
        "title": "Smart Geofenced Attendance & Self-Healing Anomaly Governance",
        "pillar": "Human Resources & Payroll",
        "regulatory_standard": "Karnataka Shops & Commercial Establishments Act / DPDP Act 2023",
        "active_guardrails": ["GRD-HRMS-004", "GRD-DPDP-003"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[Employee Mobile App Punch / WhatsApp Webhook] --> B[Capture GPS Coordinates & Facial Snapshot]\n"
            "    B --> C{Haversine Distance Check}\n"
            "    C -- Distance > 250m --> D[PUNCH REJECTED: Outside Geofence]\n"
            "    C -- Distance <= 250m --> E{Facial Recognition Liveness}\n"
            "    E -- Confidence < 85% --> F[Liveness Failed: Flag for Supervisor Review]\n"
            "    E -- Confidence >= 85% --> G[Punch Verified & Recorded in Ledger]\n"
            "    G --> H[Check Multi-Punch & Late Arrival Shifts]\n"
            "    H --> I{Anomaly Detected?}\n"
            "    I -- Missed Punch / GPS Jitter --> J[Self-Healing ML Engine Evaluates Historical Context]\n"
            "    J --> K[Auto-Regularize with Reason Code]\n"
            "    I -- Clean Shift --> L[Calculate Overtime, Shift Allowance & LOP]\n"
            "    K --> L\n"
            "    L --> M[Sync with Real-Time Salary Statement Engine]\n"
            "    M --> N[Push Instant WhatsApp & Push Notification Confirmation]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "Multi-Channel Punch Ingestion",
                "actor": "Employee Mobile / WhatsApp Bot",
                "input_data": "Latitude, Longitude, Front camera selfie, Device timestamp",
                "decision_or_processing": "Calculate distance from HQ (Horamavu, Bangalore) using Haversine formula",
                "guardrail_enforced": "GRD-HRMS-004 (250m Office Perimeter Geofence)",
                "output_state": "Geofence Validated / Rejected"
            },
            {
                "step_number": 2,
                "title": "Biometric Liveness Verification",
                "actor": "Facial Recognition Neural Model",
                "input_data": "High-resolution face crop & facial landmark vector",
                "decision_or_processing": "Validate blink/micro-motion liveness and compare embedding with HR profile",
                "guardrail_enforced": "Biometric Confidence Score >= 85.0%",
                "output_state": "Verified Biometric Identity"
            },
            {
                "step_number": 3,
                "title": "Autonomous Anomaly Detection & Self-Healing",
                "actor": "HRMS Auto-Fix Daemon",
                "input_data": "Punch times, shift schedule, badge swipes, calendar events",
                "decision_or_processing": "Identify single-punch anomalies, check calendar invites, auto-apply regularization rules",
                "guardrail_enforced": "Self-Healing Attendance Regularization Rules",
                "output_state": "Auto-Healed / Escalated to HOD"
            },
            {
                "step_number": 4,
                "title": "Instant Payroll Accrual & Notification",
                "actor": "Payroll & Messaging Engine",
                "input_data": "Effective work hours, shift differential",
                "decision_or_processing": "Compute daily pro-rata earnings, professional tax brackets, and dispatch WhatsApp alert",
                "guardrail_enforced": "Karnataka Professional Tax & Minimum Wages Act",
                "output_state": "Salary Statement Synced & WhatsApp Alert Sent"
            }
        ]
    },
    {
        "flowchart_id": "FC-SDLC-003",
        "title": "7-Stage DevSecOps & Enterprise SDLC Quality Gates",
        "pillar": "Software Engineering & DevSecOps",
        "regulatory_standard": "ISO/IEC 27001 / CMMI Level 5 / OWASP Top 10",
        "active_guardrails": ["GRD-SDLC-005", "GRD-SECR-008"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[Product PRD / SRS Approved] --> B[Architecture Decision Record ADR Logged]\n"
            "    B --> C[Feature Branch Created: git checkout -b feat/...]\n"
            "    C --> D[Developer Pull Request Submitted]\n"
            "    D --> E{DevSecOps CI/CD Automation Pipeline}\n"
            "    E --> F[Secret Scanning: Detect High-Entropy Keys & Tokens]\n"
            "    F --> G[Static Application Security Testing SAST]\n"
            "    G --> H[Software Composition Analysis SCA for Vulnerable Dependencies]\n"
            "    H --> I[Automated Unit & Integration Test Suite]\n"
            "    I --> J{Quality Gate Guardrail Check}\n"
            "    J -- SAST CVE > 0 OR Coverage < 90% --> K[PIPELINE BLOCKED: Guardrail GRD-SDLC-005]\n"
            "    J -- All Checks Passed --> L[Peer Review Approval & CAB Signoff]\n"
            "    L --> M[Automated Canary Deployment to Kubernetes Staging]\n"
            "    M --> N[Synthetics & Smoke Tests Passed]\n"
            "    N --> O[Zero-Downtime Blue/Green Production Rollout]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "SRS, RTM & Architectural Baseline",
                "actor": "Lead Architect & Product Owner",
                "input_data": "Business requirements, traceability matrix, ADR documents",
                "decision_or_processing": "Map requirements to technical components and record architectural decisions",
                "guardrail_enforced": "Traceability Index = 100%",
                "output_state": "Approved Architecture Baseline"
            },
            {
                "step_number": 2,
                "title": "Automated Secret & Credential Detection",
                "actor": "Trufflehog / GitGuardian Hook",
                "input_data": "Git commit diffs across all modified files",
                "decision_or_processing": "Entropy analysis and regex scanning for API keys, passwords, and private certs",
                "guardrail_enforced": "GRD-SECR-008 (Zero Secret Leakage)",
                "output_state": "Clean Commit / Pre-Push Block"
            },
            {
                "step_number": 3,
                "title": "SAST, SCA & Automated Test Suite",
                "actor": "GitLab CI / GitHub Actions Runner",
                "input_data": "Codebase snapshot, package dependencies",
                "decision_or_processing": "Execute Bandit, SonarQube, Snyk, and Pytest test runner with coverage evaluation",
                "guardrail_enforced": "GRD-SDLC-005 (0 Vulnerabilities, >= 90% Test Coverage)",
                "output_state": "Quality Gate Passed / Blocked"
            },
            {
                "step_number": 4,
                "title": "Change Advisory Board & Production Rollout",
                "actor": "Release Manager / CAB",
                "input_data": "Test report, rollback plan, deployment manifest",
                "decision_or_processing": "Final CAB signoff followed by Blue/Green or Canary Kubernetes cluster rollout",
                "guardrail_enforced": "ISO 27001 Change Management & Zero Downtime SLA",
                "output_state": "Live Production Deployment"
            }
        ]
    },
    {
        "flowchart_id": "FC-SEC-004",
        "title": "CERT-In 6-Hour SLA Cyber Incident Escalation & Response",
        "pillar": "Cybersecurity & Incident Response",
        "regulatory_standard": "CERT-In Cyber Security Directions (Sec 70B IT Act 2000)",
        "active_guardrails": ["GRD-CERT-007"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[SIEM / EDR Alert / Anomaly Detection] --> B[Automated Triage & Severity Categorization]\n"
            "    B --> C{Severity == P1-Critical?}\n"
            "    C -- Yes --> D[START CERT-In 6-HOUR COUNTDOWN TIMER]\n"
            "    D --> E[Isolate Affected Host / Revoke Compromised Tokens]\n"
            "    E --> F[War Room Convened: CISO, Sole Director, Legal]\n"
            "    F --> G[Extract Forensic Evidence & Packet Captures]\n"
            "    G --> H[Prepare Incident Report Template per CERT-In Guidelines]\n"
            "    H --> I{Elapsed Time <= 6 Hours?}\n"
            "    I -- Yes --> J[Dispatch Official Notification to incident@cert-in.org.in]\n"
            "    I -- Exceeded --> K[GUARD VIOLATION: GRD-CERT-007 Regulatory Breach Logged]\n"
            "    J --> L[Conduct Root Cause Analysis RCA & Patch Vulnerability]\n"
            "    L --> M[Post-Mortem Published & Guardrail Engine Updated]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "Threat Ingestion & Triage",
                "actor": "SOC Analyst / Automated SIEM",
                "input_data": "Telemetry logs, auth failures, IDS signatures",
                "decision_or_processing": "Classify incident severity: P1-Critical vs P2/P3",
                "guardrail_enforced": "Automated Triage Rules",
                "output_state": "Incident Classified"
            },
            {
                "step_number": 2,
                "title": "CERT-In Timer Initialization",
                "actor": "Autonomous SecOps Daemon",
                "input_data": "Incident timestamp and severity classification",
                "decision_or_processing": "Lock 6-hour SLA clock and initialize regulatory reporting protocol",
                "guardrail_enforced": "GRD-CERT-007 (6-Hour Statutory SLA)",
                "output_state": "Active War Room & Escalation"
            },
            {
                "step_number": 3,
                "title": "Containment & Forensics",
                "actor": "Incident Response Team",
                "input_data": "Network flows, memory dumps, firewall logs",
                "decision_or_processing": "Isolate affected hosts, rotate API tokens, capture immutable forensic evidence",
                "guardrail_enforced": "Evidence Integrity Chain of Custody",
                "output_state": "Threat Contained"
            },
            {
                "step_number": 4,
                "title": "Regulatory Dispatch & RCA",
                "actor": "CISO / Sole Director",
                "input_data": "Forensic summary, impact assessment",
                "decision_or_processing": "Dispatch encrypted report to CERT-In and publish internal RCA",
                "guardrail_enforced": "CERT-In Mandatory Reporting Directive",
                "output_state": "Statutory Compliance Achieved"
            }
        ]
    },
    {
        "flowchart_id": "FC-PMO-005",
        "title": "5-Stage-Gate PMO Governance & Delivery Lifecycle",
        "pillar": "PMO & Project Delivery",
        "regulatory_standard": "PMI PMBOK 7th Ed / CMMI-DEV v2.0 Maturity Level 3",
        "active_guardrails": ["GRD-DOA-006", "GRD-SDLC-005"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[Client Request / Business Case] --> B[Gate 1: Opportunity Qualification & Intake]\n"
            "    B --> C{Gate 1 Approved?}\n"
            "    C -- Yes --> D[Gate 2: Project Charter & WBS Decomposition]\n"
            "    D --> E[Resource Capacity Allocation & Budget Approval]\n"
            "    E --> F[Gate 3: Execution Kickoff & Sprint Cycles]\n"
            "    F --> G[Milestone Tracking, EVM & Weekly Status Reports]\n"
            "    G --> H[Gate 4: UAT Testing & Client Signoff]\n"
            "    H --> I{UAT Defect Free?}\n"
            "    I -- Yes --> J[Gate 5: Handover, Billing Clearance & Project Closure]\n"
            "    J --> K[Lessons Learned Documented & Archived in Document Vault]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "Gate 1: Project Intake & Feasibility",
                "actor": "Delivery Head / PMO Lead",
                "input_data": "Project proposal, estimated ROI, high-level scope",
                "decision_or_processing": "Feasibility study, margin analysis (>25% gross margin threshold)",
                "guardrail_enforced": "Commercial Feasibility Gate",
                "output_state": "Charter Drafting Authorized"
            },
            {
                "step_number": 2,
                "title": "Gate 2: Charter & WBS Approval",
                "actor": "PMO Director / Client Sponsor",
                "input_data": "Signed Scope of Work (SOW), Resource Matrix, Work Breakdown Structure",
                "decision_or_processing": "Approve resource commitments and project schedule",
                "guardrail_enforced": "GRD-DOA-006 (Executive Sponsorship)",
                "output_state": "Project Charter Signed"
            },
            {
                "step_number": 3,
                "title": "Gate 3: Execution & EVM Monitoring",
                "actor": "Project Manager & Delivery Squad",
                "input_data": "Jira sprints, time logs, burn-down charts",
                "decision_or_processing": "Weekly Earned Value Management (EVM): CPI >= 0.95, SPI >= 0.95",
                "guardrail_enforced": "PMO Health Metrics Thresholds",
                "output_state": "Sprint Deliverables Ready for UAT"
            },
            {
                "step_number": 4,
                "title": "Gate 4 & 5: UAT Signoff & Contractual Closure",
                "actor": "Client Stakeholders & Finance",
                "input_data": "UAT acceptance test results, final deliverable checklist",
                "decision_or_processing": "Obtain formal client acceptance and trigger final invoice billing",
                "guardrail_enforced": "Defect-Free Acceptance Gate",
                "output_state": "Formal Closure Certificate"
            }
        ]
    },
    {
        "flowchart_id": "FC-PROC-006",
        "title": "Vendor Onboarding, Due Diligence & DPDP Compliance",
        "pillar": "Strategic Sourcing & Vendor Management",
        "regulatory_standard": "Digital Personal Data Protection Act 2023 / MSMED Act 2006",
        "active_guardrails": ["GRD-DPDP-003", "GRD-MSME-002"],
        "mermaid_diagram": (
            "graph TD\n"
            "    A[Vendor Self-Registration Portal] --> B[Submit GSTIN, PAN, Bank Details & MSME Udyam]\n"
            "    B --> C[Automated GST Portal & MCA API Verification]\n"
            "    C --> D{Data Handling / Criticality Tier?}\n"
            "    D -- Tier 1 PII / Mission Critical --> E[DPDP Data Processing Agreement DPA Required]\n"
            "    D -- Tier 2/3 Standard Goods --> F[Standard Commercial Agreement]\n"
            "    E --> G{DPA Signed & Security Audit Passed?}\n"
            "    G -- No --> H[ONBOARDING SUSPENDED: Guardrail GRD-DPDP-003]\n"
            "    G -- Yes --> I[Vendor Approved & Bank Account Active]\n"
            "    F --> I\n"
            "    I --> J[Continuous Quarterly Scorecard & MSMED 45-Day Payment Priority]"
        ),
        "steps": [
            {
                "step_number": 1,
                "title": "Statutory Verification & Tax Validation",
                "actor": "Procurement Officer & API Engine",
                "input_data": "GSTIN, PAN, Bank IFSC, Udyam certificate",
                "decision_or_processing": "Verify active status on GST portal and MCA database",
                "guardrail_enforced": "Statutory Tax Compliance Check",
                "output_state": "Verified Vendor Profile"
            },
            {
                "step_number": 2,
                "title": "Criticality Tiering & DPDP Evaluation",
                "actor": "Information Security Officer / Legal",
                "input_data": "Vendor service scope, data access category",
                "decision_or_processing": "Classify into Tier 1/2/3; enforce DPA for data processors",
                "guardrail_enforced": "GRD-DPDP-003 (Mandatory DPA for Tier 1 Vendors)",
                "output_state": "DPA Executed & Approved"
            },
            {
                "step_number": 3,
                "title": "Procurement Authorization",
                "actor": "Chief Sourcing Officer",
                "input_data": "Signed master contract, SLA metrics",
                "decision_or_processing": "Activate vendor in ERP for PO issuance and bidding",
                "guardrail_enforced": "Supplier Risk Threshold <= 30",
                "output_state": "Active Approved Vendor"
            }
        ]
    }
]

# --- ENTERPRISE TECHNICAL ARCHITECTURE DOCUMENTS SPECIFICATION ---
ENTERPRISE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "doc_id": "DOC-ARCH-001",
        "title": "Asperion Enterprise OS End-to-End System Architecture Specification",
        "category": "System Architecture & Engineering",
        "version": "v4.2.0-LTS",
        "published_date": "2026-06-15",
        "classification": "CONFIDENTIAL - INTERNAL USE",
        "summary": "Exhaustive architectural specification of Asperion Enterprise OS detailing the 3-tier decoupled micro-modular architecture, event bus, SQLite WAL transactional layer, and cross-pillar orchestration.",
        "key_sections": [
            "1. Architectural Principles & Zero-Trust Posture",
            "2. Data Persistence Layer (SQLite WAL Mode, Thread-Safe Concurrency & Schema Migrations)",
            "3. Autonomous Engine Layer (FinOps 3-Way Match, Attendance Self-Healing, Guardrails)",
            "4. Multi-Tenant Role-Based Access Control (RBAC) & Stakeholder Portal Isolation",
            "5. Open Banking APIs & Real-Time WhatsApp Webhook Interfaces",
            "6. High Availability, Disaster Recovery & Continuous Backup Blueprint"
        ],
        "compliance_standards": ["ISO/IEC 27001:2022", "TOGAF Standard 10th Ed", "CMMI-DEV v2.0 ML3"]
    },
    {
        "doc_id": "DOC-SEC-002",
        "title": "Asperion Information Security & CERT-In Incident Response Manual",
        "category": "Cybersecurity & Governance",
        "version": "v3.1.0",
        "published_date": "2026-06-20",
        "classification": "RESTRICTED",
        "summary": "Mandatory standard operating procedures for detecting, triaging, isolating, and reporting cybersecurity incidents within the statutory 6-hour CERT-In deadline as per Section 70B of IT Act 2000.",
        "key_sections": [
            "1. Statutory Reporting Scope & Incident Severity Matrix (P1-Critical to P3-Low)",
            "2. 6-Hour Emergency Response Protocol & War Room Activation Workflow",
            "3. Cryptographic Token Rotation & Zero Secret Exposure Mandate (GRD-SECR-008)",
            "4. Forensic Artifact Collection & Chain of Custody Guidelines",
            "5. CERT-In Incident Report Dispatch Format & Escalation Pathways"
        ],
        "compliance_standards": ["CERT-In Cybersecurity Directions 2022", "IT Act 2000", "ISO/IEC 27001 Annex A"]
    },
    {
        "doc_id": "DOC-DOA-003",
        "title": "Asperion Delegation of Authority (DOA) & Statutory Procurement Policy",
        "category": "Corporate Governance & Sourcing",
        "version": "v2.5.0",
        "published_date": "2026-06-10",
        "classification": "INTERNAL",
        "summary": "Defines corporate financial spend limits, sole-director signoff thresholds, MSMED Act 45-day payment enforcement, and Digital Personal Data Protection Act (DPDP) vendor compliance rules.",
        "key_sections": [
            "1. Financial Authorization Matrix: Department Leads, HODs, and Sole Director Limits",
            "2. Strategic Sourcing Protocol: RFP, Competitive Bidding & Vendor Due Diligence",
            "3. Mandatory MSMED Act 2006 Statutory Protections & 45-Day Priority Clearance",
            "4. DPDP Act 2023 Data Processor Agreements (DPA) Requirements for Vendors",
            "5. Zero-Tolerance 3-Way Matching FinOps Rulebook (GRD-FIN-001)"
        ],
        "compliance_standards": ["Companies Act 2013", "MSMED Act 2006", "DPDP Act 2023"]
    },
    {
        "doc_id": "DOC-SDLC-004",
        "title": "Asperion Secure SDLC, Quality Engineering & CMMI Governance Manual",
        "category": "Engineering & DevOps",
        "version": "v5.0.0",
        "published_date": "2026-06-18",
        "classification": "INTERNAL",
        "summary": "Comprehensive 7-stage software development lifecycle guidelines incorporating SRS/RTM traceability, mandatory SAST/SCA security scans, 90% unit test coverage thresholds, and CAB deployment gates.",
        "key_sections": [
            "1. Stage 1 to Stage 7 SDLC Lifecycle & Gates Specification",
            "2. Architecture Decision Records (ADR) Process & Versioning",
            "3. Pre-Commit Hooks & Continuous Secret Scanning with TruffleHog",
            "4. Mandatory DevSecOps Quality Gate: 0 CVEs & >= 90% Automated Coverage (GRD-SDLC-005)",
            "5. Change Advisory Board (CAB) Audit Trail & Automated Canary Deployments"
        ],
        "compliance_standards": ["CMMI-DEV v2.0 ML5", "OWASP ASVS v4.0", "IEEE 12207"]
    }
]

# --- API ENDPOINTS ---

@router.get("/overview", response_model=Dict[str, Any])
def get_guardrails_overview(db: Session = Depends(get_db)):
    """
    Returns high-level telemetry and compliance summary for executive dashboards.
    """
    rules = db.query(GuardrailRule).all()
    active_count = sum(1 for r in rules if r.is_active)
    total_evals = sum(r.total_evaluations for r in rules)
    total_passed = sum(r.total_passed for r in rules)
    total_blocked = sum(r.total_blocked for r in rules)
    total_healed = sum(r.total_auto_healed for r in rules)
    
    compliance_score = round((total_passed / max(1, total_evals)) * 100.0, 1) if total_evals > 0 else 100.0

    recent_logs = db.query(GuardrailExecutionLog).order_by(GuardrailExecutionLog.evaluated_at.desc()).limit(10).all()

    return {
        "status": "HEALTHY" if total_blocked == 0 else "INTERVENTIONS_ACTIVE",
        "total_rules": len(rules),
        "active_rules": active_count,
        "total_evaluations": total_evals,
        "total_passed": total_passed,
        "total_blocked": total_blocked,
        "total_auto_healed": total_healed,
        "compliance_score_pct": compliance_score,
        "recent_interventions": [
            {
                "execution_id": l.execution_id,
                "rule_code": l.rule_code,
                "module": l.module,
                "entity": l.entity_reference,
                "result": l.evaluation_result,
                "action": l.action_taken,
                "evaluated_at": l.evaluated_at.strftime("%Y-%m-%d %H:%M:%S")
            } for l in recent_logs
        ],
        "supported_frameworks": [
            "Internal Financial Controls (IFC)",
            "MSMED Act 2006 (Section 15/16)",
            "Digital Personal Data Protection (DPDP) Act 2023",
            "CERT-In Cyber Incident Reporting 2022",
            "ISO/IEC 27001:2022 ISMS",
            "CMMI-DEV v2.0 Maturity Level 5"
        ]
    }

@router.get("/rules", response_model=List[GuardrailRuleOut])
def list_guardrail_rules(db: Session = Depends(get_db)):
    """List all configured enterprise guardrail policies."""
    return db.query(GuardrailRule).order_by(GuardrailRule.rule_code.asc()).all()

@router.post("/rules", response_model=GuardrailRuleOut, status_code=status.HTTP_201_CREATED)
def create_guardrail_rule(payload: GuardrailRuleCreate, db: Session = Depends(get_db)):
    """Register a new enterprise guardrail policy."""
    existing = db.query(GuardrailRule).filter(GuardrailRule.rule_code == payload.rule_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Rule with code {payload.rule_code} already exists.")
    
    rule = GuardrailRule(**payload.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.post("/evaluate", response_model=Dict[str, Any])
def run_live_guardrails_evaluation(db: Session = Depends(get_db)):
    """
    Triggers an on-demand real-time evaluation across all enterprise guardrails.
    Evaluates live database state against FinOps, MSMED, DPDP, Attendance, SDLC, DOA, and CERT-In rules.
    """
    return evaluate_all_enterprise_guardrails(db)

@router.get("/logs", response_model=List[GuardrailExecutionLogOut])
def list_guardrail_logs(
    limit: int = Query(50, ge=1, le=200),
    result_filter: Optional[str] = Query(None, description="Filter by result (PASSED, BLOCKED, AUTO_HEALED)"),
    db: Session = Depends(get_db)
):
    """Retrieve execution and enforcement audit logs."""
    q = db.query(GuardrailExecutionLog)
    if result_filter:
        q = q.filter(GuardrailExecutionLog.evaluation_result == result_filter)
    return q.order_by(GuardrailExecutionLog.evaluated_at.desc()).limit(limit).all()

@router.get("/blueprints", response_model=List[ArchitectureBlueprintOut])
def list_architecture_blueprints(db: Session = Depends(get_db)):
    """List all system architecture blueprints and Mermaid visual schemas."""
    return db.query(ArchitectureBlueprint).order_by(ArchitectureBlueprint.blueprint_code.asc()).all()

@router.get("/flowcharts", response_model=List[FlowchartDefinitionOut])
def list_enterprise_flowcharts():
    """Retrieve all standard enterprise governance flowcharts with Mermaid definitions and step data."""
    return ENTERPRISE_FLOWCHARTS

@router.get("/documents", response_model=List[Dict[str, Any]])
def list_technical_documents():
    """Retrieve the enterprise repository of technical architecture, DOA, and regulatory documents."""
    return ENTERPRISE_DOCUMENTS
