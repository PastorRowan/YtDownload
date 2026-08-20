

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivymd.uix.button import MDIconButton

from kivy.uix.image import AsyncImage
from kivy.metrics import dp, sp
from kivy.properties import (
    ObjectProperty
)

from .Types.DownloadTypes import Status
from .DownloadData import DownloadData

import Colors

class DownloadDataView(MDCard):

    downloadData: DownloadData = ObjectProperty(DownloadData())

    contentLayout: MDBoxLayout
    thumbnailImage: AsyncImage
    infoLayout: MDBoxLayout
    menuContainer: MDBoxLayout
    menuButton: MDIconButton
    menu: MDDropdownMenu
    titleLabel: MDLabel
    statusLabel: MDLabel
    progressIndicator: MDLinearProgressIndicator
    progressIndicatorHeight: float = dp(3)

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
            padding=0,
            spacing=0,
            radius=[0, 0, 0, 0],
            style="outlined",
            line_color=(0.7, 0.7, 0.7, 1),
            line_width=1,
            **kwargs
        )

        self.contentLayout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 1)
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(None, None),
            source=self.downloadData.thumbnail,
            fit_mode="contain"
        )

        self.infoLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.titleLabel = MDLabel(
            size_hint=(1, 1),
            text=self.downloadData.title,
            font_size=sp(14),
            max_lines=1
        )
        # text_color=(0.0941, 0.1059, 0.1255, 1)
        # it is the theme text color

        print("self.theme_cls.text_color: ", self.theme_cls.text_color)

        self.statusLabel = MDLabel(
            theme_text_color="Custom",
            text=str(self.downloadData.eta),
            size_hint=(1, 1),
            text_color=(0.5176, 0.5176, 0.5176, 1),
            font_size=sp(12)
        )

        self.infoLayout.add_widget(
            Widget(
                height=self.progressIndicatorHeight,
                size_hint=(1, None)
            )
        )
        self.infoLayout.add_widget(self.titleLabel)
        self.infoLayout.add_widget(self.statusLabel)

        self.menuButtonContainer = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(48)
        )

        self.menuButton = MDIconButton(
            icon="dots-vertical",
            size_hint=(1, 1)
        )

        self.menu = MDDropdownMenu(
            caller=self.menuButton,
            items=[
                {
                    "text": "Pause",
                    "on_release": lambda: self._onPauseButtonRelease()
                },
                {
                    "text": "Resume",
                    "on_release": lambda: self._onResumeButtonRelease()
                },
                {
                    "text": "Cancel",
                    "on_release": lambda: self._onCancelButtonRelease()
                },
            ],
            hor_growth="left"
        )

        self.menuButtonContainer.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        self.menuButtonContainer.add_widget(self.menuButton)
        self.menuButtonContainer.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        
        self.progressIndicator = MDLinearProgressIndicator(
            orientation="horizontal",
            size_hint=(1, None),
            height=self.progressIndicatorHeight,
            type="determinate",
            value=0
        )

        self.contentLayout.add_widget(self.thumbnailImage)
        self.contentLayout.add_widget(self.infoLayout)
        self.contentLayout.add_widget(self.menuButtonContainer)

        self.add_widget(self.contentLayout)
        self.add_widget(self.progressIndicator)

        self.contentLayout.bind(
            height=lambda instance, value: self._onContentLayoutHeight(instance, value)
        )

        self.menuButton.bind(
            on_release=lambda instance: self._onMenuButtonRelease(instance)
        )

        self._onDownloadDataChanged(self, self.downloadData)

    def _onContentLayoutHeight(self, instance, value):
        contentLayoutHeight = value
        self.thumbnailImage.height = contentLayoutHeight
        self.thumbnailImage.width = contentLayoutHeight * (16 / 9)

    def _updateStatusLabel(self):

        downloadedBytes = self.downloadData.downloadedBytes
        totalBytes = self.downloadData.totalBytes
        eta = self.downloadData.eta

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

    def _onDownloadDataThumbnail(self, instance, value):
        print("_onDownloadDataThumbnail value: ", value)
        self.thumbnailImage.source = value

    def _onDownloadDataTitle(self, instance, value):
        print("_onDownloadDataTitle value: ", value)

        title = value or ""

        MAX_CHARS = 70

        if len(title) > MAX_CHARS:
            title = title[:MAX_CHARS - 3] + "..."

        self.titleLabel.text = title

    def _onDownloadDataProgress(self, instance, value) -> None:
        print("_onDownloadDataProgress value: ", value)
        progress: float = value
        self.progressIndicator.value = progress * 100

    def _onDownloadDataDownloadedBytes(self, instance, value) -> None:
        print("_onDownloadDataDownloadedBytes value: ", value)
        downloadedBytes: int = value
        self._updateStatusLabel()

    def _onDownloadDataEta(self, instance, value) -> None:
        print("_onDownloadDataEta value: ", value)
        self._updateStatusLabel()

    def _onDownloadDataSpeed(self, instance, value) -> None:
        print("_onDownloadDataSpeed value", value)

    def _onDownloadDataStatus(self, instance, value) -> None:
        print("_onDownloadDataStatus value", value)
        newStatus = value

    def _onDownloadDataChanged(self, instance, value) -> None:

        downloadData: DownloadData = value

        if not downloadData:
            return

        downloadData.bind(
            thumbnail=lambda instance, value: self._onDownloadDataThumbnail(instance, value),
            title=lambda instance, value: self._onDownloadDataTitle(instance, value),
            progress=lambda instance, value: self._onDownloadDataProgress(instance, value),
            status=lambda instance, value: self._onDownloadDataStatus(instance, value),
            eta=lambda instance, value: self._onDownloadDataEta(instance, value),
            downloadedBytes=lambda instance, value: self._onDownloadDataDownloadedBytes(instance, value),
            speed=lambda instance, value: self._onDownloadDataSpeed(instance, value)
        )

        self._onDownloadDataThumbnail(instance, downloadData.thumbnail)
        self._onDownloadDataTitle(instance, downloadData.title)
        self._onDownloadDataProgress(instance, downloadData.progress)
        self._onDownloadDataStatus(instance, downloadData.status)
        self._onDownloadDataEta(instance, downloadData.eta)
        self._onDownloadDataDownloadedBytes(instance, downloadData.downloadedBytes)
        self._onDownloadDataSpeed(instance, downloadData.speed)

    def _onMenuButtonRelease(self, instance) -> None:
        self.menu.open()

    def _onPauseButtonRelease(self) -> None:
        if self.downloadData.status != Status.PAUSED:
            self.downloadData.status = Status.PAUSED
        self.menu.dismiss()

    def _onResumeButtonRelease(self) -> None:
        if self.downloadData.status != Status.QUEUED:
            self.downloadData.status = Status.QUEUED
        self.menu.dismiss()

    def _onCancelButtonRelease(self) -> None:
        if self.downloadData.status != Status.CANCELLED:
            self.downloadData.status = Status.CANCELLED
        self.menu.dismiss()
