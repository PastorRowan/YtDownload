
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
from screens.HomeScreen.DownloadOptionsDialogue import DownloadOptionsDialogue

from kivy.clock import Clock
from kivy.metrics import dp

from threading import Thread
import DownloadQueue

import Colors

import CustomGraphics

from DownloadQueue import (
    DownloadJob,
    DownloadQueue
)

import InfoDict

Window.clearcolor = Colors.white

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty
)

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

        self.selectedVideoInfoCard = VideoInfoCard(
            thumbnailLink="",
            title="",
            author="",
            pos_hint={ "center_x": 0.5, "center_y": 0.5 }
        )

        CustomGraphics.set_max_width(
            widget=self.selectedVideoInfoCard,
            reference_widget=Window,
            max_width=dp(600),
            margin=dp(100)
        )

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
        self.rootVBoxLayout.add_widget(self.selectedVideoInfoCard)
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

        self.downloadOptionsDialogue = DownloadOptionsDialogue()

        self.scroll.add_widget(self.rootVBoxLayout)

        self.add_widget(self.scroll)

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

        extractInfoResult = DownloadQueue.getVideoInfo(url="https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi")

        if extractInfoResult["ok"]:
            Clock.schedule_once(
                lambda dt: self.successFetchVideoInfo(extractInfoResult["video_info"])
            )
        else:
            Clock.schedule_once(
                lambda dt: self.failFetchVideoInfo(extractInfoResult["error_msg"])
            )

        Clock.schedule_once(
            lambda dt: self.finishFetchVideoInfo()
        )

    def successFetchVideoInfo(self, videoInfo: InfoDict.InfoDict):

        self.errorCard.show = False

        self.downloadOptionsDialogue.availableVideoExts = InfoDict.getAvailableVideoExts(videoInfo)
        self.downloadOptionsDialogue.availableVideoHeights = InfoDict.getAvailableVideoExts(videoInfo)

        self.downloadOptionsDialogue.availableAudioExts = InfoDict.getAvailableAudioExts(videoInfo)
        self.downloadOptionsDialogue.availableAbrs = InfoDict.getAvailableAudioExts(videoInfo)

        self.selectedVideoInfoCard.thumbnailLink = videoInfo["thumbnail"]
        self.selectedVideoInfoCard.title = videoInfo["title"]
        self.selectedVideoInfoCard.author = videoInfo["channel"]
        self.selectedVideoInfoCard.display = True

        self.downloadOptionsDialogue.open()

    def failFetchVideoInfo(self, message):
        self.errorCard.body = message
        self.errorCard.show = True

    def finishFetchVideoInfo(self):

        # self.downloadOptionsDialogue.open()

        """
        Clock.schedule_once(
            lambda dt: self.hideDownloadVideoOptionsDialogueForm(),
            2
        )
        """
