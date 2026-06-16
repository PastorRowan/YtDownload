
from typing import (
    TypedDict,
    NotRequired,
    Literal,
    Final
)

from threading import Thread, Event

from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
    BooleanProperty,
    ListProperty
)

class DownloadJob(EventDispatcher):

    DownloadType = Literal[
        "video",
        "audio"
    ]

    ALLOWED_DOWNLOAD_TYPES: tuple[DownloadType, ...] = (
        "video",
        "audio"
    )

    DEFAULT_DOWNLOAD_TYPE: DownloadType = ALLOWED_DOWNLOAD_TYPES[0]

    VideoExt = Literal[
        "mp4",
        "webm"
    ]

    VideoExts = tuple[VideoExt, ...]

    ALLOWED_VIDEO_EXTS: VideoExts = (
        "mp4",
        "webm"
    )

    DEFAULT_VIDEO_EXT: VideoExt = ALLOWED_VIDEO_EXTS[0]

    VideoHeight = Literal[
        "3840",
        "1440",
        "1080",
        "720",
        "480",
        "360"
    ]

    VideoHeights = tuple[VideoHeight, ...]

    ALLOWED_VIDEO_HEIGHTS: VideoHeights = (
        "3840",
        "1440",
        "1080",
        "720",
        "480",
        "360"
    )

    DEFAULT_VIDEO_HEIGHT: VideoHeight = ALLOWED_VIDEO_HEIGHTS[3]

    AudioExt = Literal[
        "m4a",
        "webm",
        "opus"
    ]

    AudioExts = tuple[AudioExt, ...]

    ALLOWED_AUDIO_EXTS: AudioExts = (
        "m4a",
        "webm",
        "opus"
    )

    DEFAULT_AUDIO_EXT: AudioExt = ALLOWED_AUDIO_EXTS[2]

    Abr = Literal[
        "150",
        "120",
        "50",
        "40"
    ]

    Abrs = tuple[Abr, ...]

    ALLOWED_ABRS: Abrs = (
        "150",
        "120",
        "50",
        "40"
    )

    DEFAULT_ABR: Abr = ALLOWED_ABRS[0]

    Status = Literal[
        "queued",
        "downloading",
        "error",
        "paused"
    ]

    STATUS_TYPES: tuple[Status, ...] = (
        "queued",
        "downloading",
        "error",
        "paused"
    )

    DEFAULT_STATUS: Status = STATUS_TYPES[0]

    cancel_event: Event = Event()

    url: str = StringProperty("")

    fileName: str = StringProperty("")
    downloadType: DownloadType = StringProperty(DEFAULT_DOWNLOAD_TYPE, options=ALLOWED_DOWNLOAD_TYPES)

    videoExts: VideoExts = ListProperty(ALLOWED_VIDEO_EXTS)
    videoExt: VideoExt = StringProperty(DEFAULT_VIDEO_EXT, options=ALLOWED_VIDEO_EXTS)

    videoHeights: VideoHeights = ListProperty(ALLOWED_VIDEO_HEIGHTS)
    videoHeight: VideoHeight = StringProperty(DEFAULT_VIDEO_HEIGHT, options=ALLOWED_VIDEO_HEIGHTS)

    audioExts: AudioExts = ListProperty(ALLOWED_AUDIO_EXTS)
    audioExt: AudioExt = StringProperty(DEFAULT_AUDIO_EXT, options=ALLOWED_AUDIO_EXTS)

    abrs: Abrs = ListProperty(ALLOWED_ABRS)
    abr: Abr = StringProperty(DEFAULT_ABR, options=ALLOWED_ABRS)

    title: str = StringProperty("")
    channel: str = StringProperty("")
    thumbnail: str = StringProperty("")

    status: Status = StringProperty("queued", options=STATUS_TYPES)
    error: str = StringProperty("")
    progress: float = NumericProperty(0)
    speed: float = NumericProperty(0)
    eta: int = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
