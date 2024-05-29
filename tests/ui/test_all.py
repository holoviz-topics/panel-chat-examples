"""Test the UI of all apps via Playwright"""

import os
import sys
import time
from pathlib import Path

import pytest
from panel.io.server import serve
from playwright.sync_api import expect

from .inputs import ACTION, TIMEOUT, ZOOM

pytestmark = pytest.mark.ui

EXPECTED_LOG_MESSAGES = [
    "[bokeh] setting log level to: 'info'",
    "[bokeh] Websocket connection 0 is now open",
    "[bokeh] document idle at",
    "Bokeh items were rendered successfully",
]
RECORD_VIDEO_SIZE = {"width": 1200, "height": 675}
VIEWPORT = {"width": 1200, "height": 675}


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


@pytest.fixture
def server(app_path, port):
    """Returns a panel server running the app"""
    bokeh_allow_ws_origin = os.environ.get("BOKEH_ALLOW_WS_ORIGIN")
    os.environ["BOKEH_ALLOW_WS_ORIGIN"] = "localhost"
    server = serve(app_path, port=port, threaded=False, show=False)
    time.sleep(0.2)
    yield server
    server.stop()
    if bokeh_allow_ws_origin:
        os.environ["BOKEH_ALLOW_WS_ORIGIN"] = bokeh_allow_ws_origin


@pytest.mark.browser_context_args(
    viewport=VIEWPORT, record_video_size=RECORD_VIDEO_SIZE
)
def test_app(server, app_path, port, page):
    """Test the UI of an app via Playwright"""
    msgs = []
    name = Path(app_path).name
    # Without the lambda below an AttributeError will be raised
    page.on("console", lambda: msgs.append)

    page.goto(f"http://localhost:{port}", timeout=40_000)

    print(f"\n\nRunning {app_path} on http://localhost:{port}\n\n")
    # zoom and run should be defined for all examples
    # even if we don't run the video
    run = ACTION.get(name, ACTION["default_chat"])
    zoom = ZOOM.get(name, 1)

    # We cannot run these tests in pipelines etc. as they require models downloaded,
    # api keys etc.
    if "on" in sys.argv and ("--screenshot" in sys.argv or "--video" in sys.argv):
        page.locator("body").evaluate(f"(sel)=>{{sel.style.zoom = {zoom}}}")
        run(page)

    page.wait_for_timeout(TIMEOUT)
    assert _bokeh_messages_have_been_logged(msgs)
    _expect_no_traceback(page)
    assert _page_not_empty(page), "The page is empty, No <div> element was not found"
