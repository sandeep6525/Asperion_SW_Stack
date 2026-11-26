"""
Unit tests for the Statutory CTC & Compensation Engine
"""
import pytest
from app.engines.ctc_calculator import compute_salary_breakup

def test_ctc_calculator_12_lakhs():
    ctc = 1200000.0 # 12 LPA
    breakup = compute_salary_breakup(annual_ctc=ctc, basic_pct=0.40, hra_pct=0.40, state="Karnataka")
    
    assert breakup["annual_ctc"] == 1200000.0
    assert breakup["monthly_ctc"] == 100000.0
    
    # Monthly Basic = 40% of 100,000 = 40,000
    assert breakup["earnings"]["basic_salary"]["monthly"] == 40000.0
    
    # Monthly HRA = 40% of 40,000 = 16,000
    assert breakup["earnings"]["hra"]["monthly"] == 16000.0
    
    # Employer PF capped at 15,000 ceiling: 12% of 15,000 = 1,800
    assert breakup["employer_contributions"]["employer_pf"]["monthly"] == 1800.0
    
    # Gratuity provision (15/26) = 40,000 * (15/26) / 12 = 1,923.08
    assert abs(breakup["employer_contributions"]["gratuity_provision"]["monthly"] - 1923.08) < 1.0
    
    # Employee PF = 1,800
    assert breakup["employee_deductions"]["employee_pf"]["monthly"] == 1800.0
    
    # Karnataka Professional Tax = Rs 200
    assert breakup["employee_deductions"]["professional_tax"]["monthly"] == 200.0
    
    # CTC is balanced
    assert breakup["reconciliation"]["is_balanced"] is True

def test_ctc_calculator_5_lakhs():
    ctc = 500000.0 # 5 LPA
    breakup = compute_salary_breakup(annual_ctc=ctc, basic_pct=0.50, hra_pct=0.50, state="Karnataka")
    
    assert breakup["reconciliation"]["is_balanced"] is True
    assert breakup["take_home"]["monthly_net_in_hand"] > 0
