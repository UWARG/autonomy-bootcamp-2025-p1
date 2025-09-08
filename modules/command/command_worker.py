from __future__ import annotations

from typing import Optional

from modules.common.logger import Logger
from modules.telemetry.telemetry import TelemetryData
from utilities.queue_wrapper import QueueProxyWrapper

from .command import CommandLogic, ConnectionInterface, Target


class CommandWorker:
    # Consumes TelemetryData, commands the drone, and emits action strings.

    def __init__(
        self,
        connection: ConnectionInterface,
        telemetry_queue: QueueProxyWrapper[TelemetryData],
        output_queue: Optional[QueueProxyWrapper[str]],
        target: Target,
        logger: Logger,
    ) -> None:
        self._logic = CommandLogic(connection=connection, target=target, logger=logger)
        self._telemetry_queue = telemetry_queue
        self._output_queue = output_queue

    def run(self, iterations: int | None = None) -> None:
        count = 0
        while iterations is None or count < iterations:
            data = self._telemetry_queue.get(timeout=1.0)
            if data is None:
                continue
            outputs = self._logic.run_once(data)
            if self._output_queue is not None:
                for msg in outputs:
                    self._output_queue.put(msg)
            count += 1
