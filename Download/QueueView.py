
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
from .JobsView import JobsView

class QueueView(MDBoxLayout):

    queue: Queue = ObjectProperty()

    queuedJobsViewLabel: MDLabel
    queuedJobsView: JobsView

    pausedJobsViewLabel: MDLabel
    pausedJobsView: JobsView

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

        self.queuedJobsViewLabel = MDLabel(text="Queued Downloads")
        self.queuedJobsView = JobsView(
            jobs=self.queue.queuedJobs
        )

        self.pausedJobsViewLabel = MDLabel(text="Paused Downloads")
        self.pausedJobsView = JobsView(
            jobs=self.queue.pausedJobs
        )

        self.add_widget(self.queuedJobsViewLabel)
        self.add_widget(self.queuedJobsView)
        self.add_widget(self.pausedJobsViewLabel)
        self.add_widget(self.pausedJobsView)

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
            queuedJobs=lambda instance, value: self._onQueuedJobs(instance, value),
            pausedJobs=lambda instance, value: self._onPausedJobs(instance, value),
        )

        self._onQueuedJobs(
            queue,
            queue.queuedJobs
        )
        self._onPausedJobs(
            queue,
            queue.pausedJobs
        )

    def _onQueuedJobs(self, instance, value):
        queuedJobs = value
        if len(queuedJobs) <= 0:
            self.queuedJobsViewLabel.opacity = 0
        else:
            self.queuedJobsViewLabel.opacity = 1
        self.queuedJobsView.jobs = queuedJobs

    def _onPausedJobs(self, instance, value):
        pausedJobs = value
        if len(pausedJobs) <= 0:
            self.pausedJobsViewLabel.opacity = 0
        else:
            self.pausedJobsViewLabel.opacity = 1
        self.pausedJobsView.jobs = pausedJobs
