
from typing import (
    List
)

from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import (
    ListProperty
)
from kivy.metrics import dp

import Colors

from .Job import Job
from .JobView import JobView

class JobsView(MDBoxLayout):

    jobs: List[Job] = ListProperty([])

    def __init__(self, **kwargs):

        kwargs.setdefault("spacing", dp(12))
        kwargs.setdefault("padding", dp(12))

        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            size_hint_x=1,
            size_hint_y=None,
            **kwargs
        )

        self.bind(
            jobs=lambda instance, value: self._onJobsChanged(instance, value),
        )

        self._onJobsChanged(self, self.jobs)

    def _onJobsChanged(self, instance, value):

        jobs: List[Job] = value            

        self.clear_widgets()

        for job in jobs:
            jobView = JobView(
                job=job
            )
            self.add_widget(jobView)
