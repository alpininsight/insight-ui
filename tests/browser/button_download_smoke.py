# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Real native download acceptance; run explicitly with Playwright installed."""

import os
from pathlib import Path
from socketserver import ThreadingMixIn
from tempfile import TemporaryDirectory
from threading import Thread
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

import django
from django.template import Context, Template
from playwright.sync_api import sync_playwright

PAYLOAD = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><path d="M0 0h1v1H0z"/></svg>'


class QuietHandler(WSGIRequestHandler):
    """Keep the small local smoke silent unless an assertion fails."""

    def log_message(self, *_args: object) -> None:
        """Suppress routine HTTP log entries."""


class ThreadedServer(ThreadingMixIn, WSGIServer):
    """Do not let browser preconnects block a file request."""

    daemon_threads = True


def main() -> None:
    """Download three public-tag variants using Enter with page JS disabled."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()
    from insight_ui.configs import ButtonConfig  # noqa: PLC0415

    buttons = [
        ButtonConfig(label="Default filename", request_url="/fixture.svg", download=True, tag_id="default"),
        ButtonConfig(label="Empty filename", request_url="/fixture.svg", download="", tag_id="empty"),
        ButtonConfig(label="Named filename", request_url="/fixture.svg", download="report.svg", tag_id="named"),
    ]
    html = (
        Template(
            '<!doctype html><html><head><title>Download smoke</title></head><body><main hx-boost="true">'
            "{% load insight_tags %}{% for item in buttons %}{% button config=item %}{% endfor %}"
            "</main></body></html>"
        )
        .render(Context({"buttons": buttons}))
        .encode()
    )

    def app(environ, start_response):  # noqa: ANN001, ANN202
        """Serve only the rendered fixture and a deterministic SVG payload."""
        file_request = environ.get("PATH_INFO") == "/fixture.svg"
        content = PAYLOAD if file_request else html
        mime = "image/svg+xml" if file_request else "text/html; charset=utf-8"
        start_response("200 OK", [("Content-Type", mime), ("Content-Length", str(len(content)))])
        return [content]

    with make_server("127.0.0.1", 0, app, server_class=ThreadedServer, handler_class=QuietHandler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright, TemporaryDirectory(prefix="ui-download-") as directory:
                browser = playwright.chromium.launch()
                with browser.new_context(java_script_enabled=False, accept_downloads=True) as context:
                    page = context.new_page()
                    page.goto(f"http://127.0.0.1:{server.server_port}/")
                    for target, filename in (
                        ("default", "fixture.svg"),
                        ("empty", "fixture.svg"),
                        ("named", "report.svg"),
                    ):
                        link = page.locator(f"#{target}")
                        link.focus()
                        with page.expect_download() as info:
                            page.keyboard.press("Enter")
                        download = info.value
                        assert download.failure() is None
                        assert download.suggested_filename == filename
                        destination = Path(directory) / f"{target}.svg"
                        download.save_as(destination)
                        assert destination.read_bytes() == PAYLOAD
                browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=5)
    print("Native download: 3/3 real no-JavaScript keyboard downloads passed.")  # noqa: T201


if __name__ == "__main__":
    main()
