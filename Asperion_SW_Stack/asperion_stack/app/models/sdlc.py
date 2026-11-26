"""
Asperion Enterprise OS - Comprehensive SDLC & DevSecOps Engineering Models
Standardized against ISO 27001 (A.14 / A.8.25-A.8.34), NIST SP 800-64, OWASP SAMM, and IEEE 12207.
Covers the complete 7-stage SDLC lifecycle:
1. SRS Requirements & Traceability Matrix (RTM)
2. ADR Architecture Decision Records & Tech Stack
3. Code Repositories, Branches & Pull Request Peer Reviews
4. CI/CD Automated Pipelines & DevSecOps Quality Gates (SAST/DAST/SCA)
5. Test Suites, Automated PyTest Runs & Defect Tracking
6. Release Deployments, Semantic Versioning & Rollback Runs
7. Post-Deployment Observability, Telemetry & SRE Error Budgets
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SDLCRequirement(Base):
    """Stage 1: Software Requirements Specification (SRS) & Traceability Matrix (RTM)"""
    __tablename__ = "sdlc_requirements"

    id = Column(Integer, primary_key=True, index=True)
    req_code = Column(String(50), unique=True, index=True) # ADT-REQ-001
    title = Column(String(255), nullable=False)
    category = Column(String(50), default="Functional") # Functional, Non-Functional (NFR), Security (DevSecOps), Performance, Compliance
    priority = Column(String(20), default="High") # MoSCoW: Must Have, Should Have, Could Have, Won't Have
    business_rationale = Column(Text, nullable=True)
    acceptance_criteria = Column(Text, nullable=False) # Gherkin / Given-When-Then
    source_stakeholder = Column(String(100), default="Client Product Sponsor")
    linked_wbs_code = Column(String(50), default="1.1") # Link to PMO WBS
    verification_method = Column(String(50), default="Automated Test") # Automated Test, Code Review, Security Scan, UAT
    status = Column(String(50), default="Approved") # Proposed, In Analysis, Approved, Implemented, Verified, Deprecated
    created_at = Column(DateTime, default=datetime.utcnow)

class ArchitectureDecisionRecord(Base):
    """Stage 2: Architecture Decision Records (ADR) - IEEE / Nygard format"""
    __tablename__ = "sdlc_adrs"

    id = Column(Integer, primary_key=True, index=True)
    adr_number = Column(String(50), unique=True, index=True) # ADR-001
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="Accepted") # Proposed, Accepted, Deprecated, Superseded
    context = Column(Text, nullable=False) # The problem and forces at play
    decision = Column(Text, nullable=False) # The architectural choice made
    consequences = Column(Text, nullable=False) # Positive & negative trade-offs
    compliance_impact = Column(String(255), default="ISO 27001 A.8.25 Secure Architecture")
    author = Column(String(100), default="Lead Architect (Arjun Sharma)")
    date_approved = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)

class CodeRepository(Base):
    """Stage 3: Git Version Control Repository Master"""
    __tablename__ = "sdlc_repositories"

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String(100), unique=True, index=True) # asperion-enterprise-os
    git_url = Column(String(255), nullable=False)
    default_branch = Column(String(50), default="main")
    branch_protection_rule = Column(String(100), default="Require 2 Reviews + CI Pass + Signed Commits")
    primary_language = Column(String(50), default="Python 3.14 / TypeScript")
    framework = Column(String(50), default="FastAPI / Tailwind / SQLite WAL")
    open_pull_requests_count = Column(Integer, default=0)
    health_score_pct = Column(Float, default=98.5)
    created_at = Column(DateTime, default=datetime.utcnow)

class PullRequestReview(Base):
    """Stage 3: Peer Code Review & Branch Merge Governance"""
    __tablename__ = "sdlc_pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(String(50), unique=True, index=True) # PR #42
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    source_branch = Column(String(100), default="feature/statutory-pt-calc")
    target_branch = Column(String(50), default="main")
    description = Column(Text, nullable=True)
    lines_added = Column(Integer, default=150)
    lines_deleted = Column(Integer, default=20)
    peer_reviewers = Column(String(255), default="Vikram Rathore, Sneha Rao")
    review_status = Column(String(50), default="Approved") # Open, Review Required, Approved, Merged, Closed
    security_signoff = Column(Boolean, default=True) # DevSecOps Peer Signoff
    merged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CICDPipelineRun(Base):
    """Stage 4: CI/CD Automated Build, Test & DevSecOps Quality Gates"""
    __tablename__ = "sdlc_pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_code = Column(String(50), unique=True, index=True) # PIPE-2026-089
    commit_sha = Column(String(64), nullable=False) # e.g. 7f8a9b2c
    branch = Column(String(50), default="main")
    triggered_by = Column(String(100), default="Arjun Sharma (Lead Architect)")
    duration_seconds = Column(Integer, default=145)
    
    # DevSecOps Quality Gates
    build_status = Column(String(30), default="SUCCESS") # SUCCESS, FAILED, RUNNING
    unit_tests_passed = Column(Integer, default=94)
    unit_tests_failed = Column(Integer, default=0)
    test_coverage_pct = Column(Float, default=94.2)
    sast_tool = Column(String(50), default="Bandit / Semgrep")
    sast_vulnerabilities_found = Column(Integer, default=0) # Must be 0 for gate pass
    sca_tool = Column(String(50), default="pip-audit / OWASP Dependency-Check")
    vulnerable_dependencies = Column(Integer, default=0)
    secret_leak_scan_status = Column(String(30), default="CLEAN") # CLEAN, LEAK_DETECTED
    quality_gate_result = Column(String(30), default="PASSED") # PASSED, BLOCKED, FAILED
    artifacts_generated = Column(String(255), default="docker-image:v1.0.89, srv-tar.gz")
    created_at = Column(DateTime, default=datetime.utcnow)

class DefectBugRecord(Base):
    """Stage 5: Software Defect & Bug Tracking (IEEE 1044 / ISO 25010)"""
    __tablename__ = "sdlc_defects"

    id = Column(Integer, primary_key=True, index=True)
    bug_id = Column(String(50), unique=True, index=True) # BUG-2026-007
    title = Column(String(255), nullable=False)
    severity = Column(String(30), default="S3-Medium") # S1-Blocker, S2-Critical, S3-Medium, S4-Minor / Cosmetic
    environment = Column(String(30), default="Staging") # Local, Staging / Pre-Prod, Production
    module_affected = Column(String(50), default="HRMS / Attendance")
    steps_to_reproduce = Column(Text, nullable=True)
    actual_behavior = Column(Text, nullable=True)
    expected_behavior = Column(Text, nullable=True)
    assigned_engineer = Column(String(100), default="Arjun Sharma")
    reported_by = Column(String(100), default="Sneha Rao (QA Lead)")
    fix_commit_sha = Column(String(64), nullable=True)
    status = Column(String(50), default="Resolved & Verified") # Logged, In Triaging, In Fixing, Fixed, Retested & Verified, Closed
    created_at = Column(DateTime, default=datetime.utcnow)

class ReleaseDeployment(Base):
    """Stage 6: Formal Production Releases, Semantic Versioning & Rollbacks"""
    __tablename__ = "sdlc_releases"

    id = Column(Integer, primary_key=True, index=True)
    release_tag = Column(String(50), unique=True, index=True) # v1.0.0, v1.1.0
    environment = Column(String(30), default="Production") # Staging, Production
    deployment_strategy = Column(String(50), default="Blue-Green / Zero Downtime") # Rolling, Blue-Green, Canary
    change_advisory_board_approval = Column(String(100), default="Approved by Varadi Vijay (CAB Chair)")
    release_notes = Column(Text, nullable=False)
    rollback_plan = Column(Text, default="Automated instant rollback to previous container digest in 30 seconds.")
    downtime_minutes = Column(Float, default=0.0)
    smoke_test_status = Column(String(30), default="PASSED") # PASSED, FAILED
    deployed_by = Column(String(100), default="Vikram Rathore (Release Manager)")
    deployment_status = Column(String(50), default="Healthy & Live") # In Progress, Healthy & Live, Rolled Back
    deployed_at = Column(DateTime, default=datetime.utcnow)

class SREObservabilityMetric(Base):
    """Stage 7: SRE Telemetry, SLO/SLA Error Budgets & Application Health"""
    __tablename__ = "sdlc_observability"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), default="asperion-core-api")
    p95_latency_ms = Column(Float, default=8.4) # p95 latency
    p99_latency_ms = Column(Float, default=14.2) # p99 latency
    uptime_30d_pct = Column(Float, default=99.98) # 99.98% uptime
    error_rate_pct = Column(Float, default=0.02) # HTTP 5xx rate
    error_budget_remaining_pct = Column(Float, default=88.5) # SLO Error budget
    active_memory_mb = Column(Float, default=184.5)
    cpu_utilization_pct = Column(Float, default=12.4)
    active_db_connections = Column(Integer, default=5)
    recorded_at = Column(DateTime, default=datetime.utcnow)
