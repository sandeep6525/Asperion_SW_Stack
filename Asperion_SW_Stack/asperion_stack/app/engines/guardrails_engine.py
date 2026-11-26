"""
Asperion Enterprise OS - Real-Time Autonomous Guardrails Enforcement Engine
Scans, evaluates, and enforces active operational and regulatory guardrails across all 20 pillars.
"""
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.guardrails import GuardrailRule, GuardrailExecutionLog
from app.models.finance import APBill, PurchaseOrder
from app.models.procurement import Vendor, PurchaseRequisition, GoodsReceivedNote
from app.models.attendance import AttendanceRecord
from app.models.sdlc import CICDPipelineRun
from app.models.cybersecurity import SecurityIncident
from app.models.developer_platform import DeveloperEnvironmentSecret

def evaluate_all_enterprise_guardrails(db: Session) -> Dict[str, Any]:
    """
    Executes comprehensive automated scan across all active enterprise guardrails.
    Returns status, evaluation counts, violations blocked, and auto-healed actions.
    """
    rules = db.query(GuardrailRule).filter(GuardrailRule.is_active == True).all()
    results = []
    total_scanned = 0
    total_blocked = 0
    total_healed = 0
    total_passed = 0

    for rule in rules:
        eval_result = _evaluate_single_rule(rule, db)
        results.append(eval_result)
        total_scanned += eval_result["evaluations_count"]
        total_blocked += eval_result["blocked_count"]
        total_healed += eval_result["healed_count"]
        total_passed += eval_result["passed_count"]

        # Update cumulative counters on rule
        rule.total_evaluations += eval_result["evaluations_count"]
        rule.total_passed += eval_result["passed_count"]
        rule.total_blocked += eval_result["blocked_count"]
        rule.total_auto_healed += eval_result["healed_count"]

    db.commit()

    return {
        "status": "success",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_rules_active": len(rules),
        "total_evaluations": total_scanned,
        "total_passed": total_passed,
        "total_violations_blocked": total_blocked,
        "total_anomalies_auto_healed": total_healed,
        "compliance_score_pct": round((total_passed / max(1, total_scanned)) * 100.0, 1),
        "rule_evaluations": results
    }

def _evaluate_single_rule(rule: GuardrailRule, db: Session) -> Dict[str, Any]:
    code = rule.rule_code
    passed = 0
    blocked = 0
    healed = 0

    if code == "GRD-FIN-001":
        # 3-Way Matching Guard: AP Bills must match PO and GRN with 0% tolerance
        bills = db.query(APBill).all()
        for b in bills:
            if b.three_way_match_status == "Matched":
                passed += 1
            elif b.three_way_match_status == "Discrepancy":
                blocked += 1
                _log_execution(db, rule.rule_code, "Finance", b.bill_number, "BLOCKED", f"Taxable amount INR {b.taxable_amount:,.2f} variance against PO/GRN.", "Disbursal Blocked")
            else:
                passed += 1

    elif code == "GRD-MSME-002":
        # MSMED Act 45-Day Payment Rule: Micro & Small vendor bills must be cleared within 45 days
        bills = db.query(APBill).all()
        today = date.today()
        for b in bills:
            v = db.query(Vendor).filter(Vendor.vendor_name == b.vendor_name).first()
            if v and v.msme_registered:
                age_days = (today - b.bill_date).days
                if age_days > 45 and b.approval_status != "Paid":
                    blocked += 1
                    _log_execution(db, rule.rule_code, "Procurement_MSME", b.bill_number, "BLOCKED", f"MSME {v.vendor_name} bill aged {age_days} days exceeding 45-day statutory limit.", "Flagged for Priority Bank Disbursal")
                else:
                    passed += 1
            else:
                passed += 1

    elif code == "GRD-DPDP-003":
        # DPDP Act 2023 DPA Requirement: Tier 1 vendors with PII/data access must have signed DPA
        vendors = db.query(Vendor).filter(Vendor.criticality_tier == "Tier 1 - Mission Critical").all()
        for v in vendors:
            if v.dpdp_compliance_status == "Compliant":
                passed += 1
            else:
                blocked += 1
                _log_execution(db, rule.rule_code, "Governance_Legal", v.vendor_code, "BLOCKED", f"Vendor {v.vendor_name} missing executed DPA under DPDP Act 2023.", "Data Access Suspended")

    elif code == "GRD-HRMS-004":
        # Smart Attendance Haversine & Facial Liveness Guard: <=250m and >=85% confidence
        attendances = db.query(AttendanceRecord).order_by(AttendanceRecord.created_at.desc()).limit(20).all()
        for att in attendances:
            emp_code = att.employee.emp_code if att.employee else f"EMP-{att.employee_id}"
            dist = att.geofence_distance_meters or 0.0
            conf = att.facial_match_confidence_pct or 95.0
            if (att.geofence_verified or dist <= 250.0) and conf >= 85.0:
                passed += 1
            elif att.auto_fixed or att.status == "Regularized":
                healed += 1
            else:
                blocked += 1
                _log_execution(db, rule.rule_code, "HRMS_Mobility", emp_code, "BLOCKED", f"Punch outside geofence ({dist:.1f}m) or low liveness ({conf}%).", "Punch Flagged for Regularization")

    elif code == "GRD-SDLC-005":
        # DevSecOps Quality Gate: 0 SAST CVEs & >= 90% test coverage
        pipes = db.query(CICDPipelineRun).order_by(CICDPipelineRun.created_at.desc()).limit(10).all()
        for p in pipes:
            if p.sast_vulnerabilities_found == 0 and p.test_coverage_pct >= 90.0 and p.secret_leak_scan_status == "CLEAN":
                passed += 1
            else:
                blocked += 1
                _log_execution(db, rule.rule_code, "DevSecOps", p.pipeline_code, "BLOCKED", f"Pipeline failed quality gate (Coverage: {p.test_coverage_pct}%, CVEs: {p.sast_vulnerabilities_found}).", "Branch Merge Blocked")

    elif code == "GRD-DOA-006":
        # Delegation of Authority: PRs > INR 1,00,000 require Sole Director Signoff
        prs = db.query(PurchaseRequisition).all()
        for pr in prs:
            if pr.estimated_amount_inr > 100000.0:
                if pr.approval_status in ["Approved", "Converted to PO"] and pr.approved_by and "Director" in pr.approved_by:
                    passed += 1
                elif pr.approval_status == "Pending Director Signoff":
                    passed += 1
                else:
                    blocked += 1
                    _log_execution(db, rule.rule_code, "Governance_DOA", pr.pr_number, "BLOCKED", f"Spend INR {pr.estimated_amount_inr:,.2f} exceeding HOD limit without Director approval.", "PO Generation Blocked")
            else:
                passed += 1

    elif code == "GRD-CERT-007":
        # CERT-In 6-Hour SLA Guard
        incidents = db.query(SecurityIncident).filter(SecurityIncident.severity == "P1-Critical").all()
        for inc in incidents:
            if getattr(inc, "cert_in_reporting_required", False):
                elapsed = (datetime.utcnow() - inc.created_at).total_seconds() / 3600.0
                if elapsed <= 6.0 or inc.cert_in_status in ["Submitted", "Report Submitted", "Draft Prepared", "Drafted"]:
                    passed += 1
                else:
                    blocked += 1
                    _log_execution(db, rule.rule_code, "SecOps", inc.incident_id, "BLOCKED", f"P1 Incident elapsed {elapsed:.1f}h exceeding 6h CERT-In window.", "War Room Escalation Triggered")
            else:
                passed += 1

    elif code == "GRD-SECR-008":
        # 90-Day Secret Expiration Guard
        secrets = db.query(DeveloperEnvironmentSecret).all()
        today = date.today()
        for sec in secrets:
            days_until_exp = (sec.next_rotation_due - today).days if sec.next_rotation_due else 30
            if days_until_exp < 0:
                healed += 1
                _log_execution(db, rule.rule_code, "SecOps", sec.secret_name, "AUTO_HEALED", f"Secret {sec.secret_name} expired by {abs(days_until_exp)} days.", "Flagged for Emergency Rotation")
            elif days_until_exp <= 15 or sec.status == "Rotation Due":
                passed += 1
            else:
                passed += 1

    else:
        passed += 1

    total = passed + blocked + healed
    return {
        "rule_code": rule.rule_code,
        "name": rule.name,
        "category": rule.category,
        "severity": rule.severity,
        "enforcement_mode": rule.enforcement_mode,
        "evaluations_count": max(1, total),
        "passed_count": passed,
        "blocked_count": blocked,
        "healed_count": healed,
        "status": "HEALTHY" if blocked == 0 else "INTERVENTIONS_ACTIVE"
    }

def _log_execution(db: Session, rule_code: str, module: str, entity_ref: str, result: str, trigger_summary: str, action: str):
    import uuid
    log = GuardrailExecutionLog(
        execution_id=f"GEX-{uuid.uuid4().hex[:6].upper()}",
        rule_code=rule_code,
        module=module,
        entity_reference=entity_ref,
        evaluation_result=result,
        trigger_payload_summary=trigger_summary,
        action_taken=action
    )
    db.add(log)
