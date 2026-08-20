
from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDActionTopAppBarButton
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp, sp

from .SettingItemRow import SettingItemRow
from Settings import Settings

from screens.navigateToScreen import navigateToScreen

import Colors

from kivymd.icon_definitions import md_icons

from pathlib import Path

class SettingsScreen(MDScreen):

    topAppBar: MDTopAppBar
    scroll: MDScrollView
    content: MDBoxLayout
    settingsScreenTitle: MDLabel
    settings: MDBoxLayout
    videoDownloadSetting: SettingItemRow
    audioDownloadSetting: SettingItemRow

    def on_pre_enter(self):
        self.build_settings()

    def build_settings(self):

        self.topAppBar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    icon_color=Colors.black,
                    on_release=lambda instance: self._onTopAppBarBackArrowButtonRelease(instance)
                ),
            ),
            type="small",
            size_hint=(1, 0.125),
            pos_hint={
                "x": 0,
                "y": 0.875
            },
            padding=(dp(30), dp(30))
        )

        self.scroll = MDScrollView(
            size_hint=(1, 0.875),
            pos_hint={
                "x": 0,
                "y": 0
            }
        )

        self.content = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True,
            padding=(dp(50), dp(50))
        )

        self.settingsScreenTitle = MDLabel(
            text="Settings",
            bold=True,
            font_size=sp(15),
            size_hint_y=None,
            height=dp(50)
        )

        self.settings = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            adaptive_height=True
        )

        self.videoDownloadDirectorySettingItemRow = SettingItemRow(
            title="Video download location",
            description=str(Settings.videoDownloadDirectory),
            icon="folder-outline",
            on_release=lambda instance: Settings.chooseVideoDownloadDirectory()
        )

        self.audioDownloadDirectorySettingItemRow = SettingItemRow(
            title="Audio download location",
            description=str(Settings.audioDownloadDirectory),
            icon="folder-outline",
            on_release=lambda instance: Settings.chooseAudioDownloadDirectory()
        )

        self.settings.add_widget(self.videoDownloadDirectorySettingItemRow)
        self.settings.add_widget(self.audioDownloadDirectorySettingItemRow)

        self.content.add_widget(self.settingsScreenTitle)
        self.content.add_widget(self.settings)

        self.scroll.add_widget(self.content)

        self.add_widget(self.topAppBar)
        self.add_widget(self.scroll)

        Settings.bind(
            videoDownloadDirectory=lambda instance, value: self._onSettingsVideoDownloadDirectory(instance, value),
            audioDownloadDirectory=lambda instance, value: self._onSettingsAudioDownloadDirectory(instance, value)
        )

    def _onTopAppBarBackArrowButtonRelease(self, instance):
        navigateToScreen("home")

    def _onSettingsVideoDownloadDirectory(self, instance, value):
        print("_onSettingsVideoDownloadDirectory value:", value)
        videoDownloadDirectory: Path = value
        self.videoDownloadDirectorySettingItemRow.description = str(videoDownloadDirectory)

    def _onSettingsAudioDownloadDirectory(self, instance, value):
        print("_onSettingsAudioDownloadDirectory value:", value)
        audioDownloadDirectory: Path = value
        self.audioDownloadDirectorySettingItemRow.description = str(audioDownloadDirectory)


