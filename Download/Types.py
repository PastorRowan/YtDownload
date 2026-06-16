
from Download import InfoDict
from typing import TypedDict

class ExtractInfoResult(TypedDict):
    ok: bool
    error_msg: str | None
    video_info: InfoDict.InfoDict | None
