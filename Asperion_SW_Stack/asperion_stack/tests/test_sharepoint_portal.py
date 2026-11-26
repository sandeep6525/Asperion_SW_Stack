"""
Asperion Enterprise OS - Comprehensive Test Suite for SharePoint & Knowledge Management Hub
Validates:
1. SharePoint Overview KPIs (Total SOPs, Thoughts, Mechanisms, Documents, Questions)
2. Articles listing with category, department, and full-text keyword filtering
3. Publishing new SOPs with structured execution steps, checklists, and RACI matrices
4. Social collaboration: Like toggles, bookmark tracking, and threaded comments
5. Community Q&A: Peer question submission, upvoting, and verified answers
6. Centralized Document Library digital assets
7. Official Authentic HTML Document Export with corporate branding and CIN
"""
import pytest
from app.database import SessionLocal, Base, engine
from app.seed_data import seed_database
from app.models.sharepoint import (
    SharePointArticle, SharePointComment, SharePointCommunityQuestion, SharePointDocumentLibraryItem
)
from app.schemas.sharepoint import (
    SharePointArticleCreate, SharePointLikeToggle, SharePointCommentCreate,
    SharePointQuestionCreate, SharePointQuestionAnswerCreate, ExecutionStepItem
)
from app.api.sharepoint import (
    get_sharepoint_overview, list_sharepoint_articles, create_sharepoint_article,
    get_sharepoint_article_details, toggle_sharepoint_article_like,
    list_article_comments, add_article_comment,
    list_community_questions, ask_community_question,
    answer_community_question, upvote_community_question,
    list_document_library, export_article_html
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

def test_sharepoint_overview(db):
    """Test SharePoint overview KPIs."""
    overview = get_sharepoint_overview(db=db)
    assert overview.total_articles >= 6
    assert overview.total_sops >= 2
    assert overview.total_thoughts >= 2
    assert overview.total_mechanisms >= 2
    assert overview.total_questions >= 2
    assert overview.total_documents >= 5
    assert overview.total_likes >= 10
    assert len(overview.featured_articles) >= 1
    assert any("Philosophy" in a.title for a in overview.featured_articles)

def test_sharepoint_articles_filtering(db):
    """Test filtering articles by category, department, and search query."""
    # 1. Filter by category
    sops = list_sharepoint_articles(category="SOP & Procedures", db=db)
    assert len(sops) >= 2
    assert all(a.category == "SOP & Procedures" for a in sops)

    # 2. Filter by thoughts
    thoughts = list_sharepoint_articles(category="Employee Thoughts", db=db)
    assert len(thoughts) >= 2
    assert all(a.category == "Employee Thoughts" for a in thoughts)

    # 3. Filter by department
    eng_articles = list_sharepoint_articles(department="Engineering", db=db)
    assert len(eng_articles) >= 2
    assert all(a.department == "Engineering" for a in eng_articles)

    # 4. Search query
    zero_trust_articles = list_sharepoint_articles(query="Zero Trust", db=db)
    assert len(zero_trust_articles) >= 1

def test_create_sharepoint_sop_and_steps(db):
    """Test publishing a new SOP with execution steps and automated code generation."""
    new_sop = SharePointArticleCreate(
        title="Automated PostgreSQL to SQLite DB Failover & Replication Drill",
        category="SOP & Procedures",
        department="Engineering",
        summary="Standard procedure for simulating read-replica failovers and verifying local SQLite cache integrity during cloud outage.",
        content="Execute quarterly disaster recovery drill simulating complete AWS connection drop and graceful local offline fallback.",
        steps=[
            ExecutionStepItem(
                step=1,
                title="Simulate Cloud VPC Route Cut",
                description="Simulate network isolation by cutting external route to primary cloud replica.",
                raci="Responsible: SRE Lead",
                estimated_minutes=10
            ),
            ExecutionStepItem(
                step=2,
                title="Verify Local SQLite Standby Cache Engagement",
                description="Ensure application switches to local read-only mode and writes queue to disk-based journal.",
                raci="Responsible: Platform Engineer",
                estimated_minutes=5
            )
        ],
        author_name="Varadi Vijay",
        author_role="Director & Founder",
        author_email="director@asperion.in",
        version="v1.0",
        iso_compliance_tag="ISO 22301 Business Continuity & ISO 27001 A.8.14",
        tags="dr, disaster-recovery, database, failover, replication"
    )
    created = create_sharepoint_article(article_in=new_sop, db=db)
    assert created.id is not None
    assert created.article_code.startswith("SOP-2026-")
    assert len(created.steps) == 2
    assert created.steps[0].title == "Simulate Cloud VPC Route Cut"

    # Detail check & view count increment
    detail = get_sharepoint_article_details(article_id=created.id, db=db)
    assert detail.views_count >= 2

def test_article_like_toggle_and_comments(db):
    """Test social engagement: likes toggle and threaded comments."""
    articles = list_sharepoint_articles(category="Employee Thoughts", db=db)
    art = articles[0]
    initial_likes = art.likes_count

    # 1. Like article
    liked = toggle_sharepoint_article_like(
        article_id=art.id,
        payload=SharePointLikeToggle(user_name="Test Engineer"),
        db=db
    )
    assert liked.likes_count == initial_likes + 1
    assert "Test Engineer" in liked.likes_users

    # 2. Unlike article
    unliked = toggle_sharepoint_article_like(
        article_id=art.id,
        payload=SharePointLikeToggle(user_name="Test Engineer"),
        db=db
    )
    assert unliked.likes_count == initial_likes
    assert "Test Engineer" not in unliked.likes_users

    # 3. Post a comment
    comment = add_article_comment(
        article_id=art.id,
        comment_in=SharePointCommentCreate(
            content="This perspective provides immense clarity for our quarterly sprint planning.",
            author_name="Ananya Sen",
            author_role="Associate DevOps Engineer"
        ),
        db=db
    )
    assert comment.id is not None
    assert comment.article_id == art.id

    # 4. List comments
    comments = list_article_comments(article_id=art.id, db=db)
    assert any(c.content == "This perspective provides immense clarity for our quarterly sprint planning." for c in comments)

def test_community_questions_and_answer(db):
    """Test peer-to-peer community Q&A and verified solutions."""
    # 1. Ask a question
    new_q = ask_community_question(
        question_in=SharePointQuestionCreate(
            title="How do we trigger on-demand Docx export for CERT-In incident reports?",
            department="Cybersecurity",
            body="Is there an internal CLI command or direct endpoint to generate official Docx files for regulatory auditors?",
            tags="secops, cert-in, docx, reporting",
            author_name="Karthik V",
            author_role="Senior Software Engineer"
        ),
        db=db
    )
    assert new_q.id is not None
    assert new_q.question_code.startswith("QA-2026-")
    assert new_q.status == "Open"

    # 2. Upvote question
    upvoted = upvote_community_question(question_id=new_q.id, user_name="Priya Nair", db=db)
    assert upvoted.upvotes_count == 1

    # 3. Submit Answer
    answered = answer_community_question(
        question_id=new_q.id,
        ans_in=SharePointQuestionAnswerCreate(
            author_name="Priya Nair",
            author_role="CISO Lead",
            text="Use the endpoint `GET /api/v1/vault/documents/secops-docx?incident_id=INC-2026-0881` or run `python asperion_cli.py secops export`."
        ),
        db=db
    )
    assert answered.answers_count == 1
    assert answered.status == "Answered"
    assert "Priya Nair" in answered.answers[0].author

def test_document_library_listing(db):
    """Test document library asset retrieval."""
    docs = list_document_library(db=db)
    assert len(docs) >= 5
    assert any(d.file_type == "DOCX" for d in docs)
    assert any(d.file_type == "PDF" for d in docs)
    assert any(d.file_type == "XLSX" for d in docs)

def test_article_export_html(db):
    """Test printable branded HTML export for an SOP."""
    articles = list_sharepoint_articles(category="SOP & Procedures", db=db)
    sop = articles[0]
    response = export_article_html(article_id=sop.id, db=db)
    assert response.status_code == 200
    html = response.body.decode("utf-8")
    assert "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED" in html
    assert "U85500KA2026OPC222069" in html
    assert sop.article_code in html
    assert "Execution Procedure & Checklists" in html
