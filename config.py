
import platform
from pathlib import Path, PureWindowsPath, PurePosixPath

class PROJECT:

    DIR = Path(__file__).resolve().parent

    PYINSTALLER_SPEC = DIR / "main.spec"
    DOWNLOADS_DIR = DIR / "downloads"

    BUILD_DIR = DIR / "build"
    DIST_DIR = DIR / "dist"
    BIN_DIR = DIR / "bin"

class WINDOWS:

    DIR = PureWindowsPath(PROJECT.DIR)

    BUILD_DIR = DIR / "windows"
    DIST_DIR = DIR / "windows"
    BIN_DIR = DIR / "windows"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg.exe"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe.exe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs.exe"

    DEST_BIN = "bin/windows"
    
class LINUX:

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "linux"
    DIST_DIR = DIR / "linux"
    BIN_DIR = DIR / "linux"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs"

    DEST_BIN = "bin/linux"
    
class MACOS:

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "macos"
    DIST_DIR = DIR / "macos"
    BIN_DIR = DIR / "macos"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs"

    DEST_BIN = "bin/macos"
    
class ANDROID:

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "android"
    DIST_DIR = DIR / "android"
    BIN_DIR = DIR / "android"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs"

    DEST_BIN = "bin/android"
    
PATHS: WINDOWS | LINUX | MACOS = None

system = platform.system().lower()

if system == "windows":
    PATHS = WINDOWS
elif system == "darwin":
    PATHS = MACOS
elif system == "linux":
    PATHS = LINUX
elif system == "android":
    PATHS = ANDROID
else:
    raise RuntimeError(f"Unsupported operating system: {system}, failed to initialise PATHS")
