"""
Demonstrates how to use the `ChatInterface` to create images using
OpenAI's [DALL-E API](https://platform.openai.com/docs/guides/images/image-generation).
"""

import panel as pn
from openai import OpenAI

pn.extension()


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    response = client.images.generate(prompt=contents, n=1, size="256x256")
    image_url = response.data[0].url
    return pn.pane.Image(image_url, width=256, height=256)


client = OpenAI()
chat_interface = pn.chat.ChatInterface(
    callback=callback, callback_user="DALL-E", placeholder_text="Generating..."
)
chat_interface.send(
    "Create an image by providing a prompt!", user="System", respond=False
)
chat_interface.servable()
