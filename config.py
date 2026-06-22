
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

    BUILD_DIR = DIR / "build" / "windows"
    DIST_DIR = DIR / "dist" / "windows"
    BIN_DIR = DIR / "bin" / "windows"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg.exe"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe.exe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs.exe"

    DEST_BIN = "bin/windows"

class LINUX:

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "build" / "linux"
    DIST_DIR = DIR / "dist" / "linux"
    BIN_DIR = DIR / "bin" / "linux"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs"

    DEST_BIN = "bin/linux"
    
class MACOS:

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "build" / "macos"
    DIST_DIR = DIR / "dist" / "macos"
    BIN_DIR = DIR / "bin" / "macos"

    FFMPEG_BIN_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_BIN_PATH = BIN_DIR / "ffprobe"
    QUICK_JS_BIN_PATH = BIN_DIR / "qjs"

    DEST_BIN = "bin/macos"

class ANDROID:
    from kivy.resources import resource_find

    DIR = PurePosixPath(PROJECT.DIR)

    BUILD_DIR = DIR / "build" / "android"
    DIST_DIR = DIR / "dist" / "android"
    BIN_DIR = DIR / "bin" / "android"

    FFMPEG_APK_BIN_PATH = resource_find("bin/android/ffmpeg")
    FFPROBE_APK_BIN_PATH = resource_find("bin/android/ffprobe")
    QUICK_JS_APK_BIN_PATH = resource_find("bin/android/qjs-linux-aarch64")
    
    FFMPEG_BIN_PATH = None
    FFPROBE_BIN_PATH = None
    QUICK_JS_BIN_PATH = None

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
