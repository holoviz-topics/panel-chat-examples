"""Generates a markdown file describing the examples apps"""

from pathlib import Path
from textwrap import dedent, indent

from convert_apps import APPS_READY_FOR_PYODIDE

ROOT_PATH = Path(__file__).parent.parent
README_PATH = ROOT_PATH / "README.md"
DOCS_PATH = ROOT_PATH / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
INDEX_MD_PATH = DOCS_PATH / "index.md"
THUMBNAILS_PATH = DOCS_PATH / "assets" / "thumbnails"
VIDEOS_PATH = DOCS_PATH / "assets" / "videos"
# ruff: noqa: E501
VIDEO_URL = "https://github.com/holoviz-topics/panel-chat-examples/assets/42288570/cdb78a39-b98c-44e3-886e-29de6a079bde"
VIDEO_TAG = """\
<video controls style="height:auto;width: 100%;max-height:500px" poster="assets/videos/panel-chat-examples-splash.png">
    <source src="assets/videos/panel-chat-examples-splash.mp4" type="video/mp4">
</video>"""

DESCRIPTION = {
    "chat_features": (
        "Highlights some features of Panel's chat components; "
        "they do not require other packages besides Panel."
    ),
    "applicable_recipes": (
        "Demonstrates how to use Panel's chat components to "
        "achieve specific tasks with popular LLM packages."
    ),
    "kickstart_snippets": (
        "Quickly start using Panel's chat components with popular LLM packages "
        "by copying and pasting one of these snippets. All of these examples support:\n\n"
        "- Streaming\n"
        "- Async\n"
        "- Memory\n"
    ),
}

ORDERING = {
    "chat_features": [
        "echo_chat.py",
        "stream_echo_chat.py",
        "custom_input_widgets.py",
        "delayed_placeholder.py",
        "chained_response.py",
    ]
}


def _copy_readme_to_index():
    text = README_PATH.read_text()
    text = text.replace(VIDEO_URL, VIDEO_TAG)
    INDEX_MD_PATH.write_text(text)


def run():
    """Generates a Gallery markdown file describing all the example

    Generates the text description looping the inside the EXAMPLES_PATH recursively

    - For each folder a header "## Folder Name" is added to the text
    - For each .py file of a header is added "### File Name" to the text as well as the
    content of the module docstring.
    """
    _copy_readme_to_index()

    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name not in DESCRIPTION.keys():
            continue

        # Loop through each .py file in the folder
        docs_file_path = DOCS_PATH / folder.with_suffix(".md").name
        description = DESCRIPTION[folder.name]
        text = f"\n# {folder.name.title().replace('_', ' ')}\n{description}\n"

        ordering = ORDERING.get(folder.name, [])
        files = sorted(
            folder.glob("*.py"),
            key=lambda file: (
                ordering.index(file.name) if file.name in ordering else 999
            ),
        )
        for file in files:
            title = (
                file.name.replace(".py", "")
                .replace("_", " ")
                .strip()
                .title()
                .rstrip("_")
            )
            parent_path = Path("..")
            source_path = parent_path / file.relative_to(EXAMPLES_PATH.parent)
            text += f"\n## {title}\n"

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

                thumbnail = THUMBNAILS_PATH / file.name.replace(".py", ".png").replace(
                    "_.png", ".png"
                )
                video = VIDEOS_PATH / file.name.replace(".py", ".mp4").replace(
                    "_.mp4", ".mp4"
                )

                print(video, video.exists())
                if video.exists() and thumbnail.exists():
                    video_str = dedent(
                        f"""
                        <video controls poster="{parent_path / thumbnail.relative_to(EXAMPLES_PATH.parent)}" >
                            <source src="{parent_path / video.relative_to(EXAMPLES_PATH.parent)}" type="video/mp4"
                            style="max-height: 400px; max-width: 600px;">
                            Your browser does not support the video tag.
                        </video>\n
                        """  # noqa: E501
                    )
                    docstring_lines.append(video_str)
                elif thumbnail.exists():
                    thumbnail_str = (
                        "\n"
                        f'[<img src="{parent_path / thumbnail.relative_to(EXAMPLES_PATH.parent)}" '  # noqa: E501
                        f'alt="{title}" style="max-height: 400px; max-width: 600px%;">]'  # noqa: E501
                        f"({source_path})\n"
                    )
                    docstring_lines.append(thumbnail_str)
                docstring_lines.append(
                    f"\n<details>\n\n"
                    f"<summary>Source code for <a href='{source_path}' "
                    f"target='_blank'>{source_path.name}</a></summary>\n\n"
                    f"```python\n"
                    f"{indent(file.read_text(), '' * 4).rstrip()}\n"
                    f"```\n"
                    "</details>\n"
                )
                if file.name in APPS_READY_FOR_PYODIDE:
                    docstring_lines.append(
                        f"""\
Live Apps: <a href='../pyodide/{file.name.replace(".py", ".html")}' \
target='_blank' title='The app is running entirely in the browser powered by Pyodide'\
>Pyodide</a>"""
                    )
                docstring = "\n".join(docstring_lines)
                text += f"\n{docstring}\n"

        docs_file_path.write_text(text.strip())


if __name__.startswith("__main__"):
    run()
