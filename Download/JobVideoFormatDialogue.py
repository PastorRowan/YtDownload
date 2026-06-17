
from typing import (
    TypedDict,
    Callable
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
    NumericProperty,
    ObjectProperty,
    ListProperty
)

from .Job import Job

class DropDownMenuItem(TypedDict):
    text: str
    on_release: Callable[[], None]

class JobVideoFormatDialogue(MDDialog):

    job: Job = ObjectProperty(Job())

    selectedVideoExtIndex: int = NumericProperty(0)
    _videoExtDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    selectedVideoHeightIndex: int = NumericProperty(0)
    _videoHeightDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.videoExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.job.videoExts[self.selectedVideoExtIndex]
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
            text=f"{self.job.videoHeights[self.selectedVideoHeightIndex]}p"
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

        self.job.bind(
            videoExts=lambda instance, value: self._onJobVideoExts(instance, value),
            videoHeights=lambda instance, value: self._onJobVideoHeights(instance, value)
        )

        self.bind(
            selectedVideoExtIndex=lambda instance, value: self._onSelectedVideoExtIndex(instance, value),
            selectedVideoHeightIndex=lambda instance, value: self._onSelectedVideoHeightIndex(instance, value)
        )

        self._onJobVideoExts(self, self.job.videoExts)
        self._onJobVideoHeights(self, self.job.videoHeights)

        self._onSelectedVideoExtIndex(self, self.selectedVideoExtIndex)
        self._onSelectedVideoHeightIndex(self, self.selectedVideoHeightIndex)

        self.register_event_type("on_confirm")

    def _onJobVideoExts(self, instance, value):

        videoExtsDropDownMenu = self.videoExtDropDownMenu

        self._videoExtDropDownMenuItems.clear()

        def _selectVideoExtIndex(index: int) -> None:
            self.selectedVideoExtIndex = index
            videoExtsDropDownMenu.dismiss()

        for index, videoExt in enumerate(self.job.videoExts):
            self._videoExtDropDownMenuItems.append({
                "text": f"{videoExt}kbps",
                "on_release": lambda i=index: _selectVideoExtIndex(i)
            })

    def _onJobVideoHeights(self, instance, value):

        videoHeightsDropDownMenu = self.videoHeightDropDownMenu

        self._videoHeightDropDownMenuItems.clear()

        def _selectVideoHeightIndex(index: int) -> None:
            self.selectedVideoHeightIndex = index
            videoHeightsDropDownMenu.dismiss()

        for index, videoHeight in enumerate(self.job.videoHeights):
            self._videoHeightDropDownMenuItems.append({
                "text": f"{videoHeight}kbps",
                "on_release": lambda i=index: _selectVideoHeightIndex(i)
            })

    def _onSelectedVideoExtIndex(self, instance, value):
        videoExt = self.job.videoExts[value]
        self.videoExtDropDownMenuButtonText.text = videoExt

    def _onSelectedVideoHeightIndex(self, instance, value):
        videoHeight = self.job.videoExts[value]
        self.videoHeightDropDownMenuButtonText.text = videoHeight

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
