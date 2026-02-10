import asyncio

from huapir.config.global_config import GlobalConfig
from huapir.im.adapter import IMAdapter
from huapir.im.message import IMMessage
from huapir.ioc.container import DependencyContainer
from huapir.logger import get_logger
from huapir.multitenancy.context import use_tenant_context
from huapir.multitenancy.service import TenantService
from huapir.workflow.core.dispatch.models.dispatch_rules import CombinedDispatchRule
from huapir.workflow.core.dispatch.registry import DispatchRuleRegistry
from huapir.observability.metrics import metrics_registry
from huapir.workflow.core.dispatch.rules.base import DispatchRule
from huapir.workflow.core.execution.exceptions import WorkflowExecutionTimeoutException
from huapir.workflow.core.execution.executor import WorkflowExecutor
from huapir.workflow.core.workflow.base import Workflow
from huapir.workflow.core.workflow.registry import WorkflowRegistry

from .exceptions import WorkflowNotFoundException


class WorkflowDispatcher:
    """工作流调度器"""

    def __init__(self, container: DependencyContainer):
        self.container = container
        self.logger = get_logger("WorkflowDispatcher")

        # 从容器获取注册表
        self.workflow_registry = container.resolve(WorkflowRegistry)
        self.dispatch_registry = container.resolve(DispatchRuleRegistry)
        self._semaphore = asyncio.Semaphore(self._resolve_max_inflight())

    def _resolve_max_inflight(self) -> int:
        if self.container.has(GlobalConfig):
            max_inflight = self.container.resolve(GlobalConfig).system.dispatcher_max_inflight
            return max(1, max_inflight)
        return 128

    def _resolve_tenant_id(self, message: IMMessage) -> str:
        if self.container.has(GlobalConfig):
            config = self.container.resolve(GlobalConfig)
            default_tenant_id = config.tenant.default_tenant_id
        else:
            default_tenant_id = "default"

        sender = message.sender
        metadata = sender.raw_metadata or {}
        if "tenant_id" in metadata and metadata["tenant_id"]:
            return str(metadata["tenant_id"])

        if self.container.has(TenantService):
            tenant_service = self.container.resolve(TenantService)
            tenant_id = tenant_service.resolve_tenant_for_user(sender.user_id)
            if tenant_id:
                return tenant_id
        return default_tenant_id

    def register_rule(self, rule: CombinedDispatchRule):
        """注册一个调度规则"""
        self.dispatch_registry.register(rule)
        self.logger.info(f"Registered dispatch rule: {rule}")

    async def dispatch(self, source: IMAdapter, message: IMMessage):
        """
        根据消息内容选择第一个匹配的规则进行处理
        """
        async with self._semaphore:
            with self.container.scoped() as scoped_container:
                scoped_container.register(IMAdapter, source)
                scoped_container.register(IMMessage, message)
                tenant_id = self._resolve_tenant_id(message)
                scoped_container.register("tenant_id", tenant_id)
                with use_tenant_context(tenant_id=tenant_id, user_id=message.sender.user_id):
                    active_rules = self.dispatch_registry.get_active_rules()
                    for rule in active_rules:
                        if rule.match(message, self.workflow_registry, scoped_container):
                            scoped_container.register(DispatchRule, rule)
                            metrics_registry.inc("workflow_dispatches_total")
                            try:
                                self.logger.debug(f"Matched rule {rule}, executing workflow")
                                workflow = rule.get_workflow(scoped_container)
                                if workflow is None:
                                    raise WorkflowNotFoundException(f"Workflow for rule {rule.name} not found, please check the rule configuration")
                                scoped_container.register(Workflow, workflow)
                                executor = WorkflowExecutor(scoped_container)
                                scoped_container.register(WorkflowExecutor, executor)
                                return await executor.run()
                            except WorkflowExecutionTimeoutException as e:
                                metrics_registry.inc("workflow_dispatch_failures_total")
                                self.logger.error(f"Workflow execution timed out: {e}")
                                return None
                            except Exception as e:
                                metrics_registry.inc("workflow_dispatch_failures_total")
                                self.logger.opt(exception=e).error(f"Workflow execution failed: {e}")
                                return None
                    self.logger.debug("No matching rule found for message")
                    return None
