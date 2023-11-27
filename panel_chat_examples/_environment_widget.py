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
# But for now it can help us deploy applications to Hugging Face etc without paying for
# api keys
import os

import panel as pn
import param

WIDGET_MAX_WIDTH = 600


class VariableNotFound(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"The __key '{key}' is not a supported variable!")


class EnvironmentWidgetBase(pn.viewable.Viewer):
    """The `EnvironmentWidgetBase` class enables you to manage variable values from a
    combination of

    - custom variable values
    - environment variables
    - user input.

    (listed by order of precedence)

    You can use it as a drop in replacement for `os.environ`.

    For example you might not have the resources to provide an `OPENAI_API_KEY`,
    `WEAVIATE_API_KEY` or `LANGCHAIN_API_KEY`. In that case you would would like to ask
    the user for it.

    >>> class EnvironmentWidget(EnvironmentWidgetBase):
    ...     OPENAI_API_KEY = param.String(doc="A key for the OpenAI api")
    ...     WEAVIATE_API_KEY = param.String(doc="A key for the Weaviate api")
    ...     LANGCHAIN_API_KEY = param.String(doc="A key for the LangChain api")"""

    message_alert: str = param.String(
        (
            "**Protect your secrets!** Make sure you trust "
            "the publisher of this app before entering your secrets."
        ),
        doc="""An Alert message to display to the user to make them handle their secrets
        securely. If not set, then no Alert is displayed""",
    )

    variables_not_set = param.List(
        constant=True, doc="A list of the variables with no value"
    )
    variables_set = param.List(
        constant=True, doc="A list of the variables with a value"
    )

    def __init__(self, **params):
        self._variables = self._get_variables()

        for variable in self._variables:
            params[variable] = params.get(variable, os.environ.get(variable, ""))

        layout_params = {}
        for variable, value in params.items():
            if variable in pn.Column.param:
                layout_params[variable] = value
        for variable in layout_params:
            params.pop(variable)

        super().__init__(**params)

        self._layout = self._create_layout(**layout_params)

    def __panel__(self):
        return self._layout

    def _get_variables(self):
        return tuple(
            key for key in self.param if key not in EnvironmentWidgetBase.param
        )

    def _create_layout(self, **params):
        self._update_missing_variables(None)
        if not self.variables_not_set:
            return pn.Column(height=0, width=0, margin=0, sizing_mode="fixed")

        layout = pn.Column(**params)
        if self.message_alert:
            alert = pn.pane.Alert(
                self.message_alert,
                alert_type="danger",
                sizing_mode="stretch_width",
            )
            layout.append(alert)

        for key in self.variables_not_set:
            parameter = self.param[key]
            input_widget = pn.widgets.PasswordInput.from_param(
                parameter,
                max_width=WIDGET_MAX_WIDTH,
                sizing_mode="stretch_width",
                align="center",
            )

            pn.bind(self._update_missing_variables, input_widget, watch=True)
            layout.append(input_widget)
        return layout

    def _update_missing_variables(self, _):
        missing = []
        not_missing = []
        for key in self._variables:
            if not getattr(self, key):
                missing.append(key)
            else:
                not_missing.append(key)
        with param.edit_constant(self):
            self.variables_not_set = sorted(missing)
            self.variables_set = sorted(not_missing)

    def get(self, __key: str, default: str) -> str:
        if __key not in self._variables:
            raise VariableNotFound(key=__key)
        return getattr(self, __key) or default

    def __getitem__(self, key):
        value = self.get(key, "")
        if not value:
            raise VariableNotFound(key=key)
        return value
