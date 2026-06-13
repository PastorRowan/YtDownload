
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

class SelectAudioFormatDialogue(MDDialog):

    audioExts = ListProperty([])
    selectedAudioExt = StringProperty("")

    audioAbrs = ListProperty([])
    selectedAudioAbr = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedAudioExt
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

        self.audioExtDropDownMenuItems = []

        def _selectAudioExt(audioExt):
            self.selectedAudioExt = audioExt

        for audioExt in self.audioExts:
            self.audioExtDropDownMenuItems.append({
                "text": audioExt,
                "on_release": lambda dt: _selectAudioExt(audioExt)
            })

        self.audioExtDropDownMenu = MDDropdownMenu(
            caller=self.audioExtDropDownMenuButton, # the widget that opens it
            items=self.audioExtDropDownMenuItems,
            position="bottom",
            hor_growth="right",
            ver_growth="down"
        )

        self.audioAbrDropDownMenuButtonText = MDListItemSupportingText(
            text=self.selectedAudioAbr
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


        self.audioAbrDropDownMenuItems = []

        def _selectAudioAbr(audioAbr):
            self.selectedAudioAbr = audioAbr

        for audioAbr in self.audioAbrs:
            self.audioAbrDropDownMenuItems.append({
                "text": audioAbr,
                "on_release": lambda dt: _selectAudioAbr(audioAbr)
            })

        self.audioAbrDropDownMenu = MDDropdownMenu(
            caller=self.audioAbrDropDownMenuButton, # the widget that opens it
            items=self.audioAbrDropDownMenuItems,
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
