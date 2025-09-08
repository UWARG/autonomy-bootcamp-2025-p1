from __future__ import annotations

import queue
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class QueueProxyWrapper(Generic[T]):
    # Simple thread/process-safe queue wrapper with a minimal API.

    def __init__(self) -> None:
        self._q: queue.Queue[T] = queue.Queue()

    def put(self, item: T) -> None:
        self._q.put(item)

    def get(self, timeout: Optional[float] = None) -> Optional[T]:
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def empty(self) -> bool:
        return self._q.empty()
