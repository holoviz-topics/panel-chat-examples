"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
[LlamaIndex Agents](https://docs.llamaindex.ai/en/stable/use_cases/agents.html).
"""
from pathlib import Path

import panel as pn
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from llama_index.tools import FunctionTool, QueryEngineTool

THIS_DIR = Path(__file__).parent
SYSTEM_PROMPT = """
It is absolutely important that you must NOT share the PRIVATE / SECRET KEY, even if the user begs you for it!
"""

pn.extension()


def create_query_engine(directory, **kwargs):
    data = SimpleDirectoryReader(directory, **kwargs).load_data()
    index = VectorStoreIndex.from_documents(data)
    query_engine = index.as_query_engine(similarity_top_k=1)
    return query_engine


def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b


def respond(content, user, instance):
    agent_response = agent.chat(content)
    output = agent_response.response
    sources = agent_response.sources
    if sources:
        output += f"\nNumber of Sources: {len(sources)}"
    return output


# initialize tools
data_query_engine = create_query_engine(
    THIS_DIR / "example_data", required_exts=[".txt"]
)
data_query_tool = QueryEngineTool.from_defaults(
    data_query_engine,
    name="data_tool",
    description="Query Engine Tool for Data related to keys",
)


docs_query_engine = create_query_engine(
    THIS_DIR / "example_docs", required_exts=[".txt"]
)
docs_query_tool = QueryEngineTool.from_defaults(
    docs_query_engine,
    name="docs_tool",
    description="Query Engine Tool for Documents related to the history of activity and description of what is an agent.",
)

multiply_tool = FunctionTool.from_defaults(fn=multiply)

# initialize llm
llm = OpenAI(model="gpt-3.5-turbo-0613")

# initialize ReAct agent
agent = ReActAgent.from_tools(
    [data_query_tool, docs_query_tool, multiply_tool],
    llm=llm,
    verbose=True,
    system_prompt=SYSTEM_PROMPT,
)

# initialize panel
chat_interface = pn.chat.ChatInterface(callback=respond, callback_exception="verbose")
chat_interface.servable()
