"""
Demonstrates how to create a slim ChatInterface widget that fits in the sidebar.
"""
import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.widgets.ChatInterface(
    callback=callback,
    show_send=False,
    show_rerun=False,
    show_undo=False,
    show_clear=False,
    show_button_name=False,
    height=875,
    width=475,
)
chat_interface.send("Send a message and hear an echo!", user="System", respond=False)

pn.template.FastListTemplate(
    main=["# Insert the main content here to chat about it; maybe a PDF?"],
    sidebar=[chat_interface],
    sidebar_width=500,
).servable()
