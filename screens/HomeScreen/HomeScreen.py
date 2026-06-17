
from kivy.uix.screenmanager import Screen

from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton
from kivymd.uix.progressindicator import MDCircularProgressIndicator

from kivymd.icon_definitions import md_icons

from kivy.core.window import Window

from screens.HomeScreen.VideoInfoCard import VideoInfoCard
from screens.HomeScreen.TopBarHBoxLayout import TopBarHBoxLayout
from screens.HomeScreen.ErrorCard import ErrorCard

from kivy.clock import Clock
from kivy.metrics import dp

from threading import Thread

import Colors

import Download

Window.clearcolor = Colors.white

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty
)

from pprint import pprint

import config

class HomeScreen(Screen):

    url = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView()

        self.rootVBoxLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True,
            spacing=dp(12),
            padding=(dp(50), dp(50)),
            md_bg_color=Colors.white
        )

        self.topBarHBoxLayout = TopBarHBoxLayout()

        self.titleBar = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(48),
            spacing=dp(10)
        )

        self.titleLabel = MDLabel(
            text="YtDownload",
            bold=True,
            adaptive_size=True
        )

        self.loadingIndicator = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            pos_hint={ "left": 0, "y": 0 },
            active=False
        )

        self.titleBar.add_widget(self.titleLabel)
        self.titleBar.add_widget(self.loadingIndicator)

        self.inputLabel = MDLabel(text="Video link")
        self.input = MDTextField(
            size_hint=(1, None),
            text=self.url,
            hint_text="Video link",
            mode="outlined",
            multiline=True
        )
        self.input.bind(
            text=lambda instance, value: self._onInputText(instance, value)
        )

        self.errorCard = ErrorCard()

        self.downloadQueueView = Download.QueueView(
            queue=Download.Queue
        )

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
        self.rootVBoxLayout.add_widget(self.titleBar)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(25)
            )
        )
        self.rootVBoxLayout.add_widget(self.inputLabel)
        self.rootVBoxLayout.add_widget(self.input)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(25)
            )
        )
        self.rootVBoxLayout.add_widget(self.errorCard)

        self.rootVBoxLayout.add_widget(self.downloadQueueView)

        self.rootVBoxLayout.add_widget(self.downloadPromptButton)

        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(200)
            )
        )

        self.downloadJobOptionsDialogue = Download.JobOptionsDialogue()

        self.scroll.add_widget(self.rootVBoxLayout)

        self.add_widget(self.scroll)

        self.downloadJobOptionsDialogue.bind(
            on_confirm=self._onDownloadOptionsDialogueConfirm
        )

    def _onInputText(self, instance, value):
        self.url = value

    def _onDownloadPromptButtonRelease(self, instance):

        TEST_URL = "https://youtu.be/nGbsO71K4g8?si=HsWSZ3NQnedkz-54"

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        url = self.url

        url = TEST_URL

        if Download.helpers.isUrlValid(url) is False:
            self.errorCard.title = "Url is invalid"
            self.errorCard.body = f"Url '{url}' is invalid"
            self.errorCard.show = True
            print(f"Url '{url}' is invalid")
            return

        job = Download.Job(url=url)
        self.downloadJobOptionsDialogue.job = job
        self.downloadJobOptionsDialogue.open()

    def _onDownloadOptionsDialogueConfirm(
        self,
        selectedFormats
    ):
        print("_onDownloadOptionsDialogueConfirm called: here is the selected formats", selectedFormats)
