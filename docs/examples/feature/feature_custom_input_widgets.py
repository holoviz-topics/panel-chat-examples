"""
Demonstrates how to use the `ChatInterface` and custom widgets,
like `ChatAreaInput` and `FileInput`, to create a chatbot that counts
the number of lines in a message or file.

Highlights:

- The `ChatAreaInput` and `FileInput` widgets are used to create a custom
    chatbot that counts the number of lines in a message or file.
- The `callback` function is used to count the number of lines in the message
    or file and return the result to the User.
"""

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    lines = contents.strip().count("\n")
    message = f"This snippet has {lines + 1} lines."
    return message


chat_input = pn.chat.ChatAreaInput(placeholder="Send a message")
file_input = pn.widgets.FileInput(accept=".py")
chat_interface = pn.chat.ChatInterface(
    callback=callback, widgets=[chat_input, file_input]
)
chat_interface.send(
    "Enter a message in the ChatAreaInput below to count how many lines there is, "
    "or upload a Python file to count the number of lines in the file.",
    user="System",
    respond=False,
)
chat_interface.servable()
