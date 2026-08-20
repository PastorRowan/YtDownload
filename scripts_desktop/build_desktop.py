
"""
Builds a binary for the desktop operating system you run this command on
with the venv requirements installed
"""

import os
from pathlib import Path
import subprocess
import sys

parent_folder_path = Path(__file__).resolve().parents[1]

sys.path.append(str(parent_folder_path))

import config

import utils

def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"

def main():

    utils.isPythonRightVersion(3, 13)

    SPECPATH_DIR = config.paths.pyinstaller_spec()
    WORKPATH_DIR = config.paths.pyinstaller_workpath_dir()
    DIST_DIR = config.paths.dist_dir()
    DEST_BIN = config.paths.packaged_dest_bin()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",

            #"--noconsole",

            # 2 output modes: --onedir or --onefile
            # enable --onefile to make the exe all in one file
            # remember that on every startup the app copies all needed
            # files into a temp dir before running the program so HUGE overhead
            # prefer --onedir because startup overhead is greatly reduced
            #"--onefile",
            "--onedir",

            # Fresh build
            # "--clean",

            "--hidden-import", "kivy.core.image.img_sdl2",
            "--collect-submodules", "kivy.core.image",
            "--collect-data", "kivy.core.image",
            "--collect-all", "kivymd",

            "--specpath", str(SPECPATH_DIR),
            "--workpath", str(WORKPATH_DIR),
            "--distpath", str(DIST_DIR),

            "--add-binary", addBinary(config.paths.executable("ffmpeg"), DEST_BIN),
            "--add-binary", addBinary(config.paths.executable("ffprobe"), DEST_BIN),
            "--add-binary", addBinary(config.paths.executable("qjs"), DEST_BIN),

            "main.py"

        ],
        check=True,
        cwd=str(parent_folder_path)
    )

if __name__ == "__main__":
    main()
