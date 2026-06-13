
from typing import TypedDict, NotRequired

import yt_dlp
import config

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty
)
from kivy.clock import Clock

from queue import Queue
from threading import Thread

from pprint import pprint

import config

import InfoDict

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
    "no_color": True,
    "progress_hooks": [],
}

class ExtractInfoResult(TypedDict):
    ok: bool
    error_msg: str | None
    video_info: InfoDict.InfoDict | None

class DownloadJob(EventDispatcher):

    url = ""
    status = StringProperty("queued")
    error = StringProperty("")
    progress = NumericProperty(0)
    speed = NumericProperty(0)
    eta = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class _DownloadQueue():

    _queue = Queue()

    def __init__(self):
        pass

    @staticmethod
    def _getVideoInfo(
        url: str,
        download: bool = False,
        job: None | DownloadJob = None
    ) -> ExtractInfoResult:

        def progressHook(d):

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

        ydl_opts_local = dict(ydl_opts)
        ydl_opts_local["progress_hooks"] = [progressHook]

        with yt_dlp.YoutubeDL(ydl_opts_local) as ydl:

            try:

                info = ydl.extract_info(
                    url=url,
                    download=download
                )

                return {
                    "ok": True,
                    "error_msg": None,
                    "video_info": info
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

    def _processDownloads(self):

        while True:

            job = self._queue.get()

            try:

                extractedInfoResult = _DownloadQueue._getVideoInfo(
                    url=job.url,
                    download=True,
                    job=job
                )

                if not extractedInfoResult["ok"]:
                    errorMsg = extractedInfoResult["error_msg"]

            except Exception as e:
                print(e)
            finally:
                self._queue.task_done()

    def addDownloadJob(self, job: DownloadJob):
        self._queue.put(job)

DownloadQueue = _DownloadQueue()

Thread(
    target=DownloadQueue._processDownloads,
    daemon=True
).start()
