"""
Asperion Enterprise OS - Learning & Training Academy API Router
"""
import json
import uuid
import hashlib
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.database import get_db
from app.models.training import (
    TrainingTrack, TrainingModule, EmployeeTrainingEnrollment, TrainingMaterial
)
from app.schemas.training import (
    TrainingTrackCreate, TrainingTrackOut,
    TrainingModuleCreate, TrainingModuleOut,
    TrainingEnrollmentCreate, TrainingEnrollmentOut,
    TrainingProgressUpdate, TrainingQuizSubmit, TrainingQuizResultOut,
    EmployeeTrainingSummaryOut, TrainingAcademyOverviewOut,
    TrainingMaterialCreate, TrainingMaterialOut,
    SyllabusChapterItem, QuizQuestionItem
)

router = APIRouter(prefix="/training", tags=["Learning & Training Academy"])

def _format_module_out(m: TrainingModule) -> TrainingModuleOut:
    syllabus_list = []
    if m.syllabus_json:
        try:
            raw_s = json.loads(m.syllabus_json)
            syllabus_list = [SyllabusChapterItem(**c) for c in raw_s]
        except Exception:
            syllabus_list = []

    quiz_list = []
    if m.quiz_json:
        try:
            raw_q = json.loads(m.quiz_json)
            quiz_list = [QuizQuestionItem(**q) for q in raw_q]
        except Exception:
            quiz_list = []

    return TrainingModuleOut(
        id=m.id,
        track_id=m.track_id,
        module_code=m.module_code,
        title=m.title,
        category=m.category,
        department=m.department,
        duration_hours=m.duration_hours or 2.0,
        level=m.level or "Foundational (Day 1-7)",
        is_mandatory=m.is_mandatory if m.is_mandatory is not None else True,
        learning_objectives=m.learning_objectives,
        syllabus=syllabus_list,
        lesson_content=m.lesson_content,
        policy_reference=m.policy_reference or "Asperion Governance & ISO Framework",
        quiz=quiz_list,
        passing_score_pct=m.passing_score_pct or 80.0,
        created_at=m.created_at or datetime.utcnow()
    )

def _format_enrollment_out(e: EmployeeTrainingEnrollment) -> TrainingEnrollmentOut:
    return TrainingEnrollmentOut(
        id=e.id,
        employee_id=e.employee_id,
        employee_name=e.employee_name,
        employee_email=e.employee_email,
        employee_role=e.employee_role,
        department=e.department,
        module_id=e.module_id,
        module_code=e.module.module_code if e.module else "TRN-000",
        module_title=e.module.title if e.module else "Unknown Module",
        module_duration=e.module.duration_hours if e.module else 2.0,
        module_level=e.module.level if e.module else "Foundational",
        status=e.status or "ENROLLED",
        progress_pct=e.progress_pct or 0.0,
        hours_spent=e.hours_spent or 0.0,
        score_pct=e.score_pct or 0.0,
        quiz_attempts=e.quiz_attempts or 0,
        completed_at=e.completed_at,
        certificate_id=e.certificate_id,
        enrolled_at=e.enrolled_at or datetime.utcnow()
    )


@router.get("/overview", response_model=TrainingAcademyOverviewOut)
def get_training_overview(db: Session = Depends(get_db)):
    """Executive Academy KPI summary."""
    total_modules = db.query(TrainingModule).count()
    total_tracks = db.query(TrainingTrack).count()
    total_materials = db.query(TrainingMaterial).count()
    total_enrollments = db.query(EmployeeTrainingEnrollment).count()
    completed_enrollments = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.status == "COMPLETED"
    ).count()
    
    rate = (completed_enrollments / total_enrollments * 100.0) if total_enrollments > 0 else 0.0

    enrollments = db.query(EmployeeTrainingEnrollment).all()
    total_hours_delivered = sum((e.hours_spent or 0.0) for e in enrollments)
    mandatory_count = db.query(TrainingModule).filter(TrainingModule.is_mandatory == True).count()

    tracks_raw = db.query(TrainingTrack).all()
    tracks_out = []
    for t in tracks_raw:
        m_count = db.query(TrainingModule).filter(TrainingModule.track_id == t.id).count()
        t_out = TrainingTrackOut.model_validate(t)
        t_out.modules_count = m_count
        tracks_out.append(t_out)

    return TrainingAcademyOverviewOut(
        total_modules=total_modules,
        total_tracks=total_tracks,
        total_materials=total_materials,
        total_enrollments=total_enrollments,
        total_completed_enrollments=completed_enrollments,
        overall_completion_rate_pct=round(rate, 1),
        total_learning_hours_delivered=round(total_hours_delivered, 1),
        mandatory_modules_count=mandatory_count,
        tracks=tracks_out
    )


@router.get("/tracks", response_model=List[TrainingTrackOut])
def list_training_tracks(department: Optional[str] = None, db: Session = Depends(get_db)):
    """List role-based training tracks with minimum and maximum hours specifications."""
    q = db.query(TrainingTrack)
    if department and department != "All":
        q = q.filter(or_(TrainingTrack.target_department == department, TrainingTrack.target_department == "All Company"))
    tracks = q.all()
    res = []
    for t in tracks:
        m_count = db.query(TrainingModule).filter(TrainingModule.track_id == t.id).count()
        t_out = TrainingTrackOut.model_validate(t)
        t_out.modules_count = m_count
        res.append(t_out)
    return res


@router.post("/tracks", response_model=TrainingTrackOut, status_code=status.HTTP_201_CREATED)
def create_training_track(track_in: TrainingTrackCreate, db: Session = Depends(get_db)):
    """Create a new role-based training curriculum track."""
    t = TrainingTrack(
        track_code=track_in.track_code,
        name=track_in.name,
        target_department=track_in.target_department,
        target_roles=track_in.target_roles,
        min_training_hours=track_in.min_training_hours,
        max_training_hours=track_in.max_training_hours,
        min_passing_score_pct=track_in.min_passing_score_pct,
        description=track_in.description,
        is_mandatory_for_probation=track_in.is_mandatory_for_probation,
        created_at=datetime.utcnow()
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    t_out = TrainingTrackOut.model_validate(t)
    t_out.modules_count = 0
    return t_out


@router.get("/modules", response_model=List[TrainingModuleOut])
def list_training_modules(
    department: Optional[str] = None,
    level: Optional[str] = None,
    category: Optional[str] = None,
    track_id: Optional[int] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List training modules filtered by department, level, track, or query."""
    q = db.query(TrainingModule)
    if department and department != "All":
        q = q.filter(or_(TrainingModule.department == department, TrainingModule.department == "All Company"))
    if level and level != "All":
        q = q.filter(TrainingModule.level == level)
    if category and category != "All":
        q = q.filter(TrainingModule.category == category)
    if track_id:
        q = q.filter(TrainingModule.track_id == track_id)
    if query:
        term = f"%{query}%"
        q = q.filter(
            or_(
                TrainingModule.title.ilike(term),
                TrainingModule.learning_objectives.ilike(term),
                TrainingModule.lesson_content.ilike(term),
                TrainingModule.policy_reference.ilike(term)
            )
        )
    modules = q.order_by(TrainingModule.is_mandatory.desc(), TrainingModule.id.asc()).all()
    return [_format_module_out(m) for m in modules]


@router.post("/modules", response_model=TrainingModuleOut, status_code=status.HTTP_201_CREATED)
def create_training_module(module_in: TrainingModuleCreate, db: Session = Depends(get_db)):
    """Create a new training module with syllabus and assessment quiz."""
    if not module_in.module_code:
        module_in.module_code = f"TRN-2026-{uuid.uuid4().hex[:4].upper()}"

    syllabus_json = "[]"
    if module_in.syllabus:
        syllabus_json = json.dumps([s.model_dump() for s in module_in.syllabus])

    quiz_json = "[]"
    if module_in.quiz:
        quiz_json = json.dumps([q.model_dump() for q in module_in.quiz])

    m = TrainingModule(
        track_id=module_in.track_id,
        module_code=module_in.module_code,
        title=module_in.title,
        category=module_in.category,
        department=module_in.department,
        duration_hours=module_in.duration_hours,
        level=module_in.level or "Foundational (Day 1-7)",
        is_mandatory=module_in.is_mandatory if module_in.is_mandatory is not None else True,
        learning_objectives=module_in.learning_objectives,
        syllabus_json=syllabus_json,
        lesson_content=module_in.lesson_content,
        policy_reference=module_in.policy_reference or "Asperion Governance & ISO Framework",
        quiz_json=quiz_json,
        passing_score_pct=module_in.passing_score_pct or 80.0,
        created_at=datetime.utcnow()
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return _format_module_out(m)


@router.get("/modules/{module_id}", response_model=TrainingModuleOut)
def get_training_module_details(module_id: int, db: Session = Depends(get_db)):
    """Retrieve full training module curriculum and quiz contents."""
    m = db.query(TrainingModule).filter(TrainingModule.id == module_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Training module not found")
    return _format_module_out(m)


@router.get("/enrollments", response_model=List[TrainingEnrollmentOut])
def list_training_enrollments(
    employee_email: Optional[str] = None,
    department: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List training enrollments with progress and quiz scores."""
    q = db.query(EmployeeTrainingEnrollment)
    if employee_email:
        q = q.filter(EmployeeTrainingEnrollment.employee_email == employee_email)
    if department and department != "All":
        q = q.filter(EmployeeTrainingEnrollment.department == department)
    if status_filter and status_filter != "All":
        q = q.filter(EmployeeTrainingEnrollment.status == status_filter)
    
    enrollments = q.order_by(EmployeeTrainingEnrollment.enrolled_at.desc()).all()
    return [_format_enrollment_out(e) for e in enrollments]


@router.post("/enrollments", response_model=TrainingEnrollmentOut, status_code=status.HTTP_201_CREATED)
def enroll_employee_in_module(enroll_in: TrainingEnrollmentCreate, db: Session = Depends(get_db)):
    """Enroll an employee in a course module."""
    # Check if already enrolled
    existing = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.employee_email == enroll_in.employee_email,
        EmployeeTrainingEnrollment.module_id == enroll_in.module_id
    ).first()
    if existing:
        return _format_enrollment_out(existing)

    module = db.query(TrainingModule).filter(TrainingModule.id == enroll_in.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Training module not found")

    enroll = EmployeeTrainingEnrollment(
        employee_id=enroll_in.employee_id,
        employee_name=enroll_in.employee_name,
        employee_email=enroll_in.employee_email,
        employee_role=enroll_in.employee_role,
        department=enroll_in.department,
        module_id=enroll_in.module_id,
        status="ENROLLED",
        progress_pct=0.0,
        hours_spent=0.0,
        score_pct=0.0,
        quiz_attempts=0,
        enrolled_at=datetime.utcnow()
    )
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    return _format_enrollment_out(enroll)


@router.patch("/enrollments/{enrollment_id}/progress", response_model=TrainingEnrollmentOut)
def update_enrollment_progress(
    enrollment_id: int,
    payload: TrainingProgressUpdate,
    db: Session = Depends(get_db)
):
    """Update course completion percentage and study hours."""
    enroll = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.id == enrollment_id
    ).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enroll.progress_pct = min(100.0, max(0.0, payload.progress_pct))
    enroll.hours_spent = max(0.0, payload.hours_spent)
    if enroll.progress_pct > 0 and enroll.status == "ENROLLED":
        enroll.status = "IN_PROGRESS"

    db.commit()
    db.refresh(enroll)
    return _format_enrollment_out(enroll)


@router.post("/enrollments/{enrollment_id}/submit-quiz", response_model=TrainingQuizResultOut)
def submit_module_quiz(
    enrollment_id: int,
    submission: TrainingQuizSubmit,
    db: Session = Depends(get_db)
):
    """Evaluate quiz answers, calculate score, mark completion, and generate certificate."""
    enroll = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.id == enrollment_id
    ).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    module = enroll.module
    if not module:
        raise HTTPException(status_code=404, detail="Associated module not found")

    quiz_questions = []
    if module.quiz_json:
        try:
            quiz_questions = json.loads(module.quiz_json)
        except Exception:
            quiz_questions = []

    if not quiz_questions:
        # No questions in quiz, automatic 100% pass
        score = 100.0
        passed = True
        correct = 0
        total = 0
    else:
        total = len(quiz_questions)
        correct = 0
        for i, q in enumerate(quiz_questions):
            if i < len(submission.answers):
                if submission.answers[i] == q.get("correct_idx"):
                    correct += 1
        score = round((correct / total) * 100.0, 1)
        passed = score >= (module.passing_score_pct or 80.0)

    enroll.quiz_attempts = (enroll.quiz_attempts or 0) + 1
    enroll.score_pct = max(enroll.score_pct or 0.0, score)

    cert_id = enroll.certificate_id
    if passed:
        enroll.status = "COMPLETED"
        enroll.progress_pct = 100.0
        enroll.hours_spent = module.duration_hours
        enroll.completed_at = datetime.utcnow()
        if not cert_id:
            cert_id = f"CERT-TRN-2026-{uuid.uuid4().hex[:6].upper()}"
            enroll.certificate_id = cert_id
            # Generate SHA-256 integrity hash
            hash_str = f"{enroll.employee_name}|{module.module_code}|{score}|{cert_id}|Asperion2026"
            enroll.certificate_hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()

    db.commit()
    db.refresh(enroll)

    feedback = f"Congratulations! You passed with {score}%." if passed else f"Score: {score}%. Minimum required passing score is {module.passing_score_pct}%. Please review the lesson material and try again."

    return TrainingQuizResultOut(
        score_pct=score,
        passed=passed,
        correct_count=correct,
        total_questions=total,
        certificate_id=cert_id if passed else None,
        feedback=feedback
    )


@router.get("/employee/summary", response_model=EmployeeTrainingSummaryOut)
def get_employee_training_summary(
    email: str = Query("siddharth.kulkarni@asperion.in"),
    db: Session = Depends(get_db)
):
    """Retrieve an employee's total completed training hours, min/max progress, and probation clearance status."""
    enrollments = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.employee_email == email
    ).all()

    emp_name = "Employee"
    emp_role = "Team Member"
    emp_dept = "Engineering"
    if enrollments:
        emp_name = enrollments[0].employee_name
        emp_role = enrollments[0].employee_role
        emp_dept = enrollments[0].department

    total_enrolled = len(enrollments)
    completed = [e for e in enrollments if e.status == "COMPLETED"]
    total_completed = len(completed)
    total_hours = sum((e.hours_spent or 0.0) for e in completed)

    # Find department or track requirements (Standard: min 16.0 hrs, max 40.0 hrs)
    min_req = 16.0
    max_rec = 40.0
    track = db.query(TrainingTrack).filter(
        or_(TrainingTrack.target_department == emp_dept, TrainingTrack.target_department == "All Company")
    ).first()
    if track:
        min_req = track.min_training_hours or 16.0
        max_rec = track.max_training_hours or 40.0

    probation_ready = (total_hours >= min_req) and (total_completed >= 3)
    compliance_status = "Compliant (Probation Clearance Ready)" if probation_ready else f"In Progress ({round(total_hours, 1)} / {min_req} hours required)"

    return EmployeeTrainingSummaryOut(
        employee_name=emp_name,
        employee_role=emp_role,
        department=emp_dept,
        total_enrolled=total_enrolled,
        total_completed=total_completed,
        total_hours_completed=round(total_hours, 1),
        min_required_hours=min_req,
        max_recommended_hours=max_rec,
        probation_clearance_ready=probation_ready,
        compliance_status=compliance_status,
        enrollments=[_format_enrollment_out(e) for e in enrollments]
    )


@router.get("/certificates/{certificate_id}/html", response_class=HTMLResponse)
def export_training_certificate_html(certificate_id: str, db: Session = Depends(get_db)):
    """Generate an official authentic Certificate of Completion with Asperion corporate seal and CIN."""
    enroll = db.query(EmployeeTrainingEnrollment).filter(
        EmployeeTrainingEnrollment.certificate_id == certificate_id
    ).first()
    if not enroll:
        raise HTTPException(status_code=404, detail="Certificate not found")

    module = enroll.module
    module_title = module.title if module else "Core Enterprise Training"
    comp_date = enroll.completed_at.strftime("%B %d, %Y") if enroll.completed_at else datetime.utcnow().strftime("%B %d, %Y")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Certificate of Completion - {certificate_id}</title>
        <style>
            body {{ font-family: 'Georgia', serif; margin: 0; padding: 40px; background: #0f172a; display: flex; justify-content: center; }}
            .cert-card {{ width: 850px; background: #ffffff; border: 12px double #1e3a8a; padding: 50px; position: relative; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); text-align: center; }}
            .header {{ border-bottom: 2px solid #cbd5e1; padding-bottom: 20px; margin-bottom: 30px; }}
            .company-name {{ font-size: 22px; font-weight: 800; color: #1e3a8a; letter-spacing: 2px; text-transform: uppercase; }}
            .cin {{ font-size: 11px; color: #64748b; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 4px; }}
            .title {{ font-size: 32px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 3px; margin: 25px 0 10px 0; }}
            .subtitle {{ font-size: 15px; color: #475569; font-style: italic; margin-bottom: 25px; }}
            .presented-to {{ font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #64748b; margin-bottom: 10px; font-family: 'Segoe UI', Arial, sans-serif; }}
            .recipient {{ font-size: 28px; font-weight: 800; color: #1e3a8a; border-bottom: 2px solid #e2e8f0; display: inline-block; padding: 0 30px 8px 30px; margin-bottom: 20px; }}
            .statement {{ font-size: 15px; color: #334155; line-height: 1.8; max-width: 650px; margin: 0 auto 30px auto; }}
            .course-name {{ font-weight: bold; color: #0f172a; font-size: 18px; display: block; margin: 8px 0; }}
            .footer-grid {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-family: 'Segoe UI', Arial, sans-serif; }}
            .sig-block {{ text-align: center; width: 220px; }}
            .sig-line {{ border-top: 1px solid #475569; padding-top: 6px; font-size: 12px; font-weight: bold; color: #1e293b; }}
            .sig-title {{ font-size: 10px; color: #64748b; }}
            .gold-seal {{ width: 90px; height: 90px; border-radius: 50%; border: 3px solid #d97706; background: #fffbeb; color: #b45309; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; letter-spacing: 1px; text-transform: uppercase; box-shadow: inset 0 0 10px #fde68a; }}
            .meta-foot {{ margin-top: 25px; font-size: 10px; color: #94a3b8; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="cert-card">
            <div class="header">
                <div class="company-name">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div class="cin">CIN: U85500KA2026OPC222069 &bull; Registered Office: Horamavu, Bangalore, Karnataka</div>
            </div>

            <div class="title">Certificate of Completion</div>
            <div class="subtitle">Asperion Enterprise Onboarding & Technical Academy</div>

            <div class="presented-to">This is proudly awarded to</div>
            <div class="recipient">{enroll.employee_name}</div>

            <div class="statement">
                For successfully completing the comprehensive role-based curriculum, meeting all minimum learning requirements, and passing the rigorous compliance assessment with a score of <strong>{enroll.score_pct}%</strong> in:
                <span class="course-name">{module_title}</span>
                covering statutory standards, operating procedures, Zero Trust architecture, and corporate governance.
            </div>

            <div class="footer-grid">
                <div class="sig-block">
                    <div style="font-family: 'Brush Script MT', cursive; font-size: 26px; color: #1e3a8a; margin-bottom: 2px;">Varadi Vijay</div>
                    <div class="sig-line">Varadi Vijay</div>
                    <div class="sig-title">Director & Founder</div>
                </div>

                <div class="gold-seal">
                    <div style="font-size: 16px;">★</div>
                    <div>VERIFIED</div>
                    <div style="font-size: 8px;">ACADEMY</div>
                </div>

                <div class="sig-block">
                    <div style="font-size: 13px; font-weight: bold; color: #334155; margin-bottom: 8px;">{comp_date}</div>
                    <div class="sig-line">Date of Certification</div>
                    <div class="sig-title">Asperion L&D Governance</div>
                </div>
            </div>

            <div class="meta-foot">
                Certificate ID: {enroll.certificate_id} &bull; SHA-256 Digest: {enroll.certificate_hash[:24] if enroll.certificate_hash else 'AUTHENTIC-ASPERION'}... &bull; ISO 9001:2015 Clause 7.2
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.get("/materials", response_model=List[TrainingMaterialOut])
def list_training_materials(
    category: Optional[str] = None,
    department: Optional[str] = None,
    doc_type: Optional[str] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List training handbooks, lab walkthroughs, access playbooks, and checklists."""
    q = db.query(TrainingMaterial)
    if category and category != "All":
        q = q.filter(TrainingMaterial.category == category)
    if department and department != "All":
        q = q.filter(or_(TrainingMaterial.department == department, TrainingMaterial.department == "All Company"))
    if doc_type and doc_type != "All":
        q = q.filter(TrainingMaterial.doc_type == doc_type)
    if query:
        term = f"%{query}%"
        q = q.filter(
            or_(
                TrainingMaterial.title.ilike(term),
                TrainingMaterial.summary.ilike(term),
                TrainingMaterial.content.ilike(term),
                TrainingMaterial.target_role.ilike(term)
            )
        )
    materials = q.order_by(TrainingMaterial.id.asc()).all()
    return materials


@router.post("/materials", response_model=TrainingMaterialOut, status_code=status.HTTP_201_CREATED)
def create_training_material(material_in: TrainingMaterialCreate, db: Session = Depends(get_db)):
    """Publish a new training handbook, lab walkthrough, or access guide."""
    if not material_in.material_code:
        prefix = "MAT"
        material_in.material_code = f"{prefix}-2026-{uuid.uuid4().hex[:4].upper()}"

    mat = TrainingMaterial(
        material_code=material_in.material_code,
        title=material_in.title,
        category=material_in.category,
        department=material_in.department,
        target_role=material_in.target_role or "All Roles",
        doc_type=material_in.doc_type or "HANDBOOK",
        reading_time_mins=material_in.reading_time_mins or 25,
        access_level=material_in.access_level or "Internal Authenticated",
        summary=material_in.summary,
        content=material_in.content,
        external_link=material_in.external_link,
        linked_module_code=material_in.linked_module_code,
        linked_sop_code=material_in.linked_sop_code,
        download_count=0,
        created_at=datetime.utcnow()
    )
    db.add(mat)
    db.commit()
    db.refresh(mat)
    return mat


@router.get("/materials/{material_id}", response_model=TrainingMaterialOut)
def get_training_material_details(material_id: int, db: Session = Depends(get_db)):
    """Retrieve full material text and increment access counter."""
    mat = db.query(TrainingMaterial).filter(TrainingMaterial.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="Training material not found")
    
    mat.download_count = (mat.download_count or 0) + 1
    db.commit()
    db.refresh(mat)
    return mat


@router.get("/materials/{material_id}/export-html", response_class=HTMLResponse)
def export_training_material_html(material_id: int, db: Session = Depends(get_db)):
    """Generate an official printable training handbook/manual with corporate branding."""
    mat = db.query(TrainingMaterial).filter(TrainingMaterial.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")

    mat.download_count = (mat.download_count or 0) + 1
    db.commit()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{mat.material_code} - {mat.title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; background: #ffffff; line-height: 1.6; }}
            .header {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #b45309; padding-bottom: 16px; margin-bottom: 24px; }}
            .company-name {{ font-size: 18px; font-weight: 800; color: #1e3a8a; text-transform: uppercase; }}
            .cin {{ font-size: 11px; color: #64748b; margin-top: 2px; }}
            .doc-tag {{ font-size: 11px; background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 4px; font-weight: bold; border: 1px solid #fde68a; }}
            .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; background: #f8fafc; padding: 14px; border-radius: 6px; margin-bottom: 24px; font-size: 12px; border: 1px solid #e2e8f0; }}
            .meta-item strong {{ display: block; color: #64748b; text-transform: uppercase; font-size: 10px; margin-bottom: 2px; }}
            .content-box {{ font-size: 13px; color: #334155; margin-bottom: 24px; white-space: pre-line; line-height: 1.8; }}
            .footer {{ margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 11px; color: #94a3b8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div class="company-name">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div class="cin">CIN: U85500KA2026OPC222069 &bull; Horamavu, Bangalore, Karnataka</div>
            </div>
            <div class="doc-tag">{mat.doc_type} &bull; {mat.material_code}</div>
        </div>

        <h1 style="color: #0f172a; margin-top: 0; font-size: 22px;">{mat.title}</h1>
        <div style="font-size: 13px; color: #475569; font-style: italic; margin-bottom: 18px;">{mat.summary}</div>

        <div class="meta-grid">
            <div class="meta-item"><strong>Department</strong>{mat.department}</div>
            <div class="meta-item"><strong>Target Role</strong>{mat.target_role}</div>
            <div class="meta-item"><strong>Category</strong>{mat.category}</div>
            <div class="meta-item"><strong>Est. Reading Time</strong>{mat.reading_time_mins} minutes</div>
            <div class="meta-item"><strong>Access Classification</strong>{mat.access_level}</div>
            <div class="meta-item"><strong>Linked Module</strong>{mat.linked_module_code or 'N/A'}</div>
            <div class="meta-item"><strong>Linked SOP</strong>{mat.linked_sop_code or 'N/A'}</div>
            <div class="meta-item"><strong>Compliance</strong>ISO 9001:2015 Clause 7.2</div>
        </div>

        <h3 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">Training Material Content & Operational Instructions</h3>
        <div class="content-box">{mat.content}</div>

        <div style="margin-top: 32px; padding: 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 11px; color: #475569; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>Authorized Governance Sign-off:</strong> Varadi Vijay (Founder & Sole Director)<br>
                <span>Registered Office: Flat No.304, 3rd Floor, Type 4, Lakshith Properties, Horamavu, Bangalore - 560043</span>
            </div>
            <div style="text-align: right; font-family: monospace;">
                <strong>CIN:</strong> U85500KA2026OPC222069<br>
                <span>ISO 9001:2015 Clause 7.2 Verified</span>
            </div>
        </div>

        <div class="footer">
            Asperion Enterprise Training Academy &bull; Official Employee Training Asset &bull; Page 1 of 1
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

