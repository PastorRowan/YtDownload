
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

class JobAudioFormatDialogue(MDDialog):

    job: Job = ObjectProperty(Job())

    selectedAudioExt: str = StringProperty(Job.DEFAULT_AUDIO_EXT)
    audioExtSelector: DropDownSelector

    selectedAbr: str = StringProperty(Job.DEFAULT_ABR)
    abrSelector: DropDownSelector

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioExtSelector = DropDownSelector(
            icon="file-audio-outline",
            values=self.job.audioExts,
        )

        self.abrSelector = DropDownSelector(
            icon="high-definition-box",
            values=self.job.abrs,
            formatter=lambda abr: f"{abr}kbps",
        )

        self.add_widget(
            MDDialogIcon(
                icon="file-audio-outline"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Audio format"
            )
        )

        self.add_widget(

            MDDialogContentContainer(
            
                MDLabel(text="Audio extension"),
                self.audioExtSelector,

                MDLabel(text="Audio bit rate"),
                self.abrSelector,

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

        self.audioExtSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedAudioExt(instance, value)
        )

        self.abrSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedAbr(instance, value)
        )

        self._onJob(self, self.job)

        self.register_event_type("on_confirm")

    def _onJob(self, instance, value):

        job = value

        job.bind(
            audioExts=lambda instance, value: self._onJobAudioExts(instance, value),
            abrs=lambda instance, value: self._onJobAbrs(instance, value)
        )

        self._onJobAudioExts(self, job.audioExts)
        self._onJobAbrs(self, job.abrs)

        self._onSelectedAudioExt(self, self.selectedAudioExt)
        self._onSelectedAbr(self, self.selectedAbr)

    def _onJobAudioExts(self, instance, value):
        print("_onJobAudioExts")

    def _onJobAbrs(self, instance, value):
        print("_onJobAbrs")

    def _onSelectedAudioExt(self, instance, value) -> None:
        print("_onSelectedAudioExt value: ", value)
        self.job.audioExt = value

    def _onSelectedAbr(self, instance, value) -> None:
        print("_onSelectedAbr value: ", value)
        self.job.abr = value

    def on_confirm(self, data):
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _on_confirm(self):

        self.dispatch(
            "on_confirm",
            {
                "ext": self.selectedAudioExt,
                "abr": self.audioExtSelector
            }
        )
