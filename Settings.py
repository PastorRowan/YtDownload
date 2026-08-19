
import config

from pathlib import Path

from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    BooleanProperty
)

from utils import ChooseDirectory

from db.Settings import getSettings, saveSettings

class SettingsClass(EventDispatcher):

    def __init__(self):

        settingsRecord = getSettings()

        if settingsRecord is None:
            raise Exception("Settings record could not be found in the database.")

        self.downloadAudioLanguage = settingsRecord.downloadAudioLanguage
        self.darkMode = settingsRecord.darkMode
        self.videoDownloadDirectory = settingsRecord.videoDownloadDirectory
        self.audioDownloadDirectory = settingsRecord.audioDownloadDirectory

    downloadAudioLanguage: str = StringProperty("en")
    darkMode: bool = BooleanProperty(False)
    videoDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())
    audioDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())

    def setDarkmode(self, newDarkMode: bool) -> None:
        self.darkMode = newDarkMode

    def chooseVideoDownloadDirectory(self) -> None:
        chosenVideoDownloadDirectory = ChooseDirectory(title="Choose video download directory")
        if chosenVideoDownloadDirectory is not None:
            self.videoDownloadDirectory = chosenVideoDownloadDirectory

    def chooseAudioDownloadDirectory(self) -> None:
        chosenAudioDownloadDirectory = ChooseDirectory(title="Choose audio download directory")
        if chosenAudioDownloadDirectory is not None:
            self.chooseAudioDownloadLocation = chosenAudioDownloadDirectory

    def save(self) -> None:
        saveSettings(self)

Settings = SettingsClass()
