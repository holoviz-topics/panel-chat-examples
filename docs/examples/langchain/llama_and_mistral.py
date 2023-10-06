"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2.
"""

import panel as pn

from langchain.chains import LLMChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

pn.extension()

MODEL_KWARGS = {
    "llama": {
        "model": "TheBloke/Llama-2-7b-Chat-GGUF",
        "model_file": "llama-2-7b-chat.Q5_K_M.gguf",
    },
    "mistral": {
        "model": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "model_file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    },
}
llm_chains = {}

TEMPLATE = """<s>[INST] You are a friendly chat bot who's willing to help answer the user:
{user_input} [/INST] </s>
"""


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    config = {"max_new_tokens": 256, "temperature": 0.5}

    for model in MODEL_KWARGS:
        if model not in llm_chains:
            llm = CTransformers(**MODEL_KWARGS[model], config=config)
            prompt = PromptTemplate(template=TEMPLATE, input_variables=["user_input"])
            llm_chain = LLMChain(prompt=prompt, llm=llm)
            llm_chains[model] = llm_chain
        instance.send(
            await llm_chains[model].apredict(user_input=contents),
            user=model.title(),
            respond=False,
        )


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Send a message to get a reply from both Llama 2 and Mistral (7B)!",
    user="System",
    respond=False,
)
chat_interface.servable()
