
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.HomeScreen.HomeScreen import HomeScreen
from screens.SettingsScreen.SettingsScreen import SettingsScreen

import Colors

import config

import os

import shutil

from kivy.utils import platform

def setup_android_binaries():
    from android.storage import app_storage_path

    user_dir = app_storage_path()

    executables = config.paths.EXECUTABLES

    for executableName in executables:

        source = config.paths.packaged_executable(executableName)
        destination = config.paths.executable(executableName)

        # Copy only if missing
        if not os.path.exists(destination):
            shutil.copy2(source, destination)

        # Always ensure executable permissions
        os.chmod(destination, 0o755)
    
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
    
    if platform == "android":
        setup_android_binaries()

    app = Application()

    app.run()
