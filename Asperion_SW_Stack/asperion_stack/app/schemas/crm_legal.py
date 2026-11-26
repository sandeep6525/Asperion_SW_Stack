"""
Asperion Enterprise OS - CRM & Legal Schemas
"""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class ProspectCreate(BaseModel):
    company_name: str
    contact_person: str
    contact_email: str
    contact_phone: Optional[str] = None
    industry: str = "Technology / Software"
    pipeline_stage: str = "Lead Qualified"
    deal_value: float = 0.0
    lead_source: str = "Direct / Referral"
    owner: str = "Sales Lead"
    notes: Optional[str] = None

class ProspectOut(ProspectCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ClientContractCreate(BaseModel):
    contract_reference: str
    prospect_id: Optional[int] = None
    client_name: str
    contract_type: str = "Master Services Agreement (MSA)"
    effective_date: date
    expiry_date: Optional[date] = None
    value_inr: float = 0.0
    status: str = "Drafted"
    governing_law: str = "Laws of India, Jurisdiction of Bangalore, Karnataka"
    special_conditions: Optional[str] = None

class ClientContractOut(ClientContractCreate):
    id: int
    stamp_duty_paid: bool
    created_at: datetime
    class Config:
        from_attributes = True

class GenerateContractDocRequest(BaseModel):
    contract_type: str # Mutual NDA, MSA, SOW
    counterparty_name: str
    counterparty_address: str
    project_purpose: str = "Software Development and Digital Consulting"
    effective_date: Optional[str] = None
