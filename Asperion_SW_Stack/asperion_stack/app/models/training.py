"""
Asperion Enterprise OS - Learning & Development Hub / New Joinee Training Academy Models
Supports:
1. Role-based curriculum tracks (Engineering, SecOps, HR, Finance, PMO, All Company)
2. Minimum and Maximum required training hours, credits, and passing scores
3. Interactive lesson materials with policy citations (ISO 9001/27001, POSH, Companies Act)
4. Knowledge check quizzes with automated scoring
5. Training enrollments, progress tracking, and verifiable completion certificates
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TrainingTrack(Base):
    __tablename__ = "training_tracks"

    id = Column(Integer, primary_key=True, index=True)
    track_code = Column(String(50), unique=True, index=True, nullable=False) # TRACK-ONB-ALL, TRACK-ENG-DEV
    name = Column(String(255), nullable=False)
    target_department = Column(String(100), nullable=False) # 'All Company', 'Engineering', 'Cybersecurity', 'Finance & Ops', 'HR & Talent', 'PMO & Delivery'
    target_roles = Column(String(255), nullable=False) # e.g. "All Employees", "Software Engineer, DevOps", "SecOps Analyst"
    min_training_hours = Column(Float, default=16.0) # Minimum mandatory training hours
    max_training_hours = Column(Float, default=40.0) # Maximum recommended training hours
    min_passing_score_pct = Column(Float, default=80.0) # Standard passing score
    description = Column(Text, nullable=False)
    is_mandatory_for_probation = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    modules = relationship("TrainingModule", back_populates="track", cascade="all, delete-orphan")


class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("training_tracks.id"), nullable=True, index=True)
    module_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. TRN-ALL-001, TRN-ENG-002
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # 'Company Policies & Culture', 'Statutory & ISO Compliance', 'Technical Architecture', 'Security Operations', 'Financial Procedures', 'HR & People Ops'
    department = Column(String(100), nullable=False) # 'All Company', 'Engineering', 'Cybersecurity', 'Finance & Ops', 'HR & Talent', 'PMO & Delivery'
    duration_hours = Column(Float, default=2.0)
    level = Column(String(50), default="Foundational (Day 1-7)") # 'Foundational (Day 1-7)', 'Intermediate (Day 8-30)', 'Advanced (Day 31-90)'
    is_mandatory = Column(Boolean, default=True)
    
    learning_objectives = Column(Text, nullable=False)
    syllabus_json = Column(Text, default="[]") # JSON list of [{chapter: 1, title: "", duration_mins: 30, summary: ""}]
    lesson_content = Column(Text, nullable=False) # Detailed markdown course body
    policy_reference = Column(String(255), default="Asperion Governance & ISO Framework")
    
    quiz_json = Column(Text, default="[]") # JSON list of [{question: "", options: ["A", "B", "C", "D"], correct_idx: 0, explanation: ""}]
    passing_score_pct = Column(Float, default=80.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    track = relationship("TrainingTrack", back_populates="modules")
    enrollments = relationship("EmployeeTrainingEnrollment", back_populates="module", cascade="all, delete-orphan")


class EmployeeTrainingEnrollment(Base):
    __tablename__ = "employee_training_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    employee_name = Column(String(150), nullable=False)
    employee_email = Column(String(150), nullable=False)
    employee_role = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False)
    
    module_id = Column(Integer, ForeignKey("training_modules.id"), nullable=False, index=True)
    status = Column(String(50), default="ENROLLED") # 'ENROLLED', 'IN_PROGRESS', 'COMPLETED', 'OVERDUE'
    progress_pct = Column(Float, default=0.0) # 0.0 to 100.0
    hours_spent = Column(Float, default=0.0)
    score_pct = Column(Float, default=0.0)
    quiz_attempts = Column(Integer, default=0)
    
    completed_at = Column(DateTime, nullable=True)
    certificate_id = Column(String(100), nullable=True) # e.g. CERT-TRN-2026-001
    certificate_hash = Column(String(255), nullable=True) # SHA-256 digest
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date, nullable=True)

    module = relationship("TrainingModule", back_populates="enrollments")


class TrainingMaterial(Base):
    __tablename__ = "training_materials"

    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. MAT-ALL-001, MAT-ENG-002
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # 'Onboarding Handbooks', 'Access & Credential Guides', 'Technical Labs & Code Walkthroughs', 'Statutory & Policy Handbooks', 'Cheatsheets & Runbooks'
    department = Column(String(100), nullable=False) # 'All Company', 'Engineering', 'Cybersecurity', 'Finance & Ops', 'HR & Talent', 'PMO & Delivery'
    target_role = Column(String(150), default="All Roles")
    doc_type = Column(String(50), default="HANDBOOK") # 'HANDBOOK', 'RUNBOOK', 'LAB_GUIDE', 'ACCESS_GUIDE', 'CHECKLIST', 'BLUEPRINT'
    reading_time_mins = Column(Integer, default=25)
    access_level = Column(String(50), default="Internal Authenticated") # 'Public / Joinee', 'Internal Authenticated', 'SecOps Restricted'
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False) # Full rich markdown handbook/guide content with methods, commands, links, credentials workflow
    external_link = Column(String(255), nullable=True)
    linked_module_code = Column(String(50), nullable=True) # e.g. TRN-ALL-001
    linked_sop_code = Column(String(50), nullable=True) # e.g. SOP-ENG-001
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

