
from dataclasses import dataclass

import config

import sqlite3

import Download

@dataclass
class DOWNLOAD_JOB_TABLE:
    id: int
    downloadType: Download.Job.DownloadType
    videoExt: Download.Job.VideoExt
    videoHeight: Download.Job.VideoHeight
    audioExt: Download.Job.AudioExt
    abr: Download.Job.Abr
    title: str
    channel: str
    thumbnail: str
    status: Download.Job.Status
    progress: float
    totalBytes: int
    downloadedBytes: int

dbPathStr = str(config.paths.base() / "sqlite3_database.db")

con = sqlite3.connect(dbPathStr)

cur = con.cursor()

def allowedValues(list):
    return ", ".join(f"'{value}'" for value in list)

allowedDownloadTypesValues = allowedValues()
allowedStatusValues = allowedValues()

cur.execute(f"""
    CREATE TABLE IF NOT EXIST DOWNLOAD_JOB(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        downloadType TEXT NOT NULL CHECK(role IN {allowedDownloadTypesValues})
    )
""")

def getDownloadJobById(id: int) -> DOWNLOAD_JOB_TABLE:
    return cur.execute("SELECT * FROM DownloadJob WHERE id = ?", (id))
