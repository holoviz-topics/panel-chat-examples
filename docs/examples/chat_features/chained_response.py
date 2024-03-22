"""
Demonstrates how to chain responses from a single message in the callback.

Highlight:

- The `respond` parameter in the `send` method is used to chain responses.
- It's also possible to use `respond` as a method to chain responses.
"""

from asyncio import sleep

import panel as pn

pn.extension()

PERSON_1 = "Happy User"
PERSON_2 = "Excited User"
PERSON_3 = "Passionate User"


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(2)
    if user == "User":
        instance.send(
            f"Hey, {PERSON_2}! Did you hear the user?",
            user=PERSON_1,
            avatar="😊",
            respond=True,  # This is the default, but it's here for clarity
        )
    elif user == PERSON_1:
        user_message = instance.objects[-2]
        user_contents = user_message.object
        yield pn.chat.ChatMessage(
            f'Yeah, they said "{user_contents}"! Did you also hear {PERSON_3}?',
            user=PERSON_2,
            avatar="😄",
        )
        instance.respond()
    elif user == PERSON_2:
        instance.send(
            f"Yup, I heard!",
            user=PERSON_3,
            avatar="😆",
            respond=False,
        )


chat_interface = pn.chat.ChatInterface(
    help_text="Send a message to start the conversation!", callback=callback
)
chat_interface.servable()
