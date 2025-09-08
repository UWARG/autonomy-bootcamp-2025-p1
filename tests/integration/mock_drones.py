from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


class _MockMav:
    def __init__(self, parent: "MockConnection") -> None:
        self._parent = parent

    def heartbeat_send(self) -> None:
        self._parent._inbox.append({"type": "HEARTBEAT"})

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
    ) -> None:
        self._parent._commands.append(
            (command, param1, param2, param3, param4, param5, param6, param7)
        )


@dataclass
class _Attitude:
    time_since_boot_ms: int
    yaw_deg: float


@dataclass
class _LocalPosition:
    time_since_boot_ms: int
    x_m: float
    y_m: float
    z_m: float


class MockConnection:
    """Tiny mock of MAVLink connection for integration tests.

    - `mav.heartbeat_send()` pushes a heartbeat message into the inbox.
    - `recv_match(type=[...])` pops the first message of the requested type.
    - `mav.command_long_send(...)` records commands in `_commands`.
    """

    def __init__(self) -> None:
        self._inbox: list[Any] = []
        self._commands: list[tuple] = []
        self.mav = _MockMav(self)

    def feed_attitude(self, time_since_boot_ms: int, yaw_deg: float) -> None:
        self._inbox.append(_Attitude(time_since_boot_ms=time_since_boot_ms, yaw_deg=yaw_deg))

    def feed_local_position(
        self, time_since_boot_ms: int, x_m: float, y_m: float, z_m: float
    ) -> None:
        self._inbox.append(
            _LocalPosition(time_since_boot_ms=time_since_boot_ms, x_m=x_m, y_m=y_m, z_m=z_m)
        )

    def recv_match(
        self, blocking: bool = False, types: list[str] | None = None, timeout: float | None = None
    ) -> Optional[Any]:
        if not self._inbox:
            return None
        if types is None:
            return self._inbox.pop(0)
        # find first matching type
        for idx, msg in enumerate(self._inbox):
            mtype = getattr(msg, "__class__", type("", (), {})).__name__
            if isinstance(msg, dict):
                mtype = msg.get("type", "")
            # Map dataclass names to MAVLink-like type strings
            if mtype == "_Attitude":
                mtype = "ATTITUDE"
            elif mtype == "_LocalPosition":
                mtype = "LOCAL_POSITION_NED"
            if mtype in types:
                return self._inbox.pop(idx)
        return None
