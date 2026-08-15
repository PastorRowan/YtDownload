
import config

from typing import (
    Literal
)

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
    ObjectProperty
)
from kivy.clock import Clock

import yt_dlp
import time
from . import (
    helpers,
    Types
)
import os

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

    DEFAULT_DOWNLOAD_TYPE_INDEX: int = 0

    DEFAULT_DOWNLOAD_TYPE: DownloadType = ALLOWED_DOWNLOAD_TYPES[DEFAULT_DOWNLOAD_TYPE_INDEX]

    downloadType: DownloadType = StringProperty(DEFAULT_DOWNLOAD_TYPE, options=ALLOWED_DOWNLOAD_TYPES)

    VideoExt = Literal[
        "webm",
        "mp4"
    ]

    VideoExts = tuple[VideoExt, ...]

    ALLOWED_VIDEO_EXTS: VideoExts = (
        "webm",
        "mp4"
    )

    DEFAULT_VIDEO_EXT_INDEX = 0

    DEFAULT_VIDEO_EXT: VideoExt = ALLOWED_VIDEO_EXTS[DEFAULT_VIDEO_EXT_INDEX]

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

    DEFAULT_VIDEO_HEIGHT_INDEX: int = 3

    DEFAULT_VIDEO_HEIGHT: VideoHeight = ALLOWED_VIDEO_HEIGHTS[DEFAULT_VIDEO_HEIGHT_INDEX]

    videoHeights: VideoHeights = ListProperty(ALLOWED_VIDEO_HEIGHTS)
    videoHeight: VideoHeight = StringProperty(DEFAULT_VIDEO_HEIGHT, options=ALLOWED_VIDEO_HEIGHTS)

    AudioExt = Literal[
        "opus",
        "m4a"
    ]

    AudioExts = tuple[AudioExt, ...]

    ALLOWED_AUDIO_EXTS: AudioExts = (
        "opus",
        "m4a"
    )

    DEFAULT_AUDIO_EXT_INDEX: int = 0

    DEFAULT_AUDIO_EXT: AudioExt = ALLOWED_AUDIO_EXTS[DEFAULT_AUDIO_EXT_INDEX]

    audioExts: AudioExts = ListProperty(ALLOWED_AUDIO_EXTS)
    audioExt: AudioExt = StringProperty(DEFAULT_AUDIO_EXT, options=ALLOWED_AUDIO_EXTS)

    Abr = Literal[
        "192",
        "160",
        "128",
        "86"
    ]

    Abrs = tuple[Abr, ...]

    ALLOWED_ABRS: Abrs = (
        "192",
        "160",
        "128",
        "86"
    )

    DEFAULT_ABR_INDEX = 0

    DEFAULT_ABR: Abr = ALLOWED_ABRS[DEFAULT_ABR_INDEX]

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

    DEFAULT_STATUS_INDEX: int = 0

    DEFAULT_STATUS: Status = STATUS_TYPES[DEFAULT_STATUS_INDEX]

    status: Status = StringProperty("queued", options=STATUS_TYPES)

    DEFAULT_ERROR: Exception | None = None

    error: Exception | None = ObjectProperty(DEFAULT_ERROR, allownone=True)

    DEFAULT_PROGRESS: float = 0

    progress: float = NumericProperty(DEFAULT_PROGRESS)

    DEFAULT_SPEED: float = 0

    speed: float = NumericProperty(DEFAULT_SPEED)

    DEFAULT_ETA: float = 0

    eta: float = NumericProperty(DEFAULT_ETA)

    DEFAULT_TOTAL_BYTES: float = 0

    totalBytes: int = NumericProperty(DEFAULT_TOTAL_BYTES)

    DEFAULT_DOWNLOADED_BYTES: float = 0

    downloadedBytes: int = NumericProperty(DEFAULT_DOWNLOADED_BYTES)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> None:

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
                    self.channel == self.DEFAULT_CHANNEL or
                    self.totalBytes == self.DEFAULT_TOTAL_BYTES) and
                    infoDict is not None
                ):

                    thumbnail = infoDict.get("thumbnail", self.DEFAULT_THUMBNAIL)
                    title = infoDict.get("title", self.DEFAULT_TITLE)
                    channel = infoDict.get("channel", self.DEFAULT_CHANNEL)
                    def updateMetaData(dt):
                        self.thumbnail = thumbnail
                        self.title = title
                        self.channel = channel
                        self.totalBytes = total
                    Clock.schedule_once(updateMetaData)

                if downloaded and total:
                    progress = downloaded / total
                    def updateJobProgressAndDownloadedBytes(dt):
                        self.downloadedBytes = downloaded
                        self.progress = progress
                    Clock.schedule_once(updateJobProgressAndDownloadedBytes)

                def updateJobSpeedAndEta(dt):
                    self.speed = speed
                    self.eta = eta
                Clock.schedule_once(updateJobSpeedAndEta)

            elif d.get("status") == "finished":
                def updateJobProgressToFinished(dt):
                    self.progress = 1.0
                Clock.schedule_once(updateJobProgressToFinished)

        try:

            print("str(config.paths.bin_platform()): ", str(config.paths.bin_platform()))

            print("str(config.paths.executable(ffmpeg)): ", str(config.paths.executable("ffmpeg")))

            base_options = {
                "logger": helpers.YTDLPLogger(),
                "outtmpl": os.path.join(
                    str(config.paths.downloads_dir),
                    "%(title)s [%(id)s].%(ext)s"
                ),
                "cachedir": str(config.paths.ytdlp_cache_dir()),
                "no_color": True,
                "progress_hooks": [progressHook],
                "retries": 10,
                "fragment_retries": 10,
            }

            ydl_download_options = {
                **base_options,
                # Prevents yt-dlp from using overwritten kivy sys.error object
                "ffmpeg_location": str(config.paths.executable("ffmpeg")),
                "js_runtimes": {
                    "quickjs": {
                        "path": str(config.paths.executable("qjs"))
                    }
                },
                "remote_components": [
                    "ejs:github"
                ],
                "concurrent_fragments": 16,
                "downloader": "aria2c",
                "downloader_args": {
                    "aria2c": "-x 16 -s 16 -k 1M"
                },
                # leave default for ffmpeg merge for video and audio format
                # "postprocessors": [],
                "postprocessor_args": {
                    "ffmpeg": [
                        "-threads",
                        str(os.cpu_count() or 1)
                    ]
                }
            }

            if self.downloadType == "video":
                ydl_download_options["format"] = (
                    f"bv*[height<={self.videoHeight}]+"
                    f"ba*[abr<={self.abr}]"
                    f"/b[height<={self.videoHeight}]"
                )
                ydl_download_options["merge_output_format"] = self.videoExt
            elif self.downloadType == "audio":
                print("Audio file chosen")
                print("self.audioExt: ", self.audioExt)
                ydl_download_options["format"] = f"ba*[abr<={self.abr}]/ba"
                ydl_download_options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.audioExt
                }]

            with yt_dlp.YoutubeDL(ydl_download_options) as ydl_download: 

                infoDict: Types.InfoDict = ydl_download.extract_info(
                    url=self.url,
                    download=True
                )

                def updateStatusToFinished(dt: int) -> None:
                    self.status = "finished"
                Clock.schedule_once(updateStatusToFinished)
            
        except Paused:
            pass
        except Cancelled:
            pass

        except Exception as e:

            error = e

            print(str(error))

            def updateStatusAndError(dt):
                self.status = "error"
                self.error = error
            Clock.schedule_once(updateStatusAndError)
