from typing import Annotated, Any, Dict

from huapir.im.message import IMMessage, TextMessage
from huapir.im.sender import ChatSender
from huapir.ioc.container import DependencyContainer
from huapir.memory.memory_manager import MemoryManager
from huapir.memory.registry import ScopeRegistry
from huapir.workflow.core.block import Block, Input, Output, ParamMeta


class ClearMemory(Block):
    """Block for clearing conversation memory"""

    name = "clear_memory"
    inputs = {
        "chat_sender": Input("chat_sender", "消息发送者", ChatSender, "消息发送者")
    }
    outputs = {"response": Output("response", "响应", IMMessage, "响应")}
    container: DependencyContainer

    def __init__(
        self,
        scope_type: Annotated[
            str, ParamMeta(label="级别", description="要清空记忆的级别")
        ] = "member",
    ):
        self.scope_type = scope_type

    def execute(self, chat_sender: ChatSender) -> dict[str, Any]:
        self.memory_manager = self.container.resolve(MemoryManager)

        # Get scope instance
        scope_registry = self.container.resolve(ScopeRegistry)
        self.scope = scope_registry.get_scope(self.scope_type)
        # Clear memory using the manager's method
        self.memory_manager.clear_memory(self.scope, chat_sender)
        return {
            "response": IMMessage(
                sender=chat_sender,
                message_elements=[TextMessage("已清空当前对话的记忆。")],
            )
        }
