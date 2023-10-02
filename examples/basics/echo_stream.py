"""
Demonstrates how to use the ChatInterface widget to echo back a message
in a streaming fashion.
"""


from time import sleep

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    sleep(1)
    message = ""
    for char in contents:
        sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="System")
chat_interface.send(
    "Send a message via the TextInput below to receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
