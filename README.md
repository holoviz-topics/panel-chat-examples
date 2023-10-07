# Panel Chat Examples

[![build](https://github.com/holoviz-topics/panel-chat-examples/workflows/Build/badge.svg)](https://github.com/holoviz-topics/panel-chat-examples/actions)
[![codecov](https://codecov.io/gh/holoviz-topics/panel-chat-examples/branch/master/graph/badge.svg)](https://codecov.io/gh/holoviz-topics/panel-chat-examples)
[![PyPI version](https://badge.fury.io/py/panel-chat-examples.svg)](https://badge.fury.io/py/panel-chat-examples)

Examples of Chat Bots using Panels chat features: Traditional, LLMs, AI Agents, LangChain, OpenAI, etc.

**Documentation**: <a href="https://holoviz-topics.github.io/panel-chat-examples/" target="_blank">https://holoviz-topics.github.io/panel-chat-examples/</a>

THIS PROJECT IS IN EARLY STAGE AND WILL CHANGE!

The examples are based on the next generation of chat features being developed in [PR #5333](https://github.com/holoviz/panel/pull/5333)

To install and serve all examples:

```bash
git clone https://github.com/holoviz-topics/panel-chat-examples
cd panel-chat-examples
pip install hatch
hatch run panel-serve
```

Note the default installation is not optimized for GPU usage. To enable GPU support for local
models (i.e. not OpenAI), install `ctransformers` with the [proper backend](https://github.com/marella/ctransformers#gpu) and modify the scripts configs' accordingly, e.g. `n_gpu_layers=1` for a single GPU.

CUDA:

```bash
pip install ctransformers[cuda]
```

Mac M1/2:

```bash
CT_METAL=1 pip install ctransformers --no-binary ctransformers  # for m1
```

---

## Contributing

Check out the [DEVELOPER GUIDE](DEVELOPER_GUIDE.md) for to get started.

## License

This project is licensed under the terms of the MIT license.
