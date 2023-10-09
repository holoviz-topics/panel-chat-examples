"""
Demonstrates how to update the response of a ChatInterface widget.
"""

from asyncio import sleep
from random import choice

import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    yield "Let me flip the coin for you..."
    await sleep(1)

    characters = "/|\\_"
    index = 0
    for _ in range(0, 28):
        index = (index + 1) % len(characters)
        yield "\r" + characters[index]
        await sleep(0.005)

    result = choice(["heads", "tails"])
    if result in contents.lower():
        yield f"Woohoo, {result}! You win!"
    else:
        yield f"Aw, got {result}. Try again!"


chat_interface = pn.widgets.ChatInterface(
    widgets=[pn.widgets.RadioButtonGroup(options=["Heads!", "Tails!"], button_type="primary", button_style="outline")],
    callback=callback,
    callback_user="Game Master",
)
chat_interface.send(
    "Select heads or tails, then click send!", user="System", respond=False
)
chat_interface.servable()
