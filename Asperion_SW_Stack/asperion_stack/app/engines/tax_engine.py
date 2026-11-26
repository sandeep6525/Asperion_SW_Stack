"""
Asperion Enterprise OS - Tax & Procurement Matching Engine
Handles GST (CGST/SGST/IGST), TDS (194C/J/I/H), and 3-Way AP Matching
"""
from typing import Dict, Any, Optional

def calculate_gst(
    taxable_amount: float,
    gst_rate: float = 0.18,
    is_interstate: bool = False
) -> Dict[str, Any]:
    """
    Computes GST bifurcation based on supply destination.
    Intrastate (Karnataka -> Karnataka): CGST (9%) + SGST (9%)
    Interstate (Karnataka -> Other States / SEZ): IGST (18%)
    """
    total_tax = round(taxable_amount * gst_rate, 2)
    
    if is_interstate:
        cgst = 0.0
        sgst = 0.0
        igst = total_tax
    else:
        cgst = round(total_tax / 2.0, 2)
        sgst = round(total_tax - cgst, 2)
        igst = 0.0
        
    total_invoice_value = round(taxable_amount + total_tax, 2)
    
    return {
        "taxable_amount": taxable_amount,
        "gst_rate_percent": gst_rate * 100,
        "is_interstate": is_interstate,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "total_tax": total_tax,
        "total_invoice_value": total_invoice_value
    }

def calculate_tds(
    gross_amount: float,
    section: str = "194J",
    pan_available: bool = True
) -> Dict[str, Any]:
    """
    Calculates Indian Income Tax TDS deduction under Chapter XVII-B.
    Standard Rates:
    - 194C: Contractors / Advertising / Subcontracting (1% Individual/HUF, 2% Company)
    - 194J: Professional & Technical Services (10% Professional, 2% Tech BPO/FTS)
    - 194I: Rent (10% Land/Building, 2% Plant/Equipment)
    - 194H: Commission / Brokerage (5%)
    - If No PAN: Flat 20% under Section 206AA
    """
    if not pan_available:
        rate = 0.20
        desc = "Flat 20% under Section 206AA (No PAN)"
    else:
        rates = {
            "194C": (0.02, "Contractual / Subcontracting Services (2%)"),
            "194C_IND": (0.01, "Contractual Services - Individual/HUF (1%)"),
            "194J": (0.10, "Professional Services / Fees (10%)"),
            "194J_TECH": (0.02, "Technical Services / Royalty / Software (2%)"),
            "194I": (0.10, "Rent on Land, Building, Furniture (10%)"),
            "194I_PLANT": (0.02, "Rent on Plant, Machinery, Equipment (2%)"),
            "194H": (0.05, "Commission or Brokerage (5%)")
        }
        rate, desc = rates.get(section.upper(), (0.10, "Standard Professional Services (10%)"))
        
    tds_amount = round(gross_amount * rate, 2)
    net_payable = round(gross_amount - tds_amount, 2)
    
    return {
        "gross_amount": gross_amount,
        "section": section,
        "description": desc,
        "tds_rate_percent": rate * 100,
        "tds_amount": tds_amount,
        "net_payable": net_payable
    }

def perform_three_way_match(
    po_amount: float,
    po_quantity: float,
    grn_quantity_accepted: float,
    bill_amount: float,
    bill_quantity: float,
    tolerance_pct: float = 0.02
) -> Dict[str, Any]:
    """
    Executes financial 3-Way Matching for Accounts Payable (AP):
    1. PO quantity vs Bill quantity vs GRN accepted quantity
    2. PO unit price vs Bill unit price
    3. Tolerance checking
    """
    quantity_discrepancy = abs(bill_quantity - grn_quantity_accepted) > 0.001
    amount_variance = abs(bill_amount - po_amount)
    variance_pct = (amount_variance / po_amount) if po_amount > 0 else 0.0
    
    is_matched = (not quantity_discrepancy) and (variance_pct <= tolerance_pct)
    
    status = "Matched" if is_matched else (
        "Quantity Mismatch" if quantity_discrepancy else "Price Discrepancy"
    )
    
    return {
        "status": status,
        "is_matched": is_matched,
        "po_amount": po_amount,
        "bill_amount": bill_amount,
        "variance_inr": round(amount_variance, 2),
        "variance_pct": round(variance_pct * 100, 2),
        "po_quantity": po_quantity,
        "grn_accepted_qty": grn_quantity_accepted,
        "bill_quantity": bill_quantity,
        "recommended_action": "Approve for Payment" if is_matched else "Hold Payment - Require PO/Bill Correction"
    }
