"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2.

Pre-requisites:
```bash
pip install llama-cpp-python
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make
curl -L https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q3_K_L.gguf" -o models/llama-2-7b-chat.Q3_K_L.gguf
```
"""

from llama_cpp import Llama
import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = llm(contents, max_tokens=2048)
    message = ""
    for chunk in response:
        message += chunk["choices"][0]["text"]
        yield message


llm = Llama(
    model_path="llama.cpp/models/llama-2-7b-chat.Q3_K_L.gguf", n_ctx=2048, verbose=False
)
chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="Llama")
chat_interface.send(
    "Send a message to get a reply from Llama 2!", user="System", respond=False
)
chat_interface.servable()
