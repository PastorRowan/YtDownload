
from typing import (
    List,
    Set
)

from . import (
    Types
)
from .Job import Job

class InfoDictWrapper():

    infoDict: Types.InfoDict

    def __init__(self, infoDictArg):
        self.infoDict = infoDictArg

    def getAvailableVideoExts(self) -> List[str]:

        ALLOWED_VIDEO_EXTS = Job.ALLOWED_VIDEO_EXTS

        formats = self.infoDict.get("formats") or []

        exts: Set[str] = set()

        for f in formats:
            ext: str = f.get("ext")
            if ext in ALLOWED_VIDEO_EXTS:
                exts.add(str(ext))

        return sorted(exts)

    def getAvailableVideoHeights(self) -> List[str]:

        ALLOWED_VIDEO_HEIGHTS = Job.ALLOWED_VIDEO_HEIGHTS

        formats = self.infoDict.get("formats") or []

        heights: Set[int] = set()

        for f in formats:
            height: int = f.get("height")
            strHeight: str = str(height)
            if strHeight in ALLOWED_VIDEO_HEIGHTS:
                heights.add(str(height))

        sortedHeights: list[int] = sorted(heights)

        sortedStrHeights: list[str] = [str(h) for h in sortedHeights]

        return sortedStrHeights

    def getAvailableAudioExts(self) -> List[str]:

        ALLOWED_AUDIO_EXTS = Job.ALLOWED_AUDIO_EXTS

        formats = self.infoDict.get("formats") or []

        exts: Set[str] = set()

        for f in formats:
            if f.get("acodec") not in (None, "none"):
                ext: str = f.get("ext")
                if ext in ALLOWED_AUDIO_EXTS:
                    exts.add(str(ext))

        return sorted(exts)

    def getAvailableAudioAbrs(self) -> list[str]:

        ALLOWED_ABRS = Job.ALLOWED_ABRS

        formats = self.infoDict.get("formats") or []

        abr_set: Set[str] = set()

        for f in formats:
            abr: float = f.get("abr")
            strAbr: str = str(abr)
            if strAbr in ALLOWED_ABRS:
                abr_set.add(abr)

        sortedAbrs: list[float] = sorted(abr_set)

        sortedStrAbrs: list[str] = [str(a) for a in sortedAbrs]

        return sortedStrAbrs
