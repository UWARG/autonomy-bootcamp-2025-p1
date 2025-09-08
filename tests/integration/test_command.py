from __future__ import annotations

from modules.common.logger import Logger
from modules.command.command_worker import CommandWorker
from modules.command.command import Target
from tests.integration.mock_drones import MockConnection
from utilities.queue_wrapper import QueueProxyWrapper


def main() -> None:
    logger = Logger("command")
    conn = MockConnection()

    telemetry_q: QueueProxyWrapper = QueueProxyWrapper()
    output_q: QueueProxyWrapper = QueueProxyWrapper()

    target = Target(x_m=0.0, y_m=0.0, z_m=5.0)
    worker = CommandWorker(
        connection=conn,
        telemetry_queue=telemetry_q,
        output_queue=output_q,
        target=target,
        logger=logger,
    )

    # Initial telemetry far from target
    from modules.telemetry.telemetry import TelemetryData

    telemetry_q.put(
        TelemetryData(
            time_since_boot_ms=0, position_x_m=10.0, position_y_m=0.0, position_z_m=2.0, yaw_deg=0.0
        )
    )
    worker.run(iterations=1)

    messages = []
    while not output_q.empty():
        messages.append(output_q.get())
    logger.info(f"Command outputs: {messages}")


if __name__ == "__main__":
    main()
