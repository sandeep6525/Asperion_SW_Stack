"""
Asperion Enterprise OS - SharePoint & Knowledge Hub API Router
"""
import json
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.database import get_db
from app.models.sharepoint import (
    SharePointArticle, SharePointComment, SharePointCommunityQuestion, SharePointDocumentLibraryItem
)
from app.schemas.sharepoint import (
    SharePointArticleCreate, SharePointArticleOut, SharePointLikeToggle,
    SharePointCommentCreate, SharePointCommentOut,
    SharePointQuestionCreate, SharePointQuestionOut, SharePointQuestionAnswerCreate,
    SharePointDocLibraryOut, SharePointOverviewOut, ExecutionStepItem, CommunityAnswerItem
)

router = APIRouter(prefix="/sharepoint", tags=["Enterprise SharePoint & Knowledge Hub"])

def _format_article_out(a: SharePointArticle) -> SharePointArticleOut:
    steps_data = []
    if a.steps_json:
        try:
            raw_steps = json.loads(a.steps_json)
            steps_data = [ExecutionStepItem(**s) for s in raw_steps]
        except Exception:
            steps_data = []
    
    likes_users_list = []
    if a.likes_users_json:
        try:
            likes_users_list = json.loads(a.likes_users_json)
        except Exception:
            likes_users_list = []

    return SharePointArticleOut(
        id=a.id,
        article_code=a.article_code,
        title=a.title,
        category=a.category,
        department=a.department,
        summary=a.summary,
        content=a.content,
        steps=steps_data,
        author_name=a.author_name,
        author_role=a.author_role,
        author_email=a.author_email,
        version=a.version or "v1.0",
        status=a.status or "Published",
        sensitivity=a.sensitivity or "Internal Use Only",
        iso_compliance_tag=a.iso_compliance_tag or "ISO 9001:2015 & ISO 27001:2022",
        tags=a.tags or "",
        views_count=a.views_count or 0,
        likes_count=a.likes_count or 0,
        likes_users=likes_users_list,
        bookmarks_count=a.bookmarks_count or 0,
        is_pinned=a.is_pinned or False,
        featured_badge=a.featured_badge,
        attachment_url=a.attachment_url,
        created_at=a.created_at or datetime.utcnow(),
        updated_at=a.updated_at or datetime.utcnow()
    )

def _format_question_out(q: SharePointCommunityQuestion) -> SharePointQuestionOut:
    answers_data = []
    if q.answers_json:
        try:
            raw_ans = json.loads(q.answers_json)
            answers_data = [CommunityAnswerItem(**item) for item in raw_ans]
        except Exception:
            answers_data = []

    return SharePointQuestionOut(
        id=q.id,
        question_code=q.question_code,
        title=q.title,
        department=q.department,
        author_name=q.author_name,
        author_role=q.author_role,
        body=q.body,
        tags=q.tags or "",
        views_count=q.views_count or 0,
        upvotes_count=q.upvotes_count or 0,
        has_verified_solution=q.has_verified_solution or False,
        answers_count=len(answers_data),
        answers=answers_data,
        status=q.status or "Open",
        created_at=q.created_at or datetime.utcnow()
    )


@router.get("/overview", response_model=SharePointOverviewOut)
def get_sharepoint_overview(db: Session = Depends(get_db)):
    """Executive KPI overview of Asperion SharePoint & Knowledge Hub."""
    total_articles = db.query(SharePointArticle).count()
    total_sops = db.query(SharePointArticle).filter(SharePointArticle.category == "SOP & Procedures").count()
    total_thoughts = db.query(SharePointArticle).filter(SharePointArticle.category == "Employee Thoughts").count()
    total_mechanisms = db.query(SharePointArticle).filter(SharePointArticle.category == "Methods & Mechanisms").count()
    total_questions = db.query(SharePointCommunityQuestion).count()
    total_documents = db.query(SharePointDocumentLibraryItem).count()
    
    # Calculate total likes across articles
    articles = db.query(SharePointArticle).all()
    total_likes = sum((a.likes_count or 0) for a in articles)

    # Featured articles
    featured_raw = db.query(SharePointArticle).filter(
        or_(SharePointArticle.is_pinned == True, SharePointArticle.featured_badge.isnot(None))
    ).order_by(desc(SharePointArticle.views_count)).limit(4).all()
    featured_articles = [_format_article_out(a) for a in featured_raw]

    # Recent thoughts
    thoughts_raw = db.query(SharePointArticle).filter(
        SharePointArticle.category == "Employee Thoughts"
    ).order_by(desc(SharePointArticle.created_at)).limit(4).all()
    recent_thoughts = [_format_article_out(a) for a in thoughts_raw]

    return SharePointOverviewOut(
        total_articles=total_articles,
        total_sops=total_sops,
        total_thoughts=total_thoughts,
        total_mechanisms=total_mechanisms,
        total_questions=total_questions,
        total_documents=total_documents,
        total_likes=total_likes,
        featured_articles=featured_articles,
        recent_thoughts=recent_thoughts
    )


@router.get("/articles", response_model=List[SharePointArticleOut])
def list_sharepoint_articles(
    category: Optional[str] = None,
    department: Optional[str] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve articles filtered by category, department, or keyword search."""
    q = db.query(SharePointArticle)
    if category and category != "All":
        q = q.filter(SharePointArticle.category == category)
    if department and department != "All":
        q = q.filter(SharePointArticle.department == department)
    if query:
        term = f"%{query}%"
        q = q.filter(
            or_(
                SharePointArticle.title.ilike(term),
                SharePointArticle.summary.ilike(term),
                SharePointArticle.content.ilike(term),
                SharePointArticle.tags.ilike(term),
                SharePointArticle.author_name.ilike(term)
            )
        )
    
    articles = q.order_by(desc(SharePointArticle.is_pinned), desc(SharePointArticle.created_at)).all()
    return [_format_article_out(a) for a in articles]


@router.post("/articles", response_model=SharePointArticleOut, status_code=status.HTTP_201_CREATED)
def create_sharepoint_article(article_in: SharePointArticleCreate, db: Session = Depends(get_db)):
    """Publish a new SOP, Method, Mechanism, or Employee Thought."""
    # Generate code if not provided
    if not article_in.article_code:
        prefix_map = {
            "SOP & Procedures": "SOP",
            "Methods & Mechanisms": "METH",
            "Employee Thoughts": "THOUGHT",
            "Architecture & Blueprints": "ARCH",
            "Policies & Compliance": "POL"
        }
        prefix = prefix_map.get(article_in.category, "DOC")
        article_in.article_code = f"{prefix}-2026-{uuid.uuid4().hex[:4].upper()}"

    steps_json = "[]"
    if article_in.steps:
        steps_json = json.dumps([s.model_dump() for s in article_in.steps])

    art = SharePointArticle(
        article_code=article_in.article_code,
        title=article_in.title,
        category=article_in.category,
        department=article_in.department,
        summary=article_in.summary,
        content=article_in.content,
        steps_json=steps_json,
        author_name=article_in.author_name,
        author_role=article_in.author_role,
        author_email=article_in.author_email,
        version=article_in.version or "v1.0",
        status=article_in.status or "Published",
        sensitivity=article_in.sensitivity or "Internal Use Only",
        iso_compliance_tag=article_in.iso_compliance_tag or "ISO 9001:2015 & ISO 27001:2022",
        tags=article_in.tags or "",
        views_count=1,
        likes_count=0,
        likes_users_json="[]",
        bookmarks_count=0,
        is_pinned=article_in.is_pinned or False,
        featured_badge=article_in.featured_badge,
        attachment_url=article_in.attachment_url,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(art)
    db.commit()
    db.refresh(art)
    return _format_article_out(art)


@router.get("/articles/{article_id}", response_model=SharePointArticleOut)
def get_sharepoint_article_details(article_id: int, db: Session = Depends(get_db)):
    """Retrieve full article detail and increment view counter."""
    art = db.query(SharePointArticle).filter(SharePointArticle.id == article_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="SharePoint article not found")
    
    art.views_count = (art.views_count or 0) + 1
    db.commit()
    db.refresh(art)
    return _format_article_out(art)


@router.post("/articles/{article_id}/like", response_model=SharePointArticleOut)
def toggle_sharepoint_article_like(
    article_id: int,
    payload: SharePointLikeToggle,
    db: Session = Depends(get_db)
):
    """Toggle like on an article/thought for an employee."""
    art = db.query(SharePointArticle).filter(SharePointArticle.id == article_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")

    likes_list = []
    if art.likes_users_json:
        try:
            likes_list = json.loads(art.likes_users_json)
        except Exception:
            likes_list = []

    user = payload.user_name.strip()
    if user in likes_list:
        likes_list.remove(user)
    else:
        likes_list.append(user)

    art.likes_count = len(likes_list)
    art.likes_users_json = json.dumps(likes_list)
    db.commit()
    db.refresh(art)
    return _format_article_out(art)


@router.get("/articles/{article_id}/comments", response_model=List[SharePointCommentOut])
def list_article_comments(article_id: int, db: Session = Depends(get_db)):
    """List discussion comments on a SharePoint article/thought."""
    comments = db.query(SharePointComment).filter(
        SharePointComment.article_id == article_id
    ).order_by(SharePointComment.created_at.asc()).all()
    return comments


@router.post("/articles/{article_id}/comments", response_model=SharePointCommentOut, status_code=status.HTTP_201_CREATED)
def add_article_comment(
    article_id: int,
    comment_in: SharePointCommentCreate,
    db: Session = Depends(get_db)
):
    """Post an employee reflection or question comment on an article."""
    art = db.query(SharePointArticle).filter(SharePointArticle.id == article_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")

    c = SharePointComment(
        article_id=article_id,
        author_name=comment_in.author_name,
        author_role=comment_in.author_role,
        content=comment_in.content,
        upvotes=0,
        created_at=datetime.utcnow()
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("/community/questions", response_model=List[SharePointQuestionOut])
def list_community_questions(
    department: Optional[str] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve community Q&A questions."""
    q = db.query(SharePointCommunityQuestion)
    if department and department != "All":
        q = q.filter(SharePointCommunityQuestion.department == department)
    if query:
        term = f"%{query}%"
        q = q.filter(
            or_(
                SharePointCommunityQuestion.title.ilike(term),
                SharePointCommunityQuestion.body.ilike(term),
                SharePointCommunityQuestion.tags.ilike(term)
            )
        )
    questions = q.order_by(desc(SharePointCommunityQuestion.created_at)).all()
    return [_format_question_out(q_item) for q_item in questions]


@router.post("/community/questions", response_model=SharePointQuestionOut, status_code=status.HTTP_201_CREATED)
def ask_community_question(question_in: SharePointQuestionCreate, db: Session = Depends(get_db)):
    """Ask a question or seek best practice guidance from colleagues."""
    code = f"QA-2026-{uuid.uuid4().hex[:4].upper()}"
    q = SharePointCommunityQuestion(
        question_code=code,
        title=question_in.title,
        department=question_in.department,
        author_name=question_in.author_name,
        author_role=question_in.author_role,
        body=question_in.body,
        tags=question_in.tags or "",
        views_count=1,
        upvotes_count=0,
        upvoters_json="[]",
        has_verified_solution=False,
        answers_count=0,
        answers_json="[]",
        status="Open",
        created_at=datetime.utcnow()
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return _format_question_out(q)


@router.post("/community/questions/{question_id}/answers", response_model=SharePointQuestionOut)
def answer_community_question(
    question_id: int,
    ans_in: SharePointQuestionAnswerCreate,
    db: Session = Depends(get_db)
):
    """Submit an answer to a community question."""
    q = db.query(SharePointCommunityQuestion).filter(SharePointCommunityQuestion.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    answers = []
    if q.answers_json:
        try:
            answers = json.loads(q.answers_json)
        except Exception:
            answers = []

    new_ans = {
        "author": ans_in.author_name,
        "role": ans_in.author_role,
        "text": ans_in.text,
        "upvotes": 0,
        "is_verified": False,
        "answered_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    }
    answers.append(new_ans)
    q.answers_json = json.dumps(answers)
    q.answers_count = len(answers)
    if q.status == "Open":
        q.status = "Answered"
    db.commit()
    db.refresh(q)
    return _format_question_out(q)


@router.post("/community/questions/{question_id}/upvote", response_model=SharePointQuestionOut)
def upvote_community_question(question_id: int, user_name: str = Query("Varadi Vijay"), db: Session = Depends(get_db)):
    """Upvote a question."""
    q = db.query(SharePointCommunityQuestion).filter(SharePointCommunityQuestion.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    upvoters = []
    if q.upvoters_json:
        try:
            upvoters = json.loads(q.upvoters_json)
        except Exception:
            upvoters = []

    user = user_name.strip()
    if user in upvoters:
        upvoters.remove(user)
    else:
        upvoters.append(user)

    q.upvotes_count = len(upvoters)
    q.upvoters_json = json.dumps(upvoters)
    db.commit()
    db.refresh(q)
    return _format_question_out(q)


@router.get("/document-library", response_model=List[SharePointDocLibraryOut])
def list_document_library(
    department: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve document library assets."""
    q = db.query(SharePointDocumentLibraryItem)
    if department and department != "All":
        q = q.filter(SharePointDocumentLibraryItem.department == department)
    if category and category != "All":
        q = q.filter(SharePointDocumentLibraryItem.category == category)
    docs = q.order_by(SharePointDocumentLibraryItem.category, SharePointDocumentLibraryItem.name).all()
    return docs


@router.get("/articles/{article_id}/export-html", response_class=HTMLResponse)
def export_article_html(article_id: int, db: Session = Depends(get_db)):
    """Generates an official authentic printable HTML document for an SOP or knowledge article."""
    art = db.query(SharePointArticle).filter(SharePointArticle.id == article_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")

    steps_html = ""
    if art.steps_json:
        try:
            steps = json.loads(art.steps_json)
            if steps:
                step_items = "".join([
                    f"""
                    <div style="margin-bottom: 12px; padding: 12px; background: #f8fafc; border-left: 4px solid #3b82f6; border-radius: 4px;">
                        <div style="font-weight: bold; color: #1e293b;">Step {s.get('step', i+1)}: {s.get('title', '')}</div>
                        <div style="color: #475569; font-size: 13px; margin-top: 4px;">{s.get('description', '')}</div>
                        <div style="color: #64748b; font-size: 11px; margin-top: 6px;">
                            <strong>RACI:</strong> {s.get('raci', 'N/A')} &bull; <strong>Est. Time:</strong> {s.get('estimated_minutes', 15)} mins
                        </div>
                    </div>
                    """
                    for i, s in enumerate(steps)
                ])
                steps_html = f"""
                <h3 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 24px;">Execution Procedure & Checklists</h3>
                {step_items}
                """
        except Exception:
            steps_html = ""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{art.article_code} - {art.title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; background: #ffffff; line-height: 1.6; }}
            .header {{ display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #1e3a8a; padding-bottom: 16px; margin-bottom: 24px; }}
            .company-name {{ font-size: 18px; font-weight: 800; color: #1e3a8a; text-transform: uppercase; }}
            .doc-tag {{ font-size: 12px; background: #eff6ff; color: #2563eb; padding: 4px 10px; border-radius: 4px; font-weight: bold; }}
            .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; background: #f1f5f9; padding: 14px; border-radius: 6px; margin-bottom: 24px; font-size: 12px; }}
            .meta-item strong {{ display: block; color: #475569; text-transform: uppercase; font-size: 10px; margin-bottom: 2px; }}
            .content-box {{ font-size: 14px; color: #334155; margin-bottom: 24px; white-space: pre-line; }}
            .footer {{ margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 11px; color: #94a3b8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div class="company-name">ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED</div>
                <div style="font-size: 11px; color: #64748b;">CIN: U85500KA2026OPC222069 &bull; Horamavu, Bangalore, Karnataka</div>
            </div>
            <div class="doc-tag">{art.category} &bull; {art.version}</div>
        </div>

        <h1 style="color: #0f172a; margin-top: 0; font-size: 24px;">{art.title}</h1>
        <div style="font-size: 14px; color: #475569; font-style: italic; margin-bottom: 18px;">{art.summary}</div>

        <div class="meta-grid">
            <div class="meta-item"><strong>Document Code</strong>{art.article_code}</div>
            <div class="meta-item"><strong>Department</strong>{art.department}</div>
            <div class="meta-item"><strong>Author & Role</strong>{art.author_name} ({art.author_role})</div>
            <div class="meta-item"><strong>Compliance Standard</strong>{art.iso_compliance_tag}</div>
            <div class="meta-item"><strong>Sensitivity</strong>{art.sensitivity}</div>
            <div class="meta-item"><strong>Status</strong>{art.status}</div>
            <div class="meta-item"><strong>Published Date</strong>{art.created_at.strftime('%Y-%m-%d')}</div>
            <div class="meta-item"><strong>Effective Review</strong>Q3 2026 Annual Audit</div>
        </div>

        <h3 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">Document Specifications & Policy Description</h3>
        <div class="content-box">{art.content}</div>

        {steps_html}

        <div class="footer">
            Asperion Enterprise Operating System &bull; SharePoint Knowledge Repository &bull; Certified Authenticity &bull; Page 1 of 1
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
