"""
Demonstrates how to use the ChatInterface widget to create two bots that
chat with each other.
"""

import openai
import panel as pn

pn.extension()


async def callback(
    contents: str,
    user: str,
    instance: pn.widgets.ChatInterface,
):
    if user in ["User", "Happy Bot"]:
        callback_user = "Nerd Bot"
        callback_avatar = "🤓"
    elif user == "Nerd Bot":
        callback_user = "Happy Bot"
        callback_avatar = "😃"

    prompt = f"Think profoundly about {contents}, then ask a question."
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=250,
        temperature=0.1,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield {"user": callback_user, "avatar": callback_avatar, "value": message}

    if len(instance.value) % 6 == 0:  # stop at every 6 messages
        instance.send(
            "That's it for now! Thanks for chatting!", user="System", respond=False
        )
        return
    instance.respond()


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a topic for the bots to discuss! Beware the token usage!",
    user="System",
    respond=False,
)
chat_interface.servable()
