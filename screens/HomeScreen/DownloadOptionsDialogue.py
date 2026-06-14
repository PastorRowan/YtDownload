
from typing import (
    TypedDict,
    Optional,
    List,
    Union,
    Dict,
    Any,
    Literal,
    Set
)

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
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    ListProperty
)

from screens.HomeScreen.SelectVideoFormatDialogue import SelectVideoFormatDialogue

from screens.HomeScreen.SelectAudioFormatDialogue import SelectAudioFormatDialogue

from DownloadQueue import (
    DownloadJob,
    DownloadQueue
)

import config

class VideoFormat(TypedDict):
    ext: str
    height: int

class AudioFormat(TypedDict):
    ext: str
    abr: int

class SelectedFormats(TypedDict):
    selectedVideoFormat: VideoFormat
    selectedAudioFormat: AudioFormat

DEFAULT_FILENAME = "Default"

class DownloadOptionsDialogue(MDDialog):

    url: str = StringProperty("")

    fileName: str = StringProperty(DEFAULT_FILENAME)
    downloadType = StringProperty(config.DEFAULT_DOWNLOAD_TYPE, options=config.ALLOWED_DOWNLOAD_TYPES)

    availableVideoExts: list[str] = ListProperty(config.ALLOWED_VIDEO_EXTS)
    selectedVideoExt: str = StringProperty(config.DEFAULT_VIDEO_EXT, options=config.ALLOWED_VIDEO_EXTS)

    availableVideoHeights: list[str] = ListProperty(config.ALLOWED_VIDEO_HEIGHTS)
    selectedVideoHeight: str = StringProperty(config.DEFAULT_VIDEO_HEIGHT, options=config.ALLOWED_VIDEO_HEIGHTS)

    availableAudioExts: list[str] = ListProperty(config.ALLOWED_AUDIO_EXTS)
    selectedAudioExt: str = StringProperty(config.DEFAULT_AUDIO_EXT, options=config.ALLOWED_AUDIO_EXTS)

    availableAbrs: list[str] = ListProperty(config.ALLOWED_ABRS)
    selectedAudioAbr: str = StringProperty(config.DEFAULT_ABR, options=config.ALLOWED_ABRS)

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

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
                text=self.fileName,
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
                    on_release=lambda dt: self._onVideoDownloadTypeChipRelease()
                ),
                MDSegmentedButtonItem(
                    MDSegmentButtonIcon(
                        icon="file-music-outline"
                    ),
                    MDSegmentButtonLabel(
                        text="Audio"
                    ),
                    on_release=lambda dt: self._onAudioDownloadTypeChipRelease()
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

        self.selectVideoFormatDialogue = SelectVideoFormatDialogue(

            videoExts=self.availableVideoExts,
            selectedVideoExt=self.selectedVideoExt,

            videoHeights=self.availableVideoHeights,
            selectedVideoHeight=self.selectedVideoHeight

        )
        self.selectVideoFormatDialogue.bind(
            on_confirm=lambda selectVideoFormatDialogue, videoFormat:
                self._onVideoFormatConfirmed(selectVideoFormatDialogue)
        )

        self.selectAudioFormatDialogue = SelectAudioFormatDialogue(

            audioExts=self.availableAudioExts,
            selectedAudioExt=self.selectedAudioExt,

            audioAbrs=self.availableAbrs,
            selectedAudioAbr=self.selectedAudioAbr

        )
        self.selectAudioFormatDialogue.bind(
            on_confirm=lambda selectAudioFormatDialogue, audioFormat:
                self._onAudioFormatConfirmed(selectAudioFormatDialogue)
        )

        self.bind(
            downloadType=self._onDownloadType
        )

    def _showVideoFormatChipButton(self):
        self.videoFormatChipButton.size_hint_x = self._videoFormatChipButtonDefaultSizeHintx
        self.videoFormatChipButton.width = self.videoFormatChipButton.minimum_width
        self.videoFormatChipButton.opacity = 1
        self.videoFormatChipButton.disabled = False

    def _hideVideoFormatChipButton(self):
        self.videoFormatChipButton.size_hint_x = None
        self.videoFormatChipButton.width = 0
        self.videoFormatChipButton.opacity = 0
        self.videoFormatChipButton.disabled = True

    def _onDownloadType(self, instance, value):
        if value == "video":
            self._showVideoFormatChipButton()
        elif value == "audio":
            self._hideVideoFormatChipButton()
        else:
            raise ValueError(f"value '{value}' is invalid")

    def _onVideoDownloadTypeChipRelease(self):
        print("_onVideoDownloadTypeChipRelease")
        print(self.availableVideoExts)
        print(self.availableVideoHeights)
        print(self.availableAudioExts)
        print(self.availableAbrs)
        self.downloadType = "video"

    def _onAudioDownloadTypeChipRelease(self):
        self.downloadType = "audio"

    def _onVideoFormatChipRelease(self):
        self.selectVideoFormatDialogue.open()

    def _onAudioFormatChipRelease(self):
        self.selectAudioFormatDialogue.open()

    def _onVideoFormatConfirmed(
        self,
        selectVideoFormatDialogue,
    ):
        selectVideoFormatDialogue.dismiss()

    def _onAudioFormatConfirmed(
        self,
        selectAudioFormatDialogue,
    ):
        selectAudioFormatDialogue.dismiss()

    def _on_download_options_confirmed(self):
        print("_onDownloadOptionsConfirmed: created download job and added it to download queue")

        jobFileName = None

        if self.fileName != DEFAULT_FILENAME:
            jobFileName =self.fileName

        newJob = DownloadJob(

            url=self.url,

            fileName=jobFileName,
            downloadType=self.downloadType,

            videoExt=self.selectedVideoExt,
            videoHeight=self.selectedVideoHeight,

            audioExt=self.selectedAudioExt,
            abr=self.selectedAudioAbr

        )

        DownloadQueue.addDownloadJob(newJob)
