
import yt_dlp
import config

class YTDLPLogger:

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def download_videos(urlArray):

    ydl_opts = {
        "logger": YTDLPLogger(),
        "ffmpeg_location": config.FFMPEG_PATH,
        "js_runtimes": {
            "deno": {
                "path": config.DENO_PATH
            }
        },
        "remote_components": [
            "ejs:github"
        ],
        "outtmpl": r"downloads\%(title)s [%(id)s].%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "no_color": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urlArray)
