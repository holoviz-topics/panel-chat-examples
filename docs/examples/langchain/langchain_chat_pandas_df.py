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

from panel_chat_examples import EnvironmentWidgetBase

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


class Environment(EnvironmentWidgetBase):
    """Will be asking the user for the API Key if not set as environment variable"""

    OPENAI_API_KEY = param.String()


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
    environ: Environment = param.ClassSelector(class_=Environment, constant=True)

    def __init__(
        self, config: AgentConfig | None = None, environ: Environment | None = None
    ):
        if not config:
            config = AgentConfig()
        if not environ:
            environ = Environment()
        super().__init__(config=config, environ=environ)

    @param.depends("environ.OPENAI_API_KEY", on_init=True, watch=True)
    def _reset_llm(self):
        with param.edit_constant(self):
            if self.environ.OPENAI_API_KEY:
                self.llm = ChatOpenAI(
                    temperature=0,
                    model="gpt-3.5-turbo-0613",
                    api_key=self.environ.OPENAI_API_KEY,
                    streaming=True,
                )
            else:
                self.llm = None

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
            return dedent(
                """\
                Please provide your `OPENAI_API_KEY`, **upload a `.csv` file**
                and click the **send** button."""
            )
        if not self.llm:
            return "Please provide your `OPENAI_API_KEY`."
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
                dedent(
                    """You can ask me anything about the data. For example 'how many
                    species are there?'"""
                )
            )
            # We `send` instead of just `return` due to the bug
            # https://github.com/holoviz/panel/issues/5708
            instance.send(message, respond=False)
            return  # message

        if self.error_message:
            message = self.config._get_agent_message(self.error_message)
            instance.send(message, respond=False)
            return  # message

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
        instance.send(message, respond=False)
        return


state = AppState()

chat_interface = pn.chat.ChatInterface(
    widgets=[
        pn.widgets.FileInput(name="Upload"),
        pn.widgets.TextInput(name="Message", placeholder="Send a message"),
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

if state.environ.variables_not_set:
    layout.sidebar.append(state.environ)

layout.servable()
