"""
Demonstrates how to use the `ChatInterface` widget with authentication for
OpenAI's API.
"""

import os

import panel as pn
from openai import AsyncOpenAI

SYSTEM_KWARGS = dict(
    user="System",
    respond=False,
)

pn.extension()


def add_key_to_env(key):
    if not key.startswith("sk-"):
        chat_interface.send("Please enter a valid OpenAI key!", **SYSTEM_KWARGS)
        return

    chat_interface.send(
        "Your OpenAI key has been set. Feel free to minimize the sidebar.",
        **SYSTEM_KWARGS,
    )
    chat_interface.disabled = False


key_input = pn.widgets.PasswordInput(placeholder="sk-...", name="OpenAI Key")
pn.bind(add_key_to_env, key=key_input, watch=True)


async def callback(
    contents: str,
    user: str,
    instance: pn.chat.ChatInterface,
):
    if "OPENAI_API_KEY" not in os.environ:
        yield "Please first set your OpenAI key in the sidebar!"
        return

    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
        api_key=key_input.value,
    )
    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield message


aclient = AsyncOpenAI()
chat_interface = pn.chat.ChatInterface(callback=callback, disabled=True)
chat_interface.send(
    "First enter your OpenAI key in the sidebar, then send a message!", **SYSTEM_KWARGS
)

pn.template.MaterialTemplate(
    title="OpenAI ChatInterface with authentication",
    sidebar=[key_input],
    main=[chat_interface],
).servable()
