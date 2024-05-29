"""
Demonstrates how to use the `ChatInterface` to create two bots that chat with each
other.

Highlights:

- The user decides the callback user and avatar for the response.
- A system message is used to control the conversation flow.
"""

import panel as pn
from openai import AsyncOpenAI

pn.extension()


async def callback(
    contents: str,
    user: str,
    instance: pn.chat.ChatInterface,
):
    if user in ["User", "Happy Bot"]:
        callback_user = "Nerd Bot"
        callback_avatar = "🤓"
    elif user == "Nerd Bot":
        callback_user = "Happy Bot"
        callback_avatar = "😃"

    if len(instance.objects) % 6 == 0:  # stop at every 6 messages
        instance.send(
            "That's it for now! Thanks for chatting!", user="System", respond=False
        )
        return

    prompt = f"Reply profoundly about '{contents}', then follow up with a question."
    messages = [{"role": "user", "content": prompt}]
    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        max_tokens=250,
        temperature=0.1,
    )

    message = ""
    async for chunk in response:
        part = chunk.choices[0].delta.content
        if part is not None:
            message += part
            yield {"user": callback_user, "avatar": callback_avatar, "object": message}

    instance.respond()


aclient = AsyncOpenAI()
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    help_text="Enter a topic for the bots to discuss! Beware the token usage!",
)
chat_interface.servable()
