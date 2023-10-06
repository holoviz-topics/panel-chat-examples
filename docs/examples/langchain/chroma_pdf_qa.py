"""
Demonstrates how to use the ChatInterface widget to chat about a PDF using
OpenAI's API with LangChain.
"""

import os
import tempfile

import panel as pn
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

pn.extension()


def initialize_chain():
    if key_input.value:
        os.environ["OPENAI_API_KEY"] = key_input.value

    selections = (pdf_input.value, k_slider.value, chain_select.value)
    if selections in pn.state.cache:
        return pn.state.cache[selections]

    chat_input.placeholder = "Ask questions here!"

    # load document
    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(pdf_input.value)
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
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": k_slider.value}
    )
    # create a chain to answer questions
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type=chain_select.value,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )
    return qa


async def respond(contents, user, chat_interface):
    if not pdf_input.value:
        chat_interface.send(
            {"user": "System", "value": "Please first upload a PDF!"}, respond=False
        )
        return
    elif chat_interface.active == 0:
        chat_interface.active = 1
        chat_interface.active_widget.placeholder = "Ask questions here!"
        yield {"user": "OpenAI", "value": "Let's chat about the PDF!"}
        return

    qa = initialize_chain()
    response = qa({"query": contents})
    answers = pn.Column(response["result"])
    answers.append(pn.layout.Divider())
    for doc in response["source_documents"][::-1]:
        answers.append(f"**Page {doc.metadata['page']}**:")
        answers.append(f"```\n{doc.page_content}\n```")
    yield {"user": "OpenAI", "value": answers}


pdf_input = pn.widgets.FileInput(accept=".pdf", value="", height=50)
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
chat_input = pn.widgets.TextInput(placeholder="First, upload a PDF!")
chat_interface = pn.widgets.ChatInterface(
    callback=respond, sizing_mode="stretch_width", widgets=[pdf_input, chat_input]
)
chat_interface.send(
    {"user": "System", "value": "Please first upload a PDF and click send!"},
    respond=False,
)
template = pn.template.BootstrapTemplate(
    sidebar=[key_input, k_slider, chain_select], main=[chat_interface]
)
template.servable()
