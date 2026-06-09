
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.HomeScreen.HomeScreen import HomeScreen
from screens.SettingsScreen.SettingsScreen import SettingsScreen

import Colors

class Application(MDApp):

    def build(self):

        self.theme_cls.text_color = Colors.black
        self.theme_cls.icon_color = Colors.black

        sm = ScreenManager()

        sm.add_widget(HomeScreen(name="home"))
        # must add later
        # sm.add_widget(QueueScreen(name="queue"))
        # sm.add_widget(SettingsScreen(name="settings"))

        return sm

if __name__ == "__main__":

    app = Application()

    app.run()
