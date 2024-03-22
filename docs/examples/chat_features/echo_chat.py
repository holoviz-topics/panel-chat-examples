"""
Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

Highlights:

- The `ChatInterface` and a `callback` function are used to create a
    chatbot that echoes back the message entered by the User.
- The `help_text` parameter is used to provide instructions to the User.
"""

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    help_text="Enter a message in the TextInput below and receive an echo!",
)
chat_interface.servable()
