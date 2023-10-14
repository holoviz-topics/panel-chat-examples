# Openai

## Async Chat

Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's with async/await.

<video controls poster="../assets/thumbnails/openai_async_chat.png" >
    <source src="../assets/videos/openai_async_chat.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_async_chat.py' target='_blank'>openai_async_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's with async/await.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
```
</details>


## Authentication

Demonstrates how to use the `ChatInterface` widget with authentication for
OpenAI's API.

<video controls poster="../assets/thumbnails/openai_authentication.png" >
    <source src="../assets/videos/openai_authentication.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_authentication.py' target='_blank'>openai_authentication.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` widget with authentication for
OpenAI's API.
"""

import os

import openai
import panel as pn

SYSTEM_KWARGS = dict(
    user="System",
    respond=False,
)

pn.extension()


def add_key_to_env(key):
    if not key.startswith("sk-"):
        chat_interface.send("Please enter a valid OpenAI key!", **SYSTEM_KWARGS)
        return

    chat_interface.send(
        "Your OpenAI key has been set. Feel free to minimize the sidebar.",
        **SYSTEM_KWARGS,
    )
    chat_interface.disabled = False


key_input = pn.widgets.PasswordInput(placeholder="sk-...", name="OpenAI Key")
pn.bind(add_key_to_env, key=key_input, watch=True)


async def callback(
    contents: str,
    user: str,
    instance: pn.widgets.ChatInterface,
):
    if "OPENAI_API_KEY" not in os.environ:
        yield "Please first set your OpenAI key in the sidebar!"
        return

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
        api_key=key_input.value,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, disabled=True)
chat_interface.send(
    "First enter your OpenAI key in the sidebar, then send a message!", **SYSTEM_KWARGS
)

pn.template.MaterialTemplate(
    title="OpenAI ChatInterface with authentication",
    sidebar=[key_input],
    main=[chat_interface],
).servable()
```
</details>


## Chat

Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's API.

<video controls poster="../assets/thumbnails/openai_chat.png" >
    <source src="../assets/videos/openai_chat.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_chat.py' target='_blank'>openai_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create a chatbot using
OpenAI's API.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
```
</details>


## Hvplot

Demonstrates how to use the `ChatInterface` to create a chatbot
that can generate plots of your data using [hvplot](https://hvplot.holoviz.org/).

<video controls poster="../assets/thumbnails/openai_hvplot.png" >
    <source src="../assets/videos/openai_hvplot.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_hvplot.py' target='_blank'>openai_hvplot.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create a chatbot
that can generate plots of your data using [hvplot](https://hvplot.holoviz.org/).
"""

import re
from typing import Union

import openai
import pandas as pd
import panel as pn
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

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        temperature=0,
        max_tokens=500,
        stream=True,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield {"user": "ChatGPT", "value": message}


async def respond_with_executor(code: str):
    code_block = f"```python\n{code}\n```"
    global df
    context = {"df": df}
    plot = exec_with_return(code=code, global_context=context)
    return {
        "user": "Executor",
        "value": pn.Tabs(
            ("Plot", plot),
            ("Code", code_block),
        ),
    }


async def callback(
    contents: Union[str, pd.DataFrame],
    name: str,
    instance: pn.widgets.ChatInterface,
):
    if not isinstance(contents, (str, pd.DataFrame)):
        return

    if name == "User":
        async for chunk in respond_with_openai(contents):
            yield chunk
        instance.respond()
    elif CODE_REGEX.search(contents):
        yield await respond_with_executor(CODE_REGEX.search(contents).group(1))


chat_interface = pn.widgets.ChatInterface(
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
```
</details>


## Image Generation

Demonstrates how to use the `ChatInterface` to create images using
OpenAI's [DALL-E API](https://platform.openai.com/docs/guides/images/image-generation).

<video controls poster="../assets/thumbnails/openai_image_generation.png" >
    <source src="../assets/videos/openai_image_generation.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_image_generation.py' target='_blank'>openai_image_generation.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create images using
OpenAI's [DALL-E API](https://platform.openai.com/docs/guides/images/image-generation).
"""

import openai
import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.Image.create(prompt=contents, n=1, size="256x256")
    image_url = response["data"][0]["url"]
    return pn.pane.Image(image_url, width=256, height=256)


chat_interface = pn.widgets.ChatInterface(
    callback=callback, callback_user="DALL-E", placeholder_text="Generating..."
)
chat_interface.send(
    "Create an image by providing a prompt!", user="System", respond=False
)
chat_interface.servable()
```
</details>


## Two Bots

Demonstrates how to use the `ChatInterface` to create two bots that chat with each
other.

<video controls poster="../assets/thumbnails/openai_two_bots.png" >
    <source src="../assets/videos/openai_two_bots.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/openai/openai_two_bots.py' target='_blank'>openai_two_bots.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` to create two bots that chat with each
other.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(
    contents: str,
    user: str,
    instance: pn.widgets.ChatInterface,
):
    if user in ["User", "Happy Bot"]:
        callback_user = "Nerd Bot"
        callback_avatar = "🤓"
    elif user == "Nerd Bot":
        callback_user = "Happy Bot"
        callback_avatar = "😃"

    prompt = f"Think profoundly about {contents}, then ask a question."
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=250,
        temperature=0.1,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield {"user": callback_user, "avatar": callback_avatar, "value": message}

    if len(instance.value) % 6 == 0:  # stop at every 6 messages
        instance.send(
            "That's it for now! Thanks for chatting!", user="System", respond=False
        )
        return
    instance.respond()


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a topic for the bots to discuss! Beware the token usage!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>