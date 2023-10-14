import re
from pathlib import Path

import panel as pn
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

EMBEDDINGS_DIR = Path.cwd() / ".cache/assistant_panel_developer"
CODE_REGEX = re.compile(r"```\s?python(.*?)```", re.DOTALL)

sitemap = [
    "https://panel.holoviz.org/how_to/streamlit_migration/index.html",
    "https://panel.holoviz.org/how_to/streamlit_migration/panes.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/layouts.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/widgets.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/templates.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/activity.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/interactivity.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/caching.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/session_state.html",
    # "https://panel.holoviz.org/how_to/streamlit_migration/multipage_apps.html",
]
SCRIPT = Path.cwd() / "script.py"
PROMPT_TEMPLATE = """You are an experienced Python developer specializing in converting
Streamlit apps to HoloViz Panel apps.
    
You must use

- `.servable` on Panel components to make your app servable
- `sizing_mode="stretch_width"` as argument to `pn.extension`
- the `fast` template instead of the default blank template
- `pn.bind` instead of `@pn.depends`
- `if pn.state.served:` syntax instead of `if __name__=="__main__:"` syntax
- Panel widgets as arguments to panel and hvplot objects and bound functions
- Pascal Cased Panel widgets, panes and layouts
- a `max_height` argument of 1000 when use `pn.pane.DataFrame`, `pn.widgets.Tabulator`,
"pn.pane.Perspective"

in the code generated.

You may not use

- `.show` method on Panel components
- Panel widgets as arguments to matplotlib, plotly or altair plots
- widgets with `pn.bind` or `@pn.depends` that have not been declared yet
- `pn.state.cache` as a function. Its a dictionary.
- `@pn.depends` annotations on functions with no arguments

in the code generated

Here is additional context

{context}

You must convert the Streamlit app below to a HoloViz Panel app

```python
{question}
```

You must return runnable code. Don't return explanations! Don't return the code inside
code blocks."""


@pn.cache(to_disk=True)
def _read_document(url, print=print):
    print(f"Loading {url}")
    loader = WebBaseLoader(url)
    return loader.load()


def _split_documents(documents, print=print):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=500, chunk_overlap=40
    )

    for document in documents:
        for chunk in text_splitter.split_documents(document):
            yield chunk


def _get_vector_db():
    documents = (_read_document(url) for url in sitemap)
    chunks = _split_documents(documents)
    chunks = list(chunks)

    openai_embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=openai_embeddings,
        persist_directory=str(EMBEDDINGS_DIR),
    )
    vectordb.persist()
    return vectordb


def _get_prompt_template():
    return PromptTemplate(
        template=PROMPT_TEMPLATE, input_variables=["context", "question"]
    )


def _get_retrieval_qa():
    vectordb = _get_vector_db()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    prompt = _get_prompt_template()

    chain_type_kwargs = {"prompt": prompt}
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
    )


def _convert(code: str, retrieval_qa) -> str:
    retrieval_qa

    answer = retrieval_qa(code)
    result = answer["result"]
    if CODE_REGEX.search(result):
        result = CODE_REGEX.search(result).group(1)
    return result


retrieval_qa = _get_retrieval_qa()


async def respond(contents, user, chat_interface):
    code = _convert(contents, retrieval_qa)
    SCRIPT.write_text(code, newline="\n")
    response = pn.Column(
        "Here is the code as a Panel data app",
        pn.widgets.Ace(value=code, height=500, width=500),
    )

    yield {"user": "OpenAI", "value": response}


if __name__.startswith("bokeh"):
    chat_interface = pn.widgets.ChatInterface(
        callback=respond,
        sizing_mode="stretch_width",
        widgets=[pn.widgets.Ace()],
    ).servable()
