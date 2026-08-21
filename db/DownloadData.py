
from dataclasses import dataclass

import config

from .execute import execute

import sqlite3

import Download

@dataclass
class DOWNLOAD_DATA_TABLE:
    id: int
    url: str
    downloadType: Download.Types.DownloadType
    videoExt: Download.Types.VideoExt
    videoHeight: Download.Types.VideoHeight
    audioExt: Download.Types.AudioExt
    abr: Download.Types.Abr
    title: str
    channel: str
    thumbnail: str
    status: Download.Types.Status
    progress: float
    totalBytes: int
    downloadedBytes: int
    createdAt: int = -1

dbPathStr = str(config.paths.base() / "sqlite3_database.db")

def allowedValues(list) -> str:
    return ", ".join(f"'{value}'" for value in list)

allowedDownloadTypesValues = allowedValues(Download.Types.ALLOWED_DOWNLOAD_TYPES)
allowedVideoExtValues = allowedValues(Download.Types.ALLOWED_VIDEO_EXTS)
allowedVideoHeightValues = allowedValues(Download.Types.ALLOWED_VIDEO_HEIGHTS)
allowedAudioExtValues = allowedValues(Download.Types.ALLOWED_AUDIO_EXTS)
allowedAbrValues = allowedValues(Download.Types.ALLOWED_ABRS)
allowedStatusValues = allowedValues(Download.Types.ALLOWED_DOWNLOAD_STATUSES)

TABLE_NAME = "DOWNLOAD_DATA"

execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
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

execute(f"""
    CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_url
    ON {TABLE_NAME}(url);
""")

execute(f"""
    CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_created_at
    ON {TABLE_NAME}(created_at);
""")

def getDownloadCount() -> int | None:

    try:
        row = execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME};"
        ).fetchone()

        return row[0]
    except sqlite3.OperationalError:
        return 0

def getAllDownloads() -> list[DOWNLOAD_DATA_TABLE]:

    try:
        rows = execute(
            f"SELECT * FROM {TABLE_NAME};"
        ).fetchall()

        return [
            DOWNLOAD_DATA_TABLE(*row)
            for row in rows
        ]
    except sqlite3.OperationalError:
        return []

def getDownloadById(id: int) -> DOWNLOAD_DATA_TABLE | None:

    try:
        row = execute(
            f"SELECT * FROM {TABLE_NAME} WHERE id = ?;",
            (id,)
        ).fetchone()

        if row is None:
            return None

        return DOWNLOAD_DATA_TABLE(*row)

    except sqlite3.OperationalError:
        return None

def getDownloadByUrl(url: str) -> DOWNLOAD_DATA_TABLE | None:

    try:
        row = execute(
            f"SELECT * FROM {TABLE_NAME} WHERE url = ?;",
            (url,)
        ).fetchone()

        if row is None:
            return None

        return DOWNLOAD_DATA_TABLE(*row)

    except sqlite3.OperationalError:
        return None

def _updateDownload(downloadTable: DOWNLOAD_DATA_TABLE) -> None:

    try:
        execute(f"""
            UPDATE {TABLE_NAME}
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
            downloadTable.url,
            downloadTable.downloadType,
            downloadTable.videoExt,
            downloadTable.videoHeight,
            downloadTable.audioExt,
            downloadTable.abr,
            downloadTable.title,
            downloadTable.channel,
            downloadTable.thumbnail,
            downloadTable.status,
            downloadTable.progress,
            downloadTable.totalBytes,
            downloadTable.downloadedBytes,
            downloadTable.id
        ))
    except sqlite3.OperationalError:
        print(f"Failed to update download with id '{downloadTable.id}'")

def createDownload(downloadTable: DOWNLOAD_DATA_TABLE) -> int:

    row = execute(f"""
        INSERT INTO {TABLE_NAME} (
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        downloadTable.url,
        downloadTable.downloadType,
        downloadTable.videoExt,
        downloadTable.videoHeight,
        downloadTable.audioExt,
        downloadTable.abr,
        downloadTable.title,
        downloadTable.channel,
        downloadTable.thumbnail,
        downloadTable.status,
        downloadTable.progress,
        downloadTable.totalBytes,
        downloadTable.downloadedBytes
    ))

    return row.lastrowid

def saveDownload(downloadTable: DOWNLOAD_DATA_TABLE) -> None:

    downloadId = downloadTable.id

    if getDownloadById(downloadId):

        _updateDownload(downloadTable)

        return

    elif getDownloadCount() >= config.MAX_DOWNLOADS:

        oldestRow = execute(f"""
            SELECT id
            FROM {TABLE_NAME}
            ORDER BY created_at ASC
            LIMIT 1;
        """).fetchone()

        if oldestRow is None:
            raise RuntimeError(f"Could not find the oldest record even though {TABLE_NAME} table is full.")

        oldestRowId = oldestRow[0]

        downloadTable.id = oldestRowId

        _updateDownload(downloadTable)

        return

    cur = execute(f"""
        INSERT INTO {TABLE_NAME}(
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
        downloadTable.url,
        downloadTable.downloadType,
        downloadTable.videoExt,
        downloadTable.videoHeight,
        downloadTable.audioExt,
        downloadTable.abr,
        downloadTable.title,
        downloadTable.channel,
        downloadTable.thumbnail,
        downloadTable.status,
        downloadTable.progress,
        downloadTable.totalBytes,
        downloadTable.downloadedBytes
    ))

    # Fetch the returned ID
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Insert failed, no ID returned")

    # row is a tuple, id is the first column
    downloadId = row[0]

    downloadTable.id = downloadId
