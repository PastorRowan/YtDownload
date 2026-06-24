
from typing import Literal

from pathlib import Path

import os

def platform():

    try:

        from kivy.utils import platform as kivy_platform

        mapping = {
            "win": "windows",
            "macosx": "macos",
            "linux": "linux",
            "android": "android",
        }

        return mapping.get(kivy_platform, "unknown")

    except Exception:
        import sys
        if sys.platform.startswith("win"):
            return "windows"
        elif sys.platform.startswith("darwin"):
            return "macos"
        elif sys.platform.startswith("linux"):
            return "linux"
        return "unknown"

class _paths:

    EXECUTABLES = ("ffmpeg", "ffprobe", "qjs")

    SUPPORTED_PLATFORMS = ("windows", "macos", "linux", "android")
    PLATFORM: Literal["windows", "macos", "linux", "android"] = None

    downloads_dir: Path | None = None

    def __init__(self, platformP: str):

        if platformP in self.SUPPORTED_PLATFORMS:
            self.PLATFORM = platformP
        else:
            raise RuntimeError(f"platform {platformP} unsupported. Supported platforms = {self.SUPPORTED_PLATFORMS}")

        self.downloads_dir = self._default_downloads_dir()

    def _ensure_dir(self, path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _default_downloads_dir(self) -> Path:
        match self.PLATFORM:
            case "android":
                try:
                    from jnius import autoclass
                    Environment = autoclass("android.os.Environment")

                    downloads_dir = Environment.getExternalStoragePublicDirectory(
                        Environment.DIRECTORY_DOWNLOADS
                    ).getAbsolutePath()

                    return self._ensure_dir(Path(downloads_dir) / "ytdownload")
                except Exception:
                    from android.storage import app_storage_path
                    return self._ensure_dir(Path(app_storage_path()) / "YtDownload")
            case _:
                return self._ensure_dir(self.base() / "downloads")

    def _bin_ext(self) -> str:
        match self.PLATFORM:
            case "android":
                return ".so"
            case "windows":
                return ".exe"
            case _:
                return ""

    def base(self) -> Path:
        match self.PLATFORM:
            case "android":
                try:
                    from android.storage import app_storage_path
                    return self._ensure_dir(Path(app_storage_path()) / "YtDownload")
                except Exception:
                    return self._ensure_dir(Path.home() / "YtDownload")
            case _:
                return self._ensure_dir(Path(__file__).resolve().parent)

    def build(self) -> Path:
        return self._ensure_dir(self.base() / "build")

    def dist(self) -> Path:
        return self._ensure_dir(self.base() / "dist")

    def bin(self) -> Path:
        return self._ensure_dir(self.base() / "bin")
    
    def ytdlp_cache_dir(self) -> Path:
        
        base_cache: Path | None = None
        
        match self.PLATFORM:
            case "android":
                from android.storage import app_storage_path

                base_cache = Path(app_storage_path()) / "cache" / "yt-dlp"
                base_cache.mkdir(parents=True, exist_ok=True)

            case _:
                base_cache = self.base() / "cache" / "yt-dlp"
                base_cache.mkdir(parents=True, exist_ok=True)
    
        # Force yt-dlp to use this
        os.environ["XDG_CACHE_HOME"] = str(base_cache)
        # extra safety (some builds respect this)
        os.environ["YT_DLP_CACHE_DIR"] = str(base_cache)
        
        print("base_cache: ", base_cache)
            
        return base_cache

    def pyinstaller_spec(self) -> Path:
        return self.base() / "main.spec"

    def set_downloads_dir(self, new_downloads_dir: Path) -> None:
        self.downloads_dir = new_downloads_dir

    # Executables
    def bin_platform(self) -> Path:
        match self.PLATFORM:
            case "android":
                from android import mActivity
                app_info = mActivity.getApplicationInfo()
                native_lib_dir = app_info.nativeLibraryDir
                print("native_lib_dir: ", native_lib_dir)
                return Path(native_lib_dir)
            case _:
                return self._ensure_dir(self.bin() / self.PLATFORM)

    def executable(self, executable_name) -> Path:

        if executable_name not in self.EXECUTABLES:
            raise RuntimeError(f"executable name {executable_name} invalid. Allowed executable names: {self.EXECUTABLES}")

        match self.PLATFORM:
            case "android":
                return self.bin_platform() / f"lib{executable_name}{self._bin_ext()}"
            case _:
                return self.bin_platform() / f"{executable_name}{self._bin_ext()}"

    def packaged_dest_bin(self) -> str:
        return f"bin/{self.PLATFORM}"

    def packaged_executable(self, executable_name) -> str:

        if executable_name not in self.EXECUTABLES:
            raise RuntimeError(f"executable name {executable_name} invalid. Allowed executable names: {self.EXECUTABLES}")

        match self.PLATFORM:
            case "android":
                from kivy.resources import resource_find

                resourcePath = Path(self.packaged_dest_bin()) / f"{executable_name}"
                result = resource_find(str(resourcePath))

                if not result:
                    raise FileNotFoundError(f"Packaged executable not found: {resourcePath}")

                return result

            case _:
                from kivy.resources import resource_find

                resourcePath = Path(self.packaged_dest_bin()) / f"{executable_name}{self._bin_ext()}"
                result = resource_find(str(resourcePath))

                if not result:
                    raise FileNotFoundError(f"Packaged executable not found: {resourcePath}")

                return result

PLATFORM = platform()
paths = _paths(platformP=PLATFORM)
