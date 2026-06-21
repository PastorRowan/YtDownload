
"""
Builds a binary for the desktop operating system you run this command on
with the venv requirements installed
"""

import os
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

DEST_BIN = config.PATHS.DEST_BIN

def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"

def main():

    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--distpath", str(config.PATHS.DIST_DIR),
            "--add-binary", addBinary(config.PATHS.FFMPEG_BIN_PATH, DEST_BIN),
            "--add-binary", addBinary(config.PATHS.FFPROBE_BIN_PATH, DEST_BIN),
            "--add-binary", addBinary(config.PATHS.QUICK_JS_BIN_PATH, DEST_BIN),
            "main.py"
        ], check=True, cwd=str(config.PROJECT.DIR)
    )

if __name__ == "__main__":
    main()
