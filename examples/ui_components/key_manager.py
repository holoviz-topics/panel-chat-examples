"""The `KeyManager` enables you to manage keys from a combination of environment variables.
and user input.

For example you might not have the resources to provide an `OpenAI_API_KEY` or `WEAVIATE_API_KEY`.
Then you would like to ask the user for it.
"""
import os

import panel as pn
import param

WIDGET_MAX_WIDTH = 600


class KeyManagerBase(pn.viewable.Viewer):
    """The `KeyManager` enables you to manage keys from a combination of environment variables.
and user input.

For example you might not have the resources to provide an `OpenAI_API_KEY` or `WEAVIATE_API_KEY`.
Then you would like to ask the user for it.

Inherit from this widget to create you custom `KeyManager`.

    >>> class KeyManager(KeyManagerBase):
    ...     OPENAI_API_KEY = param.String(doc="A key for the OpenAI api")
    ...     WEAVIATE_API_KEY = param.String(doc="A key for the Weaviate api")
    ...     LANGCHAIN_API_KEY = param.String(doc="A key for the LangChain api")
"""

    message_alert: str = param.String(
        (
            "**Protect your keys!** If you are using this tool online make sure you trust "
            "the publisher of this app before entering your keys."
        )
    )

    keys_not_set = param.List(constant=True, doc="A list of the keys with no value")
    keys_set = param.List(constant=True, doc="A list of the keys with a value")

    def __init__(self, **params):
        self._keys = self._get_keys()

        layout_params = {}
        for key, value in params.items():
            if key in pn.Column.param:
                layout_params[key] = value
        for key in layout_params:
            params.pop(key)

        super().__init__(**params)

        self._update_missing_keys(None)
        self._layout = self._create_layout(**layout_params)

    def __panel__(self):
        return self._layout

    def _get_keys(self):
        return tuple(key for key in self.param if not key in KeyManagerBase.param)

    def _create_layout(self, **params):
        layout = pn.Column(**params)
        if self.message_alert:
            alert = pn.pane.Alert(
                self.message_alert,
                alert_type="danger",
                sizing_mode="stretch_width",
            )
            layout.append(alert)

        for key in self._keys:
            if os.environ.get(key):
                continue

            parameter = self.param[key]
            input_widget = pn.widgets.PasswordInput.from_param(
                parameter,
                max_width=WIDGET_MAX_WIDTH,
                sizing_mode="stretch_width",
                align="center",
            )
            pn.bind(self._update_missing_keys, input_widget, watch=True)
            layout.append(input_widget)
        return layout

    def get_value(self, key):
        """Returns the value of the specified key

        >>> manager.get_value("OPENAI_API_KEY")

        If the parameter corresponding to the key has a value, it is returned
        If os.environ has a value corresponding to the key, it is returned
        Otherwise "" is returned
        """
        if key not in self._keys:
            return ""
        if getattr(self, key):
            return getattr(self, key)
        return os.environ.get(key, "")

    def _update_missing_keys(self, _):
        missing = []
        not_missing = []
        for key in self._keys:
            if not self.get_value(key):
                missing.append(key)
            else:
                not_missing.append(key)
        with param.edit_constant(self):
            self.keys_not_set = missing
            self.keys_set = not_missing


if pn.state.served:
    class KeyManager(KeyManagerBase):
        """An example Key Manager"""
        OPENAI_API_KEY = param.String(doc="A key for the OpenAI api")
        WEAVIATE_API_KEY = param.String(doc="A key for the Weaviate api")
        LANGCHAIN_API_KEY = param.String(doc="A key for the LangChain api")

    manager = KeyManager(max_width=1000)
    pn.template.FastListTemplate(
        title="Key Manager",
        sidebar=[manager],
        main=[__doc__, pn.Column(manager.param.keys_set, manager.param.keys_not_set)],
    ).servable()
