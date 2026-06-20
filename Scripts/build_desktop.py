
"""
Builds a binary for the desktop operating system you run this command on
with the venv requirements installed
"""

import os
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import CONFIG

DEST_BIN = CONFIG.PATHS.DEST_BIN

def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"

def main():

    pyinstaller_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--distpath", str(CONFIG.PATHS.DIST_DIR),
        "--add-binary", addBinary(CONFIG.PATHS.FFMPEG_BIN_PATH, DEST_BIN),
        "--add-binary", addBinary(CONFIG.PATHS.FFPROBE_BIN_PATH, DEST_BIN),
        "--add-binary", addBinary(CONFIG.PATHS.QUICK_JS_BIN_PATH, DEST_BIN),
        "main.py"
    ]

    subprocess.run(pyinstaller_cmd, check=True, cwd=str(CONFIG.PROJECT.DIR))

if __name__ == "__main__":
    main()
