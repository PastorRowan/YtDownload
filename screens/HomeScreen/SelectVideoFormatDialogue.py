
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

class SelectVideoFormatDialogue(MDDialog):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoFormat = {
            "fileFormat": "MP4",
            "quality": "720p"
        }

        self.videoFileFormatDropDownMenuButtonText = MDListItemSupportingText(
            text=self.videoFormat["fileFormat"]
        )

        self.videoFileFormatDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="file-video-outline"
            ),
            self.videoFileFormatDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="file-video-outline"
            ),
            size_hint=(1, None),
            on_release=lambda *_: self._onVideoFileFormatDropDownMenuButtonRelease()
        )

        self.videoFileFormatDropDownMenuItems = [
            self._makeDropDownMenuItem("fileFormat", "MP4"),
            self._makeDropDownMenuItem("fileFormat", "WEBM")
        ]

        self.videoFileFormatDropDownMenu = MDDropdownMenu(
            caller=self.videoFileFormatDropDownMenuButton, # the widget that opens it
            items=self.videoFileFormatDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.videoQualityDropDownMenuButtonText = MDListItemSupportingText(
            text=self.videoFormat["quality"]
        )

        self.videoQualityDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="high-definition-box"
            ),
            self.videoQualityDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="high-definition-box"
            ),
            size_hint=(1, None),
            on_release=lambda *_: self._onVideoQualityDropDownMenuButtonRelease()
        )

        self.videoQualityDropDownMenuItems = [
            self._makeDropDownMenuItem("quality", "Best quality"),
            self._makeDropDownMenuItem("quality", "2160p"),
            self._makeDropDownMenuItem("quality", "1440p"),
            self._makeDropDownMenuItem("quality", "1080p"),
            self._makeDropDownMenuItem("quality", "720p"),
            self._makeDropDownMenuItem("quality", "480p"),
            self._makeDropDownMenuItem("quality", "360p"),
            self._makeDropDownMenuItem("quality", "Lowest quality")
        ]

        self.videoQualityDropDownMenu = MDDropdownMenu(
            caller=self.videoQualityDropDownMenuButton, # the widget that opens it
            items=self.videoQualityDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.add_widget(
            MDDialogIcon(
                icon="file-video-outline"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Video format"
            )
        )

        self.add_widget(

            MDDialogContentContainer(
            
                MDLabel(text="Video file format"),
                self.videoFileFormatDropDownMenuButton,

                MDLabel(text="Video quality"),
                self.videoQualityDropDownMenuButton,

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

        self.register_event_type("on_confirm")

    def setVideoFormat(self, key, value):
        self.videoFormat[key] = value
        print(self.videoFormat)

    def selectItem(self, key, value):

        self.setVideoFormat(key, value)

        if key == "fileFormat":
            self.videoFileFormatDropDownMenuButtonText.text = value
            self.videoFileFormatDropDownMenu.dismiss()
        elif key == "quality":
            self.videoQualityDropDownMenuButtonText.text = value
            self.videoQualityDropDownMenu.dismiss()
        else:
            raise Exception(f"Error: key '{key}' is invalid")

    def _makeDropDownMenuItem(self, key, value):
        return {
            "text": value,
            "divider": None,
            "divider_color": (1, 0, 0, 1),
            "on_release": lambda *_: self.selectItem(key, value)
        }

    def _onVideoFileFormatDropDownMenuButtonRelease(self):

        menu = self.videoFileFormatDropDownMenu
        caller = self.videoFileFormatDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

    def _onVideoQualityDropDownMenuButtonRelease(self):

        menu = self.videoQualityDropDownMenu
        caller = self.videoQualityDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

    def on_confirm(self):
        """
        Default handler required by Kivy.
        Override or bind to this event externally.
        """
        pass

    def _on_confirm(self):

        self.dispatch(
            "on_confirm",
            self.videoFormat
        )
