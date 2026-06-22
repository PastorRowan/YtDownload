
"""
Builds an APK for android OS
"""

from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

def main():

    wsl_project_dir = str(config.paths.base())

    print("wsl_project_dir: ", wsl_project_dir)

    subprocess.run(
        "buildozer android debug",
        shell=True,
        check=True,
        cwd=str(wsl_project_dir)
    )

if __name__ == "__main__":
    main()
