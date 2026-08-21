
from enum import StrEnum

def strEnumToTuple(enum: type[StrEnum]) -> tuple[StrEnum, ...]:
    return tuple(enum)

class DownloadType(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    @classmethod
    def default(cls):
        return cls.VIDEO
ALLOWED_DOWNLOAD_TYPES: tuple[DownloadType] = strEnumToTuple(DownloadType)
print("ALLOWED_DOWNLOAD_TYPES: ", ALLOWED_DOWNLOAD_TYPES)

class VideoExt(StrEnum):
    WEBM = "webm"
    MP4 = "mp4"
    @classmethod
    def default(cls):
        return cls.WEBM
ALLOWED_VIDEO_EXTS: tuple[VideoExt] = strEnumToTuple(VideoExt)
print("ALLOWED_VIDEO_EXTS: ", ALLOWED_VIDEO_EXTS)

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
print("ALLOWED_VIDEO_HEIGHTS: ", ALLOWED_VIDEO_HEIGHTS)

class AudioExt(StrEnum):
    OPUS = "opus"
    M4A = "m4a"
    @classmethod
    def default(cls):
        return cls.OPUS
ALLOWED_AUDIO_EXTS: tuple[AudioExt] = strEnumToTuple(AudioExt)
print("ALLOWED_AUDIO_EXTS: ", ALLOWED_AUDIO_EXTS)

class Abr(StrEnum):
    K192 = "192"
    K160 = "160"
    K128 = "128"
    K86 = "86"
    @classmethod
    def default(cls):
        return cls.K192
ALLOWED_ABRS: tuple[Abr] = strEnumToTuple(Abr)
print("ALLOWED_ABRS: ", ALLOWED_ABRS)

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
print("ALLOWED_DOWNLOAD_STATUSES: ", ALLOWED_DOWNLOAD_STATUSES)
