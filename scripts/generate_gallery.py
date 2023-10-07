"""Generates a markdown file describing the examples apps"""

from pathlib import Path
from textwrap import dedent, indent

DOCS_PATH = Path(__file__).parent.parent / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
INDEX_MD_PATH = DOCS_PATH / "index.md"
THUMBNAILS_PATH = DOCS_PATH / "assets" / "thumbnails"


def run():
    """Generates a Gallery markdown file describing all the example

    Generates the text description looping the inside the EXAMPLES_PATH recursively

    - For each folder a header "## Folder Name" is added to the text
    - For each .py file of a header is added "### File Name" to the text as well as the
    content of the module docstring.
    """

    text = dedent(
        """
        # Examples

        To run all of these examples locally:
        ```bash
        git clone https://github.com/holoviz-topics/panel-chat-examples
        cd panel-chat-examples
        pip install hatch
        hatch run panel-serve
        ```

        Note the default installation is not optimized for GPU usage. To enable GPU
        support for local models (i.e. not OpenAI), install `ctransformers` with the
        proper backend and modify the scripts configs' accordingly, e.g.
        `n_gpu_layers=1` for a single GPU.
        """
    )
    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name == "examples":
            continue
        text += f"\n## {folder.name.title()}\n"

        # Loop through each .py file in the folder
        for file in sorted(folder.glob("*.py")):
            title = file.name.replace(".py", "").replace("_", " ").title()
            source_path = file.relative_to(EXAMPLES_PATH.parent)
            text += f"\n### {title}\n"

            with open(file) as f:
                docstring_lines = []
                in_docstring = False
                for line in f:
                    if in_docstring:
                        if '"""' in line:
                            break
                        docstring_lines.append(line.strip())
                    elif '"""' in line:
                        in_docstring = True

                thumbnail = THUMBNAILS_PATH / file.name.replace(".py", ".png")
                if thumbnail.exists():
                    thumbnail_str = (
                        "\n"
                        f'[<img src="{thumbnail.relative_to(EXAMPLES_PATH.parent)}" '
                        f'alt="{title}" style="max-height: 400px; max-width: 100%;">]'
                        f"({source_path})\n"
                    )
                    docstring_lines.append(thumbnail_str)
                docstring_lines.append(
                    f"<details>\n"
                    f"<summary>Source code for <a href='{source_path}' "
                    f"target='_blank'>{source_path.name}</a></summary>\n"
                    f"```python\n"
                    f"{indent(file.read_text(), '' * 4).rstrip()}\n"
                    f"```\n"
                    "</details>\n"
                )

                docstring = "\n".join(docstring_lines)

                text += f"\n{docstring}\n"

    # Write the text to the index.md file
    with open(INDEX_MD_PATH, "w") as f:
        f.write(text)


if __name__.startswith("__main__"):
    run()
