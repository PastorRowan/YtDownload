
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse

class DownloadButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disable default rectangle background
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)  # fully transparent

        with self.canvas.before:
            Color(1, 0, 0, 1)  # button color
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size
