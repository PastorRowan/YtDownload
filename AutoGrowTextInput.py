
from kivy.uix.textinput import TextInput

class AutoGrowTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "background_color" not in kwargs:
            self.background_color = (0, 0, 0, 0)

        if "background_normal" not in kwargs:
            self.background_normal = ""

        if "background_active" not in kwargs:
            self.background_active = ""

        if "size_hint_y" not in kwargs:
            self.size_hint_y = None

        self.bind(text=self._resize)

    def _resize(self, *args):
        self.height = self.minimum_height
