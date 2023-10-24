"""
Used to create the panel-chat-examples-card-HEIGHTxWIDTH.png cards for social media
"""
import panel as pn

pn.extension(design="material")

WELCOME = """
<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Ubuntu">
<style>
a {
 text-decoration: none !important;
 color:black;
}
</style>
<div style="text-align:center;margin-top:20px;font-family: Ubuntu, \
"times new roman", times, roman, serif;">
<img src="https://github.com/holoviz-topics/panel-chat-examples/raw/main/docs/assets\
/images/panel-logo.png" style="height:25px;margin-right:10px"></img>\
<span style="font-size:35px;font-weight:900;text-align:center">\
Panel Chat Examples</span>.
</div>

Reference chat apps with accessible source code.

**holoviz-topics.github.io/panel-chat-examples**
"""


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    return ""


chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="Assistant")
chat_interface.send(WELCOME, user="User", avatar="👩", respond=False)

chat_interface.servable()
