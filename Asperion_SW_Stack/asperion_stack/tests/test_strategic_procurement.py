"""
Asperion Enterprise OS - Comprehensive Test Suite for Vendor Management & Strategic Sourcing
Validates all 8 procurement pillars:
1. Approved Vendor Master & Due Diligence (KYC, MSMED Act 2006 45-day rule, DPDP Act 2023)
2. Sourcing Category Management & Spend Planning (Budgets & Strategies)
3. Purchase Requisitions (PR to PO delegation of authority workflow)
4. Strategic Sourcing e-RFX Pipeline (RFP, RFQ, Reverse Auction & Awarded Savings)
5. Vendor Bid Submissions & Multi-Criteria Weighted Scoring (Tech 40%, Comm 30%, SecOps 20%, SLA 10%)
6. Contract Lifecycle Management (CLM, Uptime SLAs & Renewal Schedule)
7. Inbound Fulfillment & Goods Received Notes (GRN 3-Way Match Verification)
8. Vendor Performance (QBR Scorecards), Third-Party Risk (TPRM) & CAPA Action Plans
"""
import uuid
from datetime import date
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.procurement import (
    list_sourcing_categories, create_sourcing_category,
    list_vendors, create_vendor, get_vendor_details,
    list_purchase_requisitions, create_purchase_requisition, update_purchase_requisition_status,
    list_sourcing_events, create_sourcing_event, award_sourcing_event, SourcingEventAward,
    list_vendor_bids, submit_vendor_bid,
    list_vendor_contracts, create_vendor_contract, get_expiring_vendor_contracts,
    list_grns, create_grn,
    list_scorecards, create_scorecard,
    list_vendor_risk_assessments, create_vendor_risk_assessment,
    list_vendor_capas, create_vendor_capa, update_capa_status, CAPAStatusUpdate,
    get_procurement_executive_overview
)
from app.schemas.procurement import (
    SourcingCategoryCreate, VendorCreate,
    PurchaseRequisitionCreate, PurchaseRequisitionStatusUpdate,
    StrategicSourcingEventCreate, VendorBidSubmissionCreate,
    VendorContractCreate, GoodsReceivedNoteCreate,
    VendorScorecardCreate, VendorRiskAssessmentCreate,
    VendorCAPACreate
)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    yield db
    db.close()


def test_sourcing_categories_and_spend_planning(db_session):
    # 1. List Sourcing Categories
    cats = list_sourcing_categories(db=db_session)
    assert len(cats) >= 5
    assert any(c.category_code == "CAT-IT-CLOUD" for c in cats)
    assert any(c.category_code == "CAT-HARDWARE" for c in cats)
    assert any(c.category_code == "CAT-SAAS" for c in cats)

    # 2. Create New Sourcing Category
    uniq_code = f"CAT-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_cat = SourcingCategoryCreate(
        category_code=uniq_code,
        category_name="Data Center Co-location & Fiber Connectivity",
        annual_budget_inr=500000.0,
        sourcing_strategy="Multi-Vendor Competitive",
        lead_buyer="Priya Nair",
        active_vendors_count=2,
        esg_weight_pct=10.0
    )
    created = create_sourcing_category(cat_in=new_cat, db=db_session)
    assert created.category_code == uniq_code
    assert created.annual_budget_inr == 500000.0


def test_vendor_master_due_diligence_and_msme(db_session):
    # 1. List Vendors
    vendors = list_vendors(db=db_session)
    assert len(vendors) >= 5
    assert any(v.vendor_name == "Amazon Web Services India Pvt Ltd" for v in vendors)
    assert any("Nexus" in v.vendor_name for v in vendors)

    # Verify MSMED Act 2006 compliance settings
    msme_vendors = [v for v in vendors if v.msme_registered]
    assert len(msme_vendors) >= 2
    assert all(v.msme_payment_due_days == 45 for v in msme_vendors)

    # 2. Create New Vendor
    uniq_code = f"ADT-VEN-{uuid.uuid4().hex[:4].upper()}"
    new_ven = VendorCreate(
        vendor_code=uniq_code,
        vendor_name="Cloudflare Security India Pvt Ltd",
        contact_person="Ramesh Patel",
        email=f"ramesh@{uuid.uuid4().hex[:6]}.com",
        phone="+91 80 4455 6677",
        category="Cloud & CDN Security",
        criticality_tier="Tier 1 - Mission Critical",
        pan="AABCC7788P",
        gstin="29AABCC7788P1Z8",
        duns_number="91-889-9900",
        msme_registered=False,
        msme_category="Non-MSME",
        payment_terms_days=30,
        rating=97.0
    )
    created = create_vendor(ven_in=new_ven, db=db_session)
    assert created.vendor_code == uniq_code
    assert created.kyc_status == "Approved"
    assert created.dpdp_compliance_status == "Compliant"

    # 3. Get Details
    details = get_vendor_details(vendor_id=created.id, db=db_session)
    assert details.vendor_name == "Cloudflare Security India Pvt Ltd"


def test_purchase_requisitions_and_approvals(db_session):
    # 1. List Requisitions
    prs = list_purchase_requisitions(db=db_session)
    assert len(prs) >= 4
    assert any(pr.pr_number == "ADT-PR-2026-001" for pr in prs)

    # 2. Create PR
    uniq_pr = f"ADT-PR-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_pr = PurchaseRequisitionCreate(
        pr_number=uniq_pr,
        requester_name="Vikram Rathore",
        requester_email="vikram.rathore@asperion.in",
        department="PMO & Project Delivery",
        category="Enterprise SaaS & Developer Tools",
        item_details="Atlassian Jira Enterprise Cloud 50-Seat Subscription",
        estimated_amount_inr=150000.0,
        urgency="Normal",
        business_justification="Required for Agile sprint capacity planning and WBS task tracking."
    )
    created = create_purchase_requisition(pr_in=new_pr, db=db_session)
    assert created.pr_number == uniq_pr
    assert created.approval_status == "Pending HOD Approval"

    # 3. Approve PR and Link PO
    update = PurchaseRequisitionStatusUpdate(
        approval_status="Converted to PO",
        approved_by="Varadi Vijay (Sole Director)",
        linked_po_number="ADT/PO/2026/009"
    )
    approved = update_purchase_requisition_status(pr_id=created.id, status_update=update, db=db_session)
    assert approved.approval_status == "Converted to PO"
    assert approved.linked_po_number == "ADT/PO/2026/009"
    assert approved.approved_date == date.today()


def test_strategic_sourcing_events_and_awarded_savings(db_session):
    # 1. List Events
    events = list_sourcing_events(db=db_session)
    assert len(events) >= 3
    ev1 = next(e for e in events if e.event_code == "ADT-RFX-2026-001")
    assert ev1.status == "Awarded"
    assert ev1.savings_realized_inr >= 50000.0

    # 2. Create Event
    uniq_ev = f"ADT-RFX-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_ev = StrategicSourcingEventCreate(
        event_code=uniq_ev,
        event_type="RFP",
        title="Multi-Cloud Disaster Recovery Warm-Standby Storage",
        category="Cloud Hosting & Infrastructure",
        budget_allocation_inr=400000.0,
        baseline_cost_inr=450000.0,
        closing_date=date(2026, 8, 15),
        technical_weight_pct=45.0,
        commercial_weight_pct=30.0,
        compliance_security_weight_pct=15.0,
        sla_weight_pct=10.0
    )
    created = create_sourcing_event(event_in=new_ev, db=db_session)
    assert created.event_code == uniq_ev
    assert created.status == "Published / Open"

    # 3. Award Sourcing Event
    award_payload = SourcingEventAward(
        awarded_vendor_name="Nexus Micro Systems Pvt Ltd",
        awarded_amount_inr=380000.0
    )
    awarded = award_sourcing_event(event_id=created.id, award_in=award_payload, db=db_session)
    assert awarded.status == "Awarded"
    assert awarded.awarded_vendor_name == "Nexus Micro Systems Pvt Ltd"
    assert awarded.savings_realized_inr == 70000.0 # 450,000 - 380,000


def test_vendor_bids_and_weighted_composite_scoring(db_session):
    # 1. List Bids
    bids = list_vendor_bids(db=db_session)
    assert len(bids) >= 4
    for b in bids:
        assert b.composite_score > 0
        assert b.is_shortlisted in [True, False]

    # 2. Submit Bid
    uniq_bid = f"ADT-BID-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_bid = VendorBidSubmissionCreate(
        bid_code=uniq_bid,
        vendor_name="Zenith InfoSec Solutions LLP",
        technical_score=95.0,
        commercial_quote_inr=320000.0,
        compliance_score=98.0,
        sla_guarantee_pct=99.9,
        award_status="Submitted",
        notes="Comprehensive SOC2 Type II attestation included."
    )
    created = submit_vendor_bid(bid_in=new_bid, db=db_session)
    assert created.bid_code == uniq_bid
    assert created.composite_score >= 80.0
    assert created.is_shortlisted is True


def test_vendor_contract_lifecycle_and_renewals(db_session):
    # 1. List Contracts
    contracts = list_vendor_contracts(db=db_session)
    assert len(contracts) >= 3
    assert any(c.contract_reference == "ADT-VCON-2026-001" for c in contracts)

    # 2. Create Contract
    uniq_con = f"ADT-VCON-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_con = VendorContractCreate(
        contract_reference=uniq_con,
        vendor_id=1,
        agreement_type="Data Processing Agreement (DPA)",
        effective_date=date(2026, 6, 20),
        expiry_date=date(2027, 6, 19),
        annual_value_inr=150000.0,
        sla_uptime_commitment=99.9,
        confidentiality_clause=True,
        data_protection_annexure=True,
        renewal_notice_days=60,
        auto_renew_enabled=True,
        liability_cap_inr=1000000.0
    )
    created = create_vendor_contract(con_in=new_con, db=db_session)
    assert created.contract_reference == uniq_con
    assert created.status == "Active"

    # 3. Check Expiring Contracts (Filter for 400 days will catch all active ones)
    expiring = get_expiring_vendor_contracts(days=400, db=db_session)
    assert len(expiring) >= 3


def test_goods_received_notes_and_three_way_match(db_session):
    # 1. List GRNs
    grns = list_grns(db=db_session)
    assert len(grns) >= 2
    assert any(g.grn_number == "ADT-GRN-2026-001" for g in grns)

    # 2. Inward New GRN Batch
    uniq_grn = f"ADT-GRN-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_grn = GoodsReceivedNoteCreate(
        grn_number=uniq_grn,
        vendor_id=2,
        po_reference="ADT/PO/2026/001",
        delivery_challan_no="DC-TEST-1234",
        received_date=date.today(),
        item_description="Apple Studio Displays 27-inch 5K Retina x 2",
        quantity_ordered=2.0,
        quantity_received=2.0,
        quantity_accepted=2.0,
        inspection_status="Accepted",
        inspected_by="Arjun Sharma",
        warehouse_location="Horamavu Bangalore HQ"
    )
    created = create_grn(grn_in=new_grn, db=db_session)
    assert created.grn_number == uniq_grn
    assert created.quantity_accepted == 2.0
    assert created.inspection_status == "Accepted"


def test_vendor_performance_scorecards_and_qbr(db_session):
    # 1. List Scorecards
    scorecards = list_scorecards(db=db_session)
    assert len(scorecards) >= 3
    assert any(s.performance_tier == "Strategic Partner" for s in scorecards)

    # 2. Create Scorecard
    new_sc = VendorScorecardCreate(
        vendor_id=2,
        evaluation_period="Q3-2026",
        quality_score=96.0,
        sla_adherence_score=98.0,
        pricing_competitiveness=94.0,
        security_privacy_score=96.0,
        evaluator="Vikram Rathore (PMO Lead)",
        qbr_action_items="Explore bundled multi-site logistics discount for Chennai and Hyderabad branches."
    )
    created = create_scorecard(score_in=new_sc, db=db_session)
    assert created.overall_rating == 96.0
    assert created.performance_tier == "Strategic Partner"


def test_third_party_risk_assessments_tprm(db_session):
    risks = list_vendor_risk_assessments(db=db_session)
    assert len(risks) >= 2
    for r in risks:
        assert r.dpdp_dpa_signed is True
        assert r.iso27001_certified is True
        assert r.residual_risk_level in ["Low", "Medium"]


def test_vendor_corrective_action_plans_capa(db_session):
    # 1. List CAPAs
    capas = list_vendor_capas(db=db_session)
    assert len(capas) >= 1
    assert any(c.capa_code == "ADT-CAPA-2026-001" for c in capas)

    # 2. Create CAPA
    uniq_capa = f"ADT-CAPA-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_capa = VendorCAPACreate(
        capa_code=uniq_capa,
        vendor_name="Nexus Micro Systems Pvt Ltd",
        issue_description="Minor 1-day delivery delay on spare USB-C Thunderbolt adapter order.",
        root_cause="Courier local transit vehicle breakdown.",
        corrective_action_agreed="Secondary priority courier air service onboarded for Tier 1 replacement parts.",
        target_closure_date=date(2026, 7, 30),
        status="In Progress",
        verified_by="Arjun Sharma"
    )
    created = create_vendor_capa(capa_in=new_capa, db=db_session)
    assert created.capa_code == uniq_capa
    assert created.status == "In Progress"

    # 3. Patch Status
    patch = CAPAStatusUpdate(status="Closed / Resolved")
    updated = update_capa_status(capa_id=created.id, update=patch, db=db_session)
    assert updated.status == "Closed / Resolved"


def test_procurement_executive_mis_overview(db_session):
    overview = get_procurement_executive_overview(db=db_session)
    assert overview["status"] == "success"
    assert "procurement_kpis" in overview
    kpi = overview["procurement_kpis"]
    assert kpi["total_active_vendors"] >= 5
    assert kpi["sourcing_categories_count"] >= 5
    assert kpi["managed_spend_inr"] > 1000000.0
    assert kpi["msme_vendor_count"] >= 2
    assert kpi["msme_spend_share_pct"] > 0.0
    assert kpi["savings_realized_inr"] >= 50000.0
    assert kpi["active_contracts_value_inr"] > 1000000.0
    assert "regulatory_compliance" in overview
    comp = overview["regulatory_compliance"]
    assert "msmed_act_section_15" in comp
    assert "dpdp_act_2023_dpa" in comp
