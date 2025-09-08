from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from modules.common.logger import Logger


@dataclass
class TelemetryData:
    time_since_boot_ms: int
    position_x_m: float
    position_y_m: float
    position_z_m: float
    yaw_deg: float


class ConnectionRecvInterface(Protocol):
    def recv_match(
        self, blocking: bool = False, types: list[str] | None = None, timeout: float | None = None
    ) -> object | None: ...


class Telemetry:
    # Collects ATTITUDE and LOCAL_POSITION_NED and emits TelemetryData.

    def __init__(self, connection: ConnectionRecvInterface, logger: Logger) -> None:
        self._connection = connection
        self._logger = logger

    def run_once(self) -> TelemetryData | None:
        attitude_msg = None
        local_pos_msg = None

        try:
            # Try to collect both within 1 second budget
            attitude_msg = self._connection.recv_match(
                blocking=False, types=["ATTITUDE"], timeout=1.0
            )
            local_pos_msg = self._connection.recv_match(
                blocking=False, types=["LOCAL_POSITION_NED"], timeout=1.0
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.error(f"Failed to receive telemetry: {exc}")
            return None

        if attitude_msg is None or local_pos_msg is None:
            self._logger.warning("Telemetry timeout waiting for ATTITUDE and LOCAL_POSITION_NED")
            return None

        # Map messages to TelemetryData fields; assume mock messages expose fields
        try:
            yaw_deg = float(getattr(attitude_msg, "yaw_deg", 0.0))
            # Using right-handed x-y-z (x right, y forward, z up)
            x = float(getattr(local_pos_msg, "x_m", 0.0))
            y = float(getattr(local_pos_msg, "y_m", 0.0))
            z = float(getattr(local_pos_msg, "z_m", 0.0))
            t_att = int(getattr(attitude_msg, "time_since_boot_ms", 0))
            t_pos = int(getattr(local_pos_msg, "time_since_boot_ms", 0))
            t = max(t_att, t_pos)
        except Exception as exc:  # noqa: BLE001
            self._logger.error(f"Malformed telemetry messages: {exc}")
            return None

        return TelemetryData(
            time_since_boot_ms=t, position_x_m=x, position_y_m=y, position_z_m=z, yaw_deg=yaw_deg
        )
