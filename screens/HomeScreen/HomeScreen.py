
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
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    ObjectProperty
)

from screens.HomeScreen.ErrorCard import ErrorCard

import Colors

import Download

import Youtube

import db

import helpers

Window.clearcolor = Colors.white

class HomeScreen(MDScreen):

    url: str = StringProperty("")
    downloadJobQueue: Download.Queue = ObjectProperty(Download.Queue())

    topAppBar: MDTopAppBar
    centerScroll: MDScrollView
    rootVBoxLayout: MDBoxLayout
    titleBar: MDBoxLayout
    titleLabel: MDLabel
    inputLabel: MDLabel
    inputTextField: MDTextField
    errorCard: ErrorCard
    downloadJobQueueView: Download.QueueView
    downloadPromptButton: MDFabButton
    downloadJobOptionsDialogue: Download.JobOptionsDialogue

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        jobModels = db.DownloadJob.getAllDownloadJobs()

        for jobModel in jobModels:
            downloadJob = Download.Job(
                id=jobModel.id,
                url=jobModel.url,
                downloadType=jobModel.downloadType,
                videoExt=jobModel.videoExt,
                videoHeight=jobModel.videoHeight,
                audioExt=jobModel.audioExt,
                abr=jobModel.abr,
                title=jobModel.title,
                channel=jobModel.channel,
                thumbnail=jobModel.thumbnail,
                status=jobModel.status,
                progress=jobModel.progress,
                totalBytes=jobModel.totalBytes,
                downloadedBytes=jobModel.downloadedBytes
            )
            self.downloadJobQueue.addJob(downloadJob)

        self.topAppBar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="cog",
                    icon_color=Colors.black
                ),
            ),
            MDTopAppBarTrailingButtonContainer(
                MDActionTopAppBarButton(
                    icon="youtube-subscription",
                    icon_color=Colors.black
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

        self.downloadJobQueueView = Download.QueueView(
            queue=self.downloadJobQueue
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
        self.rootVBoxLayout.add_widget(self.downloadJobQueueView)
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

        self.downloadJobOptionsDialogue = Download.JobOptionsDialogue()

        self.downloadPromptButton.bind(
            on_release=lambda instance: self._onDownloadPromptButtonRelease(instance)
        )

        self.downloadJobOptionsDialogue.bind(
            on_download_options_confirmed=lambda instance, value: self._onDownloadJobOptionsDialogueConfirmed(instance, value)
        )

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

        job = Download.Job(url=url)
        self.downloadJobOptionsDialogue.job = job
        self.downloadJobOptionsDialogue.open()

    def _onDownloadJobOptionsDialogueConfirmed(self, instance, value: Download.Job):

        job = value

        videoUrl = job.url

        storedDownloadJobData = db.getDownloadJobByUrl(videoUrl)

        print("storedDownloadJobData: ", storedDownloadJobData)

        if storedDownloadJobData is not None:
            job.title = storedDownloadJobData.title
            job.channel = storedDownloadJobData.channel
            job.thumbnail = storedDownloadJobData.thumbnail
        else:

            youtubeVideoMetadata = Youtube.getMetadata(videoUrl)

            print("youtubeVideoMetadata: ", youtubeVideoMetadata)

            if youtubeVideoMetadata is not None:
                job.title = youtubeVideoMetadata.title
                job.channel = youtubeVideoMetadata.author_name
                job.thumbnail = youtubeVideoMetadata.thumbnail_url

        job.bind(
            status=lambda instance, value: db.saveDownloadJob(instance)
        )

        self.downloadJobQueue.addJob(job)
