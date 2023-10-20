"""Converts the examples to pyodide apps"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess

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
