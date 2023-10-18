"""The Panel Langchain `Document` viewer enables you to explore a single LangChain `Document` or a
list of LangChain `Document`s. This is quite useful while building your
Retrieval-Augmented Generation AI (RAG)."""
import panel as pn
import panel_chat_examples as pnc

if pn.state.served:
    pn.extension()
    documents=pnc.langchain.sample_data.streamlit_to_panel_documents
    pnc.langchain.Document(object=documents, sizing_mode="fixed", width=800).servable()