"""
Asperion Enterprise OS - Comprehensive Vendor & Procurement Schemas
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# 1. Sourcing Category
class SourcingCategoryCreate(BaseModel):
    category_code: str
    category_name: str
    annual_budget_inr: float = 0.0
    sourcing_strategy: str = "Multi-Vendor Competitive"
    lead_buyer: str = "Head of Procurement"
    active_vendors_count: int = 1
    esg_weight_pct: float = 10.0

class SourcingCategoryOut(SourcingCategoryCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# 2. Vendor Master
class VendorCreate(BaseModel):
    vendor_code: str
    vendor_name: str
    contact_person: Optional[str] = None
    email: str
    phone: Optional[str] = None
    category: str = "Cloud & Infrastructure"
    criticality_tier: str = "Tier 2 - High"
    pan: Optional[str] = None
    gstin: Optional[str] = None
    duns_number: Optional[str] = "91-234-5678"
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_name: Optional[str] = None
    msme_registered: bool = False
    msme_udyam_number: Optional[str] = None
    msme_category: str = "Micro"
    msme_payment_due_days: int = 45
    annual_spend_estimate: float = 0.0
    payment_terms_days: int = 30
    rating: float = 92.5

class VendorOut(VendorCreate):
    id: int
    kyc_status: str
    dpdp_compliance_status: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# 3. Purchase Requisition (PR)
class PurchaseRequisitionCreate(BaseModel):
    pr_number: str
    requester_name: str
    requester_email: str
    department: str = "Engineering & Product"
    category: str = "Cloud & Infrastructure"
    item_details: str
    estimated_amount_inr: float
    urgency: str = "Normal"
    business_justification: str

class PurchaseRequisitionStatusUpdate(BaseModel):
    approval_status: str
    approved_by: Optional[str] = "Varadi Vijay (Director)"
    linked_po_number: Optional[str] = None

class PurchaseRequisitionOut(PurchaseRequisitionCreate):
    id: int
    approval_status: str
    approved_by: Optional[str]
    approved_date: Optional[date]
    linked_po_number: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# 4. Strategic Sourcing Event (e-RFX)
class StrategicSourcingEventCreate(BaseModel):
    event_code: str
    event_type: str = "RFP"
    title: str
    category: str = "Cloud Hosting & Infrastructure"
    budget_allocation_inr: float
    baseline_cost_inr: float
    target_delivery_date: Optional[date] = None
    closing_date: date
    technical_weight_pct: float = 40.0
    commercial_weight_pct: float = 30.0
    compliance_security_weight_pct: float = 20.0
    sla_weight_pct: float = 10.0

class StrategicSourcingEventOut(StrategicSourcingEventCreate):
    id: int
    status: str
    awarded_vendor_name: Optional[str]
    awarded_amount_inr: float
    savings_realized_inr: float
    created_at: datetime
    class Config:
        from_attributes = True

# 5. Vendor Bid Submission
class VendorBidSubmissionCreate(BaseModel):
    bid_code: str
    event_id: Optional[int] = None
    vendor_id: Optional[int] = None
    vendor_name: str
    technical_score: float = 85.0
    commercial_quote_inr: float
    compliance_score: float = 90.0
    sla_guarantee_pct: float = 99.9
    award_status: str = "Submitted"
    notes: Optional[str] = None

class VendorBidSubmissionOut(VendorBidSubmissionCreate):
    id: int
    composite_score: float
    is_shortlisted: bool
    created_at: datetime
    class Config:
        from_attributes = True

# 6. Vendor Contract
class VendorContractCreate(BaseModel):
    contract_reference: str
    vendor_id: int
    agreement_type: str = "Master Services Agreement (MSA)"
    effective_date: date
    expiry_date: Optional[date] = None
    annual_value_inr: float = 0.0
    sla_uptime_commitment: float = 99.9
    confidentiality_clause: bool = True
    data_protection_annexure: bool = True
    renewal_notice_days: int = 60
    auto_renew_enabled: bool = True
    liability_cap_inr: float = 1000000.0
    governing_jurisdiction: str = "Courts of Bengaluru, Karnataka"

class VendorContractOut(VendorContractCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# 7. Goods Received Note (GRN)
class GoodsReceivedNoteCreate(BaseModel):
    grn_number: str
    vendor_id: int
    po_reference: str
    delivery_challan_no: Optional[str] = None
    received_date: date
    item_description: str
    quantity_ordered: float = 1.0
    quantity_received: float = 1.0
    quantity_accepted: float = 1.0
    quantity_rejected: float = 0.0
    inspection_status: str = "Accepted"
    inspected_by: str = "IT Admin / Project Manager"
    warehouse_location: str = "Horamavu Bangalore HQ"
    rejection_reason: Optional[str] = None
    rtv_credit_note_ref: Optional[str] = None
    remarks: Optional[str] = None

class GoodsReceivedNoteOut(GoodsReceivedNoteCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Portal-specific DTOs
class PortalInwardGRNCreate(BaseModel):
    vendor_id: int
    po_reference: str
    delivery_challan_no: Optional[str] = None
    received_date: date
    item_description: str
    quantity_ordered: float = 1.0
    quantity_received: float = 1.0
    quantity_accepted: float = 1.0
    quantity_rejected: float = 0.0
    inspection_status: str = "Accepted"
    inspected_by: str = "Arjun Sharma (Lead Architect)"
    warehouse_location: str = "Horamavu Bangalore HQ"
    rejection_reason: Optional[str] = None
    rtv_credit_note_ref: Optional[str] = None
    remarks: Optional[str] = None

class PortalVendorBillSubmit(BaseModel):
    vendor_name: str
    bill_number: str
    bill_date: date
    due_date: Optional[date] = None
    po_reference: Optional[str] = None
    grn_reference: Optional[str] = None
    expense_category: str = "Cloud Hosting / Hardware"
    taxable_amount: float
    gst_amount: float = 0.0
    tds_section: str = "194C" # 194C (1% or 2%) or 194J (10% or 2%)

class PortalRFXBidSubmit(BaseModel):
    event_id: int
    vendor_id: int
    commercial_quote_inr: float
    technical_score: float = 88.0
    compliance_score: float = 92.0
    sla_guarantee_pct: float = 99.95
    notes: Optional[str] = None

# 8. Vendor Scorecard
class VendorScorecardCreate(BaseModel):
    vendor_id: int
    evaluation_period: str
    quality_score: float = 90.0
    sla_adherence_score: float = 95.0
    pricing_competitiveness: float = 85.0
    security_privacy_score: float = 95.0
    evaluator: str = "Procurement Lead"
    qbr_action_items: Optional[str] = None

class VendorScorecardOut(VendorScorecardCreate):
    id: int
    overall_rating: float
    performance_tier: str
    created_at: datetime
    class Config:
        from_attributes = True

# 9. Vendor Risk Assessment (TPRM)
class VendorRiskAssessmentCreate(BaseModel):
    vendor_id: int
    data_access_level: str = "PII & Confidential"
    dpdp_dpa_signed: bool = True
    iso27001_certified: bool = True
    soc2_type2_attestation: bool = True
    cross_border_data_transfer: bool = False
    subprocessor_disclosure_verified: bool = True
    residual_risk_level: str = "Low"
    review_date: date
    assessor: str = "CISO / IT Security Lead"

class VendorRiskAssessmentOut(VendorRiskAssessmentCreate):
    id: int
    class Config:
        from_attributes = True

# 10. Vendor Corrective Action Plan (CAPA)
class VendorCAPACreate(BaseModel):
    capa_code: str
    vendor_id: Optional[int] = None
    vendor_name: str
    issue_description: str
    root_cause: str
    corrective_action_agreed: str
    target_closure_date: date
    status: str = "In Progress"
    verified_by: str = "Procurement & Quality Lead"

class VendorCAPAOut(VendorCAPACreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
