"""
Demonstrates how to use the `ChatInterface` to create a chatbot
that can generate plots of your data using [hvplot](https://hvplot.holoviz.org/).
"""

import re
from typing import Union

import pandas as pd
import panel as pn
from openai import AsyncOpenAI
from panel.io.mime_render import exec_with_return

DATAFRAME_PROMPT = """
    Here are the columns in your DataFrame: {columns}.
    Create a plot with hvplot that highlights an interesting
    relationship between the columns with hvplot groupby kwarg.
"""

CODE_REGEX = re.compile(r"```\s?python(.*?)```", re.DOTALL)


def _clean(df: pd.DataFrame):
    df.columns = [column.strip() for column in df.columns]
    df = df.head(100)
    return df


async def respond_with_openai(contents: Union[pd.DataFrame, str]):
    # extract the DataFrame
    if isinstance(contents, pd.DataFrame):
        global df
        df = _clean(contents)
        columns = contents.columns
        message = DATAFRAME_PROMPT.format(columns=columns)
    else:
        message = contents

    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        temperature=0,
        max_tokens=500,
        stream=True,
    )
    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield {"user": "ChatGPT", "object": message}


async def respond_with_executor(code: str):
    code_block = f"```python\n{code}\n```"
    global df
    context = {"df": df}
    plot = exec_with_return(code=code, global_context=context)
    return {
        "user": "Executor",
        "object": pn.Tabs(
            ("Plot", plot),
            ("Code", code_block),
        ),
    }


async def callback(
    contents: Union[str, pd.DataFrame],
    name: str,
    instance: pn.chat.ChatInterface,
):
    if not isinstance(contents, (str, pd.DataFrame)):
        return

    if name == "User":
        async for chunk in respond_with_openai(contents):
            yield chunk
        instance.respond()
    elif CODE_REGEX.search(contents):
        yield await respond_with_executor(CODE_REGEX.search(contents).group(1))


aclient = AsyncOpenAI()
chat_interface = pn.chat.ChatInterface(
    widgets=[pn.widgets.FileInput(name="Upload"), pn.widgets.TextInput(name="Message")],
    callback=callback,
)
# ruff: noqa: E501
chat_interface.send(
    """Send a message to ChatGPT or upload a small CSV file to get started!

<a href="data:text/csv;base64,ZGF0ZSxjYXRlZ29yeSxxdWFudGl0eSxwcmljZQoyMDIxLTAxLTAxLGVsZWN0cm9uaWNzLDIsNTAwICAKMjAyMS0wMS0wMixjbG90aGluZywxLDUwCjIwMjEtMDEtMDMsaG9tZSBnb29kcyw0LDIwMAoyMDIxLTAxLTA0LGVsZWN0cm9uaWNzLDEsMTAwMAoyMDIxLTAxLTA1LGdyb2NlcmllcywzLDc1CjIwMjEtMDEtMDYsY2xvdGhpbmcsMiwxMDAKMjAyMS0wMS0wNyxob21lIGdvb2RzLDMsMTUwCjIwMjEtMDEtMDgsZWxlY3Ryb25pY3MsNCwyMDAwCjIwMjEtMDEtMDksZ3JvY2VyaWVzLDIsNTAKMjAyMS0wMS0xMCxlbGVjdHJvbmljcywzLDE1MDA=" download="example.csv">example.csv</a>
""",
    user="System",
    respond=False,
)
chat_interface.servable()
