
import config

from pathlib import Path

from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    BooleanProperty
)

from utils import ChooseDirectory

from

class _Settings(EventDispatcher):

    downloadAudioLanguage: str = StringProperty("en")
    darkMode: bool = BooleanProperty(False)
    videoDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())
    audioDownloadDirectory: Path = ObjectProperty(config.paths.default_downloads_dir())

    def chooseVideoDownloadDirectory(self) -> None:
        chosenVideoDownloadDirectory = ChooseDirectory(title="Choose video download directory")
        if chosenVideoDownloadDirectory is not None:
            self.videoDownloadDirectory = chosenVideoDownloadDirectory

    def chooseAudioDownloadDirectory(self) -> None:
        chosenAudioDownloadDirectory = ChooseDirectory(title="Choose audio download directory")
        if chosenAudioDownloadDirectory is not None:
            self.chooseAudioDownloadLocation = chosenAudioDownloadDirectory

    def saveSettings()
        

Settings = _Settings()
