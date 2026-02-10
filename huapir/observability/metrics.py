import threading
from typing import Dict


class MetricsRegistry:
    def __init__(self):
        self._lock = threading.Lock()
        self._counters: dict[str, int] = {}
        self._gauges: dict[str, float] = {}

    def inc(self, metric_name: str, value: int = 1):
        with self._lock:
            self._counters[metric_name] = self._counters.get(metric_name, 0) + value

    def set_gauge(self, metric_name: str, value: float):
        with self._lock:
            self._gauges[metric_name] = value

    def export_prometheus_text(self) -> str:
        with self._lock:
            lines = []
            for key, value in sorted(self._counters.items()):
                lines.append(f"# TYPE {key} counter")
                lines.append(f"{key} {value}")
            for key, value in sorted(self._gauges.items()):
                lines.append(f"# TYPE {key} gauge")
                lines.append(f"{key} {value}")
            return "\n".join(lines) + "\n"


metrics_registry = MetricsRegistry()
