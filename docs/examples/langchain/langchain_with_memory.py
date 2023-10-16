"""
Demonstrates how to use the `ChatInterface` to create a chatbot with memory using
OpenAI and [LangChain](https://python.langchain.com/docs/get_started/introduction).
"""

import panel as pn
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await chain.apredict(input=contents)


chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)

callback_handler = pn.chat.langchain.PanelCallbackHandler(chat_interface)
llm = ChatOpenAI(streaming=True, callbacks=[callback_handler])
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
chat_interface.servable()
