"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Mistral thru CTransformers.
"""

import panel as pn
from ctransformers import AutoConfig, AutoModelForCausalLM, Config

pn.extension()

SYSTEM_INSTRUCTIONS = "Reply to the user in a friendly manner."


def apply_template(contents, history):
    if not history:
        text_row = f"""<s>[INST]{SYSTEM_INSTRUCTIONS} {contents}[/INST]"""
    else:
        prior_input_output = "\n".join(history)
        text_row = f"""{prior_input_output}[INST]{contents}[/INST]"""
    return text_row


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
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
    prompt = apply_template(contents, history)
    response = llm(prompt, stream=True)
    message = ""
    for token in response:
        message += token
        yield message
    history.append(prompt + message + "</s>")


llms = {}
history = []
chat_interface = pn.widgets.ChatInterface(
    callback=callback,
    callback_user="Mistral",
    reset_on_send=True,
)
chat_interface.send(
    "Send a message to get a reply from Mistral!", user="System", respond=False
)
chat_interface.servable()
