from __future__ import annotations

from typing import Optional

from modules.common.logger import Logger
from utilities.queue_wrapper import QueueProxyWrapper

from .heartbeat_sender import ConnectionInterface, HeartbeatSender


class HeartbeatSenderWorker:
    # Wrapper around HeartbeatSender with a simple run loop.

    def __init__(
        self,
        connection: ConnectionInterface,
        output_queue: Optional[QueueProxyWrapper[str]],
        logger: Logger,
        period_sec: float = 1.0,
    ) -> None:
        self._sender = HeartbeatSender(connection=connection, logger=logger, period_sec=period_sec)
        self._output_queue = output_queue

    def run(self, iterations: int | None = None) -> None:
        self._sender.run(iterations=iterations)
