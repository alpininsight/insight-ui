"""WebSocket handlers for insight-ui demo.

This module provides a demo WebSocket endpoint that simulates a stock ticker.
It requires an ASGI server (uvicorn, daphne) to function - the standard
Django runserver (WSGI) will not support WebSocket connections.

Usage:
    uvicorn core.asgi:application --reload --port 10800

"""

import asyncio
import random
from datetime import UTC, datetime

# Simulated stock data with realistic price ranges
STOCKS = {
    "AAPL": {"name": "Apple", "base": 187.50, "volatility": 0.02},
    "MSFT": {"name": "Microsoft", "base": 378.00, "volatility": 0.015},
    "GOOGL": {"name": "Alphabet", "base": 141.00, "volatility": 0.018},
    "NVDA": {"name": "NVIDIA", "base": 892.00, "volatility": 0.03},
}


def generate_prices() -> dict[str, dict]:
    """Generate simulated stock prices with random movements."""
    result = {}
    for symbol, config in STOCKS.items():
        # Random price change within volatility range
        change_pct = random.uniform(  # noqa: S311  # nosec B311
            -config["volatility"],
            config["volatility"],
        )
        price = config["base"] * (1 + change_pct)
        result[symbol] = {
            "price": round(price, 2),
            "change": round(change_pct * 100, 2),
        }
    return result


def build_ticker_html(prices: dict[str, dict]) -> str:
    """Build HTML fragment for HTMX swap."""
    timestamp = datetime.now(tz=UTC).strftime("%H:%M:%S UTC")

    rows = []
    for symbol, data in prices.items():
        price = data["price"]
        change = data["change"]

        if change >= 0:
            arrow = "▲"
            color_class = "text-insight-success dark:text-insight-success-dark"
            sign = "+"
        else:
            arrow = "▼"
            color_class = "text-insight-danger dark:text-insight-danger-dark"
            sign = ""

        rows.append(f"""
            <div class="flex justify-between items-center py-1">
                <span class="font-mono font-semibold w-16">{symbol}</span>
                <span class="font-mono">${price:,.2f}</span>
                <span class="font-mono {color_class} w-24 text-right">
                    {arrow} {sign}{change:.2f}%
                </span>
            </div>
        """)

    return f"""
    <div id="demo-websocket-output" hx-swap-oob="innerHTML">
        <div class="space-y-1">
            {"".join(rows)}
            <div class="text-xs text-caption text-right pt-2 border-t border-insight-border-surface mt-2">
                {timestamp}
            </div>
        </div>
    </div>
    """


async def stock_ticker_handler(scope: dict, receive: callable, send: callable) -> None:
    """WebSocket handler that streams simulated stock prices.

    Args:
        scope: ASGI connection scope.
        receive: ASGI receive callable.
        send: ASGI send callable.

    """
    if scope["type"] != "websocket":
        return

    # Wait for connection
    while True:
        message = await receive()
        if message["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})
            break
        if message["type"] == "websocket.disconnect":
            return

    # Stream stock prices
    try:
        while True:
            prices = generate_prices()
            html = build_ticker_html(prices)

            await send({"type": "websocket.send", "text": html.strip()})

            # Check for disconnect while waiting
            try:
                message = await asyncio.wait_for(receive(), timeout=2.0)
                if message["type"] == "websocket.disconnect":
                    break
            except TimeoutError:
                # No message received, continue streaming
                pass
    except Exception:  # noqa: BLE001, S110  # nosec B110
        # Connection closed or error - expected when client disconnects
        pass
