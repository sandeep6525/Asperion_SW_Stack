"""
Asperion Enterprise OS - Finance, Invoicing, AP/AR & Statutory Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AccountMaster(Base):
    __tablename__ = "chart_of_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_code = Column(String(20), unique=True, index=True) # e.g. 1001, 1010, 2001, 3001, 4001, 5001
    account_group = Column(String(50), nullable=False) # Asset, Liability, Equity, Revenue, Expense
    account_name = Column(String(255), nullable=False)
    normal_balance = Column(String(20), default="Debit") # Debit or Credit
    gst_tds_relevant = Column(Boolean, default=False)
    cost_center = Column(String(100), default="Corporate")
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, index=True) # ADT/INV/2026/001
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    customer_name = Column(String(255), nullable=False)
    customer_gstin = Column(String(30), nullable=True)
    place_of_supply = Column(String(50), default="Karnataka (29)")
    project_ref = Column(String(100), nullable=True)
    taxable_value = Column(Float, default=0.0)
    is_interstate = Column(Boolean, default=False)
    cgst_amount = Column(Float, default=0.0) # 9%
    sgst_amount = Column(Float, default=0.0) # 9%
    igst_amount = Column(Float, default=0.0) # 18%
    total_tax = Column(Float, default=0.0)
    total_invoice_value = Column(Float, default=0.0)
    amount_received = Column(Float, default=0.0)
    outstanding_balance = Column(Float, default=0.0)
    status = Column(String(50), default="Drafted") # Drafted, Issued, Partially Paid, Paid, Overdue, Cancelled
    payment_terms = Column(String(50), default="Net 30 Days")
    created_at = Column(DateTime, default=datetime.utcnow)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True, index=True) # ADT/PO/2026/001
    po_date = Column(Date, nullable=False)
    vendor_name = Column(String(255), nullable=False)
    vendor_id = Column(Integer, nullable=True)
    project_code = Column(String(100), nullable=True)
    total_amount = Column(Float, default=0.0)
    delivery_due_date = Column(Date, nullable=True)
    status = Column(String(50), default="Approved") # Draft, Pending Approval, Approved, Fulfilled, Closed, Cancelled
    items_json = Column(Text, default="[]")
    payment_terms = Column(String(100), default="Net 30 Days")
    delivery_challan_no = Column(String(100), nullable=True)
    statutory_notes = Column(Text, default="Asperion Digital Technologies (OPC) Private Limited standard terms. Subject to Bangalore jurisdiction. MSMED Act 2006 terms apply.")
    created_at = Column(DateTime, default=datetime.utcnow)

class APBill(Base):
    __tablename__ = "ap_bills"
    
    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(50), unique=True, index=True) # Vendor Invoice Ref
    bill_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    vendor_name = Column(String(255), nullable=False)
    po_reference = Column(String(50), nullable=True)
    grn_reference = Column(String(50), nullable=True)
    three_way_match_status = Column(String(50), default="Pending") # Matched, Discrepancy, Not Applicable, Pending
    expense_category = Column(String(100), default="Cloud Hosting / SaaS")
    taxable_amount = Column(Float, default=0.0)
    gst_amount = Column(Float, default=0.0)
    tds_section = Column(String(50), default="194J") # 194C (1%/2%), 194J (10%/2%), 194I (10%/2%)
    tds_rate = Column(Float, default=0.10)
    tds_amount = Column(Float, default=0.0)
    net_payable = Column(Float, default=0.0)
    approval_status = Column(String(50), default="Pending Finance Approval") # Pending, Approved, Paid, Rejected
    payment_date = Column(Date, nullable=True)
    payment_reference = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CashFlowEntry(Base):
    __tablename__ = "cash_flow_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    period_label = Column(String(50), nullable=False) # e.g. "Week 1", "Week 2", "Jun 2026"
    opening_balance = Column(Float, default=0.0)
    customer_collections = Column(Float, default=0.0)
    other_inflows = Column(Float, default=0.0)
    total_inflows = Column(Float, default=0.0)
    payroll_payout = Column(Float, default=0.0)
    vendor_payments = Column(Float, default=0.0)
    tax_statutory_payout = Column(Float, default=0.0)
    capex_admin = Column(Float, default=0.0)
    total_outflows = Column(Float, default=0.0)
    closing_balance = Column(Float, default=0.0)
    net_burn_rate = Column(Float, default=0.0)
    runway_months = Column(Float, default=12.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class FixedAsset(Base):
    __tablename__ = "fixed_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String(50), unique=True, index=True) # ADT/FA/001
    asset_name = Column(String(255), nullable=False)
    category = Column(String(100), default="Laptops & IT Equipment") # Laptops, Servers, Office Equipment, Furniture
    purchase_date = Column(Date, nullable=False)
    purchase_cost = Column(Float, default=0.0)
    depreciation_rate_wdv = Column(Float, default=0.40) # Companies Act WDV rate (40% for IT)
    accumulated_depreciation = Column(Float, default=0.0)
    net_book_value = Column(Float, default=0.0)
    custodian = Column(String(100), default="Unassigned")
    physical_location = Column(String(100), default="Bangalore Head Office")
    status = Column(String(50), default="Active") # Active, Disposed, Under Repair
    created_at = Column(DateTime, default=datetime.utcnow)

class ExpenseClaim(Base):
    __tablename__ = "expense_claims"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String(50), unique=True, index=True) # ADT-EXP-001
    claim_date = Column(Date, nullable=False)
    claimant_name = Column(String(100), nullable=False)
    claimant_email = Column(String(100), nullable=False)
    category = Column(String(100), default="Travel & Conveyance") # Travel, Broadband / Remote Work, Client Entertainment, Certifications
    project_ref = Column(String(100), nullable=True)
    business_purpose = Column(Text, nullable=False)
    amount_inr = Column(Float, default=0.0)
    gst_paid = Column(Float, default=0.0)
    receipt_attached = Column(Boolean, default=True)
    status = Column(String(50), default="Pending Approval") # Pending Approval, Approved, Reimbursed, Rejected
    approved_by = Column(String(100), default="Department Head")
    reimbursement_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class BankReconciliationRecord(Base):
    __tablename__ = "bank_reconciliations"
    
    id = Column(Integer, primary_key=True, index=True)
    reconciliation_month = Column(String(20), nullable=False) # e.g. "JUN-2026"
    bank_account_name = Column(String(100), default="ICICI Bank Current A/c")
    statement_closing_balance = Column(Float, default=0.0)
    ledger_closing_balance = Column(Float, default=0.0)
    uncredited_deposits = Column(Float, default=0.0)
    unpresented_cheques = Column(Float, default=0.0)
    bank_charges_unrecorded = Column(Float, default=0.0)
    adjusted_balance = Column(Float, default=0.0)
    reconciled = Column(Boolean, default=True)
    reconciled_by = Column(String(100), default="Finance Lead")
    reconciliation_date = Column(Date, nullable=False)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    voucher_number = Column(String(50), unique=True, index=True) # ADT-JV-2026-001
    entry_date = Column(Date, nullable=False)
    debit_account = Column(String(100), nullable=False)
    credit_account = Column(String(100), nullable=False)
    amount = Column(Float, default=0.0)
    narration = Column(Text, nullable=False)
    cost_center = Column(String(100), default="Corporate")
    approved_by = Column(String(100), default="Founder / Sole Director")
    created_at = Column(DateTime, default=datetime.utcnow)

class BudgetItem(Base):
    __tablename__ = "budget_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cost_center = Column(String(100), nullable=False) # Product, People, Sales, Admin
    account_category = Column(String(100), nullable=False) # Cloud Hosting, Salaries, Legal Fees, Marketing
    annual_budget = Column(Float, default=0.0)
    ytd_budget = Column(Float, default=0.0)
    ytd_actual = Column(Float, default=0.0)
    variance_inr = Column(Float, default=0.0)
    variance_pct = Column(Float, default=0.0)
    financial_year = Column(String(20), default="2026-2027")

class ProjectPnL(Base):
    __tablename__ = "project_pnl"
    
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, index=True)
    project_name = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    contracted_revenue = Column(Float, default=0.0)
    recognized_revenue = Column(Float, default=0.0)
    direct_labor_cost = Column(Float, default=0.0)
    direct_cloud_infra_cost = Column(Float, default=0.0)
    vendor_subcontractor_cost = Column(Float, default=0.0)
    total_delivery_cost = Column(Float, default=0.0)
    gross_margin_inr = Column(Float, default=0.0)
    gross_margin_pct = Column(Float, default=0.0)
    status = Column(String(50), default="Active")

