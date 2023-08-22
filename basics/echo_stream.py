"""
Demonstrates how to use the ChatInterface widget to echo back a message
in a streaming fashion.
"""


from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: "
    for char in contents:
        await sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="System")
chat_interface.send("Send a message to receive an echo!", user="System", respond=False)
chat_interface.servable()
