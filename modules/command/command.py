from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol

from modules.common.logger import Logger
from modules.telemetry.telemetry import TelemetryData


@dataclass
class Target:
    x_m: float
    y_m: float
    z_m: float


class MavCmdInterface(Protocol):  # pragma: no cover - Protocol
    def command_long_send(
        self,
        command: int,
        param1: float,
        param2: float,
        param3: float,
        param4: float,
        param5: float,
        param6: float,
        param7: float,
    ) -> None: ...


class ConnectionInterface(Protocol):  # pragma: no cover - Protocol
    @property
    def mav(self) -> MavCmdInterface: ...


MAV_CMD_CONDITION_CHANGE_ALT = 113
MAV_CMD_CONDITION_YAW = 115


class CommandLogic:
    # Compute altitude/yaw corrections, send COMMAND_LONGs, and log average velocity.

    def __init__(self, connection: ConnectionInterface, target: Target, logger: Logger) -> None:
        self._connection = connection
        self._target = target
        self._logger = logger
        self._first: TelemetryData | None = None
        self._last: TelemetryData | None = None

    def _angle_to_target_deg(self, data: TelemetryData) -> float:
        dx = self._target.x_m - data.position_x_m
        dy = self._target.y_m - data.position_y_m
        angle_rad = math.atan2(dy, dx)
        return math.degrees(angle_rad)

    @staticmethod
    def _wrap_deg(angle: float) -> float:
        angle = (angle + 180.0) % 360.0 - 180.0
        return angle

    def _update_avg_velocity(self, data: TelemetryData) -> None:
        if self._first is None:
            self._first = data
            self._last = data
            return

        self._last = data
        dt_s = max(1e-6, (self._last.time_since_boot_ms - self._first.time_since_boot_ms) / 1000.0)
        vx = (self._last.position_x_m - self._first.position_x_m) / dt_s
        vy = (self._last.position_y_m - self._first.position_y_m) / dt_s
        vz = (self._last.position_z_m - self._first.position_z_m) / dt_s
        self._logger.info(f"Average velocity so far (m/s): ({vx:.2f}, {vy:.2f}, {vz:.2f})")

    def run_once(self, data: TelemetryData) -> list[str]:
        outputs: list[str] = []

        # Altitude control
        dz = self._target.z_m - data.position_z_m
        if abs(dz) > 0.5:
            try:
                self._connection.mav.command_long_send(
                    MAV_CMD_CONDITION_CHANGE_ALT, dz, 0, 0, 0, 0, 0, 0
                )
                outputs.append(f"CHANGE ALTITUDE: {dz:.2f}")
            except Exception as exc:  # noqa: BLE001
                self._logger.error(f"Failed to send altitude command: {exc}")

        # Yaw control
        desired_yaw = self._angle_to_target_deg(data)
        dyaw = self._wrap_deg(desired_yaw - data.yaw_deg)
        if abs(dyaw) > 5.0:
            try:
                self._connection.mav.command_long_send(
                    MAV_CMD_CONDITION_YAW, dyaw, 0, 1, 0, 0, 0, 0
                )
                outputs.append(f"CHANGE YAW: {dyaw:.2f}")
            except Exception as exc:  # noqa: BLE001
                self._logger.error(f"Failed to send yaw command: {exc}")

        self._update_avg_velocity(data)
        return outputs
