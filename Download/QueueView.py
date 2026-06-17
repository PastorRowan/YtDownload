
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty,
    ListProperty
)
from kivy.metrics import dp

import Colors

from .Queue import _Queue
from .JobView import JobView

class QueueView(GridLayout):

    queue: _Queue = ObjectProperty()

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("spacing", 10)
        kwargs.setdefault("padding", 10)

        super().__init__(
            orientation="lr-tb",
            cols=2,
            col_default_width=dp(275),
            **kwargs
        )

        self.bind(
            queue=lambda instance, value: self._onQueueChanged(instance, value)
        )

        if self.queue:
            self._onQueueChanged(
                self,
                self.queue
            )

    def _onQueueChanged(self, instance, queue):

        if not queue:
            return

        queue.bind(
            jobs=self._onJobsChanged
        )

        self._onJobsChanged(
            queue,
            queue.jobs
        )

    def _onJobsChanged(self, instance, jobs):

        self.clear_widgets()

        numberOfJobs = len(jobs)

        for index, job in enumerate(jobs):
            jobView = JobView(
                job=job,
                # width=dp(400),
                # height=dp(300),
                # pos_hint={ "center_x": 0.5, "center_y": 0.5 }
            )
            self.add_widget(jobView)
            if (index == numberOfJobs - 1) and (numberOfJobs % 2 == 1):
                self.add_widget(
                    Widget(
                        size_hint=(1, None)
                    )
                )
