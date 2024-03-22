# Kickstart Snippets
Quickly start using Panel's chat components with popular LLM packages by copying and pasting one of these snippets.

## Openai

Demonstrates how to use OpenAI's GPT-3.5 API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `OPENAI_API_KEY` environment variable.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response

<video controls poster="../assets/thumbnails/openai.png" >
    <source src="../assets/videos/openai.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/kickstart_snippets/openai.py' target='_blank'>openai.py</a></summary>

```python
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
    callback_user="ChatGPT",
    help_text="Send a message to get a reply from ChatGPT!",
)
template = pn.template.FastListTemplate(
    title="OpenAI GPT-3.5",
    header_background="#212121",
    main=[chat_interface],
    header=[api_key_input],
)
template.servable()
```
</details>


## Mistralai

Demonstrates how to use MistralAI's Small API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `MISTRAL_API_KEY` environment variable.
- Runs `pn.bind` to update the `MistralAsyncClient` when the `api_key` changes and pn.state.cache to store the client.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response.

<video controls poster="../assets/thumbnails/mistralai.png" >
    <source src="../assets/videos/mistralai.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/kickstart_snippets/mistralai.py' target='_blank'>mistralai.py</a></summary>

```python
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
```
</details>


## Llamacpp

Demonstrates how to use LlamaCpp with a local, quantized model, like TheBloke's Mistral Instruct v0.2,
with Panel's ChatInterface.

Highlights:

- Uses `pn.state.onload` to load the model from Hugging Face Hub when the app is loaded and prevent blocking the app.
- Uses `pn.state.cache` to store the `Llama` instance.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response.

<video controls poster="../assets/thumbnails/llamacpp.png" >
    <source src="../assets/videos/llamacpp.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/kickstart_snippets/llamacpp.py' target='_blank'>llamacpp.py</a></summary>

```python
"""
Demonstrates how to use LlamaCpp with a local, quantized model, like TheBloke's Mistral Instruct v0.2,
with Panel's ChatInterface.

Highlights:

- Uses `pn.state.onload` to load the model from Hugging Face Hub when the app is loaded and prevent blocking the app.
- Uses `pn.state.cache` to store the `Llama` instance.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response.
"""

import panel as pn
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.2-code-ft-GGUF"
FILENAME = "mistral-7b-instruct-v0.2-code-ft.Q5_K_S.gguf"

pn.extension()


def load_model():
    model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
    pn.state.cache["llama"] = Llama(
        model_path=model_path,
        chat_format="mistral-instruct",
        verbose=False,
        n_gpu_layers=-1,
    )
    chat_interface.disabled = False


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # memory is a list of messages
    messages = instance.serialize()

    llama = pn.state.cache["llama"]
    response = llama.create_chat_completion_openai_v1(messages=messages, stream=True)

    message = ""
    for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="LlamaCpp",
    help_text="Send a message to get a reply from LlamaCpp!",
    disabled=True,
)
template = pn.template.FastListTemplate(
    title="LlamaCpp Mistral",
    header_background="#A0A0A0",
    main=[chat_interface],
)
pn.state.onload(load_model)
template.servable()
```
</details>
