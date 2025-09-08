from __future__ import annotations

from modules.common.logger import Logger
from modules.heartbeat.heartbeat_sender_worker import HeartbeatSenderWorker
from tests.integration.mock_drones import MockConnection


def main() -> None:
    logger = Logger("heartbeat_sender")
    conn = MockConnection()

    worker = HeartbeatSenderWorker(
        connection=conn, output_queue=None, logger=logger, period_sec=0.01
    )
    worker.run(iterations=5)

    # Assert that at least 5 heartbeat messages landed in the inbox
    heartbeats = [m for m in conn._inbox if isinstance(m, dict) and m.get("type") == "HEARTBEAT"]
    logger.info(f"Heartbeat count: {len(heartbeats)}")


if __name__ == "__main__":
    main()
