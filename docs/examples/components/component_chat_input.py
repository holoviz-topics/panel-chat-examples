"""The `ChatInput` widget is a combination of a `TextInput` widget and a `Button`.
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
