

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.image import AsyncImage
from kivy.metrics import dp, sp
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty
)

from Download.DownloadJob import DownloadJob

class DownloadJobView(MDCard):

    job: DownloadJob = ObjectProperty(None)

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            size_hint=(None, None),
            size_hint_x=1,
            size_hint_y=None,
            adaptive_height=True,
            **kwargs
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(1, None),
            source=self.job.thumbnail,
            fit_mode="cover"
        )

        self.bottomBar = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True
        )

        self.titleLabel = MDLabel(
            size_hint=(1, None),
            adaptive_height=True,
            text=self.job.title,
            font_size=sp(12),
            bold=True
        )

        self.channelLabel = MDLabel(
            size_hint=(1, None),
            adaptive_height=True,
            text=self.job.channel,
            font_size=sp(10),
            theme_text_color="Secondary",
        )

        self.progressIndicator = MDLinearProgressIndicator(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(3),
            type="determinate",
            value=0
        )

        self.bottomBar.add_widget(self.titleLabel)
        self.bottomBar.add_widget(self.channelLabel)
        self.bottomBar.add_widget(self.progressIndicator)

        self.add_widget(self.thumbnailImage)
        self.add_widget(self.bottomBar)

        self.bind(width=self._updateImageHeight)

        if self.job:
            self._on_job_changed(self, self.job)

    def _onJobThumbnail(self, instance, value):
        self.thumbnailImage.source = value

    def _onJobTitle(self, instance, value):
        self.titleLabel.text = value

    def _onJobChannel(self, instance, value):
        self.channelLabel.text = value

    def _onJobProgress(self, instance, value):
        print("progress changed: ", value)
        self.progressIndicator.value = value * 100

    def _on_job_changed(self, instance, job):

        if not job:
            return

        self.thumbnailImage.source = job.thumbnail
        self.titleLabel.text = job.title
        self.channelLabel.text = job.channel
        self.progressIndicator.value = job.progress

        job.bind(
            thumbnail=self._onJobThumbnail,
            title=self._onJobTitle,
            channel=self._onJobChannel,
            progress=self._onJobProgress,
        )

    def _updateImageHeight(self, *args) -> None:
        self.thumbnailImage.height = self.width * 9 / 16

