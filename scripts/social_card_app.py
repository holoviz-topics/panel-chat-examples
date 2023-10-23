"""
Used to create the panel-chat-examples-card-HEIGHTxWIDTH.png cards for social media
"""
import panel as pn

pn.extension(design="material")

WELCOME = """
# Check out **Panel Chat Examples**.

Panel Chat Examples is a collection of reference **Panel chat apps with accessible \
source code**.

**HoloViz Panel** is the powerful data exploration & web app framework for Python.

<img src="https://panel.holoviz.org/_static/logo_horizontal_light_theme.png" \
style="height:125px"></img>
"""


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    return ""


chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="Assistant")
chat_interface.send(WELCOME, user="User", avatar="👩", respond=False)

chat_interface.servable()
