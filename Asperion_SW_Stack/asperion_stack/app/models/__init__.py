"""
Asperion Enterprise OS - Comprehensive Model Registry
"""
from app.models.governance import (
    EntityMaster, BoardResolution, ComplianceCalendarItem, PolicyRecord, AuthorityMatrixItem, AuditLog
)
from app.models.crm_legal import (
    Prospect, ClientContract, ClientOnboardingRecord, LegalRiskObligation
)
from app.models.finance import (
    AccountMaster, Invoice, PurchaseOrder, APBill, CashFlowEntry, FixedAsset,
    ExpenseClaim, BankReconciliationRecord, JournalEntry, BudgetItem, ProjectPnL
)
from app.models.hrms import (
    Candidate, Employee, SalaryStructure, PayrollRecord, HRLetter, SeparationClearance,
    LeaveRecord, POSHCase
)
from app.models.pmo import (
    Project, ProjectMilestone, WBSTask, RACIAssignment, RAIDItem, ChangeRequest,
    Sprint, Stakeholder
)
from app.models.procurement import (
    Vendor, VendorContract, GoodsReceivedNote, VendorScorecard,
    RFPComparison, VendorRiskAssessment
)
from app.models.infrastructure import (
    ITAsset, CloudAccount, IAMCredential, SaaSLicense, BackupDRPlan,
    CertificateSecret, ITProvisioningChecklist
)
from app.models.cybersecurity import (
    SecurityIncident, SecurityAlert, EvidenceItem, Playbook, VulnerabilityPatch,
    TabletopDrill, CERTInRegulatoryReport, ThreatIntelIndicator
)
from app.models.strategy_kpi import (
    StrategicFunction, CapabilityCapacity, EnterpriseKPI, StrategicDecisionThought, ImplementationRoadmapItem
)
from app.models.crm_enterprise import (
    Opportunity, CRMActivity, CustomerAccount, SupportTicket, EnterpriseRisk
)
from app.models.ticketing_notifications import (
    InternalTicket, SystemNotification, NotificationRule
)
from app.models.developer_platform import (
    DeveloperPlatformAccount, DeveloperEnvironmentSecret, StatutoryChallanFiling
)
from app.models.attendance import (
    GeofenceZone, AttendanceRecord, AttendanceAnomalyLog, WhatsAppAttendanceSession
)
from app.models.guardrails import (
    GuardrailRule, GuardrailExecutionLog, ArchitectureBlueprint
)
from app.models.ai_infrastructure import (
    AIModelEndpoint, MCPServerCatalog, CloudInfrastructureTopology,
    SecurityAuthenticityCertificate, ExecutiveAlertRule
)
from app.models.iso_standards import (
    ISOCertificationMaster, ISOClauseControl, ISOAuditInspection,
    ISOCorrectiveActionWorksheet, FormalGrievanceRecord
)
from app.models.passkey_infrastructure import (
    PasskeyCredential, ZeroTrustPolicy, DRSimulationTest
)
from app.models.communications import (
    ChatChannel, ChatMessage, TeamMemberPresence, VirtualHuddleSession
)
from app.models.sharepoint import (
    SharePointArticle, SharePointComment, SharePointCommunityQuestion, SharePointDocumentLibraryItem
)
from app.models.training import (
    TrainingTrack, TrainingModule, EmployeeTrainingEnrollment, TrainingMaterial
)
from app.models.itsm import (
    ConfigurationItem, ITSMProblem, ITSMChangeRequest, ITSMRunbookFix,
    ITSMProcurementLOI, ITSMSLAContract
)
from app.models.agentic_ai import (
    EnterpriseAgent, AgenticMission, AgentExecutionTrace
)
from app.models.enterprise_operations import (
    EnterpriseEventLedger, DisasterRecoverySnapshot, DPDPConsentRecord, SystemDiagnosticTelemetry
)

__all__ = [
    "EntityMaster", "BoardResolution", "ComplianceCalendarItem", "PolicyRecord", "AuthorityMatrixItem", "AuditLog",
    "Prospect", "ClientContract", "ClientOnboardingRecord", "LegalRiskObligation",
    "AccountMaster", "Invoice", "PurchaseOrder", "APBill", "CashFlowEntry", "FixedAsset",
    "ExpenseClaim", "BankReconciliationRecord", "JournalEntry", "BudgetItem", "ProjectPnL",
    "Candidate", "Employee", "SalaryStructure", "PayrollRecord", "HRLetter", "SeparationClearance",
    "LeaveRecord", "POSHCase",
    "Project", "ProjectMilestone", "WBSTask", "RACIAssignment", "RAIDItem", "ChangeRequest",
    "Sprint", "Stakeholder",
    "Vendor", "VendorContract", "GoodsReceivedNote", "VendorScorecard",
    "RFPComparison", "VendorRiskAssessment",
    "ITAsset", "CloudAccount", "IAMCredential", "SaaSLicense", "BackupDRPlan",
    "CertificateSecret", "ITProvisioningChecklist",
    "SecurityIncident", "SecurityAlert", "EvidenceItem", "Playbook", "VulnerabilityPatch",
    "TabletopDrill", "CERTInRegulatoryReport", "ThreatIntelIndicator",
    "StrategicFunction", "CapabilityCapacity", "EnterpriseKPI", "StrategicDecisionThought", "ImplementationRoadmapItem",
    "Opportunity", "CRMActivity", "CustomerAccount", "SupportTicket", "EnterpriseRisk",
    "InternalTicket", "SystemNotification", "NotificationRule",
    "DeveloperPlatformAccount", "DeveloperEnvironmentSecret", "StatutoryChallanFiling",
    "GeofenceZone", "AttendanceRecord", "AttendanceAnomalyLog", "WhatsAppAttendanceSession",
    "GuardrailRule", "GuardrailExecutionLog", "ArchitectureBlueprint",
    "AIModelEndpoint", "MCPServerCatalog", "CloudInfrastructureTopology",
    "SecurityAuthenticityCertificate", "ExecutiveAlertRule",
    "ISOCertificationMaster", "ISOClauseControl", "ISOAuditInspection",
    "ISOCorrectiveActionWorksheet", "FormalGrievanceRecord",
    "PasskeyCredential", "ZeroTrustPolicy", "DRSimulationTest",
    "ChatChannel", "ChatMessage", "TeamMemberPresence", "VirtualHuddleSession",
    "SharePointArticle", "SharePointComment", "SharePointCommunityQuestion", "SharePointDocumentLibraryItem",
    "TrainingTrack", "TrainingModule", "EmployeeTrainingEnrollment", "TrainingMaterial",
    "ConfigurationItem", "ITSMProblem", "ITSMChangeRequest", "ITSMRunbookFix",
    "ITSMProcurementLOI", "ITSMSLAContract",
    "EnterpriseAgent", "AgenticMission", "AgentExecutionTrace",
    "EnterpriseEventLedger", "DisasterRecoverySnapshot", "DPDPConsentRecord", "SystemDiagnosticTelemetry"
]
