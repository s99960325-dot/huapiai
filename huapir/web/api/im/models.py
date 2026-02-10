from typing import Any, Dict, Optional

from pydantic import BaseModel

from huapir.config.global_config import IMConfig
from huapir.im.im_registry import IMAdapterInfo
from huapir.im.profile import UserProfile

IMAdapterConfig = IMConfig


class IMAdapterStatus(IMAdapterConfig):
    """IM适配器状态"""

    is_running: bool
    bot_profile: Optional[UserProfile] = None

class IMAdapterList(BaseModel):
    """IM适配器列表响应"""

    adapters: list[IMAdapterStatus]


class IMAdapterResponse(BaseModel):
    """单个IM适配器响应"""

    adapter: IMAdapterStatus


class IMAdapterTypes(BaseModel):
    """可用的IM适配器类型列表"""

    types: list[str]
    adapters: dict[str, IMAdapterInfo]

class IMAdapterConfigSchema(BaseModel):
    """IM适配器配置模式"""

    error: Optional[str] = None
    configSchema: Optional[dict[str, Any]] = None
