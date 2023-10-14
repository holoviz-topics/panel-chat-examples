# Components

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