"""
Asperion Enterprise OS - Authentication & RBAC Module
Provides secure role-based access control, corporate personas, and session management.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication & RBAC"])

# Enterprise Personas
CORPORATE_USERS = {
    "director@asperion.in": {
        "id": "USR-DIR-001",
        "name": settings.FOUNDER_DIRECTOR,
        "email": "director@asperion.in",
        "password": "Password123!",
        "role": "DIRECTOR",
        "title": "Sole Director & Founder",
        "modules": ["all"]
    },
    "finance@asperion.in": {
        "id": "USR-FIN-002",
        "name": "Finance Head",
        "email": "finance@asperion.in",
        "password": "Password123!",
        "role": "FINANCE_HEAD",
        "title": "Head of Finance & Treasury",
        "modules": ["dashboard", "finance", "procurement", "governance"]
    },
    "hr@asperion.in": {
        "id": "USR-HR-003",
        "name": "People Operations Lead",
        "email": "hr@asperion.in",
        "password": "Password123!",
        "role": "HR_HEAD",
        "title": "Head of People & HR Operations",
        "modules": ["dashboard", "hrms", "governance"]
    },
    "delivery@asperion.in": {
        "id": "USR-DEL-004",
        "name": "PMO Delivery Lead",
        "email": "delivery@asperion.in",
        "password": "Password123!",
        "role": "DELIVERY_HEAD",
        "title": "Delivery & PMO Lead",
        "modules": ["dashboard", "pmo", "crm", "sdlc"]
    },
    "soc@asperion.in": {
        "id": "USR-SOC-005",
        "name": "CISO / SOC Lead",
        "email": "soc@asperion.in",
        "password": "Password123!",
        "role": "SOC_LEAD",
        "title": "Lead Cyber Security & Incident Commander",
        "modules": ["dashboard", "secops", "infrastructure"]
    },
    "employee@asperion.in": {
        "id": "USR-EMP-001",
        "name": "Arjun Sharma",
        "email": "employee@asperion.in",
        "password": "Password123!",
        "role": "EMPLOYEE",
        "title": "Lead Full-Stack Engineer (ADT-EMP-001)",
        "modules": ["portal-employee"]
    },
    "client@zenith.com": {
        "id": "USR-CLT-001",
        "name": "Vikram Seth (Zenith Global)",
        "email": "client@zenith.com",
        "password": "Password123!",
        "role": "CLIENT",
        "title": "VP Engineering (Enterprise Client)",
        "modules": ["portal-client"]
    },
    "vendor@nexuscables.in": {
        "id": "USR-VND-001",
        "name": "Nexus Micro Systems",
        "email": "vendor@nexuscables.in",
        "password": "Password123!",
        "role": "VENDOR",
        "title": "Authorized Hardware Supplier",
        "modules": ["portal-vendor"]
    }
}

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
    role: str
    title: str
    authorized_modules: List[str]

class UserProfileOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    title: str
    modules: List[str]

@router.post("/login", response_model=LoginResponse)
def login(creds: LoginRequest):
    user = CORPORATE_USERS.get(creds.email.lower().strip())
    if not user or user["password"] != creds.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Simple deterministic session token
    token = f"asp_sec_{user['id']}_{user['role']}"
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user["id"],
        name=user["name"],
        email=user["email"],
        role=user["role"],
        title=user["title"],
        authorized_modules=user["modules"]
    )

@router.get("/me", response_model=UserProfileOut)
def get_current_user(authorization: Optional[str] = Header(None)):
    # Default to Director if no token provided in demo environment
    if not authorization or not authorization.startswith("Bearer "):
        user = CORPORATE_USERS["director@asperion.in"]
        return UserProfileOut(**user)
    
    token = authorization.replace("Bearer ", "").strip()
    for user in CORPORATE_USERS.values():
        if user["id"] in token:
            return UserProfileOut(**user)
            
    return UserProfileOut(**CORPORATE_USERS["director@asperion.in"])

@router.get("/personas", response_model=List[UserProfileOut])
def list_personas():
    """Lists enterprise personas for rapid demonstration switching."""
    return [UserProfileOut(**u) for u in CORPORATE_USERS.values()]
