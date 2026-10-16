"""Database connection factory shared by the Replit and Cloudflare runtimes."""

import os
import sqlite3


def get_worker_env():
    """Return the active Cloudflare binding environment inside a Flask request."""
    try:
        from flask import has_request_context, request
    except ImportError:
        return None

    if not has_request_context():
        return None
    return request.environ.get("workers.env")


def connect_database(db_path=None):
    worker_env = get_worker_env()
    if worker_env is not None:
        database = getattr(worker_env, "DB", None)
        if database is None:
            raise RuntimeError("Cloudflare Worker is missing the D1 binding named DB.")
        from cf_runtime.d1_adapter import D1Connection

        return D1Connection(database)

    if db_path is None:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
    elif not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA cache_size = -64000")
    conn.execute("PRAGMA temp_store = MEMORY")
    return conn
