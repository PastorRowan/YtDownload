
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivymd.uix.button import MDFabButton

from kivy.metrics import dp

import Colors

class BottomBarHBoxLayout(MDBoxLayout):

    def __init__(self, **kwargs):

        kwargs.setdefault("md_bg_color", (0, 0, 0, 0))

        super().__init__(
            orientation="horizontal",
            **kwargs
        )

        self.downloadPromptButton = MDFabButton(
            icon="download",
            md_bg_color=Colors.turqoise,
            icon_color=Colors.black,
            pos_hint={
                "right": 1,
                "y": 0
            }
        )

        self.add_widget(
            Widget(
                size_hint=(1, 1),
            )
        )
        self.add_widget(self.downloadPromptButton)
