"""
Asperion Enterprise OS - Finance & Invoicing Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class AccountMasterOut(BaseModel):
    id: int
    account_code: str
    account_group: str
    account_name: str
    normal_balance: str
    cost_center: str
    is_active: bool
    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    customer_name: str
    customer_gstin: Optional[str] = None
    invoice_date: date
    due_date: date
    taxable_value: float
    is_interstate: bool = False
    project_ref: Optional[str] = None
    payment_terms: str = "Net 30 Days"

class InvoiceOut(BaseModel):
    id: int
    invoice_number: str
    customer_name: str
    customer_gstin: Optional[str]
    invoice_date: date
    due_date: date
    taxable_value: float
    is_interstate: bool
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    total_tax: float
    total_invoice_value: float
    amount_received: float
    outstanding_balance: float
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class APBillCreate(BaseModel):
    bill_number: str
    vendor_name: str
    bill_date: date
    due_date: date
    taxable_amount: float
    gst_amount: float
    tds_section: str = "194J"
    expense_category: str = "Cloud Hosting / SaaS"
    po_reference: Optional[str] = None
    grn_reference: Optional[str] = None

class APBillOut(BaseModel):
    id: int
    bill_number: str
    vendor_name: str
    bill_date: date
    due_date: date
    taxable_amount: float
    gst_amount: float
    tds_section: str
    tds_rate: float
    tds_amount: float
    net_payable: float
    three_way_match_status: str
    approval_status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CashFlowForecastOut(BaseModel):
    id: int
    period_label: str
    opening_balance: float
    total_inflows: float
    total_outflows: float
    closing_balance: float
    net_burn_rate: float
    runway_months: float
    class Config:
        from_attributes = True
