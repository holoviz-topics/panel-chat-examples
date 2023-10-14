# Features

## Chained Response

Demonstrates how to chain responses in a ChatInterface.

<video controls poster="..\assets\thumbnails\feature_chained_response.png" >
    <source src="..\assets\videos\feature_chained_response.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='..\examples\features\feature_chained_response.py' target='_blank'>feature_chained_response.py</a></summary>

```python
"""
Demonstrates how to chain responses in a ChatInterface.
"""

from time import sleep

import panel as pn

pn.extension(design="material")

ARM_BOT = "Arm Bot"
LEG_BOT = "Leg Bot"


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    sleep(1)
    if user == "User":
        yield {
            "user": ARM_BOT,
            "avatar": "🦾",
            "value": f"Hey, {LEG_BOT}! Did you hear the user?",
        }
        instance.respond()
    elif user == ARM_BOT:
        user_entry = instance.value[-2]
        user_contents = user_entry.value
        yield {
            "user": LEG_BOT,
            "avatar": "🦿",
            "value": f'Yeah! They said "{user_contents}".',
        }


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send("Send a message!", user="System", respond=False)
chat_interface.servable()
```
</details>


## Delayed Placeholder

Demonstrates how to delay the display of the placeholder.

<video controls poster="..\assets\thumbnails\feature_delayed_placeholder.png" >
    <source src="..\assets\videos\feature_delayed_placeholder.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='..\examples\features\feature_delayed_placeholder.py' target='_blank'>feature_delayed_placeholder.py</a></summary>

```python
"""
Demonstrates how to delay the display of the placeholder.
"""

from asyncio import sleep

import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    try:
        seconds = float(contents)
        if 0 < seconds < 10:
            await sleep(seconds)
            return f"Slept {contents} seconds!"
        else:
            return "Please enter a number between 1 and 9!"
    except ValueError:
        return "Please enter a number!"


chat_interface = pn.widgets.ChatInterface(
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


## Replace Response

Demonstrates how to update the response of a ChatInterface widget.

<video controls poster="..\assets\thumbnails\feature_replace_response.png" >
    <source src="..\assets\videos\feature_replace_response.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='..\examples\features\feature_replace_response.py' target='_blank'>feature_replace_response.py</a></summary>

```python
"""
Demonstrates how to update the response of a ChatInterface widget.
"""

from asyncio import sleep
from random import choice

import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    yield "Let me flip the coin for you..."
    await sleep(1)

    characters = "/|\\_"
    index = 0
    for _ in range(0, 28):
        index = (index + 1) % len(characters)
        yield "\r" + characters[index]
        await sleep(0.005)

    result = choice(["heads", "tails"])
    if result in contents.lower():
        yield f"Woohoo, {result}! You win!"
    else:
        yield f"Aw, got {result}. Try again!"


chat_interface = pn.widgets.ChatInterface(
    widgets=[
        pn.widgets.RadioButtonGroup(
            options=["Heads!", "Tails!"], button_type="primary", button_style="outline"
        )
    ],
    callback=callback,
    callback_user="Game Master",
)
chat_interface.send(
    "Select heads or tails, then click send!", user="System", respond=False
)
chat_interface.servable()
```
</details>


## Slim Interface

Demonstrates how to create a slim ChatInterface widget that fits in the sidebar.

<video controls poster="..\assets\thumbnails\feature_slim_interface.png" >
    <source src="..\assets\videos\feature_slim_interface.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='..\examples\features\feature_slim_interface.py' target='_blank'>feature_slim_interface.py</a></summary>

```python
"""
Demonstrates how to create a slim ChatInterface widget that fits in the sidebar.
"""
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.widgets.ChatInterface(
    callback=callback,
    show_send=False,
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    show_button_name=False,
    sizing_mode="stretch_both",
    min_height=200,
    width=475,
)
chat_interface.send("Send a message and hear an echo!", user="System", respond=False)

pn.template.FastListTemplate(
    main=[
        """We've put a *slim* `ChatInterface` in the sidebar. In the main area you \
could add the object you are chatting about"""
    ],
    sidebar=[chat_interface],
    sidebar_width=500,
).servable()
```
</details>