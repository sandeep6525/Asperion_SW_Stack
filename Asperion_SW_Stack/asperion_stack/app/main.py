"""
Asperion Enterprise OS - FastAPI Application Entrypoint
Unified Backend Server orchestrating all 8 enterprise operational pillars
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import settings
from app.database import engine, Base
from app.seed_data import seed_database

# Import routers
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.governance import router as governance_router
from app.api.crm_legal import router as crm_legal_router
from app.api.finance import router as finance_router
from app.api.hrms import router as hrms_router
from app.api.pmo import router as pmo_router
from app.api.procurement import router as procurement_router
from app.api.infrastructure import router as infrastructure_router
from app.api.cybersecurity import router as cybersecurity_router
from app.api.vault import router as vault_router
from app.api.strategy import router as strategy_router
from app.api.analytics import router as analytics_router
from app.api.crm_enterprise import router as crm_enterprise_router
from app.api.ticketing_notifications import router as ticketing_notifications_router
from app.api.developer_platform import router as developer_platform_router
from app.api.attendance import router as attendance_router
from app.api.system_health import router as system_health_router
from app.api.portals import router as portals_router
from app.api.sdlc import router as sdlc_router
from app.api.guardrails import router as guardrails_router
from app.api.ai_cloud import router as ai_cloud_router
from app.api.iso_standards import router as iso_standards_router
from app.api.communications import router as communications_router
from app.api.sharepoint import router as sharepoint_router
from app.api.training import router as training_router
from app.api.itsm import router as itsm_router
from app.api.agentic_ai import router as agentic_ai_router
from app.api.enterprise_operations import router as enterprise_operations_router
from app.api.crypto import router as crypto_router
from app.engines.autoupdate_manager import auto_update_manager

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-Stack Operating System & Enterprise Software Stack for ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
v1_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=v1_prefix)
app.include_router(dashboard_router, prefix=v1_prefix)
app.include_router(governance_router, prefix=v1_prefix)
app.include_router(crm_legal_router, prefix=v1_prefix)
app.include_router(finance_router, prefix=v1_prefix)
app.include_router(hrms_router, prefix=v1_prefix)
app.include_router(pmo_router, prefix=v1_prefix)
app.include_router(procurement_router, prefix=v1_prefix)
app.include_router(infrastructure_router, prefix=v1_prefix)
app.include_router(cybersecurity_router, prefix=v1_prefix)
app.include_router(vault_router, prefix=v1_prefix)
app.include_router(strategy_router, prefix=v1_prefix)
app.include_router(analytics_router, prefix=v1_prefix)
app.include_router(crm_enterprise_router, prefix=v1_prefix)
app.include_router(ticketing_notifications_router, prefix=v1_prefix)
app.include_router(developer_platform_router, prefix=v1_prefix)
app.include_router(attendance_router, prefix=v1_prefix)
app.include_router(system_health_router, prefix=v1_prefix)
app.include_router(portals_router, prefix=v1_prefix)
app.include_router(sdlc_router, prefix=v1_prefix)
app.include_router(guardrails_router, prefix=v1_prefix)
app.include_router(ai_cloud_router, prefix=v1_prefix)
app.include_router(iso_standards_router, prefix=v1_prefix)
app.include_router(communications_router, prefix=v1_prefix)
app.include_router(sharepoint_router, prefix=v1_prefix)
app.include_router(training_router, prefix=v1_prefix)
app.include_router(itsm_router, prefix=v1_prefix)
app.include_router(agentic_ai_router, prefix=v1_prefix)
app.include_router(enterprise_operations_router, prefix=v1_prefix)
app.include_router(crypto_router, prefix=v1_prefix)

# Mount Static Files
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_database()
    auto_update_manager.start(interval_seconds=30)

@app.on_event("shutdown")
def on_shutdown():
    auto_update_manager.stop()

@app.get("/", include_in_schema=False)
def serve_index():
    index_path = static_dir / "index.html"
    return FileResponse(str(index_path))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": settings.PROJECT_NAME,
        "company": settings.COMPANY_NAME,
        "cin": settings.CIN,
        "version": settings.VERSION
    }
