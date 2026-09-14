
# YtDownload

A cross platform **KivyMD application for downloading YouTube videos or audio** using <u>yt-dlp</u>.

> **Note:** YtDownload has currently been tested on only **Windows** and **Android**.

## Features
- 📥 Download YouTube videos (video and audio)
- 🎵 Download audio only
- 🖥️ Cross-platform application
- 📱 Android support
- 💻 Windows support
- ⚙️ Uses `yt-dlp` for media downloading
- 🚀 Concurrent downloading support
- 📁 Configurable download directories (Only works for Windows, Linux and MacOS at the moment)

## Demo

*Add a demonstration video or GIF here.*

## Dependencies

YtDownload is built using the following Python packages:

- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Plyer](https://github.com/kivy/plyer)
- [buildozer]()
- [pyinstaller]()

The project also requires the dependencies of the packages listed above.

Some features may additionally require external binaries, depending on the target platform and media format.

## External binaries

YtDownload requires the following external binaries for media processing and downloading:

- [FFmpeg](https://ffmpeg.org/download.html) — Media processing and audio/video conversion
- [FFprobe](https://ffmpeg.org/ffprobe.html) — Media file analysis
- [QuickJS (qjs)](https://bellard.org/quickjs/) — JavaScript runtime used by `yt-dlp`

## Getting Started

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
pip --version
```

Git:
```
git --version
```

#### Install external binaries

Install the required external binaries for your target development or production platform by following the instructions in the corresponding `README.md`:

- [Windows](libs/windows/README.md)
- [Linux](libs/linux/README.md)
- [macOS](libs/macos/README.md)
- [Android arm64-v8a](libs/arm64-v8a/README.md)

### Installation 

Open a console enviroment with python, venv and pip installed.

**1. Clone the repository**
```
git clone https://github.com/PastorRowan/YtDownload.git
```

**2. Traverse to the project directory**
```
cd YtDownload
```

**3. Create a virtual enviroment**
```
python -m venv venv
```

**4. Activate the virtual enviroment**

- Windows:
```
.\venv\Scripts\activate.bat
```
After activation, your terminal should look similar to:
```
(venv) C:\path\to\YtDownload>
```

- Linux/macOS:
```
source venv/bin/activate
```
After activation, your terminal should look similar to:
```
(venv) /path/to/YtDownload$
```

**5. Install Python dependencies to virtual enviroment**
```
pip install -r requirements.txt
```

**6. Install required binaries**

See

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
4. Make sure the application can run successfully (if using a console based virtual enviroment, like wsl, then this step cannot be done).

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
python3 build_desktop.py
```

The script will use PyInstaller to build the application and package the required dependencies and external binaries.

After a successful build, the packaged application will be available in:
```
YtDownload/
└── dist/
```

> Note: Python does not need to be installed on a computer that only runs the packaged application. The Python runtime and required Python dependencies are bundled into the packaged application by PyInstaller.

### Android

...

# License

This project is currently unlicensed.

All rights reserved unless otherwise stated.

# Author

Rowan Van Zyl
- GitHub: https://github.com/PastorRowan
