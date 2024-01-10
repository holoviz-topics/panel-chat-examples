import panel as pn
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    messages.append(ChatMessage(role="user", content=contents))

    mistral_response = ""
    for chunk in client.chat_stream(model="mistral-tiny", messages=messages):
        response = chunk.choices[0].delta.content
        if response is not None:
            mistral_response += response
            yield mistral_response

    if mistral_response:
        messages.append(ChatMessage(role="assistant", content=mistral_response))


messages = []
client = MistralClient()  # api_key=os.environ.get("MISTRAL_API_KEY", None)
chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="Mistral AI")
chat_interface.send(
    "Send a message to get a reply from Mistral AI!", user="System", respond=False
)
chat_interface.servable()
