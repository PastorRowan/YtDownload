
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

from kivymd.uix.list import (
    MDListItem,
    MDListItemSupportingText,
    MDListItemLeadingIcon,
    MDListItemTrailingIcon
)

from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock

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
            MDListItemTrailingIcon(
                icon="file-music-outline"
            ),
            size_hint=(1, None),
            on_release=lambda *_: self.onAudioFileFormatDropDownMenuButtonRelease()
        )

        self.audioFileFormatDropDownMenuItems = [
            self.makeDropDownMenuItem("fileFormat", "OPUS"),
            self.makeDropDownMenuItem("fileFormat", "M4A")
        ]

        self.audioFileFormatDropDownMenu = MDDropdownMenu(
            caller=self.audioFileFormatDropDownMenuButton, # the widget that opens it
            items=self.audioFileFormatDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.audioQualityDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="high-definition-box"
            ),
            MDListItemSupportingText(
                text="192 Kbps",
            ),
            MDListItemTrailingIcon(
                icon="high-definition-box"
            ),
            size_hint=(1, None),
            on_release=lambda *_: self.onAudioQualityDropDownMenuButtonRelease()
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
            position="bottom",
            hor_growth="right",
            ver_growth="down"
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

        self.add_widget(

            MDDialogContentContainer(
            
                MDLabel(text="Audio file format"),
                self.audioFileFormatDropDownMenuButton,

                MDLabel(text="Audio quality"),
                self.audioQualityDropDownMenuButton,

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
                ),

                orientation="vertical",
                spacing="12dp",
                padding="12dp",
                size_hint=(1, None)

            )

        )

    def setAudioFormat(self, key, value):
        self.audioFormat[key] = value
        print(self.audioFormat)

    def makeDropDownMenuItem(self, key, value):
        return {
            "text": value,
            "on_release": lambda *_: self.setAudioFormat(key, value)
        }

    def onAudioFileFormatDropDownMenuButtonRelease(self):

        menu = self.audioFileFormatDropDownMenu
        caller = self.audioFileFormatDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

    def onAudioQualityDropDownMenuButtonRelease(self):

        menu = self.audioQualityDropDownMenu
        caller = self.audioQualityDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

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
