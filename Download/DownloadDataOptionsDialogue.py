
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

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    ListProperty
)

from .DownloadData import DownloadData
from .DownloadDataVideoFormatDialogue import DownloadDataVideoFormatDialogue
from .DownloadDataAudioFormatDialogue import DownloadDataAudioFormatDialogue

class DownloadDataOptionsDialogue(MDDialog):

    downloadData: DownloadData = ObjectProperty(DownloadData())

    container: MDDialogContentContainer
    fileNameFieldVBox: MDBoxLayout
    downloadTypeVBox: MDBoxLayout
    videoDownloadTypeChip: MDSegmentedButtonItem
    audioDownloadTypeChip: MDSegmentedButtonItem
    formatVBox: MDBoxLayout
    formatChipButtonContainer: MDBoxLayout
    videoFormatChipButtonContainer: MDBoxLayout
    videoFormatChipButton: MDChip
    audioFormatChipButton: MDChip
    bottomBarContainer: MDDialogButtonContainer

    _videoFormatChipButtonDefaultSizeHintx: float
    _videoFormatChipButtonDefaultSizeHinty: float

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.container = MDDialogContentContainer(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(12)
        )

        self.fileNameFieldVBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=dp(12),
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
                text=self.downloadData.fileName,
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

        self.videoDownloadTypeChip = MDSegmentedButtonItem(
            MDSegmentButtonIcon(
                icon="file-video-outline"
            ),
            MDSegmentButtonLabel(
                text="Video"
            ),
            on_release=lambda dt: self._onVideoDownloadTypeChipRelease()
        )

        self.audioDownloadTypeChip = MDSegmentedButtonItem(
            MDSegmentButtonIcon(icon="file-music-outline"),
            MDSegmentButtonLabel(text="Audio"),
            on_release=lambda dt: self._onAudioDownloadTypeChipRelease()
        )

        self.downloadTypeVBox.add_widget(
            MDSegmentedButton(
                self.videoDownloadTypeChip,
                self.audioDownloadTypeChip
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
            on_release=lambda dt: self._onVideoFormatChipRelease()
        )

        self._videoFormatChipButtonDefaultSizeHintx = self.videoFormatChipButton.size_hint_x
        self._videoFormatChipButtonDefaultSizeHinty = self.videoFormatChipButton.size_hint_y

        self.audioFormatChipButton = MDChip(
            MDChipLeadingIcon(icon="file-music-outline"),
            MDChipText(text="Audio format"),
            type="filter",
            on_release=lambda dt: self._onAudioFormatChipRelease()
        )

        self.formatChipButtonContainer.add_widget(self.videoFormatChipButton)
        self.formatChipButtonContainer.add_widget(self.audioFormatChipButton)

        self.formatVBox.add_widget(
            MDLabel(
                text="Format preference",
                size_hint=(1, None),
                height=dp(30)
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
                on_release=lambda dt: self.dismiss()
            ),
            MDButton(
                MDButtonIcon(
                    icon="check-underline"
                ),
                MDButtonText(
                    text="Download"
                ),
                style="filled",
                on_release=lambda dt: self._on_download_options_confirmed()
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

        self.bind(
            downloadData=lambda instance, value: self._onDownloadData(instance, value)
        )

        self._onDownloadData(self, self.downloadData)

        self.register_event_type("on_download_options_confirmed")

    def _onDownloadData(self, instance, value)-> None:

        downloadData = value

        self.downloadDataVideoFormatDialogue = DownloadDataVideoFormatDialogue(
            downloadData=downloadData
        )

        self.downloadDataAudioFormatDialogue = DownloadDataAudioFormatDialogue(
            downloadData=downloadData
        )

        downloadData.bind(
            downloadType=lambda instance, value: self._onDownloadDownloadType(instance, value)
        )

        self.downloadDataVideoFormatDialogue.bind(
            on_confirm=lambda instance, value:
                self._onVideoFormatConfirmed(instance, value)
        )

        self.downloadDataAudioFormatDialogue.bind(
            on_confirm=lambda instance, value:
                self._onAudioFormatConfirmed(instance, value)
        )

        self._onDownloadDownloadType(self, downloadData.downloadType)

    def _onDownloadDownloadType(self, instance, value)-> None:
        downloadType = value
        if downloadType == "video":
            self.videoDownloadTypeChip.active = True
            self.audioDownloadTypeChip.active = False
            self._showVideoFormatChipButton()
        elif downloadType == "audio":
            self.videoDownloadTypeChip.active = False
            self.audioDownloadTypeChip.active = True
            self._hideVideoFormatChipButton()

    def _onVideoDownloadTypeChipRelease(self)-> None:
        self.downloadData.downloadType = "video"

    def _onAudioDownloadTypeChipRelease(self)-> None:
        self.downloadData.downloadType = "audio"

    def _onVideoFormatChipRelease(self)-> None:
        self.downloadDataVideoFormatDialogue.open()

    def _onAudioFormatChipRelease(self) -> None:
        self.downloadDataAudioFormatDialogue.open()

    def _onVideoFormatConfirmed(
        self,
        instance,
        value
    ) -> None:
        downloadDataVideoFormatDialogue = instance
        videoFormat = value
        downloadDataVideoFormatDialogue.dismiss()

    def _onAudioFormatConfirmed(
        self,
        instance,
        value
    ) -> None:
        downloadDataAudioFormatDialogue = instance
        audioFormat = value
        downloadDataAudioFormatDialogue.dismiss()

    def _on_download_options_confirmed(self) -> None:
        self.dispatch(
            "on_download_options_confirmed",
            self.downloadData
        )
        self.dismiss()

    def on_download_options_confirmed(self, downloadData: DownloadData) -> None:
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _showVideoFormatChipButton(self) -> None:
        self.videoFormatChipButton.size_hint_x = self._videoFormatChipButtonDefaultSizeHintx
        self.videoFormatChipButton.width = self.videoFormatChipButton.minimum_width
        self.videoFormatChipButton.opacity = 1
        self.videoFormatChipButton.disabled = False

    def _hideVideoFormatChipButton(self) -> None:
        self.videoFormatChipButton.size_hint_x = None
        self.videoFormatChipButton.width = 0
        self.videoFormatChipButton.opacity = 0
        self.videoFormatChipButton.disabled = True
