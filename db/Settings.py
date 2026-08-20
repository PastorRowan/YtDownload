
from dataclasses import dataclass

from .execute import execute

from pathlib import Path

import sqlite3

@dataclass
class SETTINGS_TABLE:
    downloadAudioLanguage: str
    darkMode: bool
    videoDownloadDirectory: Path
    audioDownloadDirectory: Path

TABLE_NAME = "SETTINGS"

def getSettingsRecordCount() -> int:

    try:
        row = execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME};"
        ).fetchone()

        return row[0]
    except sqlite3.OperationalError:
        return 0

execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
        id INTEGER PRIMARY KEY CHECK (id = 1),
        download_audio_language TEXT NOT NULL,
        dark_mode BOOLEAN NOT NULL,
        video_download_directory TEXT NOT NULL,
        audio_download_directory TEXT NOT NULL
    );
""")

def getSettings() -> SETTINGS_TABLE | None:

    try:

        row = execute(f"""
            SELECT
                download_audio_language,
                dark_mode,
                video_download_directory,
                audio_download_directory
            FROM {TABLE_NAME}
            WHERE id = 1;
        """).fetchone()

        if row is None:
            return None

        return SETTINGS_TABLE(
            downloadAudioLanguage=row[0],
            darkMode=row[1],
            videoDownloadDirectory=Path(row[2]),
            audioDownloadDirectory=Path(row[3])
        )

    except sqlite3.OperationalError:
        return None

def saveSettings(settings: SETTINGS_TABLE) -> None:
    execute(f"""
        INSERT OR REPLACE INTO {TABLE_NAME} (
            id,
            download_audio_language,
            dark_mode,
            video_download_directory,
            audio_download_directory
        ) VALUES (?, ?, ?, ?, ?);
    """, (
        1,
        settings.downloadAudioLanguage,
        settings.darkMode,
        settings.videoDownloadDirectory,
        settings.audioDownloadDirectory
    ))
