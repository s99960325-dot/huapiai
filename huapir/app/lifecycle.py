import os
import signal
import asyncio

from packaging import version

from huapir.database import DatabaseManager
from huapir.events.application import ApplicationStarted, ApplicationStopping
from huapir.events.event_bus import EventBus
from huapir.im.manager import IMManager
from huapir.internal import shutdown_event
from huapir.ioc.container import DependencyContainer
from huapir.logger import get_logger
from huapir.memory.memory_manager import MemoryManager
from huapir.plugin_manager.plugin_loader import PluginLoader
from huapir.tracing import TracingManager
from huapir.web.api.system.utils import get_installed_version, get_latest_pypi_version
from huapir.web.app import WebServer

logger = get_logger("Lifecycle")
_interrupt_count = 0


async def check_update():
    running_version = get_installed_version()
    logger.info("Checking for updates...")
    latest_version, _ = await get_latest_pypi_version("kirara-ai")
    logger.info(f"Running version: {running_version}, Latest version: {latest_version}")
    if version.parse(latest_version) > version.parse(running_version):
        logger.warning(f"New version {latest_version} is available. Please update to the latest version.")


def _signal_handler(*args):
    global _interrupt_count
    _interrupt_count += 1
    if _interrupt_count == 1:
        if not shutdown_event.is_set():
            logger.warning("Interrupt signal received. Stopping application...")
            shutdown_event.set()
    elif _interrupt_count == 2:
        logger.warning("Interrupt signal received again. Press Ctrl+C one more time to force shutdown...")
    else:
        logger.warning("Interrupt signal received for the third time. Forcing shutdown...")
        os._exit(1)


def _register_signal_handlers():
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal = lambda *args: None


def run_application(container: DependencyContainer):
    loop = container.resolve(asyncio.AbstractEventLoop)
    web_server = container.resolve(WebServer)
    plugin_loader = container.resolve(PluginLoader)
    im_manager = container.resolve(IMManager)
    event_bus = container.resolve(EventBus)

    loop.run_until_complete(web_server.start())
    logger.info(
        "WebUI: http://%s:%s/",
        getattr(web_server, "listen_host", "0.0.0.0"),
        getattr(web_server, "listen_port", 0),
    )
    plugin_loader.start_plugins()
    im_manager.start_adapters(loop=loop)
    _register_signal_handlers()

    try:
        logger.success("Application started. Waiting for events...")
        loop.create_task(check_update())
        event_bus.post(ApplicationStarted())
        loop.run_until_complete(shutdown_event.wait())
    finally:
        event_bus.post(ApplicationStopping())
        container.resolve(MemoryManager).shutdown()
        try:
            container.resolve(TracingManager).shutdown()
        except Exception as e:
            logger.error(f"Error shutting down tracing system: {e}")
        container.resolve(DatabaseManager).shutdown()
        loop.run_until_complete(web_server.stop())
        try:
            im_manager.stop_adapters(loop=loop)
            plugin_loader.stop_plugins()
        except Exception as e:
            logger.error(f"Error stopping adapters: {e}")
        loop.stop()
        logger.info("Application stopped gracefully")
        logger.remove()
