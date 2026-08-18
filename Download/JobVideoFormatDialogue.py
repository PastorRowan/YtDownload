
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

from .Job import Job

from widgets import DropDownSelector

class JobVideoFormatDialogue(MDDialog):

    job: Job = ObjectProperty(Job())

    selectedVideoExt: str = StringProperty(Job.DEFAULT_VIDEO_EXT)
    videoExtSelector: DropDownSelector

    selectedVideoHeight: str = StringProperty(Job.DEFAULT_VIDEO_HEIGHT)
    videoHeightSelector: DropDownSelector

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoExtSelector = DropDownSelector(
            icon="file-video-outline",
            values=self.job.videoExts
        )
        self.videoExtSelector.select(Job.DEFAULT_VIDEO_EXT_INDEX)

        self.videoHeightSelector = DropDownSelector(
            icon="high-definition-box",
            values=self.job.videoHeights,
            formatter=lambda videoHeight: f"{videoHeight}p"
        )
        self.videoHeightSelector.select(Job.DEFAULT_VIDEO_HEIGHT_INDEX)

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
            job=lambda instance, value: self._onJob(instance, value)
        )

        self.videoExtSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedVideoExt(instance, value)
        )

        self.videoHeightSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedVideoHeight(instance, value)
        )

        self._onJob(self, self.job)

        self.register_event_type("on_confirm")

    def _onJob(self, instance, value):

        job = value

        job.bind(
            videoExts=lambda instance, value: self._onJobVideoExts(instance, value),
            videoHeights=lambda instance, value: self._onJobVideoHeights(instance, value)
        )

        self._onJobVideoExts(self, job.videoExts)
        self._onJobVideoHeights(self, job.videoHeights)

        self._onSelectedVideoExt(self, self.selectedVideoExt)
        self._onSelectedVideoHeight(self, self.selectedVideoHeight)

    def _onJobVideoExts(self, instance, value) -> None:
        print("_onJobVideoExts")

    def _onJobVideoHeights(self, instance, value) -> None:
        print("_onJobVideoHeights")

    def _onSelectedVideoExt(self, instance, value) -> None:
        print("_onSelectedVideoExt value: ", value)
        self.job.videoExt = value

    def _onSelectedVideoHeight(self, instance, value) -> None:
        print("_onSelectedVideoHeight value: ", value)
        self.job.videoHeight = value

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
