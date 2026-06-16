
from typing import TypedDict

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

import Download.InfoDict as InfoDict

from urllib.parse import urlparse

import time

from Download.DownloadJob import DownloadJob

from Download import Types

from Download.helpers import YTDLPLogger

class DownloadPaused(Exception):
    pass

class DownloadCancelled(Exception):
    pass

class _DownloadQueue(EventDispatcher):

    jobs: list[DownloadJob] = ListProperty([])

    _currentJob: DownloadJob = ObjectProperty(None, allownone=True)
    _currentThread: Thread | None = ObjectProperty(None, allownone=True)

    def __init__(self):
        pass

    @staticmethod
    def _runDownloadJob(
        url: str,
        job: None | DownloadJob = None
    ) -> Types.ExtractInfoResult:

        last_update_time = 0.0
        UPDATE_INTERVAL = 1.5

        def progressHook(d):
            nonlocal last_update_time

            if job.status == "paused":
                raise DownloadPaused()

            if job.status == "cancelled":
                raise DownloadCancelled()

            if job is None:
                return
            
            now = time.time()

            if d.get("status") == "downloading":

                # throttle UI updates
                if now - last_update_time < UPDATE_INTERVAL:
                    return
                
                last_update_time = now

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

        try:

            ydl_download_options = {
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
                videoFormat = f"bestvideo[height>={job.videoHeight}]"
                audioFormat = f"bestaudio[acodec={job.audioExt}][abr>={job.abr}]/best"
                ydl_download_options["format"] = f"{videoFormat}+{audioFormat}"
                ydl_download_options["format_sort"] = ["+height", "+abr"]
                ydl_download_options["merge_output_format"] = job.videoExt
            elif job.downloadType == "audio":
                ydl_download_options["format"] = f"bestaudio[acodec={job.audioExt}][abr>={job.abr}] -S +abr"
                ydl_download_options["merge_output_format"] = job.audioExt
                ydl_download_options["postprocessors"] = []

            with yt_dlp.YoutubeDL(ydl_download_options) as ydl_download: 

                videoInfo: InfoDict.InfoDict = ydl_download.extract_info(
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

    def _onDownloadFinished(
        self,
        job: DownloadJob,
        result: Types.ExtractInfoResult
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

        result = self._runDownloadJob(
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

    def cancelDownloadJob(self):

        if not self.jobs:
            return
        self.jobs[0].status = "cancelled"

    def pauseDownloadJob(self):

        if not self.jobs:
            return
        self.jobs[0].status = "paused"

DownloadQueue = _DownloadQueue()
