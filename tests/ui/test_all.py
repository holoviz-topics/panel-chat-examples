"""Test the UI of all apps via Playwright"""
import os
import time
from pathlib import Path

import pytest
from panel.io.server import serve
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

SCREENSHOT = bool(os.environ.get("SCREENSHOT", ""))
SCREENSHOTS_PATH = Path(__file__).parent / "screenshots"
SCREENSHOTS_PATH.mkdir(parents=True, exist_ok=True)

EXPECTED_LOG_MESSAGES = [
    "[bokeh] setting log level to: 'info'",
    "[bokeh] Websocket connection 0 is now open",
    "[bokeh] document idle at",
    "Bokeh items were rendered successfully",
]


def _bokeh_messages_have_been_logged(msgs):
    return (
        len(
            [
                msg
                for msg in msgs
                if not any(
                    msg.text.startswith(known) for known in EXPECTED_LOG_MESSAGES
                )
            ]
        )
        == 0
    )


def _page_not_empty(page):
    div_element = page.query_selector("div")
    return div_element is not None


def _expect_no_traceback(page):
    expect(page.get_by_text("Traceback (most recent call last):")).to_have_count(0)


def _take_screenshot(app_path, page):
    if SCREENSHOT:
        page.screenshot(
            path=SCREENSHOTS_PATH / Path(app_path).name.replace(".py", ".png"),
            full_page=True,
        )


def test_app(app_path, page, port):
    """Test the UI of an app via Playwright"""
    serve(app_path, port=port, threaded=True, show=False)

    time.sleep(0.2)

    msgs = []
    page.on("console", msgs.append)

    page.goto(f"http://localhost:{port}", timeout=40_000)
    _take_screenshot(app_path, page)

    assert _bokeh_messages_have_been_logged(msgs)
    _expect_no_traceback(page)
    assert _page_not_empty(page), "The page is empty, No <div> element was not found"
