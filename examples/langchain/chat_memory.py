"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API with LangChain.
"""

import panel as pn
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    await chain.apredict(input=contents)


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)

callback_handler = pn.widgets.langchain.PanelCallbackHandler(
    chat_interface=chat_interface
)
llm = ChatOpenAI(streaming=True, callbacks=[callback_handler])
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
chat_interface.servable()
