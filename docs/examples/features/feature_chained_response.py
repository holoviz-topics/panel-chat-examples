"""
Demonstrates how to chain responses in a `ChatInterface`.
"""

from time import sleep

import panel as pn

pn.extension(design="material")

ARM_BOT = "Arm Bot"
LEG_BOT = "Leg Bot"


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    sleep(1)
    if user == "User":
        yield {
            "user": ARM_BOT,
            "avatar": "🦾",
            "object": f"Hey, {LEG_BOT}! Did you hear the user?",
        }
        instance.respond()
    elif user == ARM_BOT:
        user_message = instance.objects[-2]
        user_contents = user_message.object
        yield {
            "user": LEG_BOT,
            "avatar": "🦿",
            "object": f'Yeah! They said "{user_contents}".',
        }


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Send a message!", user="System", respond=False)
chat_interface.servable()
