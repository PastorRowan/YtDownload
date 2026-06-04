
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from download_videos import download_videos

from threading import Thread

from kivy.clock import Clock

class MyLayout(BoxLayout):

    def __init__(self, **kwargs):
    
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.input = TextInput(
            size_hint_y=None,
            height=60
        )

        self.status = TextInput(
            size_hint_y=None,
            height=40,
            readonly=True,
            multiline=False
        )

        self.downloadButton = Button(
            text="Download",
            size_hint_y=None,
            height=50
        )
        self.downloadButton.bind(on_press=self.handle_download_button_press)

        self.downloadThread = None

        self.add_widget(self.input)
        self.add_widget(self.status)
        self.add_widget(self.downloadButton)

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

            download_videos([
                url
            ])

            Clock.schedule_once(
                lambda dt: self.success_download("Downloaded video successfully")
            )

        except Exception as e:

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
        return MyLayout()
