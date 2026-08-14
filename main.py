
import config
import sys

from update_yt_dlp import update_yt_dlp

import zipfile

yt_dlp_path = str(config.paths.base() / "yt-dlp")

update_yt_dlp(yt_dlp_path)

sys.path.insert(0, str(yt_dlp_path))

import yt_dlp

print("yt_dlp.version.__version__", yt_dlp.version.__version__)
print(yt_dlp.__spec__)
print(yt_dlp.__file__)

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.HomeScreen.HomeScreen import HomeScreen
from screens.SettingsScreen.SettingsScreen import SettingsScreen

import Colors

class Application(MDApp):

    def build(self):

        self.theme_cls.text_color = Colors.black
        self.theme_cls.icon_color = Colors.black

        sm = MDScreenManager()

        sm.add_widget(HomeScreen(name="home"))
        # must add later
        # sm.add_widget(QueueScreen(name="queue"))
        # sm.add_widget(SettingsScreen(name="settings"))

        return sm

if __name__ == "__main__":

    app = Application()

    app.run()
