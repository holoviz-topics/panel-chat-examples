# Panel Chat Examples

[![build](https://github.com/holoviz-topics/panel-chat-examples/workflows/Build/badge.svg)](https://github.com/holoviz-topics/panel-chat-examples/actions)

Examples using [Panel](https://panel.holoviz.org/) and its [Chat Components](https://panel.holoviz.org/reference/index.html#chat); Panels chat components are *multi modal* and supports [LangChain](https://python.langchain.com/docs/get_started/introduction), [OpenAI](https://openai.com/blog/chatgpt), [Mistral](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjZtP35yvSBAxU00wIHHerUDZAQFnoECBEQAQ&url=https%3A%2F%2Fdocs.mistral.ai%2F&usg=AOvVaw2qpx09O_zOzSksgjBKiJY_&opi=89978449), [Llama](https://ai.meta.com/llama/), etc.

**Documentation**: <a href="https://holoviz-topics.github.io/panel-chat-examples/" target="_blank">holoviz-topics.github.io/panel-chat-examples/</a>

https://github.com/holoviz-topics/panel-chat-examples/assets/42288570/cdb78a39-b98c-44e3-886e-29de6a079bde

Panels Chat Components are available with `pip install "panel>=1.3.0"`; most examples require `pip install "panel>=1.4.0"`.

More unmaintained examples can be found in [GitHub issues](https://github.com/holoviz-topics/panel-chat-examples/issues) and [HoloViz Discourse](https://discourse.holoviz.org/)

## Quick Start

It's super easy to get started with Panel chat components.

1. Setup imports
2. Define a function to dictate what to do with the input message
3. Define a servable widget with `callback=response_callback`

```python
# 1.)
import panel as pn
pn.extension()

# 2.)
def response_callback(input_message: str, input_user: str, instance: pn.chat.ChatInterface):
    # choose your favorite LLM API to respond to the input_message
    ...
    response_message = f"Echoing your input: {input_message}"
    return response_message

# 3.)
pn.widgets.ChatInterface(callback=response_callback).servable()
```

## Exploration

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/holoviz-topics/panel-chat-examples?quickstart=1)

## Installation

To install and serve all examples:

```bash
git clone https://github.com/holoviz-topics/panel-chat-examples
cd panel-chat-examples
pip install -e ".[all]"  # or instead of `all`, just `openai`, `mistralai`, `langchain`, `llamaindex`, `llamacpp`
# Optionally set the OPENAI_API_KEY environment variable
panel serve docs/examples/**/*.py --static-dirs thumbnails=docs/assets/thumbnails --autoreload
```

Then open [http://localhost:5006](http://localhost:5006) in your browser.

![Panel Index Page](https://raw.githubusercontent.com/holoviz-topics/panel-chat-examples/main/assets/images/panel-chat-examples-index-page.png)

## Contributing

We would ❤️ to collaborate with you. Check out the [DEVELOPER GUIDE](https://github.com/holoviz-topics/panel-chat-examples/blob/main/DEVELOPER_GUIDE.md) for to get started.

## License

This project is licensed under the terms of the [MIT license](https://github.com/holoviz-topics/panel-chat-examples/blob/main/LICENSE.md).
