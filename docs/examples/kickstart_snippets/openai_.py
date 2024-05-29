"""
Demonstrates how to use OpenAI's GPT-3.5 API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `OPENAI_API_KEY` environment variable.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response
"""

import panel as pn
from openai import AsyncOpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        # use api_key_input.value if set, otherwise use OPENAI_API_KEY
        aclient.api_key = api_key_input.value

    # memory is a list of messages
    messages = instance.serialize()

    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield message


aclient = AsyncOpenAI()
api_key_input = pn.widgets.PasswordInput(
    placeholder="sk-... uses $OPENAI_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="GPT-3.5",
    help_text="Send a message to get a reply from GPT-3.5 Turbo!",
)
template = pn.template.FastListTemplate(
    title="OpenAI GPT-3.5",
    header_background="#212121",
    main=[chat_interface],
    header=[api_key_input],
)
template.servable()
