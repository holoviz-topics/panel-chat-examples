# Panel Chat Examples

[![build](https://github.com/holoviz-topics/panel-chat-examples/workflows/Build/badge.svg)](https://github.com/holoviz-topics/panel-chat-examples/actions)

Examples using [Panel](https://panel.holoviz.org/) and its [Chat Components](https://panel.holoviz.org/reference/index.html#chat); Panels chat components are *multi modal* and supports [LangChain](https://python.langchain.com/docs/get_started/introduction), [OpenAI](https://openai.com/blog/chatgpt), [Mistral](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjZtP35yvSBAxU00wIHHerUDZAQFnoECBEQAQ&url=https%3A%2F%2Fdocs.mistral.ai%2F&usg=AOvVaw2qpx09O_zOzSksgjBKiJY_&opi=89978449), [Llama](https://ai.meta.com/llama/), etc.

**Documentation**: <a href="https://holoviz-topics.github.io/panel-chat-examples/" target="_blank">holoviz-topics.github.io/panel-chat-examples/</a>

https://github.com/holoviz-topics/panel-chat-examples/assets/42288570/cdb78a39-b98c-44e3-886e-29de6a079bde

Panels Chat Components are available from Panel v1.3.0.

## Exploration

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/holoviz-topics/panel-chat-examples?quickstart=1)

## Installation

To install and serve all examples:

```bash
git clone https://github.com/holoviz-topics/panel-chat-examples
cd panel-chat-examples
# Optionally create a new virtual environment with conda, venv, etc.
pip install .
# Optionally set the OPENAI_API_KEY environment variable
panel serve docs/examples/**/*.py --static-dirs thumbnails=docs/assets/thumbnails --autoreload
```

Then open [http://localhost:5006](http://localhost:5006) in your browser.

![Panel Index Page](https://raw.githubusercontent.com/holoviz-topics/panel-chat-examples/main/assets/images/panel-chat-examples-index-page.png)

### GPU Usage

Note the default installation is not optimized for GPU usage. To enable GPU support for local
models (i.e. not OpenAI), install `ctransformers` with the [proper backend](https://github.com/marella/ctransformers#gpu) and modify the scripts configs' accordingly, e.g. `n_gpu_layers=1` for a single GPU.

CUDA:

```bash
pip install ctransformers[cuda] --no-binary ctransformers --no-cache --no-binary ctransformers --force
```

Mac M1/2:

```bash
CT_METAL=1 hatch run pip install ctransformers --no-binary ctransformers --no-cache --no-binary ctransformers --force # for m1
```

## Contributing

We would ❤️ to collaborate with you. Check out the [DEVELOPER GUIDE](https://github.com/holoviz-topics/panel-chat-examples/blob/main/DEVELOPER_GUIDE.md) for to get started.

## License

This project is licensed under the terms of the [MIT license](https://github.com/holoviz-topics/panel-chat-examples/blob/main/LICENSE.md).
