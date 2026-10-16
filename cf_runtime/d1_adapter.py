"""Small sqlite3-compatible layer over Cloudflare D1's Python binding.

Flask handlers are synchronous. Cloudflare exposes D1 as an async binding, so
the Worker runtime's ``pyodide.ffi.run_sync`` bridges each D1 operation.
"""

from collections.abc import Mapping
import sqlite3


def _field(value, name, default=None):
    if isinstance(value, Mapping):
        return value.get(name, default)
    return getattr(value, name, default)


def _cloudflare_run_sync(awaitable):
    try:
        from pyodide.ffi import run_sync
    except ImportError as exc:
        raise RuntimeError(
            "Cloudflare D1 can only be used inside a Python Worker runtime."
        ) from exc
    return run_sync(awaitable)


class D1Row(Mapping):
    """Row supporting both SQLite-style integer and column-name lookups."""

    def __init__(self, values):
        self._values = dict(values)
        self._columns = tuple(self._values.keys())

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self._columns[key]
        return self._values[key]

    def __iter__(self):
        return iter(self._columns)

    def __len__(self):
        return len(self._columns)


class D1Cursor:
    def __init__(self, result=None):
        self._result = result or {}
        raw_rows = _field(self._result, "results", []) or []
        self._rows = [
            row if isinstance(row, D1Row) else D1Row(row)
            for row in raw_rows
        ]
        self._position = 0
        self._meta = _field(self._result, "meta", {}) or {}

    @property
    def rowcount(self):
        return _field(self._meta, "changes", len(self._rows))

    @property
    def lastrowid(self):
        return _field(self._meta, "last_row_id")

    def fetchone(self):
        if self._position >= len(self._rows):
            return None
        row = self._rows[self._position]
        self._position += 1
        return row

    def fetchall(self):
        rows = self._rows[self._position:]
        self._position = len(self._rows)
        return rows


class D1Connection:
    """Compatibility subset used by this application's Flask handlers."""

    def __init__(self, database, run_sync_fn=None):
        self._database = database
        self._run_sync = run_sync_fn or _cloudflare_run_sync
        self._last_cursor = D1Cursor()
        self.row_factory = None

    @staticmethod
    def _normalize_parameters(parameters):
        if parameters is None:
            return ()
        if isinstance(parameters, Mapping):
            raise TypeError("Cloudflare D1 supports positional SQL parameters only.")
        if isinstance(parameters, (tuple, list)):
            return tuple(parameters)
        return (parameters,)

    def _prepare(self, sql, parameters=()):
        statement = self._database.prepare(sql)
        if parameters:
            statement = statement.bind(*parameters)
        return statement

    @staticmethod
    def _cursor_for_result(result):
        return D1Cursor(result)

    def execute(self, sql, parameters=()):
        parameters = self._normalize_parameters(parameters)
        try:
            result = self._run_sync(self._prepare(sql, parameters).run())
        except Exception as exc:
            message = str(exc).lower()
            if any(
                marker in message
                for marker in (
                    "constraint failed",
                    "unique constraint",
                    "not null constraint",
                    "foreign key constraint",
                )
            ):
                raise sqlite3.IntegrityError(str(exc)) from exc
            raise
        cursor = self._cursor_for_result(result)
        self._last_cursor = cursor
        return cursor

    def executemany(self, sql, seq_of_parameters):
        statements = [
            self._prepare(sql, self._normalize_parameters(parameters))
            for parameters in seq_of_parameters
        ]
        if not statements:
            self._last_cursor = D1Cursor()
            return self._last_cursor
        results = self._run_sync(self._database.batch(statements))
        last_result = results[-1] if results else {}
        cursor = self._cursor_for_result(last_result)
        self._last_cursor = cursor
        return cursor

    def cursor(self):
        # The SMS service uses a cursor object; its needs are covered by this
        # connection's execute/fetch methods.
        return self

    def fetchone(self):
        return self._last_cursor.fetchone()

    def fetchall(self):
        return self._last_cursor.fetchall()

    @property
    def rowcount(self):
        return self._last_cursor.rowcount

    @property
    def lastrowid(self):
        return self._last_cursor.lastrowid

    def commit(self):
        # D1 statements commit as they run; batch() is used for executemany.
        return None

    def close(self):
        return None

    def rollback(self):
        raise NotImplementedError(
            "D1 statements are committed when executed; use batch() for atomic writes."
        )

    def executescript(self, _sql):
        raise NotImplementedError(
            "Cloudflare schema changes must be applied as D1 migrations."
        )
