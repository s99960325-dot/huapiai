from abc import ABC
from typing import Protocol, runtime_checkable

from huapir.config.global_config import ModelConfig
from huapir.llm.format.request import LLMChatRequest
from huapir.llm.format.response import LLMChatResponse
from huapir.llm.format.embedding import LLMEmbeddingRequest, LLMEmbeddingResponse
from huapir.llm.format.rerank import LLMReRankRequest, LLMReRankResponse
from huapir.media.manager import MediaManager
from huapir.tracing.llm_tracer import LLMTracer


@runtime_checkable
class AutoDetectModelsProtocol(Protocol):
    async def auto_detect_models(self) -> list[ModelConfig]: ...

@runtime_checkable
class LLMChatProtocol(Protocol):
    def chat(self, req: LLMChatRequest) -> LLMChatResponse: ...

@runtime_checkable
class LLMEmbeddingProtocol(Protocol):
    def embed(self, req: LLMEmbeddingRequest) -> LLMEmbeddingResponse: ...

@runtime_checkable
class LLMReRankProtocol(Protocol):
    def rerank(self, req: LLMReRankRequest) -> LLMReRankResponse: ...

class LLMBackendAdapter(ABC):
    backend_name: str
    media_manager: MediaManager
    tracer: LLMTracer