

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget

from kivy.uix.image import AsyncImage
from kivy.metrics import dp, sp
from kivy.properties import (
    ObjectProperty
)

from .Job import Job
from .Queue import Queue

import Colors

class JobView(MDCard):

    job: Job = ObjectProperty(Job())
    vBoxLayout: MDBoxLayout
    hBoxLayout: MDBoxLayout
    thumbnailImage: AsyncImage
    titleLabel: MDLabel
    dataLabel: MDLabel
    etaLabel: MDLabel
    progressIndicator: MDLinearProgressIndicator

    def __init__(
        self,
        **kwargs
    ):

        kwargs.setdefault("height", dp(70))

        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            size_hint_x=1,
            size_hint_y=None,
            **kwargs
        )

        progressIndicatorHeight: float = dp(3)

        self.downloadLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.contentLayout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 1)
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(None, None),
            source=self.job.thumbnail,
            fit_mode="contain"
        )

        self.infoLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=(0, dp(4)),
            #spacing=dp(2)
        )

        self.titleLabel = MDLabel(
            size_hint=(1, 1),
            text=self.job.title,
            font_size=sp(14),
            max_lines=1
        )
        # text_color=(0.0941, 0.1059, 0.1255, 1)
        # it is the theme text color

        print("self.theme_cls.text_color: ", self.theme_cls.text_color)

        self.statusLabel = MDLabel(
            theme_text_color="Custom",
            text=str(self.job.eta),
            size_hint=(1, 1),
            text_color=(0.5176, 0.5176, 0.5176, 1),
            font_size=sp(12)
        )

        self.infoLayout.add_widget(
            Widget(
                height=progressIndicatorHeight,
                size_hint=(1, None)
            )
        )
        self.infoLayout.add_widget(self.titleLabel)
        self.infoLayout.add_widget(self.statusLabel)

        self.progressIndicator = MDLinearProgressIndicator(
            orientation="horizontal",
            size_hint=(1, None),
            height=progressIndicatorHeight,
            type="determinate",
            value=0
        )

        self.contentLayout.add_widget(self.thumbnailImage)
        self.contentLayout.add_widget(
            Widget(
                width=dp(20),
                size_hint=(None, 1)
            )
        )
        self.contentLayout.add_widget(self.infoLayout)

        self.downloadLayout.add_widget(self.contentLayout)
        self.downloadLayout.add_widget(self.progressIndicator)

        self.add_widget(self.downloadLayout)

        self.contentLayout.bind(
            height=lambda instance, value: self._onContentLayoutHeight(instance, value)
        )

        self._onJobChanged(self, self.job)

    def _onContentLayoutHeight(self, instance, value):
        contentLayoutHeight = value
        self.thumbnailImage.height = contentLayoutHeight
        self.thumbnailImage.width = contentLayoutHeight * (16 / 9)

    def _updateStatusLabel(self):

        downloadedBytes = self.job.downloadedBytes
        totalBytes = self.job.totalBytes
        eta = self.job.eta

        downloadedMB = round(downloadedBytes / (1024 * 1024))
        totalMB = round(totalBytes / (1024 * 1024))

        etaStr = ""

        seconds = int(max(0, eta))

        minutes, secs = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        etaStr = f"{hours}:{minutes:02}:{secs:02}"

        self.statusLabel.text = (
            f"{downloadedMB} MB of {totalMB} MB / {etaStr}"
        )

    def _onJobThumbnail(self, instance, value):
        print("_onJobThumbnail value: ", value)
        self.thumbnailImage.source = value

    def _onJobTitle(self, instance, value):
        print("_onJobTitle value: ", value)

        title = value or ""

        MAX_CHARS = 70

        if len(title) > MAX_CHARS:
            title = title[:MAX_CHARS - 3] + "..."

        self.titleLabel.text = title

    def _onJobProgress(self, instance, value):
        print("_onJobProgress value: ", value)
        self.progressIndicator.value = value * 100

    def _onJobDownloadedBytes(self, instance, value):
        print("_onJobDownloadedBytes value: ", value)
        self._updateStatusLabel()

    def _onJobEta(self, instance, value) -> None:
        print("_onJobEta value: ", value)
        self._updateStatusLabel()

    def _onJobSpeed(self, instance, value):
        print("_onJobSpeed value", value)

    def _onJobStatus(self, instance, value):
        newStatus = value
        print("_onJobStatus value", value)

    def _onJobChanged(self, instance, job):

        if not job:
            return

        job.bind(
            thumbnail=lambda instance, value: self._onJobThumbnail(instance, value),
            title=lambda instance, value: self._onJobTitle(instance, value),
            progress=lambda instance, value: self._onJobProgress(instance, value),
            status=lambda instance, value: self._onJobStatus(instance, value),
            eta=lambda instance, value: self._onJobEta(instance, value),
            downloadedBytes=lambda instance, value: self._onJobDownloadedBytes(instance, value),
            speed=lambda instance, value: self._onJobSpeed(instance, value)
        )

        self._onJobThumbnail(instance, job.thumbnail)
        self._onJobTitle(instance, job.title)
        self._onJobProgress(instance, job.progress)
        self._onJobStatus(instance, job.status)
        self._onJobEta(instance, job.eta)
        self._onJobSpeed(instance, job.speed)
