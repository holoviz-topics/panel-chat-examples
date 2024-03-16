"""
Demonstrates how to precisely control the callback response.

Highlights:

- Use a placeholder text to display a message while waiting for the response.
- Use a placeholder threshold to control when the placeholder text is displayed.
- Use send instead of stream/yield/return to keep the placeholder text while still sending a message, ensuring respond=False to avoid a recursive loop.
- Use yield to continuously update the response message.
- Use pn.chat.ChatMessage or dict to send a message with a custom user and avatar.
"""

from asyncio import sleep
from random import choice

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(0.5)
    # use send instead of stream/yield/return to keep the placeholder text
    # while still sending a message; ensure respond=False to avoid a recursive loop
    instance.send(
        "Let me flip the coin for you...", user="Game Master", avatar="🎲", respond=False
    )
    await sleep(1)

    characters = "/|\\_"
    index = 0
    for _ in range(0, 28):
        index = (index + 1) % len(characters)
        # use yield to continuously update the response message
        # use pn.chat.ChatMessage to send a message with a custom user and avatar
        yield pn.chat.ChatMessage("\r" + characters[index], user="Coin", avatar="🪙")
        await sleep(0.005)

    result = choice(["heads", "tails"])
    if result in contents.lower():
        # equivalently, use a dict instead of a pn.chat.ChatMessage
        yield {"object": f"Woohoo, {result}! You win!", "user": "Coin", "avatar": "🎲"}
    else:
        yield {"object": f"Aw, got {result}. Try again!", "user": "Coin", "avatar": "🎲"}


chat_interface = pn.chat.ChatInterface(
    widgets=[
        pn.widgets.RadioButtonGroup(
            options=["Heads!", "Tails!"], button_type="primary", button_style="outline"
        )
    ],
    callback=callback,
    help_text="Select heads or tails, then click send!",
    placeholder_text="Waiting for the result...",
    placeholder_threshold=0.1,
)
chat_interface.servable()
