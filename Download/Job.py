
from typing import (
    Literal
)

import config

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty
)
from kivy.clock import Clock

import yt_dlp

import time

from . import (
    helpers,
    Types
)

class Paused(Exception):
    pass

class Cancelled(Exception):
    pass

class Job(EventDispatcher):

    DEFAULT_URL: str = ""

    url: str = StringProperty(DEFAULT_URL)

    DEFAULT_FILENAME: str = ""

    fileName: str = StringProperty(DEFAULT_FILENAME)

    DownloadType = Literal[
        "video",
        "audio"
    ]

    ALLOWED_DOWNLOAD_TYPES: tuple[DownloadType, ...] = (
        "video",
        "audio"
    )

    DEFAULT_DOWNLOAD_TYPE: DownloadType = ALLOWED_DOWNLOAD_TYPES[0]

    downloadType: DownloadType = StringProperty(DEFAULT_DOWNLOAD_TYPE, options=ALLOWED_DOWNLOAD_TYPES)

    VideoExt = Literal[
        "mp4",
        "webm"
    ]

    VideoExts = tuple[VideoExt, ...]

    ALLOWED_VIDEO_EXTS: VideoExts = (
        "mp4",
        "webm"
    )

    DEFAULT_VIDEO_EXT: VideoExt = ALLOWED_VIDEO_EXTS[0]

    videoExts: VideoExts = ListProperty(ALLOWED_VIDEO_EXTS)
    videoExt: VideoExt = StringProperty(DEFAULT_VIDEO_EXT, options=ALLOWED_VIDEO_EXTS)

    VideoHeight = Literal[
        "3840",
        "1440",
        "1080",
        "720",
        "480",
        "360"
    ]

    VideoHeights = tuple[VideoHeight, ...]

    ALLOWED_VIDEO_HEIGHTS: VideoHeights = (
        "3840",
        "1440",
        "1080",
        "720",
        "480",
        "360"
    )

    DEFAULT_VIDEO_HEIGHT: VideoHeight = ALLOWED_VIDEO_HEIGHTS[3]

    videoHeights: VideoHeights = ListProperty(ALLOWED_VIDEO_HEIGHTS)
    videoHeight: VideoHeight = StringProperty(DEFAULT_VIDEO_HEIGHT, options=ALLOWED_VIDEO_HEIGHTS)

    AudioExt = Literal[
        "m4a",
        "webm",
        "opus"
    ]

    AudioExts = tuple[AudioExt, ...]

    ALLOWED_AUDIO_EXTS: AudioExts = (
        "m4a",
        "webm",
        "opus"
    )

    DEFAULT_AUDIO_EXT: AudioExt = ALLOWED_AUDIO_EXTS[2]

    audioExts: AudioExts = ListProperty(ALLOWED_AUDIO_EXTS)
    audioExt: AudioExt = StringProperty(DEFAULT_AUDIO_EXT, options=ALLOWED_AUDIO_EXTS)

    Abr = Literal[
        "150",
        "120",
        "50",
        "40"
    ]

    Abrs = tuple[Abr, ...]

    ALLOWED_ABRS: Abrs = (
        "150",
        "120",
        "50",
        "40"
    )

    DEFAULT_ABR: Abr = ALLOWED_ABRS[0]

    abrs: Abrs = ListProperty(ALLOWED_ABRS)
    abr: Abr = StringProperty(DEFAULT_ABR, options=ALLOWED_ABRS)

    DEFAULT_TITLE: str = ""

    title: str = StringProperty(DEFAULT_TITLE)

    DEFAULT_CHANNEL: str = ""

    channel: str = StringProperty(DEFAULT_CHANNEL)

    DEFAULT_THUMBNAIL: str = ""

    thumbnail: str = StringProperty(DEFAULT_THUMBNAIL)

    Status = Literal[
        "queued",
        "downloading",
        "error",
        "paused",
        "cancelled",
        "finished"
    ]

    STATUS_TYPES: tuple[Status, ...] = (
        "queued",
        "downloading",
        "error",
        "paused",
        "cancelled",
        "finished"
    )

    DEFAULT_STATUS: Status = STATUS_TYPES[0]

    status: Status = StringProperty("queued", options=STATUS_TYPES)

    DEFAULT_ERROR: str = ""

    error: str = StringProperty(DEFAULT_ERROR)

    DEFAULT_PROGRESS: float = 0

    progress: float = NumericProperty(DEFAULT_PROGRESS)

    DEFAULT_SPEED: float = 0

    speed: float = NumericProperty(DEFAULT_SPEED)

    DEFAULT_ETA: float = 0

    eta: float = NumericProperty(DEFAULT_ETA)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> Types.ExtractInfoDictResult:

        if self.url == self.DEFAULT_URL:
            raise Exception(f"Failed to run job: url is not assigned-'{self.url}'")

        last_update_time = 0.0
        UPDATE_INTERVAL = 1.5

        def progressHook(d):
            nonlocal last_update_time

            if self.status == "paused":
                raise Paused()

            if self.status == "cancelled":
                raise Cancelled()
            
            now = time.time()

            if d.get("status") == "downloading":

                # throttle UI updates
                if now - last_update_time < UPDATE_INTERVAL:
                    return

                last_update_time = now

                downloaded: float = d.get("downloaded_bytes", 0)
                total: float = d.get("total_bytes") or d.get("total_bytes_estimate")
                speed: float = d.get("speed") or 0
                eta: float = d.get("eta") or 0
                infoDict: Types.InfoDict = d.get("info_dict")

                if (
                    (self.thumbnail == self.DEFAULT_THUMBNAIL or
                    self.title == self.DEFAULT_TITLE or
                    self.channel == self.DEFAULT_CHANNEL) and
                    infoDict is not None
                ):

                    thumbnail = infoDict.get("thumbnail", self.DEFAULT_THUMBNAIL)
                    title = infoDict.get("title", self.DEFAULT_TITLE)
                    channel = infoDict.get("channel", self.DEFAULT_CHANNEL)
                    def updateMetaData(dt):
                        self.thumbnail = thumbnail
                        self.title = title
                        self.channel = channel
                    Clock.schedule_once(updateMetaData)

                if total:
                    progress = downloaded / total
                    def updateJobProgress(dt):
                        self.progress = progress
                    Clock.schedule_once(updateJobProgress)

                def updateJobSpeedAndEta(dt):
                    self.speed = speed
                    self.eta = eta
                Clock.schedule_once(updateJobSpeedAndEta)

            elif d.get("status") == "finished":
                def updateJobProgressToFinished(dt):
                    self.progress = 1.0
                Clock.schedule_once(updateJobProgressToFinished)

        try:

            ydl_download_options = {
                # Prevents yt-dlp from using overwritten kivy sys.error object
                "logger": helpers.YTDLPLogger(),
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
                # leave default for ffmpeg merge for video and audio format
                # "postprocessors": [],
                "no_color": True,
                "progress_hooks": [progressHook],
            }

            if self.downloadType == "video":
                videoFormat = f"bestvideo[height>={self.videoHeight}]"
                audioFormat = f"bestaudio[acodec={self.audioExt}][abr>={self.abr}]/best"
                ydl_download_options["format"] = f"{videoFormat}+{audioFormat}"
                ydl_download_options["format_sort"] = ["+height", "+abr"]
                ydl_download_options["merge_output_format"] = self.videoExt
            elif self.downloadType == "audio":
                ydl_download_options["format"] = f"bestaudio[acodec={self.audioExt}][abr>={self.abr}] -S +abr"
                ydl_download_options["format_sort"] = ["+abr"]
                ydl_download_options["merge_output_format"] = self.audioExt
                ydl_download_options["postprocessors"] = []

            with yt_dlp.YoutubeDL(ydl_download_options) as ydl_download: 

                infoDict: Types.InfoDict = ydl_download.extract_info(
                    url=self.url,
                    download=True
                )

                def updateStatusToFinished(dt: int) -> None:
                    self.status = "finished"
                Clock.schedule_once(updateStatusToFinished)

                return {
                    "ok": True,
                    "error_msg": None,
                    "info_dict": infoDict
                }

        except Exception as e:

            errorMsg = str(e)

            print(errorMsg)

            def updateStatusAndError(dt):
                self.status = "error"
                self.error = errorMsg
            Clock.schedule_once(updateStatusAndError)

            return {
                "ok": False,
                "error_msg": errorMsg,
                "info_dict": None
            }
