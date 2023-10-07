"""The `EnvironmentWidgetBase` class enables you to manage variable values from a
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

pn.extension()


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
