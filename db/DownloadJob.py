
from dataclasses import dataclass

import config

import sqlite3

import Download

import time

@dataclass
class DOWNLOAD_JOB_TABLE:
    id: int
    url: str
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
    createdAt: int

dbPathStr = str(config.paths.base() / "sqlite3_database.db")

con = sqlite3.connect(dbPathStr)

cur = con.cursor()

def allowedValues(list) -> str:
    return ", ".join(f"'{value}'" for value in list)

allowedDownloadTypesValues = allowedValues(Download.Job.ALLOWED_DOWNLOAD_TYPES)
allowedVideoExtValues = allowedValues(Download.Job.ALLOWED_VIDEO_EXTS)
allowedVideoHeightValues = allowedValues(Download.Job.ALLOWED_VIDEO_HEIGHTS)
allowedAudioExtValues = allowedValues(Download.Job.ALLOWED_AUDIO_EXTS)
allowedAbrValues = allowedValues(Download.Job.ALLOWED_ABRS)
allowedStatusValues = allowedValues(Download.Job.ALLOWED_STATUSES)

cur.execute(f"""
    CREATE TABLE IF NOT EXISTS DOWNLOAD_JOB(
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        download_type TEXT NOT NULL CHECK(download_type IN ({allowedDownloadTypesValues})),
        video_ext TEXT NOT NULL CHECK(video_ext IN ({allowedVideoExtValues})),
        video_height TEXT NOT NULL CHECK(video_height IN ({allowedVideoHeightValues})),
        audio_ext TEXT NOT NULL CHECK(audio_ext IN ({allowedAudioExtValues})),
        abr TEXT NOT NULL CHECK(abr IN ({allowedAbrValues})),
        title TEXT NOT NULL,
        channel TEXT NOT NULL,
        thumbnail TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ({allowedStatusValues})),
        progress REAL NOT NULL,
        total_bytes INTEGER NOT NULL,
        downloaded_bytes INTEGER NOT NULL,
        created_at INTEGER NOT NULL DEFAULT (unixepoch())
    );
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_download_job_url
    ON DOWNLOAD_JOB(url);
""")

cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_created_at
    ON DOWNLOAD_JOB(created_at);
""")

def getDownloadJobCount() -> int:

    row = cur.execute(
        "SELECT COUNT(*) FROM DOWNLOAD_JOB;"
    ).fetchone()

    return row[0]

def getAllDownloadJobs() -> list[DOWNLOAD_JOB_TABLE]:

    rows = cur.execute(
        "SELECT * FROM DOWNLOAD_JOB;"
    ).fetchall()

    return [
        DOWNLOAD_JOB_TABLE(*row)
        for row in rows
    ]

def getDownloadJobById(id: int) -> DOWNLOAD_JOB_TABLE | None:

    row = cur.execute(
        "SELECT * FROM DOWNLOAD_JOB WHERE id = ?;",
        (id,)
    ).fetchone()

    if row is None:
        return None

    return DOWNLOAD_JOB_TABLE(*row)

def getDownloadJobByUrl(url: str) -> DOWNLOAD_JOB_TABLE | None:

    row = cur.execute(
        "SELECT * FROM DOWNLOAD_JOB WHERE url = ?;",
        (url,)
    ).fetchone()

    if row is None:
        return None

    return DOWNLOAD_JOB_TABLE(*row)

def updateDownloadJob(downloadJob: Download.Job) -> None:

    cur.execute(f"""
        UPDATE DOWNLOAD_JOB
        SET
            url = ?,
            download_type = ?,
            video_ext = ?,
            video_height = ?,
            audio_ext = ?,
            abr = ?,
            title = ?,
            channel = ?,
            thumbnail = ?,
            status = ?,
            progress = ?,
            total_bytes = ?,
            downloaded_bytes = ?
        WHERE id = ?;
    """, (
        downloadJob.url,
        downloadJob.downloadType,
        downloadJob.videoExt,
        downloadJob.videoHeight,
        downloadJob.audioExt,
        downloadJob.abr,
        downloadJob.title,
        downloadJob.channel,
        downloadJob.thumbnail,
        downloadJob.status,
        downloadJob.progress,
        downloadJob.totalBytes,
        downloadJob.downloadedBytes,
        downloadJob.id
    ))

def saveDownloadJob(downloadJob: Download.Job) -> None:

    jobId = downloadJob.id

    if getDownloadJobById(jobId):

        updateDownloadJob(downloadJob)

        return

    elif getDownloadJobCount() >= config.MAX_DOWNLOAD_JOBS:

        oldestRow = cur.execute("""
            SELECT id
            FROM DOWNLOAD_JOB
            ORDER BY created_at ASC
            LIMIT 1;
        """).fetchone()

        if oldestRow is None:
            raise RuntimeError("Could not find the oldest record even though DOWNLOAD_JOB table is full.")

        oldestRowId = oldestRow[0]

        downloadJob.id = oldestRowId

        updateDownloadJob(downloadJob)

        return

    cur.execute(f"""
        INSERT INTO DOWNLOAD_JOB(
            url,
            download_type,
            video_ext,
            video_height,
            audio_ext,
            abr,
            title,
            channel,
            thumbnail,
            status,
            progress,
            total_bytes,
            downloaded_bytes
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id;
    """, (
        downloadJob.url,
        downloadJob.downloadType,
        downloadJob.videoExt,
        downloadJob.videoHeight,
        downloadJob.audioExt,
        downloadJob.abr,
        downloadJob.title,
        downloadJob.channel,
        downloadJob.thumbnail,
        downloadJob.status,
        downloadJob.progress,
        downloadJob.totalBytes,
        downloadJob.downloadedBytes
    ))

    # Fetch the returned ID
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Insert failed, no ID returned")

    # row is a tuple, id is the first column
    jobId = row[0]

    downloadJob.id = jobId
