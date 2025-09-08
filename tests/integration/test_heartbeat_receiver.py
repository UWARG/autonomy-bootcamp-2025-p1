from __future__ import annotations

from modules.common.logger import Logger
from modules.heartbeat.heartbeat_receiver_worker import HeartbeatReceiverWorker
from tests.integration.mock_drones import MockConnection
from utilities.queue_wrapper import QueueProxyWrapper


def main() -> None:
    logger = Logger("heartbeat_receiver")
    conn = MockConnection()
    out_q: QueueProxyWrapper[str] = QueueProxyWrapper()

    # Simulate receiving some heartbeats, then misses
    conn.mav.heartbeat_send()
    conn.mav.heartbeat_send()
    # 5 misses by not sending more

    worker = HeartbeatReceiverWorker(connection=conn, output_queue=out_q, logger=logger)
    worker.run(iterations=8)

    states = []
    while not out_q.empty():
        states.append(out_q.get())

    logger.info(f"States: {states}")


if __name__ == "__main__":
    main()
