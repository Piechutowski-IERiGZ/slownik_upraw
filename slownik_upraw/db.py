import sqlite3 as s3

from csv import reader
from pathlib import Path

import polars as pl




_connection: s3.Connection = s3.connect(":memory:")


def build_schema():
    sql_path = Path(__file__).parent.parent / "SQL/build_tables.sql"
    with open(sql_path, 'r', encoding="utf-8") as file:
        _connection.executescript(file.read())


def load_data():
    file_names = [
        "Dzial",
        "Grupa",
        "Klasa",
        "Kategoria",
        "PodKategoria",
        "Uprawa",
    ]
    for name in file_names:
        csv_path = Path(__file__).parent.parent / 'CSV' / f"{name}.csv"
        with open(csv_path, 'r', encoding="utf-8") as file:
            data = reader(file, delimiter=";")
            headers = next(data)
            sql = f"insert into {name} ({",".join(headers)}) values ({",".join('?' for _ in headers)})"
            _connection.executemany(sql, data)

    _connection.commit()


async def connection() -> s3.Connection:
    return _connection


async def close_connection():
    _connection.close()


