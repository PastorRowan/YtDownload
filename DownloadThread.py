
import yt_dlp
import config

from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)

def download_videos(urlArray):

    ydl_opts = {
        "ffmpeg_location": config.FFMPEG_PATH,
        "js_runtimes": {
            "deno": {
                "path": config.DENO_PATH
            }
        },
        "remote_components": [
            "ejs:github"
        ],
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "no_color": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urlArray)

class DownloadThread(QThread):

    finished_signal = pyqtSignal()
    success_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, urlArray):
        super().__init__()
        self.urlArray = urlArray

    def run(self):
        try:
            download_videos(self.urlArray)
            self.success_signal.emit("Download successful")
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            self.finished_signal.emit()
