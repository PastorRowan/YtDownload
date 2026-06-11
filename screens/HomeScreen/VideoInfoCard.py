
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator

from kivy.metrics import dp

class VideoInfoCard(MDCard):

    def __init__(
        self,
        thumbnailLink = "",
        title = "",
        author = "",
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
            source=thumbnailLink,
            fit_mode="fill"
        )

        self.title = MDLabel(
            size_hint=(1, None),
            height=dp(22),
            text=title,
            bold=True
        )

        self.author = MDLabel(
            size_hint=(1, None),
            height=dp(18),
            text=author,
            theme_text_color="Secondary"
        )

        self.progressIndicator = MDLinearProgressIndicator(
            size_hint=(1, None),
            height=dp(3)
        )

        self.add_widget(self.thumbnailImage)
        self.add_widget(self.title)
        self.add_widget(self.author)
        self.add_widget(self.progressIndicator)

        self.bind(width=self._update_image_height)

    def _update_image_height(self, *args):
        self.thumbnailImage.height = self.width * 9 / 16
