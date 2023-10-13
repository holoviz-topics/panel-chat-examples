
# Panel Chat Examples

To run all of these examples locally:

```bash
git clone https://github.com/holoviz-topics/panel-chat-examples
cd panel-chat-examples
pip install hatch
# Optionally set the OPENAI_API_KEY environment variable
hatch run panel-serve
```

!!! note
    Note the default installation is not optimized for GPU usage. To **enable
    GPU support** for local models (i.e. not OpenAI), install `ctransformers`
    with the proper backend and modify the
    scripts configs' accordingly, e.g. `n_gpu_layers=1` for a single GPU.

## Basics

### Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

The chatbot Assistant echoes back the message entered by the User.
<details>
<summary>Source code for <a href='examples\basics\basic_chat.py' target='_blank'>basic_chat.py</a></summary>
```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to respond.

The chatbot Assistant echoes back the message entered by the User.
"""

import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


### Streaming Chat

Demonstrates how to use the `ChatInterface` and a `callback` function to stream back
responses.

The chatbot Assistant echoes back the message entered by the User in a *streaming*
fashion.
<details>
<summary>Source code for <a href='examples\basics\basic_streaming_chat.py' target='_blank'>basic_streaming_chat.py</a></summary>
```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to stream back
responses.

The chatbot Assistant echoes back the message entered by the User in a *streaming*
fashion.
"""


from time import sleep

import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    sleep(1)
    message = ""
    for char in f"Echoing {user}: {contents}":
        sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


### Echo Stream Async

Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.
<details>
<summary>Source code for <a href='examples\basics\echo_stream_async.py' target='_blank'>echo_stream_async.py</a></summary>
```python
"""
Demonstrates how to use the `ChatInterface` and a `callback` function to
stream back responses.

The chatbot Assistant echoes back the message entered by the User in an
*async streaming* fashion.
"""


from asyncio import sleep

import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    await sleep(1)
    message = ""
    for char in contents:
        await sleep(0.05)
        message += char
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


## Components

### Environment Widget

The `EnvironmentWidgetBase` class enables you to manage variable values from a
combination of

- custom variable values
- environment variables
- user input.

(listed by order of precedence)

You can use it as a drop in replacement for `os.environ`.

For example you might not have the resources to provide an `OPENAI_API_KEY`,
`WEAVIATE_API_KEY` or `LANGCHAIN_API_KEY`. In that case you would would like to ask the
user for it.

Inherit from this widget to create your own custom `EnvironmentWidget`.
<details>
<summary>Source code for <a href='examples\components\component_environment_widget.py' target='_blank'>component_environment_widget.py</a></summary>
```python
"""
The `EnvironmentWidgetBase` class enables you to manage variable values from a
combination of

- custom variable values
- environment variables
- user input.

(listed by order of precedence)

You can use it as a drop in replacement for `os.environ`.

For example you might not have the resources to provide an `OPENAI_API_KEY`,
`WEAVIATE_API_KEY` or `LANGCHAIN_API_KEY`. In that case you would would like to ask the
user for it.

Inherit from this widget to create your own custom `EnvironmentWidget`.
"""
# Longer term we should try to get this widget included in Panel
import panel as pn
import param

from panel_chat_examples import EnvironmentWidgetBase

pn.extension(design="material")


class EnvironmentWidget(EnvironmentWidgetBase):
    """An example Environment Widget for managing environment variables"""

    OPENAI_API_KEY = param.String(doc="A key for the OpenAI api")
    WEAVIATE_API_KEY = param.String(doc="A key for the Weaviate api")
    LANGCHAIN_API_KEY = param.String(doc="A key for the LangChain api")


environment = EnvironmentWidget(max_width=1000)
pn.template.FastListTemplate(
    title="Environment Widget",
    sidebar=[environment],
    main=[
        __doc__,
        pn.Column(
            environment.param.variables_set,
            environment.param.variables_not_set,
        ),
    ],
).servable()
```
</details>


## Features

### Chained Response

Demonstrates how to chain responses in a ChatInterface.
<details>
<summary>Source code for <a href='examples\features\feature_chained_response.py' target='_blank'>feature_chained_response.py</a></summary>
```python
"""
Demonstrates how to chain responses in a ChatInterface.
"""

from time import sleep

import panel as pn

pn.extension(design="material")

ARM_BOT = "Arm Bot"
LEG_BOT = "Leg Bot"


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    sleep(1)
    if user == "User":
        yield {
            "user": ARM_BOT,
            "avatar": "🦾",
            "value": f"Hey, {LEG_BOT}! Did you hear the user?",
        }
        instance.respond()
    elif user == ARM_BOT:
        user_entry = instance.value[-2]
        user_contents = user_entry.value
        yield {
            "user": LEG_BOT,
            "avatar": "🦿",
            "value": f'Yeah! They said "{user_contents}".',
        }


chat_interface = pn.widgets.ChatInterface(callback=callback)
chat_interface.send("Send a message!", user="System", respond=False)
chat_interface.servable()
```
</details>


### Delayed Placeholder

Demonstrates how to delay the display of the placeholder.
<details>
<summary>Source code for <a href='examples\features\feature_delayed_placeholder.py' target='_blank'>feature_delayed_placeholder.py</a></summary>
```python
"""
Demonstrates how to delay the display of the placeholder.
"""

from asyncio import sleep

import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    try:
        seconds = float(contents)
        if 0 < seconds < 10:
            await sleep(seconds)
            return f"Slept {contents} seconds!"
        else:
            return "Please enter a number between 1 and 9!"
    except ValueError:
        return "Please enter a number!"


chat_interface = pn.widgets.ChatInterface(
    callback=callback,
    placeholder_threshold=2,
    placeholder_text="Waiting for reply...",
)
chat_interface.send(
    "Send a number to make the system sleep between 1 and 9 seconds!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


### Replace Response

Demonstrates how to update the response of a ChatInterface widget.
<details>
<summary>Source code for <a href='examples\features\feature_replace_response.py' target='_blank'>feature_replace_response.py</a></summary>
```python
"""
Demonstrates how to update the response of a ChatInterface widget.
"""

from asyncio import sleep
from random import choice

import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    yield "Let me flip the coin for you..."
    await sleep(1)

    characters = "/|\\_"
    index = 0
    for _ in range(0, 28):
        index = (index + 1) % len(characters)
        yield "\r" + characters[index]
        await sleep(0.005)

    result = choice(["heads", "tails"])
    if result in contents.lower():
        yield f"Woohoo, {result}! You win!"
    else:
        yield f"Aw, got {result}. Try again!"


chat_interface = pn.widgets.ChatInterface(
    widgets=[
        pn.widgets.RadioButtonGroup(
            options=["Heads!", "Tails!"], button_type="primary", button_style="outline"
        )
    ],
    callback=callback,
    callback_user="Game Master",
)
chat_interface.send(
    "Select heads or tails, then click send!", user="System", respond=False
)
chat_interface.servable()
```
</details>


### Slim Interface

Demonstrates how to create a slim ChatInterface widget that fits in the sidebar.
<details>
<summary>Source code for <a href='examples\features\feature_slim_interface.py' target='_blank'>feature_slim_interface.py</a></summary>
```python
"""
Demonstrates how to create a slim ChatInterface widget that fits in the sidebar.
"""
import panel as pn

pn.extension(design="material")


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
    sizing_mode="stretch_both",
    min_height=200,
    width=475,
)
chat_interface.send("Send a message and hear an echo!", user="System", respond=False)

pn.template.FastListTemplate(
    main=[
        """We've put a *slim* `ChatInterface` in the sidebar. In the main area you \
could add the object you are chatting about"""
    ],
    sidebar=[chat_interface],
    sidebar_width=500,
).servable()
```
</details>


## Langchain

### Llama And Mistral

Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2 and Mistral.
<details>
<summary>Source code for <a href='examples\langchain\langchain_llama_and_mistral.py' target='_blank'>langchain_llama_and_mistral.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Llama2 and Mistral.
"""

import panel as pn
from langchain.chains import LLMChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

pn.extension()

MODEL_KWARGS = {
    "llama": {
        "model": "TheBloke/Llama-2-7b-Chat-GGUF",
        "model_file": "llama-2-7b-chat.Q5_K_M.gguf",
    },
    "mistral": {
        "model": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "model_file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    },
}

# We cache the chains and responses to speed up things
llm_chains = pn.state.cache["llm_chains"] = pn.state.cache.get("llm_chains", {})
responses = pn.state.cache["responses"] = pn.state.cache.get("responses", {})

TEMPLATE = """<s>[INST] You are a friendly chat bot who's willing to help answer the
user:
{user_input} [/INST] </s>
"""

CONFIG = {"max_new_tokens": 256, "temperature": 0.5}


def _get_llm_chain(model, template=TEMPLATE, config=CONFIG):
    llm = CTransformers(**MODEL_KWARGS[model], config=config)
    prompt = PromptTemplate(template=template, input_variables=["user_input"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain


# Cannot use pn.cache due to https://github.com/holoviz/panel/issues/4236
async def _get_response(contents: str, model: str) -> str:
    key = (contents, model)
    if key in responses:
        return responses[key]

    llm_chain = llm_chains[model]
    response = responses[key] = await llm_chain.apredict(user_input=contents)
    return response


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    for model in MODEL_KWARGS:
        if model not in llm_chains:
            instance.placeholder_text = (
                f"Downloading {model}, this may take a few minutes,"
                f"or longer, depending on your internet connection."
            )
            llm_chains[model] = _get_llm_chain(model)

        response = await _get_response(contents, model)
        instance.send(response, user=model.title(), respond=False)


chat_interface = pn.widgets.ChatInterface(callback=callback, placeholder_threshold=0.1)
chat_interface.send(
    "Send a message to get a reply from both Llama 2 and Mistral (7B)!",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


### Math Assistant

Demonstrates how to use the ChatInterface widget to create
a math chatbot using OpenAI's text-davinci-003 model with LangChain.
<details>
<summary>Source code for <a href='examples\langchain\langchain_math_assistant.py' target='_blank'>langchain_math_assistant.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create
a math chatbot using OpenAI's text-davinci-003 model with LangChain.
"""

import panel as pn
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    final_answer = await llm_math.arun(question=contents)
    instance.stream(final_answer, entry=instance.value[-1])


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="Langchain")
chat_interface.send(
    "Send a math question to get an answer from MathGPT!", user="System", respond=False
)

callback_handler = pn.widgets.langchain.PanelCallbackHandler(
    chat_interface=chat_interface
)
llm = OpenAI(streaming=True, callbacks=[callback_handler])
llm_math = LLMMathChain.from_llm(llm, verbose=True)
chat_interface.servable()
```
</details>


### Pdf Assistant

Demonstrates how to use the ChatInterface widget to chat about a PDF using
OpenAI, LangChain and Chroma.
<details>
<summary>Source code for <a href='examples\langchain\langchain_pdf_assistant.py' target='_blank'>langchain_pdf_assistant.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to chat about a PDF using
OpenAI, LangChain and Chroma.
"""

import tempfile
from pathlib import Path

import panel as pn
import param
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from panel_chat_examples import EnvironmentWidgetBase

EXAMPLE_PDF = Path(__file__).parent / "example.pdf"
TTL = 1800  # 30 minutes

pn.extension()

# Define the Retrival Question/ Answer Chain
# We use caching to speed things up


@pn.cache(ttl=TTL)
def _get_texts(pdf):
    # load documents
    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(pdf)
    file_name = f.name
    loader = PyPDFLoader(file_name)
    documents = loader.load()

    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)


@pn.cache(ttl=TTL)
def _get_vector_db(pdf, openai_api_key):
    texts = _get_texts(pdf)
    # select which embeddings we want to use
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # create the vectorestore to use as the index
    return Chroma.from_documents(texts, embeddings)


@pn.cache(ttl=TTL)
def _get_retriever(pdf, openai_api_key: str, number_of_chunks: int):
    db = _get_vector_db(pdf, openai_api_key)
    return db.as_retriever(
        search_type="similarity", search_kwargs={"k": number_of_chunks}
    )


@pn.cache(ttl=TTL)
def _get_retrival_qa(
    pdf: bytes, number_of_chunks: int, chain_type: str, openai_api_key: str
):
    retriever = _get_retriever(pdf, openai_api_key, number_of_chunks)
    return RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=openai_api_key),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
    )


def _get_response(contents):
    qa = _get_retrival_qa(
        state.pdf, state.number_of_chunks, state.chain_type, environ.OPENAI_API_KEY
    )
    response = qa({"query": contents})
    chunks = []

    for chunk in response["source_documents"][::-1]:
        name = f"Chunk {chunk.metadata['page']}"
        content = chunk.page_content
        chunks.insert(0, (name, content))
    return response, chunks


# Define the Application State
class EnvironmentWidget(EnvironmentWidgetBase):
    OPENAI_API_KEY: str = param.String()


class State(param.Parameterized):
    pdf: bytes = param.Bytes()
    number_of_chunks: int = param.Integer(default=2, bounds=(1, 5), step=1)
    chain_type: str = param.Selector(
        objects=["stuff", "map_reduce", "refine", "map_rerank"]
    )


environ = EnvironmentWidget()
state = State()

# Define the widgets
pdf_input = pn.widgets.FileInput.from_param(state.param.pdf, accept=".pdf", height=50)
text_input = pn.widgets.TextInput(placeholder="First, upload a PDF!")
chain_type_input = pn.widgets.RadioButtonGroup.from_param(
    state.param.chain_type,
    orientation="vertical",
    sizing_mode="stretch_width",
    button_type="primary",
    button_style="outline",
)

# Define and configure the ChatInterface


def _get_validation_message():
    pdf = state.pdf
    openai_api_key = environ.OPENAI_API_KEY
    if not pdf and not openai_api_key:
        return "Please first enter an OpenAI Api key and upload a PDF!"
    if not pdf:
        return "Please first upload a PDF!"
    if not openai_api_key:
        return "Please first enter an OpenAI Api key!"
    return ""


def _send_not_ready_message(chat_interface) -> bool:
    message = _get_validation_message()

    if message:
        chat_interface.send({"user": "System", "value": message}, respond=False)
    return bool(message)


async def respond(contents, user, chat_interface):
    if _send_not_ready_message(chat_interface):
        return
    if chat_interface.active == 0:
        chat_interface.active = 1
        chat_interface.active_widget.placeholder = "Ask questions here!"
        yield {"user": "OpenAI", "value": "Let's chat about the PDF!"}
        return

    response, documents = _get_response(contents)
    pages_layout = pn.Accordion(*documents, sizing_mode="stretch_width", max_width=800)
    answers = pn.Column(response["result"], pages_layout)

    yield {"user": "OpenAI", "value": answers}


chat_interface = pn.widgets.ChatInterface(
    callback=respond,
    sizing_mode="stretch_width",
    widgets=[pdf_input, text_input],
    disabled=True,
)


@pn.depends(state.param.pdf, environ.param.OPENAI_API_KEY, watch=True)
def _enable_chat_interface(pdf, openai_api_key):
    if pdf and openai_api_key:
        chat_interface.disabled = False
    else:
        chat_interface.disabled = True


_send_not_ready_message(chat_interface)

## Wrap the app in a nice template

template = pn.template.BootstrapTemplate(
    sidebar=[
        environ,
        state.param.number_of_chunks,
        "Chain Type:",
        chain_type_input,
    ],
    main=[chat_interface],
)
template.servable()
```
</details>


### With Memory

Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API with LangChain.
<details>
<summary>Source code for <a href='examples\langchain\langchain_with_memory.py' target='_blank'>langchain_with_memory.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API with LangChain.
"""

import panel as pn
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    await chain.apredict(input=contents)


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)

callback_handler = pn.widgets.langchain.PanelCallbackHandler(
    chat_interface=chat_interface
)
llm = ChatOpenAI(streaming=True, callbacks=[callback_handler])
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
chat_interface.servable()
```
</details>


## Mistral

### Chat

Demonstrates how to use the ChatInterface widget to create a chatbot using
Mistral through CTransformers.
<details>
<summary>Source code for <a href='examples\mistral\mistral_chat.py' target='_blank'>mistral_chat.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
Mistral through CTransformers.
"""

import panel as pn
from ctransformers import AutoModelForCausalLM

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    if "mistral" not in llms:
        instance.placeholder_text = "Downloading model; please wait..."
        llms["mistral"] = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            gpu_layers=1,
        )

    llm = llms["mistral"]
    response = llm(contents, stream=True, max_new_tokens=1000)
    message = ""
    for token in response:
        message += token
        yield message


llms = pn.state.cache["llms"] = pn.state.cache.get("llms", {})
chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="Mistral")
chat_interface.send(
    "Send a message to get a reply from Mistral!", user="System", respond=False
)
chat_interface.servable()
```
</details>


## Openai

### Async Chat

Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API with async/await.

<video controls poster="assets\thumbnails\openai_async_chat.png" >  
  <source src="assets\videos\openai_async_chat.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_async_chat.py' target='_blank'>openai_async_chat.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API with async/await.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
```
</details>


### Authentication

Demonstrates how to use the ChatInterface widget with authentication for
OpenAI's API.

<video controls poster="assets\thumbnails\openai_authentication.png" >  
  <source src="assets\videos\openai_authentication.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_authentication.py' target='_blank'>openai_authentication.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget with authentication for
OpenAI's API.
"""

import os

import openai
import panel as pn

SYSTEM_KWARGS = dict(
    user="System",
    respond=False,
)

pn.extension()


def add_key_to_env(key):
    if not key.startswith("sk-"):
        chat_interface.send("Please enter a valid OpenAI key!", **SYSTEM_KWARGS)
        return

    chat_interface.send(
        "Your OpenAI key has been set. Feel free to minimize the sidebar.",
        **SYSTEM_KWARGS,
    )
    chat_interface.disabled = False


key_input = pn.widgets.PasswordInput(placeholder="sk-...", name="OpenAI Key")
pn.bind(add_key_to_env, key=key_input, watch=True)


async def callback(
    contents: str,
    user: str,
    instance: pn.widgets.ChatInterface,
):
    if "OPENAI_API_KEY" not in os.environ:
        yield "Please first set your OpenAI key in the sidebar!"
        return

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
        api_key=key_input.value,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, disabled=True)
chat_interface.send(
    "First enter your OpenAI key in the sidebar, then send a message!", **SYSTEM_KWARGS
)

pn.template.MaterialTemplate(
    title="OpenAI ChatInterface with authentication",
    sidebar=[key_input],
    main=[chat_interface],
).servable()
```
</details>


### Chat

Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API.

<video controls poster="assets\thumbnails\openai_chat.png" >  
  <source src="assets\videos\openai_chat.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_chat.py' target='_blank'>openai_chat.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API.
"""

import openai
import panel as pn

pn.extension(design="material")


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
```
</details>


### Hvplot

Demonstrates how to use the ChatInterface widget to create a chatbot
that can generate plots using hvplot.

<video controls poster="assets\thumbnails\openai_hvplot.png" >  
  <source src="assets\videos\openai_hvplot.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_hvplot.py' target='_blank'>openai_hvplot.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create a chatbot
that can generate plots using hvplot.
"""

import re
from typing import Union

import openai
import pandas as pd
import panel as pn
from panel.io.mime_render import exec_with_return

DATAFRAME_PROMPT = """
    Here are the columns in your DataFrame: {columns}.
    Create a plot with hvplot that highlights an interesting
    relationship between the columns with hvplot groupby kwarg.
"""

CODE_REGEX = re.compile(r"```\s?python(.*?)```", re.DOTALL)


def _clean(df: pd.DataFrame):
    df.columns = [column.strip() for column in df.columns]
    df = df.head(100)
    return df


async def respond_with_openai(contents: Union[pd.DataFrame, str]):
    # extract the DataFrame
    if isinstance(contents, pd.DataFrame):
        global df
        df = _clean(contents)
        columns = contents.columns
        message = DATAFRAME_PROMPT.format(columns=columns)
    else:
        message = contents

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        temperature=0,
        max_tokens=500,
        stream=True,
    )
    message = ""
    async for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield {"user": "ChatGPT", "value": message}


async def respond_with_executor(code: str):
    code_block = f"```python\n{code}\n```"
    global df
    context = {"df": df}
    plot = exec_with_return(code=code, global_context=context)
    return {
        "user": "Executor",
        "value": pn.Tabs(
            ("Plot", plot),
            ("Code", code_block),
        ),
    }


async def callback(
    contents: Union[str, pd.DataFrame],
    name: str,
    instance: pn.widgets.ChatInterface,
):
    if not isinstance(contents, (str, pd.DataFrame)):
        return

    if name == "User":
        async for chunk in respond_with_openai(contents):
            yield chunk
        instance.respond()
    elif CODE_REGEX.search(contents):
        yield await respond_with_executor(CODE_REGEX.search(contents).group(1))


chat_interface = pn.widgets.ChatInterface(
    widgets=[pn.widgets.FileInput(name="Upload"), pn.widgets.TextInput(name="Message")],
    callback=callback,
)
# ruff: noqa: E501
chat_interface.send(
    """Send a message to ChatGPT or upload a small CSV file to get started!

<a href="data:text/csv;base64,ZGF0ZSxjYXRlZ29yeSxxdWFudGl0eSxwcmljZQoyMDIxLTAxLTAxLGVsZWN0cm9uaWNzLDIsNTAwICAKMjAyMS0wMS0wMixjbG90aGluZywxLDUwCjIwMjEtMDEtMDMsaG9tZSBnb29kcyw0LDIwMAoyMDIxLTAxLTA0LGVsZWN0cm9uaWNzLDEsMTAwMAoyMDIxLTAxLTA1LGdyb2NlcmllcywzLDc1CjIwMjEtMDEtMDYsY2xvdGhpbmcsMiwxMDAKMjAyMS0wMS0wNyxob21lIGdvb2RzLDMsMTUwCjIwMjEtMDEtMDgsZWxlY3Ryb25pY3MsNCwyMDAwCjIwMjEtMDEtMDksZ3JvY2VyaWVzLDIsNTAKMjAyMS0wMS0xMCxlbGVjdHJvbmljcywzLDE1MDA=" download="example.csv">example.csv</a>
""",
    user="System",
    respond=False,
)
chat_interface.servable()
```
</details>


### Image Generation

Demonstrates how to use the ChatInterface widget to create an image using
OpenAI's DALL-E API.

<video controls poster="assets\thumbnails\openai_image_generation.png" >  
  <source src="assets\videos\openai_image_generation.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_image_generation.py' target='_blank'>openai_image_generation.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create an image using
OpenAI's DALL-E API.
"""

import openai
import panel as pn

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.Image.create(prompt=contents, n=1, size="256x256")
    image_url = response["data"][0]["url"]
    return pn.pane.Image(image_url, width=256, height=256)


chat_interface = pn.widgets.ChatInterface(
    callback=callback, callback_user="DALL-E", placeholder_text="Generating..."
)
chat_interface.send(
    "Create an image by providing a prompt!", user="System", respond=False
)
chat_interface.servable()
```
</details>


### Two Bots

Demonstrates how to use the ChatInterface widget to create two bots that
chat with each other.

<video controls poster="assets\thumbnails\openai_two_bots.png" >  
  <source src="assets\videos\openai_two_bots.webm" type="video/webm"
  style="max-height: 400px; max-width: 100%;">  
  Your browser does not support the video tag.  
</video> 
<details>
<summary>Source code for <a href='examples\openai\openai_two_bots.py' target='_blank'>openai_two_bots.py</a></summary>
```python
"""
Demonstrates how to use the ChatInterface widget to create two bots that
chat with each other.
"""

import openai
import panel as pn

pn.extension(design="material")


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
```
</details>

