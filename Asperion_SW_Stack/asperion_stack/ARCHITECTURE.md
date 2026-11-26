<p align="center">
  <img src="app/static/img/logo.png" width="130" height="130" alt="Asperion Logo" style="border-radius: 50%;">
</p>

# Asperion Enterprise Operating System - Software Architecture Blueprint (Complete & Comprehensive)

**Company:** ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED  
**CIN:** U85500KA2026OPC222069  
**Registered Office:** Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India  
**Date of Incorporation:** 2026  

---

## 1. System Vision & Architecture Overview

The **Asperion Enterprise Operating System (Asperion OS)** is an integrated, full-stack, modular software platform that translates Asperion Digital Technologies' operational packs, spreadsheets, governance frameworks, and standard operating procedures (SOPs) into an enterprise operating system.

### Architectural Paradigm: Modular Clean Monolith with Domain-Driven Design (DDD)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Asperion Web Dashboard                          │
│        (HTML5, Tailwind CSS, Responsive SPA, Chart.js, Vanilla JS)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST / JSON
┌───────────────────────────────────▼────────────────────────────────────┐
│                       FastAPI Application Gateway                      │
│     (AsyncIO, JWT / RBAC Authentication, CORS, OpenAPI Documentation)  │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────────┘
       │      │      │      │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
 ┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
 │01 GovOps ││02 LegalOps││03 FinOps ││04 People ││ 05 PMO   ││06 Procure││07 CloudOps││ 08 SecOps │
 │ MCA/ROC  ││ CRM / SOW││ AR/AP/GST││ CTC/HRMS ││ WBS/RAID ││ Vendor/PO││ Asset/IAM││ CERT-In  │
 └────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
      └───────────┴───────────┴───────────┴─────┬─────┴───────────┴───────────┴───────────┘
                                                │
 ┌──────────────────────────────────────────────▼────────────────────────────────────────┐
 │                      Computational & Document Engine Layer                           │
 │  • Statutory CTC Calculator Engine (EPFO / ESIC / Karnataka PT / Gratuity 15/26)      │
 │  • 13-Week Direct Cash Flow Forecasting Engine (Direct Receipts vs Disbursements)     │
 │  • Tax Engine (GST CGST/SGST/IGST, TDS u/s 194C/J/I, 3-Way Matching PO-GRN-Bill)     │
 │  • Monthly Automated Payroll Engine (Gross, Deductions, Bank NEFT batch export)       │
 │  • 70+ HR & Legal Letter Generator (Official Letterheads, Annexures, HTML Previews)   │
 │  • SecOps Triage & CERT-In 6-Hour Countdown Engine (NIST SP 800-61 / CERT-In 2022)   │
 └──────────────────────────────────────────────┬────────────────────────────────────────┘
                                                │
 ┌──────────────────────────────────────────────▼────────────────────────────────────────┐
 │                         Persistence & Database Layer                                  │
 │           SQLAlchemy 2.0 ORM  |  SQLite (Local/Embedded) / PostgreSQL Ready          │
 │                      (58 Enterprise Tables, Foreign Keys, Audit Trail)                 │
 └───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Exhaustive Domain & Functional Capabilities

### Module 01: Corporate Governance & Legal Entity (GovOps)
- **Scope**: Single-Member One Person Company (OPC) corporate records, MCA filings, Director decisions, and Policy registry.
- **Core Entities**:
  - `EntityMaster`: Corporate identification (CIN, PAN, TAN, GSTIN, authorized/paid-up capital, registered office).
  - `BoardResolution`: Formal sole-director member resolutions (bank accounts, borrowings, auditor appointment).
  - `ComplianceCalendarItem`: MCA AOC-4, MGT-7A, Form 24Q, GSTR-1, GSTR-3B statutory deadlines.
  - `PolicyRecord`: Corporate governance policy repository (Code of Conduct, Anti-Bribery, DPDP, POSH).
  - `AuthorityMatrixItem`: Financial and administrative Delegation of Authority (DoA) thresholds.

### Module 02: CRM, Legal Contracting, Deal Desk & Customer Success (LegalOps & Enterprise CRM)
- **Scope**: Enterprise pipeline opportunities, probability-weighted deal desk with discount guards, touchpoint activity logs, post-sale customer account health scoring (0-100), support service desk with automated SLA countdowns (P1-P4), and ISO 31000 Enterprise Risk Management (ERM).
- **Core Entities**:
  - `Prospect`: Lead pipeline tracking (Qualified, Discovery, Proposal Sent, Negotiation, Closed Won).
  - `ClientContract`: Master Services Agreements (MSA), Statements of Work (SOW), Non-Disclosure Agreements (NDA).
  - `ClientOnboardingRecord`: KYC due diligence, PAN/GSTIN verification, credit terms, delivery handover signoff.
  - `LegalRiskObligation`: Contractual warranties, indemnities, IP assignment, SLA commitments.
  - `Opportunity`: Enterprise CRM deals with stage-based auto-probabilities (Prospecting 10%, Discovery 25%, Proposal 50%, Negotiation 75%, Closed Won 100%, Closed Lost 0%), weighted pipeline value, and Deal Desk discount approval guards (>15% discount requires Director authorization).
  - `CRMActivity`: Customer touchpoint interactions (Call, Email, Meeting, Demo, Contract Review) with participant logging and follow-up tracking.
  - `CustomerAccount`: Customer success accounts with ARR/ACV tracking, dedicated Account Executives, and dynamic Health Scores (0-100: Green, Amber, Red).
  - `SupportTicket`: Service desk tickets with priority tiering and automated SLA countdown deadlines (P1: 1h, P2: 4h, P3: 12h, P4: 24h), escalation triggers, and CSAT ratings.
  - `EnterpriseRisk`: ISO 31000 Enterprise Risk Management register calculating $Inherent\ RPN = Severity \times Probability$ and $Residual\ RPN = Post\ Mitigation\ Severity \times Probability$.

### Module 03: Accounts, Finance, Treasury & Tax (FinOps)
- **Scope**: 4-digit Chart of Accounts, General Ledger, Accounts Receivable (AR), Accounts Payable (AP), 13-Week Cash Flow Forecasting, Fixed Assets depreciation.
- **Core Entities**:
  - `AccountMaster`: Standardized 4-digit Chart of Accounts across Assets (1000s), Liabilities (2000s), Equity (3000s), Revenue (4000s), and Expenses (5000s).
  - `Invoice`: Accounts Receivable (AR) invoices with automatic $9\% \text{ CGST} + 9\% \text{ SGST}$ or $18\% \text{ IGST}$ tax calculation.
  - `APBill`: Accounts Payable (AP) vendor bills with automatic Chapter XVII-B TDS deduction (Sections 194C, 194J, 194I).
  - `ExpenseClaim`: Employee travel and remote work reimbursement claims.
  - `BankReconciliationRecord`: Monthly bank statement reconciliation against general ledger.
  - `JournalEntry`: General Ledger double-entry vouchers with debit/credit balancing and cost centers.
  - `BudgetItem`: Annual and YTD budget variance tracking across Product, People, Sales, and Admin.
  - `ProjectPnL`: Direct labor, cloud infrastructure, and subcontractor delivery margins.
  - `FixedAsset`: Companies Act Written Down Value (WDV) asset depreciation schedule (40% for IT equipment).

### Module 04: Human Capital, Payroll & Letter Generator (PeopleOps)
- **Scope**: Recruitment, employee master profiles, statutory CTC calculator, monthly automated payroll execution, 70+ automated lifecycle letters, leave tracking, POSH committee case records, and No-Dues clearance.
- **Core Entities**:
  - `Candidate`: Recruitment pipeline stages (Applied, Technical Cleared, Intent to Offer, Offer Sent).
  - `Employee`: Master employee profiles (UAN, PAN, Aadhaar, ESIC, bank account, IFSC).
  - `SalaryStructure`: Statutory compensation breakup (Basic, HRA, Special Allowance, PF, ESI, PT, Gratuity, Net In-Hand).
  - `PayrollRecord`: Monthly earned salary calculations, statutory deductions, and net pay.
  - `HRLetter`: Master repository of issued official company letters.
  - `LeaveRecord`: Employee leave applications, balances, and manager approval status.
  - `POSHCase`: Internal Committee (IC) case registry and inquiry records under the POSH Act 2013.
  - `SeparationClearance`: Multi-department No Dues signoffs (IT, Finance, Admin, Manager, HR) and F&F settlement.

### Module 05: PMO, Agile & Delivery Operations (DeliveryOps)
- **Scope**: Project charters, milestone tracking, Work Breakdown Structure (WBS), interactive Kanban boards, RACI responsibility matrices, and RAID log governance.
- **Core Entities**:
  - `Project`: Project baseline, client, sponsor, budget, and RAG health status.
  - `Sprint`: Agile sprint planning, sprint goals, committed vs completed story points, and velocity.
  - `WBSTask`: Granular WBS tasks with interactive status transitions (To Do, In Progress, Done).
  - `ProjectMilestone`: Commercial milestone deliverables and payment linkages.
  - `RAIDItem`: Risk, Assumption, Issue, Dependency log with impact, probability, and mitigation plans.
  - `ChangeRequest`: Formal Scope Change Request (CR) governance with cost and schedule impact assessments.
  - `Stakeholder`: Power vs Interest matrix and communication frequency.

### Module 06: Vendor Management & Strategic Sourcing (ProcureOps / CIPS / ISO 20400)
- **Scope**: End-to-end strategic procurement and third-party lifecycle governance aligning with CIPS, ISM, ISO 20400 Sustainable Procurement, MSMED Act 2006 (Section 15 45-day statutory payment rule), DPDP Act 2023, and ISO 27001 A.15 Supplier Relationships.
- **Core Entities & Pillars**:
  - `SourcingCategory`: Category spend architecture, annual budget targets, lead buyers, active preferred vendor caps, and ESG sustainability weights.
  - `Vendor`: Master vendor registry with KYC verification, MSME Udyam classification (`Micro`, `Small`, `Medium`, `Non-MSME`), D-U-N-S numbers, bank details, rating score, and annual spend limits.
  - `PurchaseRequisition`: Departmental spend requests with Delegation of Authority (DOA) approval workflows (`Pending HOD`, `Pending Director Signoff`, `Approved`), urgency levels, and PO conversions.
  - `StrategicSourcingEvent`: e-RFX pipeline (`RFP`, `RFQ`, `RFI`, `Reverse Auction`) with multi-criteria weighted scoring (Technical 40%, Commercial 30%, SecOps 20%, SLA 10%) and automated savings realization tracking against baseline budgets.
  - `VendorBidSubmission`: Granular supplier bids with calculated composite scores, shortlisting logic, and BAFO finalists.
  - `VendorContract`: Contract Lifecycle Management (CLM) tracking Master Services Agreements (MSA), Statements of Work (SOW), SLAs, 30/60/90-day renewal alerts, liability caps, and jurisdiction.
  - `GoodsReceivedNote`: Inward goods/services inspection notes with 3-way match verification (PO $\rightarrow$ GRN $\rightarrow$ AP Bill), warehouse site tracking, and Return-to-Vendor (RTV) credit notes.
  - `VendorScorecard`: Quarterly Business Review (QBR) metrics evaluating Quality, SLA Adherence, Pricing, and Privacy/SecOps into performance tiers (`Strategic Partner`, `Preferred Vendor`, `Satisfactory`, `Under Watch`).
  - `VendorRiskAssessment`: Third-Party Risk Management (TPRM) evaluating data access tiers, DPDP Data Processing Agreements, ISO 27001, SOC 2 Type II attestations, cross-border data transfer, and subprocessor disclosures.
  - `VendorCorrectiveActionPlan`: Corrective and Preventive Action Plans (CAPA) tracking root causes, agreed remediations, and target closure dates for service discrepancies.
  - `RFPComparison`: Legacy 3-quote comparative statements with commercial justifications.

### Module 07: IT, Cloud Infrastructure & IAM Access (CloudOps/ITSM)
- **Scope**: Hardware asset registry, AWS/Cloud accounts, IAM access reviews, passwordless FIDO2 Passkeys, and SSL certificate expiration monitoring.
- **Core Entities**:
  - `ITAsset`: Hardware inventory with serial numbers, BitLocker/FileVault encryption, and EDR antivirus status.
  - `CloudAccount`: AWS, Azure, GCP multi-region subscriptions, budgets, and root account MFA enforcement.
  - `IAMCredential`: System access reviews, privilege levels, and FIDO2 Passkey / MFA posture tracking.
  - `CertificateSecret`: SSL/TLS certificates and API secrets expiration countdown monitor.
  - `ITProvisioningChecklist`: Standardized employee IT onboarding and offboarding security checklist.
  - `BackupDRPlan`: Daily automated snapshots, cross-region replication, RPO/RTO metrics, and restore drill logs.

### Module 08: Cybersecurity, SOC & Incident Response (SecOps)
- **Scope**: Threat triage queue, P1 to P4 severity classification, forensic evidence locker with SHA-256 hashes, CERT-In mandatory notifications, and tabletop drills.
- **Core Entities**:
  - `SecurityIncident`: Incident tracking with automated severity scoring and war-room coordination.
  - `SecurityAlert`: SIEM, GuardDuty, and CloudTrail alert triage queue.
  - `EvidenceItem`: Digital forensics evidence locker with SHA-256 cryptographic checksums and chain of custody.
  - `Playbook`: Containment and eradication playbooks (Ransomware, Cloud Compromise, Phishing).
  - `TabletopDrill`: Simulated cybersecurity incident drills and preparedness ratings.
  - `CERTInRegulatoryReport`: Formal statutory incident notification filing under CERT-In Directions 2022.

---

## 3. Computational Engines & Mechanics

### 1. Indian Statutory CTC Calculator Formula
$$\text{Monthly Basic} = \frac{\text{Annual CTC} \times 0.40}{12}$$
$$\text{Monthly HRA} = \text{Monthly Basic} \times 0.40$$
$$\text{Employer PF} = \min(\text{Monthly Basic}, 15000) \times 0.12 = ₹1,800$$
$$\text{Gratuity Provision} = \text{Monthly Basic} \times \frac{15}{26 \times 12} \approx \text{Basic} \times 4.81\%$$
$$\text{Special Allowance} = \text{Monthly CTC} - (\text{Basic} + \text{HRA} + \text{Employer PF} + \text{Gratuity})$$
$$\text{Gross Salary} = \text{Basic} + \text{HRA} + \text{Special Allowance}$$
$$\text{Net Take-Home} = \text{Gross Salary} - (\text{Employee PF} + \text{Karnataka PT ₹200})$$

### 2. 13-Week Direct Cash Flow Forecasting Methodology
For each week $t \in [1, 13]$:
$$\text{Opening Cash}_t = \text{Closing Cash}_{t-1}$$
$$\text{Inflows}_t = \sum \text{Customer Collections Scheduled}_t$$
$$\text{Outflows}_t = \text{Payroll}_t + \text{Vendor Payments}_t + \text{Statutory Tax Remittances}_t$$
$$\text{Closing Cash}_t = \text{Opening Cash}_t + \text{Inflows}_t - \text{Outflows}_t$$
$$\text{Runway (Months)} = \frac{\text{Starting Cash}}{\text{Average Monthly Net Burn}}$$

### 3. Financial 3-Way Matching Algorithm
$$\Delta_{\text{Qty}} = |\text{Bill Qty} - \text{GRN Accepted Qty}| \le 0.001$$
$$\Delta_{\text{Amount}} = \frac{|\text{Bill Amount} - \text{PO Amount}|}{\text{PO Amount}} \le 2.0\%$$
$$\text{Status} = \begin{cases} \text{Matched (Auto-Approved)}, & \text{if } \Delta_{\text{Qty}} = 0 \text{ and } \Delta_{\text{Amount}} \le 2\% \\ \text{Quantity Mismatch (Hold)}, & \text{if } \Delta_{\text{Qty}} > 0 \\ \text{Price Discrepancy (Hold)}, & \text{otherwise} \end{cases}$$

---

## 4. Master 70+ HR & Legal Letter Catalogue

| Category | Range | Key Document Types |
|---|---|---|
| **01. Recruitment** | `HR-REC-01` to `10` | Interview Invite, Reschedule, Cancellation, Acknowledgement, Selection Intent, Rejection, Reference Check Consent, BGV Authorization, Conditional Offer, Offer Withdrawal. |
| **02. Onboarding** | `HR-ONB-01` to `10` | Formal Offer of Employment, Appointment Letter, Internship Offer, Consultant Retainer, Joining Date Extension, Document Deficiency, Joining Confirmation, Probation Confirmation, Probation Extension, Offer Lapse. |
| **03. Employment** | `HR-ADM-01` to `12` | Salary Revision, Promotion, Role Change, Transfer, Reporting Manager Realignment, Remote/Hybrid Work Approval, Deputation, Employment Verification, Leave Approval, Leave Rejection, Return to Work, Recognition. |
| **04. Employee Relations** | `HR-ER-01` to `12` | Performance Feedback Memo, Performance Improvement Plan (PIP), PIP Closure, Counselling Memo, Show Cause Notice, Suspension Pending Inquiry, Domestic Inquiry, Warning Letter, Final Warning, Grievance Acknowledgement, Grievance Resolution, POSH Complaint Acknowledgement. |
| **05. Separation** | `HR-SEP-01` to `20` | Resignation Acknowledgement, Resignation Acceptance, Notice Buyout, Garden Leave, Unauthorized Absence, Termination (Performance), Termination (Misconduct), Position Redundancy, Probation Discontinuation, Retirement, Contract Expiry, Internship Completion, No Dues Clearance, Full & Final Settlement, Relieving Letter, Experience Certificate, Service Certificate, Asset Return Demand, Confidentiality Reminder, Rehire Reference. |
| **06. Corporate & Legal**| `LEG-01` to `04` | Mutual NDA, Non-Mutual NDA, Master Services Agreement (MSA), Statement of Work (SOW). |

---

## 5. Automated Verification Results
- **Pytest Test Suites**: 22 unit and integration tests covering all computational engines, tax calculations, letter formatting, and API endpoints.
- **Pass Rate**: `22 passed in 1.36s (100% pass rate)`.
- **Database Tables**: 41 relational tables initialized and pre-seeded in `asperion.db`.


---

## 6. Master Document & Knowledge Vault (Module 10)

The Document Vault organizes and streams 266 authentic enterprise assets extracted directly from the company's operational packs into 10 structured categories:

| Category ID | Category Name | Document Count | Formats Available | Description |
|---|---|---|---|---|
| `company_os` | Operating Handbooks & SOPs | 37 | PDF, DOCX | 17 Core Enterprise SOPs, Asset Access, and Company Governance Handbooks |
| `hr_letters` | Statutory HR & Legal Letters | 65 | DOCX | Authentic Word templates (`[[...]]` placeholders) for Recruitment, Onboarding, Separation |
| `finance_templates` | Finance & Accounting Controls | 21 | XLSX, DOCX | Payment vouchers, invoice templates, ledger controls, direct cashflow workbooks |
| `secops_templates` | SecOps & Incident Playbooks | 29 | DOCX, PDF | Incident response checklists, CERT-In mandatory reporting SOPs, tabletop drills |
| `vendor_templates` | Vendor Management & Procurement | 25 | DOCX, XLSX | Due diligence questionnaires, vendor evaluation scorecards, standard SOWs |
| `pmo_templates` | PMO & Project Delivery | 25 | DOCX, XLSX | Project charters, WBS dictionaries, RACI matrix templates, RAID logs |
| `it_cloud_templates` | IT Infrastructure & Cloud Ops | 23 | DOCX, PDF | FIDO2 passkey enforcement guidelines, cloud capacity sizing, IAM policies |
| `legal_crm_templates` | Legal, Risk & CRM Contracts | 27 | DOCX, PDF | Deal desk guidelines, master MSAs, enterprise risk registers, customer terms |
| `founder_strategy` | Strategic Theses & GTM Playbooks| 8 | PDF, DOCX | OPC strategy thesis, target customer profiles, high-velocity sales playbooks |
| `incorporation` | Statutory Incorporation Papers | 6 | PDF, DOCX | MOA, AOA, SPICe+ Part B documents, initial board resolutions |

Each document can be searched, filtered by category and format, and directly downloaded via `/api/v1/vault/download/{category}/{filename}`.

---

## 7. Dynamic Strategy, Capability Matrix & KPI Engine (Module 11)

Asperion OS provides an interactive, live management layer allowing the leadership team to dynamically configure:

1. **Strategic Functions & Review Cadences**: 5 core functions pre-seeded at maturity levels L1–L2 with customizable review cadences (Weekly, Fortnightly, Monthly, Quarterly).
2. **Capability & Capacity Constraints**: Real-time tracking of current vs target operational capacities, identified bottleneck constraints, and allocated mitigation owners.
3. **Enterprise Dynamic KPIs**: Real-time calculation of variances and variance percentages:
   $$\text{Variance} = \text{Actual Value} - \text{Target Value}$$
   $$\text{Variance \%} = \frac{\text{Variance}}{\text{Target Value}} \times 100$$
   Status auto-evaluates across `Achieved`, `On Track`, `At Risk`, and `Critical`.
4. **Founder Thoughts & Strategic Decisions Journal**: Structured logging of architecture notes, policy revisions, founder thoughts, and capital allocation rationales with timestamps, approvers, and linked artifact evidence.
5. **Implementation Roadmap Tracking**: Workstream milestones across Corporate Governance, FinOps, PMO, Cybersecurity, and Talent with real-time percentage progress bars.

---

## 8. Visual Intelligence & Multi-Capable Analytics Hub (Module 12)

The Visual Intelligence Hub provides rich graphical representations, multi-axis spider radar diagrams, time-series projections, and interactive simulation capabilities powered by Chart.js 4.4 and dedicated FastAPI computation engines (`/api/v1/analytics/*`):

### 1. Dynamic Calculated Executive Ratios
- **Net Operating Margin %**:
  $$\text{Margin \%} = \frac{\text{Total Collections} - \text{Total Disbursements}}{\text{Total Collections}} \times 100$$
- **Treasury Cash Runway (Months)**:
  $$\text{Runway} = \frac{\text{Closing Cash Position}}{\text{Average Net Burn Rate}}$$
- **Days Sales Outstanding (DSO)**:
  $$\text{DSO} = \frac{\text{Accounts Receivable (AR)}}{\text{Total Invoiced Revenue}} \times 90 \text{ days}$$
- **Statutory Compliance Index %**:
  $$\text{Compliance Index} = \frac{\text{Filings Completed or Active Within Due Date}}{\text{Total Statutory Calendar Items}} \times 100$$
- **CERT-In Statutory SLA Compliance**:
  100% adherence to the mandatory 6-hour reporting window under India's Cyber Security Directions 2022.

### 2. Specialized Visual Intelligence Dashboards
- **Financial & Treasury Visualizer**: 13-week cashflow time-series (inflows, outflows, closing cash balance area chart), AR vs AP aging analysis bar chart (0-30d, 31-60d, 61-90d, 90d+), and live tax ledger matrix (Output GST, Input Tax Credit, Net GST Payable, TDS 194C/194J).
- **PMO & Delivery Velocity**: Sprint velocity bar chart (committed vs delivered story points across sprints), interactive RAID risk heatmap distribution, and task pipeline status breakdown.
- **Talent, CTC & Payroll Analytics**: Departmental headcount allocation doughnut, compensation pyramid by CTC slabs, and statutory cost burden breakdown.
- **SecOps & CERT-In Defense Radar**: Threat vector distribution polar area chart, CERT-In statutory SLA triage time, and IAM FIDO2 passkey adoption gauge.
- **6-Pillar Organizational Maturity Radar**: Multi-axis radar chart scoring Governance, FinOps, Talent, Delivery, SecOps, and Sales readiness on a 0–100 scale.
- **Dynamic What-If Cash Flow Simulator**: Real-time interactive sandbox with live sliders for Collection Acceleration (+0% to +50%), Expense Optimization (-0% to -30%), and New Monthly Customer Retainers, instantly recomputing the 13-week cash curve, ending liquidity delta, and extended runway without reloading the page.

---

---

## 9. Internal Service Desk & Omni-Channel Alert Bus (Module 13)

### 1. Cross-Departmental Service Desk Engine
- **Scope**: Internal employee ticketing across all 7 operational departments (IT & Cloud Infrastructure, HR & People Operations, Finance & Accounts, Legal & Corporate Compliance, SecOps & Cyber, PMO & Engineering Delivery, Workplace & Administration).
- **Core Entities**:
  - `InternalTicket`: Departmental ticket records with sequential numbering (`IT-TKT-...`, `HR-TKT-...`, `FIN-TKT-...`, `LEG-TKT-...`, `SEC-TKT-...`, `PMO-TKT-...`, `ADM-TKT-...`), category routing, requester profiles, assignee specialists, threaded JSON comments, and 1–5 star CSAT feedback.
  - `SystemNotification`: Omni-channel alert bus dispatching system-wide notifications with 4 severity levels (`CRITICAL`, `WARNING`, `INFO`, `SUCCESS`), targeted role routing (`DIRECTOR`, `FINANCE_HEAD`, `HR_LEAD`, `TECH_LEAD`, `SECOPS_LEAD`, `ALL`), action deep links, and dismiss/read flags.
  - `NotificationRule`: Automated triggers linking operational threshold events (e.g. `TICKET_P1_TRIGGER`, `CERTIN_WAR_ROOM`, `COMPLIANCE_DEADLINE_15D`, `INVOICE_OVERDUE_30D`) to cross-functional notification delivery channels.

### 2. Priority & SLA Matrix
$$\text{Target Resolution Time} = \text{Creation Timestamp} + \Delta t_{\text{Priority}}$$
- **P1 - Critical (2.0 Hours)**: Production outages, VPN/network gateway failures, ransomware alerts, critical payment API blocks.
- **P2 - High (8.0 Hours)**: Developer machine hardware failures, L&D expense claims, contract redline reviews, container build cache issues.
- **P3 - Medium (24.0 Hours)**: Tax slab clarifications, leave carryover disputes, routine office facility adjustments.
- **P4 - Low (48.0 Hours)**: Minor administrative queries and non-blocking documentation requests.

### 3. Automated Scanning Engine (`notification_engine.py`)
Continuously evaluates operational state across all pillars:
- Compliance calendar deadlines within 15 days
- Unpaid AR invoices exceeding 30 days
- Active P1 cybersecurity incidents and CERT-In war room status
- Internal service desk P1 tickets approaching SLA deadlines
- Deal Desk discount approvals requiring Director sign-off ($> 15\%$)

---

---

## 10. Developer Platform Operations & Statutory Tax Deposit Engine (Module 14)

### 1. Corporate Developer Account Governance
- **Scope**: Centralized corporate organizational publishing accounts (Google Play Console, Apple Developer Enterprise, GitHub Organization, Microsoft Entra ID, Meta Business WhatsApp Cloud, AWS Cloud Operations, OpenAI/Gemini AI Enterprise).
- **Core Entities**:
  - `DeveloperPlatformAccount`: Corporate organization ownership, D-U-N-S verification (`65-102-9481`), FIDO2 hardware passkey enforcement, corporate billing profiles, and renewal schedules.
  - `DeveloperEnvironmentSecret`: Production and staging deploy keys, KMS envelope signing credentials, and automated 90-day rotation tracking with SHA-256 fingerprint validation.
  - `StatutoryChallanFiling`: Formal government tax deposit reconciliation (GSTR-3B, GSTR-1, TDS Challan 281, Karnataka PT Form 5, Advance Tax) with 7-digit BSR codes (ICICI Bank `0001234`) and government ARNs/CINs.

### 2. Corporate Recognition & Property Verification Profile
- **DPIIT Startup India Recognition**: `DIPP142089` (Ministry of Commerce & Industry, GoI).
- **MSME Udyam Registration**: `UDYAM-KR-03-0189422` (Ministry of Micro, Small and Medium Enterprises).
- **Global D-U-N-S Number**: `65-102-9481` (Dun & Bradstreet corporate identity).
- **Registered Office Premises**: Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore - 560043. Property Owner No-Objection Certificate (NOC) and BESCOM electricity utility consent granted on record by **Varadi Vijay**.

---

## 11. Smart Attendance, Biometrics & Workforce Mobility Engine (Module 15 / HRMS Extension)

### 1. Multi-Modal Attendance Architecture
- **Scope**: Geofence location verification (Haversine formula against Horamavu Bangalore HQ: `13.035820, 77.653410` + client/WFH zones), AI biometric facial recognition with 3D liveness detection, Meta WhatsApp Cloud API workforce bot, auto-calculation of work hours and breaks, and self-healing anomaly auto-fixing.
- **Core Entities**:
  - `GeofenceZone`: Approved physical geofence perimeters (`GEO-BLR-HQ` Horamavu HQ with 250m radius, `GEO-ECITY-CLT` Electronic City Client Site with 350m radius).
  - `AttendanceRecord`: Multi-modal attendance ledger recording GPS coordinates, facial match confidence % (0.0 to 100.0%), liveness verification, WhatsApp message IDs, auto-calculated hours, and regularized status.
  - `AttendanceAnomalyLog`: Self-healing audit log tracking detected punch anomalies (`MISSING_CLOCK_OUT`, `GEOFENCE_BREACH`, `FACIAL_CONFIDENCE_LOW`) and automated resolutions.
  - `WhatsAppAttendanceSession`: Conversational session state for Meta WhatsApp Cloud API bot interactions (`IN`, `OUT`, `STATUS`).

### 2. Computational Formulas & Mechanics
- **Haversine Geofencing Formula**:
  $$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$
  $$c = 2 \cdot \text{atan2}(\sqrt{a}, \sqrt{1 - a})$$
  $$d = R_{\text{earth}} \cdot c \quad (R_{\text{earth}} = 6,371,000 \text{ meters})$$
- **Work Hours & Status Logic**:
  - Shifts $\ge 5.0$ hours deduct standard $0.75$ hours (45 minutes) for meal breaks.
  - Effective Hours $\ge 7.5$h: `Present` (or `Late Mark` if Clock-In $> 09:30$ AM IST).
  - Effective Hours $\ge 4.0$h and $< 7.5$h: `Half Day`.
  - Effective Hours $< 4.0$h: `Absent`.
  - Clock-Out $< 17:30$ PM IST: Flagged as `Early Exit`.
- **Self-Healing Error Auto-Fixer**:
  - Automatically identifies missing punches from previous dates or shifts $> 10$ hours elapsed without clock-out.
  - Auto-closes shift at standard 18:30 IST, computes work hours, transitions status to `Regularized`, sets `auto_fixed=True`, and writes an immutable audit record in `AttendanceAnomalyLog`.

---

## 12. Autonomous Self-Healing & Background Auto-Update Daemon (Module 16 / System Health)

### 1. Cross-Module Self-Healing Architecture
- **Scope**: Continuously diagnoses operational discrepancies and autonomously fixes anomalies across all enterprise pillars:
  - **Smart Attendance**: Closes missing punches from prior dates or shifts $> 10$ hours, regularizes effective hours, logs audit events.
  - **FinOps & 3-Way Matching**: Auto-reconciles pending PO/GRN vendor bills within tolerance thresholds.
  - **Service Desk Escalations**: Automatically escalates tickets exceeding SLA countdown windows to `P1-Critical`.
  - **Developer Secrets & DevOps**: Identifies expired cryptographic secrets ($> 90$ days) and marks for rotation.
  - **Tax & Compliance**: Auto-reconciles statutory challan filings with government portal CIN/ARNs.
- **Background Daemon (`autoupdate_manager.py`)**:
  - Threaded singleton executor checking the system every 30 seconds.
  - Scans operational thresholds, triggers alerts, runs cross-module auto-healers, updates cumulative healing metrics, and logs immutable records.

---

## 13. Attendance-Synchronized Salary Statements, Statutory PT & Bank Disbursal (Module 17 / Payroll Execution)

### 1. Attendance-Prorated Salary Calculation
- **Payable Days & LOP Calculation**: Inspects daily Smart Attendance records (Present $= 1.0\text{d}$, Half-Day $= 0.5\text{d}$, LOP $= 1.0\text{d}$).
- **Statutory Professional Tax (Karnataka)**:
  $$\text{Monthly Gross} < ₹15,000 \implies \text{PT} = ₹0$$
  $$\text{Monthly Gross} \ge ₹15,000 \implies \text{PT} = ₹200$$
- **Bank NEFT/RTGS Batch Generation**: Exports standard banking batch file mapping beneficiary account numbers, IFSC codes, payment amounts, and corporate transaction remarks.
- **Automated Management Alerts**: Dispatches real-time broadcast notifications to the Director and Finance Head upon payroll statement compilation and disbursal.
- **Statutory HTML Payslips**: Dedicated endpoint `/api/v1/hrms/salary-statement/payslip/{id}` rendering authentic payslips with earnings, deductions, payable days, and bank UTRs.

---

## 14. Dedicated Stakeholder Login Portals & Dashboards (Module 18)

- **Dedicated Stakeholder Portals**:
  - **Employee Self-Service (ESS)**: Clock in/out, view attendance history, download payslips, submit leaves, and log IT/HR service desk tickets.
  - **Retainer Client Portal**: Track contracted project health, milestone approvals, sprint burndown, and log client support issues.
  - **Hardware & Cloud Vendor Portal**: Track POs, submit invoices, monitor payment status, and review SLA commitments.
  - **Executive & Board Persona**: High-level governance, strategic radar, cashflow simulations, ERM risk matrix, and statutory filing records.

---

## 15. Globally Acknowledged PMO & Delivery Operations (Module 19 / PMBOK, PRINCE2, CMMI-DEV, ISO 21500)

- **Stage-Gate 1: Project Intake & Business Case**: Systematic scoring across strategic fit, expected ROI, and budget approval (`ProjectIntake`).
- **Stage-Gate 2: Project Charter Baseline & Scope Lock**: In-scope/out-of-scope boundaries, assumptions, constraints, and baseline lock (`ProjectCharter`).
- **Stage-Gate 3: SteerCo Action & Decision Registers**: Bi-weekly SteerCo minutes, action items, ownership, due dates, and architecture decisions (`ActionDecisionItem`).
- **Stage-Gate 4: Resource Capacity & Skills Allocation**: Role-based hours planning, utilization %, variance analysis, and burnout mitigation (`CapacityPlanItem`).
- **Stage-Gate 5: Quality & Client UAT Acceptance Sign-Offs**: Formal test execution, pass/fail status, client sign-off, and defect clearance (`QualityUATItem`).
- **Stage-Gate 6: Project Closure, Lessons Learned & Handover**: Formal delivery retrospective, commercial closure, and organizational process assets (`ProjectClosureItem`).

---

## 16. Comprehensive SDLC & DevSecOps Engineering Cockpit (Module 20 / ISO 27001, IEEE 1044, ISO 29148, OWASP SAMM)

- **Stage 1: Software Requirements Specification (SRS) & Traceability Matrix (RTM)**:
  - Functional, Non-Functional (NFR), Security (DevSecOps), Performance, and Compliance specifications (`SDLCRequirement`).
  - MoSCoW prioritization (`Must Have`, `Should Have`, `Could Have`, `Won't Have`), Gherkin acceptance criteria (`Given-When-Then`), and bidirectional verification mapping to automated tests.
- **Stage 2: Architecture Decision Records (ADR / IEEE / Nygard Format)**:
  - Immutable architectural decisions (`ArchitectureDecisionRecord`) capturing Context, Decision, Positive & Negative Consequences, Compliance Impact (ISO 27001 A.8.25), and Author signoff.
- **Stage 3: Git Version Control & 4-Eyes Pull Request Reviews**:
  - Branch protection rules, lines $+/-$ diffs, peer reviewers, and DevSecOps security signoff (`PullRequestReview`, `CodeRepository`).
- **Stage 4: CI/CD Automated Pipelines with DevSecOps Quality Gates**:
  - Commit SHA tracking, pipeline duration, unit test execution, code coverage $\ge 90\%$, SAST (Bandit / Semgrep), SCA dependency scanning (pip-audit / OWASP Dependency-Check), secret leak scanning, and automated quality gate enforcement (`CICDPipelineRun`).
- **Stage 5: Software Defect & Bug Tracking (IEEE 1044 / ISO 25010)**:
  - Defect tracking (`DefectBugRecord`) classifying severity ($S1$-Blocker, $S2$-Critical, $S3$-Medium, $S4$-Minor/Cosmetic), environment, steps to reproduce, and fix commit SHA.
- **Stage 6: Semantic Versioning & Release Deployments with CAB Approval**:
  - Semantic releases (`v1.0.0`, `v1.1.0`), Change Advisory Board (CAB) approval, zero-downtime deployment strategies (Blue-Green / Canary), rollback plans, and smoke test status (`ReleaseDeployment`).
- **Stage 7: SRE Observability Telemetry & SLO Error Budgets**:
  - p95 and p99 API latency metrics, 30-day uptime $\%$, HTTP 5xx error rate, SLO error budget remaining $\%$, and live telemetry (`SREObservabilityMetric`).

---

## 17. Test Coverage & Verification Summary

- **Total Automated Pytest Tests**: **235 tests** across 25 test suites (`test_crypto_tools.py`, `test_enterprise_operations.py`, `test_agentic_ai.py`, `test_itsm_comprehensive.py`, `test_training_academy.py`, `test_sharepoint_portal.py`, `test_analytics.py`, `test_api_endpoints.py`, `test_attendance.py`, `test_auth_and_docx.py`, `test_autofix_engine.py`, `test_crm_enterprise.py`, `test_ctc_calculator.py`, `test_developer_platform.py`, `test_letter_generator.py`, `test_pmo_global_processes.py`, `test_salary_statement_engine.py`, `test_sdlc_engineering.py`, `test_secops_workflow.py`, `test_stakeholder_portals.py`, `test_strategic_procurement.py`, `test_strategy_and_dynamic_kpi.py`, `test_tax_engine.py`, `test_ticketing_notifications.py`, `test_vendor_portal_full.py`).
- **Pass Rate**: `235 passed in 12.42s (100% pass rate)`.
- **Database Schema**: 95+ relational SQLAlchemy tables pre-seeded and active in SQLite (`asperion.db`) with Write-Ahead Logging (WAL) mode enabled.
- **Live Background Server**: Active on `http://127.0.0.1:8080` with FastAPI, interactive OpenAPI docs (`/docs`), ReDoc (`/redoc`), and interactive single-page application.

---

## 18. Enterprise Agentic AI & Autonomous Multi-Agent Swarm Suite (Module 21 / ISO 42001, ISO 27001, DPDP Act 2023)

- **Decentralized Multi-Agent Swarm Architecture**:
  - Orchestrates specialized enterprise agents across Engineering (`AGT-SRE-01`), Legal & Governance (`AGT-COMPLY-01`), Finance & Treasury (`AGT-FINOPS-01`), Workforce Intelligence (`AGT-TALENT-01`), and Client Delivery (`AGT-DELIVERY-01`).
  - Implements multi-step **ReAct (Reasoning + Action)** execution loops decomposed into Goal Decomposition, Policy Guardrail Evaluation, Model Context Protocol (MCP) Tool Calls, Observation Synthesis, and Self-Healing Reflection.
- **Multi-Tier Autonomy Governance**:
  - **Level 4: Fully Autonomous**: Non-destructive operational scans, CMDB health harvests, and automated self-healing runbooks.
  - **Level 3: Supervised Autonomy**: Change execution with mandatory compensatory rollback and automated admin notifications.
  - **Level 2: Human-in-the-Loop Required**: High-stakes commercial tax invoicing, statutory ledger locks, and legal modifications requiring Director Varadi Vijay's digital approval gate.
- **MCP Tool Grounding & Database Integrity**:
  - Verifiable tool grounding against production SQLite tables (`invoices`, `configuration_items`, `client_contracts`, `attendance_records`, `project_milestones`).
  - Zero hallucination of corporate facts: strictly enforces official entity credentials (`ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED`, CIN `U85500KA2026OPC222069`, Founder & Sole Director `Varadi Vijay`).
- **SOC 2 & ISO 27001 Execution Trace Auditing**:
  - `AgentExecutionTrace` table records every tool call, latency ms, token consumption, and guardrail pass verification.
- **Detailed Specification**: See [AGENTIC_AI_ARCHITECTURE.md](docs/AGENTIC_AI_ARCHITECTURE.md).

---

## 19. Core Enterprise Operations, BCP/DR & Cryptographic Event Ledger (Module 22 / ISO 27001 A.12.4, SOC 2 CC7.2, DPDP Act 2023)

- **Immutable Cryptographic Event Sourcing Ledger**:
  - SHA-256 hash chaining initialized from Genesis block (`00000000...0000`).
  - Strict mathematical formula: $\text{Current Hash} = \text{SHA-256}(\text{Prev Hash} \parallel \text{Event Code} \parallel \text{Aggregate Type} \parallel \text{Aggregate ID} \parallel \text{Event Type} \parallel \text{Payload JSON} \parallel \text{Timestamp})$.
  - High-speed verification via `POST /api/v1/operations/ledger/verify` guaranteeing zero backdating, record deletion, or unauthorized field modifications.
- **Business Continuity & Disaster Recovery (BCP/DR) Drill Simulator**:
  - Full hot SQLite backups and incremental WAL transaction checkpoints (`DisasterRecoverySnapshot`).
  - Direct binary byte SHA-256 checksum calculation and AES-256-GCM envelope encryption.
  - Verification against strict operational commitments: **Recovery Point Objective (RPO) $\le 15$ minutes** and **Recovery Time Objective (RTO) $\le 5$ minutes** via automated sandbox recovery drills.
- **India DPDP Act 2023 Statutory Consent Register**:
  - Statutory compliance register under Sections 5 & 6 of the Digital Personal Data Protection Act 2023 (`DPDPConsentRecord`).
  - Tracks affirmative digital consent across Data Principals (employees, client sponsors, vendor contacts, and candidates).
  - Explicit tracking of Purpose Categories, Notice References (`ADT/DPDP/NOTICE/2026/V1`), Consent Tokens, and designated Data Protection Officer (`AGT-COMPLY-01`).
- **Autonomous SRE Storage Telemetry & Zero-Downtime Maintenance**:
  - Real-time diagnostic harvesting (`SystemDiagnosticTelemetry`) tracking database file size, Write-Ahead Log (WAL) buffer, query response latency (`SELECT 1`), and resident memory (RSS).
  - One-click and automated WAL checkpoint truncation (`PRAGMA wal_checkpoint(TRUNCATE);`) and SQLite database vacuuming reallocating disk pages without blocking concurrent application reads/writes.
- **Detailed Specification**: See [OPERATIONS_BCP_DR_ARCHITECTURE.md](docs/OPERATIONS_BCP_DR_ARCHITECTURE.md).

---

## 20. Enterprise Cryptography, PKI & Digital Attestation Tools (Module 23 / FIPS 140-3, ISO 27001 A.10, RFC 8032)

- **Standard Cryptographic Engine (`app/engines/crypto_engine.py`)**:
  - Centralized, zero-leakage cryptographic operations covering symmetric encryption, asymmetric digital signatures, message authentication, and Merkle tree roots.
- **Symmetric Authenticated Encryption (AES-256-GCM AEAD)**:
  - AES-256-GCM with 96-bit random nonces and 100,000-iteration PBKDF2-HMAC-SHA256 key derivation.
  - Provides authenticated confidentiality and tamper-detection for enterprise secrets, payloads, and backups.
- **Asymmetric Keypairs & Digital Signatures (Ed25519 & RSA-PSS)**:
  - Ultra-high speed Edwards-curve Ed25519 signatures (RFC 8032) for fast microservice non-repudiation and event ledger sealing.
  - RSA-2048 and RSA-4096 with PSS (Probabilistic Signature Scheme) for external regulatory and banking integration.
- **Merkle Tree Root Engine**:
  - Computes cryptographic Merkle tree roots across arbitrary batches of audit items, transactions, or state events for SOC 2 Type II audit certifications.
- **Interactive Workbench UI & REST API**:
  - Mounted at `/api/v1/crypto` and accessible via the sidebar navigation button (`#view-crypto-tools`).
- **Detailed Specification**: See [CRYPTOGRAPHY_PKI_ARCHITECTURE.md](docs/CRYPTOGRAPHY_PKI_ARCHITECTURE.md).


