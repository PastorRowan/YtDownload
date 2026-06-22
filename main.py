
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.HomeScreen.HomeScreen import HomeScreen
from screens.SettingsScreen.SettingsScreen import SettingsScreen

import Colors

import platform

import config

import os

import shutil

from kivy.utils import platform

def setup_android_binaries():
    from android.storage import app_storage_path

    user_dir = app_storage_path()

    binaries = {
        "ffmpeg": (
            config.ANDROID.FFMPEG_APK_BIN_PATH,
            os.path.join(user_dir, "ffmpeg"),
        ),
        "ffprobe": (
            config.ANDROID.FFPROBE_APK_BIN_PATH,
            os.path.join(user_dir, "ffprobe"),
        ),
        "qjs": (
            config.ANDROID.QUICK_JS_APK_BIN_PATH,
            os.path.join(user_dir, "qjs"),
        )
    }

    for _, (src, dst) in binaries.items():
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

        os.chmod(dst, 0o755)

    # Save usable paths back into config if desired
    config.ANDROID.FFMPEG_BIN_PATH = binaries["ffmpeg"][1]
    config.ANDROID.FFPROBE_BIN_PATH = binaries["ffprobe"][1]
    config.ANDROID.QUICK_JS_BIN_PATH = binaries["qjs"][1]
    
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
