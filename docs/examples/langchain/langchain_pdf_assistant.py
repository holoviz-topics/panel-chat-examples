"""
Demonstrates how to use the `ChatInterface` to chat about a PDF using
OpenAI, [LangChain](https://python.langchain.com/docs/get_started/introduction) and
[Chroma](https://docs.trychroma.com/).
"""

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

EXAMPLE_PDF = Path(__file__).parent / "example.pdf"
TTL = 1800  # 30 minutes

pn.extension()

# Define the Retrieval Question/ Answer Chain
# We use caching to speed things up


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


@pn.cache(ttl=TTL)
def _get_retrieval_qa(
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


def _get_response(contents):
    qa = _get_retrieval_qa(
        state.pdf, state.number_of_chunks, state.chain_type, environ.OPENAI_API_KEY
    )
    response = qa({"query": contents})
    chunks = []

    for chunk in response["source_documents"][::-1]:
        name = f"Chunk {chunk.metadata['page']}"
        content = chunk.page_content
        chunks.insert(0, (name, content))
    return response, chunks


# Define the Application State
class EnvironmentWidget(EnvironmentWidgetBase):
    OPENAI_API_KEY: str = param.String()


class State(param.Parameterized):
    pdf: bytes = param.Bytes()
    number_of_chunks: int = param.Integer(default=2, bounds=(1, 5), step=1)
    chain_type: str = param.Selector(
        objects=["stuff", "map_reduce", "refine", "map_rerank"]
    )


environ = EnvironmentWidget()
state = State()

# Define the widgets
pdf_input = pn.widgets.FileInput.from_param(state.param.pdf, accept=".pdf", height=50)
text_input = pn.widgets.TextInput(placeholder="First, upload a PDF!")
chain_type_input = pn.widgets.RadioButtonGroup.from_param(
    state.param.chain_type,
    orientation="vertical",
    sizing_mode="stretch_width",
    button_type="primary",
    button_style="outline",
)

# Define and configure the ChatInterface


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


def _send_not_ready_message(chat_interface) -> bool:
    message = _get_validation_message()

    if message:
        chat_interface.send({"user": "System", "value": message}, respond=False)
    return bool(message)


async def respond(contents, user, chat_interface):
    if _send_not_ready_message(chat_interface):
        return
    if chat_interface.active == 0:
        chat_interface.active = 1
        chat_interface.active_widget.placeholder = "Ask questions here!"
        yield {"user": "OpenAI", "value": "Let's chat about the PDF!"}
        return

    response, documents = _get_response(contents)
    pages_layout = pn.Accordion(*documents, sizing_mode="stretch_width", max_width=800)
    answers = pn.Column(response["result"], pages_layout)

    yield {"user": "OpenAI", "value": answers}


chat_interface = pn.chat.ChatInterface(
    callback=respond,
    sizing_mode="stretch_width",
    widgets=[pdf_input, text_input],
    disabled=True,
)


@pn.depends(state.param.pdf, environ.param.OPENAI_API_KEY, watch=True)
def _enable_chat_interface(pdf, openai_api_key):
    if pdf and openai_api_key:
        chat_interface.disabled = False
    else:
        chat_interface.disabled = True


_send_not_ready_message(chat_interface)

## Wrap the app in a nice template

template = pn.template.BootstrapTemplate(
    sidebar=[
        environ,
        state.param.number_of_chunks,
        "Chain Type:",
        chain_type_input,
    ],
    main=[chat_interface],
)
template.servable()
