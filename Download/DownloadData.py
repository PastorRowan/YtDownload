
from .Types import (
    DownloadType,
    VideoExt,
    ALLOWED_VIDEO_EXTS,
    VideoHeight,
    ALLOWED_VIDEO_HEIGHTS,
    AudioExt,
    ALLOWED_AUDIO_EXTS,
    Abr,
    ALLOWED_ABRS,
    Status
)

import config

from pathlib import Path

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
    ObjectProperty
)

class DownloadData(EventDispatcher):

    DEFAULT_ID: int = -1
    id: int = NumericProperty(DEFAULT_ID)

    DEFAULT_URL: str = ""
    url: str = StringProperty(DEFAULT_URL)

    DEFAULT_FILENAME: str = ""
    fileName: str = StringProperty(DEFAULT_FILENAME)

    downloadType: DownloadType = ObjectProperty(DownloadType.default())

    videoExts = ListProperty(ALLOWED_VIDEO_EXTS)
    videoExt: VideoExt = ObjectProperty(VideoExt.default())

    videoHeights = ListProperty(ALLOWED_VIDEO_HEIGHTS)
    videoHeight: VideoHeight = ObjectProperty(VideoHeight.default())

    audioExts = ListProperty(ALLOWED_AUDIO_EXTS)
    audioExt: AudioExt = ObjectProperty(AudioExt.default())

    abrs = ListProperty(ALLOWED_ABRS)
    abr: Abr = ObjectProperty(Abr.default())

    DEFAULT_TITLE: str = ""
    title: str = StringProperty(DEFAULT_TITLE)

    DEFAULT_CHANNEL: str = ""
    channel: str = StringProperty(DEFAULT_CHANNEL)

    DEFAULT_THUMBNAIL: str = ""
    thumbnail: str = StringProperty(DEFAULT_THUMBNAIL)

    status: Status = ObjectProperty(Status.default())

    ERROR_TYPE = Exception | None
    DEFAULT_ERROR: ERROR_TYPE = None
    error: ERROR_TYPE = ObjectProperty(DEFAULT_ERROR, allownone=True)

    DEFAULT_PROGRESS: float = 0
    progress: float = NumericProperty(DEFAULT_PROGRESS)

    DEFAULT_SPEED: float = 0
    speed: float = NumericProperty(DEFAULT_SPEED)

    DEFAULT_ETA: float = 0
    eta: float = NumericProperty(DEFAULT_ETA)

    DEFAULT_TOTAL_BYTES: float = 0
    totalBytes: int = NumericProperty(DEFAULT_TOTAL_BYTES)

    DEFAULT_DOWNLOADED_BYTES: float = 0
    downloadedBytes: int = NumericProperty(DEFAULT_DOWNLOADED_BYTES)

    downloadLocation: Path = ObjectProperty(config.paths.default_downloads_dir())
