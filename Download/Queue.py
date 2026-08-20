
from kivy.event import EventDispatcher
from kivy.properties import (
    ObjectProperty,
    ListProperty
)
from kivy.clock import Clock

from threading import Thread

from .Types import Status
from .DownloadData import DownloadData
from .runDownload import runDownload

class Queue(EventDispatcher):

    queuedDownloads: list[DownloadData] = ListProperty([])

    pausedDownloads: list[DownloadData] = ListProperty([])

    _currentDownload: DownloadData | None = ObjectProperty(None, allownone=True)
    _currentThread: Thread | None = ObjectProperty(None, allownone=True)

    def __init__(self):
        pass

    def _startNextDownload(self) -> None:

        if (
            (
                self._currentThread is not None
            ) or (
                not self.queuedDownloads
            )
        ):
            return

        downloadData = self.queuedDownloads[0]

        downloadData.status = Status.DOWNLOADING

        self._currentDownload = downloadData

        self._currentThread = Thread(
            target=self._downloadWorker,
            args=(downloadData,),
            daemon=True
        )

        self._currentThread.start()

    def _downloadWorker(
        self,
        downloadData: DownloadData
    ) -> None:
        try:
            runDownload(downloadData)
        except Exception:
            pass
        finally:
            Clock.schedule_once(
                lambda dt: self._onDownloadFinished(downloadData)
            )

    def _onDownloadFinished(
        self,
        downloadData: DownloadData
    ) -> None:

        if downloadData not in self.queuedDownloads:
            return

        was_current = (self._currentDownload is downloadData)

        if downloadData.status in ("finished", "cancelled", "error") and was_current:
            self.queuedDownloads = [j for j in self.queuedDownloads if j is not downloadData]

        self._currentDownload = None
        self._currentThread = None
        self._startNextDownload()

    def addDownload(
        self,
        downloadData: DownloadData
    ) -> None:

        if (
            (
                downloadData in self.queuedDownloads
            ) or (
                downloadData in self.pausedDownloads
            )
        ):
            return

        if downloadData.status in (Status.QUEUED, Status.DOWNLOADING):
            self.queuedDownloads = self.queuedDownloads + [downloadData]

        if downloadData.status == Status.PAUSED:
            self.pausedDownloads = self.pausedDownloads + [downloadData]

        if self._currentThread is None:
            self._startNextDownload()

    def cancelDownload(
        self, downloadData: DownloadData
    ):

        if (
            (
                downloadData not in self.queuedDownloads
            ) and (
                downloadData not in self.pausedDownloads
            )
        ):
            return
        
        downloadData.status = Status.CANCELLED

        self.queuedDownloads = [j for j in self.queuedDownloads if j is not downloadData]

        was_current = (self._currentDownload is downloadData)

        if was_current:
            self._currentDownload = None
            self._currentThread = None
            self._startNextDownload()
   
    def pauseDownload(self, downloadData: DownloadData):

        if (
            (
                downloadData not in self.queuedDownloads
            ) or (
                downloadData in self.pausedDownloads
            )
        ):
            return

        downloadData.status = Status.PAUSED

        was_current = (self._currentDownload is downloadData)

        # remove from active queue
        self.queuedDownloads = [j for j in self.queuedDownloads if j is not downloadData]

        # push to back of paused queue
        self.pausedDownloads = self.pausedDownloads + [downloadData]

        if was_current:
            self._currentDownload = None
            self._currentThread = None
            self._startNextDownload()

    def resumeDownload(self, downloadData: DownloadData):

        if (
            (
                downloadData in self.queuedDownloads
            ) or (
                downloadData not in self.pausedDownloads
            )
        ):
            return

        downloadData.status = Status.QUEUED

        # remove from paused queue
        self.pausedDownloads  = [j for j in self.pausedDownloads if j is not downloadData]

        # push to back of active queue
        self.queuedDownloads = [j for j in self.queuedDownloads if j is not downloadData]  + [downloadData]

        # if nothing is running, start immediately
        if self._currentDownload is None:
            self._startNextDownload()
