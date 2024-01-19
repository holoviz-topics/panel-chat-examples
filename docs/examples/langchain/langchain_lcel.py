"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[LangChain Expression Language](https://python.langchain.com/docs/expression_language/) (LCEL).
"""

import panel as pn
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

pn.extension()


async def callback(contents, user, instance):
    message = ""
    async for token in chain.astream(contents):
        message += token
        yield message


prompt = ChatPromptTemplate.from_template("Tell me a top-notch joke about {topic}")
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = {"topic": RunnablePassthrough()} | prompt | model | output_parser
chat_interface = pn.chat.ChatInterface(
    pn.chat.ChatMessage(
        "Offer a topic and ChatGPT will respond with a joke!", user="System"
    ),
    callback=callback,
    callback_user="ChatGPT",
)
chat_interface.servable()
