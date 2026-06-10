
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer
)
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDButton,
    MDButtonText,
    MDButtonIcon
)
from kivymd.uix.segmentedbutton import (
    MDSegmentedButton,
    MDSegmentedButtonItem,
    MDSegmentButtonIcon,
    MDSegmentButtonLabel
)
from kivymd.uix.chip import (
    MDChip,
    MDChipLeadingIcon,
    MDChipText
)

from screens.HomeScreen.SelectVideoQualityDialogue import SelectVideoQualityDialogue

from screens.HomeScreen.SelectAudioFormatDialogue import SelectAudioFormatDialogue

class DownloadOptionsDialogue(MDDialog):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.selectedOptions = {
            "fileName": "",
            "downloadType": "",
            "videoFormat": "",
            "audioFormat": ""
        }

        self.container = MDDialogContentContainer(
            orientation="vertical",
            spacing="12dp",
            padding="12dp"
        )

        self.fileNameFieldVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )

        self.fileNameFieldVBox.add_widget(
            MDLabel(
                text="File name",
                size_hint=(1, None),
                height=30
            )
        )
        self.fileNameFieldVBox.add_widget(
            MDTextField(
                size_hint=(1, None),
                text="",
                hint_text="File Name",
                multiline=False
            )
        )

        self.downloadTyeVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )

        self.downloadTyeVBox.add_widget(
            MDLabel(
                text="Download type",
                size_hint=(1, None),
                height=30
            )
        )

        self.downloadTyeVBox.add_widget(
            MDSegmentedButton(
                MDSegmentedButtonItem(
                    MDSegmentButtonIcon(
                        icon="file-video-outline"
                    ),
                    MDSegmentButtonLabel(
                        text="Video"
                    ),
                    on_release=lambda x: self.onDownloadTypeSelect("video")
                ),
                MDSegmentedButtonItem(
                    MDSegmentButtonIcon(
                        icon="music"
                    ),
                    MDSegmentButtonLabel(
                        text="Audio"
                    ),
                    on_release=lambda x: self.onDownloadTypeSelect("audio")
                )
            )
        )

        self.formatPreferenceVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )

        self.formatPreferenceChipButtonContainer = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )
        self.formatPreferenceChipButtonContainer.add_widget(
            MDChip( 
                MDChipLeadingIcon(
                    icon="high-definition-box"
                ),
                MDChipText(
                    text="720"
                ),
                type="filter",
                on_release=lambda x: self.onFormatPreferenceChipRelease("resolution")
            )
        )
        self.formatPreferenceChipButtonContainer.add_widget(
            MDChip(
                MDChipLeadingIcon(
                    icon="file-music-outline"
                ),
                MDChipText(
                    text="Audio format"
                ),
                type="filter",
                on_release=lambda x: self.onFormatPreferenceChipRelease("audio")
            )
        )

        self.formatPreferenceVBox.add_widget(
            MDLabel(
                text="Format preference",
                size_hint=(1, None),
                height=30
            )
        )
        self.formatPreferenceVBox.add_widget(
            self.formatPreferenceChipButtonContainer
        )

        self.bottomBarContainer = MDDialogButtonContainer(
            Widget(
                size_hint=(1, None),
                height=0
            ),
            MDButton(
                MDButtonIcon(
                    icon="cancel"
                ),
                MDButtonText(
                    text="Cancel"
                ),
                style="outlined",
                on_release=lambda x: self.dismiss()
            ),
            MDButton(
                MDButtonIcon(
                    icon="check-underline"
                ),
                MDButtonText(
                    text="Download"
                ),
                style="filled"
            ),
            spacing="8dp"
        )

        self.container.add_widget(self.fileNameFieldVBox)
        self.container.add_widget(self.downloadTyeVBox)
        self.container.add_widget(self.formatPreferenceVBox)
        self.container.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        self.container.add_widget(self.bottomBarContainer)

        self.add_widget(
            MDDialogHeadlineText(
                text="Configure download"
            )
        )
        self.add_widget(self.container)

        self.selectVideoFormatDialogue = SelectVideoQualityDialogue()
        self.selectVideoFormatDialogue.bind(
            on_confirm=lambda selectVideoFormatDialogue, videoFormat:
                self.onVideoFormatConfirmed(selectVideoFormatDialogue, videoFormat)
        )

        self.selectAudioFormatDialogue = SelectAudioFormatDialogue()
        self.selectAudioFormatDialogue.bind(
            on_confirm=lambda selectAudioFormatDialogue, audioFormat:
                self.onAudioFormatConfirmed(selectAudioFormatDialogue, audioFormat)
        )

    def onDownloadTypeSelect(self, downloadType):
        print("onDownloadTypeSelect: ", downloadType)

    def onFormatPreferenceChipRelease(self, formatPreferenceButtonName):

        if formatPreferenceButtonName == "resolution":
            self.selectVideoFormatDialogue.open()
        elif formatPreferenceButtonName == "audio":
            self.selectAudioFormatDialogue.open()
        else:
            pass

        print(formatPreferenceButtonName)

    def onVideoFormatConfirmed(self, selectVideoFormatDialogue, videoFormat):
        self.selectedOptions["videoFormat"] = videoFormat
        selectVideoFormatDialogue.dismiss()
        print(self.selectedOptions)

    def onAudioFormatConfirmed(self, selectAudioFormatDialogue, audioFormat):
        self.selectedOptions["audioFormat"] = audioFormat
        selectAudioFormatDialogue.dismiss()
        print(self.selectedOptions)
