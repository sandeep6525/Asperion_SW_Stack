"""
Asperion Enterprise OS - AI APIs, Model Context Protocol (MCP), Cloud Infrastructure & Security Authenticity Schemas
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AIModelEndpointCreate(BaseModel):
    endpoint_code: str
    model_name: str
    provider: str
    model_family: str = "Generative Reasoning"
    context_window_tokens: int = 1048576
    rpm_limit: int = 300
    tpm_limit: int = 1000000
    avg_latency_ms: float = 420.0
    cost_per_million_tokens_inr: float = 125.0
    monthly_budget_inr: float = 35000.0
    status: str = "Active"

class AIModelEndpointOut(AIModelEndpointCreate):
    id: int
    current_month_usage_inr: float
    api_key_vault_ref: str
    created_at: datetime
    class Config:
        from_attributes = True

class MCPServerCatalogCreate(BaseModel):
    server_id: str
    name: str
    protocol_version: str = "2024-11-05"
    transport_type: str = "stdio"
    endpoint_or_command: str
    module_pillar: str = "Engineering & Infrastructure"
    auth_mode: str = "Environment_Secret_Injection"
    exposed_tools_count: int = 12
    exposed_resources_count: int = 5
    exposed_prompts_count: int = 3
    description: str

class MCPServerCatalogOut(MCPServerCatalogCreate):
    id: int
    is_connected: bool
    last_ping_status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CloudInfrastructureTopologyCreate(BaseModel):
    node_code: str
    cluster_or_service_name: str
    cloud_provider: str = "AWS"
    resource_type: str = "EKS Kubernetes Cluster"
    region: str = "ap-south-1 (Mumbai)"
    availability_zone: str = "ap-south-1a / ap-south-1b Multi-AZ"
    compute_capacity: str = "8 Nodes (c6i.2xlarge)"
    monthly_cost_inr: float = 45000.0
    uptime_sla_pct: float = 99.99
    auto_scaling_enabled: bool = True
    zero_trust_ingress_verified: bool = True
    technical_lead: str = "Head of Infrastructure (Priya Nair)"

class CloudInfrastructureTopologyOut(CloudInfrastructureTopologyCreate):
    id: int
    current_health: str
    created_at: datetime
    class Config:
        from_attributes = True

class SecurityAuthenticityCertificateCreate(BaseModel):
    cert_code: str
    certificate_name: str
    cert_type: str = "Corporate_Digital_Signature_Class3"
    issuing_authority: str = "e-Mudhra / Verisign"
    subject_entity: str = "ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED"
    public_key_fingerprint: str
    valid_from: date
    valid_until: date
    key_algorithm: str = "RSA 4096-bit / ED25519"
    fips_compliance_level: str = "FIPS 140-3 Level 2 HSM"

class SecurityAuthenticityCertificateOut(SecurityAuthenticityCertificateCreate):
    id: int
    days_until_expiry: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ExecutiveAlertRuleCreate(BaseModel):
    rule_code: str
    title: str
    trigger_condition: str
    target_head_role: str
    target_head_email: str
    target_head_whatsapp: str = "+919886012345"
    dispatch_channels: str = "WhatsApp_Cloud_API, Email_SES, In_App_Cockpit"
    escalation_window_mins: int = 15
    auto_sms_enabled: bool = True

class ExecutiveAlertRuleOut(ExecutiveAlertRuleCreate):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True
