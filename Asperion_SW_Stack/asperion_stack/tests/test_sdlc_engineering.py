"""
Asperion Enterprise OS - Comprehensive Test Suite for SDLC & DevSecOps Engineering
Validates the full 7-stage engineering lifecycle:
1. SRS Requirements & Traceability Matrix (RTM / ISO 29148)
2. Architecture Decision Records (ADRs / IEEE / Nygard format)
3. Code Repositories & 4-Eyes Pull Request Reviews (ISO 27001 A.8.28)
4. CI/CD Automated Pipelines with DevSecOps Quality Gates (SAST/SCA/Coverage)
5. IEEE 1044 / ISO 25010 Defect & Bug Tracking
6. Semantic Release Management & CAB Approvals (Zero-Downtime Blue/Green)
7. SRE Observability Telemetry & Error Budget Tracking
8. SDLC Cockpit Overview Metrics
"""
import uuid
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.api.sdlc import (
    list_requirements, create_requirement,
    list_adrs, create_adr,
    list_repositories,
    list_pull_requests, create_pull_request,
    list_pipeline_runs, trigger_pipeline_run,
    list_defects, create_defect,
    list_releases, create_release,
    list_observability_metrics,
    get_sdlc_overview
)
from app.schemas.sdlc import (
    SDLCRequirementCreate, ADRCreate,
    PullRequestCreate,
    CICDPipelineRunCreate, DefectBugCreate, ReleaseDeploymentCreate
)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_sdlc_srs_requirements_and_rtm(db_session):
    # 1. List Requirements
    reqs = list_requirements(db=db_session)
    assert len(reqs) >= 5
    assert any(r.req_code == "ADT-REQ-001" for r in reqs)
    assert any(r.req_code == "ADT-REQ-002" for r in reqs)

    # 2. Create New SRS Requirement
    uniq_code = f"ADT-REQ-TEST-{uuid.uuid4().hex[:4].upper()}"
    new_req = SDLCRequirementCreate(
        req_code=uniq_code,
        title="Zero Trust WebAuthn & FIDO2 Hardware Key Authentication",
        category="Security (DevSecOps)",
        priority="Must Have",
        business_rationale="Protect administrative and executive portals against credential theft and phishing attacks.",
        acceptance_criteria="Enforce WebAuthn level 2 authentication with hardware key challenge-response.",
        source_stakeholder="Priya Nair (CISO Lead)",
        linked_wbs_code="3.1",
        verification_method="Automated Test"
    )
    created = create_requirement(req_in=new_req, db=db_session)
    assert created.req_code == uniq_code
    assert created.priority == "Must Have"
    assert created.status in ["Approved", "Draft / Under Review"]


def test_sdlc_architecture_decision_records(db_session):
    # 1. List ADRs
    adrs = list_adrs(db=db_session)
    assert len(adrs) >= 3
    assert any(a.adr_number == "ADR-001" for a in adrs)
    assert any(a.adr_number == "ADR-002" for a in adrs)
    assert any(a.adr_number == "ADR-003" for a in adrs)

    # 2. Create New ADR
    uniq_adr = f"ADR-{uuid.uuid4().hex[:8].upper()}"
    new_adr = ADRCreate(
        adr_number=uniq_adr,
        title="Autonomous Self-Healing Background Watcher Thread Pattern",
        status="Accepted",
        context="System requires continuous automated reconciliation of attendance anomalies and statutory filings without external cron dependencies.",
        decision="Implement in-process background watcher daemon with threading and safe transaction boundary.",
        consequences="Self-contained execution in any container runtime; memory footprint bounded under 200MB.",
        compliance_impact="ISO 27001 A.8.19 & ITIL Continuous Service Improvement",
        author="Arjun Sharma (Lead Architect)"
    )
    created = create_adr(adr_in=new_adr, db=db_session)
    assert created.adr_number == uniq_adr
    assert created.status == "Accepted"


def test_sdlc_code_repositories_and_prs(db_session):
    # 1. List Repositories
    repos = list_repositories(db=db_session)
    assert len(repos) >= 1
    assert any("asperion" in r.repo_name for r in repos)

    # 2. List Pull Requests
    prs = list_pull_requests(db=db_session)
    assert len(prs) >= 2
    assert any(p.security_signoff is True for p in prs)

    # 3. Create PR
    new_pr = PullRequestCreate(
        pr_number=f"PR #{uuid.uuid4().hex[:6].upper()}",
        title="feat: SDLC test coverage & automated quality gates",
        author="Sneha Rao",
        source_branch="test/sdlc-coverage",
        target_branch="main",
        description="Comprehensive PyTest test suites for all 7 SDLC stages.",
        lines_added=350,
        lines_deleted=12,
        peer_reviewers="Arjun Sharma, Vikram Rathore"
    )
    created = create_pull_request(pr_in=new_pr, db=db_session)
    assert created.review_status in ["Approved", "Open / In Review"]
    assert created.lines_added == 350


def test_sdlc_cicd_pipelines_and_trigger(db_session):
    # 1. List Pipelines
    pipelines = list_pipeline_runs(db=db_session)
    assert len(pipelines) >= 2
    for p in pipelines:
        assert p.sast_vulnerabilities_found == 0
        assert p.vulnerable_dependencies == 0
        assert p.secret_leak_scan_status == "CLEAN"
        assert p.quality_gate_result == "PASSED"

    # 2. Trigger Pipeline Run
    uniq_pipe = f"PIPE-2026-{uuid.uuid4().hex[:6].upper()}"
    trigger = CICDPipelineRunCreate(
        pipeline_code=uniq_pipe,
        commit_sha=f"{uuid.uuid4().hex[:12]}",
        branch="main",
        triggered_by="Arjun Sharma (Lead Architect)",
        duration_seconds=115
    )
    run = trigger_pipeline_run(pipe_in=trigger, db=db_session)
    assert run.build_status == "SUCCESS"
    assert run.quality_gate_result == "PASSED"
    assert run.unit_tests_passed >= 90
    assert run.test_coverage_pct >= 90.0
    assert run.sast_vulnerabilities_found == 0


def test_sdlc_ieee1044_defect_tracking(db_session):
    # 1. List Defects
    defects = list_defects(db=db_session)
    assert len(defects) >= 2
    assert any(d.bug_id == "BUG-2026-001" for d in defects)

    # 2. Log New Defect
    uniq_bug = f"BUG-2026-{uuid.uuid4().hex[:6].upper()}"
    new_bug = DefectBugCreate(
        bug_id=uniq_bug,
        title="Minor CSS alignment on 1440p ultra-wide monitors",
        severity="S4-Minor / Cosmetic",
        environment="Staging",
        module_affected="Frontend UI / Cockpit",
        steps_to_reproduce="Open cockpit on 3440x1440 resolution display.",
        actual_behavior="Card gap expands to 32px instead of uniform 24px.",
        expected_behavior="Max-width container keeps uniform 24px padding.",
        assigned_engineer="Sneha Rao",
        reported_by="QA Team"
    )
    created = create_defect(bug_in=new_bug, db=db_session)
    assert created.bug_id == uniq_bug
    assert created.status in ["Open", "Resolved & Verified"]


def test_sdlc_releases_and_deployments(db_session):
    # 1. List Releases
    releases = list_releases(db=db_session)
    assert len(releases) >= 2
    assert any(r.release_tag == "v1.0.0" for r in releases)
    assert any(r.deployment_status == "Healthy & Live" for r in releases)

    # 2. Create Release
    uniq_ver = f"v1.2.0-{uuid.uuid4().hex[:6]}"
    new_rel = ReleaseDeploymentCreate(
        release_tag=uniq_ver,
        environment="Staging",
        deployment_strategy="Blue-Green / Zero Downtime",
        change_advisory_board_approval="Approved by CAB (Director Varadi Vijay)",
        release_notes="Comprehensive SDLC, RTM traceability, and SRE error budget metrics.",
        rollback_plan="Immediate 10-second DNS flip to previous active color target group."
    )
    created = create_release(rel_in=new_rel, db=db_session)
    assert created.release_tag == uniq_ver
    assert created.deployment_status == "Healthy & Live"
    assert created.smoke_test_status == "PASSED"


def test_sdlc_sre_observability(db_session):
    obs_list = list_observability_metrics(db=db_session)
    assert len(obs_list) >= 1
    obs = obs_list[0]
    assert obs.service_name == "asperion-core-api"
    assert obs.p95_latency_ms <= 15.0
    assert obs.p99_latency_ms <= 30.0
    assert obs.uptime_30d_pct >= 99.9
    assert obs.error_rate_pct <= 0.1
    assert obs.error_budget_remaining_pct >= 90.0


def test_sdlc_cockpit_overview(db_session):
    overview = get_sdlc_overview(db=db_session)
    assert overview["status"] == "success"
    assert "sdlc_kpis" in overview
    kpis = overview["sdlc_kpis"]
    assert kpis["total_requirements"] >= 5
    assert kpis["approved_adrs"] >= 3
    assert kpis["pipeline_pass_rate_pct"] == 100.0
    assert kpis["code_coverage_pct"] >= 90.0
    assert kpis["p95_latency_ms"] <= 15.0
    assert "devsecops_gates" in overview
