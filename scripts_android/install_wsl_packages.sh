
#!/usr/bin/env bash

set -e

echo "Updating package lists..."
sudo apt update

echo "Checking for Git..."

if command -v git >/dev/null 2>&1; then
    echo "Git is already installed: $(git --version)"
else
    echo "Git is not installed. Installing Git..."
    sudo apt install -y git
fi

echo "Installing software-properties-common..."
sudo apt install -y software-properties-common

echo "Adding deadsnakes PPA..."
sudo add-apt-repository ppa:deadsnakes/ppa -y

echo "Updating package lists..."
sudo apt update

echo "Installing Python 3.11..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev

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

echo "Checking Python..."
python3.11 --version
python3.11 -m pip --version

echo "Installing Buildozer and Cython..."
python3.11 -m pip install buildozer cython

echo "Buildozer environment setup complete!"
