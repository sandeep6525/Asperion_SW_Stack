"""
Asperion Enterprise OS - CRM, Legal & Contracting API
Handles Prospects, Deal Desk, Client Onboarding, and Automated Contract Generation
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.crm_legal import Prospect, ClientContract, ClientOnboardingRecord, LegalRiskObligation
from app.schemas.crm_legal import ProspectCreate, ProspectOut, ClientContractCreate, ClientContractOut, GenerateContractDocRequest
from app.engines.letter_generator import generate_document_html

router = APIRouter(prefix="/crm-legal", tags=["CRM & Legal Contracting"])

@router.get("/prospects", response_model=List[ProspectOut])
def list_prospects(db: Session = Depends(get_db)):
    return db.query(Prospect).order_by(Prospect.created_at.desc()).all()

@router.post("/prospects", response_model=ProspectOut)
def create_prospect(prospect_in: ProspectCreate, db: Session = Depends(get_db)):
    prospect = Prospect(**prospect_in.model_dump())
    db.add(prospect)
    db.commit()
    db.refresh(prospect)
    return prospect

@router.get("/contracts", response_model=List[ClientContractOut])
def list_contracts(db: Session = Depends(get_db)):
    return db.query(ClientContract).order_by(ClientContract.created_at.desc()).all()

@router.post("/contracts", response_model=ClientContractOut)
def create_contract(contract_in: ClientContractCreate, db: Session = Depends(get_db)):
    contract = ClientContract(**contract_in.model_dump())
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

@router.post("/generate-contract-doc")
def generate_contract_document(req: GenerateContractDocRequest):
    code_map = {
        "Mutual NDA": "LEG-NDA-01",
        "Non-Mutual NDA": "LEG-NDA-01",
    }
    letter_code = code_map.get(req.contract_type, "LEG-NDA-01")
    doc = generate_document_html(letter_code, {
        "counterparty_name": req.counterparty_name,
        "counterparty_address": req.counterparty_address,
        "project_purpose": req.project_purpose,
        "effective_date": req.effective_date or "Immediate"
    })
    return doc

@router.get("/onboarding-records")
def list_client_onboardings(db: Session = Depends(get_db)):
    return db.query(ClientOnboardingRecord).all()

@router.get("/risk-obligations")
def list_risk_obligations(db: Session = Depends(get_db)):
    return db.query(LegalRiskObligation).all()
