"""
Asperion Enterprise OS - Training & Learning Academy Pydantic Schemas
"""
from typing import List, Optional, Any
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class SyllabusChapterItem(BaseModel):
    chapter: int
    title: str
    duration_mins: int = 30
    summary: str

class QuizQuestionItem(BaseModel):
    question: str
    options: List[str]
    correct_idx: int
    explanation: Optional[str] = ""

class TrainingTrackBase(BaseModel):
    track_code: str
    name: str
    target_department: str
    target_roles: str
    min_training_hours: float = 16.0
    max_training_hours: float = 40.0
    min_passing_score_pct: float = 80.0
    description: str
    is_mandatory_for_probation: bool = True

class TrainingTrackCreate(TrainingTrackBase):
    pass

class TrainingTrackOut(TrainingTrackBase):
    id: int
    created_at: datetime
    modules_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class TrainingModuleBase(BaseModel):
    title: str
    category: str
    department: str
    duration_hours: float = 2.0
    level: Optional[str] = "Foundational (Day 1-7)"
    is_mandatory: Optional[bool] = True
    learning_objectives: str
    syllabus: Optional[List[SyllabusChapterItem]] = []
    lesson_content: str
    policy_reference: Optional[str] = "Asperion Governance & ISO Framework"
    quiz: Optional[List[QuizQuestionItem]] = []
    passing_score_pct: Optional[float] = 80.0

class TrainingModuleCreate(TrainingModuleBase):
    module_code: Optional[str] = None
    track_id: Optional[int] = None

class TrainingModuleOut(TrainingModuleBase):
    id: int
    track_id: Optional[int]
    module_code: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TrainingEnrollmentCreate(BaseModel):
    employee_name: str
    employee_email: str
    employee_role: str
    department: str
    module_id: int
    employee_id: Optional[int] = None

class TrainingProgressUpdate(BaseModel):
    progress_pct: float
    hours_spent: float

class TrainingQuizSubmit(BaseModel):
    answers: List[int] # List of chosen option indexes [0, 2, 1, 3...]

class TrainingQuizResultOut(BaseModel):
    score_pct: float
    passed: bool
    correct_count: int
    total_questions: int
    certificate_id: Optional[str] = None
    feedback: str

class TrainingEnrollmentOut(BaseModel):
    id: int
    employee_id: Optional[int]
    employee_name: str
    employee_email: str
    employee_role: str
    department: str
    module_id: int
    module_code: str
    module_title: str
    module_duration: float
    module_level: str
    status: str
    progress_pct: float
    hours_spent: float
    score_pct: float
    quiz_attempts: int
    completed_at: Optional[datetime]
    certificate_id: Optional[str]
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EmployeeTrainingSummaryOut(BaseModel):
    employee_name: str
    employee_role: str
    department: str
    total_enrolled: int
    total_completed: int
    total_hours_completed: float
    min_required_hours: float
    max_recommended_hours: float
    probation_clearance_ready: bool
    compliance_status: str
    enrollments: List[TrainingEnrollmentOut] = []

class TrainingAcademyOverviewOut(BaseModel):
    total_modules: int
    total_tracks: int
    total_materials: int = 0
    total_enrollments: int
    total_completed_enrollments: int
    overall_completion_rate_pct: float
    total_learning_hours_delivered: float
    mandatory_modules_count: int
    tracks: List[TrainingTrackOut] = []

class TrainingMaterialBase(BaseModel):
    material_code: Optional[str] = None
    title: str
    category: str # 'Onboarding Handbooks', 'Access & Credential Guides', 'Technical Labs & Code Walkthroughs', 'Statutory & Policy Handbooks', 'Cheatsheets & Runbooks'
    department: str
    target_role: Optional[str] = "All Roles"
    doc_type: Optional[str] = "HANDBOOK"
    reading_time_mins: Optional[int] = 25
    access_level: Optional[str] = "Internal Authenticated"
    summary: str
    content: str
    external_link: Optional[str] = None
    linked_module_code: Optional[str] = None
    linked_sop_code: Optional[str] = None

class TrainingMaterialCreate(TrainingMaterialBase):
    pass

class TrainingMaterialOut(TrainingMaterialBase):
    id: int
    download_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

