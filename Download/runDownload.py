
import config

from Settings import Settings

from pathlib import Path

from kivy.clock import Clock

import yt_dlp
import time
from . import (
    helpers
)
import os

from .DownloadData import DownloadData

from .Types import (
    InfoDict,
    Status
)

class Paused(Exception):
    pass

class Cancelled(Exception):
    pass

def runDownload(downloadData: DownloadData) -> None:

    if downloadData.url == downloadData.DEFAULT_URL:
        raise Exception(f"Failed to run download: url is not assigned-'{downloadData.url}'")

    last_update_time = 0.0
    UPDATE_INTERVAL = 1.5

    def progressHook(d):
        nonlocal last_update_time

        if downloadData.status == Status.PAUSED:
            raise Paused()

        if downloadData.status == Status.CANCELLED:
            raise Cancelled()
        
        now = time.time()

        if d.get("status") == "downloading":

            # throttle UI updates
            if now - last_update_time < UPDATE_INTERVAL:
                return

            last_update_time = now

            downloaded: float = d.get("downloaded_bytes", 0)
            total: float = d.get("total_bytes") or d.get("total_bytes_estimate")
            speed: float = d.get("speed") or 0
            eta: float = d.get("eta") or 0
            infoDict: InfoDict = d.get("info_dict")

            if (
                (downloadData.thumbnail == downloadData.DEFAULT_THUMBNAIL or
                downloadData.title == downloadData.DEFAULT_TITLE or
                downloadData.channel == downloadData.DEFAULT_CHANNEL or
                downloadData.totalBytes == downloadData.DEFAULT_TOTAL_BYTES) and
                infoDict is not None
            ):

                thumbnail = infoDict.get("thumbnail", downloadData.DEFAULT_THUMBNAIL)
                title = infoDict.get("title", downloadData.DEFAULT_TITLE)
                channel = infoDict.get("channel", downloadData.DEFAULT_CHANNEL)
                def updateMetaData(dt):
                    downloadData.thumbnail = thumbnail
                    downloadData.title = title
                    downloadData.channel = channel
                    downloadData.totalBytes = total
                Clock.schedule_once(updateMetaData)

            if downloaded and total:
                progress = downloaded / total
                def updateDownloadProgressAndDownloadedBytes(dt):
                    downloadData.downloadedBytes = downloaded
                    downloadData.progress = progress
                Clock.schedule_once(updateDownloadProgressAndDownloadedBytes)

            def updateDownloadSpeedAndEta(dt):
                downloadData.speed = speed
                downloadData.eta = eta
            Clock.schedule_once(updateDownloadSpeedAndEta)

        elif d.get("status") == "finished":
            def updateDownloadProgressToFinished(dt):
                downloadData.progress = 1.0
            Clock.schedule_once(updateDownloadProgressToFinished)

    try:

        print("str(config.paths.bin_platform()): ", str(config.paths.bin_platform()))

        print("str(config.paths.executable(ffmpeg)): ", str(config.paths.executable("ffmpeg")))

        if downloadData.downloadType == "video":
            downloadData.downloadLocation = Settings.videoDownloadDirectory
        elif downloadData.downloadType == "audio":
            downloadData.downloadLocation = Settings.audioDownloadDirectory

        base_options = {
            "logger": helpers.YTDLPLogger(),
            "outtmpl": os.path.join(
                str(downloadData.downloadLocation),
                "%(title)s [%(id)s].%(ext)s"
            ),
            "cachedir": str(config.paths.ytdlp_cache_dir()),
            "no_color": True,
            "progress_hooks": [progressHook],
            "retries": 10,
            "fragment_retries": 10,
        }

        ydl_download_options = {
            **base_options,
            # Prevents yt-dlp from using overwritten kivy sys.error object
            "ffmpeg_location": str(config.paths.executable("ffmpeg")),
            "js_runtimes": {
                "quickjs": {
                    "path": str(config.paths.executable("qjs"))
                }
            },
            "remote_components": [
                "ejs:github"
            ],
            "concurrent_fragments": 16,
            "downloader": "aria2c",
            "downloader_args": {
                "aria2c": "-x 16 -s 16 -k 1M"
            },
            # leave default for ffmpeg merge for video and audio format
            # "postprocessors": [],
            "postprocessor_args": {
                "ffmpeg": [
                    "-threads",
                    str(os.cpu_count() or 1)
                ]
            }
        }

        if downloadData.downloadType == "video":
            ydl_download_options["format"] = (
                f"bv*[height<={downloadData.videoHeight}]+"
                f"ba*[abr<={downloadData.abr}]"
                f"/b[height<={downloadData.videoHeight}]"
            )
            ydl_download_options["merge_output_format"] = downloadData.videoExt
        elif downloadData.downloadType == "audio":
            print("Audio file chosen")
            print("downloadData.audioExt: ", downloadData.audioExt)
            ydl_download_options["format"] = f"ba*[abr<={downloadData.abr}]/ba"
            ydl_download_options["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": downloadData.audioExt
            }]

        with yt_dlp.YoutubeDL(ydl_download_options) as ydl_download: 

            infoDict: InfoDict = ydl_download.extract_info(
                url=downloadData.url,
                download=True
            )

            def updateStatusToFinished(dt: int) -> None:
                downloadData.status = Status.FINISHED
            Clock.schedule_once(updateStatusToFinished)
        
    except Paused:
        pass
    except Cancelled:
        pass

    except Exception as e:

        error = e

        print(str(error))

        def updateStatusAndError(dt):
            downloadData.status = Status.ERROR
            downloadData.error = error
        Clock.schedule_once(updateStatusAndError)
