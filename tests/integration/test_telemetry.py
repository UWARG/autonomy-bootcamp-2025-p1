from __future__ import annotations

from modules.common.logger import Logger
from modules.telemetry.telemetry_worker import TelemetryWorker
from tests.integration.mock_drones import MockConnection
from utilities.queue_wrapper import QueueProxyWrapper


def main() -> None:
    logger = Logger("telemetry")
    conn = MockConnection()
    out_q: QueueProxyWrapper = QueueProxyWrapper()

    conn.feed_attitude(time_since_boot_ms=100, yaw_deg=10.0)
    conn.feed_local_position(time_since_boot_ms=120, x_m=1.0, y_m=2.0, z_m=3.0)

    worker = TelemetryWorker(connection=conn, output_queue=out_q, logger=logger)
    worker.run(iterations=1)

    data = out_q.get()
    if data is not None:
        logger.info(
            f"TelemetryData: t={data.time_since_boot_ms}, pos=({data.position_x_m}, {data.position_y_m}, {data.position_z_m}), yaw={data.yaw_deg}"
        )


if __name__ == "__main__":
    main()
