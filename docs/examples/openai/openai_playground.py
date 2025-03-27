"""
Demonstrates how to use the `ChatInterface` to highlight a **log probabilities**
of generated tokens from the OpenAI API.
"""

import os
import re

import numpy as np
import panel as pn
from openai import AsyncOpenAI

pn.extension()

COLORS = ["#94c4df", "#1764ab", "#084a92", "#08306b", "#000000"]


def highlight(text, log_prob):
    linear_prob = np.round(np.exp(log_prob) * 100, 2)
    if linear_prob >= 0 and linear_prob < 20:
        color_idx = 0
    elif linear_prob >= 20 and linear_prob < 40:
        color_idx = 1
    elif linear_prob >= 40 and linear_prob < 60:
        color_idx = 2
    elif linear_prob >= 60 and linear_prob < 80:
        color_idx = 3
    else:
        color_idx = 4

    # Generate HTML output with the chosen color
    if "'" in text:
        html_output = f'<span style="color: {COLORS[color_idx]};">{text}</span>'
    else:
        html_output = f"<span style='color: {COLORS[color_idx]}'>{text}</span>"
    return html_output


def custom_serializer(content):
    pattern = r"<span.*?>(.*?)</span>"
    matches = re.findall(pattern, content)
    if not matches:
        return content
    return matches[0]


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        aclient.api_key = api_key_input.value
    elif not os.environ["OPENAI_API_KEY"]:
        instance.send("Please provide an OpenAI API key", respond=False, user="ChatGPT")

    # gather messages for memory
    messages = instance.serialize(custom_serializer=custom_serializer)
    if system_input.value:
        system_message = {"role": "system", "content": system_input.value}
        messages = [system_message, *messages]

    response = await aclient.chat.completions.create(
        model=model_selector.value,
        messages=messages,
        stream=True,
        logprobs=True,
        temperature=temperature_input.value,
        max_tokens=max_tokens_input.value,
        seed=seed_input.value,
    )

    # stream response
    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        token = chunk.choices[0].logprobs
        if part and token:
            log_prob = token.content[0].logprob
            message += highlight(part, log_prob)
            yield message


aclient = AsyncOpenAI()
api_key_input = pn.widgets.PasswordInput(
    name="API Key",
    placeholder="sk-...",
    width=150,
)
system_input = pn.widgets.TextInput(name="System Prompt", value="")
model_selector = pn.widgets.Select(
    name="Model",
    options=["gpt-3.5-turbo", "gpt-4"],
    width=150,
)
temperature_input = pn.widgets.FloatInput(
    name="Temperature", start=0, end=2, step=0.01, value=1, width=100
)
max_tokens_input = pn.widgets.IntInput(name="Max Tokens", start=0, value=256, width=100)
seed_input = pn.widgets.IntInput(name="Seed", start=0, end=100, value=0, width=100)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="ChatGPT",
    callback_exception="verbose",
)
pn.Column(
    pn.Row(
        api_key_input,
        system_input,
        model_selector,
        temperature_input,
        max_tokens_input,
        seed_input,
        align="center",
    ),
    chat_interface,
).servable()
