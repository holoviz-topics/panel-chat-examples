"""
Demonstrates how to delay the display of the placeholder.

Highlights:

- The `placeholder_threshold` parameter is used to delay the display of the placeholder.
    If the response time is less than the threshold, the placeholder will not be displayed.
- The `placeholder_text` parameter is used to customize the placeholder text.
"""

from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    try:
        seconds = float(contents)
        if 0 < seconds < 10:
            await sleep(seconds)
            return f"Slept {contents} seconds!"
        else:
            return "Please enter a number between 1 and 9!"
    except ValueError:
        return "Please enter a number!"


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    placeholder_threshold=2,
    placeholder_text="Waiting for reply...",
)
chat_interface.send(
    "Send a number to make the system sleep between 1 and 9 seconds!",
    user="System",
    respond=False,
)
chat_interface.servable()
