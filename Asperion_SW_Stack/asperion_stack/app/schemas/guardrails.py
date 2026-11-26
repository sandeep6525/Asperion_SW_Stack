"""
Asperion Enterprise OS - Guardrails & Architectural Schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class GuardrailRuleCreate(BaseModel):
    rule_code: str
    name: str
    category: str = "FinOps"
    regulatory_framework: str = "Internal Financial Controls (IFC)"
    severity: str = "Critical_Blocker"
    enforcement_mode: str = "Active_Blocking"
    description: str
    enforcement_logic: str

class GuardrailRuleOut(GuardrailRuleCreate):
    id: int
    is_active: bool
    total_evaluations: int
    total_passed: int
    total_blocked: int
    total_auto_healed: int
    created_at: datetime
    class Config:
        from_attributes = True

class GuardrailExecutionLogOut(BaseModel):
    id: int
    execution_id: str
    rule_code: str
    module: str
    entity_reference: str
    evaluation_result: str
    trigger_payload_summary: Optional[str]
    action_taken: str
    evaluated_at: datetime
    class Config:
        from_attributes = True

class ArchitectureBlueprintCreate(BaseModel):
    blueprint_code: str
    title: str
    architecture_type: str = "System_Architecture"
    module_pillar: str = "Core Enterprise Platform"
    standard_alignment: str = "ISO 27001 / TOGAF / CMMI"
    diagram_mermaid: str
    description: str
    key_components: str
    guardrail_linkage: Optional[str] = None

class ArchitectureBlueprintOut(ArchitectureBlueprintCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class FlowchartStep(BaseModel):
    step_number: int
    title: str
    actor: str
    input_data: str
    decision_or_processing: str
    guardrail_enforced: str
    output_state: str

class FlowchartDefinitionOut(BaseModel):
    flowchart_id: str
    title: str
    pillar: str
    regulatory_standard: str
    mermaid_diagram: str
    steps: List[FlowchartStep]
    active_guardrails: List[str]
