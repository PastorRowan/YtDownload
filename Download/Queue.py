
import yt_dlp

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

from urllib.parse import urlparse

from . import Types
from .Job import Job

class _Queue(EventDispatcher):

    queuedJobs: list[Job] = ListProperty([])

    pausedJobs: list[Job] = ListProperty([])

    _currentJob: Job | None = ObjectProperty(None, allownone=True)
    _currentThread: Thread | None = ObjectProperty(None, allownone=True)

    def __init__(self):
        pass

    def _startNextDownload(self) -> None:

        if (
            (
                self._currentThread is not None
            ) or (
                not self.queuedJobs
            )
        ):
            return

        job = self.queuedJobs[0]

        job.status = "downloading"

        self._currentJob = job

        self._currentThread = Thread(
            target=self._downloadWorker,
            args=(job,),
            daemon=True
        )

        self._currentThread.start()

    def _downloadWorker(
        self,
        job: Job
    ) -> None:
        try:
            job.run()
        except Exception:
            pass
        finally:
            Clock.schedule_once(
                lambda dt: self._onDownloadFinished(job)
            )

    def _onDownloadFinished(
        self,
        job: Job
    ) -> None:

        if job not in self.queuedJobs:
            return

        was_current = (self._currentJob is job)

        if job.status in ("finished", "cancelled", "error") and was_current:
            self.queuedJobs = [j for j in self.queuedJobs if j is not job]

        self._currentJob = None
        self._currentThread = None
        self._startNextDownload()

    def addJob(
        self,
        job: Job
    ) -> None:

        if (
            (
                job in self.queuedJobs
            ) or (
                job in self.pausedJobs
            )
        ):
            return

        self.queuedJobs = self.queuedJobs + [job]

        if self._currentThread is None:
            self._startNextDownload()

    def cancelJob(self, job: Job):

        if (
            (
                job not in self.queuedJobs
            ) and (
                job not in self.pausedJobs
            )
        ):
            return
        
        job.status = "cancelled"

        was_current = (self._currentJob is job)

        self.queuedJobs = [j for j in self.queuedJobs if j is not job]

        if was_current:
            self._currentJob = None
            self._currentThread = None
            self._startNextDownload()
   
    def pauseJob(self, job: Job):

        if (
            (
                job not in self.queuedJobs
            ) or (
                job in self.pausedJobs
            )
        ):
            return

        job.status = "paused"

        was_current = (self._currentJob is job)

        # remove from active queue
        self.queuedJobs = [j for j in self.queuedJobs if j is not job]

        # push to back of paused queue
        self.pausedJobs = self.pausedJobs + [job]

        if was_current:
            self._currentJob = None
            self._currentThread = None
            self._startNextDownload()

    def resumeJob(self, job: Job):

        if (
            (
                job in self.queuedJobs
            ) or (
                job not in self.pausedJobs
            )
        ):
            return

        job.status = "queued"

        # remove from paused queue
        self.pausedJobs  = [j for j in self.pausedJobs if j is not job]

        # push to back of active queue
        self.queuedJobs = [j for j in self.queuedJobs if j is not job]  + [job]

        # if nothing is running, start immediately
        if self._currentJob is None:
            self._startNextDownload()

Queue = _Queue()
