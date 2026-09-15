
"""
Build an Android debug APK for the YtDownload application.

This script is intended to be run from the WSL/Linux Android build
environment after the project's Python virtual environment has been
activated.

The script:
1. Verifies that Python 3.11 is being used.
2. Determines the YtDownload project root directory.
3. Adds the project root to Python's module search path so that project
   modules can be imported.
4. Runs Buildozer from the project root to create an Android debug APK.
"""

from pathlib import Path
import subprocess
import sys

# Determine the absolute path of the YtDownload project root.
# This file is located in scripts_android, so its second parent directory
# is the project root.
parent_dir = str(Path(__file__).resolve().parents[1])

# Add the project root to Python's module search path so that project
# modules can be imported regardless of the directory from which this
# script is executed.
sys.path.append(parent_dir)

from utils.enviroment import isPythonRightVersion

def main():
    """
    Verify the Python version and build the Android debug APK.

    Buildozer is executed from the project root because the project's
    buildozer.spec file is located there.
    """

    # The Android build environment uses Python 3.11.
    # Check the active Python interpreter before starting the build so
    # that the build does not proceed with an unsupported Python version.
    if not isPythonRightVersion(3, 11):
        raise Exception("Error: python is not the correct version")

    # Use the YtDownload project root as the working directory for the
    # Buildozer command.
    wsl_project_dir = parent_dir
    print("wsl_project_dir: ", wsl_project_dir)

    # Run Buildozer from the project root to create an Android debug APK.
    #
    # shell=True allows the command to be executed through the shell.
    # check=True causes Python to raise an exception if Buildozer fails.
    # cwd ensures Buildozer runs from the directory containing
    # buildozer.spec.
    subprocess.run(
        "buildozer android debug",
        shell=True,
        check=True,
        cwd=str(wsl_project_dir)
    )

# Only run the build when this file is executed directly.
# This prevents the build from starting if the module is imported elsewhere.
if __name__ == "__main__":
    main()
