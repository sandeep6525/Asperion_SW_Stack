"""
Asperion Enterprise OS - SharePoint & Knowledge Management Hub Models
Supports:
1. Standard Operating Procedures (SOPs), Processes & Procedures with Step Checklists & ISO tags
2. Methods & Mechanisms (Architecture blueprints, engineering & operational patterns)
3. Employee Thoughts & Perspectives (Thought leadership, ideas, articles with likes and comments)
4. Community Q&A & Best Practice Discussions (with verified solutions)
5. Document Libraries & Digital Asset Store
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from app.database import Base

class SharePointArticle(Base):
    __tablename__ = "sharepoint_articles"

    id = Column(Integer, primary_key=True, index=True)
    article_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. SOP-ENG-001, POST-THOUGHT-004
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # 'SOP & Procedures', 'Methods & Mechanisms', 'Employee Thoughts', 'Architecture & Blueprints', 'Policies & Compliance'
    department = Column(String(100), nullable=False) # 'Engineering', 'Cybersecurity', 'HR & Talent', 'Finance & Ops', 'Executive & Strategy', 'All Company'
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False) # Full markdown content / article body
    steps_json = Column(Text, default="[]") # JSON list of execution steps/checklists
    
    author_name = Column(String(150), nullable=False)
    author_role = Column(String(150), nullable=False)
    author_email = Column(String(150), nullable=True)
    
    version = Column(String(20), default="v1.0")
    status = Column(String(50), default="Published") # 'Published', 'Under Review', 'Archived'
    sensitivity = Column(String(50), default="Internal Use Only") # 'Public', 'Internal Use Only', 'Restricted', 'Confidential'
    iso_compliance_tag = Column(String(100), default="ISO 9001:2015 & ISO 27001:2022")
    tags = Column(String(255), default="")
    
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    likes_users_json = Column(Text, default="[]") # JSON list of employee names who liked
    bookmarks_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    featured_badge = Column(String(100), nullable=True) # e.g. "Director's Pick", "Certified SOP", "Trending"
    attachment_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SharePointComment(Base):
    __tablename__ = "sharepoint_comments"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("sharepoint_articles.id"), nullable=False, index=True)
    author_name = Column(String(150), nullable=False)
    author_role = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SharePointCommunityQuestion(Base):
    __tablename__ = "sharepoint_community_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. QA-2026-001
    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    author_name = Column(String(150), nullable=False)
    author_role = Column(String(150), nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(String(255), default="")
    
    views_count = Column(Integer, default=0)
    upvotes_count = Column(Integer, default=0)
    upvoters_json = Column(Text, default="[]")
    has_verified_solution = Column(Boolean, default=False)
    answers_count = Column(Integer, default=0)
    answers_json = Column(Text, default="[]") # JSON list of answers: [{author, role, text, upvotes, is_verified, answered_at}]
    status = Column(String(50), default="Open") # 'Open', 'Answered', 'Resolved'
    created_at = Column(DateTime, default=datetime.utcnow)


class SharePointDocumentLibraryItem(Base):
    __tablename__ = "sharepoint_document_library"

    id = Column(Integer, primary_key=True, index=True)
    doc_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. DOC-LIB-001
    name = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False) # 'DOCX', 'PDF', 'XLSX', 'MARKDOWN', 'DRAWIO'
    file_size_kb = Column(Integer, default=128)
    category = Column(String(100), nullable=False) # 'Engineering Templates', 'HR Guides', 'Financial Forms', 'Security Checklists'
    department = Column(String(100), nullable=False)
    uploaded_by = Column(String(150), nullable=False)
    version = Column(String(20), default="v1.0")
    download_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
