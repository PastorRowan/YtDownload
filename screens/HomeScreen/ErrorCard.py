
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

from kivy.metrics import dp
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
    BooleanProperty
)

import Colors

DEFAULT_HEIGHT = dp(200)

class ErrorCard(MDCard):
    
    title: str = StringProperty("")
    body: str = StringProperty("")
    show: bool = BooleanProperty(False)

    def __init__(self, **kwargs):

        kwargs.setdefault("size_hint", (1, None))
        kwargs.setdefault("height", DEFAULT_HEIGHT)
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
            text=self.title,
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
            text=self.body,
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

        self.bind(
            title=lambda instance, value: self._onTitle(instance, value),
            body=lambda instance, value: self._onBody(instance, value),
            show=lambda instance, value: self._onShow(instance, value)
        )

        self._onTitle(self, self.title)
        self._onBody(self, self.body)
        self._onShow(self, self.show)

    def _onTitle(self, instance, value):
        self.errorTitleLabel.text = value

    def _onBody(self, instance, value):
        self.errorBodyLabel.text = value

    def _onShow(self, instance, value):
        if value:
            self.height = DEFAULT_HEIGHT
            self.opacity = 1
        else:
            self.height = 0
            self.opacity = 0
