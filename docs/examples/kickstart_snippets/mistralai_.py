"""
Demonstrates how to use MistralAI's Small API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `MISTRAL_API_KEY` environment variable.
- Runs `pn.bind` to update the `MistralAsyncClient` when the `api_key` changes and pn.state.cache to store the client.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response.
"""

import panel as pn
from mistralai import Mistral, UserMessage
import os

pn.extension()

def update_api_key(api_key):
    # Use the provided api_key or default to the environment variable
    pn.state.cache["aclient"] = (
        Mistral(api_key=api_key) if api_key else Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))
    )

async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # memory is a list of serialized messages
    messages = instance.serialize()

    # Convert serialized messages into UserMessage format
    formatted_messages = [UserMessage(content=msg["content"]) for msg in messages]

    response = await pn.state.cache["aclient"].chat.stream_async(
        model="mistral-small",
        messages=formatted_messages,
    )

    message = ""
    async for chunk in response:
        part = chunk.data.choices[0].delta.content
        if part is not None:
            message += part
            yield message

# Input widget for the API key
api_key_input = pn.widgets.PasswordInput(
    placeholder="Uses $MISTRAL_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)

# Bind the API key input to the update function
pn.bind(update_api_key, api_key_input, watch=True)
api_key_input.param.trigger("value")

# Define the Chat Interface with callback
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="MistralAI",
    help_text="Send a message to get a reply from MistralAI!",
    callback_exception="verbose",
)

# Template with the chat interface
template = pn.template.FastListTemplate(
    title="MistralAI Small",
    header_background="#FF7000",
    main=[chat_interface],
    header=[api_key_input],
)

# Serve the template
template.servable()
