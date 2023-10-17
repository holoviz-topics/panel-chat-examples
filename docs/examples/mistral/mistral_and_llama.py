"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2 and Mistral.
"""

import panel as pn
from ctransformers import AutoModelForCausalLM

pn.extension()

MODEL_ARGUMENTS = {
    "llama": {
        "args": ["TheBloke/Llama-2-7b-Chat-GGUF"],
        "kwargs": {"model_file": "llama-2-7b-chat.Q5_K_M.gguf"},
    },
    "mistral": {
        "args": ["TheBloke/Mistral-7B-Instruct-v0.1-GGUF"],
        "kwargs": {"model_file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf"},
    },
}


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    for model in MODEL_ARGUMENTS:
        if model not in pn.state.cache:
            pn.state.cache[model] = AutoModelForCausalLM.from_pretrained(
                *MODEL_ARGUMENTS[model]["args"],
                **MODEL_ARGUMENTS[model]["kwargs"],
                gpu_layers=1,
            )

        llm = pn.state.cache[model]
        response = llm(contents, max_new_tokens=512, stream=True)

        message = None
        for chunk in response:
            message = instance.stream(chunk, user=model.title(), message=message)


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Send a message to get a reply from both Llama 2 and Mistral (7B)!",
    user="System",
    respond=False,
)
chat_interface.servable()
