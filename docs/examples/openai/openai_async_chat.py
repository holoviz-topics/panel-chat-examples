"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's with async/await.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
