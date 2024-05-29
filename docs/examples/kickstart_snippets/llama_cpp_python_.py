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
