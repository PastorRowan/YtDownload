
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

from threading import Thread

import config

from urllib.parse import urlparse

from . import Types
from .Job import Job

class _Queue(EventDispatcher):

    jobs: list[Job] = ListProperty([])

    _currentJob: Job = ObjectProperty(None, allownone=True)
    _currentThread: Thread | None = ObjectProperty(None, allownone=True)

    def __init__(self):
        pass

    def _onDownloadFinished(
        self,
        job: Job,
        result: Types.ExtractInfoResult
    ) -> None:

        if job not in self.jobs:
            return

        if not result["ok"]:
            job.status = "error"
            job.error = result["error_msg"] or ""

        is_current = (self._currentJob is job)

        if job.status in ("cancelled", "finished") and is_current:
            self.jobs = [j for j in self.jobs if j is not job]

        # wrong we will add paused queue later
        elif job.status == "paused" and is_current:
            self.jobs = [j for j in self.jobs if j is not job] + [job]

        self._currentJob = None
        self._currentThread = None
        self._startNextDownload()
    
    def _downloadWorker(
        self,
        job: Job
    ) -> None:

        result = job.run()

        Clock.schedule_once(
            lambda dt: self._onDownloadFinished(
                job,
                result
            )
        )

    def _startNextDownload(self) -> None:

        if self._currentThread is not None or not self.jobs:
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

    def addJob(
        self,
        job: Job
    ) -> None:

        if job in self.jobs:
            return

        self.jobs = self.jobs + [job]

        if self._currentThread is None:
            self._startNextDownload()

    def cancelJob(self, job: Job):

        if job not in self.jobs:
            return

        was_current = (self._currentJob is job)

        self.jobs = [j for j in self.jobs if j is not job]
        job.status = "cancelled"

        if was_current:
            self._currentJob = None
            self._currentThread = None
            self._startNextDownload()
   
    def pauseJob(self, job: Job):

        if job not in self.jobs:
            return

        job.status = "paused"

        was_current = (self._currentJob is job)

        # remove from active queue
        self.jobs = [j for j in self.jobs if j is not job]

        # push to back of queue
        self.jobs = self.jobs + [job]

        if was_current:
            self._currentJob = None
            self._currentThread = None
            self._startNextDownload()

    def resumeJob(self, job: Job):
        if job not in self.jobs:
            return

        if job.status != "paused":
            return

        job.status = "queued"

        # already in queue; move it to back
        self.jobs = [j for j in self.jobs if j is not job] + [job]

        # if nothing is running, start immediately
        if self._currentJob is None:
            self._startNextDownload()

Queue = _Queue()
