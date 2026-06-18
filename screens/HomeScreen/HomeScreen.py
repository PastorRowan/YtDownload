
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
    StringProperty
)

from screens.HomeScreen.ErrorCard import ErrorCard

import Colors

import Download

Window.clearcolor = Colors.white

class HomeScreen(MDScreen):

    url: str = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self.rootVBoxLayout.add_widget(self.input)
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

        self.downloadJobOptionsDialogue = Download.JobOptionsDialogue()

        self.downloadPromptButton.bind(
            on_release=lambda instance: self._onDownloadPromptButtonRelease(instance)
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
