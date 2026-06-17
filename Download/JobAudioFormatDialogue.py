
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

class JobAudioFormatDialogue(MDDialog):

    job: Job = ObjectProperty(Job())

    selectedAudioExtIndex: int = NumericProperty(0)
    _audioExtDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    selectedAudioAbrIndex: int = NumericProperty(0)
    _audioAbrDropDownMenuItems: list[DropDownMenuItem] = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.audioExtDropDownMenuButtonText = MDListItemSupportingText(
            text=self.job.audioExts[self.selectedAudioExtIndex]
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
            text=f"{self.job.abrs[self.selectedAudioAbrIndex]}kbps"
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
            on_release=lambda dt: self._onAudioAbrDropDownMenuButtonRelease(dt)
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

        self.job.bind(
            audioExts=lambda instance, value: self._onJobAudioExts(instance, value),
            abrs=lambda instance, value: self._onJobAudioAbrs(instance, value)
        )

        self.bind(
            selectedAudioExtIndex=lambda instance, value: self._onSelectedAudioExtIndex(instance, value),
            selectedAudioAbrIndex=lambda instance, value: self._onSelectedAudioAbrIndex(instance, value)
        )

        self._onJobAudioExts(self, self.job.audioExts)
        self._onJobAudioAbrs(self, self.job.abrs)

        self._onSelectedAudioExtIndex(self, self.selectedAudioExtIndex)
        self._onSelectedAudioAbrIndex(self, self.selectedAudioAbrIndex)

        self.register_event_type("on_confirm")

    def _onJobAudioExts(self, instance, value):

        audioExtsDropDownMenu = self.audioExtDropDownMenu

        self._audioExtDropDownMenuItems.clear()

        def _selectAudioExtIndex(index: int) -> None:
            self.selectedAudioExtIndex = index
            audioExtsDropDownMenu.dismiss()

        for index, audioExt in enumerate(self.job.abrs):
            self._audioExtDropDownMenuItems.append({
                "text": f"{audioExt}kbps",
                "on_release": lambda i=index: _selectAudioExtIndex(i)
            })

    def _onJobAudioAbrs(self, instance, value):

        audioAbrDropDownMenu = self.audioAbrDropDownMenu

        self._audioAbrDropDownMenuItems.clear()

        def _selectAudioAbrIndex(index: int) -> None:
            self.selectedAudioAbrIndex = index
            audioAbrDropDownMenu.dismiss()

        for index, audioAbr in enumerate(self.job.audioExts):
            self._audioAbrDropDownMenuItems.append({
                "text": f"{audioAbr}kbps",
                "on_release": lambda i=index: _selectAudioAbrIndex(i)
            })

    def _onSelectedAudioExtIndex(self, instance, value):
        audioExt = self.job.audioExts[value]
        self.audioExtDropDownMenuButtonText.text = audioExt

    def _onSelectedAudioAbrIndex(self, instance, value) -> None:
        abr = self.job.abrs[value]
        self.audioAbrDropDownMenuButtonText.text = f"{abr}kbps"

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

    def _onAudioAbrDropDownMenuButtonRelease(self, dt):

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

        selectedExt = self.job.audioExts[self.selectedAudioExtIndex]
        selectedAbr = self.job.abrs[self.selectedAudioAbrIndex]

        self.dispatch(
            "on_confirm",
            {
                "ext": selectedExt,
                "abr": selectedAbr
            }
        )
