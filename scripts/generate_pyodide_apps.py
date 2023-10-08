"""Converts the examples to pyodide apps"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

NUM_THREADS = 20

DOCS_PATH = Path(__file__).parent.parent / "docs"
EXAMPLES_PATH = DOCS_PATH / "examples"
APP_PATH = DOCS_PATH / "pyodide"


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
            files.append(file)
    return files


def run():
    """Converts the examples to pyodide apps"""
    with ThreadPoolExecutor(NUM_THREADS) as executor:
        for _ in executor.map(_convert, _get_files()):
            pass


if __name__.startswith("__main__"):
    run()
