# Panel Chat Examples

<p align="center">
    <em>Example recipes for Panel ChatInterface.</em>
</p>

THIS PROJECT IS IN EARLY STAGE AND WILL CHANGE!

The examples are based on the next generation of chat features being developed in [PR #5333](https://github.com/holoviz/panel/pull/5333)

To run the examples:
- `hatch run panel serve examples/**/*.py --static-dirs thumbnails=./assets/thumbnails --autoreload`

[![build](https://github.com/holoviz-topics/panel-chat-examples/workflows/Build/badge.svg)](https://github.com/holoviz-topics/panel-chat-examples/actions)
[![codecov](https://codecov.io/gh/holoviz-topics/panel-chat-examples/branch/master/graph/badge.svg)](https://codecov.io/gh/holoviz-topics/panel-chat-examples)
[![PyPI version](https://badge.fury.io/py/panel-chat-examples.svg)](https://badge.fury.io/py/panel-chat-examples)

---

**Documentation**: <a href="https://holoviz-topics.github.io/panel-chat-examples/" target="_blank">https://holoviz-topics.github.io/panel-chat-examples/</a>

**Source Code**: <a href="https://github.com/holoviz-topics/panel-chat-examples" target="_blank">https://github.com/holoviz-topics/panel-chat-examples</a>

---

## Development

### Clone repository

`git clone https://github.com/holoviz-topics/panel-chat-examples.git`

### Setup environment

We use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it's installed on your system with `pip install hatch`

### Run unit tests

You can run all the tests with:

```bash
hatch run test
```

### Format the code

Execute the following command to apply linting and check typing:

```bash
hatch run lint
```

### Publish a new version

You can bump the version, create a commit and associated tag with one command:

```bash
hatch version patch
```

```bash
hatch version minor
```

```bash
hatch version major
```

Your default Git text editor will open so you can add information about the release.

When you push the tag on GitHub, the workflow will automatically publish it on PyPi and a GitHub release will be created as draft.

## Serve the documentation

You can serve the Mkdocs documentation with:

```bash
python scripts/generate_gallery.py
hatch run docs-serve
```

It'll automatically watch for changes in your code.

## License

This project is licensed under the terms of the MIT license.
