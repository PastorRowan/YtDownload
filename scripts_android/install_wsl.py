
"""
Installs WSL. Must be run in Windows 11 command line like powershell or command prompt
"""

import subprocess

def main():
    
    subprocess.run(
        args="wsl.exe --install -d Ubuntu-24.04",
        shell=True,
        check=True
    )

if __name__ == "__main__":
    main()
