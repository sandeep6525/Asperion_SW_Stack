"""
Asperion Enterprise OS - SharePoint & Knowledge Hub Pydantic Schemas
"""
from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ExecutionStepItem(BaseModel):
    step: int
    title: str
    description: str
    raci: Optional[str] = "Responsible: Author | Consulted: Team"
    estimated_minutes: Optional[int] = 15

class SharePointArticleBase(BaseModel):
    title: str
    category: str # 'SOP & Procedures', 'Methods & Mechanisms', 'Employee Thoughts', 'Architecture & Blueprints', 'Policies & Compliance'
    department: str
    summary: str
    content: str
    steps: Optional[List[ExecutionStepItem]] = []
    version: Optional[str] = "v1.0"
    status: Optional[str] = "Published"
    sensitivity: Optional[str] = "Internal Use Only"
    iso_compliance_tag: Optional[str] = "ISO 9001:2015 & ISO 27001:2022"
    tags: Optional[str] = ""
    is_pinned: Optional[bool] = False
    featured_badge: Optional[str] = None
    attachment_url: Optional[str] = None

class SharePointArticleCreate(SharePointArticleBase):
    article_code: Optional[str] = None
    author_name: str = "Varadi Vijay"
    author_role: str = "Director & Founder"
    author_email: Optional[str] = "director@asperion.in"

class SharePointArticleOut(SharePointArticleBase):
    id: int
    article_code: str
    author_name: str
    author_role: str
    author_email: Optional[str]
    views_count: int
    likes_count: int
    likes_users: List[str] = []
    bookmarks_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SharePointLikeToggle(BaseModel):
    user_name: str = "Varadi Vijay"

class SharePointCommentCreate(BaseModel):
    content: str
    author_name: str = "Varadi Vijay"
    author_role: str = "Director & Founder"

class SharePointCommentOut(BaseModel):
    id: int
    article_id: int
    author_name: str
    author_role: str
    content: str
    upvotes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommunityAnswerItem(BaseModel):
    author: str
    role: str
    text: str
    upvotes: int = 0
    is_verified: bool = False
    answered_at: str

class SharePointQuestionCreate(BaseModel):
    title: str
    department: str
    body: str
    tags: Optional[str] = ""
    author_name: str = "Varadi Vijay"
    author_role: str = "Director & Founder"

class SharePointQuestionOut(BaseModel):
    id: int
    question_code: str
    title: str
    department: str
    author_name: str
    author_role: str
    body: str
    tags: str
    views_count: int
    upvotes_count: int
    has_verified_solution: bool
    answers_count: int
    answers: List[CommunityAnswerItem] = []
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SharePointQuestionAnswerCreate(BaseModel):
    author_name: str = "Varadi Vijay"
    author_role: str = "Director & Founder"
    text: str

class SharePointDocLibraryOut(BaseModel):
    id: int
    doc_code: str
    name: str
    file_type: str
    file_size_kb: int
    category: str
    department: str
    uploaded_by: str
    version: str
    download_url: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SharePointOverviewOut(BaseModel):
    total_articles: int
    total_sops: int
    total_thoughts: int
    total_mechanisms: int
    total_questions: int
    total_documents: int
    total_likes: int
    featured_articles: List[SharePointArticleOut] = []
    recent_thoughts: List[SharePointArticleOut] = []
