
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

from download_videos import download_videos

from threading import Thread

from kivy.clock import Clock

from CustomGraphics import CustomGraphics

from yt_dlp.utils import DownloadError

from AutoGrowTextInput import AutoGrowTextInput

from IconButton import IconButton

from DownloadButton import DownloadButton

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
    
        super().__init__(
            orientation="vertical",
            size_hint=(1, 1),
            padding=(50, 50),
            **kwargs
        )

        self.topHalfVBoxLayout = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.settingsCogIconWidget = IconButton(
            source="settings-cog.png",
            size_hint=(None, 1),
            width=60,
            fit_mode="contain"
        )

        self.settingsCogIconWidget.bind(
            on_press=lambda dt: print("settingsCogIconWidget pressed")
        )

        self.videosQueueIconWidget = IconButton(
            source="video-queue.png",
            size_hint=(None, 1),
            width=60,
            fit_mode="contain"
        )

        self.videosQueueIconWidget.bind(
            on_press=lambda dt: print("videosQueueIconWidget pressed")
        )

        self.topBarHBoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50
        )

        self.topBarHBoxLayout.add_widget(self.settingsCogIconWidget)
        self.topBarHBoxLayout.add_widget(
            Widget(
                size_hint=(1, 1),
            )
        )
        self.topBarHBoxLayout.add_widget(self.videosQueueIconWidget)

        self.topHalfVBoxLayout.add_widget(self.topBarHBoxLayout)
        self.topHalfVBoxLayout.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )

        self.bottomHalfVBoxLayout = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.input = AutoGrowTextInput(
            size_hint_x=1
        )

        self.status = AutoGrowTextInput(
            size_hint_x=1,
            readonly=True
        )

        self.bottomBarHBoxLayout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=110
        )

        self.downloadButton = IconButton(
            source="download-icon.png",
            size_hint=(None, None),
            width=80,
            height=80,
            pos_hint={
                "right": 1,
                "y": 1
            }
        )
        CustomGraphics.set_ellipse_bg(
            self.downloadButton,
            
        )
        self.downloadButton.bind(on_press=self.handle_download_button_press)

        self.bottomBarHBoxLayout.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        self.bottomBarHBoxLayout.add_widget(self.downloadButton)

        self.bottomHalfVBoxLayout.add_widget(self.input)
        self.bottomHalfVBoxLayout.add_widget(
            Widget(
                size_hint=(1, None),
                height=20
            )
        )
        self.bottomHalfVBoxLayout.add_widget(self.status)
        self.bottomHalfVBoxLayout.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        self.bottomHalfVBoxLayout.add_widget(self.bottomBarHBoxLayout)

        self.add_widget(self.topHalfVBoxLayout)
        self.add_widget(self.bottomHalfVBoxLayout)

        self.downloadThread = None

    def handle_download_button_press(self, instance):

        """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
        """

        url = self.input.text

        self.status.text = "Starting download..."

        # run download in background thread
        self.downloadThread = Thread(
            target=self.start_download,
            args=(url,),
            daemon=True
        )
        self.downloadThread.start()

    def start_download(self, url):

        try:

            """
https://youtu.be/A7J5eb_VeHE?si=DtRMQuAxVssPOkpi
            """

            download_videos([
                url
            ])

            Clock.schedule_once(
                lambda dt: self.success_download("Downloaded video successfully")
            )

        except DownloadError as e:

            error_msg = str(e)

            Clock.schedule_once(
                lambda dt: self.fail_download(error_msg)
            )

        finally:

            Clock.schedule_once(
                lambda dt: self.finish_download()
            )

    def fail_download(self, message):
        self.status.text = message

    def success_download(self, message):
        self.status.text = message

    def finish_download(self):
        print()

class Application(App):
    def build(self):
        return MainLayout()
