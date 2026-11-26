"""
Asperion Enterprise OS - Comprehensive Test Suite for Training Academy & New Joinee Curriculum
Validates:
1. Academy Overview KPIs & Telemetry
2. Role-based curriculum tracks with Minimum and Maximum learning hours
3. Modules listing with department, level, and category filtering
4. Course creation with syllabus chapters and assessment quizzes
5. Employee enrollment lifecycle and progress tracking
6. Automated quiz evaluation, scoring, and verifiable Certificate generation
7. Employee training summary and probation clearance readiness
8. Official printable Certificate of Completion HTML export with CIN
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.training import (
    TrainingTrack, TrainingModule, EmployeeTrainingEnrollment, TrainingMaterial
)
from app.schemas.training import (
    TrainingModuleCreate, TrainingEnrollmentCreate,
    TrainingProgressUpdate, TrainingQuizSubmit,
    SyllabusChapterItem, QuizQuestionItem,
    TrainingMaterialCreate
)
from app.api.training import (
    get_training_overview, list_training_tracks,
    list_training_modules, create_training_module, get_training_module_details,
    list_training_enrollments, enroll_employee_in_module,
    update_enrollment_progress, submit_module_quiz,
    get_employee_training_summary, export_training_certificate_html,
    list_training_materials, create_training_material,
    get_training_material_details, export_training_material_html
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_training_overview(db):
    """Test Training Academy high-level telemetry and metrics."""
    overview = get_training_overview(db=db)
    assert overview.total_modules >= 8
    assert overview.total_tracks >= 6
    assert overview.total_enrollments >= 8
    assert overview.total_completed_enrollments >= 4
    assert overview.overall_completion_rate_pct > 0.0
    assert overview.total_learning_hours_delivered > 0.0
    assert len(overview.tracks) >= 6

def test_training_tracks_min_max_hours(db):
    """Test role-based curriculum tracks have min/max hours defined."""
    tracks = list_training_tracks(db=db)
    assert len(tracks) >= 6
    
    eng_track = next(t for t in tracks if t.track_code == "TRACK-ENG-DEV")
    assert eng_track.min_training_hours == 24.0
    assert eng_track.max_training_hours == 45.0
    assert eng_track.min_passing_score_pct == 80.0
    assert "Software Engineer" in eng_track.target_roles

    all_track = next(t for t in tracks if t.track_code == "TRACK-ONB-ALL")
    assert all_track.min_training_hours == 16.0
    assert all_track.is_mandatory_for_probation is True

def test_training_modules_filtering(db):
    """Test modules listing and filtering by department, level, and category."""
    # 1. Filter by level
    foundational = list_training_modules(level="Foundational (Day 1-7)", db=db)
    assert len(foundational) >= 3
    assert all(m.level == "Foundational (Day 1-7)" for m in foundational)

    # 2. Filter by department
    eng_modules = list_training_modules(department="Engineering", db=db)
    assert len(eng_modules) >= 2

    # 3. Filter by category
    policy_modules = list_training_modules(category="Company Policies & Culture", db=db)
    assert len(policy_modules) >= 1
    assert any("Whistleblower" in m.title for m in policy_modules)

def test_create_training_module_with_quiz(db):
    """Test creating a new training module with syllabus chapters and assessment quiz."""
    new_mod = TrainingModuleCreate(
        title="WebAuthn FIDO2 Cryptographic Challenge-Response Architecture",
        category="Security Operations",
        department="Cybersecurity",
        duration_hours=2.5,
        level="Intermediate (Day 8-30)",
        is_mandatory=True,
        learning_objectives="Master public-key cryptography, hardware authenticators, and Zero Trust access verification.",
        syllabus=[
            SyllabusChapterItem(
                chapter=1,
                title="Public-Key Cryptography Foundations",
                duration_mins=45,
                summary="Asymmetric keypairs, secure enclaves, and non-exportable private keys."
            ),
            SyllabusChapterItem(
                chapter=2,
                title="FIDO2 WebAuthn Protocol Flow",
                duration_mins=60,
                summary="Attestation, assertion, and server challenge-response verification."
            )
        ],
        lesson_content="Detailed architectural guide on FIDO2 passwordless hardware passkey authentication.",
        policy_reference="ISO 27001:2022 A.9.4.2 & FIDO Alliance Spec",
        quiz=[
            QuizQuestionItem(
                question="Where is the private key stored in FIDO2 hardware passkey authentication?",
                options=["On the company cloud server", "Inside the hardware secure element (e.g. YubiKey)", "In plain text in browser cookies", "In a shared database table"],
                correct_idx=1,
                explanation="The private key never leaves the hardware secure element."
            )
        ],
        passing_score_pct=80.0
    )
    created = create_training_module(module_in=new_mod, db=db)
    assert created.id is not None
    assert created.module_code.startswith("TRN-2026-")
    assert len(created.syllabus) == 2
    assert len(created.quiz) == 1

    # Verify detail fetch
    detail = get_training_module_details(module_id=created.id, db=db)
    assert detail.title == new_mod.title

def test_employee_enrollment_lifecycle(db):
    """Test employee enrollment in module and progress updates."""
    import uuid
    modules = list_training_modules(db=db)
    target_mod = modules[0]

    unique_email = f"joinee_{uuid.uuid4().hex[:6]}@asperion.in"
    enroll = enroll_employee_in_module(
        enroll_in=TrainingEnrollmentCreate(
            employee_name="Test Joinee",
            employee_email=unique_email,
            employee_role="Junior Backend Engineer",
            department="Engineering",
            module_id=target_mod.id
        ),
        db=db
    )
    assert enroll.id is not None
    assert enroll.status == "ENROLLED"
    assert enroll.progress_pct == 0.0

    # Update progress
    updated = update_enrollment_progress(
        enrollment_id=enroll.id,
        payload=TrainingProgressUpdate(progress_pct=50.0, hours_spent=1.0),
        db=db
    )
    assert updated.status == "IN_PROGRESS"
    assert updated.progress_pct == 50.0
    assert updated.hours_spent == 1.0

def test_quiz_evaluation_and_certificate(db):
    """Test taking quiz, automatic scoring, pass threshold, and Certificate generation."""
    import uuid
    # Find module with quiz
    modules = list_training_modules(query="Corporate Culture", db=db)
    mod = modules[0]

    # Enroll user with unique email
    unique_email = f"rohan_{uuid.uuid4().hex[:6]}@asperion.in"
    enroll = enroll_employee_in_module(
        enroll_in=TrainingEnrollmentCreate(
            employee_name="Rohan Verma",
            employee_email=unique_email,
            employee_role="Associate Software Engineer",
            department="Engineering",
            module_id=mod.id
        ),
        db=db
    )

    # 1. Submit Failing Quiz answers
    fail_res = submit_module_quiz(
        enrollment_id=enroll.id,
        submission=TrainingQuizSubmit(answers=[2, 3]), # Incorrect answers
        db=db
    )
    assert fail_res.passed is False
    assert fail_res.score_pct < 80.0
    assert fail_res.certificate_id is None

    # 2. Submit Passing Quiz answers
    pass_res = submit_module_quiz(
        enrollment_id=enroll.id,
        submission=TrainingQuizSubmit(answers=[0, 1]), # Correct answers: U85500KA2026OPC222069, Sole Member & Director
        db=db
    )
    assert pass_res.passed is True
    assert pass_res.score_pct == 100.0
    assert pass_res.certificate_id is not None
    assert pass_res.certificate_id.startswith("CERT-TRN-2026-")

def test_employee_training_summary_and_probation(db):
    """Test probation clearance readiness calculation based on minimum hours."""
    # Siddharth Kulkarni is pre-seeded with 4 completed courses (> 11.5 hours)
    summary = get_employee_training_summary(email="siddharth.kulkarni@asperion.in", db=db)
    assert summary.total_completed >= 4
    assert summary.total_hours_completed >= 10.0
    assert summary.min_required_hours >= 16.0
    assert len(summary.enrollments) >= 4

    # New Joinee Ananya Sen
    summary_new = get_employee_training_summary(email="ananya.sen@asperiondigital.com", db=db)
    assert summary_new.total_enrolled >= 3
    assert summary_new.total_completed >= 1
    assert "In Progress" in summary_new.compliance_status

def test_certificate_html_export(db):
    """Test printable Certificate of Completion HTML export."""
    enrollments = list_training_enrollments(status_filter="COMPLETED", db=db)
    completed_enroll = next(e for e in enrollments if e.certificate_id is not None)

    res = export_training_certificate_html(certificate_id=completed_enroll.certificate_id, db=db)
    assert res.status_code == 200
    html = res.body.decode("utf-8")
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html
    assert "U85500KA2026OPC222069" in html
    assert "Certificate of Completion" in html
    assert completed_enroll.employee_name in html
    assert "Varadi Vijay" in html

def test_training_materials_listing_and_filtering(db):
    """Test comprehensive training materials, handbooks, and playbooks listing and filters."""
    # 1. Total seeded materials
    all_materials = list_training_materials(db=db)
    assert len(all_materials) >= 7

    # 2. Filter by category
    onboarding_books = list_training_materials(category="Onboarding Handbooks", db=db)
    assert len(onboarding_books) >= 2
    assert any(m.material_code == "MAT-ALL-001" for m in onboarding_books)

    # 3. Filter by department
    eng_materials = list_training_materials(department="Engineering", db=db)
    assert len(eng_materials) >= 1
    assert any("Local Environment Setup" in m.title for m in eng_materials)

    # 4. Filter by query
    certin_books = list_training_materials(query="CERT-In", db=db)
    assert len(certin_books) >= 1
    assert certin_books[0].material_code == "MAT-SEC-001"
    assert certin_books[0].doc_type == "RUNBOOK"

def test_create_training_material(db):
    """Test publishing new authentic training playbook or lab guide."""
    new_mat = TrainingMaterialCreate(
        title="PostgreSQL WAL Streaming Replication & Failover Playbook",
        category="Technical Labs & Code Walkthroughs",
        department="Engineering",
        target_role="DevOps Engineer, Cloud Architect",
        doc_type="PLAYBOOK",
        reading_time_mins=30,
        access_level="Internal Authenticated",
        summary="Complete procedural playbook for setting up streaming replication and Patroni automated failover.",
        content="# PostgreSQL HA & Streaming Replication Playbook\n\n### 1. Primary Node Setup\nConfigure pg_hba.conf and postgresql.conf.\n\n### 2. Standby Clone\nRun pg_basebackup with replication slot.",
        external_link="/api/v1/infrastructure/dr",
        linked_module_code="TRN-ENG-001",
        linked_sop_code="SOP-ENG-002"
    )
    created = create_training_material(material_in=new_mat, db=db)
    assert created.id is not None
    assert created.material_code.startswith("MAT-2026-")
    assert created.title == new_mat.title
    assert created.download_count == 0

    # Read details and verify download counter increment
    detail = get_training_material_details(material_id=created.id, db=db)
    assert detail.id == created.id
    assert detail.download_count == 1

def test_training_material_html_export(db):
    """Test official branded printable export of training playbook on corporate letterhead."""
    materials = list_training_materials(db=db)
    target_mat = materials[0]

    res = export_training_material_html(material_id=target_mat.id, db=db)
    assert res.status_code == 200
    html = res.body.decode("utf-8")
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html
    assert "U85500KA2026OPC222069" in html
    assert "Varadi Vijay" in html
    assert target_mat.title in html
    assert target_mat.material_code in html
    assert target_mat.summary in html
    assert "Training Material Content & Operational Instructions" in html
