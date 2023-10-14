"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[Llama2](https://ai.meta.com/llama/) and [Mistral](https://docs.mistral.ai).
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

# We cache the chains and responses to speed up things
llm_chains = pn.state.cache["llm_chains"] = pn.state.cache.get("llm_chains", {})
responses = pn.state.cache["responses"] = pn.state.cache.get("responses", {})

TEMPLATE = """<s>[INST] You are a friendly chat bot who's willing to help answer the
user:
{user_input} [/INST] </s>
"""

CONFIG = {"max_new_tokens": 256, "temperature": 0.5}


def _get_llm_chain(model, template=TEMPLATE, config=CONFIG):
    llm = CTransformers(**MODEL_KWARGS[model], config=config, streaming=True)
    prompt = PromptTemplate(template=template, input_variables=["user_input"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain


# Cannot use pn.cache due to https://github.com/holoviz/panel/issues/4236
async def _get_response(contents: str, model: str) -> str:
    key = (contents, model)
    if key in responses:
        return responses[key]

    llm_chain = llm_chains[model]
    response = responses[key] = await llm_chain.apredict(user_input=contents)
    return response


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    for model in MODEL_KWARGS:
        if model not in llm_chains:
            instance.placeholder_text = (
                f"Downloading {model}, this may take a few minutes, "
                f"or longer, depending on your internet connection."
            )
            llm_chains[model] = _get_llm_chain(model)

        entry = None
        response = await _get_response(contents, model)
        for chunk in response:
            entry = instance.stream(chunk, user=model.title(), entry=entry)


chat_interface = pn.widgets.ChatInterface(callback=callback, placeholder_threshold=0.1)
chat_interface.send(
    "Send a message to get a reply from both Llama 2 and Mistral (7B)!",
    user="System",
    respond=False,
)
chat_interface.servable()
