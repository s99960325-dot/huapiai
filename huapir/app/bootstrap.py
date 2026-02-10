import asyncio
import os
import time

from huapir.config import CONFIG_FILE
from huapir.config.config_loader import ConfigLoader
from huapir.config.global_config import GlobalConfig
from huapir.database import DatabaseManager
from huapir.events.event_bus import EventBus
from huapir.im.im_registry import IMRegistry
from huapir.im.manager import IMManager
from huapir.ioc.container import DependencyContainer
from huapir.llm.llm_manager import LLMManager
from huapir.llm.llm_registry import LLMBackendRegistry
from huapir.logger import get_logger
from huapir.media import MediaManager
from huapir.media.carrier import MediaCarrierRegistry, MediaCarrierService
from huapir.memory.composes import DefaultMemoryComposer, DefaultMemoryDecomposer, MultiElementDecomposer
from huapir.memory.memory_manager import MemoryManager
from huapir.memory.scopes import GlobalScope, GroupScope, MemberScope
from huapir.multitenancy.service import TenantService
from huapir.plugin_manager.plugin_loader import PluginLoader
from huapir.tracing import LLMTracer, TracingManager
from huapir.web.app import WebServer
from huapir.workflow.core.block import BlockRegistry
from huapir.workflow.core.dispatch import DispatchRuleRegistry, WorkflowDispatcher
from huapir.workflow.core.workflow import WorkflowRegistry
from huapir.workflow.implementations.blocks import register_system_blocks
from huapir.workflow.implementations.workflows import register_system_workflows

logger = get_logger("Bootstrap")


def init_container() -> DependencyContainer:
    container = DependencyContainer()
    container.register(DependencyContainer, container)
    return container


def load_global_config() -> GlobalConfig:
    logger.info(f"Loading configuration from {CONFIG_FILE}")
    config_dir = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        config = ConfigLoader.load_config(CONFIG_FILE, GlobalConfig)
        logger.info("Configuration loaded successfully")
        return config
    logger.warning(f"Configuration file {CONFIG_FILE} not found, using default configuration")
    logger.warning("Please create config.yaml by copying config.yaml.example")
    return GlobalConfig()


def init_memory_system(container: DependencyContainer):
    memory_manager = MemoryManager(container)
    memory_manager.register_scope("member", MemberScope)
    memory_manager.register_scope("group", GroupScope)
    memory_manager.register_scope("global", GlobalScope)
    memory_manager.register_composer("default", DefaultMemoryComposer)
    memory_manager.register_decomposer("default", DefaultMemoryDecomposer)
    memory_manager.register_decomposer("multi_element", MultiElementDecomposer)
    container.register(MemoryManager, memory_manager)
    return memory_manager


def init_media_carrier(container: DependencyContainer):
    carrier_registry = container.resolve(MediaCarrierRegistry)
    carrier_registry.register("memory", container.resolve(MemoryManager))


def init_tracing_system(container: DependencyContainer):
    tracing_manager = TracingManager(container)
    container.register(TracingManager, tracing_manager)
    llm_tracer = LLMTracer(container)
    container.register(LLMTracer, llm_tracer)
    tracing_manager.register_tracer("llm", llm_tracer)
    tracing_manager.initialize()
    return tracing_manager


def register_core_services(container: DependencyContainer, config: GlobalConfig):
    container.register(asyncio.AbstractEventLoop, asyncio.new_event_loop())
    container.register(EventBus, EventBus())
    container.register(GlobalConfig, config)
    container.register(BlockRegistry, BlockRegistry())

    db = DatabaseManager(container)
    db.initialize()
    container.register(DatabaseManager, db)

    media_manager = MediaManager()
    container.register(MediaManager, media_manager)
    container.register(MediaCarrierRegistry, MediaCarrierRegistry(container))
    container.register(MediaCarrierService, MediaCarrierService(container, media_manager))

    workflow_registry = WorkflowRegistry(container)
    container.register(WorkflowRegistry, workflow_registry)
    dispatch_registry = DispatchRuleRegistry(container)
    container.register(DispatchRuleRegistry, dispatch_registry)

    container.register(IMRegistry, IMRegistry())
    container.register(LLMBackendRegistry, LLMBackendRegistry())
    container.register(IMManager, IMManager(container))
    container.register(LLMManager, LLMManager(container))
    container.register(
        PluginLoader,
        PluginLoader(container, os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")),
    )
    container.register(WorkflowDispatcher, WorkflowDispatcher(container))
    container.register(WebServer, WebServer(container))
    container.register(TenantService, TenantService(container))


def init_application() -> DependencyContainer:
    logger.info("Initializing application...")
    config = load_global_config()
    os.environ["TZ"] = config.system.timezone
    if hasattr(time, "tzset"):
        time.tzset()

    container = init_container()
    register_core_services(container, config)

    init_memory_system(container)
    init_media_carrier(container)
    init_tracing_system(container)
    register_system_blocks(container.resolve(BlockRegistry))

    plugin_loader = container.resolve(PluginLoader)
    plugin_loader.discover_internal_plugins()
    plugin_loader.discover_external_plugins()
    plugin_loader.load_plugins()

    workflow_registry = container.resolve(WorkflowRegistry)
    workflow_registry.load_workflows()
    register_system_workflows(workflow_registry)
    dispatch_registry = container.resolve(DispatchRuleRegistry)
    dispatch_registry.load_rules()

    llm_manager = container.resolve(LLMManager)
    llm_manager.load_config()

    tenant_service = container.resolve(TenantService)
    tenant_service.ensure_default_tenant(config.tenant.default_tenant_id)
    return container
