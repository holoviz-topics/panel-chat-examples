"""
Demonstrates how to use the `ChatInterface` widget to echo back a message using the `.send` method.
"""

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="System")
chat_interface.send("Send a message to receive an echo!", user="System", respond=False)
chat_interface.servable()
