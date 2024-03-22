"""
Demonstrates how to use LangChain to wrap OpenAI's GPT-3.5 API with Panel's ChatInterface.

Highlights:

- Uses `PasswordInput` to set the API key, or uses the `OPENAI_API_KEY` environment variable.
- Uses `serialize` to get chat history from the `ChatInterface`.
- Uses `yield` to continuously concatenate the parts of the response
"""

from operator import itemgetter

import panel as pn
from langchain.memory import ConversationTokenBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        # use api_key_input.value if set, otherwise use OPENAI_API_KEY
        llm.api_key = api_key_input.value

    memory.clear()
    for message in instance.serialize():
        if message["role"] == "user":
            memory.chat_memory.add_user_message(HumanMessage(**message))
        else:
            memory.chat_memory.add_ai_message(AIMessage(**message))

    response = chain.astream({"user_input": contents})

    message = ""
    async for chunk in response:
        message += chunk
        yield message


llm = ChatOpenAI(model="gpt-3.5-turbo")
memory = ConversationTokenBufferMemory(
    return_messages=True,
    llm=llm,
    memory_key="chat_history",
    max_token_limit=8192 - 1024,
)
memory_link = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables)
    | itemgetter("chat_history")
)
prompt_link = ChatPromptTemplate.from_template(
    "{chat_history}\n\nBe a helpful chat bot and answer: {user_input}",
)
output_parser = StrOutputParser()

chain = (
    {"user_input": RunnablePassthrough()}
    | memory_link
    | prompt_link
    | llm
    | output_parser
)

api_key_input = pn.widgets.PasswordInput(
    placeholder="sk-... uses $OPENAI_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="GPT-3.5",
    help_text="Send a message to get a reply from GPT 3.5 Turbo!",
    callback_exception="verbose",
)
template = pn.template.FastListTemplate(
    title="LangChain OpenAI GPT-3.5",
    header_background="#E8B0E6",
    main=[chat_interface],
    header=[api_key_input],
)
template.servable()
