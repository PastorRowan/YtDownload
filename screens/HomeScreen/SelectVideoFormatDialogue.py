
from typing import (
    TypedDict,
    Optional,
    List,
    Union,
    Dict,
    Any,
    Literal,
    Set,
    Callable,
    Any
)

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

class DropDownMenuItem(TypedDict):
    text: str
    on_release: Callable[[], None]

class SelectVideoFormatDialogue(MDDialog):

    videoExts: list[str] = ListProperty([])
    selectedVideoExt: str = StringProperty("-")
    _videoExtDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    videoHeights: list[str] = ListProperty([])
    selectedVideoHeight: str = StringProperty("-")
    _videoHeightDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedVideoExt
        )
        self.bind(
            selectedVideoExt=lambda instance, value: setattr(
                self.videoExtDropDownMenuButtonText,
                "text",
                value
            )
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

        self.videoExtDropDownMenu = MDDropdownMenu(
            caller=self.videoExtDropDownMenuButton, # the widget that opens it
            items=self._videoExtDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.videoHeightDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedVideoHeight
        )
        self.bind(
            selectedVideoHeight=lambda instance, value: setattr(
                self.videoHeightDropDownMenuButtonText,
                "text",
                value + "p"
            )
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

        self.videoHeightDropDownMenu = MDDropdownMenu(
            caller=self.videoHeightDropDownMenuButton, # the widget that opens it
            items=self._videoHeightDropDownMenuItems,
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

        self.bind(
            videoExts=lambda instance, value: self._onVideoExts(instance, value)
        )

        self.bind(
            videoHeights=lambda instance, value: self._onVideoHeights(instance, value)
        )

    def _onVideoExts(self, instance, value):

        videoExtDropDownMenu = self.videoExtDropDownMenu

        self._videoExtDropDownMenuItems.clear()

        def _selectVideoExt(videoExt: str) -> None:
            self.selectedVideoExt = videoExt
            videoExtDropDownMenu.dismiss()

        for videoExt in self.videoExts:
            self._videoExtDropDownMenuItems.append({
                "text": videoExt,
                "on_release": lambda x=videoExt: _selectVideoExt(x)
            })

    def _onVideoHeights(self, instance, value):

        videoHeightDropDownMenu = self.videoHeightDropDownMenu

        self._videoHeightDropDownMenuItems.clear()

        def _selectVideoHeight(videoHeight: str) -> None:
            self.selectedVideoHeight = videoHeight
            videoHeightDropDownMenu.dismiss()

        for videoHeight in self.videoHeights:
            self._videoHeightDropDownMenuItems.append({
                "text": videoHeight + "p",
                "on_release": lambda x=videoHeight: _selectVideoHeight(x)
            })

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
