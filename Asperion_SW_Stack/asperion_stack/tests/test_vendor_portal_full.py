"""
Asperion Enterprise OS - Comprehensive Test Suite for Vendor Sourcing, POs & Inward GRN Portal
Validates:
1. Vendor Portal Executive Posture, MSME Priority Classification & KYC.
2. Inward Goods Received Note (GRN) Creation, QA Inspection & PO Fulfillment Sync.
3. Vendor AP Bill Submission, Chapter XVII-B TDS (194C/194J) & Automated 3-Way Match.
4. e-RFX Sourcing Bid Submission & Multi-Criteria Weighted Scoring.
5. Official Branded Purchase Order (PO) Printable Document Generation.
6. Inward GRN & QA Inspection Certificate Printable Document Generation.
"""
import uuid
from datetime import datetime, date, timedelta
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.procurement import Vendor, GoodsReceivedNote, StrategicSourcingEvent, VendorBidSubmission
from app.models.finance import PurchaseOrder, APBill
from app.schemas.procurement import PortalInwardGRNCreate, PortalVendorBillSubmit, PortalRFXBidSubmit
from app.api.portals import (
    get_vendor_portal_data,
    create_portal_inward_grn,
    submit_portal_vendor_bill,
    submit_portal_rfx_bid,
    get_purchase_order_html,
    get_goods_received_note_html
)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    yield session
    session.close()

def test_vendor_portal_dashboard_data(db):
    # 1. Default Vendor Query (Nexus Micro Systems)
    data = get_vendor_portal_data(db=db)
    assert data["entity"]["cin"] == "U85500KA2026OPC222069"
    assert "vendor_profile" in data
    assert data["vendor_profile"]["vendor_code"] == "ADT-VEN-002"
    assert data["vendor_profile"]["msme_registered"] is True
    assert "purchase_orders" in data
    assert len(data["purchase_orders"]) >= 1
    assert "inward_grns" in data
    assert len(data["inward_grns"]) >= 1
    assert "ap_bills" in data
    assert len(data["ap_bills"]) >= 1
    assert data["kpis"]["msme_priority_eligible"] is True

    # 2. Specific Vendor Query (Acroprint Technologies India)
    acro_data = get_vendor_portal_data(vendor_name="Acroprint", db=db)
    assert "Acroprint" in acro_data["vendor_profile"]["vendor_name"]
    assert acro_data["vendor_profile"]["vendor_code"] == "ADT-VEN-005"
    assert acro_data["vendor_profile"]["msme_category"] == "Micro"

def test_create_inward_grn_and_fulfillment_sync(db):
    v = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-002").first()
    assert v is not None

    grn_in = PortalInwardGRNCreate(
        vendor_id=v.id,
        po_reference="ADT/PO/2026/001",
        delivery_challan_no="DC-TEST-8811",
        received_date=date.today(),
        item_description="Apple MacBook Pro M3 Max (36GB/1TB SSD) - Unit 3 Intake",
        quantity_ordered=3.0,
        quantity_received=3.0,
        quantity_accepted=3.0,
        quantity_rejected=0.0,
        inspection_status="Accepted",
        inspected_by="Arjun Sharma (Lead Architect)",
        warehouse_location="Horamavu Bangalore HQ",
        remarks="Hardware serial numbers cataloged and MDM enrolled."
    )

    result = create_portal_inward_grn(grn_in=grn_in, db=db)
    assert result["status"] == "SUCCESS"
    assert "ADT-GRN-" in result["grn_number"]
    assert result["inspection_status"] == "Accepted"
    assert result["accepted_quantity"] == 3.0

    # Verify PO status was synced to Fulfilled
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == "ADT/PO/2026/001").first()
    assert po is not None
    assert po.status == "Fulfilled"

def test_submit_vendor_ap_bill_with_tds_and_3way_matching(db):
    unique_bill_no = f"INV-TEST-{uuid.uuid4().hex[:6].upper()}"
    bill_in = PortalVendorBillSubmit(
        vendor_name="Nexus Micro Systems Pvt Ltd",
        bill_number=unique_bill_no,
        bill_date=date.today(),
        po_reference="ADT/PO/2026/001",
        grn_reference="ADT-GRN-2026-001",
        expense_category="Hardware & Workstations",
        taxable_amount=100000.0,
        gst_amount=18000.0,
        tds_section="194C"
    )

    result = submit_portal_vendor_bill(bill_in=bill_in, db=db)
    assert result["status"] == "SUCCESS"
    assert result["bill_number"] == unique_bill_no
    # Under 194C Corporate: 2% TDS on 1,00,000 = 2,000 INR
    assert result["tds_deducted"] == 2000.0
    # Net payable = 1,00,000 + 18,000 - 2,000 = 1,16,000 INR
    assert result["net_payable"] == 116000.0
    assert result["three_way_match_status"] == "Matched"
    assert result["msme_priority"] is True

def test_submit_portal_rfx_bid_and_scoring(db):
    ev = db.query(StrategicSourcingEvent).first()
    assert ev is not None
    v = db.query(Vendor).filter(Vendor.vendor_code == "ADT-VEN-002").first()
    assert v is not None

    bid_in = PortalRFXBidSubmit(
        event_id=ev.id,
        vendor_id=v.id,
        commercial_quote_inr=520000.0,
        technical_score=94.0,
        compliance_score=96.0,
        sla_guarantee_pct=99.99,
        notes="3-year onsite hardware warranty with 4-hour MTTR."
    )

    result = submit_portal_rfx_bid(bid_in=bid_in, db=db)
    assert result["status"] == "SUCCESS"
    assert "ADT-BID-" in result["bid_code"]
    assert result["composite_score"] > 80.0
    assert result["is_shortlisted"] is True

def test_purchase_order_html_generation(db):
    response = get_purchase_order_html(po_number="ADT/PO/2026/001", db=db)
    html = response.body.decode("utf-8")
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html
    assert "U85500KA2026OPC222069" in html
    assert "Purchase Order" in html
    assert "ADT/PO/2026/001" in html
    assert "Nexus Micro Systems" in html
    assert "Varadi Vijay" in html

def test_goods_received_note_html_generation(db):
    response = get_goods_received_note_html(grn_number="ADT-GRN-2026-001", db=db)
    html = response.body.decode("utf-8")
    assert "Goods Received Note" in html
    assert "ADT-GRN-2026-001" in html
    assert "3-Way Match Verification Posture" in html
    assert "Horamavu Bangalore HQ" in html
    assert "ISO 9001:2015 Clause 8.4" in html
