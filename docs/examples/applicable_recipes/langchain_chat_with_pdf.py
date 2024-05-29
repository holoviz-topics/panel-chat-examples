"""
Demonstrates how to use the `ChatInterface` to chat about a PDF using
OpenAI, [LangChain](https://python.langchain.com/docs/get_started/introduction) and
[Chroma](https://docs.trychroma.com/).
"""

import os
import tempfile

import panel as pn
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI

pn.extension()


@pn.cache
def initialize_chain(pdf, k, chain):
    # load document
    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(pdf)

    file_name = f.name
    loader = PyPDFLoader(file_name)
    documents = loader.load()
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    # select which embeddings we want to use
    embeddings = OpenAIEmbeddings()
    # create the vectorestore to use as the index
    db = Chroma.from_documents(texts, embeddings)
    # expose this index in a retriever interface
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chain to answer questions
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type=chain,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )
    return qa


def respond(contents, user, chat_interface):
    chat_input.placeholder = "Ask questions here!"
    if chat_interface.active == 0:
        chat_interface.active = 1
        yield {"user": "OpenAI", "value": "Let's chat about the PDF!"}

        contents.seek(0)
        pn.state.cache["pdf"] = contents.read()
        return

    qa = initialize_chain(pn.state.cache["pdf"], k_slider.value, chain_select.value)
    if key_input.value:
        os.environ["OPENAI_API_KEY"] = key_input.value

    response = qa({"query": contents})
    answers = pn.Accordion(("Response", response["result"]))
    for doc in response["source_documents"][::-1]:
        answers.append((f"Snippet from page {doc.metadata['page']}", doc.page_content))
    answers.active = [0, 1]
    yield {"user": "OpenAI", "value": answers}


# sidebar widgets
key_input = pn.widgets.PasswordInput(
    name="OpenAI Key",
    placeholder="sk-...",
)
k_slider = pn.widgets.IntSlider(
    name="Number of Relevant Chunks", start=1, end=5, step=1, value=2
)
chain_select = pn.widgets.RadioButtonGroup(
    name="Chain Type", options=["stuff", "map_reduce", "refine", "map_rerank"]
)

sidebar = pn.Column(key_input, k_slider, chain_select)

# main widgets
pdf_input = pn.widgets.FileInput(accept=".pdf", value="", height=50)
chat_input = pn.chat.ChatAreaInput(placeholder="First, upload a PDF!")
chat_interface = pn.chat.ChatInterface(
    help_text="Please first upload a PDF and click send!",
    callback=respond,
    sizing_mode="stretch_width",
    widgets=[pdf_input, chat_input],
    callback_exception="verbose",
)
chat_interface.active = 0

# layout
template = pn.template.BootstrapTemplate(sidebar=[sidebar], main=[chat_interface])
template.servable()
