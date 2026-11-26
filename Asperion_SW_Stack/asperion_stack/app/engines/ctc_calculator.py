"""
Asperion Enterprise OS - Statutory CTC & Payroll Engine
Replicates exact formulas from Asperion_Digital_Salary_CTC_Calculator.xlsx
"""
from typing import Dict, Any

def compute_salary_breakup(
    annual_ctc: float,
    basic_pct: float = 0.40,
    hra_pct: float = 0.40,
    state: str = "Karnataka",
    cap_pf_at_ceiling: bool = True,
    include_gratuity: bool = True
) -> Dict[str, Any]:
    """
    Computes standard monthly and annual compensation breakup in compliance with
    Indian Labor Laws (EPFO, ESIC, Karnataka PT, Gratuity Act).
    """
    monthly_ctc = annual_ctc / 12.0
    
    # 1. Earnings: Basic Salary
    monthly_basic = round(monthly_ctc * basic_pct, 2)
    annual_basic = round(monthly_basic * 12.0, 2)
    
    # 2. Earnings: House Rent Allowance (HRA)
    monthly_hra = round(monthly_basic * hra_pct, 2)
    annual_hra = round(monthly_hra * 12.0, 2)
    
    # 3. Employer Statutory Contributions
    # PF Wage: either capped at statutory Rs. 15,000 or actual basic
    pf_wage = min(monthly_basic, 15000.0) if cap_pf_at_ceiling else monthly_basic
    monthly_employer_pf = round(pf_wage * 0.12, 2)
    annual_employer_pf = round(monthly_employer_pf * 12.0, 2)
    
    # ESI: Applicable only if Gross <= 21,000. In corporate roles with CTC >= 3L, typically 0.
    # We estimate based on gross wage threshold.
    esi_applicable = monthly_ctc <= 21000.0
    monthly_employer_esi = round(monthly_ctc * 0.0325, 2) if esi_applicable else 0.0
    annual_employer_esi = round(monthly_employer_esi * 12.0, 2)
    
    # Gratuity Provision (15/26 days per completed year of service = 4.81% of basic)
    monthly_gratuity = round(monthly_basic * (15.0 / 26.0) / 12.0, 2) if include_gratuity else 0.0
    annual_gratuity = round(monthly_gratuity * 12.0, 2)
    
    # 4. Special Allowance / Balancer
    # Balancer = Monthly CTC - (Basic + HRA + Employer PF + Employer ESI + Gratuity)
    monthly_special_allowance = round(
        monthly_ctc - (monthly_basic + monthly_hra + monthly_employer_pf + monthly_employer_esi + monthly_gratuity),
        2
    )
    if monthly_special_allowance < 0:
        # If CTC is low, clamp to 0 and recalculate
        monthly_special_allowance = 0.0
    annual_special_allowance = round(monthly_special_allowance * 12.0, 2)
    
    # Monthly Gross Salary (Earnings)
    monthly_gross = round(monthly_basic + monthly_hra + monthly_special_allowance, 2)
    annual_gross = round(monthly_gross * 12.0, 2)
    
    # 5. Employee Statutory Deductions
    monthly_employee_pf = round(pf_wage * 0.12, 2)
    annual_employee_pf = round(monthly_employee_pf * 12.0, 2)
    
    monthly_employee_esi = round(monthly_gross * 0.0075, 2) if esi_applicable else 0.0
    annual_employee_esi = round(monthly_employee_esi * 12.0, 2)
    
    # Professional Tax (Karnataka Schedule: Rs 200/month if gross salary >= Rs 25,000)
    monthly_pt = 200.0 if (state.lower() == "karnataka" and monthly_gross >= 25000.0) else (
        150.0 if (state.lower() == "karnataka" and monthly_gross >= 15000.0) else 0.0
    )
    annual_pt = round(monthly_pt * 12.0, 2)
    
    # Total Employee Deductions (before Income Tax/TDS)
    monthly_statutory_deductions = round(monthly_employee_pf + monthly_employee_esi + monthly_pt, 2)
    annual_statutory_deductions = round(monthly_statutory_deductions * 12.0, 2)
    
    # Net In-Hand / Take Home Salary (Estimated before personal income tax declarations)
    monthly_net_take_home = round(monthly_gross - monthly_statutory_deductions, 2)
    annual_net_take_home = round(monthly_net_take_home * 12.0, 2)
    
    # Validation check: CTC = Gross + Employer PF + Employer ESI + Gratuity
    computed_annual_ctc = round(annual_gross + annual_employer_pf + annual_employer_esi + annual_gratuity, 2)
    
    return {
        "annual_ctc": annual_ctc,
        "monthly_ctc": monthly_ctc,
        "earnings": {
            "basic_salary": {"monthly": monthly_basic, "annual": annual_basic, "percentage": basic_pct * 100},
            "hra": {"monthly": monthly_hra, "annual": annual_hra, "percentage": hra_pct * 100},
            "special_allowance": {"monthly": monthly_special_allowance, "annual": annual_special_allowance},
            "gross_salary": {"monthly": monthly_gross, "annual": annual_gross}
        },
        "employer_contributions": {
            "employer_pf": {"monthly": monthly_employer_pf, "annual": annual_employer_pf, "rate": "12%"},
            "employer_esi": {"monthly": monthly_employer_esi, "annual": annual_employer_esi, "rate": "3.25%"},
            "gratuity_provision": {"monthly": monthly_gratuity, "annual": annual_gratuity, "rate": "4.81% (15/26)"},
            "total_employer_cost": {
                "monthly": round(monthly_employer_pf + monthly_employer_esi + monthly_gratuity, 2),
                "annual": round(annual_employer_pf + annual_employer_esi + annual_gratuity, 2)
            }
        },
        "employee_deductions": {
            "employee_pf": {"monthly": monthly_employee_pf, "annual": annual_employee_pf, "rate": "12%"},
            "employee_esi": {"monthly": monthly_employee_esi, "annual": annual_employee_esi, "rate": "0.75%"},
            "professional_tax": {"monthly": monthly_pt, "annual": annual_pt, "state": state},
            "total_deductions": {"monthly": monthly_statutory_deductions, "annual": annual_statutory_deductions}
        },
        "take_home": {
            "monthly_net_in_hand": monthly_net_take_home,
            "annual_net_in_hand": annual_net_take_home
        },
        "reconciliation": {
            "input_ctc": annual_ctc,
            "recalculated_ctc": computed_annual_ctc,
            "is_balanced": abs(annual_ctc - computed_annual_ctc) < 1.0
        }
    }
