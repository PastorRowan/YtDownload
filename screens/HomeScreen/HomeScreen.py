
from kivy.uix.screenmanager import Screen

from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton

from kivymd.icon_definitions import md_icons

from kivy.core.window import Window

from screens.HomeScreen.VideoInfoCard import VideoInfoCard
from screens.HomeScreen.TopBarHBoxLayout import TopBarHBoxLayout
from screens.HomeScreen.ErrorCard import ErrorCard
from screens.HomeScreen.DownloadOptionsDialogue import (
    DownloadOptionsDialogue,
    SelectedFormats
)

from kivy.clock import Clock
from kivy.metrics import dp

from threading import Thread

import Colors

import CustomGraphics

from DownloadQueue import (
    isUrlValid
)

import InfoDict

Window.clearcolor = Colors.white

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty
)

from pprint import pprint

import config

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView()

        self.rootVBoxLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True,
            padding=(dp(50), dp(50)),
            md_bg_color=Colors.white
        )

        self.topBarHBoxLayout = TopBarHBoxLayout()

        self.input = MDTextField(
            size_hint=(1, None),
            text="",
            hint_text="Video link",
            mode="outlined",
            multiline=True
        )

        self.errorCard = ErrorCard()

        self.downloadPromptButton = MDFabButton(
            icon="download",
            md_bg_color=Colors.turqoise,
            icon_color=Colors.black,
            pos_hint={ "right": 1, "y": 1 }
        )
        self.downloadPromptButton.bind(
            on_release=self._onDownloadPromptButtonRelease
        )

        self.rootVBoxLayout.add_widget(self.topBarHBoxLayout)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(25)
            )
        )
        self.rootVBoxLayout.add_widget(self.input)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(25)
            )
        )
        self.rootVBoxLayout.add_widget(self.errorCard)

        self.rootVBoxLayout.add_widget(self.downloadPromptButton)

        self.downloadOptionsDialogue = DownloadOptionsDialogue(
            url="",
            downloadType="video"
        )

        self.downloadOptionsDialogue.bind(
            on_confirm=self._onDownloadOptionsDialogueConfirm
        )

        self.scroll.add_widget(self.rootVBoxLayout)

        self.add_widget(self.scroll)

        self.bind(

        )

    def _onInput():
        

    def _onDownloadPromptButtonRelease(self, instance):

        TEST_URL = "https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi"

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        url = self.input.text

        url = TEST_URL

        if not isUrlValid(url):
            self.errorCard.title = "Url is invalid"
            self.errorCard.body = f"Url '{url}' is invalid"
            self.errorCard.show = True
        else:
            self.downloadOptionsDialogue.open()

    def _onDownloadOptionsDialogueConfirm(
        self,
        selectedFormats: SelectedFormats
    ):
        print("_onDownloadOptionsDialogueConfirm called: here is the selected formats")
        pprint(selectedFormats)
