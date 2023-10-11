"""
Demonstrates how to use the ChatInterface widget to chat about a PDF using
OpenAI's API with LangChain.
"""

import os
import tempfile
from pathlib import Path

import panel as pn
import param
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from panel_chat_examples import EnvironmentWidgetBase

# Conversion to str can be removed when https://github.com/holoviz/panel/pull/5607 is released
EXAMPLE_PDF = str(Path(__file__).parent / "example.pdf")
TTL = 1800  # 30 minutes

pn.extension(design="material")


class EnvironmentWidget(EnvironmentWidgetBase):
    OPENAI_API_KEY: str = param.String()


class State(param.Parameterized):
    pdf: bytes = param.Bytes()
    number_of_chunks: int = param.Integer(default=2, bounds=(1, 5), step=1)
    chain_type: str = param.Selector(
        objects=["stuff", "map_reduce", "refine", "map_rerank"]
    )


@pn.cache(ttl=TTL)
def _get_texts(pdf):
    # load documents
    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(pdf)
    file_name = f.name
    loader = PyPDFLoader(file_name)
    documents = loader.load()

    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


@pn.cache(ttl=TTL)
def _get_vector_db(pdf, openai_api_key):
    texts = _get_texts(pdf)
    # select which embeddings we want to use
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # create the vectorestore to use as the index
    return Chroma.from_documents(texts, embeddings)


@pn.cache(ttl=TTL)
def _get_retriever(pdf, openai_api_key: str, number_of_chunks: int):
    db = _get_vector_db(pdf, openai_api_key)
    return db.as_retriever(
        search_type="similarity", search_kwargs={"k": number_of_chunks}
    )


@pn.cache(ttl=3600)
def _get_retrival_qa(
    pdf: bytes, number_of_chunks: int, chain_type: str, openai_api_key: str
):
    retriever = _get_retriever(pdf, openai_api_key, number_of_chunks)
    return RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )


environ = EnvironmentWidget()
state = State()


def _get_validation_message():
    pdf = state.pdf
    openai_api_key = environ.OPENAI_API_KEY
    if not pdf and not openai_api_key:
        return "Please first enter an OpenAI Api key and upload a PDF!"
    if not pdf:
        return "Please first upload a PDF!"
    if not openai_api_key:
        return "Please first enter an OpenAI Api key!"
    return ""


def _send_not_ready_message() -> bool:
    message = _get_validation_message()

    if message:
        chat_interface.send({"user": "System", "value": message}, respond=False)
    return bool(message)


async def respond(contents, user, chat_interface):
    if _send_not_ready_message():
        return
    if chat_interface.active == 0:
        chat_interface.active = 1
        chat_interface.active_widget.placeholder = "Ask questions here!"
        yield {"user": "OpenAI", "value": "Let's chat about the PDF!"}
        return
    text_input.placeholder = "Ask questions here!"
    qa = _get_retrival_qa(
        state.pdf, state.number_of_chunks, state.chain_type, environ.OPENAI_API_KEY
    )
    response = qa({"query": contents})
    pages = pn.Accordion()
    pages = []

    for doc in response["source_documents"][::-1]:
        name = f"Chunk {doc.metadata['page']}"
        content = doc.page_content
        pages.append((name, content))

    pages_layout = pn.Accordion(*pages)
    answers = pn.Column(response["result"], pages_layout)

    yield {"user": "OpenAI", "value": answers}


pdf_input = pn.widgets.FileInput.from_param(state.param.pdf, accept=".pdf", height=50)
text_input = pn.widgets.TextInput(placeholder="First, upload a PDF!")
chat_interface = pn.widgets.ChatInterface(
    callback=respond, sizing_mode="stretch_width", widgets=[pdf_input, text_input]
)

_send_not_ready_message()

chain_type = pn.widgets.RadioButtonGroup.from_param(
    state.param.chain_type,
    orientation="vertical",
    sizing_mode="stretch_width",
)
template = pn.template.BootstrapTemplate(
    sidebar=[
        environ,
        state.param.number_of_chunks,
        chain_type,
    ],
    main=[chat_interface],
)
template.servable()
