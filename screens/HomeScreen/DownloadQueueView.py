
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

import Colors

from DownloadQueue import (
    DownloadQueue
)

from VideoInfoCard import VideoInfoCard

class DownloadQueueView(GridLayout):

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("spacing", 10)
        kwargs.setdefault("padding", 10)

        super().__init__(
            cols=2,
            **kwargs
        )

        self.bind(
            minimum_height=self.setter("height")
        )

        DownloadQueue.bind(
            jobs=lambda instance, value: self._on_jobs_changed(instance, value)
        )
        self._on_jobs_changed(DownloadQueue, DownloadQueue.jobs)

    def _on_jobs_changed(self, instance, jobs):

        self.clear_widgets()

        for job in jobs:
            jobCard = VideoInfoCard(
                thumbnailLink=job.thumbnail,
                title=job.title,
                author=job.channel,
            )
            self.add_widget(jobCard)
