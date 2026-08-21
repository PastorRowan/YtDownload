
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import Widget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDFabButton
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDActionTopAppBarButton,
    MDTopAppBarTrailingButtonContainer
)

from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    ObjectProperty
)

from screens.HomeScreen.ErrorCard import ErrorCard

from screens.navigateToScreen import navigateToScreen

import Colors

import Download

import Youtube

import db

import helpers

import conversions

Window.clearcolor = Colors.white

class HomeScreen(MDScreen):

    url: str = StringProperty("")
    downloadQueue: Download.Queue = ObjectProperty(Download.Queue())

    topAppBar: MDTopAppBar
    centerScroll: MDScrollView
    rootVBoxLayout: MDBoxLayout
    titleBar: MDBoxLayout
    titleLabel: MDLabel
    inputLabel: MDLabel
    inputTextField: MDTextField
    errorCard: ErrorCard
    downloadQueueView: Download.QueueView
    downloadPromptButton: MDFabButton
    downloadDataOptionsDialogue: Download.DownloadDataOptionsDialogue

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        downloadModels = db.DownloadData.getAllDownloads()

        for downloadModel in downloadModels:
            downloadData = conversions.downloadDataTableToDownloadData(downloadModel)
            helpers.saveDownloadDataOnStatus(downloadData)
            self.downloadQueue.addDownload(downloadData)

        self.topAppBar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="cog",
                    icon_color=Colors.black,
                    on_release=lambda instance: self._onTopAppBarSettingsButtonRelease(instance)
                ),
            ),
            MDTopAppBarTrailingButtonContainer(
                MDActionTopAppBarButton(
                    icon="youtube-subscription",
                    icon_color=Colors.black,
                    on_release=lambda instance: self._onTopAppBarDownloadsButtonRelease(instance)
                ),
            ),
            type="small",
            size_hint=(1, 0.125),
            pos_hint={
                "x": 0,
                "y": 0.875
            },
            padding=(dp(30), dp(30))
        )

        self.centerScroll = MDScrollView(
            size_hint=(1, 0.875),
            pos_hint={
                "x": 0,
                "y": 0
            }
        )

        self.rootVBoxLayout = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True,
            spacing=dp(12),
            padding=(dp(50), dp(50))
        )

        """
        self.rootVBoxLayout.add_widget(
            AsyncImage(
                source="https://i.ytimg.com/vi_webp/JgTdopl9yng/maxresdefault.webp",
                size_hint=(1, None),
                height=dp(200),
                fit_mode="contain"
            )
        )
        """

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

        self.titleBar.add_widget(self.titleLabel)

        self.inputLabel = MDLabel(text="Video link")
        self.inputTextField = MDTextField(
            size_hint=(1, None),
            text=self.url,
            hint_text="Video link",
            mode="outlined",
            multiline=True
        )
        self.inputTextField.bind(
            text=lambda instance, value: self._onInputTextFieldText(instance, value)
        )

        self.errorCard = ErrorCard()

        self.downloadQueueView = Download.QueueView(
            queue=self.downloadQueue
        )

        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(60)
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
        self.rootVBoxLayout.add_widget(self.inputTextField)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(25)
            )
        )
        self.rootVBoxLayout.add_widget(self.errorCard)
        self.rootVBoxLayout.add_widget(self.downloadQueueView)
        self.rootVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=dp(200)
            )
        )

        self.centerScroll.add_widget(self.rootVBoxLayout)

        self.downloadPromptButton = MDFabButton(
            icon="download",
            md_bg_color=Colors.turqoise,
            icon_color=Colors.black,
            pos_hint={
                "right": 0.95,
                "y": 0.05
            }
        )

        self.add_widget(self.topAppBar)
        self.add_widget(self.centerScroll)
        self.add_widget(self.downloadPromptButton)

        self.downloadDataOptionsDialogue = Download.DownloadDataOptionsDialogue()

        self.downloadPromptButton.bind(
            on_release=lambda instance: self._onDownloadPromptButtonRelease(instance)
        )

        self.downloadDataOptionsDialogue.bind(
            on_download_options_confirmed=lambda instance, value: self._onDownloadDataOptionsDialogueConfirmed(instance, value)
        )

    def _onTopAppBarSettingsButtonRelease(self, instance):
        print("_onTopAppBarSettingsButtonRelease called")
        navigateToScreen("settings")

    def _onTopAppBarDownloadsButtonRelease(self, instance):
        print("_onTopAppBarDownloadsButtonRelease called")
        navigateToScreen("downloads")

    def _onInputTextFieldText(self, instance, value):
        url = value
        self.url = url

    def _onDownloadPromptButtonRelease(self, instance):

        url = self.url

        if helpers.isUrlValid(url) is False:
            self.errorCard.title = "Url is invalid"
            self.errorCard.body = f"Url '{url}' is invalid"
            self.errorCard.show = True
            return

        downloadData = Download.DownloadData(url=url)
        self.downloadDataOptionsDialogue.downloadData = downloadData
        self.downloadDataOptionsDialogue.open()

    def _onDownloadDataOptionsDialogueConfirmed(self, instance, value):

        downloadData: Download.DownloadData = value

        videoUrl = downloadData.url

        storedDownloadData = db.DownloadData.getDownloadByUrl(videoUrl)

        print("storedDownloadData: ", storedDownloadData)

        if storedDownloadData is not None:
            downloadData.title = storedDownloadData.title
            downloadData.channel = storedDownloadData.channel
            downloadData.thumbnail = storedDownloadData.thumbnail
        else:

            youtubeVideoMetadata = Youtube.getMetadata(videoUrl)

            print("youtubeVideoMetadata: ", youtubeVideoMetadata)

            if youtubeVideoMetadata is not None:
                downloadData.title = youtubeVideoMetadata.title
                downloadData.channel = youtubeVideoMetadata.author_name
                downloadData.thumbnail = youtubeVideoMetadata.thumbnail_url

        dbId = db.DownloadData.createDownload(conversions.downloadDataToDownloadDataTable(
            downloadData
        ))

        downloadData.id = dbId

        helpers.saveDownloadDataOnStatus(downloadData)

        self.downloadQueue.addDownload(downloadData)
