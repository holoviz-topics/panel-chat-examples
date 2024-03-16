# Feature

## Feature Chained Response

Demonstrates how to chain responses from a single message in the callback.

Highlight:

- The `respond` parameter in the `send` method is used to chain responses.
- It's also possible to use `respond` as a method to chain responses.

<video controls poster="../assets/thumbnails/feature_chained_response.png" >
    <source src="../assets/videos/feature_chained_response.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_chained_response.py' target='_blank'>feature_chained_response.py</a></summary>

```python
"""
Demonstrates how to chain responses from a single message in the callback.

Highlight:

- The `respond` parameter in the `send` method is used to chain responses.
- It's also possible to use `respond` as a method to chain responses.
"""

from asyncio import sleep

import panel as pn

pn.extension()

PERSON_1 = "Happy User"
PERSON_2 = "Excited User"
PERSON_3 = "Passionate User"


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(2)
    if user == "User":
        instance.send(
            f"Hey, {PERSON_2}! Did you hear the user?",
            user=PERSON_1,
            avatar="😊",
            respond=True,  # This is the default, but it's here for clarity
        )
    elif user == PERSON_1:
        user_message = instance.objects[-2]
        user_contents = user_message.object
        yield pn.chat.ChatMessage(
            f'Yeah, they said "{user_contents}"! Did you also hear {PERSON_3}?',
            user=PERSON_2,
            avatar="😄",
        )
        instance.respond()
    elif user == PERSON_2:
        instance.send(
            f"Yup, I heard!",
            user=PERSON_3,
            avatar="😆",
            respond=False,
        )


chat_interface = pn.chat.ChatInterface(
    help_text="Send a message to start the conversation!", callback=callback
)
chat_interface.servable()
```
</details>

Live Apps: <a href='../pyodide/feature_chained_response.html' target='_blank' title='The app is running entirely in the browser powered by Pyodide'>Pyodide</a>

## Feature Control Callback Response

Demonstrates how to precisely control the callback response.

Highlights:

- Use a placeholder text to display a message while waiting for the response.
- Use a placeholder threshold to control when the placeholder text is displayed.
- Use send instead of stream/yield/return to keep the placeholder text while still sending a message, ensuring respond=False to avoid a recursive loop.
- Use yield to continuously update the response message.
- Use pn.chat.ChatMessage or dict to send a message with a custom user and avatar.

<video controls poster="../assets/thumbnails/feature_control_callback_response.png" >
    <source src="../assets/videos/feature_control_callback_response.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_control_callback_response.py' target='_blank'>feature_control_callback_response.py</a></summary>

```python
"""
Demonstrates how to precisely control the callback response.

Highlights:

- Use a placeholder text to display a message while waiting for the response.
- Use a placeholder threshold to control when the placeholder text is displayed.
- Use send instead of stream/yield/return to keep the placeholder text while still sending a message, ensuring respond=False to avoid a recursive loop.
- Use yield to continuously update the response message.
- Use pn.chat.ChatMessage or dict to send a message with a custom user and avatar.
"""

from asyncio import sleep
from random import choice

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(0.5)
    # use send instead of stream/yield/return to keep the placeholder text
    # while still sending a message; ensure respond=False to avoid a recursive loop
    instance.send(
        "Let me flip the coin for you...", user="Game Master", avatar="🎲", respond=False
    )
    await sleep(1)

    characters = "/|\\_"
    index = 0
    for _ in range(0, 28):
        index = (index + 1) % len(characters)
        # use yield to continuously update the response message
        # use pn.chat.ChatMessage to send a message with a custom user and avatar
        yield pn.chat.ChatMessage("\r" + characters[index], user="Coin", avatar="🪙")
        await sleep(0.005)

    result = choice(["heads", "tails"])
    if result in contents.lower():
        # equivalently, use a dict instead of a pn.chat.ChatMessage
        yield {"object": f"Woohoo, {result}! You win!", "user": "Coin", "avatar": "🎲"}
    else:
        yield {"object": f"Aw, got {result}. Try again!", "user": "Coin", "avatar": "🎲"}


chat_interface = pn.chat.ChatInterface(
    widgets=[
        pn.widgets.RadioButtonGroup(
            options=["Heads!", "Tails!"], button_type="primary", button_style="outline"
        )
    ],
    callback=callback,
    help_text="Select heads or tails, then click send!",
    placeholder_text="Waiting for the result...",
    placeholder_threshold=0.1,
)
chat_interface.servable()
```
</details>


## Feature Custom Input Widgets

Demonstrates how to use the `ChatInterface` and custom widgets,
like `ChatAreaInput` and `FileInput`, to create a chatbot that counts
the number of lines in a message or file.

Highlights:

- The `ChatAreaInput` and `FileInput` widgets are used to create a custom
chatbot that counts the number of lines in a message or file.
- The `callback` function is used to count the number of lines in the message
or file and return the result to the User.

<video controls poster="../assets/thumbnails/feature_custom_input_widgets.png" >
    <source src="../assets/videos/feature_custom_input_widgets.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_custom_input_widgets.py' target='_blank'>feature_custom_input_widgets.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and custom widgets,
like `ChatAreaInput` and `FileInput`, to create a chatbot that counts
the number of lines in a message or file.

Highlights:

- The `ChatAreaInput` and `FileInput` widgets are used to create a custom
    chatbot that counts the number of lines in a message or file.
- The `callback` function is used to count the number of lines in the message
    or file and return the result to the User.
"""

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    lines = contents.strip().count("\n")
    message = f"This snippet has {lines + 1} lines."
    return message


chat_input = pn.chat.ChatAreaInput(placeholder="Send a message")
file_input = pn.widgets.FileInput(accept=".py")
chat_interface = pn.chat.ChatInterface(
    callback=callback, widgets=[chat_input, file_input]
)
chat_interface.send(
    "Enter a message in the ChatAreaInput below to count how many lines there is, "
    "or upload a Python file to count the number of lines in the file.",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


## Feature Delayed Placeholder

Demonstrates how to delay the display of the placeholder.

Highlights:

- The `placeholder_threshold` parameter is used to delay the display of the placeholder.
If the response time is less than the threshold, the placeholder will not be displayed.
- The `placeholder_text` parameter is used to customize the placeholder text.

<video controls poster="../assets/thumbnails/feature_delayed_placeholder.png" >
    <source src="../assets/videos/feature_delayed_placeholder.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_delayed_placeholder.py' target='_blank'>feature_delayed_placeholder.py</a></summary>

```python
"""
Demonstrates how to delay the display of the placeholder.

Highlights:

- The `placeholder_threshold` parameter is used to delay the display of the placeholder.
    If the response time is less than the threshold, the placeholder will not be displayed.
- The `placeholder_text` parameter is used to customize the placeholder text.
"""

from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    try:
        seconds = float(contents)
        if 0 < seconds < 10:
            await sleep(seconds)
            return f"Slept {contents} seconds!"
        else:
            return "Please enter a number between 1 and 9!"
    except ValueError:
        return "Please enter a number!"


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    placeholder_threshold=2,
    placeholder_text="Waiting for reply...",
)
chat_interface.send(
    "Send a number to make the system sleep between 1 and 9 seconds!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>

Live Apps: <a href='../pyodide/feature_delayed_placeholder.html' target='_blank' title='The app is running entirely in the browser powered by Pyodide'>Pyodide</a>

## Feature Echo Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

Highlights:

- The `ChatInterface` and a `callback` function are used to create a
chatbot that echoes back the message entered by the User.
- The `help_text` parameter is used to provide instructions to the User.

<video controls poster="../assets/thumbnails/feature_echo_chat.png" >
    <source src="../assets/videos/feature_echo_chat.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_echo_chat.py' target='_blank'>feature_echo_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

Highlights:

- The `ChatInterface` and a `callback` function are used to create a
    chatbot that echoes back the message entered by the User.
- The `help_text` parameter is used to provide instructions to the User.
"""

import panel as pn

pn.extension()


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    help_text="Enter a message in the TextInput below and receive an echo!",
)
chat_interface.servable()
```
</details>


## Feature Slim Interface

Demonstrates how to create a slim `ChatInterface` that fits in the sidebar.

Highlights:

- The `ChatInterface` is placed in the sidebar.
- Set `show_*` parameters to `False` to hide the respective buttons.
- Use `message_params` to customize the appearance of each chat messages.

<video controls poster="../assets/thumbnails/feature_slim_interface.png" >
    <source src="../assets/videos/feature_slim_interface.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_slim_interface.py' target='_blank'>feature_slim_interface.py</a></summary>

```python
"""
Demonstrates how to create a slim `ChatInterface` that fits in the sidebar.

Highlights:

- The `ChatInterface` is placed in the sidebar.
- Set `show_*` parameters to `False` to hide the respective buttons.
- Use `message_params` to customize the appearance of each chat messages.
"""
import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    show_send=False,
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    show_avatar=False,
    show_timestamp=False,
    show_button_name=False,
    show_reaction_icons=False,
    sizing_mode="stretch_width",
    height=700,
    message_params={
        "stylesheets": [
            """
            .message {
                font-size: 1em;
            }
            .name {
                font-size: 0.9em;
            }
            .timestamp {
                font-size: 0.9em;
            }
            """
        ]
    },
)

main = """
We've put a *slim* `ChatInterface` in the sidebar. In the main area you
could add the object you are chatting about
"""

pn.template.FastListTemplate(
    main=[main],
    sidebar=[chat_interface],
    sidebar_width=500,
).servable()
```
</details>

Live Apps: <a href='../pyodide/feature_slim_interface.html' target='_blank' title='The app is running entirely in the browser powered by Pyodide'>Pyodide</a>

## Feature Stream Echo Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.

Highlights:

- The function is defined as `async` and uses `yield` to stream back responses.
- Initialize `message` first to gather the characters and then `yield` it;
without it, only one letter would be displayed at a time.

<video controls poster="../assets/thumbnails/feature_stream_echo_chat.png" >
    <source src="../assets/videos/feature_stream_echo_chat.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/feature/feature_stream_echo_chat.py' target='_blank'>feature_stream_echo_chat.py</a></summary>

```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.

Highlights:

- The function is defined as `async` and uses `yield` to stream back responses.
- Initialize `message` first to gather the characters and then `yield` it;
    without it, only one letter would be displayed at a time.
"""


from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(1)
    message = ""
    for char in "Echoing User: " + contents:
        await sleep(0.05)
        message += char
        yield message


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>
