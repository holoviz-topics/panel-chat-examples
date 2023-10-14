# Basics

## Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

The chatbot Assistant echoes back the message entered by the User.

<video controls poster="../assets/thumbnails/basic_chat.png" >
    <source src="../assets/videos/basic_chat.webm" type="video/webm"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/basics/basic_chat.py' target='_blank'>basic_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

The chatbot Assistant echoes back the message entered by the User.
"""

import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


## Echo Stream Async

Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.

<video controls poster="../assets/thumbnails/basic_echo_stream_async.png" >
    <source src="../assets/videos/basic_echo_stream_async.webm" type="video/webm"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/basics/basic_echo_stream_async.py' target='_blank'>basic_echo_stream_async.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.
"""


from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    await sleep(1)
    message = ""
    for char in "Echoing User: " + contents:
        await sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


## Streaming Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to stream back
responses.

The chatbot Assistant echoes back the message entered by the User in a *streaming*
fashion.

<video controls poster="../assets/thumbnails/basic_streaming_chat.png" >
    <source src="../assets/videos/basic_streaming_chat.webm" type="video/webm"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/basics/basic_streaming_chat.py' target='_blank'>basic_streaming_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to stream back
responses.

The chatbot Assistant echoes back the message entered by the User in a *streaming*
fashion.
"""


from time import sleep

import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    sleep(1)
    message = ""
    for char in f"Echoing {user}: {contents}":
        sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>
