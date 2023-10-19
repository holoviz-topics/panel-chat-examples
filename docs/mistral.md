# Mistral

## And Llama

Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2 and Mistral.

<details>

<summary>Source code for <a href='../examples/mistral/mistral_and_llama.py' target='_blank'>mistral_and_llama.py</a></summary>

```python
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
```
</details>


## Chat

Demonstrates how to use the `ChatInterface` to create a chatbot using
[Mistral](https://docs.mistral.ai) through
[CTransformers](https://github.com/marella/ctransformers).

<video controls poster="../assets/thumbnails/mistral_chat.png" >
    <source src="../assets/videos/mistral_chat.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/mistral/mistral_chat.py' target='_blank'>mistral_chat.py</a></summary>

```python
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
```
</details>


## With Memory

Demonstrates how to use the `ChatInterface` to create a chatbot using
[Mistral](https://docs.mistral.ai) through
[CTransformers](https://github.com/marella/ctransformers). The chatbot includes a
memory of the conversation history.

<video controls poster="../assets/thumbnails/mistral_with_memory.png" >
    <source src="../assets/videos/mistral_with_memory.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/mistral/mistral_with_memory.py' target='_blank'>mistral_with_memory.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[Mistral](https://docs.mistral.ai) through
[CTransformers](https://github.com/marella/ctransformers). The chatbot includes a
memory of the conversation history.
"""

import panel as pn
from ctransformers import AutoConfig, AutoModelForCausalLM, Config

pn.extension(design="material")

SYSTEM_INSTRUCTIONS = "Do what the user requests."


def apply_template(history):
    history = [message for message in history if message.user != "System"]
    prompt = ""
    for i, message in enumerate(history):
        if i == 0:
            prompt += f"<s>[INST]{SYSTEM_INSTRUCTIONS} {message.value}[/INST]"
        else:
            if message.user == "Mistral":
                prompt += f"{message.value}</s>"
            else:
                prompt += f"""[INST]{message.value}[/INST]"""
    return prompt


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
    history = [message for message in instance.value]
    prompt = apply_template(history)
    response = llm(prompt, stream=True)
    message = ""
    for token in response:
        message += token
        yield message


llms = {}
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="Mistral",
)
chat_interface.send(
    "Send a message to get a reply from Mistral!", user="System", respond=False
)
chat_interface.servable()
```
</details>