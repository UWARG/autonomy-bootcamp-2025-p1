from __future__ import annotations

from typing import Protocol

from modules.common.logger import Logger


class ConnectionRecvInterface(Protocol):  # pragma: no cover - Protocol
    def recv_match(
        self, blocking: bool = False, types: list[str] | None = None, timeout: float | None = None
    ) -> object | None: ...


class HeartbeatReceiver:
    # Receives HEARTBEAT messages and tracks connection state.

    def __init__(
        self, connection: ConnectionRecvInterface, logger: Logger, misses_to_disconnect: int = 5
    ) -> None:
        self._connection = connection
        self._logger = logger
        self._misses_to_disconnect = misses_to_disconnect
        self._misses = 0
        self._connected = False

    @property
    def state(self) -> str:
        return "Connected" if self._connected else "Disconnected"

    def run_once(self) -> str:
        """Handle one second's worth of checks.

        Returns the current state string.
        """

        try:
            msg = self._connection.recv_match(blocking=False, types=["HEARTBEAT"], timeout=1.0)
        except Exception as exc:  # noqa: BLE001
            self._logger.error(f"Failed to receive HEARTBEAT: {exc}")
            msg = None

        if msg is not None:
            self._misses = 0
            if not self._connected:
                self._logger.info("Heartbeat received; transitioning to Connected")
            self._connected = True
        else:
            self._misses += 1
            self._logger.warning("Missed HEARTBEAT")
            if self._misses >= self._misses_to_disconnect:
                if self._connected:
                    self._logger.warning(
                        "Missed 5 consecutive HEARTBEATs; transitioning to Disconnected"
                    )
                self._connected = False

        return self.state
