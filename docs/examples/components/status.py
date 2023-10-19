"""The `Status` *indicator* can report progress in steps and with
detailed context.

If you need a `Status` widget you can copy the code from
[here](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/components/chat_input/components/status.py).
"""
import time

import panel as pn

from panel_chat_examples.components import Status

status = Status("Downloading data...", sizing_mode="stretch_width")


def run(_):
    with status.report() as progress:
        status.collapsed = False
        progress("Searching for data...")
        time.sleep(1.5)
        progress("Downloading data...")
        time.sleep(1.5)
        progress("Validating data...")
        time.sleep(1.5)
        status.collapsed = True


run_button = pn.widgets.Button(
    name="Run", on_click=run, button_type="primary", button_style="outline"
)

pn.Column(
    status,
    run_button,
).servable()
