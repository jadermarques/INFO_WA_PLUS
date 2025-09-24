from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Iterable, Any

from src.app.config import settings


def _ensure_db_file(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    _ensure_db_file(settings.db_path)
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(schema_sql_path: str) -> None:
    with get_conn() as conn, open(schema_sql_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def execute(query: str, params: Iterable[Any] | None = None) -> int:
    with get_conn() as conn:
        cur = conn.execute(query, tuple(params or ()))
        return cur.lastrowid


def query_all(query: str, params: Iterable[Any] | None = None) -> list[sqlite3.Row]:
    with get_conn() as conn:
        cur = conn.execute(query, tuple(params or ()))
        return cur.fetchall()
