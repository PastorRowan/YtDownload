
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

## Screenshots

*Add screenshots of the application here.*

## Demo

*Add a demonstration video or GIF here.*

## Dependencies

YtDownload is built using the following Python packages:

- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Plyer](https://github.com/kivy/plyer)

The project also requires the dependencies of the packages listed above.

Some features may additionally require external binaries, depending on the target platform and media format.

## External binaries

YtDownload requires the following external binaries for media processing and downloading:

- FFmpeg — Media processing and audio/video conversion
- FFprobe — Media file analysis
- QuickJS (qjs) — JavaScript runtime used by yt-dlp

## Getting Started

### Prerequisites

Before installing YtDownload, make sure the following are installed:

- Python
- `venv`
- `pip`
- Git

You can verify prerequisites are installed via:

python:
```
python --version
```

venv:
```
python venv --version
```

pip:
```
pip --version
```

Git:
```
git --version
```

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

Windows:
```
.\venv\Scripts\activate.bat
```
After activation, your terminal should look similar to:

(venv) C:\path\to\YtDownload>

Linux/macOS:
```
source venv/bin/activate
```
After activation, your terminal should look similar to:

(venv) /path/to/YtDownload$

**5. Install Python dependencies to virtual enviroment**
```
pip install -r requirements.txt
```

**6. Install required binaries**

YtDownload requires additional binaries for some media-processing and downloading functionality.

The required binaries depend on your operating system and CPU architecture.

See the project configuration and platform-specific documentation for more information.

**7. Run the application**
```
python main.py
```

## Deployment

1st install the development enviroment

YtDownload can be packaged for supported platforms using the appropriate Kivy deployment tools.

### Desktop (Windows, Linux and MacOS)

### Android

## Build

# License

This project is currently unlicensed.

All rights reserved unless otherwise stated.

# Author

Rowan Van Zyl
- GitHub: https://github.com/PastorRowan
