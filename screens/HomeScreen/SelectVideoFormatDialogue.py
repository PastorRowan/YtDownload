
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
from kivy.properties import (
    StringProperty,
    ListProperty
)

class SelectVideoFormatDialogue(MDDialog):

    videoExts = ListProperty([])
    selectedVideoExt = StringProperty("")

    videoHeights = ListProperty([])
    selectedVideoHeight = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedVideoExt
        )

        self.videoExtDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="file-video-outline"
            ),
            self.videoExtDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="file-video-outline"
            ),
            size_hint=(1, None),
            on_release=lambda dt: self._onVideoExtDropDownMenuButtonRelease()
        )

        self.videoExtDropDownMenuItems = []

        def _selectVideoExt(videoExt):
            self.selectedVideoExt = videoExt

        for videoExt in self.videoExts:
            self.videoExtDropDownMenuItems.append({
                "text": videoExt,
                "on_release": lambda dt: _selectVideoExt(videoExt)
            })

        self.videoExtDropDownMenu = MDDropdownMenu(
            caller=self.videoExtDropDownMenuButton, # the widget that opens it
            items=self.videoExtDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.videoHeightDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedVideoHeight
        )

        self.videoHeightDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="high-definition-box"
            ),
            self.videoHeightDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="high-definition-box"
            ),
            size_hint=(1, None),
            on_release=lambda dt: self._onVideoHeightDropDownMenuButtonRelease()
        )


        self.videoHeightDropDownMenuItems = []

        def _selectVideoHeight(videoHeight):
            self.selectedVideoHeight = videoHeight

        for videoHeight in self.videoHeights:
            self.videoHeightDropDownMenuItems.append({
                "text": videoHeight,
                "on_release": lambda dt: _selectVideoHeight(videoHeight)
            })

        self.videoHeightDropDownMenu = MDDropdownMenu(
            caller=self.videoHeightDropDownMenuButton, # the widget that opens it
            items=self.videoHeightDropDownMenuItems,
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
            
                MDLabel(text="Video extension"),
                self.videoExtDropDownMenuButton,

                MDLabel(text="Video height"),
                self.videoHeightDropDownMenuButton,

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

        self.register_event_type("on_confirm")

    def _onVideoExtDropDownMenuButtonRelease(self):

        menu = self.videoExtDropDownMenu
        caller = self.videoExtDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

    def _onVideoHeightDropDownMenuButtonRelease(self):

        menu = self.videoHeightDropDownMenu
        caller = self.videoHeightDropDownMenuButton

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
            {
                "ext": self.selectedVideoExt,
                "height": self.selectedVideoHeight
            }
        )
