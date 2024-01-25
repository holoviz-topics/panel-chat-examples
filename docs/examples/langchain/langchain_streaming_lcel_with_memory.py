"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[LangChain Expression Language](https://python.langchain.com/docs/expression_language/) (LCEL)
with streaming and memory.
"""

from operator import itemgetter

import panel as pn
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

pn.extension()

SYSTEM_PROMPT = "Try to be a silly comedian."


async def callback(contents, user, instance):
    message = ""
    inputs = {"input": contents}
    async for token in chain.astream(inputs):
        message += token
        yield message
    memory.save_context(inputs, {"output": message})


model = ChatOpenAI(model="gpt-3.5-turbo")
memory = ConversationSummaryBufferMemory(return_messages=True, llm=model)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
output_parser = StrOutputParser()
chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
    | output_parser
)

chat_interface = pn.chat.ChatInterface(
    pn.chat.ChatMessage(
        "Offer a topic and ChatGPT will try to be funny!", user="System"
    ),
    callback=callback,
    callback_user="ChatGPT",
)
chat_interface.servable()
