
import config

import sqlite3

_dbPathStr = str(config.paths.base() / "sqlite3_database.db")

_con = sqlite3.connect(_dbPathStr)

_cur = _con.cursor()

def execute(
    query: str,
    parameters: tuple = ()
) -> sqlite3.Cursor:

    cursor = _cur.execute(
        query,
        parameters
    )

    _con.commit()

    return cursor
