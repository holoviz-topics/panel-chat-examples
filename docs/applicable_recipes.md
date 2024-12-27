# Applicable Recipes
Demonstrates how to use Panel's chat components to achieve specific tasks with popular LLM packages.

## Langchain Chat With Pdf

Demonstrates how to use the `ChatInterface` to chat about a PDF using
OpenAI, [LangChain](https://python.langchain.com/docs/get_started/introduction) and
[Chroma](https://docs.trychroma.com/).

<video controls poster="../assets/thumbnails/langchain_chat_with_pdf.png" >
    <source src="../assets/videos/langchain_chat_with_pdf.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/langchain_chat_with_pdf.py' target='_blank'>langchain_chat_with_pdf.py</a></summary>

```python
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
```
</details>

## pydantic-ai Find City Agent

We use a [`pydantic-ai`](https://ai.pydantic.dev/) `Agent` to find the city that matches the users questions.
This example is derived from the [pydantic-model example](https://ai.pydantic.dev/examples/pydantic-model/).

<video controls poster="../assets/thumbnails/pydanticai_find_city_agent.png" >
    <source src="../assets/videos/pydanticai_find_city_agent.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/pydanticai_find_city_agent.py' target='_blank'>pydanticai_find_city_agent.py</a></summary>

```python
"""An example Agent UI to find a city.

Originally derived from https://ai.pydantic.dev/examples/pydantic-model/.
"""
import os
from typing import cast
import param
from pydantic import BaseModel
import urllib.parse
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName
import panel as pn

HEADER_CSS = """
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: linear-gradient(135deg, #0078d7, #00a1ff);
    color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
"""

SYSTEM_PROMPT = """"Find the city that best matches the question asked by the user and
explain why you chose that city."""


QUESTIONS = {
    "AI Capital of Europe": "Where is the AI capital of Europe?",
    "Gravel Cycling in Denmark": "Where do I find the best gravel cycling in Denmark",
    "Best food in Germany": "Where do I find the best food in Germany?",
}

class LocationModel(BaseModel):
    city: str
    country: str
    explanation: str

    @property
    def view(self, map_type="h", zoom: int = 8) -> str:
        query = f"{self.city}, {self.country}"
        encoded_query = urllib.parse.quote(query, safe="")
        src = f"https://maps.google.com/maps?q={encoded_query}&z={zoom}&t={map_type}&output=embed"
        return f"""
        <h1>{self.city}, {self.country}</h1>
        <p>{self.explanation}</p>
        <iframe width="100%" height="400px" src="{src}"
        frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
        """


model = cast(KnownModelName, os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o"))
agent = Agent(
    model,
    result_type=LocationModel,
    system_prompt=SYSTEM_PROMPT,
)


async def callback(contents):
    result = await agent.run(contents)
    return pn.pane.HTML(result.data.view, sizing_mode="stretch_width")


chat = pn.chat.ChatInterface(callback=callback, sizing_mode="stretch_both")


def send_chat_message(message):
    return lambda e: chat.send(message)


buttons = [
    pn.widgets.Button(
        name=key,
        on_click=send_chat_message(value),
    )
    for key, value in QUESTIONS.items()
]

header = pn.pane.HTML(
    "<h1 class='header'>City Finder<h1>",
    stylesheets=[HEADER_CSS],
    sizing_mode="stretch_width",
    margin=0,
)
footer = pn.pane.Markdown("Made with Panel, pydantic-ai and ❤️", align="center")

pn.Column(
    header,
    pn.Row(*buttons, align="center", margin=(10, 5, 25, 5)),
    chat,
    footer,
    sizing_mode="stretch_both",
).servable()
```
</details>


## Openai Chat With Hvplot

We use [OpenAI *Function Calling*](https://platform.openai.com/docs/guides/function-calling) and
[hvPlot](https://hvplot.holoviz.org/) to create an **advanced chatbot** that can create plots.

<video controls poster="../assets/thumbnails/openai_chat_with_hvplot.png" >
    <source src="../assets/videos/openai_chat_with_hvplot.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/openai_chat_with_hvplot.py' target='_blank'>openai_chat_with_hvplot.py</a></summary>

```python
"""
We use [OpenAI *Function Calling*](https://platform.openai.com/docs/guides/function-calling) and
[hvPlot](https://hvplot.holoviz.org/) to create an **advanced chatbot** that can create plots.
"""

import json
from pathlib import Path

import hvplot.pandas  # noqa
import pandas as pd
import panel as pn
from openai import AsyncOpenAI

ROOT = Path(__file__).parent

ACCENT = "#00A67E"
THEME = pn.config.theme
CSS_TO_BE_UPSTREAMED_TO_PANEL = """
a {color: var(--accent-fill-rest) !important;}
a:hover {color: var(--accent-fill-hover) !important;}
div.pn-wrapper{height: calc(100% - 25px)}
#sidebar {padding-left: 5px;background: var(--neutral-fill-active)}
"""

JSON_THEME = "light"

MODEL = "gpt-3.5-turbo-1106"
CHAT_GPT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png"
CHAT_GPT_URL = "https://chat.openai.com/"
HVPLOT_LOGO = "https://holoviz.org/assets/hvplot.png"
PANEL_LOGO = {
    "default": "https://panel.holoviz.org/_static/logo_horizontal_light_theme.png",
    "dark": "https://panel.holoviz.org/_static/logo_horizontal_dark_theme.png",
}
PANEL_URL = "https://panel.holoviz.org/index.html"

pn.chat.message.DEFAULT_AVATARS["assistant"] = HVPLOT_LOGO
pn.chat.ChatMessage.show_reaction_icons = False


@pn.cache
def _read_data():
    return pd.read_csv(
        "https://raw.githubusercontent.com/kirenz/datasets/master/gapminder.csv"
    )


DATA = _read_data()


@pn.cache
def _read_tool(name: str) -> dict:
    # See https://json-schema.org/learn/glossary
    with open(ROOT / f"tool_{name}.json", encoding="utf8") as file:
        return json.load(file)


TOOLS_MAP = {"hvplot": _read_tool("hvplot"), "renderer": _read_tool("renderer")}
TOOLS = list(TOOLS_MAP.values())

HVPLOT_ARGUMENTS = (
    "`"
    + "`, `".join(sorted(TOOLS_MAP["hvplot"]["function"]["parameters"]["properties"]))
    + "`"
)
EXPLANATION = f"""
## hvPlot by HoloViz
---

`hvPlot` is a high-level plotting library that that works almost in the same way as \
the well known `Pandas` `.plot` method.

The `.hvplot` method supports more data backends, plotting backends and provides more \
features than the `.plot` method.

## OpenAI GPT with Tools
---

We are using the OpenAI `{MODEL}` model with the `hvplot` and `renderer` *tools*.

You can refer to the following `hvplot` arguments

- {HVPLOT_ARGUMENTS}

and `renderer` arguments

- `backend`
"""

SYSTEM_PROMPT = """\
You are now a **Plotting Assistant** that helps users plot their data using `hvPlot` \
by `HoloViz`.\
"""

DATA_PROMPT = f"""\
Hi. Here is a description of your `data`.

The type is `{DATA.__class__.__name__}`. The `dtypes` are

```bash
{DATA.dtypes}
```"""

pn.extension(raw_css=[CSS_TO_BE_UPSTREAMED_TO_PANEL])

tools_pane = pn.pane.JSON(
    object=TOOLS, depth=6, theme=JSON_THEME, name="Tools", sizing_mode="stretch_both"
)
tabs_layout = pn.Tabs(
    pn.Column(name="Plot"),
    tools_pane,
    pn.Column(name="Arguments"),
    sizing_mode="stretch_both",
    styles={"border-left": "2px solid var(--neutral-fill-active)"},
    dynamic=True,
)


def _powered_by():
    """Returns a component describing the frameworks powering the chat ui"""
    params = {"height": 50, "sizing_mode": "fixed", "margin": (10, 10)}
    return pn.Column(
        pn.Row(
            pn.pane.Image(CHAT_GPT_LOGO, **params),
            pn.pane.Image(HVPLOT_LOGO, **params),
        ),
        sizing_mode="stretch_width",
    )


def _to_code(kwargs):
    """Returns the .hvplot code corresponding to the kwargs"""
    code = "data.hvplot("
    if kwargs:
        code += "\n"
    for key, value in kwargs.items():
        code += f"    {key}={repr(value)},\n"
    code += ")"
    return code


def _update_tool_kwargs(tool_calls, original_kwargs):
    if tool_calls:
        for tool_call in tool_calls:
            name = tool_call.function.name
            kwargs = json.loads(tool_call.function.arguments)
            if kwargs:
                # the llm does not always specify both the hvplot and renderer args
                # if not is specified its most natural to assume we continue with the
                # same args as before
                original_kwargs[name] = kwargs


def _clean_tool_kwargs(kwargs):
    # Sometimes the llm adds the backend argument to the hvplot arguments
    backend = kwargs["hvplot"].pop("backend", None)
    if backend and "backend" not in kwargs["renderer"]:
        # We add the backend argument to the renderer if none is specified
        kwargs["renderer"]["backend"] = backend
    # Use responsive by default
    if "responsive" not in kwargs:
        kwargs["hvplot"]["responsive"] = True


client = AsyncOpenAI()
tool_kwargs = {"hvplot": {}, "renderer": {}}


async def callback(
    contents: str, user: str, instance
):  # pylint: disable=unused-argument
    """Responds to a task"""
    messages = instance.serialize()
    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    _update_tool_kwargs(tool_calls, tool_kwargs)
    _clean_tool_kwargs(tool_kwargs)
    code = _to_code(tool_kwargs["hvplot"])

    response = f"Try running\n```python\n{code}\n```\n"
    chat_interface.send(response, user="Assistant", respond=False)
    plot = DATA.hvplot(**tool_kwargs["hvplot"])
    pane = pn.pane.HoloViews(
        object=plot, sizing_mode="stretch_both", name="Plot", **tool_kwargs["renderer"]
    )
    arguments = pn.pane.JSON(
        tool_kwargs,
        sizing_mode="stretch_both",
        depth=3,
        theme=JSON_THEME,
        name="Arguments",
    )
    tabs_layout[:] = [pane, tools_pane, arguments]


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    callback_exception="verbose",
)
chat_interface.send(
    SYSTEM_PROMPT,
    user="System",
    respond=False,
)
chat_interface.send(
    DATA_PROMPT,
    user="Assistant",
    respond=False,
)


component = pn.Row(chat_interface, tabs_layout, sizing_mode="stretch_both")

pn.template.FastListTemplate(
    title="Chat with hvPlot",
    sidebar=[
        _powered_by(),
        EXPLANATION,
    ],
    main=[component],
    main_layout=None,
    accent=ACCENT,
).servable()
```
</details>


## Openai Two Bots

Demonstrates how to use the `ChatInterface` to create two bots that chat with each
other.

Highlights:

- The user decides the callback user and avatar for the response.
- A system message is used to control the conversation flow.

<video controls poster="../assets/thumbnails/openai_two_bots.png" >
    <source src="../assets/videos/openai_two_bots.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/openai_two_bots.py' target='_blank'>openai_two_bots.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create two bots that chat with each
other.

Highlights:

- The user decides the callback user and avatar for the response.
- A system message is used to control the conversation flow.
"""

import panel as pn
from openai import AsyncOpenAI

pn.extension()


async def callback(
    contents: str,
    user: str,
    instance: pn.chat.ChatInterface,
):
    if user in ["User", "Happy Bot"]:
        callback_user = "Nerd Bot"
        callback_avatar = "🤓"
    elif user == "Nerd Bot":
        callback_user = "Happy Bot"
        callback_avatar = "😃"

    if len(instance.objects) % 6 == 0:  # stop at every 6 messages
        instance.send(
            "That's it for now! Thanks for chatting!", user="System", respond=False
        )
        return

    prompt = f"Reply profoundly about '{contents}', then follow up with a question."
    messages = [{"role": "user", "content": prompt}]
    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        max_tokens=250,
        temperature=0.1,
    )

    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield {"user": callback_user, "avatar": callback_avatar, "object": message}

    instance.respond()


aclient = AsyncOpenAI()
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    help_text="Enter a topic for the bots to discuss! Beware the token usage!",
)
chat_interface.servable()
```
</details>


## Langchain Chat With Pandas

Demonstrates how to use the `ChatInterface` and `PanelCallbackHandler` to create a
chatbot to talk to your Pandas DataFrame. This is heavily inspired by the
[LangChain `chat_pandas_df` Reference Example](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/chat_pandas_df.py).

<video controls poster="../assets/thumbnails/langchain_chat_with_pandas.png" >
    <source src="../assets/videos/langchain_chat_with_pandas.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/langchain_chat_with_pandas.py' target='_blank'>langchain_chat_with_pandas.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and `PanelCallbackHandler` to create a
chatbot to talk to your Pandas DataFrame. This is heavily inspired by the
[LangChain `chat_pandas_df` Reference Example](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/chat_pandas_df.py).
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pandas as pd
import panel as pn
import param
import requests
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

pn.extension("perspective")

PENGUINS_URL = (
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
)
PENGUINS_PATH = Path(__file__).parent / "penguins.csv"
if not PENGUINS_PATH.exists():
    response = requests.get(PENGUINS_URL)
    PENGUINS_PATH.write_text(response.text)

FILE_DOWNLOAD_STYLE = """
.bk-btn a {
    padding: 0px;
}
.bk-btn-group > button, .bk-input-group > button {
    font-size: small;
}
"""


class AgentConfig(param.Parameterized):
    """Configuration used for the Pandas Agent"""

    user = param.String("Pandas Agent")
    avatar = param.String("🐼")

    show_chain_of_thought = param.Boolean(default=False)

    def _get_agent_message(self, message: str) -> pn.chat.ChatMessage:
        return pn.chat.ChatMessage(message, user=self.user, avatar=self.avatar)


class AppState(param.Parameterized):
    data = param.DataFrame()

    llm = param.Parameter(constant=True)
    pandas_df_agent = param.Parameter(constant=True)

    config: AgentConfig = param.ClassSelector(class_=AgentConfig)

    def __init__(self, config: AgentConfig | None = None):
        if not config:
            config = AgentConfig()

        super().__init__(config=config)
        with param.edit_constant(self):
            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-3.5-turbo-0613",
                streaming=True,
            )

    @param.depends("llm", "data", on_init=True, watch=True)
    def _reset_pandas_df_agent(self):
        with param.edit_constant(self):
            if not self.error_message:
                self.pandas_df_agent = create_pandas_dataframe_agent(
                    self.llm,
                    self.data,
                    verbose=True,
                    agent_type=AgentType.OPENAI_FUNCTIONS,
                    handle_parsing_errors=True,
                )
            else:
                self.pandas_df_agent = None

    @property
    def error_message(self):
        if not self.llm and self.data is None:
            return "Please **upload a `.csv` file** and click the **send** button."
        if self.data is None:
            return "Please **upload a `.csv` file** and click the **send** button."
        return ""

    @property
    def welcome_message(self):
        return dedent(
            f"""
            I'm your <a href="\
            https://python.langchain.com/docs/integrations/toolkits/pandas" \
            target="_blank">LangChain Pandas DataFrame Agent</a>.

            I execute LLM generated Python code under the hood - this can be bad if
            the `llm` generated Python code is harmful. Use cautiously!

            {self.error_message}"""
        ).strip()

    async def callback(self, contents, user, instance):
        if isinstance(contents, pd.DataFrame):
            self.data = contents
            instance.active = 1
            message = self.config._get_agent_message(
                "You can ask me anything about the data. For example "
                "'how many species are there?'"
            )
            return message

        if self.error_message:
            message = self.config._get_agent_message(self.error_message)
            return message

        if self.config.show_chain_of_thought:
            langchain_callbacks = [
                pn.chat.langchain.PanelCallbackHandler(instance=instance)
            ]
        else:
            langchain_callbacks = []

        response = await self.pandas_df_agent.arun(
            contents, callbacks=langchain_callbacks
        )
        message = self.config._get_agent_message(response)
        return message


state = AppState()

chat_interface = pn.chat.ChatInterface(
    widgets=[
        pn.widgets.FileInput(name="Upload", accept=".csv"),
        pn.chat.ChatAreaInput(name="Message", placeholder="Send a message"),
    ],
    renderers=pn.pane.Perspective,
    callback=state.callback,
    callback_exception="verbose",
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    min_height=400,
)
chat_interface.send(
    state.welcome_message,
    user=state.config.user,
    avatar=state.config.avatar,
    respond=False,
)

download_button = pn.widgets.FileDownload(
    PENGUINS_PATH,
    button_type="primary",
    button_style="outline",
    height=30,
    width=335,
    stylesheets=[FILE_DOWNLOAD_STYLE],
)

layout = pn.template.MaterialTemplate(
    title="🦜 LangChain - Chat with Pandas DataFrame",
    main=[chat_interface],
    sidebar=[
        download_button,
        "#### Agent Settings",
        state.config.param.show_chain_of_thought,
    ],
)

layout.servable()
```
</details>


## Openai Images Dall E

Use the OpenAI API to generate images using the DALL·E model.

<video controls poster="../assets/thumbnails/openai_images_dall_e.png" >
    <source src="../assets/videos/openai_images_dall_e.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/applicable_recipes/openai_images_dall_e.py' target='_blank'>openai_images_dall_e.py</a></summary>

```python
"""
Use the OpenAI API to generate images using the DALL·E model.
"""

import panel as pn
from openai import AsyncOpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        # use api_key_input.value if set, otherwise use OPENAI_API_KEY
        aclient.api_key = api_key_input.value

    response = await aclient.images.generate(
        model=model_buttons.value,
        prompt=contents,
        n=n_images_slider.value,
        size=size_buttons.value,
    )

    image_panes = [
        (str(i), pn.pane.Image(data.url)) for i, data in enumerate(response.data)
    ]
    return pn.Tabs(*image_panes) if len(image_panes) > 1 else image_panes[0][1]


def update_model_params(model):
    if model == "dall-e-2":
        size_buttons.param.update(
            options=["256x256", "512x512", "1024x1024"],
            value="256x256",
        )
        n_images_slider.param.update(
            start=1,
            end=10,
            value=1,
        )
    else:
        size_buttons.param.update(
            options=["1024x1024", "1024x1792", "1792x1024"],
            value="1024x1024",
        )
        n_images_slider.param.update(
            start=1,
            end=1,
            value=1,
        )


aclient = AsyncOpenAI()
api_key_input = pn.widgets.PasswordInput(
    placeholder="sk-... uses $OPENAI_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
model_buttons = pn.widgets.RadioButtonGroup(
    options=["dall-e-2", "dall-e-3"],
    value="dall-e-2",
    name="Model",
    sizing_mode="stretch_width",
)
size_buttons = pn.widgets.RadioButtonGroup(
    options=["256x256", "512x512", "1024x1024"],
    name="Size",
    sizing_mode="stretch_width",
)
n_images_slider = pn.widgets.IntSlider(
    start=1, end=10, value=1, name="Number of images"
)
pn.bind(update_model_params, model_buttons, watch=True)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="DALL·E",
    help_text="Send a message to get a reply from DALL·E!",
)
template = pn.template.BootstrapTemplate(
    title="OpenAI DALL·E",
    header_background="#212121",
    main=[chat_interface],
    header=[api_key_input],
    sidebar=[model_buttons, size_buttons, n_images_slider],
)
template.servable()
```
</details>
