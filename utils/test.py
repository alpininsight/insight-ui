"""Simple WebSocket client for manual testing of the demo server."""

from __future__ import annotations

import asyncio
import json
import logging
import signal
from typing import Any

import websockets
from websockets.client import WebSocketClientProtocol

LOGGER = logging.getLogger(__name__)
if not LOGGER.handlers:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

WEBSOCKET_URL = "ws://localhost:8765"
_SHUTDOWN_EVENT = asyncio.Event()


def _shutdown_handler(signum: int, frame: Any) -> None:  # noqa: D401, ANN401
    """Set the shutdown flag when the process receives a termination signal."""
    LOGGER.info("Client wird beendet (Signal %s empfangen)", signum)
    _SHUTDOWN_EVENT.set()


signal.signal(signal.SIGINT, _shutdown_handler)
signal.signal(signal.SIGTERM, _shutdown_handler)


async def _log_message(message: str) -> None:
    """Parse a WebSocket message and log a prettified representation."""
    try:
        data = json.loads(message)
        pretty_payload = json.dumps(data.get("content"), indent=2)
        LOGGER.info("[%s] Daten empfangen:\n%s", data.get("connection_id", "?"), pretty_payload)
    except json.JSONDecodeError:
        LOGGER.warning("Ungültige Nachricht:\n%s", message)


async def run_client() -> None:
    """Connect to the demo WebSocket and stream messages until stopped."""
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await _consume_messages(websocket)
    except Exception:  # noqa: BLE001
        LOGGER.exception("Verbindungsfehler beim Aufbau der WebSocket-Verbindung")


async def _consume_messages(websocket: WebSocketClientProtocol) -> None:
    """Receive messages until the shutdown event is triggered."""
    LOGGER.info("Verbunden mit %s", WEBSOCKET_URL)
    while not _SHUTDOWN_EVENT.is_set():
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=10)
            await _log_message(message)
        except TimeoutError:
            LOGGER.debug("Timeout – keine Nachricht empfangen")


if __name__ == "__main__":
    asyncio.run(run_client())
