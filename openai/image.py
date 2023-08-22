"""
Demonstrates how to use the ChatInterface widget to create an image using
OpenAI's DALL-E API.
"""

import openai
import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.Image.create(prompt=contents, n=1, size="256x256")
    image_url = response["data"][0]["url"]
    return pn.pane.Image(image_url, width=256, height=256)


chat_interface = pn.widgets.ChatInterface(
    callback=callback, callback_user="DALL-E", placeholder_text="Generating..."
)
chat_interface.send(
    "Create an image by providing a prompt!", user="System", respond=False
)
chat_interface.servable()
