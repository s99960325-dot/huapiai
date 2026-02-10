from abc import ABC, abstractmethod
from typing import Optional, Union

from huapir.im.message import IMMessage
from huapir.im.sender import ChatSender
from huapir.ioc.container import DependencyContainer
from huapir.llm.format.message import LLMChatMessage
from huapir.llm.format.response import Message
from huapir.memory.entry import MemoryEntry

# 可组合的消息类型
ComposableMessageType = Union[IMMessage, LLMChatMessage, Message, str]


class MemoryComposer(ABC):
    """记忆组合器抽象类"""
    
    container: DependencyContainer

    @abstractmethod
    def compose(
        self, sender: Optional[ChatSender], message: list[ComposableMessageType]
    ) -> MemoryEntry:
        """将消息转换为记忆条目"""


class MemoryDecomposer(ABC):
    """记忆解析器抽象类"""
    
    container: DependencyContainer

    @abstractmethod
    def decompose(self, entries: list[MemoryEntry]) -> list[ComposableMessageType]:
        """将记忆条目转换为消息"""

    @property
    def empty_message(self) -> ComposableMessageType:
        """空记忆消息"""
        return "<空记忆>"
