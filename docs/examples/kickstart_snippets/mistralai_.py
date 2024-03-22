"""
Demonstrates how to use MistralAI's Small API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `MISTRAL_API_KEY` environment variable.
- Runs `pn.bind` to update the `MistralAsyncClient` when the `api_key` changes and pn.state.cache to store the client.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response.
"""

import panel as pn
from mistralai.async_client import MistralAsyncClient

pn.extension()


def update_api_key(api_key):
    # use api_key_input.value if set, otherwise use MISTRAL_API_KEY
    pn.state.cache["aclient"] = (
        MistralAsyncClient(api_key=api_key) if api_key else MistralAsyncClient()
    )


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # memory is a list of messages
    messages = instance.serialize()

    response = pn.state.cache["aclient"].chat_stream(
        model="mistral-small",
        messages=messages,
    )

    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield message


api_key_input = pn.widgets.PasswordInput(
    placeholder="Uses $MISTRAL_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
pn.bind(update_api_key, api_key_input, watch=True)
api_key_input.param.trigger("value")

chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="MistralAI",
    help_text="Send a message to get a reply from MistralAI!",
    callback_exception="verbose",
)
template = pn.template.FastListTemplate(
    title="MistralAI Small",
    header_background="#FF7000",
    main=[chat_interface],
    header=[api_key_input],
)
template.servable()
