
from typing import TypedDict, NotRequired

import yt_dlp
import config

class YTDLPLogger:

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

ydl_opts = {
    "logger": YTDLPLogger(),
    "ffmpeg_location": config.FFMPEG_PATH,
    "js_runtimes": {
        "deno": {
            "path": config.DENO_PATH
        }
    },
    "remote_components": [
        "ejs:github"
    ],
    "outtmpl": r"downloads\%(title)s [%(id)s].%(ext)s",
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "no_color": True
}

class VideoInfo(TypedDict):
    id: str
    title: str
    webpage_url: str
    thumbnail: NotRequired[str | None]
    duration: NotRequired[int | None]

class ExtractInfoResult(TypedDict):
    ok: bool
    error_msg: str | None
    video_info: VideoInfo | None

def get_video_info(
    url: str,
    download: bool = False
) -> ExtractInfoResult:

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:

            info = ydl.extract_info(
                url,
                download
            )

            return {
                "ok": True,
                "error_msg": None,
                "video_info": info
            }

        except Exception as e:

            return {
                "ok": False,
                "error_msg": str(e),
                "video_info": None
            }
