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
