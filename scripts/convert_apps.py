"""Converts the examples to pyodide apps"""

import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

NUM_THREADS = 20

DOCS_PATH = Path(__file__).parent.parent / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
APP_PATH = DOCS_PATH / "pyodide"

APPS_READY_FOR_PYODIDE = [
    "basic_chat.py",
    "basic_streaming_chat.py",
    "basic_streaming_chat_async.py",
    # "component_environment_widget.py", # imports panel_chat_examples
    "feature_chained_response.py",
    "feature_delayed_placeholder.py",
    # "feature_replace_response.py", # https://github.com/holoviz/panel/issues/5700
    "feature_slim_interface.py",
]

BEFORE = """\
    <meta charset="utf-8">
    <title>Panel Application</title>"""

AFTER = """\
    <meta charset="utf-8">
    <meta name= “description” content="An example of a HoloViz Panel chat app powered \
by Pyodide">
    <meta name="author" content="Panel Chat Examples">
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:site" content="@Panel_org" />
    <meta name="twitter:creator" content="@Panel_org" />
    <meta property="og:image" content="https://holoviz-topics.github.io/panel-chat-examples/assets/thumbnails/{image_name}">
    <meta property="og:description" content="An example of a HoloViz Panel chat app \
powered by Pyodide">
    <meta property="og:title" content="{app_title} | Panel Chat Examples">
    <meta property="og:type" content="website">
    <meta property="og:video:url" content="https://holoviz-topics.github.io/\
panel-chat-examples/assets/videos/{video_name}">
    <meta property="og:video:secure_url" content="https://holoviz-topics.github.io/\
panel-chat-examples/assets/videos/{video_name}">
    <meta property="og:video:width" content="1699">
    <meta property="og:video:height" content="900">
    <link rel="icon" href="../assets/images/favicon.png">
    <title>{app_title} | Panel Chat Examples</title>"""


def _replace(file):
    html_file = APP_PATH / file.name.replace(".py", ".html")
    content = html_file.read_text(encoding="utf-8")
    app_title = file.name.replace(".py", "").replace("_", " ").title()
    image_name = file.name.replace(".py", ".png")
    video_name = file.name.replace(".py", ".mp4")
    after = AFTER.format(
        app_title=app_title,
        image_name=image_name,
        video_name=video_name,
    )
    content = content.replace(BEFORE, after)
    html_file.write_text(content, encoding="utf-8")


def _convert(file):
    print(f"converting {file}")
    subprocess.run(
        [
            "panel",
            "convert",
            str(file),
            "--to",
            "pyodide-worker",
            "--out",
            str(APP_PATH),
        ]
    )
    _replace(file)


def _get_files():
    files = []
    for folder in sorted(EXAMPLES_PATH.glob("**/"), key=lambda folder: folder.name):
        if folder.name == "examples":
            continue

        for file in sorted(folder.glob("*.py")):
            if file.name in APPS_READY_FOR_PYODIDE:
                files.append(file)
    return files


def _clean_app_folder():
    if APP_PATH.exists():
        shutil.rmtree(APP_PATH)


def run():
    """Converts the examples to pyodide apps"""
    _clean_app_folder()

    with ThreadPoolExecutor(NUM_THREADS) as executor:
        for _ in executor.map(_convert, _get_files()):
            pass


if __name__.startswith("__main__"):
    run()
