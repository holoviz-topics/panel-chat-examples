"""
Demonstrates how to use LlamaIndex to wrap OpenAI's GPT-3.5 API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `OPENAI_API_KEY` environment variable.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response
"""

import panel as pn
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

pn.extension()


def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        # use api_key_input.value if set, otherwise use OPENAI_API_KEY
        llm.api_key = api_key_input.value

    # memory is a list of messages
    messages = [ChatMessage(**message) for message in instance.serialize()]

    response = await llm.astream_chat(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    async for chunk in response:
        message = chunk.message.content
        yield str(message)


llm = OpenAI(model="gpt-3.5-turbo-0613")

multiply_tool = FunctionTool.from_defaults(fn=multiply)
agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)

api_key_input = pn.widgets.PasswordInput(
    placeholder="sk-... uses $OPENAI_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="GPT-3.5",
    help_text="Send a message to get a reply from GPT 3.5 Turbo!",
)
template = pn.template.FastListTemplate(
    title="LlamaIndex OpenAI GPT-3.5",
    header_background="#83CBF2",
    main=[chat_interface],
    header=[api_key_input],
)
template.servable()
