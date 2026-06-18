
from typing import (
    List
)

from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.widget import Widget

from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty,
    ListProperty
)
from kivy.metrics import dp

import Colors

from .Job import Job
from .JobView import JobView

class JobsView(GridLayout):

    jobs: List[Job] = ListProperty([])

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("size_hint_x", 1)
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("spacing", dp(12))
        kwargs.setdefault("padding", dp(12))
        kwargs.setdefault("row_force_default", False)
        kwargs.setdefault("col_force_default", False)

        super().__init__(
            orientation="lr-tb",
            cols=2,
            col_default_width=dp(275),
            **kwargs
        )

        self.bind(
            jobs=lambda instance, value: self._onJobsChanged(instance, value),
        )

        self._onJobsChanged(self, self.jobs)

    def _onJobsChanged(self, instance, value):

        jobs: List[Job] = value            

        self.clear_widgets()

        numberOfJobs = len(jobs)

        for index, job in enumerate(jobs):
            jobView = JobView(
                job=job
            )
            self.add_widget(jobView)
            if (index == numberOfJobs - 1) and (numberOfJobs % 2 == 1):
                self.add_widget(
                    Widget(
                        size_hint=(1, None)
                    )
                )
            print("jobView: ", jobView.height, jobView.width)
