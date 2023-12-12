"""
We use [OpenAI *Function Calling*](https://platform.openai.com/docs/guides/function-calling) and
[hvPlot](https://hvplot.holoviz.org/) to create an **advanced chatbot** that can create plots.
"""
import json
from pathlib import Path

import hvplot.pandas  # noqa
import matplotlib.pyplot as plt
import pandas as pd
import panel as pn
import plotly.io as pio
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
    return (
        pd.read_csv(ROOT / "ABC.csv", parse_dates=["date"])
        .sort_values(by="date", ascending=False)
        .head(100)
    )


DATA = _read_data()


@pn.cache
def _read_tool(name: str) -> dict:
    # See https://json-schema.org/learn/glossary
    with open(ROOT / f"tool_{name}.json", encoding="utf8") as file:
        return json.load(file)


def _set_theme():
    if THEME == "dark":
        pio.templates.default = "plotly_dark"
        plt.style.use(["default", "dark_background"])
    else:
        pio.templates.default = "plotly"
        plt.style.use(["default", "seaborn-v0_8"])


TOOLS_MAP = {"hvplot": _read_tool("hvplot"), "renderer": _read_tool("renderer")}
TOOLS = list(TOOLS_MAP.values())

HVPLOT_ARGUMENTS = (
    "`" + "`, `".join(TOOLS_MAP["hvplot"]["function"]["parameters"]["properties"]) + "`"
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

client = AsyncOpenAI()
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "assistant", "content": DATA_PROMPT},
]

tools_pane = pn.pane.JSON(
    object=TOOLS, depth=6, theme=JSON_THEME, name="Tools", sizing_mode="stretch_both"
)
tabs_layout = pn.Tabs(
    pn.Column(name="Plot"),
    tools_pane,
    pn.Column(name="Arguments"),
    sizing_mode="stretch_both",
    styles={"border-left": "2px solid var(--neutral-fill-active)"},
)


def powered_by():
    """Returns a component describing the frameworks powering the chat ui"""
    params = {"height": 50, "sizing_mode": "fixed", "margin": (10, 10)}
    return pn.Column(
        pn.Row(
            pn.pane.Image(CHAT_GPT_LOGO, **params),
            pn.pane.Image(HVPLOT_LOGO, **params),
        ),
        sizing_mode="stretch_width",
    )


def to_code(kwargs):
    """Returns the .hvplot code corresponding to the kwargs"""
    code = "data.hvplot("
    if kwargs:
        code += "\n"
    for key, value in kwargs.items():
        code += f"    {key}={repr(value)},\n"
    code += ")"
    return code


tool_kwargs = {"hvplot": {}, "renderer": {}}


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
    code = to_code(tool_kwargs["hvplot"])

    response = f"""
Try running

```python
{code}
```"""
    chat_interface.send(response, user="Assistant", respond=False)
    plot = DATA.hvplot(**tool_kwargs["hvplot"], responsive=True)
    _set_theme()
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


pn.extension(
    "plotly",
    raw_css=[CSS_TO_BE_UPSTREAMED_TO_PANEL],
)

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
        powered_by(),
        EXPLANATION,
    ],
    main=[component],
    main_layout=None,
    accent=ACCENT,
).servable()
