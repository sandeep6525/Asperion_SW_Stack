"""
Unit tests for the SecOps Triage & CERT-In Workflow Engine
"""
import pytest
from app.engines.secops_triage import triage_security_incident

def test_ransomware_triage_triggers_cert_in():
    res = triage_security_incident(
        category="Ransomware Outbreak",
        affected_systems="Core Production Database & File Share",
        data_classification="Confidential",
        is_customer_facing=True,
        estimated_impacted_users=500
    )
    
    assert res["severity"] == "P1-Critical"
    assert res["war_room_required"] is True
    assert res["cert_in_statutory_reporting"]["mandatory"] is True
    assert res["cert_in_statutory_reporting"]["deadline"] is not None
    assert res["recommended_playbook"]["code"] == "PB-SEC-01"

def test_minor_phishing_triage():
    res = triage_security_incident(
        category="Phishing Attempt",
        affected_systems="Corporate Email Box",
        data_classification="Internal",
        is_customer_facing=False,
        estimated_impacted_users=1
    )
    
    assert res["severity"] == "P3-Medium"
    assert res["war_room_required"] is False
    assert res["recommended_playbook"]["code"] == "PB-SEC-03"
