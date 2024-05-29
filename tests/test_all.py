"""Test all app .py files py running them with python"""

import subprocess
from pathlib import Path

THUMBNAILS_PATH = Path.cwd() / "docs/assets/thumbnails"
VIDEOS_PATH = Path.cwd() / "docs/assets/videos"


def test_app(app_path):
    subprocess.call(["python", app_path])


def test_has_thumbnail(app_path):
    name = Path(app_path).name
    assert (THUMBNAILS_PATH / name.replace(".py", ".png")).exists()


def test_has_video(app_path):
    name = Path(app_path).name
    assert (VIDEOS_PATH / name.replace(".py", ".mp4")).exists()
