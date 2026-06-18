
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
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    ListProperty
)

from .Job import Job
from .Queue import Queue
from .JobVideoFormatDialogue import JobVideoFormatDialogue
from .JobAudioFormatDialogue import JobAudioFormatDialogue

class JobOptionsDialogue(MDDialog):

    job: Job = ObjectProperty(Job())

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
                text=self.job.fileName,
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
            job=lambda instance, value: self._onJob(instance, value)
        )

        self._onJob(self, self.job)

    def _onJob(self, instance, value):

        job = value

        self.jobVideoFormatDialogue = JobVideoFormatDialogue(
            job=job
        )

        self.jobAudioFormatDialogue = JobAudioFormatDialogue(
            job=job
        )

        job.bind(
            downloadType=lambda instance, value: self._onJobDownloadType(instance, value)
        )

        self.jobVideoFormatDialogue.bind(
            on_confirm=lambda jobVideoFormatDialogue, videoFormat:
                self._onVideoFormatConfirmed(jobVideoFormatDialogue, videoFormat)
        )

        self.jobAudioFormatDialogue.bind(
            on_confirm=lambda jobAudioFormatDialogue, audioFormat:
                self._onAudioFormatConfirmed(jobAudioFormatDialogue, audioFormat)
        )

        self._onJobDownloadType(self, job.downloadType)

    def _onJobDownloadType(self, instance, value):
        downloadType = value
        print("new downloadType: ", downloadType)
        if downloadType == "video":
            self.videoDownloadTypeChip.active = True
            self.audioDownloadTypeChip.active = False
            self._showVideoFormatChipButton()
        elif downloadType == "audio":
            self.videoDownloadTypeChip.active = False
            self.audioDownloadTypeChip.active = True
            self._hideVideoFormatChipButton()

    def _onVideoDownloadTypeChipRelease(self):
        print("_onVideoDownloadTypeChipRelease")
        self.job.downloadType = "video"

    def _onAudioDownloadTypeChipRelease(self):
        print("_onAudioDownloadTypeChipRelease")
        self.job.downloadType = "audio"

    def _onVideoFormatChipRelease(self):
        self.jobVideoFormatDialogue.open()

    def _onAudioFormatChipRelease(self):
        self.jobAudioFormatDialogue.open()

    def _onVideoFormatConfirmed(
        self,
        jobVideoFormatDialogue,
        videoFormat
    ):
        jobVideoFormatDialogue.dismiss()

    def _onAudioFormatConfirmed(
        self,
        jobAudioFormatDialogue,
        audioFormat
    ):
        jobAudioFormatDialogue.dismiss()

    def _on_download_options_confirmed(self):
        print("_onDownloadOptionsConfirmed: created download job and added it to download queue")

        Queue.addJob(self.job)

        self.dismiss()

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
