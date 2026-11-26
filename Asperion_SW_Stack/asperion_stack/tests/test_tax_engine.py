"""
Unit tests for the Tax & 3-Way Matching Engine
"""
import pytest
from app.engines.tax_engine import calculate_gst, calculate_tds, perform_three_way_match

def test_gst_intrastate():
    res = calculate_gst(taxable_amount=100000.0, gst_rate=0.18, is_interstate=False)
    assert res["taxable_amount"] == 100000.0
    assert res["cgst"] == 9000.0
    assert res["sgst"] == 9000.0
    assert res["igst"] == 0.0
    assert res["total_tax"] == 18000.0
    assert res["total_invoice_value"] == 118000.0

def test_gst_interstate():
    res = calculate_gst(taxable_amount=200000.0, gst_rate=0.18, is_interstate=True)
    assert res["cgst"] == 0.0
    assert res["sgst"] == 0.0
    assert res["igst"] == 36000.0
    assert res["total_invoice_value"] == 236000.0

def test_tds_194j_professional():
    res = calculate_tds(gross_amount=50000.0, section="194J", pan_available=True)
    assert res["tds_rate_percent"] == 10.0
    assert res["tds_amount"] == 5000.0
    assert res["net_payable"] == 45000.0

def test_tds_194c_contractor():
    res = calculate_tds(gross_amount=100000.0, section="194C", pan_available=True)
    assert res["tds_rate_percent"] == 2.0
    assert res["tds_amount"] == 2000.0
    assert res["net_payable"] == 98000.0

def test_three_way_match_success():
    res = perform_three_way_match(
        po_amount=100000.0, po_quantity=10,
        grn_quantity_accepted=10,
        bill_amount=100000.0, bill_quantity=10
    )
    assert res["is_matched"] is True
    assert res["status"] == "Matched"

def test_three_way_match_quantity_mismatch():
    res = perform_three_way_match(
        po_amount=100000.0, po_quantity=10,
        grn_quantity_accepted=8, # accepted 8
        bill_amount=100000.0, bill_quantity=10 # billed 10
    )
    assert res["is_matched"] is False
    assert res["status"] == "Quantity Mismatch"
