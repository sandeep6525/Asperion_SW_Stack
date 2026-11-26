"""
Asperion Enterprise OS - Comprehensive Vendor Management & Strategic Sourcing Models
Aligns with CIPS, ISM, ISO 20400 Sustainable Procurement, MSMED Act 2006, and DPDP Act 2023.
Covers 8 enterprise procurement pillars:
1. Approved Vendor Master & KYC Due Diligence
2. Sourcing Category Master & Spend Planning
3. Purchase Requisitions (PR) & Departmental Approvals
4. Strategic Sourcing e-RFX Pipeline (RFP, RFQ, BAFO)
5. Vendor Bid Submissions & Multi-Criteria Scoring
6. Contract Lifecycle Management (CLM) & Renewals
7. Goods Received Notes (GRN) & 3-Way Inspection
8. Vendor Performance Scorecards, Third-Party Risk & CAPA
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SourcingCategory(Base):
    """Pillar 2: Sourcing Category Master & Spend Targets"""
    __tablename__ = "sourcing_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String(50), unique=True, index=True) # CAT-IT-CLOUD
    category_name = Column(String(100), nullable=False)
    annual_budget_inr = Column(Float, default=0.0)
    sourcing_strategy = Column(String(100), default="Multi-Vendor Competitive") # Multi-Vendor Competitive, Strategic Sole Source, Preferred Partner Panel, Direct Spot Buy
    lead_buyer = Column(String(100), default="Head of Procurement")
    active_vendors_count = Column(Integer, default=1)
    esg_weight_pct = Column(Float, default=10.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vendor(Base):
    """Pillar 1: Approved Vendor Master & Due Diligence"""
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String(50), unique=True, index=True) # ADT-VEN-001
    vendor_name = Column(String(255), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100), nullable=False)
    phone = Column(String(50))
    category = Column(String(100), default="Cloud & Infrastructure") # Cloud, SaaS, Professional Services, Hardware, Staffing
    criticality_tier = Column(String(50), default="Tier 2 - High") # Tier 1 - Mission Critical, Tier 2 - High, Tier 3 - Medium, Tier 4 - Low
    pan = Column(String(20))
    gstin = Column(String(30))
    duns_number = Column(String(50), default="91-234-5678")
    bank_account_number = Column(String(50))
    bank_ifsc = Column(String(20))
    bank_name = Column(String(100))
    msme_registered = Column(Boolean, default=False)
    msme_udyam_number = Column(String(50), nullable=True)
    msme_category = Column(String(50), default="Micro") # Micro, Small, Medium, Non-MSME
    msme_payment_due_days = Column(Integer, default=45) # Statutory 45-day rule under MSMED Act 2006
    kyc_status = Column(String(50), default="Approved") # Pending, Approved, Rejected
    dpdp_compliance_status = Column(String(50), default="Compliant") # Assessed & Compliant, Pending DPA, High Risk
    annual_spend_estimate = Column(Float, default=0.0)
    payment_terms_days = Column(Integer, default=30)
    rating = Column(Float, default=92.5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    contracts = relationship("VendorContract", back_populates="vendor")
    scorecards = relationship("VendorScorecard", back_populates="vendor")
    grns = relationship("GoodsReceivedNote", back_populates="vendor")
    risk_assessments = relationship("VendorRiskAssessment", back_populates="vendor")

class PurchaseRequisition(Base):
    """Pillar 3: Internal Spend Request & Departmental Approval Workflow"""
    __tablename__ = "purchase_requisitions"
    
    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(String(50), unique=True, index=True) # ADT-PR-2026-001
    requester_name = Column(String(100), nullable=False)
    requester_email = Column(String(100), nullable=False)
    department = Column(String(100), default="Engineering & Product")
    category = Column(String(100), default="Cloud & Infrastructure")
    item_details = Column(Text, nullable=False)
    estimated_amount_inr = Column(Float, default=0.0)
    urgency = Column(String(50), default="Normal") # Normal, Urgent, Critical
    business_justification = Column(Text, nullable=False)
    approval_status = Column(String(50), default="Pending HOD Approval") # Draft, Pending HOD Approval, Pending Director Signoff, Approved, Converted to PO, Rejected
    approved_by = Column(String(100), nullable=True)
    approved_date = Column(Date, nullable=True)
    linked_po_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StrategicSourcingEvent(Base):
    """Pillar 4: Strategic Sourcing e-RFX Pipeline (RFP, RFQ, RFI, Reverse Auction)"""
    __tablename__ = "strategic_sourcing_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_code = Column(String(50), unique=True, index=True) # ADT-RFX-2026-001
    event_type = Column(String(50), default="RFP") # RFP, RFQ, RFI, Reverse Auction
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Cloud Hosting & Infrastructure")
    budget_allocation_inr = Column(Float, default=0.0)
    baseline_cost_inr = Column(Float, default=0.0)
    target_delivery_date = Column(Date, nullable=True)
    status = Column(String(50), default="Published / Open") # Draft, Published / Open, Technical Evaluation, Commercial BAFO, Awarded, Closed
    closing_date = Column(Date, nullable=False)
    technical_weight_pct = Column(Float, default=40.0)
    commercial_weight_pct = Column(Float, default=30.0)
    compliance_security_weight_pct = Column(Float, default=20.0)
    sla_weight_pct = Column(Float, default=10.0)
    awarded_vendor_name = Column(String(255), nullable=True)
    awarded_amount_inr = Column(Float, default=0.0)
    savings_realized_inr = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    bids = relationship("VendorBidSubmission", back_populates="event")

class VendorBidSubmission(Base):
    """Pillar 5: Vendor Bid Submissions & Multi-Criteria Weighted Scoring"""
    __tablename__ = "vendor_bid_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    bid_code = Column(String(50), unique=True, index=True) # ADT-BID-2026-001
    event_id = Column(Integer, ForeignKey("strategic_sourcing_events.id"), nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    vendor_name = Column(String(255), nullable=False)
    technical_score = Column(Float, default=85.0) # 0 - 100
    commercial_quote_inr = Column(Float, default=0.0)
    compliance_score = Column(Float, default=90.0) # 0 - 100
    sla_guarantee_pct = Column(Float, default=99.9)
    composite_score = Column(Float, default=87.5) # calculated
    is_shortlisted = Column(Boolean, default=True)
    award_status = Column(String(50), default="Submitted") # Submitted, Shortlisted, BAFO Finalist, Awarded, Unsuccessful
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("StrategicSourcingEvent", back_populates="bids")

class VendorContract(Base):
    """Pillar 6: Contract Lifecycle Management (CLM), MSAs & Renewals"""
    __tablename__ = "vendor_contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_reference = Column(String(50), unique=True, index=True) # ADT-VCON-001
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    agreement_type = Column(String(50), default="Master Services Agreement (MSA)") # MSA, SOW, SLA, NDA, DPA
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    annual_value_inr = Column(Float, default=0.0)
    sla_uptime_commitment = Column(Float, default=99.9) # percentage
    confidentiality_clause = Column(Boolean, default=True)
    data_protection_annexure = Column(Boolean, default=True)
    renewal_notice_days = Column(Integer, default=60)
    auto_renew_enabled = Column(Boolean, default=True)
    liability_cap_inr = Column(Float, default=1000000.0)
    governing_jurisdiction = Column(String(100), default="Courts of Bengaluru, Karnataka")
    status = Column(String(50), default="Active") # Active, Expiring, Expired, Terminated
    created_at = Column(DateTime, default=datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="contracts")

class GoodsReceivedNote(Base):
    """Pillar 7: Inbound Fulfillment, Inspection & 3-Way Match Verification"""
    __tablename__ = "goods_received_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    grn_number = Column(String(50), unique=True, index=True) # ADT-GRN-2026-001
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    po_reference = Column(String(50), nullable=False)
    delivery_challan_no = Column(String(100), nullable=True)
    received_date = Column(Date, nullable=False)
    item_description = Column(String(255), nullable=False)
    quantity_ordered = Column(Float, default=1.0)
    quantity_received = Column(Float, default=1.0)
    quantity_accepted = Column(Float, default=1.0)
    quantity_rejected = Column(Float, default=0.0)
    inspection_status = Column(String(50), default="Accepted") # Accepted, Partial Rejection, Rejected
    inspected_by = Column(String(100), default="IT Admin / Project Manager")
    warehouse_location = Column(String(100), default="Horamavu Bangalore HQ")
    rejection_reason = Column(String(255), nullable=True)
    rtv_credit_note_ref = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="grns")

class VendorScorecard(Base):
    """Pillar 8: Vendor Performance Management & Quarterly Business Reviews (QBR)"""
    __tablename__ = "vendor_scorecards"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    evaluation_period = Column(String(50), nullable=False) # e.g. "Q2-2026"
    quality_score = Column(Float, default=90.0)       # 0 - 100
    sla_adherence_score = Column(Float, default=95.0) # 0 - 100
    pricing_competitiveness = Column(Float, default=85.0)
    security_privacy_score = Column(Float, default=95.0)
    overall_rating = Column(Float, default=91.25)
    performance_tier = Column(String(50), default="Preferred Vendor") # Strategic Partner, Preferred Vendor, Satisfactory, Under Watch, Disqualified
    evaluator = Column(String(100), default="Procurement Lead")
    qbr_action_items = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="scorecards")

class RFPComparison(Base):
    """Legacy & Multi-Quote Comparative Statement (3-Quote Rule)"""
    __tablename__ = "rfp_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    rfp_reference = Column(String(50), unique=True, index=True) # ADT-RFP-2026-001
    item_title = Column(String(255), nullable=False) # e.g. "Cloud Managed Kubernetes Infrastructure"
    category = Column(String(100), default="Cloud Hosting")
    vendor_a_name = Column(String(100), nullable=False)
    vendor_a_quote = Column(Float, default=0.0)
    vendor_b_name = Column(String(100), nullable=False)
    vendor_b_quote = Column(Float, default=0.0)
    vendor_c_name = Column(String(100), nullable=True)
    vendor_c_quote = Column(Float, default=0.0)
    selected_vendor = Column(String(100), nullable=False)
    commercial_justification = Column(Text, nullable=False)
    approved_by = Column(String(100), default="Founder / Procurement Committee")
    created_at = Column(DateTime, default=datetime.utcnow)

class VendorRiskAssessment(Base):
    """Third-Party Risk Management (TPRM / ISO 27001 A.15 / DPDP Act 2023)"""
    __tablename__ = "vendor_risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    data_access_level = Column(String(50), default="PII & Confidential") # None, Internal, PII & Confidential
    dpdp_dpa_signed = Column(Boolean, default=True)
    iso27001_certified = Column(Boolean, default=True)
    soc2_type2_attestation = Column(Boolean, default=True)
    cross_border_data_transfer = Column(Boolean, default=False)
    subprocessor_disclosure_verified = Column(Boolean, default=True)
    residual_risk_level = Column(String(20), default="Low") # Low, Medium, High
    review_date = Column(Date, nullable=False)
    assessor = Column(String(100), default="CISO / IT Security Lead")
    
    vendor = relationship("Vendor", back_populates="risk_assessments")

class VendorCorrectiveActionPlan(Base):
    """Vendor Corrective & Preventive Action Plan (CAPA)"""
    __tablename__ = "vendor_capas"
    
    id = Column(Integer, primary_key=True, index=True)
    capa_code = Column(String(50), unique=True, index=True) # ADT-CAPA-2026-001
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    vendor_name = Column(String(255), nullable=False)
    issue_description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=False)
    corrective_action_agreed = Column(Text, nullable=False)
    target_closure_date = Column(Date, nullable=False)
    status = Column(String(50), default="In Progress") # Open, In Progress, Under Verification, Closed / Resolved
    verified_by = Column(String(100), default="Procurement & Quality Lead")
    created_at = Column(DateTime, default=datetime.utcnow)
