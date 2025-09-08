from __future__ import annotations

from modules.common.logger import Logger
from utilities.queue_wrapper import QueueProxyWrapper

from .heartbeat_receiver import ConnectionRecvInterface, HeartbeatReceiver


class HeartbeatReceiverWorker:
    """Worker that emits state updates to an output queue once per iteration."""

    def __init__(
        self,
        connection: ConnectionRecvInterface,
        output_queue: QueueProxyWrapper[str],
        logger: Logger,
    ) -> None:
        self._receiver = HeartbeatReceiver(connection=connection, logger=logger)
        self._output_queue = output_queue

    def run(self, iterations: int | None = None) -> None:
        count = 0
        while iterations is None or count < iterations:
            state = self._receiver.run_once()
            self._output_queue.put(state)
            count += 1
