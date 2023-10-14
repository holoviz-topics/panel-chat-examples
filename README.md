# Panel Chat Examples

[![build](https://github.com/holoviz-topics/panel-chat-examples/workflows/Build/badge.svg)](https://github.com/holoviz-topics/panel-chat-examples/actions)
[![codecov](https://codecov.io/gh/holoviz-topics/panel-chat-examples/branch/master/graph/badge.svg)](https://codecov.io/gh/holoviz-topics/panel-chat-examples)
[![PyPI version](https://badge.fury.io/py/panel-chat-examples.svg)](https://badge.fury.io/py/panel-chat-examples)

Examples of chat components using Panel; supports LangChain, OpenAI, Mistral, Llama, etc.

**Documentation**: <a href="https://holoviz-topics.github.io/panel-chat-examples/" target="_blank">https://holoviz-topics.github.io/panel-chat-examples/</a>

THIS PROJECT IS IN EARLY STAGE AND WILL CHANGE!

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

---

## Contributing

We would ❤️ to collaborate with you. Check out the [DEVELOPER GUIDE](https://github.com/holoviz-topics/panel-chat-examples/blob/main/DEVELOPER_GUIDE.md) for to get started.

## License

This project is licensed under the terms of the MIT license.
