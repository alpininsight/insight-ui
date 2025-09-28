# websocket_main.py

import asyncio
import json
import logging
import os
import shutil
import traceback
import uuid
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler

import psutil
import websockets
from websockets.server import WebSocketServerProtocol

# --- Konfiguration ---
DEBUG = os.getenv("DEBUG", "true").lower() in ("1", "true", "yes")
HOST, PORT = "127.0.0.1", 8765

# --- Logging Setup (wie zuvor) ---
level = logging.DEBUG if DEBUG else logging.INFO
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s] %(message)s", datefmt="%H:%M:%S")

root = logging.getLogger()
root.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
ch.setFormatter(formatter)
root.addHandler(ch)

fh = RotatingFileHandler("app.log", maxBytes=10 * 1024 * 1024, backupCount=3)
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
root.addHandler(fh)

logger = logging.getLogger(__name__)


# --- Helper Funktionen ---
def safe_json(data) -> str:  # noqa: ANN001
    """Dump data to json string."""

    def default(o) -> str:  # noqa: ANN001
        if isinstance(o, datetime | datetime.date):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        return str(o)

    return json.dumps(data, default=default)


async def system_info() -> dict:
    """Retrieve system information, like disk and memory usage."""
    now = datetime.now(UTC)
    disk = shutil.disk_usage("/")
    mem = psutil.virtual_memory()
    return {
        "timestamp": now,
        "disk": {
            "total_gb": round(disk.total / 2**30, 2),
            "used_gb": round(disk.used / 2**30, 2),
            "free_gb": round(disk.free / 2**30, 2),
        },
        "memory": {
            "total_gb": round(mem.total / 2**30, 2),
            "available_gb": round(mem.available / 2**30, 2),
            "percent_used": mem.percent,
        },
    }


# --- WebSocket-Handler ---
async def handler(ws: WebSocketServerProtocol) -> None:
    """Handle WebSocket to send data to connected client."""
    conn_id = str(uuid.uuid4())
    remote = ws.remote_address or ("unknown", "?")
    ip, port = remote[0], remote[1] if len(remote) > 1 else "?"
    ua = ws.request.headers.get("User-Agent", "Unknown") if ws.request else "Unknown"

    logger.info("[%s] Connected: %s:%s (%s)", conn_id, ip, port, ua)

    try:
        while True:
            info = await system_info()
            timestamp = datetime.now(tz=UTC).strftime("%H:%M:%S")

            # HTML-Fragment für HTMX WebSocket Extension erstellen
            html_content = f"""
            <div id="demo-websocket-output" hx-swap-oob="innerHTML">
                <div class="mb-2 p-2 border-l-4 border-blue-500 bg-white dark:bg-gray-600 rounded">
                    <div class="text-xs text-insight-text-secondary
                        dark:text-insight-text-secondary-dark">{timestamp}</div>
                    <div class="font-semibold text-blue-600 dark:text-blue-400">Connection: {conn_id[:8]}</div>
                    <div class="text-sm space-y-1">
                        <div>💾 Disk: {info["disk"]["used_gb"]}GB / {info["disk"]["total_gb"]}GB</div>
                        <div>🧠 Memory: {info["memory"]["percent_used"]}% used</div>
                        <div>🌐 Client: {ip}</div>
                    </div>
                </div>
            </div>
            """

            await ws.send(html_content.strip())
            await asyncio.sleep(5)

    except websockets.ConnectionClosed as e:
        logger.info("[%s] Disconnected (code=%s, reason=%s)", conn_id, e.code, e.reason)
    except Exception:
        logger.exception("[%s] Unexpected error in handler", conn_id)
    finally:
        logger.info("[%s] Session closed.", conn_id)


# --- Server-Start ---
async def main() -> None:
    """Start WebSocket server."""
    async with websockets.serve(handler, HOST, PORT, ping_interval=20, ping_timeout=20):
        logger.info("WebSocket server listening on ws://%s:$%s", HOST, PORT)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped via CTRL+C")
    except Exception:  # noqa: BLE001
        logger.critical("Server crashed unexpectedly", exc_info=DEBUG)
        traceback.print_exc()
