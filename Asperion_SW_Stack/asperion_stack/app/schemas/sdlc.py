"""
Asperion Enterprise OS - SDLC & DevSecOps Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

# 1. Requirements
class SDLCRequirementCreate(BaseModel):
    req_code: str
    title: str
    category: str = "Functional"
    priority: str = "High"
    business_rationale: Optional[str] = None
    acceptance_criteria: str
    source_stakeholder: str = "Client Product Sponsor"
    linked_wbs_code: str = "1.1"
    verification_method: str = "Automated Test"

class SDLCRequirementOut(SDLCRequirementCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# 2. ADR
class ADRCreate(BaseModel):
    adr_number: str
    title: str
    context: str
    decision: str
    consequences: str
    compliance_impact: str = "ISO 27001 A.8.25 Secure Architecture"
    author: str = "Lead Architect"

class ADROut(ADRCreate):
    id: int
    status: str
    date_approved: date
    created_at: datetime
    class Config:
        from_attributes = True

# 3. Code Repo & PRs
class CodeRepositoryOut(BaseModel):
    id: int
    repo_name: str
    git_url: str
    default_branch: str
    branch_protection_rule: str
    primary_language: str
    framework: str
    open_pull_requests_count: int
    health_score_pct: float
    created_at: datetime
    class Config:
        from_attributes = True

class PullRequestCreate(BaseModel):
    pr_number: str
    title: str
    author: str
    source_branch: str = "feature/new-enhancement"
    target_branch: str = "main"
    description: Optional[str] = None
    lines_added: int = 50
    lines_deleted: int = 5
    peer_reviewers: str = "Vikram Rathore, Sneha Rao"

class PullRequestOut(PullRequestCreate):
    id: int
    review_status: str
    security_signoff: bool
    merged_at: Optional[datetime]
    created_at: datetime
    class Config:
        from_attributes = True

# 4. CI/CD Pipeline Run
class CICDPipelineRunCreate(BaseModel):
    pipeline_code: str
    commit_sha: str
    branch: str = "main"
    triggered_by: str = "Lead Engineer"
    duration_seconds: int = 120

class CICDPipelineRunOut(CICDPipelineRunCreate):
    id: int
    build_status: str
    unit_tests_passed: int
    unit_tests_failed: int
    test_coverage_pct: float
    sast_tool: str
    sast_vulnerabilities_found: int
    sca_tool: str
    vulnerable_dependencies: int
    secret_leak_scan_status: str
    quality_gate_result: str
    artifacts_generated: str
    created_at: datetime
    class Config:
        from_attributes = True

# 5. Defect & Bug Tracking
class DefectBugCreate(BaseModel):
    bug_id: str
    title: str
    severity: str = "S3-Medium"
    environment: str = "Staging"
    module_affected: str = "HRMS / Attendance"
    steps_to_reproduce: Optional[str] = None
    actual_behavior: Optional[str] = None
    expected_behavior: Optional[str] = None
    assigned_engineer: str = "Arjun Sharma"
    reported_by: str = "Sneha Rao (QA Lead)"

class DefectBugOut(DefectBugCreate):
    id: int
    fix_commit_sha: Optional[str]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# 6. Release & Deployment
class ReleaseDeploymentCreate(BaseModel):
    release_tag: str
    environment: str = "Production"
    deployment_strategy: str = "Blue-Green / Zero Downtime"
    change_advisory_board_approval: str = "Approved by CAB"
    release_notes: str
    rollback_plan: str = "Automated rollback within 30s"

class ReleaseDeploymentOut(ReleaseDeploymentCreate):
    id: int
    downtime_minutes: float
    smoke_test_status: str
    deployed_by: str
    deployment_status: str
    deployed_at: datetime
    class Config:
        from_attributes = True

# 7. SRE Observability
class SREObservabilityOut(BaseModel):
    id: int
    service_name: str
    p95_latency_ms: float
    p99_latency_ms: float
    uptime_30d_pct: float
    error_rate_pct: float
    error_budget_remaining_pct: float
    active_memory_mb: float
    cpu_utilization_pct: float
    active_db_connections: int
    recorded_at: datetime
    class Config:
        from_attributes = True
