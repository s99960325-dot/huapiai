

from pydantic import BaseModel

from huapir.workflow.core.dispatch import CombinedDispatchRule


class DispatchRuleList(BaseModel):
    """调度规则列表"""

    rules: list[CombinedDispatchRule]


class DispatchRuleResponse(BaseModel):
    """调度规则响应"""

    rule: CombinedDispatchRule
