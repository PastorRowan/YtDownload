
from typing import Literal

from pathlib import Path

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
        return self._ensure_dir(self.base() / "downloads")

    def _bin_ext(self) -> str:
        match self.PLATFORM:
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

    def pyinstaller_spec(self) -> Path:
        return self.base() / "main.spec"

    def set_downloads_dir(self, new_downloads_dir: Path) -> None:
        self.downloads_dir = new_downloads_dir

    # Executables

    def executable(self, executable_name) -> Path:
        if executable_name not in self.EXECUTABLES:
            raise RuntimeError(f"executable name {executable_name} invalid. Allowed executable names: {self.EXECUTABLES}")
        dir = self._ensure_dir(self.bin() / self.PLATFORM)
        return dir / f"{executable_name}{self._bin_ext()}"

    def packaged_dest_bin(self) -> str:
        return f"bin/{self.PLATFORM}"

    def packaged_executable(self, executable_name) -> str:
        from kivy.resources import resource_find
        if executable_name not in self.EXECUTABLES:
            raise RuntimeError(f"executable name {executable_name} invalid. Allowed executable names: {self.EXECUTABLES}")

        dir = Path(self.packaged_dest_bin()) / f"{executable_name}{self._bin_ext()}"
        result = resource_find(str(dir))

        if not result:
            raise FileNotFoundError(f"Packaged executable not found: {dir}")

        return result

paths = _paths(platformP=platform())
