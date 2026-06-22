
"""
Installs WSL packages to build android APK with bulldozer and creates venv
"""

from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

def main():
    
    subprocess.run("sudo apt update", shell=True, check=True)
    
    subprocess.run("sudo apt install software-properties-common -y", shell=True, check=True)
    
    subprocess.run("sudo add-apt-repository ppa:deadsnakes/ppa -y", shell=True, check=True)
    
    subprocess.run("sudo apt update", shell=True, check=True)
    
    subprocess.run("sudo apt install python3.11 -y", shell=True, check=True)
    
    subprocess.run("sudo apt update", shell=True, check=True)
    
    subprocess.run("sudo apt install python3.11-venv -y", shell=True, check=True)
    
    subprocess.run("sudo apt update", shell=True, check=True)

    subprocess.run("sudo apt install python3.11-dev -y", shell=True, check=True)
    
    subprocess.run("sudo apt update", shell=True, check=True)
    
    subprocess.run((
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
        "cmake"
    ), shell=True, check=True)
    
    subprocess.run("sudo apt update", shell=True, check=True)
    
    subprocess.run("python3.11 -m pip --version", shell=True, check=True)

    subprocess.run(
        "python3.11 -m pip install buildozer cython",
        shell=True,
        check=True
    )

if __name__ == "__main__":
    main()
