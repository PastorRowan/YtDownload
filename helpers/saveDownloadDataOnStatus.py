
import Download

import db

import conversions

def saveDownloadDataOnStatus(downloadData: Download.DownloadData):
    downloadData.bind(
        status=lambda instance, value: db.DownloadData.saveDownload(
            conversions.downloadDataToDownloadDataTable(instance)
        )
    )
