
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator

from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty
)

class VideoInfoCard(MDCard):

    thumbnailLink = StringProperty("")
    title = StringProperty("")
    author = StringProperty("")
    progress = NumericProperty(0.0)
    display = BooleanProperty(False)

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            size_hint=(None, None),
            size_hint_y=None,
            adaptive_height=True,
            **kwargs
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(1, None),
            source=self.thumbnailLink,
            fit_mode="fill"
        )

        self.titleLabel = MDLabel(
            size_hint=(1, None),
            height=dp(22),
            text=self.title,
            bold=True
        )

        self.authorLabel = MDLabel(
            size_hint=(1, None),
            height=dp(18),
            text=self.author,
            theme_text_color="Secondary"
        )

        self.progressIndicator = MDLinearProgressIndicator(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(3)
        )

        self.add_widget(self.thumbnailImage)
        self.add_widget(self.titleLabel)
        self.add_widget(self.authorLabel)
        self.add_widget(self.progressIndicator)

        self.bind(width=self._updateImageHeight)

        self.bind(thumbnailLink=lambda i, v: setattr(self.thumbnailImage, "source", v))
        self.bind(title=lambda i, v: setattr(self.titleLabel, "text", v))
        self.bind(author=lambda i, v: setattr(self.authorLabel, "text", v))
        self.bind(progress=self._on_progress)
        self.bind(display=self._onDisplay)

        self._onDisplay(
            instance=None,
            value=False
        )

    def _updateImageHeight(self, *args) -> None:
        self.thumbnailImage.height = self.width * 9 / 16

    def _on_progress(self, instance, value) -> None:
        self.progressIndicator.value = value

    def _onDisplay(self, instance, value):
        if value:
            self.opacity = 1
            self.disabled = False
            self.height = self.minimum_height
        else:
            self.opacity = 0
            self.disabled = True
            self.height = 0
