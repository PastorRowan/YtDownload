
from typing import (
    TypedDict,
    Callable
)

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
    MDDialogIcon
)
from kivymd.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDButton,
    MDButtonText
)
from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    ListProperty
)
from kivy.metrics import dp

from .Types import (
    VideoExt,
    VideoHeight
)

from .DownloadData import DownloadData

from widgets import DropDownSelector

class DownloadDataVideoFormatDialogue(MDDialog):

    downloadData: DownloadData = ObjectProperty(DownloadData())

    selectedVideoExt: VideoExt = ObjectProperty(VideoExt.default())
    videoExtSelector: DropDownSelector

    selectedVideoHeight: VideoHeight = ObjectProperty(VideoHeight.default())
    videoHeightSelector: DropDownSelector

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoExtSelector = DropDownSelector(
            icon="file-video-outline",
            values=self.downloadData.videoExts
        )
        self.videoExtSelector.selectValue(self.selectedVideoExt)

        self.videoHeightSelector = DropDownSelector(
            icon="high-definition-box",
            values=self.downloadData.videoHeights,
            formatter=lambda videoHeight: f"{videoHeight}p"
        )
        self.videoHeightSelector.selectValue(self.selectedVideoHeight)

        self.add_widget(
            MDDialogIcon(
                icon="file-video-outline"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Video format"
            )
        )

        self.add_widget(

            MDDialogContentContainer(
            
                MDLabel(text="Video extension"),
                self.videoExtSelector,

                MDLabel(text="Video height"),
                self.videoHeightSelector,

                MDDialogButtonContainer(
                    Widget(
                        size_hint=(1, None),
                        height=0
                    ),
                    MDButton(
                        MDButtonText(
                            text="Cancel"
                        ),
                        style="text",
                        on_release=lambda dt: self.dismiss()
                    ),
                    MDButton(
                        MDButtonText(
                            text="Confirm"
                        ),
                        style="text",
                        on_release=lambda dt: self._on_confirm()
                    ),
                    spacing="8dp"
                ),

                orientation="vertical",
                spacing="12dp",
                padding="12dp",
                size_hint=(1, None)

            )

        )

        self.bind(
            downloadData=lambda instance, value: self._onDownloadData(instance, value)
        )

        self.videoExtSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedVideoExt(instance, value)
        )

        self.videoHeightSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedVideoHeight(instance, value)
        )

        self._onDownloadData(self, self.downloadData)

        self.register_event_type("on_confirm")

    def _onDownloadData(self, instance, value):

        downloadData = value

        downloadData.bind(
            videoExts=lambda instance, value: self._onDownloadDataVideoExts(instance, value),
            videoHeights=lambda instance, value: self._onDownloadDataVideoHeights(instance, value)
        )

        self._onDownloadDataVideoExts(self, downloadData.videoExts)
        self._onDownloadDataVideoHeights(self, downloadData.videoHeights)

        self._onSelectedVideoExt(self, self.selectedVideoExt)
        self._onSelectedVideoHeight(self, self.selectedVideoHeight)

    def _onDownloadDataVideoExts(self, instance, value) -> None:
        print("_onDownloadDataVideoExts")

    def _onDownloadDataVideoHeights(self, instance, value) -> None:
        print("_onDownloadDataVideoHeights")

    def _onSelectedVideoExt(self, instance, value) -> None:
        print("_onSelectedVideoExt value: ", value)
        self.downloadData.videoExt = value

    def _onSelectedVideoHeight(self, instance, value) -> None:
        print("_onSelectedVideoHeight value: ", value)
        self.downloadData.videoHeight = value

    def on_confirm(self, data) -> None:
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _on_confirm(self) -> None:

        self.dispatch(
            "on_confirm",
            {
                "ext": self.selectedVideoExt,
                "height": self.selectedVideoHeight
            }
        )
