"""
Asperion Enterprise OS - Comprehensive Finance, Tax & Accounting API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from app.database import get_db
from app.models.finance import (
    AccountMaster, Invoice, PurchaseOrder, APBill, CashFlowEntry, FixedAsset,
    ExpenseClaim, BankReconciliationRecord, JournalEntry, BudgetItem, ProjectPnL
)
from app.schemas.finance import AccountMasterOut, InvoiceCreate, InvoiceOut, APBillCreate, APBillOut, CashFlowForecastOut
from app.engines.tax_engine import calculate_gst, calculate_tds, perform_three_way_match
from app.engines.cashflow_engine import generate_13_week_cashflow_model

router = APIRouter(prefix="/finance", tags=["Finance, Accounting & Tax"])

class ExpenseClaimCreate(BaseModel):
    claimant_name: str
    claimant_email: str
    category: str = "Travel & Conveyance"
    business_purpose: str
    amount_inr: float
    gst_paid: float = 0.0
    project_ref: Optional[str] = None

class JournalEntryCreate(BaseModel):
    debit_account: str
    credit_account: str
    amount: float
    narration: str
    cost_center: str = "Corporate"

@router.get("/chart-of-accounts", response_model=List[AccountMasterOut])
def get_chart_of_accounts(db: Session = Depends(get_db)):
    return db.query(AccountMaster).order_by(AccountMaster.account_code.asc()).all()

@router.get("/invoices", response_model=List[InvoiceOut])
def list_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).order_by(Invoice.invoice_date.desc()).all()

@router.post("/invoices", response_model=InvoiceOut)
def create_invoice(inv_in: InvoiceCreate, db: Session = Depends(get_db)):
    tax_calc = calculate_gst(inv_in.taxable_value, 0.18, inv_in.is_interstate)
    count = db.query(Invoice).count() + 1
    invoice_number = f"ADT/INV/2026/{count:04d}"
    
    inv = Invoice(
        invoice_number=invoice_number,
        invoice_date=inv_in.invoice_date,
        due_date=inv_in.due_date,
        customer_name=inv_in.customer_name,
        customer_gstin=inv_in.customer_gstin,
        project_ref=inv_in.project_ref,
        taxable_value=inv_in.taxable_value,
        is_interstate=inv_in.is_interstate,
        cgst_amount=tax_calc["cgst"],
        sgst_amount=tax_calc["sgst"],
        igst_amount=tax_calc["igst"],
        total_tax=tax_calc["total_tax"],
        total_invoice_value=tax_calc["total_invoice_value"],
        amount_received=0.0,
        outstanding_balance=tax_calc["total_invoice_value"],
        status="Issued",
        payment_terms=inv_in.payment_terms
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/ap-bills", response_model=List[APBillOut])
def list_ap_bills(db: Session = Depends(get_db)):
    return db.query(APBill).order_by(APBill.bill_date.desc()).all()

@router.post("/ap-bills", response_model=APBillOut)
def create_ap_bill(bill_in: APBillCreate, db: Session = Depends(get_db)):
    tds_calc = calculate_tds(bill_in.taxable_amount, bill_in.tds_section, pan_available=True)
    gross_with_gst = bill_in.taxable_amount + bill_in.gst_amount
    net_payable = gross_with_gst - tds_calc["tds_amount"]
    
    bill = APBill(
        bill_number=bill_in.bill_number,
        bill_date=bill_in.bill_date,
        due_date=bill_in.due_date,
        vendor_name=bill_in.vendor_name,
        po_reference=bill_in.po_reference,
        grn_reference=bill_in.grn_reference,
        expense_category=bill_in.expense_category,
        taxable_amount=bill_in.taxable_amount,
        gst_amount=bill_in.gst_amount,
        tds_section=bill_in.tds_section,
        tds_rate=tds_calc["tds_rate_percent"] / 100.0,
        tds_amount=tds_calc["tds_amount"],
        net_payable=net_payable,
        three_way_match_status="Matched" if bill_in.po_reference else "Not Applicable",
        approval_status="Pending Finance Approval"
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

@router.get("/expense-claims")
def list_expense_claims(db: Session = Depends(get_db)):
    return db.query(ExpenseClaim).order_by(ExpenseClaim.claim_date.desc()).all()

@router.post("/expense-claims")
def create_expense_claim(claim_in: ExpenseClaimCreate, db: Session = Depends(get_db)):
    count = db.query(ExpenseClaim).count() + 1
    claim = ExpenseClaim(
        claim_id=f"ADT-EXP-{count:03d}",
        claim_date=date.today(),
        claimant_name=claim_in.claimant_name,
        claimant_email=claim_in.claimant_email,
        category=claim_in.category,
        business_purpose=claim_in.business_purpose,
        amount_inr=claim_in.amount_inr,
        gst_paid=claim_in.gst_paid,
        project_ref=claim_in.project_ref,
        status="Pending Approval"
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim

@router.get("/bank-reconciliations")
def list_bank_reconciliations(db: Session = Depends(get_db)):
    return db.query(BankReconciliationRecord).all()

@router.get("/journal-entries")
def list_journal_entries(db: Session = Depends(get_db)):
    return db.query(JournalEntry).order_by(JournalEntry.entry_date.desc()).all()

@router.post("/journal-entries")
def create_journal_entry(jv_in: JournalEntryCreate, db: Session = Depends(get_db)):
    count = db.query(JournalEntry).count() + 1
    jv = JournalEntry(
        voucher_number=f"ADT-JV-2026-{count:03d}",
        entry_date=date.today(),
        debit_account=jv_in.debit_account,
        credit_account=jv_in.credit_account,
        amount=jv_in.amount,
        narration=jv_in.narration,
        cost_center=jv_in.cost_center
    )
    db.add(jv)
    db.commit()
    db.refresh(jv)
    return jv

@router.get("/budgets")
def list_budgets(db: Session = Depends(get_db)):
    return db.query(BudgetItem).all()

@router.get("/project-pnl")
def list_project_pnl(db: Session = Depends(get_db)):
    return db.query(ProjectPnL).all()

@router.get("/cashflow-forecast", response_model=List[CashFlowForecastOut])
def get_cashflow_forecast(db: Session = Depends(get_db)):
    return db.query(CashFlowEntry).all()

@router.get("/13-week-forecast")
def get_detailed_13_week_forecast(db: Session = Depends(get_db)):
    return generate_13_week_cashflow_model(db)

@router.get("/fixed-assets")
def list_fixed_assets(db: Session = Depends(get_db)):
    return db.query(FixedAsset).all()

@router.post("/calc-gst")
def api_calculate_gst(taxable_amount: float, is_interstate: bool = False):
    return calculate_gst(taxable_amount, 0.18, is_interstate)

@router.post("/calc-tds")
def api_calculate_tds(gross_amount: float, section: str = "194J"):
    return calculate_tds(gross_amount, section)
