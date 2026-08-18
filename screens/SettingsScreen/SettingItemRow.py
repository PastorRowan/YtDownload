
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.uix.widget import Widget

from kivy.metrics import dp

class SettingItemRow(MDCard):

    settingIconContainer: MDBoxLayout
    settingIcon: MDIcon
    settingInfoBox: MDBoxLayout
    settingTitle: MDLabel
    settingDescription: MDLabel

    def __init__(
        self,
        title: str,
        description: str,
        icon: str = None,
        on_release=None,
        **kwargs
    ):

        kwargs.setdefault("height", dp(120))

        super().__init__(
            orientation="horizontal",
            size_hint=(1, None),
            size_hint_x=1,
            size_hint_y=None,
            padding=(dp(20), dp(0)),
            **kwargs
        )

        self.settingIconContainer = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(50)
        )

        self.settingIcon = MDIcon(
            icon=icon,
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )

        self.settingIconContainer.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )
        self.settingIconContainer.add_widget(self.settingIcon)
        self.settingIconContainer.add_widget(
            Widget(
                size_hint=(1, 1)
            )
        )

        self.settingInfoBox = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.settingTitle = MDLabel(
            text=title,
            font_style="Title",
            role="large",
            theme_text_color="Primary",
            max_lines=1,
            shorten=True
        )

        self.settingDescription = MDLabel(
            text=description,
            font_style="Body",
            role="medium",
            theme_text_color="Secondary",
            max_lines=2,
            shorten=True
        )

        self.settingInfoBox.add_widget(self.settingTitle)
        self.settingInfoBox.add_widget(self.settingDescription)

        self.add_widget(self.settingIconContainer)
        self.add_widget(self.settingInfoBox)

        if on_release:
            self.bind(
                on_release=lambda instance: on_release(instance)
            )
