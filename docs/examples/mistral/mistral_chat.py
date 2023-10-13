"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Mistral through CTransformers.
"""

import panel as pn
from ctransformers import AutoModelForCausalLM

pn.extension(design="material")

llms = pn.state.cache["llms"] = pn.state.cache.get("llms", {})


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    if "mistral" not in llms:
        instance.placeholder_text = "Downloading model; please wait..."
        llms["mistral"] = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            gpu_layers=1,
        )

    llm = llms["mistral"]
    response = llm(contents, stream=True, max_new_tokens=1000)
    message = ""
    for token in response:
        message += token
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="Mistral")
chat_interface.send(
    "Send a message to get a reply from Mistral!", user="System", respond=False
)
chat_interface.servable()
