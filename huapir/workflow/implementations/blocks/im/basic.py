from typing import Any, Dict

from huapir.im.message import IMMessage
from huapir.im.sender import ChatSender
from huapir.ioc.container import DependencyContainer
from huapir.workflow.core.block import Block
from huapir.workflow.core.block.input_output import Input, Output


class ExtractChatSender(Block):
    """提取消息发送者"""

    name = "extract_chat_sender"
    container: DependencyContainer
    inputs = {"msg": Input("msg", "IM 消息", IMMessage, "IM 消息")}
    outputs = {"sender": Output("sender", "消息发送者", ChatSender, "消息发送者")}

    def execute(self, **kwargs) -> dict[str, Any]:
        msg = self.container.resolve(IMMessage)
        return {"sender": msg.sender}
