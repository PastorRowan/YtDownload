

from urllib.parse import urlparse

class YTDLPLogger:

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

"""
def getVideoMetaData(
    url: str
) -> Types.ExtractInfoDictResult:

    ydl_metadata_options = {
        # Prevents yt-dlp from using overwritten kivy sys.error object
        "logger": YTDLPLogger(),
        "ffmpeg_location": config.FFMPEG_PATH,
        "js_runtimes": {
            "quickjs": {
                "path": config.QUICK_JS_PATH
            }
        },
        "remote_components": [
            "ejs:github"
        ],
        "outtmpl": r"downloads\%(title)s [%(id)s].%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        # leave default for ffmpeg merge for video and audio format
        # "postprocessors": [],
        "no_color": True,
        "progress_hooks": []
    }

    try:

        with yt_dlp.YoutubeDL(ydl_metadata_options) as ydl_metadata: 

            infoDict: Types.InfoDict = ydl_metadata.extract_info(
                url=url,
                download=False
            )

            return Types.ExtractInfoDictResult(
                {
                    "ok": True,
                    "error_msg": None,
                    "info_dict": infoDict
                }
            )

    except Exception as e:

        errorMsg = str(e)

        return {
            "ok": False,
            "error_msg": errorMsg,
            "info_dict": None
        }
"""
