"""Test the UI of all apps via Playwright"""
import os
import time
from pathlib import Path

import pytest
from panel.io.server import serve
from playwright.sync_api import expect

from .user import ACTION, ZOOM

pytestmark = pytest.mark.ui

EXPECTED_LOG_MESSAGES = [
    "[bokeh] setting log level to: 'info'",
    "[bokeh] Websocket connection 0 is now open",
    "[bokeh] document idle at",
    "Bokeh items were rendered successfully",
]
VIEWPORT={ 'width': 1600, 'height': 900 } # Optimal for Twitter

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
    """Returns a panel server runnning the app"""
    bokeh_allow_ws_origin = os.environ.get("BOKEH_ALLOW_WS_ORIGIN")
    os.environ["BOKEH_ALLOW_WS_ORIGIN"] = "localhost"
    server = serve(app_path, port=port, threaded=True, show=False)
    time.sleep(0.2)
    yield server
    server.stop()
    if bokeh_allow_ws_origin:
        os.environ["BOKEH_ALLOW_WS_ORIGIN"] = bokeh_allow_ws_origin



@pytest.mark.browser_context_args(viewport=VIEWPORT)
def test_app(server, app_path, port, page):
    """Test the UI of an app via Playwright"""
    msgs = []
    name = Path(app_path).name
    # Without the lambda below an AttributeError will be raised
    page.on("console", lambda: msgs.append)

    page.goto(f"http://localhost:{port}", timeout=40_000)
    
    zoom = ZOOM.get(name, None)
    if zoom:
        page.locator('body').evaluate(f"(sel)=>{{sel.style.zoom = {zoom}}}")
    
    run = ACTION.get(name, None)
    if run:
        run(page)

    assert _bokeh_messages_have_been_logged(msgs)
    _expect_no_traceback(page)
    assert _page_not_empty(page), "The page is empty, No <div> element was not found"
