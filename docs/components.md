# Components

## Environment Widget

The `EnvironmentWidgetBase` class enables you to manage variable values from a
combination of

- custom variable values
- environment variables
- user input.

(listed by order of precedence)

You can use it as a drop in replacement for `os.environ`.

For example you might not have the resources to provide an `OPENAI_API_KEY`,
`WEAVIATE_API_KEY` or `LANGCHAIN_API_KEY`. In that case you would would like to ask the
user for it.

Inherit from this widget to create your own custom `EnvironmentWidget`.

<video controls poster="../assets/thumbnails/component_environment_widget.png" >
    <source src="../assets/videos/component_environment_widget.webm" type="video/webm"
    style="max-height: 400px; max-width: 600px;">
    Your browser does not support the video tag.
</video>



<details>

<summary>Source code for <a href='../examples/components/component_environment_widget.py' target='_blank'>component_environment_widget.py</a></summary>

```python
"""
The `EnvironmentWidgetBase` class enables you to manage variable values from a
combination of

- custom variable values
- environment variables
- user input.

(listed by order of precedence)

You can use it as a drop in replacement for `os.environ`.

For example you might not have the resources to provide an `OPENAI_API_KEY`,
`WEAVIATE_API_KEY` or `LANGCHAIN_API_KEY`. In that case you would would like to ask the
user for it.

Inherit from this widget to create your own custom `EnvironmentWidget`.
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
