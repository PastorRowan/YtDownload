
from kivymd.uix.label import MDIcon

from kivy.uix.behaviors import ButtonBehavior

class MDIconButtonCustom(ButtonBehavior, MDIcon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
