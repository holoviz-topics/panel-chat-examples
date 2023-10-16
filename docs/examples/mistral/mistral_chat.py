"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[Mistral](https://docs.mistral.ai) through
[CTransformers](https://github.com/marella/ctransformers).
"""

import panel as pn
from ctransformers import AutoConfig, AutoModelForCausalLM, Config

pn.extension(design="material")

llms = pn.state.cache["llms"] = pn.state.cache.get("llms", {})

INSTRUCTIONS = "You are a friendly chat bot willing to help out the user."


def apply_template(instructions, contents):
    text_row = f"""<s>[INST]{instructions} {contents}[/INST]"""
    return text_row


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if "mistral" not in llms:
        instance.placeholder_text = "Downloading model; please wait..."
        config = AutoConfig(
            config=Config(
                temperature=0.5, max_new_tokens=2048, context_length=2048, gpu_layers=1
            ),
        )
        llms["mistral"] = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            config=config,
        )

    llm = llms["mistral"]
    response = llm(apply_template(INSTRUCTIONS, contents), stream=True)
    message = ""
    for token in response:
        message += token
        yield message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="Mistral",
    reset_on_send=True,
)
chat_interface.send(
    "Send a message to get a reply from Mistral!", user="System", respond=False
)
chat_interface.servable()
