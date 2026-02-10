from typing import Any, Dict, Optional

from pydantic import BaseModel

from huapir.workflow.core.workflow.base import WorkflowConfig


class Wire(BaseModel):
    """工作流连线"""

    source_block: str  # block ID
    source_output: str
    target_block: str  # block ID
    target_input: str


class BlockInstance(BaseModel):
    """工作流中的Block实例"""

    type_name: str
    name: str
    config: dict[str, Any]
    position: dict[str, int]  # x, y 坐标


class WorkflowDefinition(BaseModel):
    """工作流定义"""

    group_id: str
    workflow_id: str
    name: str
    description: str
    blocks: list[BlockInstance]
    wires: list[Wire]
    config: WorkflowConfig = WorkflowConfig()
    metadata: Optional[dict[str, Any]] = None


class WorkflowInfo(BaseModel):
    """工作流基本信息"""

    group_id: str
    workflow_id: str
    name: str
    description: str
    block_count: int
    metadata: Optional[dict[str, Any]] = None


class WorkflowList(BaseModel):
    """工作流列表响应"""

    workflows: list[WorkflowInfo]


class WorkflowResponse(BaseModel):
    """单个工作流响应"""

    workflow: WorkflowDefinition
