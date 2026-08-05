"""
ASGI config for insight-ui project.

It exposes the ASGI callable as a module-level variable named ``application``.

This configuration supports both HTTP and WebSocket connections:
- HTTP requests are handled by Django
- WebSocket requests to /ws/ticker/ are handled by the demo stock ticker

For WebSocket support, run with an ASGI server:
    uvicorn core.asgi:application --reload --port 10800

The standard Django runserver (WSGI) will work for HTTP but not WebSockets.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from logging_config import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
setup_logging()

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()


async def application(scope: dict, receive: callable, send: callable) -> None:
    """ASGI application that routes WebSocket and HTTP requests.

    Args:
        scope: ASGI connection scope.
        receive: ASGI receive callable.
        send: ASGI send callable.

    """
    if scope["type"] == "websocket" and scope["path"] == "/ws/ticker/":
        from core.websocket import stock_ticker_handler  # noqa: PLC0415

        await stock_ticker_handler(scope, receive, send)
    else:
        await django_asgi_app(scope, receive, send)
