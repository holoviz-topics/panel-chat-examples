"""Retrieval-Augmented Generation (RAG) can answer questions by using

- A *large language model* (`llm`)
- A list of (templated) `messages` to *prompt* the `llm`
- A list of `documents` embedded in a `vector_store` to provide context to the `llm`.
"""
from pathlib import Path
from typing import List
from uuid import uuid4

import panel as pn
import param
from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseLanguageModel
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.schema.vectorstore import VectorStore
from langchain.vectorstores import Chroma

from panel_chat_examples.langchain._document import Document

ROLE_MAP = {
    AIMessage: "assistant",
    HumanMessage: "user",
    SystemMessage: "system",
}


def _get_persist_directory() -> Path:
    return Path.cwd() / ".cache/panel_chat_examples/vector_store" / str(uuid4())

class LLMValueError(ValueError):
    def __init__(self, llm):
        super().__init__(f"llm of type {type(llm)} is not supported")

def _get_embedding(llm):
    if isinstance(llm, ChatOpenAI):
        return OpenAIEmbeddings()
    raise LLMValueError(llm)


def _convert_message(message):
    if isinstance(message, tuple):
        return pn.widgets.ChatEntry(user=message[0], value=message[1])
    user = ROLE_MAP[message.__class__]
    return pn.widgets.ChatEntry(user=user, value=message.content)


def _to_chat_entries(messages):
    return [_convert_message(message) for message in messages]


class RAG(pn.viewable.Viewer):
    """
    Retrieval-Augmented Generation (RAG) can answer questions by using

- A *large language model* (`llm`)
- A list of (templated) `messages` to *prompt* the `llm`
- A list of `documents` embedded in a `vector_store` to provide context to the `llm`.
"""
    documents: List[Document] = param.List(
        class_=Document, allow_None=False, constant=True
    )
    messages: List = param.List(allow_None=False, constant=True)
    llm: BaseLanguageModel = param.ClassSelector(
        class_=BaseLanguageModel, allow_None=False, constant=True
    )

    def __init__(self, **params):
        super().__init__(**params)

        self._prompt = None
        self._vector_db = None
        self._retrieval_qa = None
        self._script = "script.py"

        chat_feed = pn.widgets.ChatFeed(
            value=_to_chat_entries(self.messages),
            name="Prompt",
        )
        documents_viewer = Document(objects=self.documents, name="Documents")

        self._layout = pn.Tabs(
            chat_feed,
            documents_viewer,
            pn.panel(self.param.llm, name="LLM"),
        )

    def __panel__(self):
        return self._layout

    @staticmethod
    def _create_prompt(messages) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(messages)

    @property
    def prompt(self) -> ChatPromptTemplate:
        if not self._prompt:
            self._prompt = self._create_prompt(self.messages)
        return self._prompt

    @staticmethod
    def _create_vector_store(documents, embedding) -> VectorStore:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding,
            persist_directory=str(_get_persist_directory()),
        )
        vector_store.persist()
        return vector_store

    @property
    def vector_store(self) -> VectorStore:
        if not self._vector_db:
            self._vector_db = self._create_vector_store(
                self.documents, _get_embedding(self.llm)
            )
        return self._vector_db

    @staticmethod
    def create_retrival_qa(vector_store, prompt, llm) -> BaseRetrievalQA:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        chain_type_kwargs = {"prompt": prompt}
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs=chain_type_kwargs,
        )

    @property
    def retrieval_qa(self) -> BaseRetrievalQA:
        if not self._retrieval_qa:
            self._retrieval_qa = self.create_retrival_qa(
                self.vector_store, self.prompt, self.llm
            )
        return self._retrieval_qa
