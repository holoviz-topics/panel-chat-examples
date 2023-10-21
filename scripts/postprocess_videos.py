import subprocess
from pathlib import Path

# this directory
THIS_DIR = Path(__file__).parent
ASSETS_DIR = THIS_DIR.parent / "docs" / "assets"
TEST_RESULTS_DIR = THIS_DIR.parent / "test-results"
THUMBNAILS_DIR = ASSETS_DIR / "thumbnails"
VIDEOS_DIR = ASSETS_DIR / "videos"

webm_paths = TEST_RESULTS_DIR.rglob("*.webm")
png_paths = TEST_RESULTS_DIR.rglob("*.png")
for webm_path, png_path in zip(webm_paths, png_paths):
    # examples-...-openai-openai-chat-py-chromium -> openai_chat
    example_name = "_".join(
        webm_path.parent.name.split("examples-")[-1].split("-")[1:-1]
    ).replace("_py", "")
    mp4_path = (VIDEOS_DIR / example_name).with_suffix(".mp4").absolute()
    print(f"Converting {webm_path} to {mp4_path}")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(webm_path),
            "-ss",
            "00:00:01.000",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "22",
            "-c:a",
            "copy",
            str(mp4_path),
        ]
    )

    thumbnail_path = (THUMBNAILS_DIR / example_name).with_suffix(".png").absolute()
    print(f"Moving {png_path} to {thumbnail_path}")
    png_path.rename(thumbnail_path)
