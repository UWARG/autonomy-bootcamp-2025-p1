from __future__ import annotations

import time
from typing import Protocol

from modules.common.logger import Logger


class MavInterface(Protocol):  # pragma: no cover - Protocol
    def heartbeat_send(self) -> None: ...


class ConnectionInterface(Protocol):  # pragma: no cover - Protocol
    @property
    def mav(self) -> MavInterface: ...


class HeartbeatSender:
    # Sends HEARTBEAT messages at a fixed interval.

    def __init__(
        self, connection: ConnectionInterface, logger: Logger, period_sec: float = 1.0
    ) -> None:
        self._connection = connection
        self._logger = logger
        self._period_sec = period_sec

    def run_once(self) -> None:
        """Send a single HEARTBEAT."""

        try:
            self._connection.mav.heartbeat_send()
            self._logger.info("Sent HEARTBEAT")
        except Exception as exc:  # noqa: BLE001 - want broad catch to log
            self._logger.error(f"Failed to send HEARTBEAT: {exc}")

    def run(self, iterations: int | None = None) -> None:
        """Run sending loop.

        iterations: if provided, run that many cycles; otherwise run forever.
        """

        count = 0
        while iterations is None or count < iterations:
            self.run_once()
            count += 1
            time.sleep(self._period_sec)
