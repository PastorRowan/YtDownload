

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import (
    MDButton,
    MDButtonIcon,
    MDIconButton
)

from MDIconButtonCustom import MDIconButtonCustom

#test = MDIconButton()


from kivy.uix.image import AsyncImage
from kivy.metrics import dp, sp
from kivy.properties import (
    ObjectProperty
)

from .Job import Job
from .Queue import Queue

import KivyCustomGraphics

import Colors

class JobView(MDCard):

    job: Job = ObjectProperty(Job())
    thumbnailContainer: MDFloatLayout
    thumbnailImage: AsyncImage
    cancelIconButton: MDButtonIcon
    pausePlayIconButton: MDIconButton
    etaLabel: MDLabel
    bottomBar: MDBoxLayout
    titleLabel: MDLabel
    channelLabel: MDLabel
    progressIndicator: MDLinearProgressIndicator

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            size_hint_x=1,
            size_hint_y=None,
            adaptive_height=True,
            adaptive_width=False,
            **kwargs
        )

        self.thumbnailContainer = MDFloatLayout(
            size_hint=(1, None),
            height=dp(50)
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(1, None),
            source=self.job.thumbnail,
            fit_mode="cover",
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        self.cancelIconButton = MDIconButton(
            theme_width="Custom",
            theme_height="Custom",
            theme_font_size="Custom",
            theme_icon_color="Custom",
            theme_bg_color="Custom",
            icon="pause-circle-outline",
            size_hint=(1, 1),
            size=(dp(100), dp(100)),
            font_size=sp(50),
            pos_hint={
                "right": 1,
                "y": 1
            }
        )

        self.pausePlayIconButton = MDIconButtonCustom(
            theme_width="Custom",
            theme_height="Custom",
            theme_font_size="Custom",
            theme_icon_color="Custom",
            theme_bg_color="Custom",
            icon="pause-circle-outline",
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            adaptive_size=False,
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            },
            font_size=sp(50),
            icon_color=Colors.black,
            md_bg_color=Colors.grey,
            on_release=lambda dt: self._onPausePlayIconButtonRelease(dt)
        )

        self.etaLabel = MDLabel(
            text=str(self.job.eta),
            size_hint=(None, None),
            adaptive_size=True,
            pos_hint={
                "right": 0.98,
                "y": 0.02
            },
            md_bg_color=(0, 0, 0, 0.5),
        )

        self.thumbnailContainer.add_widget(self.thumbnailImage)
        self.thumbnailContainer.add_widget(self.cancelIconButton)
        self.thumbnailContainer.add_widget(self.pausePlayIconButton)
        self.thumbnailContainer.add_widget(self.etaLabel)

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

        self.add_widget(self.thumbnailContainer)
        self.add_widget(self.bottomBar)

        self.bind(width=lambda instance, value: self._onWidth(instance, value))

        """
        self.bind(width=self._updateImageHeight)
        """

        self._onJobChanged(self, self.job)

    def _onJobThumbnail(self, instance, value):
        self.thumbnailImage.source = value

    def _onJobTitle(self, instance, value):
        self.titleLabel.text = value

    def _onJobChannel(self, instance, value):
        self.channelLabel.text = value

    def _onJobProgress(self, instance, value):
        self.progressIndicator.value = value * 100

    def _onJobEta(self, instance, value) -> None:

        if value is None:
            return
        
        etaStr = ""

        seconds = int(max(0, value))

        minutes, secs = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            etaStr = f"{hours}:{minutes:02}:{secs:02}"
        else:
            etaStr = f"{minutes}:{secs:02}"

        self.etaLabel.text = etaStr

    def _onJobSpeed(self, instance, value):
        pass

    def _onJobStatus(self, instance, value):
    
        newStatus = value
    
        match newStatus:
            case "downloading":
                self.pausePlayIconButton.icon = "pause-circle-outline"
            case "paused":
                self.pausePlayIconButton.icon = "play-circle-outline"
            case _:
                pass

    def _onJobChanged(self, instance, job):

        if not job:
            return

        job.bind(
            thumbnail=lambda instance, value: self._onJobThumbnail(instance, value),
            title=lambda instance, value: self._onJobTitle(instance, value),
            channel=lambda instance, value: self._onJobChannel(instance, value),
            progress=lambda instance, value: self._onJobProgress(instance, value),
            status=lambda instance, value: self._onJobStatus(instance, value),
            eta=lambda instance, value: self._onJobEta(instance, value),
            speed=lambda instance, value: self._onJobSpeed(instance, value)
        )

        self._onJobThumbnail(instance, job.thumbnail)
        self._onJobTitle(instance, job.title)
        self._onJobChannel(instance, job.channel)
        self._onJobProgress(instance, job.progress)
        self._onJobStatus(instance, job.status)
        self._onJobEta(instance, job.eta)
        self._onJobSpeed(instance, job.speed)

    def _onPausePlayIconButtonRelease(self, dt: int) -> None:

        if (
            self.job.status == "downloading" or
            self.job.status == "queued"
        ):
            Queue.pauseJob(self.job)
        elif self.job.status == "paused":
            Queue.resumeJob(self.job)

    def _onWidth(self, *args) -> None:
        height = self.width * 9 / 16

        self.thumbnailContainer.height = height
        self.thumbnailImage.height = height

    """
    def _updateImageHeight(self, *args) -> None:
        self.thumbnailImage.height = self.width * 9 / 16
    """
