
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
from Download.DownloadJobOptionsDialogue import (
    DownloadJobOptionsDialogue
)

from kivy.clock import Clock
from kivy.metrics import dp

from threading import Thread

import Colors

import CustomGraphics

from Download.DownloadJob import DownloadJob
from Download.DownloadQueue import DownloadQueue
from Download.helpers import getVideoMetaData, isUrlValid

from Download.DownloadQueueView import DownloadQueueView

import Download.InfoDict as InfoDict

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
    fetchVideoMetaDataThread = ObjectProperty(None, allownone=True)

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

        self.downloadQueueView = DownloadQueueView(
            size_hint=(1, None),
            downloadQueue=DownloadQueue
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

        self.downloadJobOptionsDialogue = DownloadJobOptionsDialogue()

        self.scroll.add_widget(self.rootVBoxLayout)

        self.add_widget(self.scroll)

        self.downloadJobOptionsDialogue.bind(
            on_confirm=self._onDownloadOptionsDialogueConfirm
        )

        self.bind(
            fetchVideoMetaDataThread=self._onFetchVideoMetaDataThread
        )

    def _onInputText(self, instance, value):
        self.url = value

    def _onFetchVideoMetaDataThread(self, instance, value):
        self.loadingIndicator.active = value is not None

    def _onDownloadPromptButtonRelease(self, instance):

        TEST_URL = "https://youtu.be/nGbsO71K4g8?si=HsWSZ3NQnedkz-54"

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        url = self.url

        url = TEST_URL

        if not isUrlValid(url):
            self.errorCard.title = "Url is invalid"
            self.errorCard.body = f"Url '{url}' is invalid"
            self.errorCard.show = True
            print(f"Url '{url}' is invalid")
        elif self.fetchVideoMetaDataThread is None:
            print("Starting fetchVideoMetaDataThread")
            self.fetchVideoMetaDataThread = Thread(
                target=self._fetchVideoMetaData,
                args=(url,),
                daemon=True
            )
            self.fetchVideoMetaDataThread.start()
        else:
            print("Extracting metadata already in progress")

    def _fetchVideoMetaData(self, url):

        try:

            print("Starting _fetchVideoMetaData")

            extractInfoResult = getVideoMetaData(url)

            ok = extractInfoResult["ok"]
            errorMsg = extractInfoResult["error_msg"]
            videoInfo = extractInfoResult["video_info"]

            if not ok:
                raise Exception(errorMsg)
            
            def openDialog(dt):
                downloadJob = DownloadJob(
                    url=url,
                    thumbnail=videoInfo["thumbnail"],
                    title=videoInfo["title"],
                    channel=videoInfo["channel"],
                    videoExts=InfoDict.getAvailableVideoExts(videoInfo),
                    videoHeights=InfoDict.getAvailableVideoHeights(videoInfo),
                    audioExts=InfoDict.getAvailableAudioExts(videoInfo),
                    abrs=InfoDict.getAvailableAudioAbrs(videoInfo)
                )
                self.downloadJobOptionsDialogue.downloadJob = downloadJob
                self.downloadJobOptionsDialogue.open()

            Clock.schedule_once(openDialog)

            print("Opened downloadJobOptionsDialogue")

        except Exception as e:
            print(str(e))

            def show_error(dt):
                self.errorCard.title = "Metadata error"
                self.errorCard.body = str(e)
                self.errorCard.show = True

            Clock.schedule_once(show_error)

        finally:
            print("Ending _fetchVideoMetaData")
            def setFetchVideoMetaDataThread(dt):
                self.fetchVideoMetaDataThread = None
            Clock.schedule_once(setFetchVideoMetaDataThread)

    def _onDownloadOptionsDialogueConfirm(
        self,
        selectedFormats
    ):
        print("_onDownloadOptionsDialogueConfirm called: here is the selected formats")
        pprint(selectedFormats)
