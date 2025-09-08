from __future__ import annotations

from modules.common.logger import Logger
from utilities.queue_wrapper import QueueProxyWrapper

from .telemetry import ConnectionRecvInterface, Telemetry, TelemetryData


class TelemetryWorker:
    # Emits the latest TelemetryData when both messages are present.

    def __init__(
        self,
        connection: ConnectionRecvInterface,
        output_queue: QueueProxyWrapper[TelemetryData],
        logger: Logger,
    ) -> None:
        self._telemetry = Telemetry(connection=connection, logger=logger)
        self._output_queue = output_queue

    def run(self, iterations: int | None = None) -> None:
        count = 0
        while iterations is None or count < iterations:
            data = self._telemetry.run_once()
            if data is not None:
                self._output_queue.put(data)
            count += 1
