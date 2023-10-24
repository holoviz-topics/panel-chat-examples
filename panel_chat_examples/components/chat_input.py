"""The `ChatInput` widget is a combination of a `TextInput` widget and a `Button`.
When the input is submitted the `TextInput` widget is cleared and ready to accept
a new input."""
import panel as pn
import param


class ChatInput(pn.viewable.Viewer):
    """The `ChatInput` widget is a combination of a `TextInput` widget and a `Button`.
    When the input is submitted the `TextInput` widget is cleared and ready to accept
    a new input."""

    value: str = param.String(doc="""The text value""")

    disabled: bool = param.Boolean(
        doc="""
        Whether or not the widget is disabled. Default is False"""
    )
    max_length = param.Integer(
        default=5000,
        doc="""
        The max_length of the text input""",
    )
    placeholder = param.String(
        "Send a message",
        doc="""
        An initial placeholder to display in the TextInput""",
    )

    def __init__(self, **params):
        layout_params = {
            key: value
            for key, value in params.items()
            if key not in ["value", "placeholder", "disabled", "max_length"]
        }
        params = {
            key: value for key, value in params.items() if key not in layout_params
        }

        super().__init__(**params)

        self._text_input = pn.widgets.TextInput(
            align="center",
            disabled=self.param.disabled,
            max_length=self.param.max_length,
            name="Message",
            placeholder=self.param.placeholder,
            sizing_mode="stretch_width",
        )
        self._submit_button = pn.widgets.Button(
            align="center",
            disabled=self.param.disabled,
            icon="send",
            margin=(18, 5, 10, 0),
            name="",
            sizing_mode="fixed",
        )
        pn.bind(
            self._update_value,
            value=self._text_input,
            event=self._submit_button,
            watch=True,
        )

        self._layout = pn.Row(
            self._text_input, self._submit_button, align="center", **layout_params
        )

    def __panel__(self):
        return self._layout

    def _update_value(self, value, event):
        self.value = value or self.value
        self._text_input.value = ""
