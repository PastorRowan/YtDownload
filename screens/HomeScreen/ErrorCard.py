
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

import Colors

class ErrorCard(MDCard):

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("height", 200)
        kwargs.setdefault("opacity", 0)
        kwargs.setdefault("padding", 12)
        kwargs.setdefault("md_bg_color", Colors.errorRedBackground)
        kwargs.setdefault("radius", [10, 10, 10, 10])

        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.errorTopBar = MDBoxLayout(
            size_hint=(1, None),
            orientation="horizontal",
            adaptive_height=True
        )

        self.errorIcon = MDIcon(
            icon="alert-circle",
            theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1),  # red
            size_hint=(None, None),
            width=20,
            height=20,
            halign="left",
            valign="top"
        )

        self.errorTitleLabel = MDLabel(
            text="Could not fetch video info",
            theme_text_color="Custom",
            text_color=Colors.black,
            halign="left",
            valign="top"
        )

        self.errorTopBar.add_widget(self.errorIcon)
        self.errorTopBar.add_widget(
            Widget(
                size_hint=(None, None),
                width=20,
                height=0
            )
        )
        self.errorTopBar.add_widget(self.errorTitleLabel)

        self.errorBodyLabel = MDLabel(
            text="",
            theme_text_color="Custom",
            text_color=Colors.black,
            halign="left",
            valign="top"
        )

        self.add_widget(self.errorTopBar)
        self.add_widget(self.errorBodyLabel)
        self.add_widget(
            Widget(
                size_hint=(1, 1),
            )
        )

    def show(self):
        self.opacity = 1

    def hide(self):
        self.opacity = 0

    def setTitle(self, newTitle):
        self.errorTitleLabel.text = newTitle

    def setBody(self, newBody):
        self.errorBodyLabel.text = newBody
