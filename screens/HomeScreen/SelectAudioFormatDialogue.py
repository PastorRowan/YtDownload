
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
    MDDialogSupportingText,
    MDDialogIcon
)
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDButton,
    MDButtonText,
    MDButtonIcon,
    MDFabButton,
    MDExtendedFabButtonIcon,
    MDExtendedFabButtonText
)

from kivymd.uix.list import (
    MDListItem, MDListItemSupportingText, MDListItemLeadingIcon
)

from kivymd.uix.menu import MDDropdownMenu

class SelectAudioFormatDialogue(MDDialog):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioFormat = {
            "fileFormat": "OPUS",
            "quality": "192 Kbps"
        }

        self.register_event_type("on_confirm")

        self.audioFileFormatDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="file-music-outline"
            ),
            MDListItemSupportingText(
                text="OPUS"
            ),
            #style="outlined",
            #size_hint=(None, None),
            width=1200,
            height=600,
            md_bg_color=(0, 1, 0, 1),
            size_hint_min_x=1,
            size_hint_min_y=1,
            on_release=lambda *_: self.audioFileFormatDropDownMenu.open(),
        )

        self.audioFileFormatDropDownMenuItems = [
            self.makeDropDownMenuItem("fileFormat", "OPUS"),
            self.makeDropDownMenuItem("fileFormat", "M4A")
        ]

        self.audioFileFormatDropDownMenu = MDDropdownMenu(
            caller=self.audioFileFormatDropDownMenuButton, # the widget that opens it
            items=self.audioFileFormatDropDownMenuItems,
            width_mult=4
        )

        self.audioQualityDropDownMenuButton = MDButton(
            MDButtonIcon(
                icon="high-definition-box"
            ),
            MDButtonText(
                text="192 Kbps",
                size_hint=(1, None)
            ),
            MDButtonIcon(
                icon="high-definition-box"
            ),
            style="outlined",
            size_hint=(1, None),
            pos_hint={"center_x": 0.5},
            on_release=lambda *_: self.audioQualityDropDownMenu.open()
        )

        self.audioQualityDropDownMenuItems = [
            self.makeDropDownMenuItem("quality", "Unlimited"),
            self.makeDropDownMenuItem("quality", "192 Kbps"),
            self.makeDropDownMenuItem("quality", "128 Kbps"),
            self.makeDropDownMenuItem("quality", "64 Kbps"),
            self.makeDropDownMenuItem("quality", "32 Kbps"),
        ]

        self.audioQualityDropDownMenu = MDDropdownMenu(
            caller=self.audioQualityDropDownMenuButton, # the widget that opens it
            items=self.audioQualityDropDownMenuItems,
            width_mult=4
        )

        self.add_widget(
            MDDialogIcon(
                icon="file-music-outline"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Audio format"
            )
        )

        content = MDDialogContentContainer(
            orientation="vertical",
            spacing="12dp",
            padding="12dp",
            size_hint=(1, None)
        )

        content.add_widget(
            MDLabel(
                text="Audio file format"
            )
        )

        content.add_widget(
            self.audioFileFormatDropDownMenuButton
        )

        content.add_widget(
            MDLabel(
                text="Audio quality"
            )
        )
        content.add_widget(
            MDDialogButtonContainer(
                self.audioQualityDropDownMenuButton,
                orientation="horizontal",
                size_hint=(1, None),
                # adaptive_height=True
            )
        )

        content.add_widget(
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
                    on_release=lambda x: self.dismiss()
                ),
                MDButton(
                    MDButtonText(
                        text="Confirm"
                    ),
                    style="text",
                    on_release=lambda x: self._on_confirm()
                ),
                spacing="8dp"
            )
        )

        self.add_widget(content)

        self.audioFileFormatDropDownMenuButton.width = 600

    def setAudioFormat(self, key, value):
        self.audioFormat[key] = value
        print(self.audioFormat)

    def makeDropDownMenuItem(self, key, value):
        return {
            "text": value,
            "on_release": lambda *_: self.setAudioFormat(key, value)
        }

    def on_confirm(self, videoQuality):
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _on_confirm(self):

        self.dispatch(
            "on_confirm",
            self.audioFormat
        )
