# Components

## Chat Input

The `ChatInput` widget is a combination of a `TextInput` widget and a `Button`.
When the input is submitted the `TextInput` widget is cleared and ready to accept
a new input.

If you need a `ChatInput` widget you can copy the code from
[here](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/components/chat_input.py).

<video controls poster="../assets/thumbnails/component_chat_input.png" >
    <source src="../assets/videos/component_chat_input.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/components/component_chat_input.py' target='_blank'>component_chat_input.py</a></summary>

```python
"""
The `ChatInput` widget is a combination of a `TextInput` widget and a `Button`.
When the input is submitted the `TextInput` widget is cleared and ready to accept
a new input.

If you need a `ChatInput` widget you can copy the code from
[here](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/components/chat_input.py).
"""
import panel as pn

from panel_chat_examples.components import ChatInput

pn.extension(design="material")

chat_input = ChatInput(placeholder="Say something")


def message(prompt):
    if not prompt:
        return ""
    return f"User has sent the following prompt: **{prompt}**"


pn.Column(pn.bind(message, chat_input.param.value), chat_input, margin=25).servable()
```
</details>


## Environment Widget

The [`EnvironmentWidgetBase`](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/_environment_widget.py)
class enables you to manage variable values from a combination of custom values,
environment variables and user input.

Its very useful when you don't have the resources to provide API keys for services
like OpenAI. It will determine which variables have not been set as environment
variables and ask the user for them.

<video controls poster="../assets/thumbnails/component_environment_widget.png" >
    <source src="../assets/videos/component_environment_widget.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/components/component_environment_widget.py' target='_blank'>component_environment_widget.py</a></summary>

```python
"""
The [`EnvironmentWidgetBase`](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/_environment_widget.py)
class enables you to manage variable values from a combination of custom values,
environment variables and user input.

Its very useful when you don't have the resources to provide API keys for services
like OpenAI. It will determine which variables have not been set as environment
variables and ask the user for them.
"""
# Longer term we should try to get this widget included in Panel
import panel as pn
import param

from panel_chat_examples import EnvironmentWidgetBase

pn.extension(design="material")


class EnvironmentWidget(EnvironmentWidgetBase):
    """An example Environment Widget for managing environment variables"""

    OPENAI_API_KEY = param.String(doc="A key for the OpenAI api")
    WEAVIATE_API_KEY = param.String(doc="A key for the Weaviate api")
    LANGCHAIN_API_KEY = param.String(doc="A key for the LangChain api")


environment = EnvironmentWidget(max_width=1000)
pn.template.FastListTemplate(
    title="Environment Widget",
    sidebar=[environment],
    main=[
        __doc__,
        pn.Column(
            environment.param.variables_set,
            environment.param.variables_not_set,
        ),
    ],
).servable()
```
</details>


## Status

The `Status` *indicator* can report progress in steps and with
detailed context.

If you need a `Status` widget you can copy the code from
[here](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/components/chat_input/components/status.py).

<video controls poster="../assets/thumbnails/component_status.png" >
    <source src="../assets/videos/component_status.mp4" type="video/mp4"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/components/component_status.py' target='_blank'>component_status.py</a></summary>

```python
"""
The `Status` *indicator* can report progress in steps and with
detailed context.

If you need a `Status` widget you can copy the code from
[here](https://github.com/holoviz-topics/panel-chat-examples/blob/main/panel_chat_examples/components/chat_input/components/status.py).
"""
import time

import panel as pn

from panel_chat_examples.components import Status

status = Status("Downloading data...", sizing_mode="stretch_width")


def run(_):
    with status.report() as progress:
        status.collapsed = False
        progress("Searching for data...")
        time.sleep(1.5)
        progress("Downloading data...")
        time.sleep(1.5)
        progress("Validating data...")
        time.sleep(1.5)
        status.collapsed = True


run_button = pn.widgets.Button(
    name="Run", on_click=run, button_type="primary", button_style="outline"
)

pn.Column(
    status,
    run_button,
).servable()
```
</details>
