
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import (
    ObjectProperty
)
from kivy.metrics import dp

import Colors

from .Queue import Queue
from .DownloadDatasView import DownloadDatasView

class QueueView(MDBoxLayout):

    queue: Queue = ObjectProperty(Queue())

    queuedDownloadDatasViewLabel: MDLabel
    queuedDownloadDatasView: DownloadDatasView

    pausedDownloadDatasViewLabel: MDLabel
    pausedDownloadDatasView: DownloadDatasView

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("size_hint_x", 1)
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("spacing", dp(12))

        super().__init__(
            orientation="vertical",
            adaptive_height=True,
            **kwargs
        )

        self.queuedDownloadDatasViewLabel = MDLabel(text="Queued Downloads")
        self.queuedDownloadDatasView = DownloadDatasView(
            downloadDatas=self.queue.queuedDownloads
        )

        self.pausedDownloadDatasViewLabel = MDLabel(text="Paused Downloads")
        self.pausedDownloadDatasView = DownloadDatasView(
            downloadDatas=self.queue.pausedDownloads
        )

        self.add_widget(self.queuedDownloadDatasViewLabel)
        self.add_widget(self.queuedDownloadDatasView)
        self.add_widget(self.pausedDownloadDatasViewLabel)
        self.add_widget(self.pausedDownloadDatasView)

        self.bind(
            queue=lambda instance, value: self._onQueue(instance, value)
        )

        if self.queue:
            self._onQueue(
                self,
                self.queue
            )

    def _onQueue(self, instance, value):

        queue = value

        if not queue:
            return

        queue.bind(
            queuedDownloads=lambda instance, value: self._onQueuedDownloads(instance, value),
            pausedDownloads=lambda instance, value: self._onPausedDownloads(instance, value),
        )

        self._onQueuedDownloads(
            queue,
            queue.queuedDownloads
        )
        self._onPausedDownloads(
            queue,
            queue.pausedDownloads
        )

    def _onQueuedDownloads(self, instance, value):
        queuedDownloads = value
        if len(queuedDownloads) <= 0:
            self.queuedDownloadDatasViewLabel.opacity = 0
        else:
            self.queuedDownloadDatasViewLabel.opacity = 1
        self.queuedDownloadDatasView.downloads = queuedDownloads

    def _onPausedDownloads(self, instance, value):
        pausedDownloads = value
        if len(pausedDownloads) <= 0:
            self.pausedDownloadDatasViewLabel.opacity = 0
        else:
            self.pausedDownloadDatasViewLabel.opacity = 1
        self.pausedDownloadDatasView.downloads = pausedDownloads
