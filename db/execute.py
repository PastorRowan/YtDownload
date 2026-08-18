
import config

import sqlite3

_dbPathStr = str(config.paths.base() / "sqlite3_database.db")

_con = sqlite3.connect(_dbPathStr)

_cur = _con.cursor()

def execute(
    query: str,
    parameters: tuple = ()
) -> sqlite3.Cursor:
    return _cur.execute(
        query,
        parameters
    )
