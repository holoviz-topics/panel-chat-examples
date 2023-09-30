"""Generates a markdown file describing the examples apps"""

from pathlib import Path

EXAMPLES_PATH = Path(__file__).parent.parent / "examples"
INDEX_MD_PATH = EXAMPLES_PATH / "index.md"
THUMBNAILS_PATH = Path(__file__).parent.parent / "assets" / "thumbnails"


def run():
    """Generates a Gallery markdown file describing all the example

    Generates the text description looping the inside the EXAMPLES_PATH recursively

    - For each folder a header "## Folder Name" is added to the text
    - For each .py file of a header is added "### File Name" to the text as well as the content of the
    module docstring.
    """

    text = """  
# Panel Chat Examples Gallery
"""
    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        text += f"\n## [{folder.name.title()}]({folder.relative_to(EXAMPLES_PATH)})\n"

        # Loop through each .py file in the folder
        for file in folder.glob("*.py"):
            title = file.name.replace(".py", "").replace("_", " ").title()
            text += f"\n### [{title}]({file.relative_to(EXAMPLES_PATH)})\n"

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
                    docstring_lines.append(
                        f"\n![{title}](../{thumbnail.relative_to(EXAMPLES_PATH.parent)})"
                    )

                docstring = "\n".join(docstring_lines)

                text += f"\n{docstring}\n"

    # Write the text to the index.md file
    with open(INDEX_MD_PATH, "w") as f:
        f.write(text)


if __name__.startswith("__main__"):
    run()
