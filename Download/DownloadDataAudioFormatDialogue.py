
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

from .DownloadData import DownloadData

from .Types import (
    AudioExt,
    Abr
)

from widgets import DropDownSelector

class DownloadDataAudioFormatDialogue(MDDialog):

    downloadData: DownloadData = ObjectProperty(DownloadData())

    selectedAudioExt: AudioExt = ObjectProperty(AudioExt.default())
    audioExtSelector: DropDownSelector

    selectedAbr: Abr = ObjectProperty(Abr.default())
    abrSelector: DropDownSelector

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioExtSelector = DropDownSelector(
            icon="file-audio-outline",
            values=self.downloadData.audioExts
        )
        self.audioExtSelector.selectValue(self.selectedAudioExt)

        self.abrSelector = DropDownSelector(
            icon="high-definition-box",
            values=self.downloadData.abrs,
            formatter=lambda abr: f"{abr}kbps"
        )
        self.abrSelector.selectValue(self.selectedAbr)

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
            downloadData=lambda instance, value: self._onDownload(instance, value)
        )

        self.audioExtSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedAudioExt(instance, value)
        )

        self.abrSelector.bind(
            on_selection_changed=lambda instance, value: self._onSelectedAbr(instance, value)
        )

        self._onDownloadData(self, self.downloadData)

        self.register_event_type("on_confirm")

    def _onDownloadData(self, instance, value):

        downloadData = value

        downloadData.bind(
            audioExts=lambda instance, value: self._onDownloadDataAudioExts(instance, value),
            abrs=lambda instance, value: self._onDownloadDataAbrs(instance, value)
        )

        self._onDownloadDataAudioExts(self, downloadData.audioExts)
        self._onDownloadDataAbrs(self, downloadData.abrs)

        self._onSelectedAudioExt(self, self.selectedAudioExt)
        self._onSelectedAbr(self, self.selectedAbr)

    def _onDownloadDataAudioExts(self, instance, value):
        print("_onDownloadDataAudioExts")

    def _onDownloadDataAbrs(self, instance, value):
        print("_onDownloadAbrs")

    def _onSelectedAudioExt(self, instance, value) -> None:
        print("_onSelectedAudioExt value: ", value)
        self.downloadData.audioExt = value

    def _onSelectedAbr(self, instance, value) -> None:
        print("_onSelectedAbr value: ", value)
        self.downloadData.abr = value

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
                "abr": self.selectedAbr
            }
        )
