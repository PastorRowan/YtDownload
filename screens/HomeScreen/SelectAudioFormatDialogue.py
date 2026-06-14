
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
    NumericProperty,
    ObjectProperty,
    ListProperty
)

class DropDownMenuItem(TypedDict):
    text: str
    on_release: Callable[[], None]

class SelectAudioFormatDialogue(MDDialog):

    audioExts: list[str] = ListProperty([])
    selectedAudioExt: str = StringProperty("-")
    _audioExtDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    audioAbrs: list[str] = ListProperty([])
    selectedAudioAbr: str = StringProperty("-")
    _audioAbrDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedAudioExt
        )
        self.bind(
            selectedAudioExt=lambda instance, value: setattr(
                self.audioExtDropDownMenuButtonText,
                "text",
                value
            )
        )

        self.audioExtDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="file-audio-outline"
            ),
            self.audioExtDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="file-audio-outline"
            ),
            size_hint=(1, None),
            on_release=lambda dt: self._onAudioExtDropDownMenuButtonRelease()
        )

        self.audioExtDropDownMenu = MDDropdownMenu(
            caller=self.audioExtDropDownMenuButton, # the widget that opens it
            items=self._audioExtDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.audioAbrDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedAudioAbr
        )
        self.bind(
            selectedAudioAbr=lambda instance, value: setattr(
                self.audioAbrDropDownMenuButtonText,
                "text",
                value + "kbps"
            )
        )

        self.audioAbrDropDownMenuButton = MDListItem(
            MDListItemLeadingIcon(
                icon="high-definition-box"
            ),
            self.audioAbrDropDownMenuButtonText,
            MDListItemTrailingIcon(
                icon="high-definition-box"
            ),
            size_hint=(1, None),
            on_release=lambda dt: self._onAudioAbrDropDownMenuButtonRelease()
        )

        self.audioAbrDropDownMenu = MDDropdownMenu(
            caller=self.audioAbrDropDownMenuButton, # the widget that opens it
            items=self._audioAbrDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.add_widget(
            MDDialogIcon(
                icon="file-audio-outline"
            )
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Audio format"
            )
        )

        self.add_widget(

            MDDialogContentContainer(
            
                MDLabel(text="Audio extension"),
                self.audioExtDropDownMenuButton,

                MDLabel(text="Audio height"),
                self.audioAbrDropDownMenuButton,

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
            audioExts=lambda instance, value: self._onAudioExts()
        )

        self.bind(
            audioAbrs=lambda instance, value: self._onAudioAbrs()
        )

        self._onAudioExts()

        self._onAudioAbrs()

    def _onAudioExts(self):

        audioExtDropDownMenu = self.audioExtDropDownMenu

        self._audioExtDropDownMenuItems.clear()

        def _selectAudioExt(audioExt: str) -> None:
            self.selectedAudioExt = audioExt
            audioExtDropDownMenu.dismiss()

        for audioExt in self.audioExts:
            self._audioExtDropDownMenuItems.append({
                "text": audioExt,
                "on_release": lambda x=audioExt: _selectAudioExt(x)
            })

    def _onAudioAbrs(self):

        audioAbrDropDownMenu = self.audioAbrDropDownMenu

        self._audioAbrDropDownMenuItems.clear()

        def _selectAudioAbr(audioAbr: str) -> None:
            self.selectedAudioAbr = audioAbr
            audioAbrDropDownMenu.dismiss()

        for audioAbr in self.audioAbrs:
            self._audioAbrDropDownMenuItems.append({
                "text": audioAbr + "kbps",
                "on_release": lambda x=audioAbr: _selectAudioAbr(x)
            })

    def _onAudioExtDropDownMenuButtonRelease(self):

        menu = self.audioExtDropDownMenu
        caller = self.audioExtDropDownMenuButton

        def openMenu(*_):
            menu.open()
            menu.width = caller.width
            wx, wy = caller.to_window(*caller.pos)
            menu.x = wx
            menu.y = wy - menu.height

        Clock.schedule_once(openMenu)

    def _onAudioAbrDropDownMenuButtonRelease(self):

        menu = self.audioAbrDropDownMenu
        caller = self.audioAbrDropDownMenuButton

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
                "ext": self.selectedAudioExt,
                "abr": self.selectedAudioAbr
            }
        )
