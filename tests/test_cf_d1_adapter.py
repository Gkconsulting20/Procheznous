import asyncio
import sqlite3
import unittest

from cf_runtime.d1_adapter import D1Connection


class FakeStatement:
    def __init__(self, database, sql, parameters=()):
        self.database = database
        self.sql = sql
        self.parameters = parameters

    def bind(self, *parameters):
        self.parameters = parameters
        return self

    async def run(self):
        cursor = self.database.connection.execute(self.sql, self.parameters)
        if cursor.description:
            rows = [dict(row) for row in cursor.fetchall()]
        else:
            rows = []
        return {
            "results": rows,
            "meta": {
                "changes": max(cursor.rowcount, 0),
                "last_row_id": cursor.lastrowid,
            },
        }


class FakeD1:
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row

    def prepare(self, sql):
        return FakeStatement(self, sql)

    async def batch(self, statements):
        results = []
        try:
            self.connection.execute("BEGIN")
            for statement in statements:
                cursor = self.connection.execute(statement.sql, statement.parameters)
                results.append({
                    "results": [],
                    "meta": {
                        "changes": max(cursor.rowcount, 0),
                        "last_row_id": cursor.lastrowid,
                    },
                })
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return results


class D1AdapterTests(unittest.TestCase):
    def setUp(self):
        self.database = FakeD1()
        self.connection = D1Connection(
            self.database,
            run_sync_fn=lambda awaitable: asyncio.run(awaitable),
        )
        self.connection.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT UNIQUE)"
        )

    def test_rows_support_sqlite_name_and_index_access(self):
        self.connection.execute(
            "INSERT INTO users (name) VALUES (?)", ("Amina",)
        )
        row = self.connection.execute(
            "SELECT id, name FROM users WHERE name = ?", ("Amina",)
        ).fetchone()

        self.assertEqual(row["name"], "Amina")
        self.assertEqual(row[1], "Amina")
        self.assertEqual(dict(row), {"id": 1, "name": "Amina"})

    def test_fetchall_and_empty_fetchone(self):
        self.connection.executemany(
            "INSERT INTO users (name) VALUES (?)",
            [("Amina",), ("Kossi",)],
        )
        cursor = self.connection.execute("SELECT name FROM users ORDER BY id")

        self.assertEqual([row["name"] for row in cursor.fetchall()], ["Amina", "Kossi"])
        self.assertIsNone(cursor.fetchone())

    def test_constraint_errors_match_sqlite_integrity_error(self):
        self.connection.execute("INSERT INTO users (name) VALUES (?)", ("Amina",))

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("INSERT INTO users (name) VALUES (?)", ("Amina",))


if __name__ == "__main__":
    unittest.main()
