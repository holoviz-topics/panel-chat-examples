"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's API.
"""

import panel as pn
from openai import OpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield message


client = OpenAI()
chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
