
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator

from kivy.metrics import dp

from kivy.core.window import Window

class VideoInfoCard(MDBoxLayout):

    def __init__(
        self,
        thumbnailLink = "",
        title = "",
        author = "",
        MAX_WIDTH=dp(600),
        **kwargs
    ):

        self._MAX_WIDTH=MAX_WIDTH

        super().__init__(
            orientation="vertical",
            size_hint=(None, None),
            adaptive_height=True,
            **kwargs
        )

        self.thumbnailImage = AsyncImage(
            size_hint=(1, None),
            source=thumbnailLink,
            fit_mode="contain"
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

        """
        self.bind(
            width=lambda *_: setattr(
                self.thumbnailImage,
                "height",
                self.width * 9 / 16
            )
        )
        """

        # keep 16:9 ratio
        self.bind(width=self._update_image_height)

        # responsive resize when window changes
        Window.bind(size=self._update_width)

    def _update_image_height(self, *args):
        self.thumbnailImage.height = self.width * 9 / 16

    def _update_width(self, *args):
        self.width = min(Window.width - dp(32), self._MAX_WIDTH)
