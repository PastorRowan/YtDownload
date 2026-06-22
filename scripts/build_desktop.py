
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

def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"

def main():

    DEST_BIN = config.paths.packaged_dest_bin()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--distpath", str(config.PATHS.DIST_DIR),
            "--add-binary", addBinary(config.paths.executable("ffmpeg"), DEST_BIN),
            "--add-binary", addBinary(config.paths.executable("ffprobe"), DEST_BIN),
            "--add-binary", addBinary(config.paths.executable("qjs"), DEST_BIN),
            "main.py"
        ],
        check=True,
        cwd=str(config.paths.base())
    )

if __name__ == "__main__":
    main()
