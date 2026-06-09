
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget

from kivymd.uix.button import MDIconButton

import Colors

class TopBarHBoxLayout(MDBoxLayout):

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("height", 50)

        super().__init__(
            orientation="horizontal",
            **kwargs
        )

        self.settingsButton = MDIconButton(
            icon="cog",
            icon_color=Colors.black
        )
        self.settingsButton.bind(
            on_release=lambda arg: print("settingsButton released")
        )

        self.videosQueueButton = MDIconButton(
            icon="youtube-subscription",
            icon_color=Colors.black
        )
        self.videosQueueButton.bind(
            on_release=lambda arg: print("videosQueueButton released")
        )

        self.add_widget(self.settingsButton)
        self.add_widget(
            Widget(
                size_hint=(1, 1),
            )
        )
        self.add_widget(self.videosQueueButton)
