
"""
Builds an APK for android OS
"""

import os
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import CONFIG

# DEST_BIN = CONFIG.PATHS.DEST_BIN

"""
def addBinary(src, dest) -> str:
    return f"{src}{os.pathsep}{dest}"
"""

def convertWindowsPathToLinuxPath(path: Path) -> str:
    path = path.resolve()

    drive = path.drive[0].lower()
    rest = path.as_posix().split(":", 1)[1]

    return f"/mnt/{drive}{rest}"

def main():

    wsl_project_dir = convertWindowsPathToLinuxPath(CONFIG.PROJECT.DIR)

    subprocess.run(
        [
            "wsl.exe",
            "-d",
            "Ubuntu-26.04",
            "--",
            "bash",
            "-lc",
            (
                "sudo apt update && "
                "sudo apt install -y "
                "git "
                "zip "
                "unzip "
                "openjdk-17-jdk "
                "python3.11 "
                "python3.11-pip "
                "python3.11-venv "
                "build-essential "
                "autoconf "
                "automake "
                "libtool "
                "libcairo2-dev "
                "pkg-config "
                "zlib1g-dev "
                "libgl1-mesa-glx "
                "libgles2-mesa "
                "libegl1-mesa "
                "libmtdev1 "
                "cmake && "
            ) + (
                f"cd '{wsl_project_dir}' && "
                "[ -d venv-linux ] || python3 -m venv venv-linux && "
                "source venv-linux/bin/activate && "
                "pip install --upgrade pip && "
                "pip install -r android-build-requirements.txt"
            )
        ],
        check=True
    )

if __name__ == "__main__":
    main()
