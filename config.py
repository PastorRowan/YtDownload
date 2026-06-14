
import pathlib

PROJECT_DIR = pathlib.Path(__file__).resolve().parent

FFMPEG_PATH = str(PROJECT_DIR / "bin" / "windows" / "ffmpeg.exe")
DENO_PATH = str(PROJECT_DIR / "bin" / "windows" / "deno.exe")

ALLOWED_DOWNLOAD_TYPES = (
    "video",
    "audio"
)

DEFAULT_DOWNLOAD_TYPE = "video"

ALLOWED_VIDEO_EXTS: tuple[str] = (
    "mp4",
    "webm"
)

DEFAULT_VIDEO_EXT: str = "mp4"

ALLOWED_VIDEO_HEIGHTS: tuple[str] = [
    "3840",
    "1440",
    "1080",
    "720",
    "480",
    "360"
]

DEFAULT_VIDEO_HEIGHT: str = "720"

ALLOWED_AUDIO_EXTS: tuple[str] = [
    "m4a",
    "webm",
    "opus"
]

DEFAULT_AUDIO_EXT: str = "opus"

ALLOWED_ABRS: tuple[str] = [
    "150",
    "120",
    "50",
    "40"
]

DEFAULT_ABR: str = "150"
