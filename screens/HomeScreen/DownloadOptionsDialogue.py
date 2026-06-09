
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

class DownloadOptionsDialogue(MDDialog):

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

        self.formatPreferenceHBox = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            spacing="12dp"
        )
        self.formatPreferenceHBox.add_widget(
            MDChip( 
                MDChipLeadingIcon(
                    icon="high-definition-box"
                ),
                MDChipText(
                    text="720"
                ),
                type="filter"
            )
        )
        self.formatPreferenceHBox.add_widget(
            MDChip(
                MDChipLeadingIcon(
                    icon="file-music-outline"
                ),
                MDChipText(
                    text="Audio format"
                ),
                type="filter"
            )
        )

        """
        
        """

        self.bottomBarContainer = MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonIcon(
                    icon="cancel"
                ),
                MDButtonText(
                    text="Cancel"
                ),
                style="outlined"
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

        self.container.add_widget(
            MDLabel(
                text="File name",
                size_hint=(1, None),
                height=30
            )
        )
        self.container.add_widget(
            MDTextField(
                size_hint=(1, None),
                text="",
                hint_text="File Name",
                multiline=False
            )
        )
        self.container.add_widget(
            MDLabel(
                text="Download type",
                size_hint=(1, None),
                height=30
            )
        )
        self.container.add_widget(
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

        self.container.add_widget(
            MDLabel(
                text="Format preference",
                size_hint=(1, None),
                height=30
            )
        )

        self.container.add_widget(self.formatPreferenceHBox)

        self.container.add_widget(self.bottomBarContainer)

        self.add_widget(
            MDDialogHeadlineText(
                text="Configure download"
            )
        )
        self.add_widget(self.container)

    def onDownloadTypeSelect(self, downloadType):
        print("onDownloadTypeSelect: ", downloadType)
