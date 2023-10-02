# Panel Chat Examples

This project provides a collection of [examples](examples) of [Panel](https://panel.holoviz.org/)s
chat features.

The examples are based on the next generation of chat features being developed in [PR #5333](https://github.com/holoviz/panel/pull/5333).

https://github.com/ahuang11/panel-chat-examples/assets/15331990/247ed34a-aa76-4be4-8f83-70aca60af046

Your contributions would mean the world ❤️

THIS PROJECT IS AN EARLY STAGE AND WILL CHANGE!

## Get Started

Clone the repository

```bash
git clone https://github.com/ahuang11/panel-chat-examples.git
```

Navigate to the repository

```bash
cd panel-chat-examples
```

Create and activate your virtual environment

```bash
python -m venv .venv
source .venv/bin/activate # linux or windows git bash
```

Install the requirements

```bash
pip install -r requirements.txt
```

Set the `OPENAI_API_KEY` environment variable.

```bash
export OPENAI_API_KEY='sk-...' # linux or git bash on windows
```

## Serve the examples

Serve the apps

```bash
panel serve examples/**/*.py --static-dirs thumbnails=./assets/thumbnails --autoreload # linux
```

Open [http://localhost:5006](http://localhost:5006).

![Panel Index Page](assets/images/panel-chat-examples-index-page.png)