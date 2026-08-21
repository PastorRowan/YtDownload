
import config

from pathlib import Path

from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    BooleanProperty
)

from utils.ChooseDirectory import ChooseDirectory

from db.Settings import getSettings, saveSettings, SETTINGS_TABLE

class SettingsClass(EventDispatcher):

    downloadAudioLanguage: str = StringProperty("en")
    darkMode: bool = BooleanProperty(False)
    videoDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())
    audioDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())

    def __init__(self):
        super().__init__()

        for name, prop in self.properties().items():
            prop.bind(self, lambda instance, value: self._onPropertyChanged(instance, value))

        settingsRecord = getSettings()

        if settingsRecord is not None:
            self.downloadAudioLanguage = settingsRecord.downloadAudioLanguage
            self.darkMode = settingsRecord.darkMode
            self.videoDownloadDirectory = settingsRecord.videoDownloadDirectory
            self.audioDownloadDirectory = settingsRecord.audioDownloadDirectory

    def setDarkmode(self, newDarkMode: bool) -> None:
        self.darkMode = newDarkMode

    def chooseVideoDownloadDirectory(self) -> None:
        chosenVideoDownloadDirectory = ChooseDirectory(title="Choose video download directory")
        if chosenVideoDownloadDirectory is not None:
            self.videoDownloadDirectory = chosenVideoDownloadDirectory

    def chooseAudioDownloadDirectory(self) -> None:
        chosenAudioDownloadDirectory = ChooseDirectory(title="Choose audio download directory")
        if chosenAudioDownloadDirectory is not None:
            self.audioDownloadDirectory = chosenAudioDownloadDirectory

    def _onPropertyChanged(self, instance, value):
        self.save()

    def save(self) -> None:
        saveSettings(SETTINGS_TABLE(
            downloadAudioLanguage=self.downloadAudioLanguage,
            darkMode=self.darkMode,
            videoDownloadDirectory=self.videoDownloadDirectory,
            audioDownloadDirectory=self.audioDownloadDirectory
        ))

Settings = SettingsClass()
