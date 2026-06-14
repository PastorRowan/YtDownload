
from typing import TypedDict, NotRequired

import yt_dlp
import config

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
    BooleanProperty,
    ListProperty
)
from kivy.clock import Clock

from threading import Thread, Event

from pprint import pprint

import config

import InfoDict

from urllib.parse import urlparse

class YTDLPLogger:

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

class ExtractInfoResult(TypedDict):
    ok: bool
    error_msg: str | None
    video_info: InfoDict.InfoDict | None

class DownloadJob(EventDispatcher):

    STATUS_TYPES = (
        "queued",
        "downloading",
        "error",
        "paused"
    )

    cancel_event = None

    url = StringProperty("")

    fileName = StringProperty(None)
    downloadType = StringProperty(config.DEFAULT_DOWNLOAD_TYPE, options=config.ALLOWED_DOWNLOAD_TYPES)

    videoExt = StringProperty(None, options=config.ALLOWED_VIDEO_EXTS)
    videoHeight = StringProperty(None, options=config.ALLOWED_VIDEO_HEIGHTS)

    audioExt = StringProperty(None, options=config.ALLOWED_AUDIO_EXTS)
    abr = StringProperty(None, options=config.ALLOWED_ABRS)

    title = StringProperty("")
    channel = StringProperty("")
    thumbnail = StringProperty("")

    status = StringProperty("queued", options=STATUS_TYPES)
    error = StringProperty("")
    progress = NumericProperty(0)
    speed = NumericProperty(0)
    eta = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cancel_event = Event()

class DownloadCancelled(Exception):
    pass

class _DownloadQueue(EventDispatcher):

    jobs = ListProperty([])

    _currentJob = ObjectProperty(None, allownone=True)
    _currentThread = ObjectProperty(None, allownone=True)

    def __init__(self):
        pass

    @staticmethod
    def _getVideoInfo(
        url: str,
        job: None | DownloadJob = None
    ) -> ExtractInfoResult:

        def progressHook(d):

            if job.cancel_event.is_set():
                raise DownloadCancelled()

            if job is None:
                return

            if d.get("status") == "downloading":

                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate")

                if total:
                    progress = downloaded / total
                    def updateJobProgress(dt):
                        job.progress = progress
                    Clock.schedule_once(updateJobProgress)

                speed = d.get("speed") or 0
                eta = d.get("eta") or 0

                def updateJobSpeedAndEta(dt):
                    job.speed = speed
                    job.eta = eta
                Clock.schedule_once(updateJobSpeedAndEta)

            elif d.get("status") == "finished":
                def updateJobProgressToFinished(dt):
                    job.progress = 1.0
                Clock.schedule_once(updateJobProgressToFinished)

        ydl_opts = {
            # Prevents yt-dlp from using overwritten kivy sys.error object
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
            # leave default for ffmpeg merge for video and audio format
            # "postprocessors": [],
            "no_color": True,
            "progress_hooks": [progressHook],
        }

        if job.downloadType == "video":
            ydl_opts["format"] = f"bestvideo[height={job.videoHeight}]+bestaudio[acodec={job.audioExt}][abr>={job.abr}]"
            ydl_opts["merge_output_format"] = job.videoExt
        elif job.downloadType == "audio":
            ydl_opts["format"] = f"bestaudio[acodec={job.audioExt}][abr>={job.abr}]"
            ydl_opts["postprocessors"] = []
        else:
            raise ValueError(f"job.downloadType '{job.downloadType}' is invalid")
        
        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                metaData: InfoDict.InfoDict = ydl.extract_info(
                    url=url,
                    download=False
                )

                def updateMetaData(dt):
                    job.title = metaData["title"]
                    job.channel = metaData["channel"]
                    job.thumbnail = metaData["thumbnail"]

                Clock.schedule_once(updateMetaData)

                videoInfo: InfoDict.InfoDict = ydl.extract_info(
                    url=url,
                    download=True
                )

                return {
                    "ok": True,
                    "error_msg": None,
                    "video_info": videoInfo
                }

        except Exception as e:

            errorMsg = str(e)

            print(errorMsg)

            def updateStatusAndError(dt):
                job.status = "error"
                job.error = errorMsg

            Clock.schedule_once(updateStatusAndError)

            return {
                "ok": False,
                "error_msg": errorMsg,
                "video_info": None
            }

    @staticmethod
    def getVideoInfo(
        url: str
    ) -> ExtractInfoResult:
        return _DownloadQueue._getVideoInfo(
            url=url,
            download=False
        )
    
    def _onDownloadFinished(
        self,
        job: DownloadJob,
        result: ExtractInfoResult
    ) -> None:

        if not result["ok"]:
            job.status = "error"
            job.error = result["error_msg"] or ""

        if self.jobs and self.jobs[0] is job:
            self.jobs = self.jobs[1:]

        self._currentJob = None
        self._currentThread = None

        self._startNextDownload()
    
    def _downloadWorker(
        self,
        job: DownloadJob
    ) -> None:

        result = self._getVideoInfo(
            url=job.url,
            job=job
        )

        Clock.schedule_once(
            lambda dt: self._onDownloadFinished(
                job,
                result
            )
        )

    def _startNextDownload(self) -> None:

        if self._currentThread is not None:
            return

        if not self.jobs:
            return

        job = self.jobs[0]

        self._currentJob = job

        job.status = "downloading"

        self._currentThread = Thread(
            target=self._downloadWorker,
            args=(job,),
            daemon=True
        )

        self._currentThread.start()

    def addDownloadJob(
        self,
        job: DownloadJob
    ) -> None:

        self.jobs = self.jobs + [job]

        if self._currentThread is None:
            self._startNextDownload()

DownloadQueue = _DownloadQueue()

def isUrlValid(url: str) -> bool:

    try:

        parsed = urlparse(url.strip())

        return (
            parsed.scheme in ("http", "https")
            and parsed.netloc != ""
        )

    except Exception:
        return False    
