"""
Asperion Enterprise OS - AI APIs, Model Context Protocol (MCP), Cloud Infrastructure & Security Authenticity Models
Pillars: AI Engineering, Autonomous Agents, Multi-Cloud Topology, Cryptographic Authenticity & Security Mesh
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AIModelEndpoint(Base):
    """
    Catalog of enterprise-grade AI LLMs, SLMs, Embedding Models & Vision APIs.
    Tracks token rate limits, monthly spend quotas, latency SLA, and context window.
    """
    __tablename__ = "ai_model_endpoints"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_code = Column(String(50), unique=True, index=True) # e.g. AI-GEMINI-25-PRO, AI-CLAUDE-37, AI-DEEPSEEK-R1
    model_name = Column(String(100), nullable=False) # Gemini 2.5 Pro, Claude 3.7 Sonnet, DeepSeek-R1, OpenAI GPT-4.5
    provider = Column(String(50), nullable=False) # Google Cloud Vertex, Anthropic, OpenAI, DeepSeek, AWS Bedrock
    model_family = Column(String(50), default="Generative Reasoning") # Multimodal LLM, Code Intelligence, Small Language Model (SLM), Embedding
    context_window_tokens = Column(Integer, default=1048576) # Context window size (e.g. 1M or 2M tokens)
    rpm_limit = Column(Integer, default=300) # Requests per minute rate limit
    tpm_limit = Column(Integer, default=1000000) # Tokens per minute
    avg_latency_ms = Column(Float, default=420.0)
    cost_per_million_tokens_inr = Column(Float, default=125.0)
    monthly_budget_inr = Column(Float, default=35000.0)
    current_month_usage_inr = Column(Float, default=14200.0)
    status = Column(String(30), default="Active") # Active, Throttled, Deprecated, Standby
    api_key_vault_ref = Column(String(100), default="SEC-ROT-001 (Encrypted Vault)")
    created_at = Column(DateTime, default=datetime.utcnow)

class MCPServerCatalog(Base):
    """
    Model Context Protocol (MCP) Server Registry.
    Standardized open protocol connecting AI reasoning agents to enterprise tools, DBs, and repositories.
    """
    __tablename__ = "mcp_servers"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String(50), unique=True, index=True) # e.g. MCP-POSTGRES-SRV, MCP-GITHUB-SRV, MCP-AWS-SRV
    name = Column(String(100), nullable=False)
    protocol_version = Column(String(20), default="2024-11-05")
    transport_type = Column(String(30), default="stdio") # stdio, sse (Server-Sent Events), websocket
    endpoint_or_command = Column(String(255), nullable=False) # npx -y @modelcontextprotocol/server-postgres, etc.
    module_pillar = Column(String(50), default="Engineering & Infrastructure")
    auth_mode = Column(String(50), default="Environment_Secret_Injection") # Environment_Secret_Injection, OAuth2, Mutual_TLS
    exposed_tools_count = Column(Integer, default=12)
    exposed_resources_count = Column(Integer, default=5)
    exposed_prompts_count = Column(Integer, default=3)
    is_connected = Column(Boolean, default=True)
    last_ping_status = Column(String(30), default="Healthy (12ms)")
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CloudInfrastructureTopology(Base):
    """
    Multi-Cloud & Hybrid Infrastructure Topology.
    AWS, Azure, GCP, Cloudflare edge, Kubernetes clusters, VPC peering, and DR failover nodes.
    """
    __tablename__ = "cloud_infrastructure_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_code = Column(String(50), unique=True, index=True) # e.g. CLD-K8S-MUM-01, CLD-RDS-WAL-01, CLD-CF-EDGE
    cluster_or_service_name = Column(String(100), nullable=False)
    cloud_provider = Column(String(50), default="AWS") # AWS, GCP, Cloudflare, Azure, Hybrid Local Horamavu
    resource_type = Column(String(50), default="EKS Kubernetes Cluster") # EKS Cluster, RDS Postgres WAL, Edge CDN, VPC NAT Gateway
    region = Column(String(50), default="ap-south-1 (Mumbai)")
    availability_zone = Column(String(50), default="ap-south-1a / ap-south-1b Multi-AZ")
    compute_capacity = Column(String(100), default="8 Nodes (c6i.2xlarge, 64 vCPU, 128 GB RAM)")
    monthly_cost_inr = Column(Float, default=45000.0)
    uptime_sla_pct = Column(Float, default=99.99)
    current_health = Column(String(30), default="Optimal") # Optimal, Warning, Degraded, Disaster_Recovery_Active
    auto_scaling_enabled = Column(Boolean, default=True)
    zero_trust_ingress_verified = Column(Boolean, default=True)
    technical_lead = Column(String(100), default="Head of Infrastructure (Priya Nair)")
    created_at = Column(DateTime, default=datetime.utcnow)

class SecurityAuthenticityCertificate(Base):
    """
    Cryptographic authenticity, verifiable credentials, and public key pinning registry.
    Ensures non-repudiation, tamper-evident signing of letters, payroll, invoices, and certificates.
    """
    __tablename__ = "security_authenticity_certificates"

    id = Column(Integer, primary_key=True, index=True)
    cert_code = Column(String(50), unique=True, index=True) # e.g. AUTH-CORP-SIGN-2026, AUTH-MCA-DS-01
    certificate_name = Column(String(150), nullable=False)
    cert_type = Column(String(50), default="Corporate_Digital_Signature_Class3") # Class 3 DSC, TLS Wildcard, ED25519 Document Key, mTLS Service Key
    issuing_authority = Column(String(100), default="e-Mudhra / Verisign / Let's Encrypt")
    subject_entity = Column(String(200), default="ASPERION DIGITAL TECHNOLOGIES (OPC) PRIVATE LIMITED")
    public_key_fingerprint = Column(String(128), nullable=False) # SHA-256 fingerprint
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)
    days_until_expiry = Column(Integer, default=340)
    key_algorithm = Column(String(50), default="RSA 4096-bit / ED25519")
    status = Column(String(30), default="Valid & Trusted") # Valid & Trusted, Revocation_Pending, Expired
    fips_compliance_level = Column(String(50), default="FIPS 140-3 Level 2 HSM")
    created_at = Column(DateTime, default=datetime.utcnow)

class ExecutiveAlertRule(Base):
    """
    High-priority automated escalation rules to concerned department heads and Sole Director.
    Routes security breaches, cash dips, statutory MSME dues, SLA breaches, and quality gates.
    """
    __tablename__ = "executive_alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_code = Column(String(50), unique=True, index=True) # e.g. EAR-FIN-CASH, EAR-SEC-P1, EAR-MSME-45D
    title = Column(String(150), nullable=False)
    trigger_condition = Column(String(255), nullable=False)
    target_head_role = Column(String(100), nullable=False) # Sole Director (Varadi Vijay), Head of Legal, CFO, CISO, Head of Delivery
    target_head_email = Column(String(100), nullable=False)
    target_head_whatsapp = Column(String(50), default="+919886012345")
    dispatch_channels = Column(String(100), default="WhatsApp_Cloud_API, Email_SES, In_App_Cockpit")
    escalation_window_mins = Column(Integer, default=15) # Escalate within 15 mins if unacknowledged
    auto_sms_enabled = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
