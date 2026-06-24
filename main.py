
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.HomeScreen.HomeScreen import HomeScreen
from screens.SettingsScreen.SettingsScreen import SettingsScreen

import Colors

import config

import os

import shutil

from kivy.utils import platform

import subprocess

def setup_android_binaries():
    from android.storage import app_storage_path
    from android import mActivity
    from jnius import autoclass
    from os.path import join
    from os import environ

    app_info = mActivity.getApplicationInfo()

    # /data/app/~~jjR6KAwuKhxTL90VMYY6iw==/ytdownload.ytdownload.ytdownload-5NkpWthjv32EhJE8DfI0Rg==/lib/arm64
    native_lib_dir = app_info.nativeLibraryDir

    print("native_lib_dir: ", native_lib_dir)

    environ["LD_LIBRARY_PATH"] = native_lib_dir 

    user_dir = app_storage_path()

    print("user_dir: ", user_dir)
    """
    executables = config.paths.EXECUTABLES

    for executableName in executables:

        destination = config.paths.executable(executableName)

        if executableName == "qjs":
            result = subprocess.Popen(
                [
                    str(destination),
                    "-e",
                    "console.log('hello world')"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = result.communicate()
            returncode = result.returncode

            print("RETURN CODE:", returncode)
            print("STDOUT:", stdout)
            print("STDERR:", stderr)

        else:
            result = subprocess.Popen(
                [
                    str(destination),
                    "-version"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = result.communicate()
            returncode = result.returncode

            print("RETURN CODE:", returncode)
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
    """

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
