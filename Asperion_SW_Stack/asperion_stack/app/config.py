"""
Asperion Enterprise Operating System - Global Configuration & Settings
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Asperion Enterprise OS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Corporate Entity Details
    COMPANY_NAME: str = "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    CIN: str = "U85500KA2026OPC222069"
    REGISTERED_OFFICE: str = "Flat No.304, 3 Floor, Type4, Lakshith Properties, Horamavu, Bangalore North, Bangalore - 560043, Karnataka, India"
    PAN: str = "AAACA1234D"
    TAN: str = "BLRA12345D"
    GSTIN: str = "29AAACA1234D1Z5"
    DEFAULT_STATE: str = "Karnataka"
    STATE_CODE: str = "29"
    FOUNDER_DIRECTOR: str = "Varadi Vijay (Director / Sole Member)"
    PRIMARY_DOMAIN: str = "asperion.in"
    DESIGNATED_EMAIL: str = "contact@asperion.in"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'asperion.db'}"
    
    # Statutory Defaults (India)
    PF_EMPLOYER_RATE: float = 0.12
    PF_EMPLOYEE_RATE: float = 0.12
    PF_WAGE_CEILING: float = 15000.0
    ESI_EMPLOYER_RATE: float = 0.0325
    ESI_EMPLOYEE_RATE: float = 0.0075
    ESI_WAGE_CEILING: float = 21000.0
    KARNATAKA_PTAX_SLAB: float = 200.0  # Monthly PT for gross > Rs 25,000
    GRATUITY_RATE: float = 0.0481      # 15/26 days per year (approx 4.81% of basic)
    
    # CERT-In Regulatory Notification SLA (Hours)
    CERT_IN_REPORTING_HOURS: int = 6
    
    # Secret Key for JWT / Sessions
    SECRET_KEY: str = "asperion-enterprise-secret-key-prod-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"

settings = Settings()
