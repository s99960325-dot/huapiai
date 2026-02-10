

from pydantic import BaseModel

from huapir.workflow.core.block.schema import BlockConfig, BlockInput, BlockOutput


class BlockType(BaseModel):
    """Block类型信息"""

    type_name: str
    name: str
    label: str
    description: str
    inputs: list[BlockInput]
    outputs: list[BlockOutput]
    configs: list[BlockConfig]


class BlockTypeList(BaseModel):
    """Block类型列表响应"""

    types: list[BlockType]


class BlockTypeResponse(BaseModel):
    """单个Block类型响应"""

    type: BlockType
