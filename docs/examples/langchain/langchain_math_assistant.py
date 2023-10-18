"""
Demonstrates how to use the `ChatInterface` to create
a math chatbot using OpenAI and the `PanelCallbackHandler` for
[LangChain](https://python.langchain.com/docs/get_started/introduction). See
[LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/).
"""

import panel as pn
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    final_answer = await llm_math.arun(question=contents)
    instance.stream(final_answer, message=instance.value[-1])


chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="Langchain")
chat_interface.send(
    "Send a math question to get an answer from MathGPT!", user="System", respond=False
)

callback_handler = pn.chat.langchain.PanelCallbackHandler(chat_interface)
llm = OpenAI(streaming=True, callbacks=[callback_handler])
llm_math = LLMMathChain.from_llm(llm, verbose=True)
chat_interface.servable()
