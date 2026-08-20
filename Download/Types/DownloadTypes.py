
from enum import StrEnum

def strEnumToTuple(enum: type[StrEnum]) -> tuple[str, ...]:
    return tuple(value.value for value in enum)

class DownloadType(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    @classmethod
    def default(cls):
        return cls.VIDEO
ALLOWED_DOWNLOAD_TYPES: tuple[DownloadType] = strEnumToTuple(DownloadType)

class VideoExt(StrEnum):
    WEBM = "webm"
    MP4 = "mp4"
    @classmethod
    def default(cls):
        return cls.WEBM
ALLOWED_VIDEO_EXTS: tuple[VideoExt] = strEnumToTuple(VideoExt)

class VideoHeight(StrEnum):
    P2160 = "2160"
    P1440 = "1440"
    P1080 = "1080"
    P720 = "720"
    P480 = "480"
    P360 = "360"
    P144 = "144"
    @classmethod
    def default(cls):
        return cls.P720
ALLOWED_VIDEO_HEIGHTS: tuple[VideoHeight] = strEnumToTuple(VideoHeight)

class AudioExt(StrEnum):
    OPUS = "opus"
    M4A = "m4a"
    @classmethod
    def default(cls):
        return cls.OPUS
ALLOWED_AUDIO_EXTS: tuple[AudioExt] = strEnumToTuple(AudioExt)

class Abr(StrEnum):
    K192 = "192"
    K160 = "160"
    K128 = "128"
    K86 = "86"
    @classmethod
    def default(cls):
        return cls.K192
ALLOWED_ABRS: tuple[Abr] = strEnumToTuple(Abr)

class Status(StrEnum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    FINISHED = "finished"
    ERROR = "error"
    @classmethod
    def default(cls):
        return cls.QUEUED
ALLOWED_DOWNLOAD_STATUSES: tuple[Status] = strEnumToTuple(Status)
