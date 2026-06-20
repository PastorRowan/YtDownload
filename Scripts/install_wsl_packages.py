
"""
Builds an APK for android OS
"""

import os
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import CONFIG

def main():

    wsl_project_dir = CONFIG.LINUX.DIR

    subprocess.run(
        [
            "wsl.exe",
            "-d",
            "Ubuntu-24.04",
            "--",
            "bash",
            "-lc",
            (
                "sudo apt update && "
                "sudo apt install software-properties-common && "
                "sudo add-apt-repository ppa:deadsnakes/ppa && "
                "sudo apt update && "
                "sudo apt install python3.11 && "
                "sudo apt update && "
                "sudo apt install python3.11-venv && "
                "sudo apt update && "
                "sudo apt install -y "
                "git "
                "zip "
                "unzip "
                "openjdk-17-jdk "
                "build-essential "
                "autoconf "
                "automake "
                "libtool "
                "libcairo2-dev "
                "pkg-config "
                "zlib1g-dev "
                "cmake && "
            ) + (
                f"cd '{wsl_project_dir}' && "
                "[ -d venv-linux ] || python3.11 -m venv venv-linux && "
                "source venv-linux/bin/activate && "
                "pip install --upgrade pip && "
                "pip install -r android-build-requirements.txt"
            )
        ],
        check=True
    )

if __name__ == "__main__":
    main()
