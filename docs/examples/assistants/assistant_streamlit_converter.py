"""The `StreamlitConverter` converts Streamlit apps to Panel apps based on
Retrieval-Augmented Generation (RAG) which uses

- A *llm* to answer questions
- A list of (templated) `messages` to *prompt* the llm
- A list of `documents` to provide context to the llm.
  - The documents are embedded into a `VectorStore` which provides *similarity search*.
The most *similar* documents are provided to the `llm` as context.
"""
import re
from pathlib import Path

import panel as pn
import param
    from langchain.callbacks import get_openai_callback
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, WebBaseLoader
from langchain.schema import AIMessage, HumanMessage
from langchain.text_splitter import MarkdownHeaderTextSplitter

import panel_chat_examples as pnc

EMBEDDINGS_DIR = Path.cwd() / ".cache/assistant_panel_developer"
CODE_REGEX = re.compile(r"```\s?python(.*?)```", re.DOTALL)
MODEL_NAME = "gpt-3.5-turbo"
DOCS = Path(__file__).parent.parent.parent
URLS = [
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/activity.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/caching.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/get_started.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/index.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/index.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/interactivity.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/layouts.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/multipage_apps.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/panes.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/session_state.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/templates.md",
    "https://raw.githubusercontent.com/holoviz/panel/main/doc/how_to/streamlit_migration/widgets.md",
]
SYSTEM_INSTRUCTION = """I am an experienced Python developer specializing in converting
Streamlit apps to HoloViz Panel apps.

In the converted code, I will always!!!

- answer with working Panel code inside a Python Markdown code block.
- include `import panel as pn`
- provide `sizing_mode="stretch_width"` as argument to `pn.extension`
- provide `template="fast"` as argument to `pn.extension`
- Pascal Cased Panel widgets, panes and layouts
- Panel widgets as arguments to panel and hvplot objects and bound functions
- `pn.pane.Perspective` instead of `pn.pane.DataFrame`. And I will remember to add
`"perspective"` as an argument to `pn.extension` if I do.
- a `max_height` argument of 1000 when I use `pn.pane.Perspective` or
`pn.widgets.Tabulator`.
- hvPlot to plot with unless I recognize the plotting library Streamlit is using and
know how to use it with Panel
- Rename any 'Streamlit' text to 'Panel'

In the converted code, I will never!!!

- add `.show` method anywhere
- add `.servable` method to functions or methods
- use Panel widgets as arguments to Matplotlib, Plotly or Altair plots
- use widgets that have not yet been declared with `pn.bind` or `@pn.depends`
- use `pn.state.cache` as a function because it is a dictionary.
- use `@pn.depends` annotations on functions with no arguments
- include `import streamlit as st`

The converted code will contain exactly one Panel component named `app`, that I mark
`.servable()`.
"""
USER_CONTEXT_INSTRUCTIONS = """
Below I provide you with selected documentation or example code that you might find
useful as background material when converting the code.

<hr/>

{context}
"""
ASSISTANT_ANSWER_INSTRUCTIONS = """```python
{answer}
```"""
USER_QUESTION_INSTRUCTION = """\
Please convert the `source` Streamlit app below

```python
{question}
```"""

EXAMPLE_2_STREAMLIT = """\
import streamlit as st
import pandas as pd

st.header('First Streamlit Application')
st.subheader('Created by: MP')

df= pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

st.write('This is a sample dataframe')
st.dataframe(df)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button('Download the Sample DataFrame', data=csv)"""
EXAMPLE_2_PANEL = """\
import panel as pn
import pandas as pd
from io import StringIO

pn.extension("perspective", sizing_mode="stretch_width", template="fast")

df= pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

@pn.cache
def convert_df(df):
    sio = StringIO()
    df.to_csv(sio)
    sio.seek(0)
    return sio

app = pn.Column(
    "# First Panel Application",
    "## Created by: MP",
    pn.pane.Perspective(df, sizing_mode="stretch_width", max_height=1000),
    pn.widgets.FileDownload(file=convert_df(df), name="Download the Sample DataFrame",),
)
app.servable()"""

MESSAGES = [
    ("system", SYSTEM_INSTRUCTION),
    (
        "user",
        USER_QUESTION_INSTRUCTION.format(
            question="""import streamlit as st\nst.write("Hello World")"""
        ),
    ),
    (
        "assistant",
        ASSISTANT_ANSWER_INSTRUCTIONS.format(
            answer="""import panel as pn\npn.extension(sizing_mode="stretch_width", template="fast")\napp=pn.panel("Hello World")\napp.servable()"""
        ),
    ),
    HumanMessage(
        content=USER_QUESTION_INSTRUCTION.format(question=EXAMPLE_2_STREAMLIT)
    ),
    AIMessage(content=ASSISTANT_ANSWER_INSTRUCTIONS.format(answer=EXAMPLE_2_PANEL)),
    ("user", USER_CONTEXT_INSTRUCTIONS),
    ("user", USER_QUESTION_INSTRUCTION),
]
HEADERS_TO_SPLIT_ON = [("#", "Header 1"), ("##", "Header 2")]
COST_PER_TOKEN = {"gpt-3.5-turbo": 0.002 / 1000}


@pn.cache(to_disk=True, ttl=60 * 60 * 24)
def _get_web_documents():
    migration_documents = WebBaseLoader(URLS).load()
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON
    )
    documents = []
    for source in migration_documents:
        for document in markdown_splitter.split_text(source.page_content):
            documents.append(document)
    return documents


@pn.cache(ttl=60 * 60 * 24)
def _get_code_documents():
    documents = []
    code_documents = DirectoryLoader(DOCS, glob="*.py", recursive=True).load()
    for source in code_documents:
        if "```" in source.page_content:
            continue
        title = (
            source.metadata["source"]
            .split("/")[-1]
            .replace(".py", "")
            .replace("_", " ")
            .title()
        )
        source.page_content = f"""
# {title}

```python
{source.page_content}
```
"""
        documents.append(source)
    return documents


def _get_documents():
    return _get_web_documents() + _get_code_documents()


class StreamlitConverter(pn.viewable.Viewer):
    source = param.String(label="Source: Streamlit")
    target = param.String(label="Target: Panel")
    convert = param.Event()

    converting = param.Boolean()
    retrieval_qa: BaseRetrievalQA = param.ClassSelector(
        class_=BaseRetrievalQA, allow_None=False
    )
    tokens = param.Integer()
    total_tokens = param.Integer()

    def __init__(self, **params):
        super().__init__(**params)
        self._layout = self._create_layout()

    def _create_layout(
        self,
    ):
        self._convert_button = pn.widgets.Button.from_param(
            self.param.convert, button_type="primary", align="center"
        )
        conversion = pn.Row(
            pn.Column(
                f"### {self.param.source.label}",
                pn.widgets.CodeEditor.from_param(
                    self.param.source, sizing_mode="stretch_width"
                ),
            ),
            self._convert_button,
            pn.Column(
                f"### {self.param.target.label}",
                pn.widgets.CodeEditor.from_param(
                    self.param.target, sizing_mode="stretch_width"
                ),
            ),
            name="Code Converter",
        )
        return pn.Column(conversion, self.status)

    def __panel__(self):
        return self._layout

    def _clean(self, result: str) -> str:
        if CODE_REGEX.search(result):
            result = CODE_REGEX.search(result).group(1)
        result = result.strip()
        return result

    @param.depends("converting", watch=True)
    def _handle_disabled(self):
        self.param.convert.constant = self.converting
        self._convert_button.loading = self.converting

    @param.depends("convert", watch=True)
    def _handle_conversion(self):
        self.converting = True
        try:
            with get_openai_callback() as cb:
                answer = self.retrieval_qa(self.source)

            self.tokens = cb.total_tokens
            self.total_tokens += cb.total_tokens

            result = answer["result"]
            self.target = self._clean(result)
        except Exception as ex:
            self.target = str(ex)
        self.converting = False

    @param.depends("tokens", "total_tokens")
    def status(self):
        cost_per_token = COST_PER_TOKEN["gpt-3.5-turbo"]
        return f"""
## Status

Tokens = {self.tokens}
Total Tokens = {self.total_tokens}
Total Cost = {self.total_tokens * cost_per_token} $
"""


if __name__.startswith("bokeh"):
    pn.extension("codeeditor")

    rag = pnc.langchain.RAG(
        messages=MESSAGES,
        documents=_get_documents(),
        llm=ChatOpenAI(model_name=MODEL_NAME),
        name="RAG",
    )
    converter = StreamlitConverter(
        source=EXAMPLE_2_STREAMLIT, retrieval_qa=rag.retrieval_qa, name="Converter"
    )

    @param.depends(converter.param.target, watch=True)
    def save_target(target):
        (Path.cwd() / "script.py").write_text(target, newline="\n")
        print("saved to script.py")

    main = pn.Tabs(
        converter,
        rag,
        pn.pane.Markdown(__doc__, name="Info", sizing_mode="stretch_width"),
    )

    pn.template.FastListTemplate(
        site="Panel Chat Examples", title="StreamlitConverter", main=[main]
    ).servable()
