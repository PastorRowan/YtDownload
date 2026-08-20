
import Download

import db

def downloadDataToDownloadDataTable(downloadData: Download.DownloadData) -> db.DownloadData.DOWNLOAD_DATA_TABLE:
    return db.DownloadData.DOWNLOAD_DATA_TABLE(
        id=downloadData.id,
        url=downloadData.url,
        downloadType=downloadData.downloadType,
        videoExt=downloadData.videoExt,
        videoHeight=downloadData.videoHeight,
        audioExt=downloadData.audioExt,
        abr=downloadData.abr,
        title=downloadData.title,
        channel=downloadData.channel,
        thumbnail=downloadData.thumbnail,
        status=downloadData.status,
        progress=downloadData.progress,
        totalBytes=downloadData.totalBytes,
        downloadedBytes=downloadData.downloadedBytes
    )

def downloadDataTableToDownloadData(downloadDataTable: db.DownloadData.DOWNLOAD_DATA_TABLE) -> Download.DownloadData:
    return Download.DownloadData(
        id=downloadDataTable.id,
        url=downloadDataTable.url,
        downloadType=downloadDataTable.downloadType,
        videoExt=downloadDataTable.videoExt,
        videoHeight=downloadDataTable.videoHeight,
        audioExt=downloadDataTable.audioExt,
        abr=downloadDataTable.abr,
        title=downloadDataTable.title,
        channel=downloadDataTable.channel,
        thumbnail=downloadDataTable.thumbnail,
        status=downloadDataTable.status,
        progress=downloadDataTable.progress,
        totalBytes=downloadDataTable.totalBytes,
        downloadedBytes=downloadDataTable.downloadedBytes
    )
