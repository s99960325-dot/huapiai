import asyncio
import inspect
from typing import Any, Callable, Dict, Optional, Type

from huapir.logger import get_logger

logger = get_logger("EventBus")

class EventBus:
    def __init__(self):
        self._listeners: dict[Type, list[Callable]] = {}
        self._queue: Optional[asyncio.Queue[Any]] = None
        self._worker_task: Optional[asyncio.Task[Any]] = None
        self._metrics = {
            "posted": 0,
            "processed": 0,
            "failed": 0,
            "queued": 0,
            "dropped": 0,
        }

    def register(self, event_type: Type, listener: Callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unregister(self, event_type: Type, listener: Callable):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def _run_listener(self, listener: Callable, event: Any):
        listener_name = getattr(listener, "__name__", listener.__class__.__name__)
        try:
            result = listener(event)
            if inspect.isawaitable(result):
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(result)
                except RuntimeError:
                    asyncio.run(result)
        except Exception as e:
            self._metrics["failed"] += 1
            logger.opt(exception=e).error(f"Error in listener {listener_name}")

    def post(self, event: Any):
        self._metrics["posted"] += 1
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                self._run_listener(listener, event)
        self._metrics["processed"] += 1

    async def post_async(self, event: Any):
        self.post(event)

    async def start_worker(self, max_queue_size: int = 1000):
        if self._queue is None:
            self._queue = asyncio.Queue(maxsize=max_queue_size)
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker(), name="kirara-event-bus-worker")

    async def stop_worker(self):
        if self._worker_task is None:
            return
        await self._queue.put(None)  # type: ignore[arg-type]
        await self._worker_task
        self._worker_task = None

    async def enqueue(self, event: Any) -> bool:
        if self._queue is None:
            await self.start_worker()
        assert self._queue is not None
        if self._queue.full():
            self._metrics["dropped"] += 1
            return False
        await self._queue.put(event)
        self._metrics["queued"] += 1
        return True

    async def _worker(self):
        assert self._queue is not None
        while True:
            event = await self._queue.get()
            if event is None:
                self._queue.task_done()
                break
            try:
                self.post(event)
            finally:
                self._queue.task_done()

    def get_metrics(self) -> dict[str, int]:
        return dict(self._metrics)
