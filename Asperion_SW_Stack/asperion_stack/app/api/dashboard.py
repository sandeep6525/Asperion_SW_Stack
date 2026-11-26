"""
Asperion Enterprise OS - Executive Dashboard & Metrics API
Aggregates top-level KPI metrics across all 8 enterprise operating pillars
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.finance import Invoice, APBill, CashFlowEntry
from app.models.hrms import Employee, Candidate
from app.models.pmo import Project
from app.models.procurement import Vendor
from app.models.cybersecurity import SecurityIncident
from app.models.governance import ComplianceCalendarItem
from app.models.infrastructure import ITAsset, CloudAccount

router = APIRouter(prefix="/dashboard", tags=["Executive Dashboard"])

@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    # Finance metrics
    total_revenue_invoiced = db.query(func.sum(Invoice.total_invoice_value)).scalar() or 0.0
    total_received = db.query(func.sum(Invoice.amount_received)).scalar() or 0.0
    outstanding_ar = db.query(func.sum(Invoice.outstanding_balance)).scalar() or 0.0
    pending_ap = db.query(func.sum(APBill.net_payable)).filter(APBill.approval_status != "Paid").scalar() or 0.0
    
    # Headcount
    active_employees = db.query(Employee).filter(Employee.employment_status == "Active").count()
    active_candidates = db.query(Candidate).filter(Candidate.stage.notin_(["Rejected", "Accepted"])).count()
    
    # PMO
    active_projects = db.query(Project).filter(Project.status.in_(["In Progress", "Planning"])).count()
    
    # Vendors
    total_vendors = db.query(Vendor).filter(Vendor.is_active == True).count()
    
    # SecOps & Compliance
    open_incidents = db.query(SecurityIncident).filter(SecurityIncident.status.notin_(["Closed", "Recovered"])).count()
    cert_in_alerts = db.query(SecurityIncident).filter(
        SecurityIncident.cert_in_reporting_required == True,
        SecurityIncident.cert_in_status.in_(["Drafted", "Not Required"])
    ).count()
    upcoming_compliance = db.query(ComplianceCalendarItem).filter(ComplianceCalendarItem.status == "Upcoming").count()
    
    # IT Assets & Cloud
    total_assets = db.query(ITAsset).count()
    cloud_accounts = db.query(CloudAccount).count()
    total_cloud_spend = db.query(func.sum(CloudAccount.current_month_spend_inr)).scalar() or 0.0
    
    return {
        "status": "success",
        "company": "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
        "cin": "U85500KA2026OPC222069",
        "kpis": {
            "financials": {
                "total_invoiced_inr": total_revenue_invoiced,
                "collections_received_inr": total_received,
                "accounts_receivable_outstanding_inr": outstanding_ar,
                "accounts_payable_due_inr": pending_ap
            },
            "people_hrms": {
                "active_headcount": active_employees,
                "candidates_in_pipeline": active_candidates
            },
            "delivery_pmo": {
                "active_projects": active_projects
            },
            "governance_compliance": {
                "upcoming_statutory_filings": upcoming_compliance
            },
            "secops": {
                "active_security_incidents": open_incidents,
                "cert_in_sla_critical_alerts": cert_in_alerts
            },
            "procurement": {
                "active_vendors": total_vendors
            },
            "infrastructure": {
                "managed_assets": total_assets,
                "cloud_accounts": cloud_accounts,
                "monthly_cloud_spend_inr": total_cloud_spend
            }
        }
    }
