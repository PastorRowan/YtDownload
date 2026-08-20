
"""
Builds an APK for android OS
"""

from pathlib import Path
import subprocess
import sys

parent_dir = str(Path(__file__).resolve().parents[1])

sys.path.append(parent_dir)

import utils

def main():

    utils.enviroment.isPythonRightVersion(3, 11)

    wsl_project_dir = parent_dir

    print("wsl_project_dir: ", wsl_project_dir)

    subprocess.run(
        "buildozer android debug",
        shell=True,
        check=True,
        cwd=str(wsl_project_dir)
    )

if __name__ == "__main__":
    main()
