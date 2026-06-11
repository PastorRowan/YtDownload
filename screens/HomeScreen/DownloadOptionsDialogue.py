
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

from screens.HomeScreen.SelectVideoFormatDialogue import SelectVideoFormatDialogue

from screens.HomeScreen.SelectAudioFormatDialogue import SelectAudioFormatDialogue

from kivy.clock import Clock

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

        self.downloadTypeVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )

        self.downloadTypeVBox.add_widget(
            MDLabel(
                text="Download type",
                size_hint=(1, None),
                height=30
            )
        )

        self.downloadTypeVBox.add_widget(
            MDSegmentedButton(
                MDSegmentedButtonItem(
                    MDSegmentButtonIcon(
                        icon="file-video-outline"
                    ),
                    MDSegmentButtonLabel(
                        text="Video"
                    ),
                    on_release=lambda x: self._onDownloadTypeSelect("video")
                ),
                MDSegmentedButtonItem(
                    MDSegmentButtonIcon(
                        icon="file-music-outline"
                    ),
                    MDSegmentButtonLabel(
                        text="Audio"
                    ),
                    on_release=lambda x: self._onDownloadTypeSelect("audio")
                )
            )
        )

        self.formatVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing="12dp",
            adaptive_height=True
        )

        self.formatChipButtonContainer = MDBoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            adaptive_height=True
        )

        self.videoFormatChipButtonContainer = MDBoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            adaptive_height=True
        )

        self.videoFormatChipButton = MDChip( 
            MDChipLeadingIcon(icon="file-video-outline"),
            MDChipText(text="Video format"),
            type="filter",
            on_release=lambda x: self._onFormatChipRelease("video")
        )

        self._videoFormatChipButtonDefaultSizeHintx = self.videoFormatChipButton.size_hint_x
        self._videoFormatChipButtonDefaultSizeHinty = self.videoFormatChipButton.size_hint_y

        # self.videoFormatChipButtonContainer.add_widget(self.videoFormatChipButton)

        self.audioFormatChipButton = MDChip(
            MDChipLeadingIcon(icon="file-music-outline"),
            MDChipText(text="Audio format"),
            type="filter",
            on_release=lambda x: self._onFormatChipRelease("audio")
        )

        self.formatChipButtonContainer.add_widget(self.videoFormatChipButton)
        self.formatChipButtonContainer.add_widget(self.audioFormatChipButton)

        self.formatVBox.add_widget(
            MDLabel(
                text="Format preference",
                size_hint=(1, None),
                height=30
            )
        )
        self.formatVBox.add_widget(self.formatChipButtonContainer)

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
        self.container.add_widget(self.downloadTypeVBox)
        self.container.add_widget(self.formatVBox)
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

        self.selectVideoFormatDialogue = SelectVideoFormatDialogue()
        self.selectVideoFormatDialogue.bind(
            on_confirm=lambda selectVideoFormatDialogue, videoFormat:
                self._onVideoFormatConfirmed(selectVideoFormatDialogue, videoFormat)
        )

        self.selectAudioFormatDialogue = SelectAudioFormatDialogue()
        self.selectAudioFormatDialogue.bind(
            on_confirm=lambda selectAudioFormatDialogue, audioFormat:
                self._onAudioFormatConfirmed(selectAudioFormatDialogue, audioFormat)
        )

    def showVideoFormatChipButton(self):
        self.videoFormatChipButton.size_hint_x = self._videoFormatChipButtonDefaultSizeHintx
        self.videoFormatChipButton.width = self.videoFormatChipButton.minimum_width
        self.videoFormatChipButton.opacity = 1
        self.videoFormatChipButton.disabled = False

    def hideVideoFormatChipButton(self):
        self.videoFormatChipButton.size_hint_x = None
        self.videoFormatChipButton.width = 0
        self.videoFormatChipButton.opacity = 0
        self.videoFormatChipButton.disabled = True

    def _onDownloadTypeSelect(self, downloadType):
        print("_onDownloadTypeSelect: ", downloadType)

        if downloadType == "video":
            Clock.schedule_once(lambda dt: self.showVideoFormatChipButton())
        elif downloadType == "audio":
            Clock.schedule_once(lambda dt: self.hideVideoFormatChipButton())

    def _onFormatChipRelease(self, formatPreferenceButtonName):

        if formatPreferenceButtonName == "video":
            self.selectVideoFormatDialogue.open()
        elif formatPreferenceButtonName == "audio":
            self.selectAudioFormatDialogue.open()
        else:
            pass

        print(formatPreferenceButtonName)

    def _onVideoFormatConfirmed(self, selectVideoFormatDialogue, videoFormat):
        self.selectedOptions["videoFormat"] = videoFormat
        selectVideoFormatDialogue.dismiss()
        print(self.selectedOptions)

    def _onAudioFormatConfirmed(self, selectAudioFormatDialogue, audioFormat):
        self.selectedOptions["audioFormat"] = audioFormat
        selectAudioFormatDialogue.dismiss()
        print(self.selectedOptions)
