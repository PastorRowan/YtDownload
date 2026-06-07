
from kivy.uix.textinput import TextInput

class AutoGrowTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.bind(text=self._resize)

    def _resize(self, *args):
        self.height = self.minimum_height
