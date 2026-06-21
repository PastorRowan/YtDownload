
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

    windows_path = Path(CONFIG.PROJECT.DIR)

    print("windows_path = ", windows_path)

    drive = windows_path.drive.rstrip(":").lower()
    rest = windows_path.parts[1:]

    wsl_project_dir = f"/mnt/{drive}/{'/'.join(rest)}"

    print("wsl_project_dir: ", wsl_project_dir)

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
                "sudo apt install python3.11-dev && "
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
                "libssl-dev "
                "openssl "
                "ca-certificates "
                "libffi-dev "
                "cmake && "
                "sudo apt update && "
            ) + (
                f"cd '{wsl_project_dir}' && "
                "if [ ! -d venv-linux ]; then "
                "python3.11 -m venv venv-linux; fi && "
                "source venv-linux/bin/activate && "
                "pip install --upgrade pip && "
                "pip install -r android-build-requirements.txt"
            )
        ],
        check=True
    )

if __name__ == "__main__":
    main()
