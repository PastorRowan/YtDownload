
from typing import (
    List
)

from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDActionTopAppBarButton
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp, sp

from screens.navigateToScreen import navigateToScreen

import Colors

from db.DownloadJob import getAllDownloadJobs

import Download

class DownloadsScreen(MDScreen):

    topAppBar: MDTopAppBar
    scroll: MDScrollView
    content: MDBoxLayout
    downloadsScreenTitle: MDLabel
    downloadJobs: List[Download.Job]
    downloadJobsView: Download.JobsView

    def on_pre_enter(self):
        self.build_downloads()

    def build_downloads(self):

        self.topAppBar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    icon_color=Colors.black,
                    on_release=lambda instance: self._onTopAppBarBackArrowButtonRelease(instance)
                ),
            ),
            type="small",
            size_hint=(1, 0.125),
            pos_hint={
                "x": 0,
                "y": 0.875
            },
            padding=(dp(30), dp(30))
        )

        self.scroll = MDScrollView(
            size_hint=(1, 0.875),
            pos_hint={
                "x": 0,
                "y": 0
            }
        )

        self.content = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True,
            padding=(dp(50), dp(50))
        )

        self.downloadsScreenTitle = MDLabel(
            text="Settings",
            bold=True,
            font_size=sp(15),
            size_hint_y=None,
            height=dp(50)
        )

        self.downloads = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True
        )

        downloadJobRecords = getAllDownloadJobs()

        self.downloadJobs.clear()

        for downloadJobRecord in downloadJobRecords:
            self.downloadJobs.append(Download.Job(
                *downloadJobRecord
            ))

        self.downloadJobsView = Download.JobsView(self.downloadJobs)

        self.content.add_widget(self.downloadsScreenTitle)
        self.content.add_widget(self.downloadJobsView)

        self.scroll.add_widget(self.content)

        self.add_widget(self.topAppBar)
        self.add_widget(self.scroll)

    def _onTopAppBarBackArrowButtonRelease(self, instance):
        navigateToScreen("home")
