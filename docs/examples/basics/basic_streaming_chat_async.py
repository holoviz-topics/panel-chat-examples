"""
Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.
"""


from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(1)
    message = ""
    for char in "Echoing User: " + contents:
        await sleep(0.05)
        message += char
        yield message


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
