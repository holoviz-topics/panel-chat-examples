"""
Demonstrates how to create a slim `ChatInterface` that fits in the sidebar.

Highlights:

- The `ChatInterface` is placed in the sidebar.
- Set `show_*` parameters to `False` to hide the respective buttons.
- Use `message_params` to customize the appearance of each chat messages.
"""

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    show_send=False,
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    show_avatar=False,
    show_timestamp=False,
    show_button_name=False,
    show_reaction_icons=False,
    sizing_mode="stretch_width",
    height=700,
    message_params={
        "stylesheets": [
            """
            .message {
                font-size: 1em;
            }
            .name {
                font-size: 0.9em;
            }
            .timestamp {
                font-size: 0.9em;
            }
            """
        ]
    },
)

main = """
We've put a *slim* `ChatInterface` in the sidebar. In the main area you
could add the object you are chatting about
"""

pn.template.FastListTemplate(
    main=[main],
    sidebar=[chat_interface],
    sidebar_width=500,
).servable()
