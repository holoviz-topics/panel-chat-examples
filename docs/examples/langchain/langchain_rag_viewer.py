"""The Panel Langchain `RAG` viewer makes it easy to create and explore a
Retrival-Augmented Generator (RAG) chain.

You just need to provide a list of prompt `messages`, a list of `documents` and a `llm`.
"""
import panel as pn
import panel_chat_examples as pnc
from langchain.chat_models import ChatOpenAI

if pn.state.served:
    pn.extension()
    documents=pnc.langchain.sample_data.streamlit_to_panel_documents
    rag = pnc.langchain.RAG(
        messages=messages,
        documents=documents,
        llm=ChatOpenAI(model_name=MODEL_NAME),
        name="RAG",
    )