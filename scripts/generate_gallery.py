"""Generates a markdown file describing the examples apps"""

from pathlib import Path
from textwrap import dedent, indent

DOCS_PATH = Path(__file__).parent.parent / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
INDEX_MD_PATH = DOCS_PATH / "index.md"
THUMBNAILS_PATH = DOCS_PATH / "assets" / "thumbnails"
VIDEOS_PATH = DOCS_PATH / "assets" / "videos"
PREFIX = {"basics": "basic", "components": "component", "features": "feature"}


def run():
    """Generates a Gallery markdown file describing all the example

    Generates the text description looping the inside the EXAMPLES_PATH recursively

    - For each folder a header "## Folder Name" is added to the text
    - For each .py file of a header is added "### File Name" to the text as well as the
    content of the module docstring.
    """

    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name in ["examples", "__pycache__"]:
            continue

        # Loop through each .py file in the folder
        docs_file_path = DOCS_PATH / folder.with_suffix(".md").name
        text = f"\n# {folder.name.title()}\n"

        for file in sorted(folder.glob("*.py")):
            prefix = PREFIX.get(folder.name, folder.name)

            title = (
                file.name.replace(".py", "")
                .replace("_", " ")
                .replace(prefix, "")
                .strip()
                .title()
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

                thumbnail = THUMBNAILS_PATH / file.name.replace(".py", ".png")
                video = VIDEOS_PATH / file.name.replace(".py", ".webm")

                if video.exists() and thumbnail.exists():
                    video_str = dedent(
                        f"""
                        <video controls poster="{parent_path / thumbnail.relative_to(EXAMPLES_PATH.parent)}" >
                            <source src="{parent_path / video.relative_to(EXAMPLES_PATH.parent)}" type="video/webm"
                            style="max-height: 400px; max-width: 600px;">
                            Your browser does not support the video tag.
                        </video>\n
                        """
                    )
                    docstring_lines.append(video_str)
                elif thumbnail.exists():
                    thumbnail_str = (
                        "\n"
                        f'[<img src="{parent_path / thumbnail.relative_to(EXAMPLES_PATH.parent)}" '
                        f'alt="{title}" style="max-height: 400px; max-width: 600px%;">]'
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
                docstring = "\n".join(docstring_lines)
                text += f"\n{docstring}\n"

        docs_file_path.write_text(text.strip())


if __name__.startswith("__main__"):
    run()
