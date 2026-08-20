
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

def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"

def main():

    REQUIRED_MAJOR = 3
    REQUIRED_MINOR = 13
    REQUIRED_MICRO = -1

    CURRENT_MAJOR = sys.version_info.major
    CURRENT_MINOR = sys.version_info.minor
    CURRENT_MICRO = sys.version_info.micro

    isRightVersion = False

    if (REQUIRED_MAJOR != -1) and (REQUIRED_MAJOR != CURRENT_MAJOR):
        isRightVersion = False
    elif (REQUIRED_MINOR != -1) and (REQUIRED_MINOR != CURRENT_MINOR):
        isRightVersion = False
    elif (REQUIRED_MICRO != -1) and (REQUIRED_MICRO != CURRENT_MICRO):
        isRightVersion = False
    else:
        isRightVersion = True

    if not isRightVersion:

        def version_number_to_str(version: int) -> str:
            if version == -1:
                return "x"
            return str(version)

        REQUIRED_MAJOR_STR = version_number_to_str(REQUIRED_MAJOR)
        REQUIRED_MINOR_STR = version_number_to_str(REQUIRED_MINOR)
        REQUIRED_MICRO_STR = version_number_to_str(REQUIRED_MICRO)

        CURRENT_MAJOR_STR = version_number_to_str(CURRENT_MAJOR)
        CURRENT_MINOR_STR = version_number_to_str(CURRENT_MINOR)
        CURRENT_MICRO_STR = version_number_to_str(CURRENT_MICRO)

        print(
            f"\nERROR: This build script must be run with Python "
            f"{REQUIRED_MAJOR_STR}.{REQUIRED_MINOR_STR}.{REQUIRED_MICRO_STR}"
            f" You are using {CURRENT_MAJOR_STR}.{CURRENT_MINOR_STR}.{CURRENT_MICRO_STR}"
        )
        return

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
