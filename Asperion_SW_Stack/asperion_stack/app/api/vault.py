"""
Asperion Enterprise OS - Enterprise Knowledge & Document Vault API
Serves and indexes all 260+ authentic operational manuals, handbooks, SOPs,
policies, legal contracts, and HR letter templates extracted from Asperion packs.
"""
import os
import urllib.parse
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter(prefix="/vault", tags=["Enterprise Document & Knowledge Vault"])

VAULT_DIR = Path(__file__).resolve().parent.parent / "static" / "templates_vault"

CATEGORY_METADATA = {
    "company_os": {"name": "Company OS & Governance", "icon": "fa-building-columns", "desc": "17 Core Operating Manuals, Handbooks, SOPs, and Capability Blueprints"},
    "hr_letters": {"name": "HR & Legal Letter Master Registry", "icon": "fa-envelope-open-text", "desc": "65+ Authentic Word (.docx) Letter Templates across all employee lifecycle stages"},
    "finance_templates": {"name": "Finance, Accounting & Treasury", "icon": "fa-file-invoice-dollar", "desc": "Vouchers, Journals, AP/AR Controls, Month-End Close, and Payment SOPs"},
    "secops_templates": {"name": "Cybersecurity & Incident Management", "icon": "fa-shield-halved", "desc": "Incident Playbooks, CERT-In Reporting SOPs, Severity Matrices, and Training Drills"},
    "vendor_templates": {"name": "Vendor Management & Outsourcing", "icon": "fa-truck-ramp-box", "desc": "Due Diligence, Comparative Statements, SOW/SLA, and Performance SOPs"},
    "pmo_templates": {"name": "PMO & Project Delivery", "icon": "fa-diagram-project", "desc": "Project Charters, WBS Milestones, RACI Matrices, RAID SOPs, and Agile Delivery"},
    "it_cloud_templates": {"name": "IT, Cloud & Passkeys", "icon": "fa-server", "desc": "Operating Models, Passkeys/MFA Authentication SOPs, and Cloud Architecture"},
    "legal_crm_templates": {"name": "Legal Operations & Deal Desk", "icon": "fa-scale-balanced", "desc": "Contracts, NDAs, MSAs, SOWs, Risk Registers, and Authority Matrices"},
    "founder_strategy": {"name": "Founder Strategic Pack", "icon": "fa-chess", "desc": "Strategic Positioning, Brand Narrative, GTM Playbooks, and Product Roadmaps"},
    "incorporation": {"name": "Incorporation & Statutory Pack", "icon": "fa-stamp", "desc": "MOA, AOA, MCA Incorporation Checklists, and Statutory Board Resolutions"}
}

class VaultItemOut(BaseModel):
    category_id: str
    category_name: str
    filename: str
    relative_path: str
    file_type: str
    file_size_kb: float
    download_url: str

class VaultCategorySummary(BaseModel):
    category_id: str
    category_name: str
    icon: str
    description: str
    document_count: int

@router.get("/categories", response_model=List[VaultCategorySummary])
def list_vault_categories():
    results = []
    if not VAULT_DIR.exists():
        return results

    for cat_id, meta in CATEGORY_METADATA.items():
        cat_path = VAULT_DIR / cat_id
        count = 0
        if cat_path.exists():
            for root, dirs, files in os.walk(cat_path):
                count += len([f for f in files if f.endswith(('.docx', '.pdf', '.xlsx', '.txt', '.png'))])
        results.append(VaultCategorySummary(
            category_id=cat_id,
            category_name=meta["name"],
            icon=meta["icon"],
            description=meta["desc"],
            document_count=count
        ))
    return results

@router.get("/documents", response_model=List[VaultItemOut])
def search_vault_documents(
    category: Optional[str] = Query(None, description="Filter by category ID"),
    file_type: Optional[str] = Query(None, description="Filter by extension: docx, pdf, xlsx, txt"),
    search: Optional[str] = Query(None, description="Keyword search in filename")
):
    if hasattr(category, "default"):
        category = None
    if hasattr(file_type, "default"):
        file_type = None
    if hasattr(search, "default"):
        search = None

    items = []
    if not VAULT_DIR.exists():
        return items

    target_cats = [category] if category and category in CATEGORY_METADATA else list(CATEGORY_METADATA.keys())

    for cat_id in target_cats:
        cat_path = VAULT_DIR / cat_id
        if not cat_path.exists():
            continue

        meta = CATEGORY_METADATA.get(cat_id, {"name": cat_id})

        for root, dirs, files in os.walk(cat_path):
            for f in sorted(files):
                ext = f.split(".")[-1].lower() if "." in f else ""
                if file_type and ext != file_type.lower().strip("."):
                    continue
                if search and search.lower() not in f.lower():
                    continue

                full_p = Path(root) / f
                rel_to_cat = full_p.relative_to(cat_path)
                rel_encoded = str(rel_to_cat).replace("\\", "/")
                
                size_kb = round(full_p.stat().st_size / 1024, 1)
                
                download_url = f"/api/v1/vault/download/{cat_id}/{urllib.parse.quote(rel_encoded)}"

                items.append(VaultItemOut(
                    category_id=cat_id,
                    category_name=meta["name"],
                    filename=f,
                    relative_path=rel_encoded,
                    file_type=ext.upper(),
                    file_size_kb=size_kb,
                    download_url=download_url
                ))
    return items

@router.get("/download/{category}/{filepath:path}")
def download_vault_file(category: str, filepath: str):
    if category not in CATEGORY_METADATA:
        raise HTTPException(status_code=404, detail="Category not found")
        
    safe_rel = urllib.parse.unquote(filepath).replace("/", os.sep)
    file_path = (VAULT_DIR / category / safe_rel).resolve()
    
    # Path traversal protection
    if not str(file_path).startswith(str(VAULT_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
        
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
        
    filename = file_path.name
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )

@router.get("/stats")
def get_vault_statistics():
    total_docs = 0
    type_counts = {"DOCX": 0, "PDF": 0, "XLSX": 0, "TXT": 0, "OTHER": 0}
    
    if VAULT_DIR.exists():
        for root, dirs, files in os.walk(VAULT_DIR):
            for f in files:
                ext = f.split(".")[-1].upper()
                if ext in type_counts:
                    type_counts[ext] += 1
                else:
                    type_counts["OTHER"] += 1
                total_docs += 1
                
    return {
        "status": "success",
        "total_documents": total_docs,
        "by_file_type": type_counts,
        "total_categories": len(CATEGORY_METADATA)
    }
