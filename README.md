
# YtDownload

A cross-platform **KivyMD application for downloading YouTube videos or audio** using <u>yt-dlp</u>.

> **Note:** YtDownload has currently been tested on only **Windows** and **Android**.

## Features
- 📥 Download YouTube videos (video and audio)
- 🎵 Download audio only
- ⚙️ Powered by yt-dlp
- 📁 Configurable download directories (Only works for Windows, Linux and MacOS at the moment)

## Supported Platforms

| Platform | Run | Build |
| --- | --- | --- |
| Windows | ✅ | ✅ |
| Linux | Not tested | ✅ |
| MacOS | Not tested | Not tested |
| Android arm64-v8a | ✅ | ✅ |

## Demo

*Add a demonstration video or GIF here.*

## Dependencies

YtDownload is built using the following Python packages:

- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Plyer](https://github.com/kivy/plyer)
- [Buildozer](https://buildozer.readthedocs.io/en/latest/)
- [PyInstaller](https://pyinstaller.org/en/stable/)

The project also requires the dependencies of the packages listed above.

Some features may additionally require external binaries, depending on the target platform and media format.

## External binaries

YtDownload requires the following external binaries for media processing and downloading:

- [FFmpeg](https://ffmpeg.org/download.html) — Media processing and audio/video conversion
- [FFprobe](https://ffmpeg.org/ffprobe.html) — Media file analysis
- [QuickJS (qjs)](https://bellard.org/quickjs/) — JavaScript runtime used by `yt-dlp`

## Getting Started

Getting started video

### Prerequisites

Before installing YtDownload, make sure the following are installed and accessible in your console environment:

- [Python](https://www.python.org/downloads/)
- [venv](https://docs.python.org/3/library/venv.html)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)

You can verify prerequisites are installed via:

Python:
```
python --version
```

venv:
```
python -m venv --help
```

pip:
```
python -m pip --version
```

Git:
```
git --version
```

#### Install external binaries

Install the required external binaries for your target development or production platform by following the instructions in the corresponding `README.md`:

- [Windows](libs/windows/README.md)
- [Linux](libs/linux/README.md)
- [MacOS](libs/macos/README.md)
- [Android arm64-v8a](libs/arm64-v8a/README.md)

### Installation 

Open a console environment with python, venv and pip installed.

**1. Clone the repository**
```
git clone https://github.com/PastorRowan/YtDownload.git
```

**2. Traverse to the project directory**
```
cd YtDownload
```

**3. Create a virtual environment**
```
python -m venv venv
```

**4. Activate the virtual environment**

- Windows:
```
.\venv\Scripts\activate.bat
```
After activation, your terminal should look similar to:
```
(venv) DriveLetter:\path\to\YtDownload>
```

- Linux/MacOS:
```
source venv/bin/activate
```
After activation, your terminal should look similar to:
```
(venv) /path/to/YtDownload$
```

**5. Install Python dependencies to virtual environment**
```
pip install -r requirements.txt
```

**6. Install required binaries**

See the [Install external binaries](#install-external-binaries) section.

**7. Run the application**
```
python main.py
```

## Build

### Prerequisites

Before building the application (applies to all platforms):
1. Follow the [Installation](#installation) instructions above.
2. Activate the project's virtual environment.
3. [Install external binaries](#install-external-binaries) for the target operating system and architecture.
4. Make sure the application can run successfully (if using a console based virtual environment, like wsl, then this step cannot be done).

### Desktop (Windows, Linux and MacOS)

Desktop builds are created using **PyInstaller**.

The desktop build must be performed on the target operating system. For example, a Windows build should be created on Windows, while a Linux build should be created on Linux.

The build script uses the Python environment currently active in the console and packages the required Python dependencies and external binaries with the application.

#### Build Instructions

**1. Traverse to desktop scripts directory**
From the project root:
```
cd scripts_desktop
```

**2. Run the desktop build script**
```
python build_desktop.py
```

The script will use PyInstaller to build the application and package the required dependencies and external binaries.

After a successful build, the packaged application will be available in:
```
YtDownload/
└── dist/
```

> Note: Python does not need to be installed on a computer that only runs the packaged application. The Python runtime and required Python dependencies are bundled into the packaged application by PyInstaller.

### Android

Android builds are created using `Buildozer` and `python-for-android`.

Android builds must be performed from a Linux environment. On Windows, this project uses [WSL](https://learn.microsoft.com/en-us/windows/wsl/) (Windows Subsystem for Linux).

> Note: WSL is only required for building the Android application. It is not required to run the application on Windows.

#### Windows

If you are building the Android application on Windows, WSL must first be installed and activated.

**1. Traverse to the Android build scripts**

From the project root:
```
cd scripts_android
```

**2. Install WSL**

Run:
```
install_wsl.bat
```
This script installs the required WSL environment if it is not already installed.

Follow the on-screen instructions to create a Linux user for WSL.

**3. Activate wsl**

Run:
```
activate_wsl.bat
```

A WSL terminal should open. You should now be working inside a Linux environment.

Your terminal should look similar to:
```
WSL-username@computer-name:/mnt/DriveLetter/path/to/YtDownload/scripts_android$
```

> The exact username, computer name, drive letter and path will depend on your system.

**4. Move to the home directory**

Run:
```
cd ~
```

This moves to the WSL user's home directory so that the repository can be cloned and built within the WSL Linux filesystem rather than from the Windows-mounted /mnt/... filesystem.

Building from the Linux filesystem can provide better performance and compatibility with Linux-based Android build tools.

You can now continue with the Linux instructions below.

### Linux

**1. Clone the repository**
```
git clone https://github.com/PastorRowan/YtDownload.git
```

**2. Traverse to the project root directory**
```
cd YtDownload
```

**3. Traverse to the Android build scripts directory**
```
cd scripts_android
```

**4. Give the setup scripts execute permissions**
```
chmod +x activate_venv.sh setup_wsl_environment.sh
```

**5. Setup wsl environment**
```
source setup_wsl_environment.sh
```

**6. Activate venv**
```
source activate_venv.sh
```

**7. Run the build tool**
```
python3.11 build_wsl_android_package.py
```

> Note: Android builds are performed using Buildozer and depend on a number of external tools, repositories, and Python-for-Android recipes. As a result, builds may occasionally fail due to problems outside of this project, such as temporary unavailability of an upstream repository or a dependency failing to compile.<br><br> For example, during development, an Android build failed because the [freetype recipe](https://github.com/kivy/python-for-android/tree/develop/pythonforandroid/recipes/freetype) could not download its source from [savannah.org](https://download.savannah.gnu.org/releases/freetype/). These failures may be temporary and can sometimes be resolved by retrying the build later.<br><br>If a Buildozer build fails, check the error message and the relevant upstream dependency before assuming that the problem is caused by YtDownload.

# License

This project is currently unlicensed.

All rights reserved unless otherwise stated.

# Author

Rowan Van Zyl
- GitHub: https://github.com/PastorRowan
