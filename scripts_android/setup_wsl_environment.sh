
#!/usr/bin/env bash

# Determine the absolute path of the directory containing this script.
# This allows the script to locate the project directory regardless of
# the directory from which the script is executed.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# The script is located in the scripts_android directory, so its parent
# directory is the root directory of the YtDownload project.
SCRIPT_PARENT_DIR="$SCRIPT_DIR/.."

# Stop the script immediately if any command returns a non-zero exit status.
set -e

# Update the local APT package lists before installing packages.
echo "Updating package lists..."
sudo apt update

# Check whether Git is already installed.
# Git is required by the Android build environment and python-for-android.
echo "Checking for Git..."
if command -v git >/dev/null 2>&1; then
    # Git is already installed, so display its installed version.
    echo "Git is already installed: $(git --version)"
else
    # Git is not installed, so install it using APT.
    echo "Git is not installed. Installing Git..."
    sudo apt install -y git
fi

# Install software-properties-common.
# This package provides tools such as add-apt-repository, which is used
# below to add the Deadsnakes PPA (personal package archive).
echo "Installing software-properties-common..."
sudo apt install -y software-properties-common

# Add the Deadsnakes PPA.
# The PPA provides additional Python versions that may not be available
# in the default Ubuntu repositories.
echo "Adding deadsnakes PPA..."
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Update the APT package lists again so that packages provided by the
# newly added PPA are available for installation.
echo "Updating package lists..."
sudo apt update

# Install Python 3.11 and the packages required to create Python virtual
# environments and compile Python packages with native components.
#
# python3.11 - Python 3.11 interpreter
# python3.11-venv - Support for creating Python virtual environments
# python3.11-dev - Python development headers and files
echo "Installing Python 3.11..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev

# Install the system-level dependencies required by Buildozer,
# python-for-android, and their native build dependencies.
#
# git - Version control and source retrieval
# zip/unzip - Archive creation and extraction
# openjdk-17-jdk - Java Development Kit required by the Android toolchain
# build-essential - C/C++ compiler and standard build tools
# autoconf - Generates portable build configuration scripts
# automake - Generates Makefile templates
# libtool - Builds and manages portable native libraries
# libcairo2-dev - Cairo graphics development library
# pkg-config - Locates installed development libraries
# zlib1g-dev - Compression library development files
# libssl-dev - OpenSSL development files
# openssl - OpenSSL command-line tools
# ca-certificates - Trusted CA certificates for secure connections
# libffi-dev - Foreign Function Interface development library
# cmake - Cross-platform build system
echo "Installing build dependencies..."
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    build-essential \
    autoconf \
    automake \
    libtool \
    libcairo2-dev \
    pkg-config \
    zlib1g-dev \
    libssl-dev \
    openssl \
    ca-certificates \
    libffi-dev \
    cmake

# Verify that Python 3.11 was installed successfully.
echo "Checking Python..."
python3.11 --version

# Move from the scripts_android directory to the YtDownload project root.
# The virtual environment is created in the project root so that it can
# be shared by the project's Android build scripts.
echo "Moving up to parent directory..."
cd "$SCRIPT_PARENT_DIR"

# Create a Python 3.11 virtual environment named "venv".
# This isolates the Python packages required by the Android build
# environment from the system Python installation.
echo "Creating Python 3.11 virtual environment..."
python3.11 -m venv venv

# Activate the newly created virtual environment.
# This ensures that packages installed with pip are installed into the
# project's virtual environment rather than the system Python installation.
echo "Activating virtual environment..."
source venv/bin/activate

# Verify that pip is available inside the virtual environment.
echo "Checking pip..."
python3.11 -m pip --version

# Install Buildozer and Cython into the project's virtual environment.
#
# Buildozer is used to automate the process of packaging the Python
# application for Android.
#
# Cython is required by parts of the Python-to-Android build toolchain.
echo "Installing Buildozer and Cython..."
python3.11 -m pip install buildozer cython

# The WSL/Linux environment is now prepared for the Android build process.
echo "Buildozer environment setup complete!"
