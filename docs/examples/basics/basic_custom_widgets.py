"""
Demonstrates how to use the `ChatInterface` and custom widgets,
like `TextAreaInput` and `FileInput`, to create a chatbot that counts
the number of lines in a message or file.
"""

import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    lines = contents.strip().count("\n")
    message = f"This snippet has {lines + 1} lines."
    return message


text_area_input = pn.widgets.TextAreaInput(auto_grow=True, placeholder="Click Send to count lines.")
file_input = pn.widgets.FileInput()
chat_interface = pn.chat.ChatInterface(callback=callback, widgets=[text_area_input, file_input])
chat_interface.send(
    "Enter a message in the TextAreaInput below to count how many lines there is, "
    "or upload a file to count the number of lines in the file.",
    user="System",
    respond=False,
)
chat_interface.servable()
