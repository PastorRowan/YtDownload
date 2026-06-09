
from kivy.uix.screenmanager import Screen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton

from kivymd.icon_definitions import md_icons

from kivy.core.window import Window

from screens.HomeScreen.TopBarHBoxLayout import TopBarHBoxLayout
from screens.HomeScreen.ErrorCard import ErrorCard
from screens.HomeScreen.DownloadOptionsDialogue import DownloadOptionsDialogue

import Colors

from threading import Thread
from kivy.clock import Clock
import yt_download

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rootVBoxLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=(50, 50),
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
            on_release=self.onDownloadPromptButtonRelease
        )

        self.rootVBoxLayout.add_widget(self.topBarHBoxLayout)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=125
            )
        )
        self.rootVBoxLayout.add_widget(self.input)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=40
            )
        )
        self.rootVBoxLayout.add_widget(self.errorCard)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, 1),
            )
        )

        self.rootVBoxLayout.add_widget(self.downloadPromptButton)

        self.downloadOptionsDialogue = DownloadOptionsDialogue()

        self.add_widget(self.rootVBoxLayout)

        self.fetchVideoInfoThead = None

    def onDownloadPromptButtonRelease(self, instance):

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        url = self.input.text

        # run download in background thread
        self.fetchVideoInfoThead = Thread(
            target=self.fetchVideoInfo,
            args=(url,),
            daemon=True
        )
        self.fetchVideoInfoThead.start()

    def fetchVideoInfo(self, url):

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        extractInfoResult = yt_download.get_video_info(
            url,
            download=False
        )

        if extractInfoResult["ok"]:
            Clock.schedule_once(
                lambda dt: self.successFetchVideoInfo()
            )
        else:
            Clock.schedule_once(
                lambda dt: self.failFetchVideoInfo(extractInfoResult["error_msg"])
            )

        Clock.schedule_once(
            lambda dt: self.finishFetchVideoInfo()
        )

    def successFetchVideoInfo(self):
        self.errorCard.hide()
        self.downloadOptionsDialogue.open()

    def failFetchVideoInfo(self, message):
        self.errorCard.setBody(message)
        self.errorCard.show()

    def finishFetchVideoInfo(self):

        self.downloadOptionsDialogue.open()

        """
        Clock.schedule_once(
            lambda dt: self.hideDownloadVideoOptionsDialogueForm(),
            2
        )
        """
